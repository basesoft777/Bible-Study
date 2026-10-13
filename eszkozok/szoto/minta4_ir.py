"""F94.3/2 (FELADATOK #94): a negyedik, független minta írása a modell szótárialak-javaslataival — a hibrid v3
befagyasztása után, a hibrid futtatása ELŐTT (a javaslatokat a modell a példavers alapján, a DT130 és a DT-F94a/b
szerint írta; a hibrid és a simplemma kimenetét a 4. minta alakjain nem látta).

Bemenet: a `minta4_jeloltek.py` jelölt-listája (alak, gyakoriság, réteg, példa-igehely, példavers).
Kimenet: `adat/szoto/szoto_minta_4_fuggetlen.tsv` (SEMA 2.27). Az `ellenorzes` értéke mindenütt
`modell_ellenorizetlen`: a felhasználó soronként ellenőrzi és ő írja `felhasznalo`-ra (F94.3 ⛔); a modell soha.
A `strong` a repó párosításából (`adat/karoli_strong/szavak_<könyv>.tsv`), ahol a könyv párosított; Mk, Ján, Róm,
Jel nincs párosítva: ott üres.

Használat: python eszkozok/szoto/minta4_ir.py --jeloltek <tsv> [--ts …]"""
import argparse
import datetime
import hashlib
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
KI = os.path.join(REPO, 'adat', 'szoto', 'szoto_minta_4_fuggetlen.tsv')
SZAVAK = {'5Móz': '5Moz', '1Sám': '1Sam', 'Péld': 'Peld', 'Ez': 'Ez'}
OSZLOPOK = ['alak', 'gyakorisag', 'kategoria', 'szotari_alak', 'szotari_alak_mai', 'alapige', 'tovabbi_elfogadhato',
            'ellenorzes', 'indoklas', 'pelda_igehely', 'strong']


def J(sz, mai=None, ap='', tov='', ind='', biz=''):
    return dict(szotari_alak=sz, szotari_alak_mai=mai or sz, alapige=ap, tovabbi_elfogadhato=tov,
                indoklas=ind + (f' [bizonytalan: {biz}]' if biz else ''))


NEVMAS = 'ragos személyes névmás (DT130 (3))'
JAVASLAT = {
    # gyakori
    'hanem': J('hanem', ind='kötőszó'), 'Saul': J('Saul', ind='tulajdonnév'), 'közül': J('közül', ind='névutó'),
    'Istened': J('Isten', ind='birtokos E/2 („az Úr, a te Istened”); Isten névként (DT130 (5))'),
    'által': J('által', ind='névutó'), 'azon': J('az', ind='mutató névmás -on raggal / jelzői „azon” (5Móz 1:44 „azon a hegyen”)'),
    'Akkor': J('akkor', ind='határozószó, mondatkezdő nagybetű'), 'sok': J('sok', ind='határozatlan számnév'),
    'Filiszteusok': J('Filiszteus', tov='Filiszteusok', ind='népnév többese; a népnév Károli-átírásban (DT130 (5))',
                      biz='a népnév szótári alaka egyes számú (Filiszteus) vagy a többes (Filiszteusok); mindkettő elfogadhatónak jelölve'),
    'Istennek': J('Isten', ind='-nek rag; név'), 'többé': J('többé', ind='határozószó („nem … többé”)'),
    'oda': J('oda', ind='határozószó / igekötő'), 'se': J('se', ind='tagadószó'), 'jó': J('jó', ind='melléknév'),
    'Sámuel': J('Sámuel', ind='tulajdonnév'), 'két': J('két', tov='kettő', ind='a kettő jelzői alakja'),
    'valaki': J('valaki', ind='határozatlan névmás'), 'maga': J('maga', ind='visszaható névmás'),
    'hét': J('hét', ind='számnév (5Móz 16:3 „hét napig”)'), 'hol': J('hol', ind='kérdő határozószó'),
    'most': J('most', ind='határozószó'), 'hozzám': J('én', ind=NEVMAS), 'sing': J('sing', ind='mértékegység (könyök)'),
    'volna': J('van', ind='a van feltételes alakja (DT130 (6))'), 'senki': J('senki', ind='névmás'),
    # régies helyesírás
    'kilenczedik': J('kilenczedik', 'kilencedik', ind='cz = c (régies helyesírás); sorszámnév'),
    'harminczezer': J('harminczezer', 'harmincezer', ind='cz = c; számnév'),
    'körülöttök': J('körül', ind='névutó + régies -ök (= -ük) személyrag (a 2. minta előttök → előtt mintájára)'),
    'lánczot': J('láncz', 'lánc', ind='cz = c, tárgyrag'), 'utczára': J('utcza', 'utca', ind='cz = c, -ra rag'),
    'harczolnának': J('harczol', 'harcol', ind='cz = c; feltételes T/3'),
    'közűlök': J('közül', ind='névutó + régies -ök személyrag; űl = ül (régies helyesírás)'),
    'czédrusfa': J('czédrusfa', 'cédrusfa', ind='cz = c; összetett főnév'),
    'fejedelmök': J('fejedelem', ind='birtokos T/3 régies -ök (= -ük); tőváltó (fejedelm-)'),
    'kivánságát': J('kivánság', 'kívánság', ind='kiván = kíván (régies helyesírás); birtokos + tárgyrag'),
    'czédrusfából': J('czédrusfa', 'cédrusfa', ind='cz = c; -ból rag'),
    'összegyűlekezének': J('összegyűlekezik', 'összegyülekezik', ap='gyülekezik', ind='régies múlt T/3; igekötős (DT130 (4))',
                           biz='a mai írásmód (összegyülekezik, rövid ü) és az alapige írásmódja'),
    # régies ige
    'ötvenedesekké': J('ötvenedes', ind='főnév többese + -ké (-vé) rag; nem ige (a mintavevő -é végződés-szűrője hozta)'),
    'vágván': J('vág', ind='-ván határozói igenév'), 'vagyunk-é': J('van', ind='a van T/1 alakja + -é kérdőszócska'),
    'tartózkodék': J('tartózkodik', ind='régies múlt E/3 (-ik-es igénél az -ék E/3: „Saul … tartózkodék”)'),
    'elküldének': J('elküld', ap='küld', ind='régies múlt T/3; igekötős'),
    'terítsék': J('terít', ind='felszólító T/3 tárgyas; az igekötő külön áll („terítsék ki”), ezért a szótári alak igekötő nélkül (N-F94a)'),
    'elfeledték': J('elfeled', 'elfelejt', ap='feled', ind='múlt T/3 tárgyas; az elfeled az elfelejt régi alakja (DT130 (2)); igekötős',
                    biz='az elfeled / elfelejt egy szó két alakjának vehető-e (DT130 (2))'),
    'házánál': J('ház', ind='birtokos + -nál'), 'merítvén': J('merít', ind='-vén határozói igenév'),
    'ítél': J('ítél', ind='jelen E/3'), 'kényszeríték': J('kényszerít', ind='régies múlt T/3 tárgyas („kényszeríték őt”)'),
    'elhajtá': J('elhajt', ap='hajt', ind='régies múlt E/3 tárgyas; igekötős'),
    'veszszejévé': J('veszsző', 'vessző', ind='szsz = ssz (régies helyesírás); birtokos + -vé rag'),
    'törlé': J('töröl', ind='régies múlt E/3 tárgyas; tővéghangzó-kiesés (törl-); az igekötő külön áll („törlé meg”)'),
    'megkené': J('megken', ap='ken', ind='régies múlt E/3 tárgyas; igekötős'),
    'fügefának': J('fügefa', ind='-nak rag'), 'hosszútűrésénél': J('hosszútűrés', ind='birtokos + -nél (névutós szerkezet: … fogva)'),
    'futván': J('fut', ind='-ván határozói igenév'), 'kárbunkulusoknál': J('kárbunkulus', ind='többes + -nál'),
    'tévelyedjék': J('tévelyedik', ind='felszólító E/3; az igekötő külön áll („el ne tévelyedjék”)'),
    # tulajdonnév
    'Istenünkéi': J('Isten', ind='birtokos T/1 + -é birtokjel + -i többes birtok („a mi Istenünkéi”); név'),
    'Úré': J('Úr', ind='név + -é birtokjel'), 'Gileádot': J('Gileád', ind='tulajdonnév + tárgyrag'),
    'Krisztussal': J('Krisztus', ind='tulajdonnév + -sal'), 'Jóna': J('Jóna', ind='tulajdonnév („a Jóna fia”)'),
    'Üldözzem-é': J('üldöz', ind='mondatkezdő ige, nem tulajdonnév; felszólító E/1 tárgyas + -é kérdőszócska'),
    'Béth-Avenen': J('Béth-Aven', ind='helynév + -en rag („Béth-Avenen túl”)'),
    'Girzeusokat': J('Girzeus', tov='Girzeusok', ind='népnév többese + tárgyrag', biz='a népnév egyes vagy többes alaka (mint Filiszteusok)'),
    # ragos névszó
    'szombatimat': J('szombat', ind='birtokos többes E/1 (régies -im) + tárgyrag'), 'házától': J('ház', ind='birtokos + -tól'),
    'másodiknak': J('második', ind='sorszámnév + -nak'), 'összehívá': J('összehív', ap='hív', ind='régies múlt E/3 tárgyas; igekötős'),
    'hunyorgat': J('hunyorgat', ind='jelen E/3'), 'hosszúságot': J('hosszúság', ind='tárgyrag'),
    'feltámadására': J('feltámadás', ind='birtokos + -ra'), 'nyelvével': J('nyelv', ind='birtokos + -vel'),
    'kezemnek': J('kéz', ind='birtokos E/1 + -nek; tőváltó (kez-)'), 'siklusnak': J('siklus', ind='-nak rag'),
    'hívogatnak': J('hívogat', ind='jelen T/3'), 'atyafiaival': J('atyafi', ind='birtokos többes + -val'),
    'egeknek': J('ég', ind='többes + -nek; tőváltó (eg-)'), 'szolgáivá': J('szolga', ind='birtokos többes + -vá'),
    'unokákat': J('unoka', ind='többes + tárgyrag'), 'dicsőségétől': J('dicsőség', ind='birtokos + -től'),
    'szómat': J('szó', ind='birtokos E/1 + tárgyrag'), 'megtére': J('megtér', ap='tér', ind='régies múlt E/3; igekötős'),
    'törekesznek': J('törekedik', 'törekszik', ind='jelen T/3; a törekedik a törekszik régi alakja (DT130 (2))'),
    'szívűeknek': J('szívű', ind='melléknév főnevesült többese + -nek („a keseredett szívűeknek”)'),
    'köntösökben': J('köntös', ind='többes + -ben'), 'tisztátalanságodnak': J('tisztátalanság', ind='birtokos E/2 + -nak'),
    'szemnek': J('szem', ind='-nek rag'), 'káromlásra': J('káromlás', ind='-ra rag'), 'romlásra': J('romlás', ind='-ra rag'),
    'vehet': J('vehet', ap='vesz', tov='vesz', ind='-het képzős ige külön szótári alak (DT130 (10)); alapige: vesz'),
    'kivánnak': J('kiván', 'kíván', ind='kiván = kíván (régies helyesírás); jelen T/3'),
    'mikre': J('mi', 'ami', ind='vonatkozó névmás többes + -re („a mikre” = amikre); mai alakja ami (DT130 (2))',
               biz='vonatkozó (ami) vagy kérdő (mi) olvasat; mindkettő elfogadhatónak jelölve'),
    'tisztátalannak': J('tisztátalan', ind='-nak rag'), 'betegségben': J('betegség', ind='-ben rag'),
    'szegénységet': J('szegénység', ind='tárgyrag'),
    'felingereltessenek': J('felingereltetik', ap='ingerel', tov='ingerel',
                            ind='szenvedő (-tetik) felszólító T/3 („hogy ők felingereltessenek”); külön szótári alak (DT130 (10)); igekötős',
                            biz='szenvedő vagy műveltető olvasat'),
    'keresztülszúrjanak': J('keresztülszúr', ap='szúr', ind='felszólító T/3; igekötős'),
    'múlnak': J('múlik', ind='jelen T/3; az igekötő külön áll („el nem múlnak”)'), 'űzzenek': J('űz', ind='felszólító T/3 („gúnyt űzzenek”)'),
    # mai igealak
    'dolgotok': J('dolog', ind='birtokos T/2; tőváltó (dolg-)'), 'jóakaratja': J('jóakarat', ind='birtokos'),
    'várja': J('vár', ind='jelen E/3 tárgyas'),
    'bízott': J('bíz', tov='bízik', ind='múlt E/3; itt tárgyas „rábíz” jelentés („bízott reám valamit”)',
                biz='bíz (megbíz) vagy bízik (bizalom); mindkettő elfogadhatónak jelölve'),
    'dicsekedünk': J('dicsekedik', 'dicsekszik', ind='jelen T/1; a dicsekedik a dicsekszik régi alakja (DT130 (2))'),
    'látják': J('lát', ind='jelen T/3 tárgyas'), 'felállának': J('feláll', ap='áll', ind='régies múlt T/3; igekötős'),
    'szegénységök': J('szegénység', ind='birtokos T/3, régies -ök (= -ük)'),
    'ehetének': J('ehet', ap='eszik', tov='eszik', ind='-het képzős ige külön szótári alak, régies múlt T/3 (DT130 (10)); alapige: eszik'),
    'öltek': J('öl', ind='múlt T/3 („senkit sem öltek meg”)'), 'nyiratkoznak': J('nyiratkozik', ind='jelen T/3'),
    'kioltani': J('kiolt', ap='olt', ind='főnévi igenév; igekötős'), 'építeni': J('épít', ind='főnévi igenév'),
}


def strong(alak, igehely):
    konyv = igehely.rsplit(' ', 1)[0]
    if konyv not in SZAVAK:
        return ''
    p = os.path.join(REPO, 'adat', 'karoli_strong', f'szavak_{SZAVAK[konyv]}.tsv')
    tok = []
    for s in open(p, encoding='utf-8').read().split('\n'):
        if s.startswith(igehely + '\thu\t'):
            m = s.split('\t')
            tok.append(m)
    e = [t for t in tok if t[3] == alak] or [t for t in tok if t[3].lower() == alak.lower()]
    return e[0][6] if e and e[0][4] == 'parositva' else ''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--jeloltek', required=True)
    ap.add_argument('--felulir', action='store_true', help='a meglévő (a felhasználó által már ellenőrzött) minta felülírása')
    ap.add_argument('--ts', default=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%MZ'))
    a = ap.parse_args()
    if os.path.exists(KI) and not a.felulir:
        sys.exit(f'HIBA: {KI} már létezik (a felhasználó ellenorzes-jelölései elveszhetnek); --felulir kell')
    sorok = open(a.jeloltek, encoding='utf-8').read().split('\n')
    prov_j = sorok[0].lstrip('# ').strip()
    fej = sorok[1].split('\t')
    rek = [dict(zip(fej, s.split('\t'))) for s in sorok[2:] if s]
    hiany = [r['alak'] for r in rek if r['alak'] not in JAVASLAT]
    folos = [w for w in JAVASLAT if w not in {r['alak'] for r in rek}]
    if hiany or folos:
        sys.exit(f'HIBA: javaslat nélküli alak: {hiany}; jelölt nélküli javaslat: {folos}')
    hj = hashlib.sha256(open(a.jeloltek, 'rb').read()).hexdigest()[:12]
    with open(KI, 'w', encoding='utf-8', newline='\n') as o:
        o.write(f'# proveniencia: {prov_j.replace("proveniencia: ", "")} (jelölt-lista sha256:{hj}) + manual (a szótári alak modell-javaslat '
                f'a DT130 és a DT-F94a/b szerint, modell: claude-opus-5-5, a hibrid v3 befagyasztása után, a hibrid futtatása ELŐTT; '
                f'eszkozok/szoto/minta4_ir.py) | ts={a.ts}\n')
        o.write('# allapot: független minta; ellenorzes=modell_ellenorizetlen minden sorban — a felhasználó soronként ellenőrzi és ő '
                'írja felhasznalo-ra (F94.3 ⛔); a mérés (meres.py --csak-felhasznalo) csak a felhasznalo sorokon. A [bizonytalan: …] jelölésű '
                'sorok döntést kérnek. A strong a repó párosításából (5Móz, 1Sám, Péld, Ez); Mk, Ján, Róm, Jel nincs párosítva: üres\n')
        o.write('\t'.join(OSZLOPOK) + '\n')
        for r in rek:
            j = JAVASLAT[r['alak']]
            sor = dict(alak=r['alak'], gyakorisag=r['gyakorisag'], kategoria=r['kategoria'], ellenorzes='modell_ellenorizetlen',
                       pelda_igehely=r['pelda_igehely'], strong=strong(r['alak'], r['pelda_igehely']), **j)
            if any('\t' in v for v in sor.values()):
                sys.exit('HIBA: tab a mezőben')
            o.write('\t'.join(sor[k] for k in OSZLOPOK) + '\n')
    print(f'{KI}: {len(rek)} sor; bizonytalan: {sum(1 for r in rek if "[bizonytalan" in JAVASLAT[r["alak"]]["indoklas"])}')


if __name__ == '__main__':
    main()
