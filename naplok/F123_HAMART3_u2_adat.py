# -*- coding: utf-8 -*-
"""F123 HAMART-001 új cikk, U2 — a DT-F123ha döntésének átvezetése a jelöltekbe.

Ír (a nem érintett sorok bájtra egyezésének kontrolljával, split('\\t'), CLAUDE.md):
  - adat/jeloltek.tsv: a 109 HAMART-001 `nyitva` sor döntése, olvasói indoklással (belső jel nélkül) és
    `dontes_ref`-fel; négy új `beépítve` sor a szűretlen blokkokból kiemelt helyekre (1Móz 7:4, 7:23,
    Sof 1:2-3, Jer 51:25);
  - adat/elutasitasi_okok.tsv: a HAMART-001 hat új elutasítási oka (az 1/b. blokk címkéi).
Szerző: claude-opus-5-5. Döntés: DT-F123ha (az orkesztrátor döntése a felhasználó felhatalmazásával, 2026-11-05).
"""
import io
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ID = 'HAMART-001'
DATUM = '2026.11.05'
REF = 'DT-F123ha'
PROV = 'scope=manual | forras=F123 HAMART-001 új cikk, U2 (DT-F123ha) | ts=2026-11-05'

# --- egyedi döntések: igehely -> (dontes, indoklas)
D = {}

KIALTO = ('A föld itt tanúként szólal meg a kiontott vér mellett. Ez a kiáltó vér képe, amely az 1Móz 4:10 '
          'vérkiáltásából nő ki, és önálló motívum; a hely nem az átok, a föld és a romlás láncát folytatja.')
D['Jób 16:18'] = ('elutasítva', KIALTO)
D['Jób 31:38'] = ('elutasítva', KIALTO)

SZOV = ('A romlás igéje (sáchat) itt a szövetséges nép hűtlenségét nevezi meg. Hiányzik belőle az, ami a Zsolt 14:1 '
        'és 53:2 helyeit az 1Móz 6:12-höz köti: az egyetemes ítélet („nincs, a ki jót cselekedjék”) és Isten '
        'tekintete az egész emberiségre; a hely nem a Genezis romlás-mondatára utal vissza.')
D['5Móz 4:25'] = ('elutasítva', SZOV)
D['Bír 2:19'] = ('elutasítva', SZOV)
D['Sof 3:7'] = ('elutasítva', SZOV)
D['5Móz 9:26-27'] = ('elutasítva', 'Mózes közbenjárása a szövetséges népért: az Úr ne veszítse el (sáchat) a népet a '
                     'bűne miatt. A romlás és a bűn szava egymás mellett áll, de a hely a pusztában vétkező népre '
                     'szól, és nem a Genezis egyetemes romlás-mondatára utal vissza.')
D['Hós 9:9'] = ('elutasítva', 'A szövetséges nép mélyen megromlott, „mint Gibea napjaiban”: a próféta itt a Bírák '
                'könyvének gibeai gyalázatára utal vissza, nem a Genezisre; a romlás és a bűn szava ezért a lánc '
                'nélkül áll egymás mellett.')

D['2Pét 3:10'] = ('elutasítva', 'A hely a 2Pét 3:6-7 sorának folytatása. A tűz-ítélet, az elemek felbomlása és a föld '
                  'megégése önmagában nem utal vissza az özönvízre; a visszautalás a 3:6-7-ben áll, és az a '
                  'motívumban van.')
D['2Pét 3:12'] = ('elutasítva', 'A hely a 2Pét 3:6-7 sorának folytatása. Az Isten napjának várása és az egek '
                  'felbomlása önmagában nem utal vissza az özönvízre; a visszautalás a 3:6-7-ben áll, és az a '
                  'motívumban van.')
D['Ez 28:17'] = ('elutasítva', 'A hely az Ez 28:16 sorának folytatása: ott áll a „megtelt erőszakkal” szókapcsolat. '
                 'A 28:17 Tírusz fejedelmének megrontott bölcsességét és földre vetését mondja ki, új láncelem nélkül.')
D['Mik 6:13'] = ('elutasítva', 'A hely a Mik 6:12 sorának folytatása: a 6:12 mondja ki, hogy a gazdagok megteltek '
                 'erőszakkal, a 6:13 a rájuk mért csapást, új láncelem nélkül.')

D['2Tim 3:8'] = ('elutasítva', 'A φθείρω-szócsalád tagja áll benne („romlott elméjű emberek”), de erkölcsi jellemzésként, '
                 'mint a korábban elutasított Ef 4:22 és Júd 1:10 helyeken: a szócsalád tagjai, de nem a föld '
                 'romlását mondják.')

ENYESZET = ('A test enyészete a sírban: a hely a Zsolt 16:10 idézete vagy magyarázata („nem látja a rothadást”). Ez a '
            'romlandóság antropológiai és eszkatológiai értelme, mint a korábban elutasított 1Kor 15:42 és 15:50 '
            'helyeken, nem a föld romlása.')
for h in ('ApCsel 2:27', 'ApCsel 2:31', 'ApCsel 13:34', 'ApCsel 13:35', 'ApCsel 13:36', 'ApCsel 13:37'):
    D[h] = ('elutasítva', ENYESZET)
ROMLANDO = ('A romlandó és a romolhatatlan ellentéte áll benne: a romlandóság általános értelme, mint a korábban '
            'elutasított 1Kor 15:42 és 15:50 helyeken. A teremtett világ romlását az Újszövetségben csak a Róm 8:20-22 '
            'köti a lánchoz.')
for h in ('Róm 1:23', '1Kor 9:25', '1Kor 15:53', '1Kor 15:54', '1Pét 1:18', '1Pét 1:23'):
    D[h] = ('elutasítva', ROMLANDO)

D['1Kir 8:34-35'] = ('elutasítva', 'A bűn és a föld itt a szövetségi rendben kapcsolódik: a vétek miatt a nép fogságba '
                     'kerül a földről, vagy elmarad az eső, és a megtérés után visszakapja. Ez a szövetségi átok rendje, '
                     'mint a korábban elutasított 5Móz 28:23-24 és 3Móz 26:20 helyeken; a szöveg a Genezisre nem utal '
                     'vissza.')
D['2Krón 6:25-26'] = ('elutasítva', 'A bűn és a föld itt a szövetségi rendben kapcsolódik: a vétek miatt a nép fogságba '
                      'kerül a földről, vagy elmarad az eső, és a megtérés után visszakapja. Ez a szövetségi átok '
                      'rendje, mint a korábban elutasított 5Móz 28:23-24 és 3Móz 26:20 helyeken; a szöveg a Genezisre '
                      'nem utal vissza.')
FOLDVESZTES = ('a „föld színéről” fordulat itt a szövetségi rendben áll: egy királyi ház vagy a nép bűne miatti '
               'földvesztést mondja. A fordulat közös az 1Móz 6:7-tel, de a hely nem az egyetemes ítéletre utal vissza; '
               'hogy a föld elvesztése a kiűzetés ismétlése-e, a következő kiadás nyitott kérdése.')
D['1Kir 13:34'] = ('elutasítva', 'Jeroboám házának bűne és kiirtása: ' + FOLDVESZTES)
D['1Kir 14:15-16'] = ('elutasítva', 'Izrael kigyomlálása a jó földről Jeroboám bűne miatt: ' + FOLDVESZTES)
D['2Kir 17:22-23'] = ('elutasítva', 'Izrael fogságba vitele a földjéről Jeroboám bűnei miatt: ' + FOLDVESZTES)

D['5Móz 19:15-16'] = ('elutasítva', 'Jogi szabály a tanúkról: a bűn és az erőszak (a hamis tanúé) szava egymás mellett '
                      'áll, de a láncra való visszautalás nélkül.')
D['Neh 9:1-2'] = ('elutasítva', 'Bűnbánati gyűlés: a fejre hintett por (a föld szava) és a bűnvallás egymás mellett áll, '
                  'de a láncra való visszautalás nélkül.')
D['Zsolt 25:18-19'] = ('elutasítva', 'Panasz-zsoltár: a zsoltáros a bűnei bocsánatát kéri, és menedéket az erőszakos '
                       'ellenségek elől; a bűn és az erőszak szava egymás mellett áll, de a láncra való visszautalás '
                       'nélkül.')

D['Hós 10:8'] = ('beépítve', 'Beépítve: „tövis és bogáncs nő fel oltáraikon”, és a vers megnevezi Izrael bűnét is. Az '
                 '1Móz 3:18 szópárja (kóc vedardar) az Ószövetségben csak itt tér vissza, és itt is a bűn '
                 'következményeként, a föld termése helyén.')
D['Ez 12:19'] = ('beépítve', 'Beépítve: a föld (adamá) „pusztává lesz teljességéből, a benne lakók erőszaka miatt”. '
                 'A vers együtt hozza az erőszak (chámász), a föld és a teljesség (a „megtelt” igének tövéből) szavát, '
                 'vagyis az 1Móz 6:11-13 szerkezetét. Ez különbözteti meg az elutasított „föld színéről” helyektől, '
                 'amelyekben csak a földvesztés fordulata áll, az erőszakkal megtelt föld szókapcsolata nélkül.')
D['Mal 3:11'] = ('beépítve', 'Beépítve: a 3:9 átka (arar) után az Úr megígéri, hogy a pusztító „nem rontja meg (sáchat) '
                 'a föld (adamá) gyümölcsét”. Az átkozott föld termésének helyreállítása az 1Móz 3:17-18 és 4:12 '
                 'megfordítása, ahogy az Ézs 60:18 az erőszakét.')

JEL22 = ('Beépítve, tematikus, nem lexikai jelöléssel: „semmi átok nem lesz többé” (κατανάθεμα, a kritérium szava '
         'nélkül). A kánon záró képe, az élet fájával (Jel 22:2) együtt, az 1Móz 3 átkának megszűnését mondja ki.')

# --- az összesítő (blokk-) sorok: igehely -> indoklás (a versszám a meglévő forras_kereses-ből)
BLOKK_STRONG = {
    '1Kir 7:46': ('az אֲדָמָה (adamá, föld, talaj) szava áll bennük, általános használatban: a föld mint talaj, szántó, '
                  'ország vagy a „föld színe” fordulat, a láncra való visszautalás nélkül. A „föld színéről” fordulat '
                  'szövetségi földvesztést mondó helyei is ide tartoznak; hogy a föld elvesztése a kiűzetés '
                  'ismétlése-e, a következő kiadás nyitott kérdése. Az 1Móz 7:4, 7:23 és a Sof 1:2-3 saját sorban, '
                  'beépítve áll.'),
    '1Kir 8:36': ('a חַטָּאת (chattát, bűn, bűnáldozat) szava áll bennük, általános használatban: a bűnáldozat '
                  'törvényeiben, bűnvallásban és a bűn megnevezéseként, a láncra való visszautalás nélkül. A motívumban '
                  'a szó a lánc első bűn-szavaként (1Móz 4:7) és a tövis-képpel együtt (Hós 10:8) áll.'),
    '1Krón 12:17': ('a חָמָס (chámász, erőszak) szava áll bennük, általános használatban: a „megtelt erőszakkal” és a '
                    '„hallatszik az erőszak” szókapcsolata nélkül, a láncra való visszautalás nélkül.'),
    '1Krón 20:1': ('a שָׁחַת (sáchat, megront, elpusztít) szava áll bennük, általános használatban: katonai vagy fizikai '
                   'pusztítás, egy nép vagy ház bűne, az egyetemes romlás szerkezete nélkül. A Jer 51:25 saját sorban, '
                   'beépítve áll.'),
}
SZOTAR_VEG = ('a szótár ezeket a verseket a szó szócikkében idézi, de a Károli-versben a szó nem áll: a szótár a héber '
              'vagy a görög versszámozás szerint idéz, vagy rokon alakot ért. Ahol a szó ténylegesen áll, ott a '
              'szövegkeresés találja meg.')
KAROLI_VEG_REGI = ' Elbírálás az értelmező menetben, blokkban.'
KAROLI_VEG_UJ = ' A kritérium szava nélkül a versek nem tartoznak a motívumba.'
KAROLI_KEZI = '; kézi olvasásra marad. A versekben a motívum egyik szava sem áll.'
KAROLI_KEZI_UJ = '. A versekben a kritérium egyik szava sem áll, ezért nem tartoznak a motívumba.'

UJ_SOROK = [
    ('1Móz 7:4', 'Beépítve: „eltörlök a föld színéről minden állatot, melyet teremtettem”. Az 1Móz 6:7 kimondása '
                 '(eltöröl, a föld színéről) itt szó szerint megismétlődik, az özönvíz bejelentésében.'),
    ('1Móz 7:23', 'Beépítve: „eltörle az Isten minden állatot, a mely a föld színén vala”. Az 1Móz 6:7 kimondásának '
                  'végrehajtása, ugyanazzal az igével és ugyanazzal a felsorolással (embertől a baromig, a '
                  'csúszó-mászóig és az égi madárig).'),
    ('Sof 1:2-3', 'Beépítve: „kiirtok mindent a földnek színéről … embert és barmot, az ég madarait”. A próféta az '
                  '1Móz 6:7 egyetemes felsorolását (ember, barom, madár) és fordulatát idézi fel. Ez különbözteti meg '
                  'az elutasított „föld színéről” helyektől, amelyek egy ház vagy a nép földvesztését mondják, az '
                  'egyetemes felsorolás nélkül.'),
    ('Jer 51:25', 'Beépítve: Babilon „romlásnak hegye, … a ki az egész földet megrontottad”. A romlás igéje (sáchat) és '
                  'az egész föld együtt az 1Móz 6:11-13 mondata, és pontos előképe a Jel 19:2-nek, ahol Babilon '
                  '„megrontotta a földet”.'),
]


def main():
    ut = 'adat/jeloltek.tsv'
    nyers = io.open(ut, encoding='utf-8', newline='').read()
    sorvege = '\r\n' if '\r\n' in nyers else '\n'
    sorok = nyers.split(sorvege)
    fejlec_i = next(i for i, l in enumerate(sorok) if l and not l.startswith('#'))
    h = sorok[fejlec_i].split('\t')
    ix = {n: i for i, n in enumerate(h)}
    valt, felhasznalt = 0, set()
    ki = []
    for i, l in enumerate(sorok):
        if i <= fejlec_i or not l or l.startswith('#'):
            ki.append(l)
            continue
        r = l.split('\t')
        if r[0] != ID or r[ix['dontes']] != 'nyitva':
            ki.append(l)
            continue
        ige, fk, ind = r[ix['igehely']], r[ix['forras_kereses']], r[ix['indoklas']]
        if ige == 'Jel 22:3':
            r[ix['dontes']], r[ix['indoklas']] = 'beépítve', JEL22
            r[ix['forras_kereses']] = fk.replace('blokk-sor (DT564 minta): 1 vers, a sor igehelye a blokk egy verse',
                                                 'egy vers (átok-csoport)')
        elif ige in D and 'blokk-' not in fk:
            r[ix['dontes']], r[ix['indoklas']] = D[ige]
        elif 'Strong-háló, blokk-sor' in fk and ige in BLOKK_STRONG:
            fej = ind.split(': ', 1)[0]
            r[ix['dontes']], r[ix['indoklas']] = 'elutasítva', fej + ': ' + BLOKK_STRONG[ige]
        elif 'szótár-háló' in fk and 'blokk-' in fk:
            fej = ind.split(': ', 1)[0]
            r[ix['dontes']], r[ix['indoklas']] = 'elutasítva', fej + ': ' + SZOTAR_VEG
        elif 'Károli-szó háló' in fk and 'blokk-' in fk and (KAROLI_VEG_REGI in ind or ind.endswith(KAROLI_KEZI)):
            r[ix['dontes']] = 'elutasítva'
            if ind.endswith(KAROLI_KEZI):
                r[ix['indoklas']] = ind[:-len(KAROLI_KEZI)].rstrip() + KAROLI_KEZI_UJ
            else:
                r[ix['indoklas']] = ind.replace(KAROLI_VEG_REGI, KAROLI_VEG_UJ)
        else:
            raise SystemExit('nem kezelt nyitva sor: %s | %s' % (ige, fk[:80]))
        r[ix['datum']] = DATUM
        r[ix['dontes_ref']] = REF
        felhasznalt.add(ige)
        valt += 1
        ki.append('\t'.join(r))
    hianyzo = [k for k in D if k not in felhasznalt]
    if hianyzo:
        raise SystemExit('a döntéslista helye nem volt nyitva: %s' % hianyzo)
    # új beépítve sorok a meglévő HAMART-001 sorok után
    utolso = max(i for i, l in enumerate(ki) if l.startswith(ID + '\t'))
    uj = []
    for ige, ind in UJ_SOROK:
        r = [''] * len(h)
        r[ix['id']], r[ix['igehely']] = ID, ige
        r[ix['forras_kereses']] = ('F123 U2: a teljesség-mérés Strong-hálójának szűretlen versei, mintamérés '
                                   '(a föld színe + pusztító ige; a romlás igéje + föld) | ' + PROV)
        r[ix['dontes']], r[ix['indoklas']] = 'beépítve', ind
        r[ix['datum']], r[ix['jelolt_tipus']], r[ix['dontes_ref']] = DATUM, 'elofordulas', REF
        uj.append('\t'.join(r))
    ki = ki[:utolso + 1] + uj + ki[utolso + 1:]
    # kontroll: a nem HAMART-001 sorok bájtra azonosak
    regi_mas = [l for l in sorok if not l.startswith(ID + '\t')]
    uj_mas = [l for l in ki if not l.startswith(ID + '\t')]
    assert regi_mas == uj_mas, 'nem HAMART-001 sor változott'
    io.open(ut, 'w', encoding='utf-8', newline='').write(sorvege.join(ki))
    print('jeloltek: döntött sor %d, új sor %d' % (valt, len(uj)))

    # elutasítási okok
    ut2 = 'adat/elutasitasi_okok.tsv'
    nyers2 = io.open(ut2, encoding='utf-8', newline='').read()
    sv2 = '\r\n' if '\r\n' in nyers2 else '\n'
    p2 = 'scope=manual | forras=F123 HAMART-001 új cikk, U2 (DT-F123ha; az orkesztrátor döntése a felhasználó felhatalmazásával) | ts=2026-11-05'
    uj_okok = [
        ('98', '^összesítő sor .*általános használatban', 'a szó áll, de általános használatban, a lánc nélkül (összesítő sor)',
         'a kritérium lexémája áll a versekben, a genezisi láncra való visszautalás nélkül'),
        ('99', '^összesítő sor .*a szótár ezeket a verseket', 'a szótár idézi, de a Károli-versben a szó nem áll (összesítő sor)',
         'versszámozási eltérés vagy rokon alak'),
        ('122', 'szövetséges nép', 'a romlás igéje a szövetséges nép hűtlenségére, az egyetemes szerkezet nélkül',
         'a sáchat erkölcsi használata Izraelre'),
        ('123', '^a hely az? .* sorának folytatása', 'egy bent lévő hely folytatása, a szerkezet ott áll',
         'a szomszédos vers a motívumban van'),
        ('124', 'szövetségi rend', 'a föld elvesztése vagy terméketlensége a szövetségi rendben, nem a lánc',
         'szövetségi átok és földvesztés'),
        ('125', '^jogi szabály|^bűnbánati|^panasz', 'jogi, bűnbánati vagy panasz-használat, a lánc nélkül',
         'a két szó egymás mellett, visszautalás nélkül'),
    ]
    sorok2 = nyers2.rstrip(sv2).split(sv2)
    for s, minta, cimke, megj in uj_okok:
        sorok2.append('\t'.join([s, ID, minta, cimke, megj, p2]))
    io.open(ut2, 'w', encoding='utf-8', newline='').write(sv2.join(sorok2) + sv2)
    print('elutasitasi_okok: +%d' % len(uj_okok))


if __name__ == '__main__':
    main()
