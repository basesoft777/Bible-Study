"""Olvasói pilot: a szakasz-paraméter (--szakasz) feloldása.

Egy szakasz megadása: "1Móz 1:1-2:3" (vers-tartomány, akár fejezethatáron át) vagy "Zsolt 22"
(egész fejezet). A versek listája és sorrendje a konkordancia/Karoli_1908.tsv-ből jön.
A könyvfájlok (Macula, LXX_OS) a megnevezett könyvekhez itt vannak felsorolva; ismeretlen
könyvre a pilot hibával áll meg (nem találgat). A STEPBible-rövidítést (Gen, Psa) a
konkordancia/Konyv_normalizalo_tabla.tsv adja."""
import os
import re
import sys
import tempfile

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GY = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))).replace(chr(92), '/') + '/'

# magyar rövidítés -> (Macula-fájl, LXX_OS-fájl); a pilot eddig ezt a két könyvet vizsgálta
KONYVFAJLOK = {
    '1Móz': ('konkordancia/Macula_heber_Genezis.tsv', 'konkordancia/LXX_OS/genesis.tsv'),
    'Zsolt': ('konkordancia/Macula_heber_Zsoltarok.tsv', 'konkordancia/LXX_OS/psalms-lxx.tsv'),
}
ASCII = {'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ö': 'o', 'ő': 'o', 'ú': 'u', 'ü': 'u', 'ű': 'u'}


def _ascii(s):
    return ''.join(ASCII.get(c.lower(), c) for c in s)


def parse(szakasz):
    """-> (könyv, (f1, v1) vagy None, (f2, v2) vagy None, fejezet vagy None)."""
    m = re.match(r'^\s*(\S+)\s+(\d+)(?::(\d+))?\s*(?:[-–]\s*(?:(\d+):)?(\d+))?\s*$', szakasz)
    if not m:
        raise SystemExit('Érthetetlen --szakasz: %r (példa: "1Móz 1:1-2:3" vagy "Zsolt 22")' % szakasz)
    konyv, f1, v1, f2, v2 = m.groups()
    if v1 is None:
        return konyv, None, None, int(f1)
    f1 = int(f1)
    if v2 is None:
        return konyv, (f1, int(v1)), (f1, int(v1)), None
    return konyv, (f1, int(v1)), (int(f2) if f2 else f1, int(v2)), None


def szakasz_azonosito(szakasz):
    """Fájlnévbe illő azonosító, pl. 1Moz_1_1-2_3, Zsolt_22."""
    return re.sub(r'[^A-Za-z0-9_-]+', '_', _ascii(szakasz.replace(':', '_').replace(' ', '_'))).strip('_')


def szakasz_cim(szakasz):
    """Megjelenítendő szakaszcím a prov-sorokhoz és a laphoz: tartománynál nagykötőjel."""
    konyv, a, b, fej = parse(szakasz)
    if fej is not None:
        return '%s %d' % (konyv, fej)
    if a == b:
        return '%s %d:%d' % (konyv, a[0], a[1])
    if a[0] == b[0]:
        return '%s %d:%d–%d' % (konyv, a[0], a[1], b[1])
    return '%s %d:%d–%d:%d' % (konyv, a[0], a[1], b[0], b[1])


def alap_kimenet(szakasz):
    return os.path.join(tempfile.gettempdir(), 'olvaso_pilot', szakasz_azonosito(szakasz))


def szakasz_versei(szakasz):
    """A szakasz versei a Karoli_1908.tsv sorrendjében. Üres szakaszra hibával áll meg."""
    konyv, a, b, fej = parse(szakasz)
    if konyv not in KONYVFAJLOK:
        raise SystemExit('A könyv (%s) fájljai nincsenek felsorolva a szakasz.py KONYVFAJLOK táblájában.' % konyv)
    kulcsok = []
    with open(GY + 'konkordancia/Karoli_1908.tsv', encoding='utf-8') as fh:
        for s in fh:
            r = s.rstrip('\r\n').split('\t')
            m = re.match(r'^(\S+) (\d+):(\d+)$', r[0]) if r else None
            if m and m.group(1) == konyv:
                kulcsok.append((int(m.group(2)), int(m.group(3)), r[0]))
    if fej is not None:
        out = [k for f, v, k in kulcsok if f == fej]
    else:
        out = [k for f, v, k in kulcsok if a <= (f, v) <= b]
    if not out:
        raise SystemExit('A szakasz (%s) nem ad egyetlen Károli-verset sem.' % szakasz)
    return out


def step_tabla():
    """STEPBible-rövidítés -> magyar rövidítés (Konyv_normalizalo_tabla.tsv, első előfordulás)."""
    d = {}
    with open(GY + 'konkordancia/Konyv_normalizalo_tabla.tsv', encoding='utf-8') as fh:
        next(fh)
        for s in fh:
            r = s.rstrip('\r\n').split('\t')
            if len(r) > 1 and r[0] and not r[0].startswith('#'):
                d.setdefault(r[0], r[1])
    return d
