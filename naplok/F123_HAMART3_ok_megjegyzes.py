# -*- coding: utf-8 -*-
"""F123 HAMART-001: a saját elutasítási okok `megjegyzes` mezője olvasói mondat lesz (az 1/b. döntési tábla „Mit jelent”
oszlopa; a felhasználó átnézése, 2026-11-05). Csak a HAMART-001 sorai változnak; a minta és a címke nem."""
import io
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

M = {
    '98': 'a lánc szava áll a versben, de köznapi értelemben (föld mint talaj, bűnáldozat, pusztítás), és a hely nem utal vissza a Genezisre',
    '99': 'a szótár a héber vagy a görög versszámozás szerint idézi a helyet; a Károli-versben a szó nem áll',
    '101': 'rituális, jogi vagy indulati átok; a hely nem mondja, hogy egy tett következménye továbbterjed',
    '102': 'a szövetség átkait sorolja, de a Genezis átok-igéje nélkül',
    '103': 'tövis vagy bogáncs képként áll, a Genezis tövis és bogáncs szópárja nélkül',
    '104': 'a fáradság a bölcsességirodalom témája, a Genezis fáradság-szava nélkül',
    '105': 'általában szól az engedetlenségről, a föld átkának szerkezete nélkül',
    '106': 'más szókapcsolat (Isten letekint, minden test), nem a romlás láncához tartozik',
    '107': 'a romlás szócsaládjának más használata, például erkölcsi jellemzés',
    '108': 'épület, ország vagy termés fizikai pusztulása, nem erkölcsi megromlás',
    '109': 'a test enyészete vagy romlandósága, nem a föld romlása',
    '110': 'bűnlista vagy általános megállapítás az emberi szívről, a terjedés szerkezete nélkül',
    '111': 'az öröklött bűnösség kérdése, amelyet a lap nem dönt el',
    '112': 'a föld szava elbeszélésben áll, átok nélkül',
    '113': 'ember átkoz embert vagy tárgyat; nem a Genezis átkának folytatása',
    '114': 'a mező füve mint táplálék, nem az átkozott föld tövise',
    '115': 'Noé vagy az özönvíz felidézése, az átok terjedése nélkül',
    '116': 'a bujdosás büntetés, de a föld szava nem áll a versben',
    '117': 'a „vég” prófétai formulája, más kulcsszóval',
    '118': 'az „Isten előtt” kifejezés miatt felhozott hely',
    '119': 'az erőszak szava személyek közti sérelemre, a föld megtelése nélkül',
    '120': 'a szív romlott hajlama, amely önálló motívum',
    '121': 'a Károli magyar szava itt más héber vagy görög szót fordít; a motívum szava a versben nem áll',
    '122': 'a romlás igéje Izrael hűtlenségéről, az egész emberiségre kiterjedő ítélet nélkül',
    '123': 'a szomszédos vers a motívumban van, ott áll a szerkezet',
    '124': 'a föld elvesztése vagy terméketlensége a szövetség rendjében, a Genezisre való visszautalás nélkül',
    '125': 'jogi szabály, bűnbánat vagy panasz; a két szó egymás mellett áll, visszautalás nélkül',
}
ut = 'adat/elutasitasi_okok.tsv'
nyers = io.open(ut, encoding='utf-8', newline='').read()
nl = '\r\n' if '\r\n' in nyers else '\n'
sorok = nyers.split(nl)
n = 0
for i, s in enumerate(sorok):
    r = s.split('\t')
    if len(r) >= 6 and r[1] == 'HAMART-001' and r[0] in M:
        r[4] = M[r[0]]
        sorok[i] = '\t'.join(r)
        n += 1
assert n == len(M), n
io.open(ut, 'w', encoding='utf-8', newline='').write(nl.join(sorok))
print('elutasitasi_okok.tsv: %d megjegyzés' % n)
