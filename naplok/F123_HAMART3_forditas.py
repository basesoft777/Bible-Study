# -*- coding: utf-8 -*-
"""F123 HAMART-001: a lap fordítatlan Thayer-szócikkeinek fordítása előfizetői keretből, a batch kérésével (DT587 mintája).

Alparancsok (a munkakönyvtár a repón kívül, `--munka`):
  prompt   a `thayer_api_koteg` kéréseinek user-szövege kérésenként fájlba (prompt_<custom_id>.txt), hálózat nélkül
  valasz   a subagent válaszfájljai (valasz_<custom_id>.txt) a `valaszok.jsonl`-be, a tényleges modellnévvel
  kapuz    a `thayer_api_koteg.kapuz` (javítóréteg + kapuk)
  rogzit   a kapun átmentek szakaszsorai a munkatábla repón kívüli másolatába (munka.tsv)
  beir     a másolat sorai az `adat/forditasok.tsv`-be (`forditas.beir`, allapot=sonnet)
Futtatás: python naplok/F123_HAMART3_forditas.py --munka <könyvtár> --strongok <fájl> <alparancs>
"""
import argparse
import json
import os
import shutil
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

GY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(GY, 'eszkozok'))
import thayer_api_koteg as TK  # noqa: E402

MODELL = 'claude-sonnet-5-5'
MEGJ = ('Code-session (előfizetői keret), general-purpose subagent claude-sonnet-5-5, a batch user-kérése szó szerint '
        '(thayer_api_koteg terv/kuldendo_prompt, adag 9002 hamart1); eltérés: Claude Code alap rendszerutasítás, '
        'effort/max_tokens nem állítható')


def main():
    a = argparse.ArgumentParser()
    a.add_argument('--munka', required=True)
    a.add_argument('--strongok', required=True)
    a.add_argument('parancs', choices=['prompt', 'valasz', 'kapuz', 'rogzit', 'beir'])
    a = a.parse_args()
    TK.MUNKA = a.munka
    os.makedirs(a.munka, exist_ok=True)
    strongok = TK.strongok_olvas(a.strongok)
    tabla = os.path.join(a.munka, 'munka.tsv')
    if a.parancs == 'prompt':
        for k in TK.terv(strongok):
            cid = TK.custom_id(k['strong'], k['csoport'], 1)
            szoveg = TK.uzenet(TK.kuldendo_prompt(k))[0]['text']
            with open(os.path.join(a.munka, 'prompt_%s.txt' % cid), 'w', encoding='utf-8', newline='\n') as f:
                f.write(szoveg)
            print(cid, len(szoveg))
    elif a.parancs == 'valasz':
        meglevo = {r['custom_id'] for r in TK.jsonl_olvas(TK.ut('valaszok.jsonl'))}
        rek = []
        for fn in sorted(os.listdir(a.munka)):
            if fn.startswith('valasz_') and fn.endswith('.txt'):
                cid = fn[len('valasz_'):-4]
                if cid in meglevo:
                    continue
                with open(os.path.join(a.munka, fn), encoding='utf-8') as f:
                    rek.append({'custom_id': cid, 'tipus': 'succeeded', 'modell': MODELL, 'stop': 'end_turn', 'usage': {},
                                'szoveg': f.read(), 'hiba': '', 'batch_id': 'code-session-hamart1'})
        TK.jsonl_hozzaad(TK.ut('valaszok.jsonl'), rek)
        print('valaszok.jsonl: +%d' % len(rek))
    elif a.parancs == 'kapuz':
        return TK.kapuz(strongok)
    elif a.parancs == 'rogzit':
        if not os.path.exists(tabla):
            shutil.copy(TK.MUNKA_TABLA, tabla)
        return TK.rogzit(strongok, munka_ut=tabla, bukott_ut=os.path.join(a.munka, 'bukottak.tsv'))
    elif a.parancs == 'beir':
        import forditas as F
        n = F.beir(strongok, 'sonnet', megjegyzes=MEGJ, munka_ut=tabla)
        print('forditasok.tsv: %s sor' % n)
    return 0


if __name__ == '__main__':
    sys.exit(main())
