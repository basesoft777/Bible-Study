"""F94.2 (FELADATOK #94, DT-F94c): a C+K változat K táblája — a Károli 1908 leggyakoribb N alakjának szótári alakja.

A sorok kiválasztása gépi: a `konkordancia/Karoli_1908.tsv` korpusz-lexikonjából (`adat/szoto/karoli_lexikon.tsv`)
a kisbetűs és a mondatkezdő nagybetűs előfordulások összege szerinti első N alak (a mondat belsejében nagybetűs
előfordulás név, az nem számít). N = 400 (indoklás: naplok/SZOTOVEZES_meres.md 11. szakasz). A kiválasztás NEM a
mérés hibáiból és nem a minták alakjaiból történik (meresi_terv 1.3).

A szótári alakok modell-javaslatok a DT130 szerint (modell: claude-opus-5-5), NEM a simplemma kimenetéből: a
kitöltéskor sem a simplemma, sem a hibrid kimenete nem volt a modell előtt (DT-F94c: különben ODbL-származék).
`ellenorzes=modell_ellenorizetlen`; `felhasznalo` csak a felhasználó átnézése után lehet (a modell soha nem írja).

Az alábbi JAVASLAT szótár csak a nem önmagára leképezett alakokat sorolja; a többi alak szótári alakja önmaga
(önálló szótári alak: kötőszó, határozószó, névutó, szám, alapalakú névszó vagy ige).

Használat: python eszkozok/szoto/k_tabla_epit.py [--n 400] [--ts …]   (kimenet: adat/szoto/gyakori_alakok.tsv)"""
import argparse
import collections
import datetime
import hashlib
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LEX = os.path.join(REPO, 'adat', 'szoto', 'karoli_lexikon.tsv')
KI = os.path.join(REPO, 'adat', 'szoto', 'gyakori_alakok.tsv')
OSZLOP = ['rang', 'alak', 'gyakorisag', 'szotari_alak', 'szotari_alak_mai', 'alapige', 'tovabbi_elfogadhato',
          'ellenorzes', 'indoklas']


def J(sz, mai=None, ap='', tov='', ind=''):
    return (sz, mai or sz, ap, tov, ind)


_NEVMAS = 'ragos személyes névmás: a szótári alak a személyes névmás (DT130 (3))'
_MUTATO = 'mutató névmás ragos/többes alakja'
_VONATK = 'vonatkozó/kérdő névmás; mai alakja vonatkozó használatban aki (DT130 (2)); kérdő olvasat: ki'
_MELY = 'vonatkozó névmás, régi alak; mai: amely (DT130 (2))'
_NEVUTO = 'névutó személyragos alakja; a szótári alak a névutó'
_VAN = 'a van rendhagyó alakja, kivételtábla (DT130 (6))'
_LESZ = 'a lesz alakja, külön szótári alak (DT130 (7))'
_MULT = 'régies múlt idő'
_FIU = 'tőváltó (fi-): fiú'

JAVASLAT = {
    # ragos személyes névmás (DT130 (3))
    'néki': J('ő', ind=_NEVMAS), 'nékik': J('ő', ind=_NEVMAS), 'őt': J('ő', ind='személyes névmás tárgyesete'),
    'őket': J('ő', ind='személyes névmás tárgyesete, többes'), 'ők': J('ő', ind='személyes névmás többese'),
    'vele': J('ő', ind=_NEVMAS), 'velök': J('ő', ind=_NEVMAS + '; régies -ök = -ük'), 'benne': J('ő', ind=_NEVMAS),
    'rajta': J('ő', ind=_NEVMAS), 'tőle': J('ő', ind=_NEVMAS),
    'hozzá': J('ő', tov='hozzá', ind=_NEVMAS + '; igekötői / határozószói olvasat: hozzá (DT130 (11))'),
    'reá': J('ő', tov='rá', ind=_NEVMAS + '; régies rá; igekötői olvasat: rá (DT130 (11))'),
    'nékem': J('én', ind=_NEVMAS), 'engem': J('én', ind='személyes névmás tárgyesete'), 'velem': J('én', ind=_NEVMAS),
    'hozzám': J('én', ind=_NEVMAS), 'tőlem': J('én', ind=_NEVMAS), 'reám': J('én', ind=_NEVMAS + '; régies rám'),
    'néked': J('te', ind=_NEVMAS), 'téged': J('te', ind='személyes névmás tárgyesete'), 'veled': J('te', ind=_NEVMAS),
    'hozzád': J('te', ind=_NEVMAS), 'benned': J('te', ind=_NEVMAS),
    'néktek': J('ti', ind=_NEVMAS), 'titeket': J('ti', ind='személyes névmás tárgyesete'), 'veletek': J('ti', ind=_NEVMAS),
    'hozzátok': J('ti', ind=_NEVMAS),
    'nékünk': J('mi', ind=_NEVMAS), 'minket': J('mi', ind='személyes névmás tárgyesete'), 'velünk': J('mi', ind=_NEVMAS),
    'magát': J('maga', ind='visszaható névmás tárgyesete'), 'magának': J('maga', ind='visszaható névmás, -nak rag'),
    # mutató névmás
    'azt': J('az', ind=_MUTATO), 'annak': J('az', ind=_MUTATO), 'azok': J('az', ind=_MUTATO), 'azokat': J('az', ind=_MUTATO),
    'azoknak': J('az', ind=_MUTATO), 'abban': J('az', ind=_MUTATO), 'abból': J('az', ind=_MUTATO), 'arra': J('az', ind=_MUTATO),
    'azzal': J('az', ind=_MUTATO), 'azon': J('az', ind=_MUTATO + ' (azon: -on rag, vagy jelzői „azon”)'),
    'ezt': J('ez', ind=_MUTATO), 'ezek': J('ez', ind=_MUTATO), 'ezeket': J('ez', ind=_MUTATO), 'ennek': J('ez', ind=_MUTATO),
    'e': J('e', 'ez', ind='régies mutató névmás, az ez régi alakja (DT130 (2)); kérdőszócska-olvasat: e'),
    # vonatkozó / kérdő névmás
    'ki': J('ki', tov='aki', ind='igekötő, kérdő névmás vagy vonatkozó névmás (mai: aki) — DT-F94a, DT130 (11)'),
    'kik': J('ki', 'aki', tov='ki', ind=_VONATK), 'kinek': J('ki', 'aki', tov='ki', ind=_VONATK),
    'kit': J('ki', 'aki', tov='ki', ind=_VONATK), 'kiket': J('ki', 'aki', tov='ki', ind=_VONATK),
    'kiknek': J('ki', 'aki', tov='ki', ind=_VONATK),
    'mit': J('mi', tov='ami', ind='kérdő/vonatkozó névmás tárgyesete; a Károli „a mit” szerkezetében vonatkozó névmás, mai alakja amit (felhasználó, 2026-10-13)'),
    'miket': J('mi', tov='ami', ind='kérdő/vonatkozó névmás tárgyesete, többes; vonatkozó olvasatban mai alakja amiket (felhasználó, 2026-10-13)'),
    'mely': J('mely', 'amely', ind=_MELY), 'melyet': J('mely', 'amely', ind=_MELY), 'melyeket': J('mely', 'amely', ind=_MELY),
    'melyek': J('mely', 'amely', ind=_MELY), 'melyen': J('mely', 'amely', ind=_MELY),
    'melylyel': J('mely', 'amely', ind=_MELY + '; régies helyesírás (lyly = lly)'),
    # van / lesz (DT130 (6), (7))
    'vala': J('van', ind=_VAN + '; régies múlt'), 'valának': J('van', ind=_VAN + '; régies múlt T/3'),
    'volt': J('van', ind=_VAN), 'voltak': J('van', ind=_VAN), 'vannak': J('van', ind=_VAN), 'vagyok': J('van', ind=_VAN),
    'vagytok': J('van', ind=_VAN), 'vagyunk': J('van', ind=_VAN), 'volna': J('van', ind=_VAN + '; feltételes'),
    'vagy': J('vagy', tov='van', ind='kötőszó, vagy a van E/2-je (DT130 (11))'),
    'valók': J('való', ind='melléknévi igenév (van) többese'),
    'lesz': J('lesz', ind=_LESZ), 'lesznek': J('lesz', ind=_LESZ), 'lészen': J('lesz', ind=_LESZ + '; régies'),
    'legyen': J('lesz', ind=_LESZ + '; felszólító'), 'legyenek': J('lesz', ind=_LESZ + '; felszólító'),
    'legyetek': J('lesz', ind=_LESZ + '; felszólító'), 'légy': J('lesz', ind=_LESZ + '; felszólító E/2'),
    'lőn': J('lesz', ind=_LESZ + '; régies múlt'), 'lett': J('lesz', ind=_LESZ + '; múlt'),
    'nincsen': J('nincs', ind='a nincs régies alakja'),
    # igék
    'monda': J('mond', ind=_MULT + ', alanyi E/3'), 'mondá': J('mond', ind=_MULT + ', tárgyas E/3'),
    'mondának': J('mond', ind=_MULT + ' T/3'), 'mondván': J('mond', ind='határozói igenév'), 'mondja': J('mond', ind='jelen, tárgyas E/3'),
    'mondják': J('mond', ind='jelen, tárgyas T/3'), 'mondom': J('mond', ind='jelen, tárgyas E/1'),
    'mondjátok': J('mond', ind='felszólító / jelen, tárgyas T/2'), 'mondd': J('mond', ind='felszólító, tárgyas E/2'),
    'szóla': J('szól', ind=_MULT + ', alanyi E/3'), 'szólott': J('szól', ind='múlt'), 'szólj': J('szól', ind='felszólító E/2'),
    'felele': J('felel', ind=_MULT + ', alanyi E/3'), 'felelvén': J('felel', ind='határozói igenév'),
    'menj': J('megy', ind='felszólító E/2; tőváltó'), 'menjetek': J('megy', ind='felszólító T/2; tőváltó'),
    'menjen': J('megy', ind='felszólító E/3; tőváltó'), 'ment': J('megy', tov='ment', ind='múlt E/3; tőváltó; a ment ige olvasata: ment (DT130 (11))'),
    'méne': J('megy', ind=_MULT + '; tőváltó'), 'menének': J('megy', ind=_MULT + ' T/3; tőváltó'),
    'elméne': J('elmegy', ap='megy', ind=_MULT + '; igekötős (DT130 (4))'), 'kiméne': J('kimegy', ap='megy', ind=_MULT + '; igekötős'),
    'beméne': J('bemegy', ap='megy', ind=_MULT + '; igekötős'),
    'jő': J('jön', ind='a jön régi alakja (DT130 (2))'), 'jött': J('jön', ind='múlt E/3'),
    'adott': J('ad', ind='múlt E/3 (melléknévi olvasat: adott)'), 'adá': J('ad', ind=_MULT + ', tárgyas E/3'),
    'adom': J('ad', ind='jelen, tárgyas E/1'), 'adok': J('ad', ind='jelen, alanyi E/1'), 'adja': J('ad', ind='jelen, tárgyas E/3'),
    'adta': J('ad', ind='múlt, tárgyas E/3'), 'adtam': J('ad', ind='múlt E/1'), 'ád': J('ad', ind='régies jelen E/3 (ad)'),
    'cselekedett': J('cselekedik', 'cselekszik', ind='múlt E/3; a cselekedik a cselekszik régi alakja (DT130 (2))'),
    'cselekedék': J('cselekedik', 'cselekszik', ind=_MULT + ' E/1; DT130 (2)'),
    'cselekszik': J('cselekedik', 'cselekszik', ind='DT130 (2): egy szó régi és mai alakja'),
    'nemzé': J('nemz', ind=_MULT + ', tárgyas E/3'), 'meghala': J('meghal', ap='hal', ind=_MULT + '; igekötős'),
    'uralkodék': J('uralkodik', ind=_MULT + ' E/3 (-ék)'), 'kérlek': J('kér', ind='jelen E/1, 2. személyű tárggyal (-lek)'),
    'kelj': J('kel', ind='felszólító E/2'), 'vedd': J('vesz', ind='felszólító, tárgyas E/2; tőváltó'),
    'írva': J('ír', ind='határozói igenév'),
    'fogva': J('fogva', tov='fog', ind='névutóként (… fogva); határozói igenév olvasata: fog'),
    'hadd': J('hadd', tov='hagy', ind='módosítószó; a hagy felszólító alakjából'),
    # névutó személyragos alakja
    'előtte': J('előtt', ind=_NEVUTO), 'előttem': J('előtt', ind=_NEVUTO), 'előtted': J('előtt', ind=_NEVUTO),
    'ellene': J('ellen', ind=_NEVUTO), 'ellenem': J('ellen', ind=_NEVUTO), 'ellened': J('ellen', ind=_NEVUTO),
    'utána': J('után', tov='utána', ind=_NEVUTO + '; határozószói olvasat: utána'),
    'közt': J('között', tov='közt', ind='a között rövid alakja'),
    # névszók
    'fiai': J('fiú', ind=_FIU), 'fia': J('fiú', ind=_FIU), 'fiainak': J('fiú', ind=_FIU), 'fiának': J('fiú', ind=_FIU),
    'fiát': J('fiú', ind=_FIU), 'fiait': J('fiú', ind=_FIU), 'fiam': J('fiú', ind=_FIU),
    'atyámfiai': J('atyafi', ind='birtokos (atyámfia) többes; régies összetétel'),
    'uram': J('úr', ind='birtokos E/1; tőváltó (ur-); a nagybetűs Uram névként a hibrid névágán megy'),
    'királya': J('király', ind='birtokos'), 'királynak': J('király', ind='-nak rag'), 'királyának': J('király', ind='birtokos + -nak'),
    'háza': J('ház', ind='birtokos'), 'házának': J('ház', ind='birtokos + -nak'), 'házában': J('ház', ind='birtokos + -ban'),
    'házába': J('ház', ind='birtokos + -ba'), 'házát': J('ház', ind='birtokos + tárgyrag'), 'házat': J('ház', ind='tárgyrag'),
    'népnek': J('nép', ind='-nek rag'), 'népet': J('nép', ind='tárgyrag'), 'népe': J('nép', ind='birtokos'),
    'népem': J('nép', ind='birtokos E/1'), 'népek': J('nép', ind='többes'),
    'földön': J('föld', ind='-ön rag'), 'földet': J('föld', ind='tárgyrag'), 'földre': J('föld', ind='-re rag'),
    'földnek': J('föld', ind='-nek rag'), 'földén': J('föld', ind='birtokos + -n'),
    'napon': J('nap', ind='-on rag'), 'napig': J('nap', ind='-ig rag'), 'napján': J('nap', ind='birtokos + -n'),
    'embernek': J('ember', ind='-nek rag'), 'emberek': J('ember', ind='többes'), 'embert': J('ember', ind='tárgyrag'),
    'neve': J('név', ind='birtokos; tőváltó (nev-)'), 'nevét': J('név', ind='birtokos + tárgyrag; tőváltó (nev-)'),
    'keze': J('kéz', ind='birtokos; tőváltó (kez-)'), 'kezébe': J('kéz', ind='birtokos + -be; tőváltó'),
    'kezét': J('kéz', ind='birtokos + tárgyrag; tőváltó'), 'kezéből': J('kéz', ind='birtokos + -ből; tőváltó'),
    'lelkem': J('lélek', ind='birtokos E/1; tőváltó (lelk-)'), 'lelke': J('lélek', ind='birtokos; tőváltó (lelk-)'),
    'szíve': J('szív', ind='birtokos'), 'szemei': J('szem', ind='birtokos többes'), 'szolgái': J('szolga', ind='birtokos többes'),
    'atyja': J('atya', ind='birtokos; tőváltó (atyj-)'), 'atyjának': J('atya', ind='birtokos + -nak; tőváltó (atyj-)'),
    'leánya': J('leány', 'lány', ind='birtokos; a lány a leány összevont alakja (DT130 (2))'),
    'szavát': J('szó', ind='birtokos + tárgyrag; tőváltó (szav-)'), 'vizet': J('víz', ind='tárgyrag; tőváltó (viz-)'),
    'dolgot': J('dolog', ind='tárgyrag; tőváltó (dolg-)'), 'kenyeret': J('kenyér', ind='tárgyrag; tőváltó (kenyer-)'),
    'várost': J('város', ind='tárgyrag'), 'úton': J('út', ind='-on rag'), 'helyen': J('hely', ind='-en rag'),
    'helyre': J('hely', ind='-re rag'), 'pusztában': J('puszta', ind='-ban rag'), 'időben': J('idő', ind='-ben rag'),
    'igazságot': J('igazság', ind='tárgyrag'), 'nemzetségéből': J('nemzetség', ind='birtokos + -ből'),
    'nemzetsége': J('nemzetség', ind='birtokos'), 'beszéde': J('beszéd', ind='birtokos'), 'beszédét': J('beszéd', ind='birtokos + tárgyrag'),
    'esztendeig': J('esztendő', ind='tőváltó (esztende-) + -ig'), 'esztendejében': J('esztendő', ind='birtokos + -ben; tőváltó (esztendej-)'),
    'papok': J('pap', ind='többes'), 'próféták': J('próféta', ind='többes'), 'zsidók': J('zsidó', ind='többes'),
    'pogányok': J('pogány', ind='többes'), 'férfiak': J('férfiú', 'férfi', ind='többes; a férfiú a férfi régi alakja (DT130 (2))'),
    'férfiú': J('férfiú', 'férfi', ind='a férfi régi alakja (DT130 (2))'),
    'bűnért': J('bűn', ind='-ért rag'), 'bizonyságot': J('bizonyság', ind='tárgyrag'), 'áldozatul': J('áldozat', ind='-ul rag'),
    'gonoszt': J('gonosz', ind='tárgyrag'), 'jót': J('jó', ind='tárgyrag'), 'mindent': J('minden', ind='tárgyrag'),
    'semmit': J('semmi', ind='tárgyrag'), 'sokan': J('sok', ind='-an határozórag'),
    'jobb': J('jobb', tov='jó', ind='a jó középfoka (vagy: jobb kéz); középfokú olvasat: jó'),
    'két': J('két', tov='kettő', ind='a kettő jelzői alakja'),
    # helyesírás / régi alak (DT130 (2))
    'ímé': J('íme', ind='régies indulatszó (ím, íme)'), 'miképen': J('miképen', 'miképpen', ind='régies helyesírás'),
    'vajjon': J('vajjon', 'vajon', ind='régies helyesírás'), 'kivül': J('kivül', 'kívül', ind='régies helyesírás'),
    'oh': J('oh', 'ó', ind='régies indulatszó'),
    'jézus': J('Jézus', ind='tulajdonnév (a mondatkezdő előfordulásokkal együtt számolva)'),
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--n', type=int, default=400)
    ap.add_argument('--ts', default=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%MZ'))
    ap.add_argument('--lista', action='store_true', help='csak az önmagára leképezett alakok listája (átnézéshez)')
    ap.add_argument('--felhasznalo-atnezte', metavar='PROVENIENCIA',
                    help='a felhasználó mind a sorokat átnézte: minden sor ellenorzes=felhasznalo, ezzel a proveniencia-sorral '
                         '(csak a felhasználó kifejezett döntése alapján; a modell magától soha)')
    a = ap.parse_args()
    f = collections.Counter()
    for l in open(LEX, encoding='utf-8'):
        if l.startswith('#') or l.rstrip('\n') == 'alak\tkisbetus\tnagy_belul\tnagy_kezdo':
            continue
        w, k, nb, nk = l.rstrip('\n').split('\t')
        f[w.lower()] += int(k) + int(nk)
    rend = sorted(f.items(), key=lambda x: (-x[1], x[0]))[:a.n]
    fol = [w for w in JAVASLAT if w not in dict(rend)]
    if fol:
        sys.exit(f'HIBA: a javaslat-szótárban az első {a.n} alakon kívüli alak: {fol}')
    if a.lista:
        print(' '.join(w for w, _ in rend if w not in JAVASLAT))
        return
    h = hashlib.sha256(open(LEX, 'rb').read()).hexdigest()
    # a felhasználó által már kitöltött `ellenorzes` megmarad, ha a sor szótári alakja nem változott
    regi = {}
    regi_prov = []
    if os.path.exists(KI):
        regi_prov = [s[len('# ellenorzes-proveniencia: '):] for s in open(KI, encoding='utf-8').read().split('\n')
                     if s.startswith('# ellenorzes-proveniencia: ')]
        sorok = [s for s in open(KI, encoding='utf-8').read().split('\n') if s and not s.startswith('#')]
        fej = sorok[0].split('\t')
        for s in sorok[1:]:
            r = dict(zip(fej, s.split('\t')))
            regi[r['alak']] = r
    with open(KI, 'w', encoding='utf-8', newline='\n') as o:
        o.write(f'# proveniencia: scope=a Károli 1908 leggyakoribb {a.n} alakja (kisbetűs + mondatkezdő előfordulás; a teljes Károli '
                f'{sum(f.values())} tokenjének {100 * sum(n for _, n in rend) / sum(f.values()):.1f}%-a) | forras=adat/szoto/karoli_lexikon.tsv '
                f'(sha256:{h[:12]}; a kiválasztás) + manual (a szótári alak modell-javaslat a DT130 szerint, modell: claude-opus-5-5, '
                f'a simplemma és a hibrid kimenete nélkül) | ts={a.ts}\n')
        prov_e = a.felhasznalo_atnezte or (regi_prov[0] if regi_prov else '')
        o.write('# allapot: ellenorzes soronként: felhasznalo, ha a felhasználó átnézte (l. ellenorzes-proveniencia), különben '
                'modell_ellenorizetlen. A szótári alak kézi forrása az eszkozok/szoto/k_tabla_epit.py JAVASLAT szótára (javítás ott); az ellenorzes oszlopot '
                'a felhasználó tölti, az újraépítés megtartja, ha a sor szótári alakja nem változott (DT-F94c, SEMA 2.27)\n')
        if prov_e:
            o.write('# ellenorzes-proveniencia: ' + prov_e + '\n')
        o.write('\t'.join(OSZLOP) + '\n')
        for i, (w, n) in enumerate(rend, 1):
            sz, mai, apg, tov, ind = JAVASLAT.get(w, (w, w, '', '', 'önálló szótári alak'))
            ell = 'felhasznalo' if a.felhasznalo_atnezte else 'modell_ellenorizetlen'
            r = regi.get(w)
            if not a.felhasznalo_atnezte and r and (r['szotari_alak'], r['szotari_alak_mai'], r['alapige'], r['tovabbi_elfogadhato']) == (sz, mai, apg, tov):
                ell = r['ellenorzes']
            o.write('\t'.join([str(i), w, str(n), sz, mai, apg, tov, ell, ind]) + '\n')
    print(f'{KI}: {len(rend)} sor, ebből {sum(1 for w, _ in rend if w in JAVASLAT)} nem önmagára leképezett')


if __name__ == '__main__':
    main()
