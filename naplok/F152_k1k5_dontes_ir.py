"""F152.9: két nyitott döntési sor (DT-F152b, DT-F152c) a DONTESEK.md-be, a DT-F151c sora után.

A K1–K5 (DT-F151c) átvezetése előtt mért két kérdés, amelyre a felhasználó
K1–K5 válasza nem ad választ. CRLF-fájl: newline='' olvasás és írás.
"""
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

UT = 'DONTESEK.md'

B = ('| DT-F152b | #152 K1–K5 átvezetés (⛔ a DT-F151c K4 hatóköre) | A K4 elhatárolása: „a *besém* után álló JHVH (H3068)”; '
     'ezzel marad bent a 2Móz 33:19 és 34:5, és marad kint az Ézs 43:1, 45:3 (*besimchá*) és a 44:5 (*besém Jaakóv*). '
     'Mért (`naplok/F152_k4_meres.py`, TAHOT, `split(\'\\t\')`): a 33 beépített sorból hét ÓSZ-sornál a *besém* után nem a JHVH szó áll, '
     'hanem névmási rag, ugyanaz a szerkezet, mint az Ézs 43:1-ben: Zak 13:9 (*bismí*, „nevemet”), Zsolt 105:1, 1Krón 16:8, Ézs 12:4 '
     '(*bismó*, „nevét”), Jer 10:25, Zsolt 79:6, Ézs 64:6 (*bismchá*, „nevedet”). Szó szerint alkalmazva ez a hét sor is kikerülne; '
     'ezt a K4 válasza nem mondja ki. Ugyanez dönti el a `negativ_kriterium` új szövegét. | '
     '(a) szó szerint: a *besém* után a JHVH szónak kell állnia, a hét sor is kikerül (33 → 22, a K1/K2-vel) · '
     '(b) a ragnak a JHVH-ra kell visszautalnia: a hét sor marad (mindegyikben Isten a rag gazdája: a Zak 13:9-ben Ő beszél, '
     'a többiben Őt szólítják meg vagy Róla szól a vers), az Ézs 43:1 és 45:3 kint marad, mert ott a rag a megszólított emberre '
     '(Jákób, Círus) utal, a 44:5 is kint marad, mert ott Jákób neve áll · (c) más | (b) | 🟡 | '
     'A végrehajtó javaslata (b): a tagadó formát (Jer 10:25, Zsolt 79:6, Ézs 64:6) a `hatar-ellenor` következetesnek találta '
     '(`naplok/HATAR_ISTENTISZT-001.md` „Nem kérdés”), és a K4 kérdése a 2Móz 33/34 és az Ézs 43–45 kettősségéről szólt. '
     'A döntésig a `jeloltek.tsv` Ézs 43:1/44:5/45:3 indoka és a `negativ_kriterium` nem változik. | '
     '`naplok/F152_k4_meres.py`; `naplok/F152_K1K5_atvezetes_naplo.md` 1. |')

C = ('| DT-F152c | #152 K1–K5 átvezetés (⛔ a Róm 10:14 kapcsolatai) | A K2 szerint a Róm 10:14 kikerül. A `kapcsolatok.tsv`-ben '
     'hat ISTENTISZT-001-sor áll rajta: 10:13 → 10:14, és 10:14 → 1Kor 1:2, 2Tim 2:22, 1Pét 1:17, ApCsel 9:14, ApCsel 22:16. '
     'A 2Tim 2:22 és az 1Pét 1:17 sora a K1/K2-vel mindenképp kiesik (mindkét vége kikerül). Mi legyen a másik négy sorral? '
     'Ezenkívül két nyitott motívumközi jelölt (`jeloltek.tsv`: Róm 10:12 és Róm 10:14 ↔ TEREMT-001 Róm 10:7, DT280) '
     'olyan igehelyen áll, amely a K2 után nem előfordulás. | '
     'kapcsolat: (a) a négy sor törlődik; az 1Kor 1:2, az ApCsel 9:14 és a 22:16 ekkor csak a 9:14 → 9:21 sorral kapcsolódik · '
     '(b) a 10:13 → 10:14 sor törlődik, a három másik a Róm 10:13-ra horgonyoz át (10:13 → 1Kor 1:2, ApCsel 9:14, ApCsel 22:16), '
     'új indoklással: azonos görög ige *és* ὄνομα (a 10:13-ban „τὸ ὄνομα κυρίου”), `manual` provenienciával · '
     'motívumközi: (i) mindkettő `elutasítva`, indok: a DT-F151c K2 · (ii) marad `nyitva` | (b), (i) | 🟡 | '
     'A végrehajtó javaslata: (b), mert a Róm 10:13 ugyanazt az igét hordozza névvel, így az ÚSZ-sorok nem szakadnak le a '
     'Jóel 2:32 → Róm 10:13 idézetről; (i), mert a motívumközi jelölt az `id` motívum előfordulásán áll (SEMA 2.4). | '
     '`adat/kapcsolatok.tsv` 17–21, 23; `adat/jeloltek.tsv` (Róm 10:12, Róm 10:14 `motivumkozi`) |')

with open(UT, encoding='utf-8', newline='') as f:
    szoveg = f.read()
sorok = szoveg.split('\r\n')
idx = [i for i, s in enumerate(sorok) if s.startswith('| DT-F151c |')]
assert len(idx) == 1, idx
assert 'DT-F152b' not in szoveg and 'DT-F152c' not in szoveg
uj = sorok[:idx[0] + 1] + [B, C] + sorok[idx[0] + 1:]
assert len(uj) == len(sorok) + 2
with open(UT, 'w', encoding='utf-8', newline='') as f:
    f.write('\r\n'.join(uj))
print('beírva: DT-F152b, DT-F152c a(z) %d. sor után' % (idx[0] + 1))
