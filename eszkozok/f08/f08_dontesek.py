"""f08_dontesek.py -- F08.3: a 87 fuggo LXX-hely kutatoi dontesei az adat/lxx_dontesek.tsv-be.

A dontesek (DONTESEK lista lent) a naplok/F08_bemenet.txt kutatoi olvasatabol
szarmaznak (F08_LXX_DONTESEK_BRIEF.md 3. lepes skalaja szerint):
  biztos    -- ket fuggetlen forras egyezik: a Macula szo-szintu illesztese ES az
               LXX_OS KK-kotesu verseben ugyanaz a lemma a heber szo szerkezeti helyen;
  valoszinu -- egy forras (az LXX_OS versolvasata), ellentmondas nelkul (a Macula
               nem illeszt);
  nyitott   -- nincs forras, vagy a forrasok ellentmondanak; a jelolt csak a
               megjegyzesben all, a gorog_lemma/tipus ures.
Az FJ1 jeloltje nem fuggetlen forras (a Macula XML-bol szarmazik).

A szkript:
  - a gorog_strong-ot, lxx_pozicio-t es lxx_igehely-et az LXX_OS-bol tolti
    (a megadott szoalak n-edik elofordulasa a Karoli-vershez kotott LXX-versben);
  - a heber_strong-ot az adat/elofordulasok.tsv motivum-sorabol veszi
    (SEMA 2.11: a motivum heber Strong-tokenje), kiveve, ahol a sor tematikus;
  - a meglevo sorokat (LD001-LD004) valtozatlanul hagyja (az uj `bizonyossag`
    mezo nalunk ures), es iras elott osszeveti oket az eredetivel; eltéresnel
    vagy sorcsokkenesnel megall.

Futtatas: python eszkozok/f08/f08_dontesek.py [--ir]
(--ir nelkul csak ellenoriz es kiirja az osszesitot.)
"""
import glob
import io
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TABLA = os.path.join(GYOKER, 'adat', 'lxx_dontesek.tsv')
TS = '2026-09-30'
REGI_FEJLEC = ['id', 'igehely', 'lxx_igehely', 'heber_strong', 'gorog_lemma', 'gorog_strong',
               'lxx_pozicio', 'tipus', 'megjegyzes', 'proveniencia']
UJ_FEJLEC = ['id', 'igehely', 'lxx_igehely', 'heber_strong', 'gorog_lemma', 'gorog_strong',
             'lxx_pozicio', 'tipus', 'megjegyzes', 'bizonyossag', 'proveniencia']

M = 'Macula_heber (macula-hebrew@47db250b, szó-szintű illesztés)'
L = 'LXX_OS (lxx-morph@c91f6b1e, KK-kötés)'
E = 'adat/elofordulasok.tsv'
BIZ = 'biztos'
VAL = 'valoszinu'
NYI = 'nyitott'
NA = 'nem_alkalmazhato'  # F8.5: a nincs_heber_kulcsszo sorok bizonyossaga (ELLENOR_F08 4.)
ELT = 'eltero_forditas'
MIN = 'lxx_minusz'
NHK = 'nincs_heber_kulcsszo'

# (F17-sorszamok, motivum, igehely, tipus, gorog_lemma, keresett LXX-szoalak, hanyadik elofordulas,
#  gorog_strong-feluliras (None = LXX_OS-bol), bizonyossag, forrasok, megjegyzes)
DONTESEK = [
    ([1], 'ALVIL-001', '2Sám 22:6', ELT, 'θάνατος', 'θανάτου', 1, None, BIZ, [M, L],
     'A שְׁאוֹל-t a fordító θάνατος-szal adja (ὠδῖνες θανάτου); a vers második θανάτου-ja a מָוֶת megfelelője. Macula és LXX_OS egyezik.'),
    ([2], 'ALVIL-001', 'Jób 24:19', MIN, '', None, 0, '', VAL, [L],
     'Az LXX_OS Jób 24:19 szövege tartalmilag eltér a maszoréta verstől (ἀναφανείη δὲ τὰ φυτὰ αὐτῶν … ὀρφανῶν ἥρπασαν), a שְׁאוֹל-nak nincs görög megfelelője; a Macula a verset nem illeszti (’’ jelek), ezért egy forrás.'),
    ([3], 'ALVIL-001', 'Péld 23:14', ELT, 'θάνατος', 'θανάτου', 1, None, BIZ, [M, L],
     'מִשְּׁאוֹל → ἐκ θανάτου; Macula és LXX_OS egyezik.'),
    ([4], 'ALVIL-001', 'Préd 9:10', '', '', None, 0, '', NYI, [M, L, 'Karoli_versmegfeleltetes (KK)', E],
     'A munkalap-igehely MT/KJV-számozású: a Károli Préd 9:10 = MT 9:8 (KK, KEZI), ebben nincs שְׁאוֹל; a kulcsszó a Károli 9:12-ben (MT 9:10) áll, ott a Macula ἅδη G0086 és az LXX_OS ἐν ᾅδῃ (ᾅδης, 86) egyezik. Az előfordulás-sor igehelyének javításáig nyitott (DT23).'),
    ([5], 'ALVIL-001', 'Ézs 7:11', '', '', None, 0, '', NYI, [M, L],
     'A הַעְמֵק שְׁאָלָה kifejezést a LXX egyetlen εἰς βάθος-szal adja; a Macula a βάθος-t a הַעְמֵק-hez köti, a שְׁאָלָה-t nem illeszti. A kulcsszó saját megfelelője nem dönthető el (jelölt: βάθος G0899, vagy LXX-minusz).'),
    ([6], 'ALVIL-001', 'Ez 32:21', ELT, 'βόθρος', 'βόθρου', 1, '', BIZ, [M, L],
     'מִתּוֹךְ שְׁאוֹל → ἐν βάθει βόθρου; Macula és LXX_OS egyezik. A Macula G0999-e a konkordancia/Strong_szotar.tsv szerint βόθυνος, nem βόθρος, ezért a Strong-mező üres.'),
    ([7], 'HAMART-001', '1Móz 3:16', ELT, 'λύπη', 'λύπας', 1, None, BIZ, [M, L],
     'עִצְּבוֹנֵךְ → τὰς λύπας σου; Macula és LXX_OS egyezik (a vers ἐν λύπαις-a az עֶצֶב megfelelője).'),
    ([8], 'HAMART-001', '1Móz 3:18', ELT, 'ἄκανθα', 'ἀκάνθας', 1, None, BIZ, [M, L],
     'קוֹץ → ἀκάνθας; Macula és LXX_OS egyezik.'),
    ([9], 'HAMART-001', '1Móz 3:19', ELT, 'γῆ', 'γῆν', 1, None, BIZ, [M, L],
     'אֶל־הָאֲדָמָה → εἰς τὴν γῆν; Macula és LXX_OS egyezik (a vers további γῆ-alakjai az עָפָר megfelelői).'),
    ([10], 'HAMART-001', '1Móz 3:23', ELT, 'γῆ', 'γῆν', 1, None, BIZ, [M, L],
     'לַעֲבֹד אֶת־הָאֲדָמָה → ἐργάζεσθαι τὴν γῆν; Macula és LXX_OS egyezik.'),
    ([11], 'HAMART-001', '1Móz 4:2', ELT, 'γῆ', 'γῆν', 1, None, BIZ, [M, L],
     'עֹבֵד אֲדָמָה → ἐργαζόμενος τὴν γῆν; Macula és LXX_OS egyezik.'),
    ([12], 'HAMART-001', '1Móz 4:3', ELT, 'γῆ', 'γῆς', 1, None, BIZ, [M, L],
     'מִפְּרִי הָאֲדָמָה → ἀπὸ τῶν καρπῶν τῆς γῆς; Macula és LXX_OS egyezik.'),
    ([13], 'HAMART-001', '1Móz 4:7', ELT, 'ἁμαρτάνω', 'ἥμαρτες', 1, None, BIZ, [M, L],
     'A חַטָּאת főnevet a LXX igével adja (ἥμαρτες), eltérő mondattagolással (οὐκ ἐὰν ὀρθῶς προσενέγκῃς …); Macula és LXX_OS egyezik.'),
    ([14], 'HAMART-001', '1Móz 4:10', NHK, '', None, 0, '', NA, [M, E],
     'Az előfordulás-sor (HAMART-001, 1Móz 4:10-11) Strong-ja H0779 (אָרַר), amely a 4:11-ben áll; a 4:10 Macula-versében nincs H0779, LXX-döntés tárgytalan.'),
    ([15], 'HAMART-001', '1Móz 4:12', ELT, 'γῆ', 'γῆν', 1, None, BIZ, [M, L],
     'תַעֲבֹד אֶת־הָאֲדָמָה → ἐργᾷ τὴν γῆν; Macula és LXX_OS egyezik (a vers második γῆς-e az אֶרֶץ megfelelője).'),
    ([16], 'HAMART-001', '1Móz 4:14', ELT, 'γῆ', 'γῆς', 1, None, BIZ, [M, L],
     'מֵעַל פְּנֵי הָאֲדָמָה → ἀπὸ προσώπου τῆς γῆς; Macula és LXX_OS egyezik (a második γῆς az אֶרֶץ megfelelője).'),
    ([17], 'HAMART-001', '1Móz 5:29', ELT, 'λύπη', 'λυπῶν', 1, None, VAL, [L],
     'A Macula a עִצְּבוֹן-t nem illeszti; az LXX_OS versében a szerkezeti helyén ἀπὸ τῶν λυπῶν τῶν χειρῶν ἡμῶν áll (λύπη, 3077), mint 1Móz 3:16-ban. Egy forrás, ellentmondás nélkül.'),
    ([18], 'HAMART-001', '1Móz 6:5', ELT, 'πονηρός', 'πονηρὰ', 1, None, BIZ, [M, L],
     'A kulcsszó a második רַע (רַק רַע → ἐπιμελῶς ἐπὶ τὰ πονηρά); Macula és LXX_OS egyezik. Az első (רָעַת הָאָדָם) megfelelője αἱ κακίαι, ezt a Macula nem illeszti.'),
    ([19], 'HAMART-001', '1Móz 6:7', ELT, 'γῆ', 'γῆς', 1, None, BIZ, [M, L],
     'מֵעַל פְּנֵי הָאֲדָמָה → ἀπὸ προσώπου τῆς γῆς; Macula és LXX_OS egyezik.'),
    ([20], 'HAMART-001', '1Móz 6:12', ELT, 'καταφθείρω', 'κατέφθειρεν', 1, None, BIZ, [M, L],
     'הִשְׁחִית → κατέφθειρεν (a nif. נִשְׁחָתָה → κατεφθαρμένη); a Macula (Strong nélkül) és az LXX_OS (2704) egyezik.'),
    ([21], 'HAMART-001', '1Móz 6:13', ELT, 'ἀδικία', 'ἀδικίας', 1, None, BIZ, [M, L],
     'מָלְאָה הָאָרֶץ חָמָס → ἐπλήσθη ἡ γῆ ἀδικίας; Macula és LXX_OS egyezik.'),
    ([22], 'HAMART-001', '1Móz 6:17', ELT, 'καταφθείρω', 'καταφθεῖραι', 1, None, BIZ, [M, L],
     'לְשַׁחֵת → καταφθεῖραι; a Macula (Strong nélkül) és az LXX_OS (2704) egyezik.'),
    ([23], 'HAMART-001', '1Móz 8:21', ELT, 'καταράομαι', 'καταράσασθαι', 1, None, VAL, [L],
     'A Macula a קַלֵּל-t ἔτι-hez köti, ami a עוֹד megfelelője; az LXX_OS versében a kulcsszó helyén τοῦ καταράσασθαι áll (LXX_OS/genesis.tsv „Genesis 8:21” 18. pozíció: καταράομαι, strong 2672; a LXX_kivonat itt Strong nélküli). A két forrás ellentmondott; DT23 (b) felhasználói döntés: a jelölt (καταράομαι G2672) elfogadva. Bizonyosság valószínű: egy forrás + felhasználói döntés, a brief „biztos” definíciója nem teljesül.'),
    ([24], 'HAMART-001', '1Móz 9:11', ELT, 'καταφθείρω', 'καταφθεῖραι', 1, None, BIZ, [M, L],
     'לְשַׁחֵת הָאָרֶץ → τοῦ καταφθεῖραι πᾶσαν τὴν γῆν; a Macula (Strong nélkül) és az LXX_OS (2704) egyezik.'),
    ([25], 'HAMART-001', '1Móz 9:15', ELT, 'ἐξαλείφω', 'ἐξαλεῖψαι', 1, None, BIZ, [M, L],
     'לְשַׁחֵת כָּל־בָּשָׂר → ὥστε ἐξαλεῖψαι πᾶσαν σάρκα; a Macula alakja (ἐχαλεῖψαι) elírás, a lemma azonos; LXX_OS: ἐξαλείφω, 1813.'),
    ([26], 'HAMART-001', '1Móz 12:3', ELT, 'καταράομαι', 'καταράσομαι', 1, None, BIZ, [M, L],
     'אָאֹר → καταράσομαι; a Macula (Strong nélkül) és az LXX_OS egyezik; a Strong az LXX_OS/genesis.tsv „Genesis 12:3” 10. pozíciójának strong mezője (2672); a LXX_kivonat (lekerdez.py lxx-hid) itt Strong nélküli. A מְקַלֶּלְךָ megfelelője (τοὺς καταρωμένους) ugyanez a lemma.'),
    ([27], 'HAMART-001', 'Ez 7:23', ELT, 'ἀνομία', 'ἀνομίας', 1, None, BIZ, [M, L],
     'וְהָעִיר מָלְאָה חָמָס → ἡ πόλις πλήρης ἀνομίας; Macula és LXX_OS egyezik.'),
    ([28], 'HAMART-001', 'Ez 8:17', ELT, 'ἀνομία', 'ἀνομίας', 2, None, BIZ, [M, L],
     'מָלְאוּ אֶת־הָאָרֶץ חָמָס → ἔπλησαν τὴν γῆν ἀνομίας (a vers második ἀνομίας-a; az első a תּוֹעֵבוֹת megfelelője); Macula és LXX_OS egyezik.'),
    ([29], 'HAMART-001', 'Ez 28:16', ELT, 'ἀνομία', 'ἀνομίας', 1, None, BIZ, [M, L],
     'מָלוּ תוֹכְךָ חָמָס → ἔπλησας τὰ ταμίειά σου ἀνομίας; Macula és LXX_OS egyezik.'),
    ([30], 'HAMART-001', 'Zsolt 74:20', ELT, 'ἀνομία', 'ἀνομιῶν', 1, None, BIZ, [M, L],
     'נְאוֹת חָמָס → οἴκων ἀνομιῶν (Zsolt(LXX) 73:20); Macula és LXX_OS egyezik.'),
    ([31], 'HAMART-001', 'Mik 6:12', ELT, 'ἀσέβεια', 'ἀσεβείας', 1, None, VAL, [L],
     'A Macula felcseréli a két szomszédos szót (מָלְאוּ → ἀσεβείας, חָמָס → ἔπλησαν); az LXX_OS szórendje (ἀσεβείας ἔπλησαν) szerint a חָמָס megfelelője ἀσέβεια (763). A két forrás ellentmondott; DT23 (b) felhasználói döntés: a jelölt (ἀσέβεια G0763) elfogadva. Bizonyosság valószínű: egy forrás + felhasználói döntés, a brief „biztos” definíciója nem teljesül.'),
    ([32], 'HAMART-001', 'Sof 1:9', ELT, 'ἀσέβεια', 'ἀσεβείας', 1, None, BIZ, [M, L],
     'הַמְמַלְאִים בֵּית אֲדֹנֵיהֶם חָמָס → τοὺς πληροῦντας τὸν οἶκον … ἀσεβείας; Macula és LXX_OS egyezik.'),
    ([33], 'HAMART-001', 'Hab 2:8', ELT, 'ἀσέβεια', 'ἀσεβείας', 1, None, BIZ, [M, L],
     'וַחֲמַס־אֶרֶץ → καὶ ἀσεβείας γῆς; Macula és LXX_OS egyezik.'),
    ([34], 'HAMART-001', 'Hab 2:17', ELT, 'ἀσέβεια', 'ἀσεβείας', 1, None, BIZ, [M, L],
     'A kulcsszó a második חֲמַס (חֲמַס־אֶרֶץ → ἀσεβείας γῆς); az első (חֲמַס לְבָנוֹן → ἀσέβεια τοῦ Λιβάνου) ugyanez a lemma. Macula és LXX_OS egyezik.'),
    ([35], 'HAMART-001', 'Jón 3:8', ELT, 'ἀδικία', 'ἀδικίας', 1, None, BIZ, [M, L],
     'וּמִן־הֶחָמָס → καὶ ἀπὸ τῆς ἀδικίας; Macula és LXX_OS egyezik.'),
    ([36], 'HAMART-001', 'Ézs 60:18', ELT, 'ἀδικία', 'ἀδικία', 1, None, BIZ, [M, L],
     'לֹא־יִשָּׁמַע עוֹד חָמָס → οὐκ ἀκουσθήσεται ἔτι ἀδικία; Macula és LXX_OS egyezik.'),
    ([37], 'HAMART-001', 'Jer 6:7', ELT, 'ἀσέβεια', 'ἀσέβεια', 1, None, BIZ, [M, L],
     'חָמָס וָשֹׁד → ἀσέβεια καὶ ταλαιπωρία; Macula és LXX_OS egyezik.'),
    ([38], 'HAMART-001', 'Hab 1:2', ELT, 'ἀδικέω', 'ἀδικούμενος', 1, None, BIZ, [M, L],
     'A חָמָס felkiáltást a LXX participiummal adja (βοήσομαι πρὸς σὲ ἀδικούμενος); Macula és LXX_OS egyezik.'),
    ([39], 'HAMART-001', 'Ézs 24:5', NHK, '', None, 0, '', NA, [M, E],
     'Az előfordulás-sor (HAMART-001, Ézs 24:5-6) tematikus (gerinc_elem: tematikus:1Móz 3:17), Strong nélkül; a versben nincs héber kulcsszó, LXX-döntés tárgytalan.'),
    ([40], 'HAMART-001', 'Ézs 24:6', NHK, '', None, 0, '', NA, [M, E],
     'Az előfordulás-sor (HAMART-001, Ézs 24:5-6) tematikus (gerinc_elem: tematikus:1Móz 3:17), Strong nélkül; a versben nincs héber kulcsszó, LXX-döntés tárgytalan.'),
    ([41], 'HAMART-001', 'Hós 4:1', NHK, '', None, 0, '', NA, [M, E],
     'Az előfordulás-sor (HAMART-001, Hós 4:1-3) tematikus (gerinc_elem: tematikus:1Móz 3:17, „chámász nélkül”), Strong nélkül; LXX-döntés tárgytalan.'),
    ([42], 'HAMART-001', 'Hós 4:2', NHK, '', None, 0, '', NA, [M, E],
     'Az előfordulás-sor (HAMART-001, Hós 4:1-3) tematikus (gerinc_elem: tematikus:1Móz 3:17, „chámász nélkül”), Strong nélkül; LXX-döntés tárgytalan.'),
    ([43], 'HAMART-001', 'Hós 4:3', NHK, '', None, 0, '', NA, [M, E],
     'Az előfordulás-sor (HAMART-001, Hós 4:1-3) tematikus (gerinc_elem: tematikus:1Móz 3:17, „chámász nélkül”), Strong nélkül; LXX-döntés tárgytalan.'),
    ([44], 'HODIT-001', '1Móz 14:5', ELT, 'γίγας', 'γίγαντας', 1, '', VAL, [L],
     'A Macula a רְפָאִים-ot nem illeszti; az LXX_OS versében a helyén κατέκοψαν τοὺς γίγαντας áll (γίγας; Strong nincs). Egy forrás, ellentmondás nélkül.'),
    ([45], 'HODIT-001', '1Móz 15:20', ELT, 'Ραφαϊν', 'Ραφαϊν', 1, '', BIZ, [M, L],
     'A népnevet a LXX átírja (τοὺς Ραφαϊν); Macula és LXX_OS egyezik.'),
    ([46, 82], 'HODIT-001', '4Móz 13:34', MIN, '', None, 0, '', VAL, [L, 'Karoli_versmegfeleltetes (KK)'],
     'HODIT-001 és MENNY-001 közös sora; Károli 13:34 = MT 13:33 (KK). A munkalap kulcsszó-alakja a második נְפִלִים (בְּנֵי עֲנָק מִן־הַנְּפִלִים): a Macula nem illeszti (’’), az LXX_OS-ben ez a tagmondat hiányzik. Az első נְפִילִים → τοὺς γίγαντας (Macula és LXX_OS egyezik), erre a sor nem vonatkozik. DT23 (b) felhasználói döntés: LXX-minusz a munkalap-szóra. Bizonyosság valószínű: egy forrás + felhasználói döntés, a brief „biztos” definíciója nem teljesül.'),
    ([47], 'HODIT-001', '5Móz 2:11', ELT, 'Ραφαϊν', 'Ραφαϊν', 1, '', BIZ, [M, L],
     'רְפָאִים יֵחָשְׁבוּ → Ραφαϊν λογισθήσονται (átírás); Macula és LXX_OS egyezik.'),
    ([48], 'HODIT-001', '5Móz 2:20', ELT, 'Ραφαϊν', 'Ραφαϊν', 2, '', VAL, [L],
     'A munkalap-alak a második רְפָאִים: a Macula a szomszédos igével felcserélve (κατῴκουν) illeszti, az LXX_OS-ben mindkét רְפָאִים helyén Ραφαϊν áll. A két forrás a munkalap-szóra ellentmondott; DT23 (b) felhasználói döntés: a jelölt (Ραφαϊν) elfogadva. Bizonyosság valószínű: egy forrás + felhasználói döntés, a brief „biztos” definíciója nem teljesül.'),
    ([49], 'HODIT-001', '5Móz 3:11', ELT, 'Ραφαϊν', 'Ραφαϊν', 1, '', BIZ, [M, L],
     'מִיֶּתֶר הָרְפָאִים → ἀπὸ τῶν Ραφαϊν (átírás); Macula és LXX_OS egyezik.'),
    ([50], 'HODIT-001', '5Móz 3:13', ELT, 'Ραφαϊν', 'Ραφαϊν', 1, '', BIZ, [M, L],
     'אֶרֶץ רְפָאִים → γῆ Ραφαϊν (átírás); Macula és LXX_OS egyezik.'),
    ([51], 'HODIT-001', '2Sám 21:16', ELT, 'Ραφα', 'Ραφα', 1, '', VAL, [L],
     'A versben הָרָפָה áll (TAHOT: H7497, a kulcs; Macula: H7498). A Macula a vers nagy részét nem illeszti; az LXX_OS: ἐν τοῖς ἐκγόνοις τοῦ Ραφα (átírás). Egy forrás.'),
    ([52], 'HODIT-001', '2Sám 21:18', ELT, 'Ραφα', 'Ραφα', 1, '', BIZ, [M, L],
     'בִּילִדֵי הָרָפָה (TAHOT: H7497, a kulcs; Macula: H7498) → ἐν τοῖς ἐκγόνοις τοῦ Ραφα; Macula és LXX_OS egyezik.'),
    ([53], 'HODIT-001', '2Sám 21:20', ELT, 'Ραφα', 'Ραφα', 1, '', VAL, [L],
     'יֻלַּד לְהָרָפָה (TAHOT: H7497, a kulcs; Macula: H7498) → ἐτέχθη τῷ Ραφα; a Macula nem illeszti. Egy forrás.'),
    ([54], 'HODIT-001', '2Sám 21:22', '', '', None, 0, '', NYI, [M, L],
     'A Macula a לְהָרָפָה-t (TAHOT: H7497, a kulcs; Macula: H7498) nem illeszti; az LXX_OS kettős fordítást mutat (ἀπόγονοι τῶν γιγάντων ἐν Γεθ τῷ Ραφα οἶκος): a megfelelő a γίγας és a Ραφα is lehet (jelölt: Ραφα, a 21:16/18/20 mintájára).'),
    ([55], 'HODIT-001', '1Krón 20:4', ELT, 'γίγας', 'γιγάντων', 1, '', BIZ, [M, L],
     'מִילִדֵי הָרְפָאִים → ἀπὸ τῶν υἱῶν τῶν γιγάντων; Macula és LXX_OS egyezik.'),
    ([56], 'HODIT-001', '1Krón 20:6', ELT, 'γίγας', 'γιγάντων', 1, '', VAL, [L],
     'נוֹלַד לְהָרָפָא (TAHOT: H7497, a kulcs; Macula: H7498) → ἦν ἀπόγονος γιγάντων; a Macula nem illeszti. Egy forrás.'),
    ([57], 'HODIT-001', '1Krón 20:8', ELT, 'Ραφα', 'Ραφα', 1, '', VAL, [L],
     'נוּלְּדוּ לְהָרָפָא (TAHOT: H7497, a kulcs; Macula: H7498) → ἐγένοντο Ραφα ἐν Γεθ; a πάντες ἦσαν τέσσαρες γίγαντες LXX-többlet. A Macula nem illeszti. Egy forrás.'),
    ([58], 'HODIT-001', 'Jób 26:5', ELT, 'γίγας', 'γίγαντες', 1, '', BIZ, [M, L],
     'הָרְפָאִים יְחוֹלָלוּ → μὴ γίγαντες μαιωθήσονται; Macula és LXX_OS egyezik.'),
    ([59], 'HODIT-001', 'Zsolt 88:11', ELT, 'ἰατρός', 'ἰατροὶ', 1, None, BIZ, [M, L],
     'רְפָאִים → ἰατροί (Zsolt(LXX) 87:11); Macula és LXX_OS egyezik. Értelmezés: a fordító a רפא „gyógyít” tőből olvassa.'),
    ([60], 'HODIT-001', 'Péld 2:18', '', '', None, 0, '', NYI, [M, L],
     'A Macula nem illeszti; az LXX_OS-ben a וְאֶל־רְפָאִים helyén kettős fordítás áll (παρὰ τῷ ᾅδῃ μετὰ τῶν γηγενῶν): a megfelelő a γηγενής és a ᾅδης is lehet (jelölt: γηγενής, a Péld 9:18 mintájára).'),
    ([61], 'HODIT-001', 'Péld 9:18', ELT, 'γηγενής', 'γηγενεῖς', 1, '', BIZ, [M, L],
     'כִּי־רְפָאִים שָׁם → ὅτι γηγενεῖς παρ᾿ αὐτῇ ὄλλυνται; Macula és LXX_OS egyezik.'),
    ([62], 'HODIT-001', 'Péld 21:16', ELT, 'γίγας', 'γιγάντων', 1, '', BIZ, [M, L],
     'בִּקְהַל רְפָאִים → ἐν συναγωγῇ γιγάντων; Macula és LXX_OS egyezik.'),
    ([63], 'HODIT-001', 'Ézs 14:9', ELT, 'γίγας', 'γίγαντες', 1, '', BIZ, [M, L],
     'עוֹרֵר לְךָ רְפָאִים → συνηγέρθησάν σοι πάντες οἱ γίγαντες; Macula és LXX_OS egyezik.'),
    ([64], 'HODIT-001', 'Ézs 26:14', ELT, 'ἰατρός', 'ἰατροὶ', 1, None, BIZ, [M, L],
     'רְפָאִים בַּל־יָקֻמוּ → οὐδὲ ἰατροὶ οὐ μὴ ἀναστήσωσιν; Macula és LXX_OS egyezik.'),
    ([65], 'HODIT-001', 'Ézs 26:19', ELT, 'ἀσεβής', 'ἀσεβῶν', 1, None, VAL, [L],
     'A Macula illesztése érvénytelen jel („{δ}”); az LXX_OS: ἡ δὲ γῆ τῶν ἀσεβῶν πεσεῖται — a וָאָרֶץ רְפָאִים תַּפִּיל megfelelője γῆ τῶν ἀσεβῶν. Egy forrás.'),
    ([66], 'HODIT-001', '2Sám 5:18', ELT, 'τιτάν', 'τιτάνων', 1, '', BIZ, [M, L],
     'בְּעֵמֶק רְפָאִים → εἰς τὴν κοιλάδα τῶν τιτάνων; Macula és LXX_OS egyezik. Az LXX_OS lemmája itt τιτάν, az 5:22-ben τίτανος (lemmatizálási eltérés).'),
    ([67], 'HODIT-001', '2Sám 5:22', ELT, 'τιτάν', 'τιτάνων', 1, '', BIZ, [M, L],
     'בְּעֵמֶק רְפָאִים → ἐν τῇ κοιλάδι τῶν τιτάνων; Macula és LXX_OS egyezik. Az LXX_OS lemmája itt τίτανος, az 5:18-ban τιτάν; a tábla a τιτάν-t használja.'),
    ([68], 'HODIT-001', '2Sám 23:13', ELT, 'Ραφαϊμ', 'Ραφαϊμ', 1, '', BIZ, [M, L],
     'בְּעֵמֶק רְפָאִים → ἐν τῇ κοιλάδι Ραφαϊμ (átírás); Macula és LXX_OS egyezik.'),
    ([69], 'HODIT-001', '1Krón 11:15', ELT, 'γίγας', 'γιγάντων', 1, '', BIZ, [M, L],
     'בְּעֵמֶק רְפָאִים → ἐν τῇ κοιλάδι τῶν γιγάντων; Macula és LXX_OS egyezik.'),
    ([70], 'HODIT-001', '1Krón 14:9', ELT, 'γίγας', 'γιγάντων', 1, '', BIZ, [M, L],
     'בְּעֵמֶק רְפָאִים → ἐν τῇ κοιλάδι τῶν γιγάντων; Macula és LXX_OS egyezik.'),
    ([71], 'HODIT-001', 'Ézs 17:5', ELT, 'στερεός', 'στερεᾷ', 1, None, BIZ, [M, L],
     'בְּעֵמֶק רְפָאִים → ἐν φάραγγι στερεᾷ: a helynevet a LXX köznévi jelzővel adja; Macula és LXX_OS egyezik.'),
    ([72], 'KIRALY-001', '1Móz 14:18', ELT, 'ἱερεύς', 'ἱερεὺς', 1, None, BIZ, [M, L],
     'וְהוּא כֹהֵן → ἦν δὲ ἱερεύς; Macula és LXX_OS egyezik.'),
    ([73], 'KIRALY-001', '1Móz 14:19', NHK, '', None, 0, '', NA, [M, E],
     'Az előfordulás-sor (KIRALY-001, 1Móz 14:18-20) Strong-ja H3548 (כֹּהֵן), amely csak a 14:18-ban áll; a 14:19 Macula-versében nincs H3548, LXX-döntés tárgytalan.'),
    ([74], 'KIRALY-001', '1Móz 14:20', NHK, '', None, 0, '', NA, [M, E],
     'Az előfordulás-sor (KIRALY-001, 1Móz 14:18-20) Strong-ja H3548 (כֹּהֵן), amely csak a 14:18-ban áll; a 14:20 Macula-versében nincs H3548, LXX-döntés tárgytalan.'),
    ([75], 'KIRALY-001', 'Zsolt 76:3', ELT, 'εἰρήνη', 'εἰρήνῃ', 1, None, BIZ, [M, L],
     'בְשָׁלֵם → ἐν εἰρήνῃ (Zsolt(LXX) 75:3); Macula és LXX_OS egyezik. Értelmezés: a helynevet a fordító köznévként (šālôm) olvassa.'),
    ([76], 'KIRALY-001', '2Móz 19:6', ELT, 'ἱεράτευμα', 'ἱεράτευμα', 1, None, BIZ, [M, L],
     'מַמְלֶכֶת כֹּהֲנִים → βασίλειον ἱεράτευμα; Macula és LXX_OS egyezik.'),
    ([77], 'KIRALY-001', 'Zak 6:13', ELT, 'ἱερεύς', 'ἱερεὺς', 1, None, BIZ, [M, L],
     'וְהָיָה כֹהֵן → καὶ ἔσται ὁ ἱερεύς; Macula és LXX_OS egyezik.'),
    ([78], 'MENNY-001', '1Móz 6:2', ELT, 'υἱός', 'υἱοὶ', 1, None, BIZ, [M, L],
     'בְנֵי הָאֱלֹהִים → οἱ υἱοὶ τοῦ θεοῦ; Macula és LXX_OS egyezik (az 1Móz 6:4 is υἱοί; Jób 1:6 és 2:1 ἄγγελοι).'),
    ([79], 'MENNY-001', '1Móz 6:4', ELT, 'γίγας', 'γίγαντες', 1, '', BIZ, [M, L],
     'הַנְּפִלִים → οἱ δὲ γίγαντες; Macula és LXX_OS egyezik (a vers második γίγαντες-e a הַגִּבֹּרִים megfelelője).'),
    ([80], 'MENNY-001', 'Jób 1:6', ELT, 'ἄγγελος', 'ἄγγελοι', 1, None, BIZ, [M, L],
     'בְּנֵי הָאֱלֹהִים → οἱ ἄγγελοι τοῦ θεοῦ; Macula és LXX_OS egyezik.'),
    ([81], 'MENNY-001', 'Jób 2:1', ELT, 'ἄγγελος', 'ἄγγελοι', 1, None, BIZ, [M, L],
     'בְּנֵי הָאֱלֹהִים → οἱ ἄγγελοι τοῦ θεοῦ; Macula és LXX_OS egyezik.'),
    ([83], 'TEREMT-001', '1Móz 49:25', ELT, 'γῆ', 'γῆς', 1, None, BIZ, [M, L],
     'בִּרְכֹת תְּהוֹם → εὐλογίαν γῆς; Macula és LXX_OS egyezik.'),
    ([84], 'TEREMT-001', '2Móz 15:5', ELT, 'πόντος', 'πόντῳ', 1, None, BIZ, [M, L],
     'תְּהֹמֹת יְכַסְיֻמוּ → πόντῳ ἐκάλυψεν αὐτούς; a Macula (Strong nélkül) és az LXX_OS (4195) egyezik.'),
    ([85], 'TEREMT-001', '2Móz 15:8', ELT, 'κῦμα', 'κύματα', 1, None, VAL, [L],
     'A Macula a תְהֹמֹת-ot nem illeszti; az LXX_OS: ἐπάγη τὰ κύματα ἐν μέσῳ τῆς θαλάσσης — a קָפְאוּ תְהֹמֹת בְּלֶב־יָם megfelelője τὰ κύματα (κῦμα, 2949). Egy forrás.'),
    ([86], 'TEREMT-001', 'Péld 8:27', ELT, 'ἄνεμος', 'ἀνέμων', 1, None, BIZ, [M, L],
     'עַל־פְּנֵי תְהוֹם → ἐπ᾿ ἀνέμων (szabad fordítás, a פְּנֵי fordítatlan); Macula és LXX_OS egyezik.'),
    ([87], 'TEREMT-001', 'Péld 8:28', ELT, 'οὐρανός', 'οὐρανὸν', 1, None, BIZ, [M, L],
     'עִינוֹת תְּהוֹם → πηγὰς τῆς ὑπ᾿ οὐρανόν: körülírás („az ég alatti” a mélység helyett); Macula és LXX_OS egyezik a szó helyén.'),
]


def tsv(path):
    with io.open(path, encoding='utf-8', newline='') as f:
        sorok = [s.rstrip('\r') for s in f.read().split('\n') if s and not s.startswith('#')]
    fej = sorok[0].split('\t')
    return [dict(zip(fej, s.split('\t'))) for s in sorok[1:]]


IGEHELY_RE = re.compile(r'^(\S+) (\d+):(\d+)(?:-(\d+))?$')


def elofordulas_strong(motivum, igehely, eloford):
    k, f, v = IGEHELY_RE.match(igehely).group(1, 2, 3)
    f, v = int(f), int(v)
    for r in eloford:
        if r['id'] != motivum:
            continue
        m = IGEHELY_RE.match(r['igehely'])
        if not m or m.group(1) != k or int(m.group(2)) != f:
            continue
        v1 = int(m.group(3))
        v2 = int(m.group(4)) if m.group(4) else v1
        if v1 <= v <= v2:
            return r.get('strong') or ''
    return None


def main():
    ir = '--ir' in sys.argv
    f17 = tsv(os.path.join(GYOKER, 'naplok', 'F17_87_hely.tsv'))
    eloford = tsv(os.path.join(GYOKER, 'adat', 'elofordulasok.tsv'))
    celok = {d[2] for d in DONTESEK}
    lxx = {}
    for p in sorted(glob.glob(os.path.join(GYOKER, 'konkordancia', 'LXX_OS', '*.tsv'))):
        with io.open(p, encoding='utf-8', newline='') as fh:
            for s in fh:
                if s.startswith('#'):
                    continue
                mezok = s.rstrip('\r\n').split('\t')
                if len(mezok) > 2 and mezok[2] in celok:
                    lxx.setdefault(mezok[2], []).append(mezok)
    # LXX_OS oszlopok: igehely_lxx igehely_kjv igehely_karoli karoli_ok pozicio szoalak normalizalt lemma morf strong ...

    hibak = []
    lefedett = sorted(i for d in DONTESEK for i in d[0])
    if lefedett != list(range(1, 88)):
        hibak.append('a dontesek nem fedik le pontosan a 87 F17-sort: %r' % lefedett)
    for d in DONTESEK:
        for i in d[0]:
            if f17[i - 1]['igehely_karoli'] != d[2] or f17[i - 1]['motivum'] not in (d[1], 'MENNY-001'):
                hibak.append('F17 #%d igehely/motivum eltér: %s %s' % (i, f17[i - 1]['igehely_karoli'], d[2]))

    uj_sorok = []
    for n, (idx, motivum, hely, tipus, lemma, szoalak, hanyadik, gs_felul, biz, forrasok, megj) in enumerate(DONTESEK, 5):
        vers = lxx.get(hely, [])
        lxx_igehely = vers[0][0] if vers else ''
        if not lxx_igehely:
            hibak.append('%s: nincs LXX_OS-vers' % hely)
        poz, gs = '', ''
        if szoalak:
            talalat = [r for r in vers if r[5] == szoalak]
            if len(talalat) < hanyadik:
                hibak.append('%s: a(z) %s %d. elofordulasa nincs az LXX_OS-versben' % (hely, szoalak, hanyadik))
            else:
                r = talalat[hanyadik - 1]
                poz = r[4]
                if r[7] != lemma and lemma not in ('τιτάν',):
                    hibak.append('%s: az LXX_OS lemmaja %s, a dontes %s' % (hely, r[7], lemma))
                nyers = r[9].strip()
                gs = ('G%04d' % int(nyers)) if nyers.isdigit() else ''
        if gs_felul is not None:
            gs = gs_felul
        hs = elofordulas_strong(motivum, hely, eloford)
        if hs is None:
            hibak.append('%s: nincs elofordulas-sor (%s)' % (hely, motivum))
            hs = ''
        hs = hs.split('+')[0] if hs.startswith('H') else ''
        # F8.8: a DT23 (b) felhasznaloi dontessel kitoltott sorok proveniencia-bovitese
        dontes = ' | dontes=DT23(b)' if 'DT23 (b) felhasználói döntés' in megj else ''
        prov = 'scope=F08 LXX-döntés, 87 függő hely (naplok/F17_87_hely.tsv, #%s) | forras=%s + kutatói versolvasat (naplok/F08_bemenet.txt)%s | ts=%s' % (
            ','.join(str(i) for i in idx), ' + '.join(forrasok), dontes, TS)
        uj_sorok.append(['LD%03d' % n, hely, lxx_igehely, hs, lemma, gs, poz, tipus, megj, biz, prov])

    for s in uj_sorok:
        for m in s:
            if '\t' in m or '\n' in m:
                hibak.append('%s: tab/soremelés a mezőben' % s[0])

    # a meglevo tabla
    with io.open(TABLA, encoding='utf-8', newline='') as f:
        nyers = f.read()
    sorok = nyers.split('\n')
    if sorok and sorok[-1] == '':
        sorok = sorok[:-1]
    komment = [s for s in sorok if s.startswith('#')]
    adat = [s for s in sorok if s and not s.startswith('#')]
    fej = adat[0].split('\t')
    regi = [s.split('\t') for s in adat[1:]]
    if fej == REGI_FEJLEC:
        regi_uj = [r[:9] + [''] + r[9:] for r in regi]
    elif fej == UJ_FEJLEC:
        regi_uj = [r for r in regi if not any(r[0] == u[0] for u in uj_sorok)]
    else:
        hibak.append('ismeretlen fejlec: %r' % fej)
        regi_uj = []
    # osszevetes: a regi sorok mezoi valtozatlanok
    for r_eredeti, r_uj in zip(regi, regi_uj):
        vissza = r_uj[:9] + r_uj[10:] if fej == REGI_FEJLEC else r_uj
        if vissza != r_eredeti:
            hibak.append('regi sor megvaltozna: %s' % r_eredeti[0])
    if len(regi_uj) < len(regi) and fej == REGI_FEJLEC:
        hibak.append('sorcsokkenes: %d -> %d' % (len(regi), len(regi_uj)))

    from collections import Counter
    print('uj sorok: %d (F17-sorok: %d)' % (len(uj_sorok), len(lefedett)))
    print('bizonyossag:', dict(Counter(s[9] for s in uj_sorok)))
    print('tipus:', dict(Counter(s[7] or '(ures)' for s in uj_sorok)))
    print('regi sorok: %d' % len(regi))
    for s in uj_sorok:
        print('  %s %-12s %-6s %-22s %-6s %-3s %-20s %s' % (s[0], s[1], s[3], s[4], s[5], s[6], s[7], s[9]))
    if hibak:
        print('HIBA (%d):' % len(hibak))
        for h in hibak:
            print('  ' + h)
        sys.exit(1)
    if ir:
        ki = komment + ['\t'.join(UJ_FEJLEC)] + ['\t'.join(r) for r in regi_uj] + ['\t'.join(s) for s in uj_sorok]
        with io.open(TABLA, 'w', encoding='utf-8', newline='') as f:
            f.write('\n'.join(ki) + '\n')
        print('irva: %s (%d adatsor)' % (TABLA, len(regi_uj) + len(uj_sorok)))


if __name__ == '__main__':
    main()
