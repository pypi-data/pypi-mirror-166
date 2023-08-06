import logging
import re

from PIL import Image

from .presmanager import delete_run

CMD_P1_ = CMD_P2_ = '{'
CMD_S1_ = CMD_S2_ = '}'

REPLACE_CHARS_ = {'‘': '\'', '’': '\''}


def cmd_p():
    return f"{CMD_P1_}{CMD_P2_}"


def cmd_s():
    return f"{CMD_S1_}{CMD_S2_}"


def cmd_pattern():
    return re.compile(f"{cmd_p()}(.*?){cmd_s()}")


def img_pattern():
    return f"{cmd_p()}img:(.*?):(.*?){cmd_s()}"


# https://docs.python.org/3/library/functions.html#exec
def interp(cmd, **kwargs):
    if '_r' in kwargs and '_c' in kwargs:
        context = f"[Slide {kwargs['_idx']}, cell at row {kwargs['_r']} and col {kwargs['_c']}]"
    else:
        context = f"[Slide {kwargs['_idx']}]"

    logging.debug("%s Interpreting command '%s'", context, cmd)
    for p, t in REPLACE_CHARS_.items():
        cmd = cmd.replace(p, t)
    try:
        exec(f"_ret={cmd}", None, kwargs)
    except Exception as e:
        logging.warning("%s Error executing:\n%s\n%s", context, cmd, e)
        # raise again or just keep going ?
        # for now just keep going
        return ''
    return kwargs['_ret']


# https://docs.python.org/3/library/re.html
def run_replace(run, **kwargs):
    cmd_pat = cmd_pattern()
    # do not use 'subn' since we want to remove the code before executing
    m = cmd_pat.search(run.text)
    while m is not None:
        # delete code, then interpret and insert where the code used to be
        # prevents issues when the piece of code duplicates the current slide
        run.text = run.text[:m.start()] + run.text[m.end():]
        val = str(interp(m.group(1), **kwargs))
        run.text = run.text[:m.start()] + val + run.text[m.start():]

        m = cmd_pat.search(run.text)


def cell_replace(cell, _cell=None, **kwargs):
    textframe_replace(cell.text_frame, **kwargs, _cell=cell)


def paragraph_replace(par, _p=None, **kwargs):
    for run in par.runs:
        run_replace(run, **kwargs, _p=par)

    idx = 0
    runs = list(par.runs)
    matches = list(cmd_pattern().finditer(par.text))
    for match in matches:
        idcs = -1  # char start
        while idcs == -1:
            rt = runs[idx].text
            if not rt:
                continue
            idcs = rt.find(cmd_p())

            if idcs == -1 and rt[-1] == CMD_P1_ and \
               runs[idx + 1].text[0] == CMD_P2_:
                idcs = len(rt) - 1

            idx += 1

        idrs = idx - 1  # run start

        idce = 1  # char end
        while idce == 1:
            rt = runs[idx].text
            if not rt:
                continue
            idce = rt.find(cmd_s()) + 2

            if idce == 1 and rt[-1] == CMD_S1_ and \
               runs[idx + 1].text[0] == CMD_S2_:
                idx += 2
                idce = 1
                break

            idx += 1

        idre = idx - 1  # run end

        runs[idrs].text = runs[idrs].text[:idcs]
        runs[idre].text = runs[idre].text[idce:]

        idx = idrs + 1

        for i in range(idrs + 1, idre):
            delete_run(runs[i])
        if not runs[idre].text:
            delete_run(runs[idre])

        # delete code, then interpret and insert where the code used to be
        # prevents issues when the piece of code duplicates the current slide
        val = interp(match.group(1), **kwargs, _p=par)
        runs[idrs].text += str(val)

        if not runs[idrs].text:
            delete_run(runs[idrs])
        runs = list(par.runs)


def textframe_replace(tf, _tf=None, **kwargs):
    # match image
    m = re.search(img_pattern(), tf.text)

    if m is None:
        for par in tf.paragraphs:
            paragraph_replace(par, **kwargs, _tf=tf)
        return
        # don't replace across paragraphs

    # insert the image
    slide = tf.part.slide
    sh = tf._element.getparent()
    l, t, w, h = sh.x, sh.y, sh.cx, sh.cy

    modifs = set(m.group(1))
    file = interp(m.group(2), **kwargs, _tf=tf)
    slide.shapes.element.remove(sh)

    if not file:
        # ignore placeholders with undefined image
        return

    context = f"[Slide {kwargs['_idx']}] textframe_replace (image '{file}', modifiers={modifs})"

    try:
        with Image.open(file, mode='r') as im:
            width = im.width
            height = im.height
    except (FileNotFoundError, PermissionError, OSError):
        logging.exception("%s: ", context)
        return

    hm = {'r', 'l', 'c'}
    vm = {'t', 'b', 'm'}
    allm = hm | vm

    if not modifs.issubset(allm):
        logging.info("%s: unknown modifiers %s ignored", context,
                     modifs - allm)

    if len(modifs.intersection(hm)) > 1:
        logging.warning("%s: several horizontal modifiers %s", context,
                        modifs.intersection(hm))
        return
    if len(modifs.intersection(vm)) > 1:
        logging.warning("%s: several vertical modifiers %s", context,
                        modifs.intersection(vm))
        return

    factor = min(w / width, h / height)
    if modifs.isdisjoint(hm):
        width = w
    else:
        # scaling horizontal
        width *= factor
    if modifs.isdisjoint(vm):
        height = h
    else:
        # scaling vertical
        height *= factor

    if 'r' in modifs:
        # aligned right
        l += w - width
    if 'c' in modifs:
        # centered (horizontal)
        l += (w - width) // 2
    if 'b' in modifs:
        # aligned bottom
        t += h - height
    if 'm' in modifs:
        # centered (vertically)
        t += (h - height) // 2

    slide.shapes.add_picture(file, l, t, width=width, height=height)


def row_replace(row, _c=None, **kwargs):
    for _c in range(len(row.cells)):
        cell_replace(row.cells[_c], **kwargs, _c=_c)


def table_replace(table, _r=None, _table=None, **kwargs):
    for _r in range(len(table.rows)):
        row_replace(table.rows[_r], **kwargs, _table=table, _r=_r)


def slide_replace(slide, _sl=None, **kwargs):
    for sh in slide.shapes:
        if sh.has_text_frame:
            textframe_replace(sh.text_frame, **kwargs, _sl=slide)
        if sh.has_table:
            table_replace(sh.table, **kwargs, _sl=slide)


def pres_replace(pres, _idx=None, _pres=None, **kwargs):
    for idx, slide in enumerate(pres.slides):
        slide_replace(slide, **kwargs, _pres=pres, _idx=idx)
