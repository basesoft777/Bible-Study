#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
licenc.py -- F06 4. lepes: licenc- es eredetelemzes (minimax/minimax-m3, OpenRouter).

Bemenet: naplok/F06_licenc_szovegek/INDEX.tsv (a 3. lepes szo szerinti licenc-/README-masolatai).
Minden szoveg kulon hivas. Szabalyok (brief 4. lepes, F06-D2/D3/D4):
  - homerseklet 0 (az eszkozok/fordit.py OpenRouter-hivoja; uj HTTP-kliens nincs);
  - a teljes prompt legfeljebb 12 000 karakter; hosszabb szoveg NEM darabolodik, 'kezi_hosszu';
  - JSON-valasz: licenc_tipus, kereskedelmi_hasznalat, szarmaztatott_mu, forrasmegjeloles_kell,
    kozkincs_allitas, idezet;
  - kapu: az 'idezet' szo szerint szerepel a bemeneti szovegben (szokoz-/sortores-egyseges­ites
    utan). Ures idezet csak akkor elfogadott, ha licenc_tipus == 'nincs_adat' es a tobbi mezo
    'nem_derul_ki'. Sikertelen kapu/hibas JSON eseten EGYSZER ujraprobal, utana 'kezi_kapu';
  - hivasonkenti naplo: modell, provider, tokenek, koltseg; osszkoltseg-plafon 1 USD
    (0.9 USD-nal megall, a maradek 'kezi_plafon').
A MiniMax itelete JAVASLAT; a vegso licencdontes a felhasznaloe.

Kulcs: OPENROUTER_API_KEY csak kornyezeti valtozobol; sehova nem kerul.
Kimenet: naplok/F06_licenc.tsv, naplok/F06_koltseg.tsv
"""

import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import kozos  # noqa: E402

MODELL = 'minimax/minimax-m3'
PROMPT_LIMIT = 12000
PLAFON_USD = 1.0
LEALLAS_USD = 0.9
MEZOK = ['licenc_tipus', 'kereskedelmi_hasznalat', 'szarmaztatott_mu', 'forrasmegjeloles_kell', 'kozkincs_allitas', 'idezet']

SABLON = (
    'Az alabbi szoveg egy nyilt adatforras licenc- vagy README-fajlja. Kizarolag a szoveg tartalma '
    'alapjan dolgozz; ne hasznalj kulso tudast, ne tegyel hozza semmit.\n'
    'Valaszolj EGYETLEN JSON-objektummal, magyarazat es kodblokk nelkul, pontosan ezekkel a mezokkel:\n'
    '- licenc_tipus: a szovegben nevesitett licenc (pl. "CC BY 4.0", "GPL-3.0", "CC0"), vagy "nincs_adat"\n'
    '- kereskedelmi_hasznalat: "igen" | "nem" | "nem_derul_ki"\n'
    '- szarmaztatott_mu: "engedelyezett" | "tiltott" | "copyleft" | "nem_derul_ki"\n'
    '- forrasmegjeloles_kell: "igen" | "nem" | "nem_derul_ki"\n'
    '- kozkincs_allitas: a szoveg altal a tartalom eredeterol/kozkincs-statuszarol tett allitas roviden, vagy "nincs"\n'
    '- idezet: EGY szo szerinti reszlet a szovegbol (legfeljebb 300 karakter), amely az itelet alapja; '
    'karakterre pontosan masold ki, ne fordits, ne rovidits kozepen.\n'
    'Ha a szovegbol a licenc nem derul ki: licenc_tipus="nincs_adat", a tobbi itelet "nem_derul_ki" '
    '(kozkincs_allitas "nincs"), idezet "".\n\n'
    'FAJL: %s\n=== SZOVEG KEZDETE ===\n%s\n=== SZOVEG VEGE ==='
)


def egyseges(s):
    return re.sub(r'\s+', ' ', s).strip()


def kapu(valasz, szoveg):
    """(ok, ok_szoveg)."""
    if not isinstance(valasz, dict) or any(k not in valasz for k in MEZOK):
        return False, 'hianyzo_mezo'
    if not all(isinstance(valasz[k], str) for k in MEZOK):
        return False, 'nem_szoveg_mezo'
    idezet = egyseges(valasz['idezet'])
    if not idezet:
        nincs = valasz['licenc_tipus'] == 'nincs_adat' and all(
            valasz[k] == 'nem_derul_ki' for k in ('kereskedelmi_hasznalat', 'szarmaztatott_mu', 'forrasmegjeloles_kell'))
        return (True, 'ures_idezet_nincs_adat') if nincs else (False, 'ures_idezet')
    return (True, 'idezet_szo_szerint_megvan') if idezet in egyseges(szoveg) else (False, 'idezet_nincs_a_bemenetben')


def hiv(fordit, kulcs, prompt, response_format):
    parameterek = {}
    if response_format:
        parameterek['response_format'] = {'type': 'json_object'}
    uzenetek = [{'role': 'user', 'content': prompt}]
    try:
        return fordit._http_post_nyers(MODELL, uzenetek, kulcs, parameterek)
    except fordit.OpenRouterHiba as e:
        uzenet = str(e)
        if 'easoning' in uzenet and MODELL not in fordit.GONDOLKODAS_KOTELEZO_MODELLEK:
            fordit.GONDOLKODAS_KOTELEZO_MODELLEK.add(MODELL)   # a modell nem tiltatja le a gondolkodast
            return fordit._http_post_nyers(MODELL, uzenetek, kulcs, parameterek)
        if response_format and ('response_format' in uzenet or 'json' in uzenet.lower()):
            raise KeyError('response_format') from e
        raise


def fut(parancs):
    ut = os.path.join(kozos.LICENC_MAPPA, 'INDEX.tsv')
    if kozos.SZARAZ:
        print('licenc: szaraz futas, index letezik: %s' % os.path.exists(ut))
        return
    kulcs = os.environ.get('OPENROUTER_API_KEY')
    if not kulcs:
        raise SystemExit('HIBA: nincs OPENROUTER_API_KEY a kornyezetben')
    import fordit
    fej, sorok = kozos.tsv_olvas(ut)
    licenc_sorok, koltseg_sorok = [], []
    osszes = 0.0
    response_format = True
    sorszam = 0
    for forras, mentett, eredeti, karakter in sorok:
        if not mentett:
            licenc_sorok.append((forras, eredeti, karakter, 'kezi_tul_nagy_fajl') + ('',) * 6)
            continue
        with open(os.path.join(kozos.LICENC_MAPPA, mentett), encoding='utf-8', newline='') as f:
            szoveg = f.read()
        prompt = SABLON % (eredeti, szoveg)
        if len(prompt) > PROMPT_LIMIT:
            licenc_sorok.append((forras, eredeti, str(len(szoveg)), 'kezi_hosszu') + ('',) * 6)
            continue
        if osszes >= LEALLAS_USD:
            licenc_sorok.append((forras, eredeti, str(len(szoveg)), 'kezi_plafon') + ('',) * 6)
            continue
        eredmeny, valasz = 'kezi_kapu', None
        for kiserlet in (1, 2):
            sorszam += 1
            try:
                try:
                    nyers, http_k = hiv(fordit, kulcs, prompt, response_format)
                except KeyError:
                    response_format = False
                    nyers, http_k = hiv(fordit, kulcs, prompt, False)
            except Exception as e:  # noqa: BLE001
                koltseg_sorok.append((str(sorszam), forras, eredeti, MODELL, '', '0', '0', '0', str(kiserlet), 'hiba:' + type(e).__name__))
                eredmeny = 'kezi_hiba'
                continue
            usage = nyers.get('usage') or {}
            koltseg = usage.get('cost') or 0.0
            osszes += koltseg
            tartalom = ((nyers.get('choices') or [{}])[0].get('message') or {}).get('content') or ''
            try:
                m = re.search(r'\{.*\}', tartalom, re.S)
                valasz = json.loads(m.group(0)) if m else None
            except json.JSONDecodeError:
                valasz = None
            ok, ok_szoveg = kapu(valasz, szoveg)
            koltseg_sorok.append((str(sorszam), forras, eredeti, MODELL, str(nyers.get('provider', '')),
                                  str(usage.get('prompt_tokens', 0)), str(usage.get('completion_tokens', 0)),
                                  '%.6f' % koltseg, str(kiserlet), ok_szoveg if ok else 'kapu_bukott:' + ok_szoveg))
            if ok:
                eredmeny = 'ok'
                break
            eredmeny = 'kezi_kapu'
            if osszes >= LEALLAS_USD:
                break
        if eredmeny == 'ok':
            licenc_sorok.append((forras, eredeti, str(len(szoveg)), 'javaslat_kapun_atment') + tuple(valasz[k] for k in MEZOK))
        else:
            licenc_sorok.append((forras, eredeti, str(len(szoveg)), eredmeny) + ('',) * 6)
    kozos.tsv_ir(os.path.join(kozos.NAPLOK, 'F06_licenc.tsv'),
                 ['modell: %s (OpenRouter), hőmérséklet 0; a sorok a MiniMax JAVASLATAI, a licencdöntés a felhasználóé' % MODELL,
                  'letoltes datuma: %s' % kozos.ma(), 'futtatasi parancs: %s' % parancs,
                  'a szovegek forrasa: naplok/F06_licenc_szovegek/INDEX.tsv'],
                 ['forras', 'fajl', 'karakter', 'allapot'] + MEZOK, licenc_sorok)
    kozos.tsv_ir(os.path.join(kozos.NAPLOK, 'F06_koltseg.tsv'),
                 ['osszkoltseg_usd=%.6f hivasok=%d plafon=%.2f' % (osszes, len(koltseg_sorok), PLAFON_USD),
                  'letoltes datuma: %s' % kozos.ma(), 'futtatasi parancs: %s' % parancs],
                 ['sorszam', 'forras', 'fajl', 'modell', 'provider', 'prompt_tokens', 'completion_tokens', 'koltseg_usd', 'kiserlet', 'eredmeny'],
                 koltseg_sorok)
    print('licenc: %d szoveg, %d hivas, osszkoltseg=%.6f USD' % (len(licenc_sorok), len(koltseg_sorok), osszes))
