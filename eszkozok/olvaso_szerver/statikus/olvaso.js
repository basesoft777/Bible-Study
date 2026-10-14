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
    betolt('/r/szo/' + encodeURIComponent(a.getAttribute('data-strong')), cel, 'szo');
  });
})();
