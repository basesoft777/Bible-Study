# ELLENOR_F105_3 — az ellenőr végleges válaszának eltérése a rögzített jelentéstől

*Az `ELLENOR_F105_3.md` az ellenőr első válaszát rögzíti (F105.31). Az ellenőr ezután megvárta a saját háttérben futó CI-futását, és újra elküldte a jelentést. Az első sor (`ELTÉRÉS: 2 tétel`) és a két ELTÉRÉS nem változott. Egyetlen sor változott, ez lent szó szerint áll. Az `ELLENOR_F105_3.md` változatlan marad (az `/elteres` 7. pontja szerint).*

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| F105.30: a kiegészítés tartalma | OK | `naplok/ELLENOR_F105_2.md:52` | Újrafuttatás: `futtat.py --valtozott $(git diff --name-only 3d7605a1..35ab5379 \| grep -v '^lexikon/') --diff-alap 3d7605a1 --diff-fej 35ab5379 --commit-uzenet "$(git log --format=%B 3d7605a1..35ab5379)"` → E12 0, E13 0, E28 0, E32 0; JELENTES: E25 3, E27 43, E30 4, E34 41, E36 1; a többi E-pont 0. Ez egyezik a kiegészítés számaival. Az E30 rejtett negyedik találata ebből sem látszik; ez a régi tétel NEM ELLENŐRIZHETŐ marad. |

Az ellenőr 1. ELTÉRÉS-ének záró mondata a végleges változatban: „A hozzáírt szöveg tartalmát az újrafuttatás igazolja, a folyamatszabály sérülése ettől még fennáll.”
