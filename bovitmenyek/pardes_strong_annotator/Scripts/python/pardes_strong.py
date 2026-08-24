# -*- coding: utf-8 -*-
"""
PaRDeS Strong-annotáció — LibreOffice Writer bővítmény (Python-UNO script).

A konkordancia/inline_strong_megjelenito.py (eszkozok/) parancssoros
referenciaszkript fájl-betöltési, igehely-konverziós és beillesztési
logikájának UNO-adaptációja. A TSV-betöltő és annotate_verse() függvények
tartalmilag változatlanok — csak a fájl-elérési út lett UNO-kompatibilissé
téve (a bővítmény telepítési mappájából olvas, nem a repóból).

Menüből hívva: show_dialog() nyit egy párbeszédablakot, amelyben az
igehely megadható, majd a beillesztés a dokumentum aktuális kijelölése
(csere) vagy kurzorpozíciója (beszúrás) helyén történik.
"""

import os
import csv
import uno
import unohelper
from com.sun.star.awt.MessageBoxButtons import BUTTONS_OK
from com.sun.star.awt.MessageBoxType import MESSAGEBOX, WARNINGBOX, ERRORBOX

EXTENSION_ID = "org.pardes.strong_annotator"

# ---------------------------------------------------------------------------
# Adatelérés — a bővítmény saját "data/" mappájából (a konkordancia/ TSV-k
# másolatai, becsomagolva az .oxt-be build időben, lásd README.md).
# ---------------------------------------------------------------------------

_data_dir_cache = None


def _get_data_dir(ctx):
    global _data_dir_cache
    if _data_dir_cache is not None:
        return _data_dir_cache
    pip = ctx.getValueByName(
        "/singletons/com.sun.star.deployment.PackageInformationProvider"
    )
    ext_url = pip.getPackageLocation(EXTENSION_ID)
    ext_path = uno.fileUrlToSystemPath(ext_url)
    _data_dir_cache = os.path.join(ext_path, "data")
    return _data_dir_cache


# ---------------------------------------------------------------------------
# TSV-betöltés és igehely-konverzió — az inline_strong_megjelenito.py
# logikájának átemelése, változtatás nélkül (csak a path-forrás más).
# ---------------------------------------------------------------------------

def load_tsv(ctx, filename):
    path = os.path.join(_get_data_dir(ctx), filename)
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter='\t')
        header = next(reader)
        rows = [row for row in reader if row and len(row) == len(header)]
    return header, rows


def load_konyv_normalizalo(ctx):
    """STEPBible-rövidítés <-> Magyar rövidítés kétirányú megfeleltetés."""
    _, rows = load_tsv(ctx, 'Konyv_normalizalo_tabla.tsv')
    step_to_hu = {}
    hu_to_step = {}
    for step, hu, _full in rows:
        step_to_hu[step] = hu
        hu_to_step[hu] = step
    return step_to_hu, hu_to_step


def load_karoli_verses(ctx):
    """Magyar igehely (pl. '1Móz 1:1') -> teljes Károli-vers szövege."""
    _, rows = load_tsv(ctx, 'Karoli_1908.tsv')
    return {ref: text for ref, text in rows}


def load_join_table(ctx):
    """STEPBible-natív igehely -> [(Strong-szám, Károli-szó), ...] lista, sorrendben."""
    _, rows = load_tsv(ctx, 'Karoli_Strong_kivonat.tsv')
    by_verse = {}
    for row in rows:
        igehely, strong, karoli_szo = row[0], row[1], row[2]
        by_verse.setdefault(igehely, []).append((strong, karoli_szo))
    return by_verse


def to_step_ref(ref, hu_to_step):
    """'1Móz 1:1' -> 'Gen.1.1'; ha már STEPBible-natív ('Gen.1.1'), változatlanul hagyja."""
    if ' ' not in ref or ':' not in ref:
        return ref
    hu_abbrev, cv = ref.rsplit(' ', 1)
    if hu_abbrev not in hu_to_step:
        return ref
    ch, v = cv.split(':')
    return f"{hu_to_step[hu_abbrev]}.{ch}.{v}"


def to_hu_ref(step_ref, step_to_hu):
    """'Gen.1.1' -> '1Móz 1:1'."""
    parts = step_ref.split('.')
    if len(parts) != 3:
        return step_ref
    step_abbrev, ch, v = parts
    hu_abbrev = step_to_hu.get(step_abbrev)
    if not hu_abbrev:
        return step_ref
    return f"{hu_abbrev} {ch}:{v}"


def annotate_verse(verse_text, join_rows):
    """Beszúrja a Strong-számokat a Károli-vers szövegébe, pozíció szerint hátulról előre."""
    positioned = []
    for strong, karoli_szo in join_rows:
        idx = verse_text.find(karoli_szo)
        if idx == -1:
            # Nem található szó szerint a versben — defenzíven kihagyjuk (lásd a
            # parancssoros referenciaszkript azonos logikáját).
            continue
        positioned.append((idx, karoli_szo, strong))

    positioned.sort(key=lambda x: x[0], reverse=True)
    result = verse_text
    for idx, karoli_szo, strong in positioned:
        insert_at = idx + len(karoli_szo)
        result = f"{result[:insert_at]}[{strong}]{result[insert_at:]}"
    return result


class VerseLookupError(Exception):
    pass


def annotate_ref(ctx, raw_ref, karoli_verses, join_table, step_to_hu, hu_to_step):
    """Egyetlen igehely (bármely formátumban) -> annotált Károli-szöveg, vagy VerseLookupError."""
    step_ref = to_step_ref(raw_ref.strip(), hu_to_step)
    hu_ref = to_hu_ref(step_ref, step_to_hu)
    verse_text = karoli_verses.get(hu_ref)
    if verse_text is None:
        raise VerseLookupError(
            f"Nincs Károli-szöveg ehhez az igehelyhez: {hu_ref} ({step_ref})"
        )
    join_rows = join_table.get(step_ref, [])
    return hu_ref, step_ref, annotate_verse(verse_text, join_rows), bool(join_rows)


def list_chapter_step_refs(konyv, fejezet, karoli_verses, join_table, step_to_hu):
    """Egy teljes fejezet igehelyeinek (STEPBible-natív) listája, versszám szerint rendezve."""
    prefix = f"{konyv}.{fejezet}."
    verses = sorted(
        {int(k.split('.')[2]) for k in join_table if k.startswith(prefix)}
    )
    if not verses:
        hu_abbrev = step_to_hu.get(konyv, konyv)
        verses = sorted(
            int(ref.rsplit(':', 1)[1])
            for ref in karoli_verses
            if ref.startswith(f"{hu_abbrev} {fejezet}:")
        )
    return [f"{prefix}{v}" for v in verses]


# ---------------------------------------------------------------------------
# UNO segédfüggvények
# ---------------------------------------------------------------------------

def _msgbox(ctx, parent_peer, text, title, box_type=MESSAGEBOX):
    smgr = ctx.ServiceManager
    toolkit = smgr.createInstanceWithContext("com.sun.star.awt.Toolkit", ctx)
    rect = uno.createUnoStruct("com.sun.star.awt.Rectangle")
    box = toolkit.createMessageBox(parent_peer, box_type, BUTTONS_OK, title, text)
    box.execute()


def _insert_multiline(text_obj, cursor, s):
    lines = s.split('\n')
    for i, line in enumerate(lines):
        if i > 0:
            text_obj.insertControlCharacter(
                cursor, uno.getConstantByName(
                    "com.sun.star.text.ControlCharacter.PARAGRAPH_BREAK"
                ), False
            )
        text_obj.insertString(cursor, line, False)


# ---------------------------------------------------------------------------
# Párbeszédablak
# ---------------------------------------------------------------------------

def _build_dialog(ctx, initial_ref):
    smgr = ctx.ServiceManager
    dialog_model = smgr.createInstanceWithContext(
        "com.sun.star.awt.UnoControlDialogModel", ctx
    )
    dialog_model.PositionX = 100
    dialog_model.PositionY = 100
    dialog_model.Width = 220
    dialog_model.Height = 110
    dialog_model.Title = "PaRDeS Strong-annotáció"

    def add(name, service, x, y, w, h, **props):
        model = dialog_model.createInstance(service)
        model.PositionX = x
        model.PositionY = y
        model.Width = w
        model.Height = h
        for k, v in props.items():
            setattr(model, k, v)
        dialog_model.insertByName(name, model)
        return model

    add("lblRef", "com.sun.star.awt.UnoControlFixedTextModel", 10, 8, 200, 10,
        Label='Igehely (pl. "1Móz 1:1" vagy "Gen.1.1"):')
    add("txtRef", "com.sun.star.awt.UnoControlEditModel", 10, 19, 200, 14,
        Text=initial_ref or "")

    add("chkChapter", "com.sun.star.awt.UnoControlCheckBoxModel", 10, 40, 200, 12,
        Label="Teljes fejezet beszúrása (könyv-rövidítés + fejezetszám):")

    add("lblKonyv", "com.sun.star.awt.UnoControlFixedTextModel", 20, 56, 60, 10,
        Label="Könyv (pl. Gen):")
    add("txtKonyv", "com.sun.star.awt.UnoControlEditModel", 85, 54, 50, 14)

    add("lblFejezet", "com.sun.star.awt.UnoControlFixedTextModel", 145, 56, 30, 10,
        Label="Fejezet:")
    add("txtFejezet", "com.sun.star.awt.UnoControlEditModel", 178, 54, 32, 14)

    add("btnOk", "com.sun.star.awt.UnoControlButtonModel", 60, 82, 50, 16,
        Label="OK", DefaultButton=True, PushButtonType=1)
    add("btnCancel", "com.sun.star.awt.UnoControlButtonModel", 115, 82, 50, 16,
        Label="Mégse", PushButtonType=2)

    dialog = smgr.createInstanceWithContext("com.sun.star.awt.UnoControlDialog", ctx)
    dialog.setModel(dialog_model)
    toolkit = smgr.createInstanceWithContext("com.sun.star.awt.Toolkit", ctx)
    dialog.setVisible(False)
    dialog.createPeer(toolkit, None)
    return dialog


def _get_selected_text(doc):
    try:
        controller = doc.getCurrentController()
        sel = controller.getSelection()
        if sel is not None and sel.getCount() > 0:
            s = sel.getByIndex(0).getString().strip()
            return s
    except Exception:
        pass
    return ""


def show_dialog(*args):
    ctx = XSCRIPTCONTEXT.getComponentContext()
    doc = XSCRIPTCONTEXT.getDocument()

    initial_ref = _get_selected_text(doc)
    dialog = _build_dialog(ctx, initial_ref)
    parent_peer = doc.getCurrentController().getFrame().getContainerWindow()

    try:
        result = dialog.execute()
        if result != 1:  # nem OK
            return

        ref_text = dialog.getControl("txtRef").getModel().Text.strip()
        chapter_mode = bool(dialog.getControl("chkChapter").getState())
        konyv = dialog.getControl("txtKonyv").getModel().Text.strip()
        fejezet_raw = dialog.getControl("txtFejezet").getModel().Text.strip()
    finally:
        dialog.dispose()

    try:
        step_to_hu, hu_to_step = load_konyv_normalizalo(ctx)
        karoli_verses = load_karoli_verses(ctx)
        join_table = load_join_table(ctx)
    except OSError as e:
        _msgbox(
            ctx, parent_peer,
            f"Nem sikerült betölteni a konkordancia-adatokat a bővítményből:\n{e}",
            "PaRDeS Strong-annotáció — hiba", ERRORBOX,
        )
        return

    step_refs = []
    if chapter_mode:
        if not konyv or not fejezet_raw:
            _msgbox(
                ctx, parent_peer,
                "Teljes fejezet módhoz add meg a könyv-rövidítést (pl. \"Gen\") "
                "és a fejezetszámot is.",
                "PaRDeS Strong-annotáció", WARNINGBOX,
            )
            return
        try:
            fejezet = int(fejezet_raw)
        except ValueError:
            _msgbox(
                ctx, parent_peer,
                f'A fejezetszám nem érvényes egész szám: "{fejezet_raw}"',
                "PaRDeS Strong-annotáció", WARNINGBOX,
            )
            return
        step_refs = list_chapter_step_refs(konyv, fejezet, karoli_verses, join_table, step_to_hu)
        if not step_refs:
            _msgbox(
                ctx, parent_peer,
                f"Nem található vers a(z) {konyv} {fejezet}. fejezethez.",
                "PaRDeS Strong-annotáció", WARNINGBOX,
            )
            return
    else:
        if not ref_text:
            _msgbox(
                ctx, parent_peer,
                "Add meg az igehelyet (pl. \"1Móz 1:1\" vagy \"Gen.1.1\").",
                "PaRDeS Strong-annotáció", WARNINGBOX,
            )
            return
        step_refs = [ref_text]

    output_lines = []
    errors = []
    for raw in step_refs:
        try:
            hu_ref, step_ref, annotated, has_strong = annotate_ref(
                ctx, raw, karoli_verses, join_table, step_to_hu, hu_to_step
            )
        except VerseLookupError as e:
            errors.append(str(e))
            continue
        if chapter_mode:
            verse_num = step_ref.rsplit('.', 1)[1]
            output_lines.append(f"{verse_num}. {annotated}")
        else:
            output_lines.append(annotated)

    if errors and not output_lines:
        _msgbox(
            ctx, parent_peer,
            "HIBA:\n" + "\n".join(errors),
            "PaRDeS Strong-annotáció — hiba", ERRORBOX,
        )
        return

    if errors:
        _msgbox(
            ctx, parent_peer,
            "Néhány igehely kimaradt (nincs Károli-szöveg hozzá):\n" + "\n".join(errors),
            "PaRDeS Strong-annotáció — figyelmeztetés", WARNINGBOX,
        )

    result_text = "\n".join(output_lines)
    text_obj = doc.getText()
    view_cursor = doc.getCurrentController().getViewCursor()
    _insert_multiline(text_obj, view_cursor, result_text)


g_exportedScripts = (show_dialog,)
