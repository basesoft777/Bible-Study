// A színséma alkalmazása az első rajzolás előtt (#134 M3; DT295, DT-F134i (a)). A szerver a `<html data-tema="light">` alapot adja
// (az alapértelmezett téma a világos); ez a kis, nem halasztott külső szkript a `<head>`-ben a böngésző helyi tárolójában
// (localStorage, `pardes_tema`) megőrzött választást alkalmazza: `dark` → sötét, `rendszer` → az attribútum nélkül a rendszer-
// beállítás (a token-blokk `prefers-color-scheme` szabálya), minden más (nincs tárolt érték, `light`) → világos. A választót
// (Rendszer / Világos / Sötét) az olvaso.js kezeli. Inline szkript nincs (CSP: script-src 'self').
(function () {
  'use strict';
  var t = null;
  try { t = window.localStorage.getItem('pardes_tema'); } catch (e) { /* tiltott tároló: az alap (világos) marad */ }
  var h = document.documentElement;
  if (t === 'dark') { h.setAttribute('data-tema', 'dark'); }
  else if (t === 'rendszer') { h.removeAttribute('data-tema'); }
  else { h.setAttribute('data-tema', 'light'); }
})();
