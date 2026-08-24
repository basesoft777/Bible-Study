# Join-tábla lefedettség — élő lekérdezés (újrafelhasználható prompt)

*Ezt a promptot bármikor bemásolhatod Claude Code-nak, ha friss, aktuális adatot szeretnél
arról, hol tart a Károli-Strong join-tábla építése — nem kell hozzá semmilyen technikai
tudás, csak másold be változtatás nélkül.*

---

## Alapváltozat — teljes, könyvenkénti összesítés

```
Futtasd le ezt, és add vissza az eredményt: számold meg könyvenként, hány egyedi
igehely szerepel a konkordancia/Karoli_Strong_kivonat.tsv-ben, és vesd össze a
Konyv_normalizalo_tabla.tsv alapján az adott könyv teljes vers-számával. Add meg
táblázatos formában: Könyv | Feldolgozott versek | Összes vers | Lefedettség (%).
```

## Ha csak egy adott könyv érdekel (pl. 1Mózes)

```
Futtasd le ezt: számold meg, hány egyedi 1Mózes-beli igehely (Gen.*) szerepel a
konkordancia/Karoli_Strong_kivonat.tsv-ben, és hasonlítsd össze 1Mózes teljes
(50 fejezet, 1533 vers) terjedelmével. Sorold is fel, mely fejezeteket érinti eddig.
```

## Ha azt akarod tudni, mely tanulmányokhoz mennyi sor tartozik

```
Futtasd le ezt: a konkordancia/Karoli_Strong_kivonat.tsv "Forrás-tanulmány" oszlopa
alapján számold össze, melyik tanulmányhoz hány sor tartozik, csökkenő sorrendben.
```

## Ha a négy lezárt tematikus tanulmány visszamenőleges ellenőrzésének állását akarod látni

```
Nézd meg a döntési fájl 8. szakaszában a "négy már lezárt tematikus tanulmány
visszamenőleges STEPBible-ellenőrzése" checklist jelenlegi állapotát (mely alpontok
vannak kipipálva), és jelentsd vissza egyszerű listában.
```

---

## Technikai háttér (nem szükséges elolvasni, csak dokumentációs célból)

A könyvenkénti összesítés mögött ez a parancs áll:
```bash
cut -f1 konkordancia/Karoli_Strong_kivonat.tsv | tail -n +2 | sort -u | \
  cut -d'.' -f1 | sort | uniq -c
```
Ez az igehely-oszlop (`Gen.1.1` formátum) könyv-részét (`Gen`) számolja meg egyedi
igehelyenként, majd könyvenként összesíti.
