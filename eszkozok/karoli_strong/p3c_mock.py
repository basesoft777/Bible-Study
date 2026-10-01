#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F21.42 — a P3c mérővázak (meres_p3c, koltseg_vetit_p3c, c_diff_p3c) öntesztjeinek
mock-adata. Csak önteszthez; nincs API-hívás, nincs titok.

general(mappa): a futtat.py gépezetével (MockKuldo-alosztály) létrehozza a mappa/valaszok/
{F3V2,F3V2B,F3V3,SONNETV3}.jsonl és a mappa/futasnaplo.tsv fájlt a TELJES 200 verses
mintán, valamint a mappa/arany_teszt.jsonl + arany_teszt.sha256 mock-aranyat (az arany v2
másolata, a hash-fájllal). A válaszok determinisztikusak: az aranyba eső versekre a
mock az arany linkjeit adja, futásonként más hash-szabály szerint módosítva (a módosítás
kapun átmenő); tartós és első-próbás kapuhibák is vannak (l. a visszaadott dict).

regi_kimenetek_hibak(): a régi mérők kimeneteinek bájtazonossága (LF-normalizált sha256 a
BAJTAZONOS táblával szemben); az öntesztek ezt ellenőrzik (a P3c-eszközök nem
módosíthatják a meglévő kimeneteket).
"""

import contextlib
import copy
import io
import json
import os
import shutil
import sys
import tempfile

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import bemenet  # noqa: E402
import futtat  # noqa: E402
import tokenek  # noqa: E402

MOCK_FUTASOK = ('F3V2', 'F3V2B', 'F3V3', 'SONNETV3')
# hash_stabil(igehely) % modulus == ofszet  ->  a mock módosított (nem arany szerinti) választ ad
ELTERES = {'F3V2': (5, 0), 'F3V2B': (5, 2), 'F3V3': (9, 0), 'SONNETV3': (7, 0)}

# A régi mérők kimenetei, amelyeknek bájtra változatlannak kell maradniuk (F21.42 szabály):
# LF-normalizált sha256 (tokenek.sha256_lf) az F21.42 indulásakor (b1426ca/1941e81 alap).
BAJTAZONOS = {
    'f21p/meres_eredmeny.tsv': 'cd698b525f107f52e0d0c2390dd859d801512bd54c4fe6dcb255176eeb4ec549',
    'f21p/meres_v2_eredmeny.tsv': '3d3e8d0afff062349e9f44fa6a7489857a876de13b27d265b8398054c40fa37d',
    'f21p/meres_p3b_eredmeny.tsv': '737fbdf6f6865268e5cac8428efe0455d5b38d125e1cbbb8abd818c42d7744a3',
    'f21p/koltseg_vetites.tsv': 'a5cf8332c211bf81bedc1b16814a090e3b33054248d48ed0f5f75905a1c7acd7',
    'f21p/koltseg_vetites_p3b.tsv': '007b98693ee5ddbd322a262c6e502b09260540510fceb29752bed386c1ea6622',
    'naplok/F21P_meres_v1.md': 'f57adda6fec47a8ff7ec1a9e97091ee67e0b580db893166bc5478786d1a2c2e8',
    'naplok/F21P_meres_v2.md': 'be40d60de201944c0658be040668a5cc087e1a8977bde933157a04584e8dc03a',
    'naplok/F21P_meres_p3b.md': '2136fc152b601bc24ed0894e06916c64a0470594bef3e8feddbe5113b375a2bc',
    'naplok/F21P_C_diff.md': '498fc55718daa05d7a09cd224b4aa50d4aa19afc8c2b627c8c8f6b4f5b3e4e16',
    'naplok/F21P_C_diff_F3V2.md': 'e0614337c699e037b3efb9a02f87036d31be617b6f3bc6b3f9c01d88e457f081',
    'naplok/F21P_C_diff_F3V2B.md': '83de158f19149e12f482c584f8fe19be0fce5d07f9450e51af1dee74a3478488',
}


def regi_kimenetek_hibak(gyoker=None):
    """A régi mérők kimeneteinek bájtazonossága; hibaüzenetek listája (üres = rendben)."""
    gyoker = tokenek.ROOT if gyoker is None else gyoker
    hibak = []
    for rel, vart in BAJTAZONOS.items():
        ut = os.path.join(gyoker, *rel.split('/'))
        if not os.path.exists(ut):
            hibak.append('hiányzik a régi kimenet: %s' % rel)
        elif tokenek.sha256_lf(ut) != vart:
            hibak.append('a régi kimenet megváltozott: %s' % rel)
    return hibak


class P3cMock(futtat.MockKuldo):
    """MockKuldo: az aranyba eső versekre az arany linkjeit adja (futásonként módosítva),
    a többire a MockKuldo szokásos kapun átmenő párosítását; futásszintű kapuhibákkal."""

    def __init__(self, arany, futas_hibas_mindig=None, futas_hibas_elso=None, **kw):
        super().__init__(**kw)
        self.arany = arany
        self.futas = None          # az éppen futó futás (a hívó állítja)
        self.futas_hibas_mindig = {f: set(v) for f, v in (futas_hibas_mindig or {}).items()}
        self.futas_hibas_elso = {f: set(v) for f, v in (futas_hibas_elso or {}).items()}

    @staticmethod
    def _modosit(obj, ig):
        """Kapun átmenő módosítás: az első pár első eredeti-linkje a következő eredetire kötve."""
        d = bemenet.vers_adat(ig)
        ne = len(d['eredeti'])
        if ne < 2 or not obj['parok']:
            return obj
        k0, es = obj['parok'][0]
        uj = (es[0] % ne) + 1
        obj['parok'][0] = [k0, [uj]]
        fedett = {e for _, el in obj['parok'] for e in el}
        obj['forditatlan'] = sorted(set(range(1, ne + 1)) - fedett)
        return obj

    def _valasz_versekre(self, modell_id, igehelyek, masodik, biro=False):
        elemek = []
        mod, ofs = ELTERES.get(self.futas, (0, -1))
        for ig in igehelyek:
            if ig in self.futas_hibas_mindig.get(self.futas, ()) or (
                    ig in self.futas_hibas_elso.get(self.futas, ()) and not masodik):
                obj = self._helyes(ig, False)
                obj['megjegyzes'] = 'H1234'       # Strong-minta: az 5. kapupont fogja
            else:
                if ig in self.arany:
                    g = self.arany[ig]
                    obj = {'vers': ig, 'parok': copy.deepcopy(g['parok']), 'betoldas': list(g['betoldas']),
                           'forditatlan': list(g['forditatlan'])}
                else:
                    obj = self._helyes(ig, False)
                if mod and futtat.hash_stabil(ig) % mod == ofs:
                    obj = self._modosit(obj, ig)
            elemek.append(obj)
        return json.dumps(elemek, ensure_ascii=False)


def general(mappa, arany_forras=None):
    """A mock-adat létrehozása a mappában. Visszaad: dict (kapuhibás versek, aranypéldák, útvonalak)."""
    arany_forras = arany_forras or os.path.join(tokenek.ROOT, 'f21p', 'arany_opus_v2.jsonl')
    arany = {}
    with open(arany_forras, encoding='utf-8') as f:
        for s in f:
            if s.strip():
                o = json.loads(s)
                arany[o['vers']] = o
    minta = futtat.minta_betolt()
    ig_all = [s['igehely'] for s in minta]
    gold = [ig for ig in ig_all if ig in arany]
    assert len(gold) >= 20, len(gold)
    # kapuhibás esetek (aranyversek): S egyedül, F3V3 egyedül, mindkettő tartósan; első-próbás hibák
    s_hiba, c_hiba, mind_hiba = gold[3], gold[7], gold[11]
    hibas_mindig = {'SONNETV3': {s_hiba, mind_hiba}, 'F3V3': {c_hiba, mind_hiba}, 'F3V2': {gold[13]}}
    hibas_elso = {'SONNETV3': {gold[9]}, 'F3V3': {gold[5], ig_all[0] if ig_all[0] not in arany else gold[1]},
                  'F3V2B': {gold[15]}}
    mock = P3cMock(arany, hibas_mindig, hibas_elso)
    os.makedirs(mappa, exist_ok=True)
    tmp_v3 = os.path.join(mappa, 'prompt_v3_teszt.md')
    with open(bemenet.PROMPT_V2_UT, encoding='utf-8') as f:
        v2 = f.read()
    with open(tmp_v3, 'w', encoding='utf-8', newline='\n') as f:
        f.write(v2.replace(bemenet.VEGE, '\nP3c-mock: a prompt_v3 ideiglenes helyettesítője.\n' + bemenet.VEGE))
    eredeti = {f: futtat.FUTASOK[f]['prompt'] for f in futtat.V3_FUTASOK}
    try:
        for f in futtat.V3_FUTASOK:
            futtat.FUTASOK[f]['prompt'] = tmp_v3
        ctx = futtat.Kontextus(mock, 'mock-kulcs-nem-titok', mappa, plafon=futtat.PLAFON_USD)
        for f in MOCK_FUTASOK:
            mock.futas = f
            with contextlib.redirect_stdout(io.StringIO()):
                kod = futtat.futasok_vegrehajt(ctx, [f], minta)
            assert kod == 0, (f, kod)
    finally:
        for f, p in eredeti.items():
            futtat.FUTASOK[f]['prompt'] = p
    arany_ut = os.path.join(mappa, 'arany_teszt.jsonl')
    shutil.copyfile(arany_forras, arany_ut)
    with open(os.path.join(mappa, 'arany_teszt.sha256'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('%s  arany_teszt.jsonl\n' % tokenek.sha256_lf(arany_ut))
    return {'mappa': mappa, 'arany_ut': arany_ut, 'arany_sha': os.path.join(mappa, 'arany_teszt.sha256'),
            'sonnet_hiba': s_hiba, 'c_hiba': c_hiba, 'mind_hiba': mind_hiba,
            'hibas_mindig': hibas_mindig, 'hibas_elso': hibas_elso, 'gold': gold, 'minta': minta}


def ideiglenes(elotag):
    return tempfile.mkdtemp(prefix=elotag)


if __name__ == '__main__':
    print('p3c_mock: csak az öntesztek használják (general, regi_kimenetek_hibak)')
