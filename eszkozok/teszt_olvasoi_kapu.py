#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Az olvasoi_kapu.py tesztjei.

Negatív tesztek: a lap-átvilágítás (2026-11-02) konkrét, gépesíthető példái (A/T/G-sorok), szó szerint vagy
rövidítve, egy minimális lapba ágyazva -- a kapunak el kell kapnia őket. Pozitív tesztek: az arany lap
(ISTENTISZT-001) jó részeinek alakja -- ezekre nem jelezhet.

Használat: python eszkozok/teszt_olvasoi_kapu.py
"""
import os
import sys
import unittest

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import olvasoi_kapu as K  # noqa: E402

KOLOFON_JO = """## Kolofon

| Mező | Érték |
|---|---|
| Státusz | publikálható (`v4`, 2026.11.02) |
| Kereszthivatkozás-napló | generált (`adat/jeloltek.tsv`) |
| Sablon-megfelelőség | v12 |
| Kiadás | 1 |
| Próza modellje | `manual` |

**Változásjegyzék**

| Kiadás | Dátum | Mi változott |
|---|---|---|
| 1 | 2026.11.02 | Első kiadás. |
"""

TABLA_FEJ = """## 1. Előfordulások

| Igehely | Kulcsszó | Jelentés (a szó) | Funkció (a motívumban) | PaRDeS-szint |
|---|---|---|---|---|
"""


def lap(kivonat='', tabla_sorok=None, egy_a='', tobbi='', kolofon=KOLOFON_JO):
    sorok = tabla_sorok if tabla_sorok is not None else [
        '| [1Móz 4:26](#ige) | segítségül hívni | hívni | 🌱 alap-előfordulás | Drash |']
    return '\n'.join(['# 📖 X-001 — Próba', '', '## Kivonat', '', kivonat, '', TABLA_FEJ + '\n'.join(sorok),
                      '', '#### 1/a. Az igehelyek szövege', '', egy_a, '', tobbi, '', kolofon])


def meres(szoveg):
    return K.lap_meres(szoveg, kh=False, atvett=False, arany=False)[0]


def azonositok(szoveg, suly=None):
    return {t['azonosito'] for t in meres(szoveg) if suly is None or t['sulyossag'] == suly}


class Negativ(unittest.TestCase):
    """Az átvilágítás példái: a kapunak jeleznie kell."""

    def jelez(self, szoveg, azon, suly=K.BUKAS):
        tal = [t for t in meres(szoveg) if t['azonosito'] == azon and t['sulyossag'] == suly]
        self.assertTrue(tal, '%s/%s nem jelzett; találatok: %s' % (azon, suly, meres(szoveg)))
        return tal

    def test_A1_ures_funkcio_cella(self):
        sorok = ['| [1Móz 37:35](#ige) | a sírba | alvilág · 1 | — | Remez |',
                 '| [1Móz 42:38](#ige) | a koporsóba | alvilág · 1 | — | Remez |']
        t = self.jelez(lap(tabla_sorok=sorok), 'FUNKCIO_URES')
        self.assertEqual(t[0]['db'], 2)

    def test_cella_ismetles_tartomany_sor(self):
        # F123.HAMART3: a tartomány-sor versenként ugyanazt a jelentést írta a cellába
        elem = 'megátkozni; átkot kimondani [ⓘ](/szo/H0779)'
        sorok = ['| [5Móz 27:15-26](#ige) | Átkozott | átkoz · Qal | formula | Remez | H0779 | %s; %s |' % (elem, elem)]
        self.jelez(lap(tabla_sorok=sorok), 'CELLA_ISMETLES')

    def test_nave_angol_es_nyers_kod(self):
        # F123.HAMART3 javítókör: a Nave-blokk angol témaneve és a nyers karakterkód BUKÁS; a title-ben álló angol nem
        blokk = '## 2. Szótári háttér\n\n#### 12. Tematikus index (témák és igehely-hivatkozások)\n\n'
        self.jelez(lap(tobbi=blokk + '- **átok (*CURSE*)** — 7 motívumvers / 51 témavers (13,7%): 1Móz 3:14'), 'NAVE_ANGOL')
        self.jelez(lap(tobbi=blokk + '  - Kainé, hogy „bujdosó” legyen (&#8220;a fugitive,&#8221): 1Móz 4:14'),
                   'NAVE_ANGOL')
        jo = lap(tobbi=blokk + '- **<span title="CURSE">átok</span>** — 7 motívumvers / 51 témavers (13,7%): 1Móz 3:14')
        self.assertNotIn('NAVE_ANGOL', azonositok(jo))

    def test_A4_belso_jelolesek_az_1b_indokban(self):
        szoveg = lap(tobbi='## 1/b. Kizárt és vizsgált helyek\n\n| Igehely | Miért lett jelölt | Döntés és indok |\n'
                     '|---|---|---|\n| 2Móz 12:29 | gépi keresés | **elutasítva** — Minősítési mérce (a #123 2e. 4. '
                     'küszöbdöntése; orkesztrátor): „Megerősítem” (DT414, DONTESEK.md; ELLENOR_F123_ALVIL-001 E8) |')
        uz = ' '.join(t['uzenet'] for t in self.jelez(szoveg, 'BELSO'))
        for minta in ('#123', 'DT414', 'ELLENOR_', 'orkesztrátor', 'DONTESEK.md'):
            self.assertIn(minta, uz)

    def test_A5_T5_G1_masolt_karoli_kh(self):
        szoveg = lap(tobbi='## 4. Kereszthivatkozások\n\n#### ApCsel 2:27\n- Károli-KH: 1Móz 46:27\n\n'
                     '#### Ézs 34:11\n- Károli-KH: Ésa 66:12\n\n#### Zsolt 116:13\n- Károli-KH: Róm 3:13\n')
        tal = K.ell_kh(K.tagol(szoveg))
        self.assertEqual({t['idezet'].split(' →')[0] for t in tal}, {'ApCsel 2:27', 'Ézs 34:11', 'Zsolt 116:13'})
        self.assertTrue(all(t['sulyossag'] == K.FIGY for t in tal))

    def test_A7_kivonat_szam(self):
        sorok = ['| [Mt %d:1](#ige) | hádész | alvilág | f | Remez |' % i for i in range(1, 9)]
        szoveg = lap(kivonat='A szó az Ószövetségben él, az Újszövetségben — teljes szövegvizsgálat szerint — '
                             'tíz ᾍδης-előfordulásban.', tabla_sorok=sorok)
        t = self.jelez(szoveg, 'KIVONAT_SZAM', K.FIGY)
        self.assertIn('(10)', t[0]['uzenet'])
        self.assertIn('újszövetségi', t[0]['uzenet'])

    def test_A8_idezet_nem_a_karoli_szovege(self):
        egy_a = ('<a id="ige-1móz-37-35"></a>\n**1Móz 37:35**\n*Felkelének pedig minden ő fiai … hanem monda: Sírva '
                 'megyek fiamhoz a sírba; és siratá őt az atyja.*\nJákób gyásza: „leszállok fiamhoz a Seolba, gyászolva”.')
        self.jelez(lap(egy_a=egy_a), 'IDEZET')

    def test_A10_G8_egyenes_idezojel(self):
        self.jelez(lap(kivonat='Pál idézi („"Halál! hol a te fullánkod?"”).'), 'IDEZOJEL')
        self.jelez(lap(kivonat='„segítségül hívni az Úr nevét" formulát követi.'), 'IDEZOJEL')

    def test_A11_T7_atiras_egyseg(self):
        szoveg = lap(kivonat='Az ᾍδης (*hádész*) a görög alvilág.',
                     tobbi='## 2. Szótári háttér\n\nA ᾅδης (hadész) szó.')
        self.jelez(szoveg, 'ATIRAS')
        szoveg = lap(kivonat='A תֹהוּ (tóhú) és a בֹהוּ (bóhú) pár; a *tohu va-vohu* kifejezés.')
        self.jelez(szoveg, 'ATIRAS_VALT', K.FIGY)

    def test_A11_T16_regi_konyvrovidites(self):
        szoveg = lap(tobbi='## 4. Kereszthivatkozások\n\n#### Jón 2:3\n- Károli-KH: Ésa 53:10-12\n- Károli-KH: Csel 2:31'
                           '\n- Károli-KH: Mát 4:13\n- Károli-KH: Ezék 16:36\n')
        kulcsok = {t['uzenet'].split('„')[1].rstrip('”') for t in self.jelez(szoveg, 'KONYV')}
        self.assertEqual(kulcsok, {'Ésa', 'Csel', 'Mát', 'Ezék'})

    def test_A12_T8_G9_bdb_szovegtisztasag(self):
        szoveg = lap(tobbi='## 2. Szótári háttér\n\nShe®°ôl, alvilág; nőnemű főnév^**Zsolt 86:13**, l. Albr^ZAW\n\n'
                           'ítélete alatt álló földről; קַותֿֿהֹוּ וְאַבְנֵי בֹהוּ Ézs 34:11\n')
        nevek = {t['uzenet'] for t in self.jelez(szoveg, 'BDB_JEL')}
        self.assertTrue({'nyers ^ elválasztó', 'torzult jel (® / °)', 'rafe (ֿ) pontjel a héber szóban'} <= nevek)

    def test_A23_dupla_vesszo(self):
        self.jelez(lap(tobbi='## 2. Szótári háttér\n\nᾅδης,, ὁ (a régebbi alakból) a klasszikus nyelvben\n'),
                   'BDB_JEL')

    def test_T9_nyitott_zarojel_a_szotarban(self):
        szoveg = lap(tobbi='## 2. Szótári háttér\n\nátvitt értelemben arról, ami üres, valótlan, mint a bálványok '
                           '1Sám 12:21 (gyűjtőnévként\n')
        self.jelez(szoveg, 'ZAROJEL')

    def test_A16_T12_szint_alatti_blokk(self):
        szoveg = lap(tobbi='## 5. Kapcsolatok\n\nEz a rész a kapcsolatokat mutatná; ennél a motívumnál még nincs ilyen.\n')
        self.jelez(szoveg, 'SZINT_ALATT', K.FIGY)

    def test_A18_T13_kolofon_hianyos(self):
        kolofon = ('## Kolofon\n\n| Mező | Érték |\n|---|---|\n| Státusz | feldolgozás alatt (`v1`, 2026.09.25) |\n'
                   '| Kereszthivatkozás-napló | — |\n| Sablon-megfelelőség |  |\n')
        uz = {t['uzenet'] for t in self.jelez(lap(kolofon=kolofon), 'KOLOFON')}
        self.assertIn('a Kolofonban nincs „Kiadás” sor', uz)
        self.assertIn('a Kolofonban nincs „Próza modellje” sor', uz)
        self.assertIn('a Kolofonban nincs Változásjegyzék', uz)
        self.assertIn('üres törzsadat-mező: Kereszthivatkozás-napló', uz)
        self.assertIn('üres törzsadat-mező: Sablon-megfelelőség', uz)

    def test_A21_G7_belso_id_a_prozaban(self):
        egy_a = ('**1Kir 18:25**\n*És monda Illés …*\nA Baál-próféták felszólítása. Kontraszt (DT476 K5): a besém után '
                 'nem JHVH áll.\nFunkció: a próbatétel gyakorlati végrehajtása')
        self.jelez(lap(egy_a=egy_a), 'BELSO')

    def test_A22_T11_G4_angol_es_zsargon(self):
        for mondat in ('Ez a study fő ívét adja.', 'A tanítói táblában 17 tanítónál gap.',
                       'K1_passziv: passzív/megnevezett (was called)', 'az LXX_OS-ben Strong-szám nélkül áll',
                       'az Isa.34.11 lista az Isa.40.11 másolata', 'A P3 teljes scanje szerint.'):
            self.jelez(lap(kivonat=mondat), 'ANGOL')

    def test_T3_pont_hivatkozas(self):
        szoveg = lap(kivonat='Kapcsolt hely, de nem előfordulás (3. pont, Remez). A görög nem így fordítja '
                             '(2. pont, „Septuaginta”). Lásd a 9. pontot.',
                     tobbi='## 2. Szótári háttér\n\nszöveg\n\n## 3. LXX-fordítói döntések\n\nszöveg\n')
        uz = [t['uzenet'] for t in self.jelez(szoveg, 'PONT')]
        self.assertTrue(any('Remez' in u for u in uz))
        self.assertTrue(any('Septuaginta' in u for u in uz))
        self.assertTrue(any('nincs 9. szakasz' in u for u in uz))

    def test_T3_P_lepesjel(self):
        self.jelez(lap(kivonat='A három vers számlálásából következik (P4); a P2 mező-hipotézise szerint.'), 'BELSO')

    def test_T4_kivonat_lxx_mindharom(self):
        szoveg = lap(kivonat='A Septuaginta a párt mindhárom helyen másként fordítja.',
                     tobbi='## 3. LXX-fordítói döntések\n\n*Összesítés: egyező=0, eltérő=2, LXX-minusz=0, '
                           'kutatói azonosítás függőben=1, szamozas_elteres=0.*\n')
        self.jelez(szoveg, 'KIVONAT_SZAM', K.FIGY)

    def test_T10_G6_hianyjelzes(self):
        sorok = ['| [1Móz 1:2](#ige) | x | H0922: *(nincs címke: tagolatlan)* | f | Peshat |',
                 '| [1Móz 4:26](#ige) | x | H8034: *(nincs hozzárendelés)* ⓘ | f | Drash |']
        self.jelez(lap(tabla_sorok=sorok), 'HIANYJEL', K.FIGY)

    def test_T11_manual_a_prozaban(self):
        self.jelez(lap(kivonat='A tagolás (nyelvtani értelmezés, `manual`) szerint.'), 'BELSO')

    def test_T14_motivum_id_link_nelkul(self):
        self.jelez(lap(kivonat='Precedens: KIRALY-001 2Móz 19:6 → 1Pét 2:9.'), 'MOTIVUM_ID', K.FIGY)

    def test_strong_a_szo_es_kiejtese_mellett(self):
        """F123.INDOKLAS: ISTENTISZT-001, a Minősítés jelölt-táblája (Róm 10:12) és az LXX-tábla alakja."""
        t = self.jelez(lap(kivonat='A versben ἐπικαλέομαι áll, de ὄνομα (G3686) nélkül.'), 'BELSO')
        self.assertTrue(any(x['uzenet'].startswith('Strong-szám') for x in t))
        self.jelez(lap(tobbi='## 3. LXX-fordítói döntések\n\n| Igehely | Görög megfelelő |\n|---|---|\n'
                             '| 1Móz 4:26 | ἐπικαλεῖσθαι (epikaleiszthai) (ἐπικαλέω, epikaleó G1941) |\n'), 'BELSO')

    def test_GENKOR_bdb_atirasi_betukeszlet(self):
        """F123.GENKOR: a BDB átírási betűkészletének többi torz jele (N89) is gátló: „Leµi”, „Kor¹n”."""
        nevek = {t['uzenet'] for t in self.jelez(lap(tobbi='## 2. Szótári háttér\n\nhelyesen olvassa Leµi felé\n'),
                                                   'BDB_JEL')}
        self.assertTrue(any('betűkészlete' in n for n in nevek), nevek)
        self.jelez(lap(tobbi='## 2. Szótári háttér\n\nrecitálni (a Kor¹n)\n'), 'BDB_JEL')

    def test_GENKOR_nyitott_zarojel_vazlatsor(self):
        """F123.GENKOR (C2/C3): a gerinc vázlatsora a tagmondat-határon vágott, nyitva maradt zárójellel."""
        self.jelez(lap(tobbi="## 2. Szótári háttér\n\n- `Niph'al 2.c` — megidéztetni (vö. Qal 5\n"), 'ZAROJEL')

    def test_GENKOR_csupasz_strong_a_kezi_prozaban(self):
        """DT-F181b: a csupasz zárójeles Strong-szám a szó és a kiejtés mellett hiba (a generátor jelölt alakra írja)."""
        t = self.jelez(lap(tobbi='## 6. Értelmezés\n\nAz „oltár” (מִזְבֵּחַ, mizbéah, H4196) négy helyen áll.\n'),
                       'BELSO')
        self.assertTrue(any(x['uzenet'].startswith('Strong-szám') for x in t))

    def test_GENKOR_szerzosegi_jeloles(self):
        """DT-F181c: a „(kézi)” / „(generált)” jelölés címsorban és a Tartalomjegyzék magyarázatában is hiba."""
        t = self.jelez(lap(tobbi='## 6. Értelmezés *(kézi)*\n\nSzöveg.\n\n### Minősítés *(generált)*\n\nx\n'),
                       'BELSO')
        self.assertEqual(sum(x['db'] for x in t if x['uzenet'].startswith('szerzőségi')), 2)
        self.jelez(lap(tobbi='## Tartalomjegyzék\n\nA lap szakaszai. A „(kézi)” jelölésű szakaszokat a kutató írta.\n'),
                   'BELSO')

    def test_G5_munkafolyamat_kerdes(self):
        self.jelez(lap(tobbi='## 6. Értelmezés\n\nFel kell-e venni a jeloltek.tsv-be, és át kell-e vezetni '
                             'a tematikus study 2. és 3. pontjába?\n'), 'BELSO')


class Pozitiv(unittest.TestCase):
    """Az arany lap jó részeinek alakja: nem jelezhet."""

    def nincs(self, szoveg, *azon):
        tal = [t for t in meres(szoveg) if t['azonosito'] in azon]
        self.assertEqual(tal, [], tal)

    def test_cella_ket_kulonbozo_elem_nem_hiba(self):
        sorok = ['| [Mk 7:21-23](#ige) | gondolatok | gondolat · 1 | tematikus | Drash | G1261 | '
                 'okoskodás [ⓘ](/szo/G1261); kétely [ⓘ](/szo/G1261) |']
        self.nincs(lap(tabla_sorok=sorok), 'CELLA_ISMETLES')

    def test_GENKOR_jelolt_strong_nem_hiba(self):
        """DT-F181b: a jelölt alak (kiejtés-hivatkozás + halvány felső index) nem belső jel, és a kiejtés-pár látszik."""
        tobbi = ('## 6. Értelmezés\n\nAz „oltár” (מִזְבֵּחַ, [mizbéah](/szo/H4196)<sup class="strong" title="H4196 · oltár">'
                 'H4196</sup>) négy helyen áll.\n')
        self.nincs(lap(tobbi=tobbi), 'BELSO', 'IDEZOJEL', 'ZAROJEL')
        tobbi = ('## 6. Értelmezés\n\nA תְּהוֹם ([tehóm](/szo/H8415)<sup class="strong" title="H8415 · mélység">H8415</sup>) '
                 'lexéma.\n')
        self.nincs(lap(tobbi=tobbi), 'BELSO')
        self.assertTrue(any(k == 'tehóm' for _h, k, _n, _i in K.kiejtes_parok(K.tagol(lap(tobbi=tobbi)))))

    def test_GENKOR_szerzoseg_a_kolofonban_nem_hiba(self):
        kolofon = KOLOFON_JO.replace('| Mező | Érték |', '**Szerzőség.** Az értelmező szakaszok (Kivonat) készítőjét a '
                                     'kiadás nem rögzíti modellnévvel (kézi rögzítés, `manual`); a szerző jóváhagyta.\n\n'
                                     '| Mező | Érték |')
        self.nincs(lap(kolofon=kolofon), 'BELSO')

    def test_strong_oszlop_es_onallo_strong(self):
        """A táblázat „Strong” oszlopa, a címsor és a szó nélkül álló Strong-szám nem belső jel."""
        tobbi = ('## 2. Szótári háttér\n\n### H5303 — נְפִלִים (ne.phil)\n\n| Szó | Kiejtés | Strong |\n|---|---|---|\n'
                 '| שֵׁם | sém | H8034 |\n\nA H7496/H7497 Strong-szám szerinti megoszlás; a kárá (H7121) ige.\n')
        tal = [t for t in meres(lap(tobbi=tobbi)) if t['uzenet'].startswith('Strong-szám')]
        self.assertEqual(tal, [], tal)

    def test_arany_1a_blokk(self):
        egy_a = ('<a id="ige-1móz-4-26"></a>\n**1Móz 4:26**\n*Séthnek is született fia, és nevezé annak nevét Énósnak. '
                 'Akkor kezdték segítségül hívni az Úrnak nevét.*\nA formula első előfordulása — Séth fia, Énós '
                 'nemzedéke; a Kain-vonal önerős civilizációépítése utáni korszakváltás jele.\nFunkció: a motívum '
                 'legelső megjelenése a kánonban, minden későbbi eset erre vezethető vissza')
        self.nincs(lap(egy_a=egy_a), 'IDEZET', 'IDEZOJEL', 'BELSO', 'ANGOL', 'ZAROJEL', 'KONYV')

    def test_karoli_szoveget_idezo_jegyzet(self):
        egy_a = ('**Jóel 2:32**\n*De mindaz, a ki az Úrnak nevét hívja segítségül, megmenekül; mert a Sion hegyén …*\n'
                 'Az ígéret: „mindaz, a ki az Úrnak nevét hívja segítségül, megmenekül”, ezt Péter is idézi.')
        self.nincs(lap(egy_a=egy_a), 'IDEZET')

    def test_glossza_zarojelben_nem_versidezet(self):
        egy_a = ('**1Kir 18:26**\n*És vevék a tulkot …*\nKontraszt: a besém után nem JHVH áll, hanem ha-Báal '
                 '(„a Baálnak nevét hívák”).')
        self.nincs(lap(egy_a=egy_a), 'IDEZET')

    def test_modernizalt_helyesiras_es_kihagyas(self):
        """A Károli régies helyesírása (setétség) és a kihagyott szavak nem tesznek saját fordítássá egy idézetet."""
        egy_a = ('**1Móz 7:11**\n*Noé életének hatszázadik esztendejében, … felfakadának ezen a napon a nagy mélység '
                 'minden forrásai, és az ég csatornái megnyilatkozának.*\nA dekreáció kezdete: „felfakadának a nagy '
                 'mélység forrásai”, a teremtéskor elválasztott vizek újraegyesülnek.\n\n'
                 '**1Móz 1:2**\n*És a föld kietlen és puszta vala, és setétség vala a mélység színén.*\n'
                 'Az ősállapot: „sötétség vala a mélység színén”, a rendezés előtti kép.')
        self.nincs(lap(egy_a=egy_a), 'IDEZET')

    def test_sajat_forditas_jelolve(self):
        egy_a = ('**1Móz 37:35**\n*… Sírva megyek fiamhoz a sírba …*\nJákób gyásza: „leszállok fiamhoz a Seolba, '
                 'gyászolva” (saját fordítás).')
        self.nincs(lap(egy_a=egy_a), 'IDEZET')

    def test_arany_kivonat(self):
        kivonat = ('A motívum az ószövetségi קָרָא בְּשֵׁם יְהוָה (kárá besém JHVH), „segítségül hívni az Úr nevét” '
                   'formulát és újszövetségi folytatását követi: formulaikus azonosság, 1 igehelyen (1 ószövetségi, '
                   '0 újszövetségi). A Septuaginta az ἐπικαλέω (epikaleó) igével adja vissza.')
        self.nincs(lap(kivonat=kivonat), 'IDEZOJEL', 'KIVONAT_SZAM', 'ATIRAS', 'BELSO', 'ANGOL')

    def test_teljes_kolofon(self):
        self.nincs(lap(), 'KOLOFON')

    def test_technikai_dolt_sor_es_proveniencia_kivetel(self):
        tobbi = ('*Ez a blokk a `[ID: X-001]` motívum igehely-sorát fedi az `elofordulasok.tsv`-ből (F131, DT272 (d)).*\n'
                 '\n[^1]: proveniencia: ‹E2› | igazolas: nincs | `adat/bdb_vers_jelentes.tsv` sorszam 39\n')
        self.nincs(lap(tobbi=tobbi), 'BELSO')

    def test_kodcella_es_forras_oszlop(self):
        tobbi = ('## 3. LXX-fordítói döntések\n\n| Igehely | Görög | Egyezés | Forrás |\n|---|---|---|---|\n'
                 '| Jóel 2:32 | ἐπικαλέσηται (epikaleszétai) | egyező | LXX_OS |\n')
        self.nincs(lap(tobbi=tobbi), 'ANGOL')

    def test_sortordelt_bekezdes_zarojele(self):
        tobbi = ('## 6. Értelmezés\n\nA formula konkrét, helyhez kötött kultikus jelhez kapcsolva (oltárépítés '
                 '12:8,\n13:4; 26:25) jelenik meg.\n')
        self.nincs(lap(tobbi=tobbi), 'ZAROJEL')

    def test_szakasz_sajat_alpontja(self):
        tobbi = ('## 2. Szótári háttér\n\nMinden szónál számozott pontok követik egymást; a 2. pont a fő szótár.\n\n'
                 '#### 1. Alapjelentés\n\nx\n\n#### 2. Mélységi szócikk\n\ny\n')
        self.nincs(lap(tobbi=tobbi), 'PONT')

    def test_magyar_is_nem_angol(self):
        self.nincs(lap(kivonat='Ez is jó, az is jó, és az is igaz, hogy be is mutatja.'), 'ANGOL_SOR')

    def test_jo_konyvrovidites_es_apokrif(self):
        self.nincs(lap(kivonat='Lásd 1Móz 4:26; ApCsel 2:21; 1Thessz 4:16; Sir 3:8; Az 5:29 nem tartozik ide.'), 'KONYV')

    def test_karoli_vers_alakja_nem_kiejtes(self):
        egy_a = '**Jón 2:3**\n*… a Seol torkából sikolték …*\nA שְׁאוֹל (seól) a halottak helye, ahová Jónás alászáll.'
        self.nincs(lap(egy_a=egy_a), 'ATIRAS_VALT')


class UjSzerkezet(unittest.TestCase):
    """F178.4: az új szerkezetű lapon (1. Döntési út) a kapu kivétel nélkül mér; a régi lapon a régi mérce."""

    TECH = '*Ez a blokk a `[ID: X-001]` motívum sorait fedi az `adat/elofordulasok.tsv`-ből (G3, DT272).*'

    def test_technikai_sor_az_uj_lapon_bukas(self):
        uj = lap(tobbi='## 1. Döntési út\n\n' + self.TECH)
        self.assertIn('BELSO', azonositok(uj, K.BUKAS))

    def test_technikai_sor_a_regi_lapon_nem(self):
        regi = lap(tobbi='## 3. Valami\n\n' + self.TECH)
        self.assertNotIn('BELSO', azonositok(regi, K.BUKAS))

    def test_felhasznalo_csak_az_uj_lapon(self):
        szoveg = 'A sor a felhasználó döntése szerint maradt.'
        self.assertIn('BELSO', azonositok(lap(tobbi='## 1. Döntési út\n\n' + szoveg), K.BUKAS))
        self.assertNotIn('BELSO', azonositok(lap(tobbi='## 3. Valami\n\n' + szoveg), K.BUKAS))

    def test_kolofon_is_merve_az_uj_lapon(self):
        uj = lap(tobbi='## 1. Döntési út\n\nSemmi.', kolofon=KOLOFON_JO + '\n| Forrás | `motivumok/X-001.md` |')
        self.assertIn('BELSO', azonositok(uj, K.BUKAS))


class Arany(unittest.TestCase):
    """Az arany lap ismert hibái (G-sorok): a javítatlanok megjelennek a valódi lapon, a javítottak nem."""

    MOTIVUM = K.ARANY

    @classmethod
    def setUpClass(cls):
        tal, _ = K.motivum_meres(cls.MOTIVUM)
        cls.tal = tal or []

    def van(self, azon, minta):
        self.assertTrue(any(t['azonosito'] == azon and minta in (t['uzenet'] + t['idezet']) for t in self.tal),
                        '%s / %s nincs a találatok között' % (azon, minta))

    def nincs(self, azon, minta):
        self.assertFalse(any(t['azonosito'] == azon and minta in (t['uzenet'] + t['idezet']) for t in self.tal),
                         '%s / %s a találatok között van' % (azon, minta))

    def test_G1_masolt_kh(self):
        """DT-F156n óta a másolat-gyanús KH-lista nem kerül a lapra: a G1 sorai eltűntek, a kapu nem jelez."""
        self.assertFalse(any(t['azonosito'] == 'KH_MASOLT' for t in self.tal))

    def test_G4_szurojel_es_angol(self):
        """OLVJ.1 óta az 1/b. táblában az olvasói ok áll, a szűrő-jel és az angol címke a lábjegyzetben."""
        self.nincs('BELSO', 'F110')
        self.nincs('ANGOL', 'was called')

    def test_G6_hianyjel(self):
        self.van('HIANYJEL', 'nincs hozzárendelés')

    def test_G7_dt_a_prozaban(self):
        """F194 (az ISTENTISZT-001 2. kiadása) óta a próza nulláról készült, a DT476 nem áll benne."""
        self.nincs('BELSO', 'DT476')

    def test_G8_idezojel(self):
        """OLVJ.2 óta a lap utófeldolgozása az egyenes idézőjelet „…”-ra cseréli."""
        self.assertFalse(any(t['azonosito'] == 'IDEZOJEL' for t in self.tal))

    def test_G9_bdb_jel(self):
        """OLVJ.4 óta a ^ jel nem marad a lapon."""
        self.nincs('BDB_JEL', 'nyers ^')


class AranyHamart(Arany):
    """F194 (az orkesztrátor döntése): a javított G-sorok a HAMART-001 lapján, az új aranyon sem jelennek meg; a
    G6 (a szótári hozzárendelés hiányjele) csak a szópáros ISTENTISZT-001 második szaván áll."""
    MOTIVUM = 'HAMART-001'

    def test_G6_hianyjel(self):
        self.nincs('HIANYJEL', 'nincs hozzárendelés')


class BdbOlvasoiReteg(unittest.TestCase):
    """F104 (DT-F104b): a 4.2 BDB-kártyájának olvasói rétegében nem maradhat feloldatlan rövidítés, belső címke vagy nyers
    sorszám; az apparátusban igen. Csak az új szerkezetű, kétrétegű kártyát hordozó lapon fut."""

    def kartya(self, olvasoi, apparatus='(J) Dl Pr 105 BDB2699 sorszám 9', marker=True):
        import lexikon_general as LG
        app = ['', LG.APPARATUS_KEZDET % 'H0001', '', '<details>', '<summary>Szótári apparátus</summary>', '', apparatus, '',
               '</details>', '', LG.APPARATUS_VEGE % 'H0001'] if marker else ['', apparatus]
        return '\n'.join(['#### 4.2. Mélységi szócikk', '', '##### H0001 — אָב (áv) · BDB', '', olvasoi] + app +
                         ['', '#### 4.3. Teológiai szócikk', '', 'Semmi.'])

    def bdb(self, szoveg):
        return [t for t in meres(szoveg) if t['azonosito'] == 'BDB_OLVASOI']

    def test_tiszta_olvasoi_reteg(self):
        self.assertEqual(self.bdb(lap(tobbi='## 1. Döntési út\n\n' + self.kartya('- **1.** apa, atya'))), [])

    def test_hibak_az_olvasoi_retegben(self):
        for hibas in ('- 1. apa (J)', '- 1. apa_224', '- 1. apa, l. Dl Pr 105', '- 1. a szótár sorszám 9 szerint',
                      '- 1. BDB2699 apa', '- 1. apa (nincs címke: 1.b)', '- 1. א׳ apa', '- 1. apa (Klo)'):
            self.assertTrue(self.bdb(lap(tobbi='## 1. Döntési út\n\n' + self.kartya(hibas))), hibas)

    def test_f187_szocikk_sorszam_fej_es_ismetles(self):
        for hibas in ('- *1. szócikk*', '- *II. szócikk*', '**A motívum helyein:** 1Móz 4:7 → a szócikk feje (alakok)',
                      '**A motívum helyein:** 1Móz 3:17, 3:23 → 1. föld · 1Móz 3:23 → 3. anyag.'):
            self.assertTrue(self.bdb(lap(tobbi='## 1. Döntési út\n\n' + self.kartya(hibas))), hibas)
        jo = '**A motívum helyein:** 1Móz 3:17, 3:23 → 1. föld; 3. anyag · 1Móz 4:2 → 1. föld.'
        self.assertEqual(self.bdb(lap(tobbi='## 1. Döntési út\n\n' + self.kartya(jo))), [])
        self.assertEqual(K.helyek_ismetlese('**A motívum helyein:** 1Móz 3:17, 3:23 → a · Zsolt 3:23 → b.'), [])

    def test_f187_thayer_kartya(self):
        def thayer(olvasoi):
            return self.kartya(olvasoi).replace('##### H0001 — אָב (áv) · BDB', '##### G0001 — ἄλφα (alfa) · Thayer')
        self.assertTrue(self.bdb(lap(tobbi='## 1. Döntési út\n\n' + thayer('- 1. ἐπικατάρατος, átkozott'))))
        self.assertEqual(self.bdb(lap(tobbi='## 1. Döntési út\n\n' + thayer('- **1.** átkozott'))), [])
        # a BDB-kártyán a görög betű nem hiba (a görög-szabály a Thayer-kártyára szól)
        self.assertEqual(self.bdb(lap(tobbi='## 1. Döntési út\n\n' + self.kartya('- 1. apa (LXX πατήρ)'))), [])

    def test_regi_es_jelolo_nelkuli_lapon_nem_fut(self):
        self.assertEqual(self.bdb(lap(tobbi='## 3. Valami\n\n' + self.kartya('- 1. apa (J)'))), [])
        self.assertEqual(self.bdb(lap(tobbi='## 1. Döntési út\n\n' + self.kartya('- 1. apa (J)', marker=False))), [])



def uj_lap(torzs, cimek=('2. Előfordulások', '9. Értelmezés', '11. Módszertan és nyitott kérdések')):
    reszek = ['# 📖 X-001 — Minta', '', '## 1. Döntési út', '', 'Bevezető.', '']
    for c in cimek:
        reszek += ['## ' + c, '', 'Szöveg.', '']
    return '\n'.join(reszek + [torzs, '', KOLOFON_JO])


def talalatok(szoveg, azon):
    return [t for t in meres(szoveg) if t['azonosito'] == azon]


class MunkaszoSzakaszHiv(unittest.TestCase):
    """F182 (2. fázis; F22 (a)(b), H4 (a), F24 (a)(c), F35): a MUNKASZO és a SZAKASZ_HIV kapu."""

    def test_munkaszo_uj_lapon_bukas(self):
        for hibas in ('A hely próba jellegű.', 'Az azonosítás függőben.', 'A sor ellenőrzendő.', 'Ez egy javaslat.',
                      'A tokenek száma 5.', 'Négyforrásos audit szerint.', 'D-minta: passzív szerkezet.',
                      'Három független keresés egybeesése.', 'Mért pontosság: 94,0%.', '↳ Alpont: a hely',
                      'A szavak nincs bekötve.', '*(kutatói jelölés: x)*', 'azonosításra vár 3'):
            t = talalatok(uj_lap(hibas), 'MUNKASZO')
            self.assertTrue(t and all(x['sulyossag'] == K.BUKAS for x in t), hibas)

    def test_munkaszo_nem_jelez(self):
        for jo in ('A próbatétel gyakorlati végrehajtása.', 'A két gyűjtemény független egymástól.',
                   'Ennél a pontnál a lap nem közöl adatot.'):
            self.assertEqual(talalatok(uj_lap(jo), 'MUNKASZO'), [], jo)

    def test_munkaszo_regi_lapon_figyelmeztetes(self):
        t = talalatok(lap(tobbi='## 3. Valami\n\nA hely próba jellegű.'), 'MUNKASZO')
        self.assertTrue(t and all(x['sulyossag'] == K.FIGY for x in t))

    def test_szakasz_hivatkozas(self):
        self.assertEqual(talalatok(uj_lap('A kifejtés a 9. (Értelmezés) és a 11. szakaszban (Módszertan és nyitott '
                                          'kérdések) áll; a részletek a 2. szakaszban.'), 'SZAKASZ_HIV'), [])
        self.assertEqual(talalatok(uj_lap('A BDB az 1. szakaszban idézi; a szócikk 5. szakaszának fordítása.'),
                                   'SZAKASZ_HIV'), [])
        for hibas in ('A kifejtés a 6. Értelmezésben áll, l. a 7. szakaszt.', 'A kifejtés a 9. (Kapcsolatok) pontban.',
                      'A részletek a 11. szakaszban (Értelmezés).'):
            self.assertTrue(talalatok(uj_lap(hibas), 'SZAKASZ_HIV'), hibas)

    def test_szakasz_hivatkozas_forrasrovidites_utan_nem_jelez(self):
        # F203 (DT-F203b): a G2671 Thayer-fordítása „c. 3. (…)” caput-hivatkozást tartalmaz — nem a lap 3. szakasza
        for jo in ('ἐγώ κατάρα ἐγενήθην, Protevangelium Jacobi, c. 3. (Aiszkhülosz, Eurípidész, Platón, mások.)',
                   'Winer, p. 5. (Lipcse kiadás) szerint.', 'Lásd § 3. (Hivatkozás) alatt.'):
            self.assertEqual(talalatok(uj_lap(jo), 'SZAKASZ_HIV'), [], jo)
        # a valódi, rossz nevű szakaszhivatkozás továbbra is BUKÁS
        t = talalatok(uj_lap('A részletek a 3. (Előfordulások) alatt állnak.'), 'SZAKASZ_HIV')
        self.assertTrue(t and all(x['sulyossag'] == K.BUKAS for x in t))

    def test_szakasz_hivatkozas_regi_lapon_nem_fut(self):
        self.assertEqual(talalatok(lap(tobbi='## 3. Valami\n\nA részletek a 7. szakaszban.'), 'SZAKASZ_HIV'), [])


class HamartLapMunkaszo(unittest.TestCase):
    """F182: a HAMART-001 lapján a MUNKASZO és a SZAKASZ_HIV 0 BUKÁS; a rontott másolat jelez."""

    @classmethod
    def setUpClass(cls):
        ut = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'lexikon', 'HAMART-001_TUDOMANYOS.md')
        with open(ut, encoding='utf-8') as f:
            cls.lap = f.read()

    def test_hamart_tiszta(self):
        for azon in ('MUNKASZO', 'SZAKASZ_HIV'):
            self.assertEqual([t for t in talalatok(self.lap, azon) if t['sulyossag'] == K.BUKAS], [], azon)

    def test_rontott_masolat_jelez(self):
        # F183: a 9. a Hatástörténet, az Értelmezés a 10.
        self.assertIn('10. (Értelmezés)', self.lap)
        rontott = self.lap.replace('10. (Értelmezés)', '10. (Kapcsolatok)', 1).replace(
            '## Kivonat\n\n', '## Kivonat\n\nA lap próba, a forrás ellenőrzendő. ', 1)
        self.assertTrue([t for t in talalatok(rontott, 'MUNKASZO') if t['sulyossag'] == K.BUKAS])
        self.assertTrue(talalatok(rontott, 'SZAKASZ_HIV'))

if __name__ == '__main__':
    unittest.main(verbosity=1)
