// Az olvasói felület kis JavaScriptje (#76 M2). Nélküle is minden működik: a szó-kattintás és a fülek sima hivatkozások
// (szerveroldali lap). Itt csak a gyorsítás: a fülváltás, a töredék-betöltés (/r/...) és a Ctrl+K.
(function () {
  'use strict';

  // Ctrl+K: ugrás a gyorsugrás dobozra
  document.addEventListener('keydown', function (ev) {
    if ((ev.ctrlKey || ev.metaKey) && ev.key && ev.key.toLowerCase() === 'k') {
      var be = document.querySelector('.ugras input[name=q]');
      if (be) { ev.preventDefault(); be.focus(); be.select(); }
    }
  });

  var panel = document.querySelector('.panel');

  function fulValt(nev) {
    if (!panel || !panel.querySelector('.fulek')) { return; }
    panel.setAttribute('data-ful', nev);
    panel.querySelectorAll('.fulek .ful').forEach(function (f) { f.classList.toggle('aktiv', f.getAttribute('data-ful') === nev); });
    panel.querySelectorAll('.ful-tartalom').forEach(function (t) { t.hidden = t.getAttribute('data-ful') !== nev; });
  }

  if (panel) {
    panel.querySelectorAll('.fulek .ful').forEach(function (f) {
      f.addEventListener('click', function (ev) { ev.preventDefault(); fulValt(f.getAttribute('data-ful')); });
    });
  }

  function betolt(url, cel, ful) {
    fetch(url, { headers: { 'X-Requested-With': 'fetch' } }).then(function (r) {
      if (!r.ok) { throw new Error(r.status); }
      return r.text();
    }).then(function (html) {
      cel.innerHTML = html;      // a szerver által escape-elt, regiszterből készült töredék
      if (ful) { fulValt(ful); }
    }).catch(function () { /* hiba esetén a hivatkozás a teljes lapra visz */ });
  }

  // szó-kattintás: a szó-lap töredéke a jobb oldali „Szó” fülbe (csak az Olvasópultban és a Munkaasztalban van panel)
  document.addEventListener('click', function (ev) {
    var a = ev.target.closest ? ev.target.closest('a.szo[data-strong]') : null;
    if (!a || !panel || ev.ctrlKey || ev.metaKey || ev.shiftKey) { return; }
    var cel = panel.querySelector('.ful-tartalom[data-ful=szo]');
    if (!cel) { return; }
    ev.preventDefault();
    // a vers-kontextus a hivatkozás útvonalából (/1Moz/1/2): az „Ebben a versben” blokkhoz
    var m = /^\/([A-Za-z0-9]+)\/(\d+)\/(\d+)$/.exec(a.pathname);
    betolt('/r/szo/' + encodeURIComponent(a.getAttribute('data-strong')) + (m ? '?ig=' + m[1] + '/' + m[2] + '/' + m[3] : ''), cel, 'szo');
  });

  // a BDB egybetűs rövidítése (N-F131x): a koppintás fókuszba teszi, így mobilon is megjelenik a feloldás (a CSS :focus felugrója)
  document.addEventListener('click', function (ev) {
    var r = ev.target.closest ? ev.target.closest('abbr.rovidites') : null;
    if (r) { r.focus(); }
  });

  // az olvasó helyi beállításai (csak a böngészőben, localStorage; sütit nem hoznak létre): a kapcsolt szavak jelölése és a színséma
  function tarol(kulcs, ertek) { try { window.localStorage.setItem(kulcs, ertek); } catch (e) { /* tiltott tároló: a beállítás csak az oldalra érvényes */ } }
  function olvas(kulcs) { try { return window.localStorage.getItem(kulcs); } catch (e) { return null; } }

  var jeloles = document.getElementById('jeloles');
  if (jeloles) {
    var jelolesAllit = function () {
      document.querySelectorAll('.szoveg-oszlop').forEach(function (o) { o.classList.toggle('nincs-jeloles', !jeloles.checked); });
    };
    jeloles.checked = olvas('pardes_jeloles') !== 'ki';
    jelolesAllit();
    jeloles.addEventListener('change', function () { tarol('pardes_jeloles', jeloles.checked ? 'be' : 'ki'); jelolesAllit(); });
  }

  var temaGombok = document.querySelectorAll('.tema button[data-tema]');
  function temaAllit(tema) {
    if (tema === 'light' || tema === 'dark') { document.documentElement.setAttribute('data-tema', tema); }
    else { document.documentElement.removeAttribute('data-tema'); tema = 'rendszer'; }
    temaGombok.forEach(function (g) { g.setAttribute('aria-pressed', g.getAttribute('data-tema') === tema ? 'true' : 'false'); });
  }
  if (temaGombok.length) {
    temaAllit(olvas('pardes_tema'));
    temaGombok.forEach(function (g) {
      g.addEventListener('click', function () { var t = g.getAttribute('data-tema'); tarol('pardes_tema', t); temaAllit(t); });
    });
  }
})();
