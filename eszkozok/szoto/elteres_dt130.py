"""F94.0/3 (FELADATOK #94, SZOTOVEZES): az 1. és 2. szótövezési minta gépi összevetése a DT130 végleges
pontjaival. Csak listáz, nem javít; a kimenet (markdown) a naplok/SZOTOVEZES_meres.md eltérés-listája.
A javítás a felhasználó döntése után történik (F94_SZOTOVEZES_BRIEF.md .0/3, ⛔).

Ellenőrzött pontok (DT130):
  (4)  igénél az alapige külön oszlop (igekötős ige: az igekötő nélküli ige);
  (6)  a van rendhagyó alakjai a van alá;  (7) a lesz külön szótári alak (lőn, legyen, lészen -> lesz);
  (8)  Seregek: nagybetűvel (Istenre vonatkozó cím) névként marad, kisbetűvel sereg;
  (9)  kevéssé önálló határozószó;
  (10) C) képzett igealak: szenvedő (-tatik/-tetik, -atik/-etik) és -hat/-het külön szótári alak, kitöltött alapigével;
  (11) kétértelmű alak: mindkét olvasat elfogadott (tovabbi_elfogadhato).
A javaslat-oszlop modell-állítás (manual), a felhasználó dönt.

Használat: python eszkozok/szoto/elteres_dt130.py > kimenet.md"""
import datetime
import hashlib
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MINTAK = [('1', os.path.join(REPO, 'adat', 'szoto', 'szoto_minta_1_fejlesztes.tsv')),
          ('2', os.path.join(REPO, 'adat', 'szoto', 'szoto_minta_2_fejlesztes.tsv'))]
KAROLI = os.path.join(REPO, 'konkordancia', 'Karoli_1908.tsv')

IGEKOTO = ['vissza', 'össze', 'utána', 'hozzá', 'széjjel', 'szét', 'meg', 'fel', 'föl', 'ki', 'be', 'el', 'le', 'rá',
           'reá', 'át', 'oda', 'ide', 'alá', 'elő', 'ellen', 'végig', 'után']
LESZ = {'lőn', 'lőnek', 'lőnének', 'lőne', 'lészen', 'lésznek', 'legyen', 'legyenek', 'legyetek', 'legyél', 'légy',
        'legyünk', 'lett', 'lettek', 'lenne', 'lennének', 'lennék', 'lesz', 'lesznek', 'leszek', 'leszel', 'leve', 'levén',
        'lévén', 'lenni'}
VAN = {'vala', 'valának', 'valék', 'valál', 'valánk', 'valátok', 'volt', 'voltak', 'vagyon', 'vagynak', 'vagyok',
       'vagyunk', 'vagytok', 'van', 'vannak', 'volna', 'volnék', 'volnának', 'való'}
IGEKAT = {'regies_ige', 'ige_mai_alak'}


def beolvas(p):
    sorok = [s for s in open(p, encoding='utf-8').read().split('\n') if s and not s.startswith('#')]
    fej = sorok[0].split('\t')
    return [dict(zip(fej, s.split('\t'))) for s in sorok[1:]]


def igekotos(t):
    for ik in IGEKOTO:
        if t.startswith(ik) and len(t) - len(ik) >= 2:
            return ik, t[len(ik):]
    return None


def seregek_kornyezet():
    """A kisbetűs seregek-alakok és a nagybetűs Seregek-alakok Károli-előfordulása, és hány áll Ur-/Isten- előtt."""
    szam = {}
    for sor in open(KAROLI, encoding='utf-8').read().split('\n')[1:]:
        if '\t' not in sor:
            continue
        szavak = re.findall(r'[\wÁÉÍÓÖŐÚÜŰáéíóöőúüű-]+', sor.split('\t')[1])
        for i, w in enumerate(szavak):
            if w.lower().startswith('seregek'):
                k = (w, i + 1 < len(szavak) and re.match(r'(Ur|Isten)', szavak[i + 1]) is not None)
                szam[k] = szam.get(k, 0) + 1
    return szam


def main():
    talalat = {k: [] for k in ('4', '6-7', '8', '9', '10', '10m', '11')}
    for mid, p in MINTAK:
        for r in beolvas(p):
            a, al = r['alak'], r['alak'].lower()
            sz, mai, ap, tov = r['szotari_alak'], r['szotari_alak_mai'], r['alapige'], r['tovabbi_elfogadhato']
            ige = r['kategoria'] in IGEKAT or al in LESZ or al in VAN
            sor = dict(m=mid, r=r)
            # (6)-(7) van / lesz
            alap = igekotos(al)
            tor = alap[1] if alap else al
            if (al in LESZ or tor in LESZ) and not sz.lower().endswith('lesz'):
                talalat['6-7'].append(dict(sor, j=f'szótári alak: {"meg" if alap else ""}lesz'))
            elif al in VAN and al != 'való' and sz.lower() != 'van':
                talalat['6-7'].append(dict(sor, j='szótári alak: van'))
            # (8) Seregek
            if al.startswith('sereg'):
                elvart = 'Seregek' if a[:1].isupper() else 'sereg'
                j = 'rendben' if sz == elvart else f'szótári alak: {elvart}'
                if j == 'rendben' and elvart == 'sereg' and al.startswith('seregek'):
                    j = ('a pont betűje szerint rendben; de a példavers (' + r['pelda_igehely'] + ') kisbetűs Istenre vonatkozó cím '
                         '(„a seregeknek Ura”), l. alább: a felhasználó dönt (sereg, vagy Seregek / tovabbi_elfogadhato)')
                talalat['8'].append(dict(sor, j=j))
            # (9) kevéssé
            if al == 'kevéssé' and sz != 'kevéssé':
                talalat['9'].append(dict(sor, j='szótári alak: kevéssé'))
            # (10) C) képzett igealak
            szenvedo = re.search(r'(t[ae]t|[^aáeéiíoóöőuúüű][ae]t)ik$', sz.lower()) is not None
            hathet = ige and re.search(r'h[ae]t', al) is not None and re.search(r'h[ae]t', sz.lower()) is not None
            if szenvedo or hathet:
                alapige_ok = ap and ap.lower() != sz.lower()
                if alapige_ok:
                    j = 'rendben'
                elif szenvedo and not re.search(r't[ae]tik$', sz.lower()):
                    j = ('gépi jelölt (-etik/-atik): ha szenvedő képzés, alapige kitöltendő; ha önálló -ik-es ige '
                         '(pl. születik), változatlan — a felhasználó dönt')
                else:
                    j = 'alapige kitöltendő (az igekötő és a képző nélküli ige)'
                talalat['10'].append(dict(sor, j=j))
            elif ige and re.search(r'(t[ae]t)$', sz.lower()) and not (ap and ap.lower() != sz.lower()):
                talalat['10m'].append(dict(sor, j='műveltető (-tat/-tet): a DT130 (10) nem nevezi meg; a felhasználó dönt, kap-e alapigét'))
            # (11) kétértelmű alak
            if ('kétértelmű' in r['indoklas'] or re.search(r'\bvagy\b', r['indoklas']) or al == 'vagy') and not tov:
                j = {'az': 'a két olvasat (névelő / mutató névmás) szótári alakja azonos: változatlan',
                     'ki': 'tovabbi_elfogadhato: aki (a vonatkozó névmás mai alakja; az igekötői olvasat: ki)'}.get(
                    al, 'a második olvasat a tovabbi_elfogadhato oszlopba, ha a két olvasat szótári alakja eltér')
                talalat['11'].append(dict(sor, j=j))
            elif al == 'elvesznek' and not tov:
                talalat['11'].append(dict(sor, j='elvesz / elvész: a forma szövegkörnyezet nélkül kétértelmű; a felhasználó a sort elvész-ként zárta'))
            # (4) alapige igekötős igénél
            if ige and not (szenvedo or hathet):
                ik = igekotos(sz.lower())
                if ik and not ap and not sz.lower().endswith('lesz') or (ik and not ap and sz.lower() == 'meglesz'):
                    talalat['4'].append(dict(sor, j=f'alapige: {ik[1]}'))
    # 1. minta: az alapige minden sorban kitöltve (nem ige is) — konvenció-eltérés a 3. mintától
    m1 = beolvas(MINTAK[0][1])
    nem_ige_alapige = [r for r in m1 if r['alapige'] and r['kategoria'] not in IGEKAT and r['alapige'] == r['szotari_alak_mai']]
    nem_igekotos_ige = [r for r in m1 if r['alapige'] and r['kategoria'] in IGEKAT and r['alapige'] == r['szotari_alak_mai']]
    m2 = beolvas(MINTAK[1][1])

    ts = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%MZ')
    h = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()[:12]
    cim = {
        '6-7': 'E-1. DT130 (6)–(7): a van rendhagyó alakjai / a lesz külön szótári alak',
        '8': 'E-2. DT130 (8): Seregek / sereg',
        '9': 'E-3. DT130 (9): kevéssé',
        '10': 'E-4. DT130 (10): C) képzett igealak (szenvedő, -hat/-het) alapigével',
        '10m': 'E-5. Kérdéses (nem DT130-pont): műveltető igealak alapige nélkül',
        '11': 'E-6. DT130 (11): kétértelmű alak, kettős elfogadás',
        '4': 'E-7. DT130 (4): igekötős ige alapige nélkül',
    }
    print('| csoport | eltérő sor | ebből `felhasznalo` |')
    print('|---|---|---|')
    for k in ('6-7', '8', '9', '10', '10m', '11', '4'):
        elt = [t for t in talalat[k] if t['j'] != 'rendben' and not t['j'].startswith('a két olvasat')]
        print(f'| {cim[k]} | {len(elt)} | {sum(1 for t in elt if t["r"]["ellenorzes"] == "felhasznalo")} |')
    print(f'| E-8. Konvenció: az 1. minta alapige-oszlopa nem igén és igekötő nélküli igén is ki van töltve | '
          f'{len(nem_ige_alapige) + len(nem_igekotos_ige)} | 0 |')
    for k in ('6-7', '8', '9', '10', '10m', '11', '4'):
        print(f'\n#### {cim[k]}\n')
        if not talalat[k]:
            print('Nincs eltérő sor (az 1. és 2. mintában ilyen alak nem fordul elő, vagy a pont szerint áll).')
            continue
        print('| minta | alak | gyak. | szotari_alak / mai | alapige | tovabbi | ellenorzes | javaslat (modell, manual) |')
        print('|---|---|---|---|---|---|---|---|')
        for t in talalat[k]:
            r = t['r']
            print(f'| {t["m"]} | {r["alak"]} | {r["gyakorisag"]} | {r["szotari_alak"]} / {r["szotari_alak_mai"]} | '
                  f'{r["alapige"] or "—"} | {r["tovabbi_elfogadhato"] or "—"} | {r["ellenorzes"]} | {t["j"]} |')
        if k == '8':
            sz = seregek_kornyezet()
            kis = sum(v for (w, _), v in sz.items() if w[:1].islower())
            kis_ur = sum(v for (w, u), v in sz.items() if w[:1].islower() and u)
            nagy = sum(v for (w, _), v in sz.items() if w[:1].isupper())
            nagy_ur = sum(v for (w, u), v in sz.items() if w[:1].isupper() and u)
            pontos = sum(v for (w, _), v in sz.items() if w == 'Seregek')
            print(f'\nKörnyezet a `Karoli_1908.tsv`-ben (a teljes Károli): nagybetűs *Seregek…* {nagy} token (ebből a pontos *Seregek* '
                  f'alak {pontos}, ez a DT130 (8) „119”-e; a többi *Seregeknek*), ebből Ur-/Isten- előtt {nagy_ur}; '
                  f'kisbetűs *seregek…* {kis} token, ebből Ur-/Isten- előtt {kis_ur}. A DT130 (8) a kisbetűs alakot a *sereg* alá veszi; '
                  f'ha a kisbetűs alak Ur-/Isten- előtt áll (Istenre vonatkozó cím kisbetűvel), az a pont hatókörén kívüli kérdés, '
                  f'a felhasználó dönt.')
    print(f'\n#### {"E-8. Konvenció: az 1. minta alapige-oszlopa"}\n')
    print(f'Az 1. minta a forrásban minden sorban kitölti az `alapige`-t: nem igei sorban a mai szótári alakkal ({len(nem_ige_alapige)} sor, '
          f'pl. {", ".join(r["alak"] for r in nem_ige_alapige[:5])}), igekötő nélküli igénél a szótári alakkal ({len(nem_igekotos_ige)} sor, '
          f'pl. {", ".join(r["alak"] for r in nem_igekotos_ige[:5])}). A 3. minta (felhasználó által ellenőrzött) az `alapige`-t csak ott tölti, '
          f'ahol eltér a szótári alaktól (igekötős vagy képzett ige); a 2. mintának nincs `alapige` oszlopa (mind a {len(m2)} sor üres). '
          f'Javaslat (modell): a 3. minta konvenciója, vagyis az 1. minta azonos értékű `alapige`-mezőinek ürítése. A mérést nem érinti '
          f'(az M1 a szótári alakot, a mai alakot és a tovabbi_elfogadhato-t veti össze).')
    print(f'\nscope=adat/szoto/szoto_minta_1_fejlesztes.tsv (sha256:{h(MINTAK[0][1])}) + szoto_minta_2_fejlesztes.tsv '
          f'(sha256:{h(MINTAK[1][1])}), DT130 (4), (6)–(11) | forras=eszkozok/szoto/elteres_dt130.py + konkordancia/Karoli_1908.tsv '
          f'(sha256:{h(KAROLI)}) | ts={ts}')


if __name__ == '__main__':
    main()
