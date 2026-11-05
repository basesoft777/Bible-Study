# -*- coding: utf-8 -*-
"""F123 HAMART-001 U3b (DT595): a 12. szótári blokk (Tematikus index, Nave) jelöltjeinek döntése.

A jelöltlista a mai 60 előfordulás-soron újraszámolva (`eszkozok/szerep_nave.py` jeloltek(); az U1 listája az 52 soron
készült). A mérce: a téma a motívum funkcióját fedi-e (az átok, a föld, a romlás és az özönvíz lánca), vagy a hely csak
mellékesen (személy, könyv, műfaj, túl tág téma) esik bele; `tiltott`: a bűn általában felé hígítana. A sorok a session
javaslatai (claude-opus-5-5), az orkesztrátor jóváhagyására. Ír: adat/tematikus_temak.tsv (új HAMART-001 sorok).
"""
import io
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

GY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(GY, 'eszkozok'))
import szerep_nave as SN  # noqa: E402

ID = 'HAMART-001'
PROV = ('scope=manual | forras=F123 HAMART-001 új cikk, U3b (DT595 mércéje; a session javaslata, claude-opus-5-5, az '
        'orkesztrátor jóváhagyására) | ts=2026-11-05')

KIV = {
    'NAVE-1298': 'funkció-téma: az átok, a lánc első szava (1Móz 3:14, 3:17, 4:11, 9:25)',
    'NAVE-1786': 'funkció-téma: a bűneset, ahonnan a lánc indul (1Móz 3)',
    'NAVE-2090': 'funkció-téma: a föld, a következmény hordozója (1Móz 3:17, 3:19, 3:23, 5:29)',
    'NAVE-1855': 'funkció-téma: az özönvíz, a romlás ítélete (1Móz 6:13, 6:17)',
    'NAVE-0312': 'funkció-téma: az özönvíz előtti nemzedék egyetemes romlása (1Móz 6:5, 6:7, 6:17, 7:23)',
    'NAVE-4897': 'funkció-téma: a tövis és bogáncs, az átkozott föld termése (1Móz 3:18, Hós 10:8)',
    'NAVE-0586': 'funkció-téma: a kiűzetés a földről (1Móz 3:23, 4:14)',
}
TILT = {
    'NAVE-4587': 'a bűn általában felé hígítana: a téma a bűn minden fajtáját gyűjti, nem a következmény láncát',
    'NAVE-1386': 'a bűn általában felé hígítana: az emberi romlottság általános tanítása, nem a föld romlásának lánca',
}
KIZ = {
    'NAVE-2879': 'túl tág: Isten ítéletei általában; a hely büntetésként esik bele',
    'NAVE-3594': 'személy: Noé alakja, a hely mellékesen esik bele',
    'NAVE-4863': 'mellékes: a kísértés a bűneset előzménye, nem a következmény lánca',
    'NAVE-4040': 'mellékes: az eső az özönvíz eszköze, nem a motívum funkciója',
    'NAVE-0305': 'mellékes: az állatok az ítélet felsorolásában állnak',
    'NAVE-1182': 'nem a motívum funkciója: Isten leereszkedése (a „letekint” toposz)',
    'NAVE-2255': 'túl tág: a szív bibliai fogalma általában',
    'NAVE-1254': 'mellékes: a szövetség a lánc megszakítása, de a téma a szövetségek általában',
    'NAVE-0937': 'személy: Kain alakja, a hely mellékesen esik bele',
    'NAVE-0013': 'személy: Ábel alakja, a hely mellékesen esik bele',
    'NAVE-1861': 'mellékes: a balgatag a Zsoltárok alakja, nem a romlás lánca',
    'NAVE-1168': 'nem a motívum funkciója: Isten és az ember közössége',
    'NAVE-2473': 'mellékes: a képzelet (a szív gondolata) a diagnózis szava, nem a lánc',
    'NAVE-4608': 'nem a motívum funkciója: a kétkedés a balgatag tagadása',
    'NAVE-4041': 'mellékes: a szivárvány a szövetség jele, nem a lánc',
    'NAVE-0481': 'nem a motívum funkciója: az istentagadás a Zsoltárok témája',
    'NAVE-3614': 'túl tág: a megkeményedés általában',
    'NAVE-0865': 'mellékes: az ív (a szivárvány) tárgya',
    'NAVE-4512': 'mellékes: a bárka mint hajó',
    'NAVE-1502': 'túl tág: a föld mint égitest és világ; a motívum földje a GROUND téma',
    'NAVE-1394': 'nem a motívum funkciója: a csüggedés lelkiállapota',
    'NAVE-0140': 'mellékes: a földművelés mint foglalkozás',
    'NAVE-3812': 'könyv- és népnév: a hely a Babilon elleni próféciában mellékesen esik bele',
    'NAVE-4123': 'túl tág: a megátalkodottság általában',
    'NAVE-2500': 'túl tág: a hitetlenség általában',
}


def main():
    sorok = [l.rstrip('\n').split('\t') for l in io.open(os.path.join(GY, 'adat', 'elofordulasok.tsv'), encoding='utf-8')
             if not l.startswith('#')]
    sorai = [dict(zip(sorok[0], r)) for r in sorok[1:] if r[0] == ID]
    jel = SN.jeloltek(sorai)
    dont = {}
    for x in jel:
        t = x['tema_id']
        if t in KIV:
            dont[t] = (x['tema'], 'kivalasztott', KIV[t])
        elif t in TILT:
            dont[t] = (x['tema'], 'tiltott', TILT[t])
        elif t in KIZ:
            dont[t] = (x['tema'], 'kizart', KIZ[t])
        else:
            sys.exit('döntés nélküli jelölt: %s %s' % (t, x['tema']))
    ut = os.path.join(GY, 'adat', 'tematikus_temak.tsv')
    nyers = io.open(ut, encoding='utf-8', newline='').read()
    nl = '\r\n' if '\r\n' in nyers else '\n'
    meglevo = [s for s in nyers.split(nl) if s.startswith(ID + '\t')]
    assert not meglevo, 'a HAMART-001-nek már van sora'
    uj = ['\t'.join([ID, 'Nave', t, tema, d, ind, PROV]) for t, (tema, d, ind) in dont.items()]
    io.open(ut, 'w', encoding='utf-8', newline='').write(nyers.rstrip(nl) + nl + nl.join(uj) + nl)
    print('tematikus_temak.tsv: +%d (kivalasztott %d, tiltott %d, kizart %d)' % (
        len(uj), sum(d == 'kivalasztott' for _, d, _ in dont.values()), sum(d == 'tiltott' for _, d, _ in dont.values()),
        sum(d == 'kizart' for _, d, _ in dont.values())))


if __name__ == '__main__':
    main()
