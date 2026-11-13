"""lapgen.szamitas.szotari_gerinc — a „Jelentés (a szó)” oszlop: egy szó jelentéscímkéje egy versen.

Elsőbbség: ha a szótár maga idézi a helyet, és az útja a szerkesztői hozzárendelés alá esik, a finomabb út
címkéje áll; ha a kettő közül egyik sem esik a másik alá, a futás megáll (GerincHiba), választás nélkül.
A címke a szóról szól; a hely motívumbeli funkciója külön oszlop.

A kimenet szerkezet: a címke, a szakasz jele és az indokok sora. Minden indok kétféleképp jelenik meg: a
megjelenítő a fajtájából és a mezőiből mondatot választ a sablontáblából, a `prov` mezője pedig a teljes belső
leírás, amely csak megjegyzésbe kerül.
"""
import dataclasses
from typing import Optional, Tuple

from lapgen.bemenet import gerinc as G
from lapgen.ertekek import IndokFajta, JelentesFajta
from lapgen.szoveg import Igehely, Kulcs, Lathato, Proveniencia, Strong, idezet, prov, prov_fuz, proza

_TAGOLATLAN_KULCS = 'tagolatlan'


@dataclasses.dataclass(frozen=True)
class Indok:
    """Miért ez a címke áll a soron (vagy miért nincs címke)."""
    fajta: IndokFajta
    prov: Proveniencia
    szakaszok: Tuple[Lathato, ...] = ()        # a szótár szakaszjelei prózai alakban („1.”, „Qal”)
    szotar: Optional[Kulcs] = None             # a szótár, amelynek a tagolása szerint a hozzárendelés áll
    jel: Optional[Lathato] = None              # a szakasz jele a cella alakjában („1”, „Qal”); fejnél hiányzik
    fej: bool = False                          # a hozzárendelés a szócikk fejére mutat
    idezett: Optional[Lathato] = None          # a forrás hibás alakja (sajtóhiba)
    kezdo_vers: Optional[Igehely] = None       # verstartomány kezdete
    veg: int = 0                               # verstartomány utolsó verse
    darab: int = 0                             # hányszor áll a szó a versben; Thayer-jelentés száma


@dataclasses.dataclass(frozen=True)
class TokenJelentes:
    """Egy szó jelentéscellája: a fajta, a megjelenő címke vagy glossza, a jel és az indokok."""
    strong: Strong
    fajta: JelentesFajta
    cimke: Optional[Lathato]
    jel: Optional[Lathato]
    indokok: Tuple[Indok, ...]
    cimke_cella: Optional[Lathato] = None      # a címke cellakezdő alakja (adat), ha a cella vele kezdődik


def _proza_jelek(g, strong, jelek):
    """Szakaszjelek prózai alakban: a puszta szám sorszámnév-pontot kap („4” → „4.”)."""
    return tuple(idezet(g.jel_szoveg(G.pontos_jel(j), strong)) for j in jelek)


def _belso_jelek(jelek, nevelo=True):
    """A szakaszjelek belső (megjegyzésbe kerülő) alakja névelővel: „a 4.”, „a Qal 2.c”, „a 3., 4.”."""
    pontos = [G.pontos_jel(j) for j in jelek]
    if not nevelo:
        return prov_fuz(', ', pontos)
    return prov('{} {}', G.nevelo(pontos[0]), prov_fuz(', ', pontos))


def _cimke_token(g, f, szotar, strong, jelentes_szam, vers, kutatoi_token):
    """Egy szó címkéje egy versen: (választott kulcs vagy None, a jel belső alakja, indokok)."""
    st = strong.kod
    kulcs, minosito = G.kutatoi_kulcs(jelentes_szam) if kutatoi_token else ('', '')
    kut_k = g.kutatoi_szakasz(szotar, st, kulcs) if kulcs else None
    cimketabla, peldatabla = f.utvonal('B16'), f.utvonal('B19')
    if kutatoi_token and kulcs and kut_k is None:
        fajta = IndokFajta.TAGOLATLAN if kulcs == _TAGOLATLAN_KULCS else IndokFajta.NINCS_LEKEPEZVE
        return None, '', [Indok(fajta, prov('a kutatói jelentésszám („{}”) nincs leképezve a {} tagolására (`{}`)',
                                            kulcs, szotar, cimketabla))]

    def kjel(k):
        return g.kulcs_jel(szotar, st, k)

    peldak, nem_azon = [], []
    for r, bdb_id, ok in (g.bdb_peldak(st, vers.kod) if szotar == G.SZOTAR_BDB else []):
        if bdb_id is None:
            nem_azon.append(Indok(IndokFajta.NEM_AZONOSITHATO, prov(
                'a BDB a helyet idézi (`{}` sorszam {}), de nem azonosítható, melyik szócikkében ({}); a BDB-példa '
                'ezért nem kerül erre a tokenre', peldatabla, r['sorszam'], ok)))
        else:
            peldak.append((g.pelda_kulcs(st, bdb_id, r), r))
    tobb_token = []
    n_token = g.token_szam(vers.kod, st)
    if peldak and n_token >= 2:
        jelek = sorted({kjel(k) for k, _r in peldak})
        tobb_token.append(Indok(IndokFajta.TOBB_TOKEN, prov(
            'a BDB a verset {} szakaszban idézi (`{}` sorszam {}), de a versben a szó {} áll (`{}`), és a szótár nem '
            'jelöli, melyikre gondol; a BDB-példa ezért nem kerül erre a tokenre',
            _belso_jelek(jelek), peldatabla, prov_fuz(', ', [r['sorszam'] for _k, r in peldak]),
            G.hanyszor(n_token), f.utvonal('B08')),
            szakaszok=_proza_jelek(g, strong, jelek), darab=n_token))
        peldak = []
    pelda_k = sorted({k for k, _r in peldak})
    indokok = []
    if len(pelda_k) > 1:
        ala = [k for k in pelda_k if kut_k and G.kulcs_ala_esik(k, kut_k)]
        if len(ala) != 1:
            raise G.GerincHiba('B19: %s %s: a BDB-példák több útvonalra mutatnak (%s): kézi kérdés'
                               % (st, vers.kod, pelda_k))
        mas = [(k, r) for k, r in peldak if k != ala[0]]
        jelek = sorted({kjel(k) for k, _r in mas})
        indokok.append(Indok(IndokFajta.MASUTT_IS, prov(
            'a BDB a helyet {} is idézi (`{}` sorszam {}); a kutatói hozzárendelés ({} → {}, `{}`) dönt',
            _belso_jelek(jelek), peldatabla, prov_fuz(', ', [r['sorszam'] for _k, r in mas]), kulcs, kjel(kut_k),
            cimketabla), szakaszok=_proza_jelek(g, strong, jelek)))
        peldak = [(k, r) for k, r in peldak if k == ala[0]]
        pelda_k = ala
    if peldak:
        p_k = pelda_k[0]
        sorszamok = prov_fuz(', ', [r['sorszam'] for _k, r in peldak])
        for _k, r in peldak:
            if G.forras_javitott(r):
                indokok.append(Indok(IndokFajta.FORRAS_JAVITAS, prov(
                    'a BDB forrásszövege itt a „{}” helyet idézi (sajtóhiba); javítva: {} — a javítás forrása: `{}`, '
                    'kézi sor (`hivatkozas_kezi`, `manual`; indok: a TAHOT és a szövegkörnyezet; DT381 (a))',
                    r['nyers'], r['karoli_vers'], f.utvonal('B17', 1)),
                    idezett=idezet(g.idezet_szoveg('B19', 'nyers', r['nyers'], vers))))
        p_jel = _proza_jelek(g, strong, [kjel(p_k)])
        if kut_k is None:
            valasztott = p_k
            indokok.append(Indok(IndokFajta.BDB_PELDA, prov(
                'BDB-példa: a BDB {} szakaszban maga idézi a helyet (`{}` sorszam {})',
                _belso_jelek([kjel(p_k)]), peldatabla, sorszamok), szakaszok=p_jel))
        elif G.kulcs_ala_esik(p_k, kut_k):
            valasztott = p_k
            indokok.append(Indok(IndokFajta.BDB_PELDA, prov(
                'BDB-példa: a BDB {} szakaszban maga idézi a helyet (`{}` sorszam {}); ez a kutatói hozzárendelés '
                '({} → {}) alá esik, a címke a finomabb útvonalé',
                _belso_jelek([kjel(p_k)]), peldatabla, sorszamok, kulcs, kjel(kut_k)), szakaszok=p_jel))
        elif G.kulcs_ala_esik(kut_k, p_k):
            valasztott = kut_k
            indokok.append(Indok(IndokFajta.KUTATOI_TAGABB, prov(
                'kutatói hozzárendelés a BDB tagolása szerint ({} → {}, `{}`); a BDB a helyet a tágabb {} szakaszban '
                'idézi (`{}` sorszam {})', kulcs, kjel(kut_k), cimketabla, _belso_jelek([kjel(p_k)], nevelo=False),
                peldatabla, sorszamok), szakaszok=p_jel, szotar=f.szotar_kulcs(szotar),
                jel=idezet(g.jel_szoveg(kjel(kut_k), strong))))
        else:
            raise G.GerincHiba('B19: %s %s: a BDB-példa (%s) és a szerkesztői hozzárendelés (%s → %s) egyike sem '
                               'esik a másik alá: kézi kérdés, választás nélkül' % (st, vers.kod, p_k, kulcs, kut_k))
    elif kut_k is not None:
        valasztott = kut_k
        fej = kut_k[1] == 'fej'
        indokok.append(Indok(IndokFajta.KUTATOI, prov(
            'kutatói hozzárendelés a {} tagolása szerint (`elofordulasok.tsv` jelentes_szam „{}” → {}, `{}`)',
            szotar, kulcs, G.szotaras_jel(szotar, kjel(kut_k)), cimketabla),
            szotar=f.szotar_kulcs(szotar), fej=fej,
            jel=None if fej else idezet(g.jel_szoveg(kjel(kut_k), strong))))
        indokok.extend(tobb_token)
        if szotar == G.SZOTAR_BDB and not tobb_token:
            indokok.extend(_tartomany_indokok(g, f, strong, vers))
    else:
        tart = _tartomany_indokok(g, f, strong, vers) if szotar == G.SZOTAR_BDB and not tobb_token else []
        return None, '', tobb_token + nem_azon + tart
    indokok.extend(nem_azon)
    if minosito:
        indokok.append(Indok(IndokFajta.MINOSITO, prov(
            'a kutatói jelentésszám minősítője („{}”) nem a szó jelentése, a címkébe nem kerül (a minősítő nem része '
            'a SEMA 2.2.2 értékkészletének)', minosito)))
    return valasztott, G.szotaras_jel(szotar, kjel(valasztott)), indokok


def _tartomany_indokok(g, f, strong, vers):
    ki = []
    for t in g.tartomanyban(strong.kod, vers.kod):
        jel = g.kulcs_jel(G.SZOTAR_BDB, strong.kod, t.kulcs)
        kezdo = f.konyvek.igehely(t.kezdo_vers)
        ki.append(Indok(IndokFajta.TARTOMANYBAN, prov(
            'a BDB a helyet nem önállóan idézi, hanem {} szakaszban {} {}–{} verstartomány belsejében (a BDB-ben: '
            '„{}{}”; `{}` sorszam {}); a tartomány nincs kibontva (DT382 (A)), ezért a hely nem BDB-példa',
            _belso_jelek([jel]), G.nevelo(t.kezdo_vers), t.kezdo_vers, t.veg, t.nyers, t.folytatas, f.utvonal('B19'),
            t.sorszam), szakaszok=_proza_jelek(g, strong, [jel]), kezdo_vers=kezdo, veg=t.veg))
    return ki


def token_jelentes(g, f, sor, strong, versek):
    """Egy szó jelentéscellája a sor versein: a `jelentes_cella` egy tokenre eső része."""
    st = strong.kod
    szotar_sor = sor.szotar.ertek
    kutatoi_token = sor.entry is not None and sor.entry == strong
    szotar = szotar_sor if kutatoi_token else (G.SZOTAR_BDB if strong.heber else '')
    valasztott, jel, indokok = None, '', []
    for vers in versek:
        v, j, i = _cimke_token(g, f, szotar, strong, sor.jelentes_szam.ertek, vers, kutatoi_token)
        if v or j or i:
            valasztott, jel, indokok = v, j, list(i)
            break
    if not strong.heber and szotar != f.szotar_thayer:
        peldak = g.thayer_peldak(st, [v.kod for v in versek])
        if peldak:
            jelek = sorted({j for j, _s in peldak})
            szamos = [j for j in jelek if j.isdigit()]
            indokok.append(Indok(IndokFajta.THAYER_PELDA, prov(
                'a Thayer saját példahelye: {} (`{}` sorszam {})',
                prov_fuz(', ', [G.szotaras_jel(f.szotar_thayer, j) for j in jelek]),
                f.utvonal('B21'), prov_fuz(', ', [s for _j, s in peldak])),
                darab=int(szamos[0]) if szamos else 0))
        else:
            indokok.append(Indok(IndokFajta.THAYER_NEM_IDEZI,
                                 prov('a Thayer a helyet nem idézi (`{}`)', f.utvonal('B21'))))
    cimke = g.cimke(szotar, st, valasztott) if valasztott is not None else None
    jel_lathato = idezet(g.jel_szoveg(jel, strong)) if jel else None
    if cimke is not None:
        return TokenJelentes(strong, JelentesFajta.CIMKE, proza(cimke), jel_lathato, tuple(indokok),
                             cimke_cella=proza(g.cimke_cella(szotar, st, valasztott)))
    if jel and szotar == G.SZOTAR_BDB:
        glossza = g.szakasz_glossza(st, jel)
        if glossza is not None:
            return TokenJelentes(strong, JelentesFajta.GLOSSZA, idezet(glossza), jel_lathato, tuple(indokok))
    if not jel and strong.heber:
        tagolatlan, glossza = g.tagolatlan(st)
        if tagolatlan:
            return TokenJelentes(strong, JelentesFajta.SZOCIKK_EGESZE, idezet(glossza) if glossza else None, None,
                                 tuple(indokok))
    if jel:
        return TokenJelentes(strong, JelentesFajta.NINCS_CIMKE, None, jel_lathato, tuple(indokok))
    if not indokok:
        indokok.append(Indok(IndokFajta.NINCS_HOZZARENDELES,
                             prov('ehhez a tokenhez nincs kutatói hozzárendelés és szótári példahely')))
    return TokenJelentes(strong, JelentesFajta.NINCS_HOZZARENDELES, None, None, tuple(indokok))
