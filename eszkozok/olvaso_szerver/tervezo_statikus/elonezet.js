// Az önfrissítő előnézet kliense (F225). Csak a belso kiadásban linkelődik (alap.html, `elonezet`), és a szerver a /elonezet/elonezet.js
// (ez a fájl) és a /elonezet/kulcs útvonalat is csak ott jegyzi be: más kiadásban 404. A fájl ezért nem a statikus/-ban áll (azt minden kiadás
// kiszolgálja), hanem a tervezo_statikus/-ban, a tervező mód kliensének mintájára. CSP: saját fájl (script-src 'self'); inline szkript és inline stílus nincs, új CSS-osztály nincs.
//
// Működés: a lap a renderelés pillanatában kapott azonosítót a szkript-címke `data-azonosito` attribútumában hordozza; a szkript 2
// másodpercenként lekérdezi a /elonezet/kulcs-ot (a szerver már számolt kulcsai: kód, arculat, lábléc, adatbázis; adatbázis-olvasás nélkül),
// és ha az azonosító eltér, újratölti a lapot (a böngésző a görgetési helyzetet megtartja; tartaléknak a szkript is menti és visszaállítja).
// - A szerver újraindulása (kódváltozás után az újratöltő pár másodpercre leállítja) VÁRAKOZÁS, nem hiba: a sikertelen lekérdezés némán
//   újrapróbálódik, a visszatérő szerver új azonosítóját pedig a következő sikeres lekérdezés újratöltéssel fogadja.
// - Bekapcsolt tervező mód (`<html data-tervezo>`) mellett szünetel: a tervező kijelölését és panelét nem szabad elvenni a felhasználótól; a
//   kikapcsolás után a következő lekérdezés pótolja az elmaradt frissítést.
// - Rejtett lapfülön szünetel; a fül előtérbe kerülésekor azonnal lekérdez.
(function () {
  'use strict';

  var szkript = document.currentScript;
  if (!szkript || !window.fetch) { return; }
  var alap = szkript.getAttribute('data-azonosito') || '';
  if (!alap) { return; }

  var URL_KULCS = '/elonezet/kulcs';
  var IDO_MS = 2000;
  var GORGETES = 'pardes_elonezet_gorgetes';
  var idozito = null;
  var uj = false;                                  // újratöltés indult: több lekérdezés nem kell

  // -- a görgetési helyzet tartaléka: újratöltés előtt mentjük, a betöltés után (ugyanaz a cím, friss mentés) visszaállítjuk -----------
  function gorgetesMent() {
    try { window.sessionStorage.setItem(GORGETES, JSON.stringify({ u: window.location.href, y: window.pageYOffset, t: Date.now() })); } catch (e) { /* tiltott tároló */ }
  }
  function gorgetesVissza() {
    try {
      var m = JSON.parse(window.sessionStorage.getItem(GORGETES) || 'null');
      window.sessionStorage.removeItem(GORGETES);
      if (m && m.u === window.location.href && Date.now() - m.t < 15000 && m.y > 0) { window.scrollTo(0, m.y); }
    } catch (e) { /* tiltott tároló vagy hibás mentés */ }
  }
  if (document.readyState === 'complete') { gorgetesVissza(); } else { window.addEventListener('load', gorgetesVissza); }

  function tervezoBe() { return document.documentElement.hasAttribute('data-tervezo'); }

  function utana() {
    if (idozito !== null) { window.clearTimeout(idozito); }
    idozito = window.setTimeout(lekerdez, IDO_MS);
  }

  function lekerdez() {
    if (idozito !== null) { window.clearTimeout(idozito); idozito = null; }
    if (uj) { return; }
    if (document.hidden || tervezoBe()) { utana(); return; }
    window.fetch(URL_KULCS, { cache: 'no-store', credentials: 'same-origin' }).then(function (r) {
      if (!r.ok) { throw new Error('nincs válasz'); }
      return r.json();
    }).then(function (j) {
      if (j && j.azonosito && j.azonosito !== alap && !tervezoBe()) {
        uj = true;
        gorgetesMent();
        window.location.reload();
        return;
      }
      utana();
    }).catch(function () { utana(); });             // újraindul a szerver: várunk, nem jelzünk hibát
  }

  document.addEventListener('visibilitychange', function () { if (!document.hidden && !uj) { lekerdez(); } });
  utana();
})();
