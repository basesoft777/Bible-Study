// 1. Előfordulások kiemelése (Accordance, STEPBible)
let v1Strong = null;
const v1Info = h("div", "v1info"); v1Info.hidden = true;
document.querySelector(".szurok").after(v1Info);
const v1Sav = h("div", "v1sav"); v1Sav.hidden = true; document.body.append(v1Sav);
function v1Kiemel(strong){
  v1Strong = strong;
  const lista = [...olvRoot.querySelectorAll("a.szo")].filter(a => { const on = a.dataset.strong === strong; a.classList.toggle("egyezik", on); return on; });
  if(!strong || !lista.length){ v1Info.hidden = true; v1Sav.hidden = true; return; }
  const versek = new Set(lista.map(a => a.closest(".vers").id));
  const x = D.szoindex[strong] || [strong, ""];
  v1Info.innerHTML = "";
  const uj = h("span","uj","ÚJ");
  const t = h("span", null); t.innerHTML = `<b>${x[0].replace(/^(\S+)\s+(.*)$/, '$1 <span class="heb">$2</span>')}</b> · ${x[1] ? x[1] + " · " : ""}<b>${lista.length}</b> előfordulás, <b>${versek.size}</b> versben ebben a fejezetben`;
  let i = -1;
  const lep = d => { i = (i + d + lista.length) % lista.length; lista[i].scrollIntoView({block:"center", behavior:"smooth"}); lista.forEach((a, j) => a.classList.toggle("aktualis", j === i)); };
  const el = h("button","ib","‹ előző"); el.onclick = () => lep(-1);
  const ko = h("button","ib","következő ›"); ko.onclick = () => lep(1);
  const tor = h("button","ib","kiemelés törlése"); tor.onclick = () => v1Kiemel(null);
  v1Info.append(uj, t, el, ko, tor); v1Info.hidden = false;
  v1Rajz(lista);
}
function v1Rajz(lista){
  lista = lista || [...olvRoot.querySelectorAll("a.szo.egyezik")];
  v1Sav.innerHTML = ""; if(!lista.length){ v1Sav.hidden = true; return; }
  const host = $("olvHost").getBoundingClientRect(), fent = host.top + window.scrollY, mag = host.height;
  lista.forEach(a => { const r = a.getBoundingClientRect(); const p = (r.top + window.scrollY - fent) / mag;
    const m = h("button","v1jel"); m.style.top = (p * 100) + "%"; m.title = a.closest(".vers").id.replace("v", "Ez 37:") + " · " + a.textContent;
    m.onclick = () => a.scrollIntoView({block:"center", behavior:"smooth"}); v1Sav.append(m); });
  const lab = h("span","v1cim","a fejezet"); v1Sav.append(lab);
  v1Sav.hidden = false;
}
on("szo", (v, strong) => v1Kiemel(strong));
window.addEventListener("resize", () => { if(v1Strong) v1Rajz(); });
on("betoltve", () => {
  const d = h("div"); d.append(h("span","uj","ÚJ"), h("b",null,"Egy szó összes előfordulása"), h("span","ih","Accordance „Highlight all occurrences”, STEPBible: a szóra kattintva a fejezet minden azonos Strong-számú szava kiemelődik; a jobb szélső sáv mutatja, hol vannak, a gombokkal lépegethetsz köztük."), h("span","ma","Ma: a szóra kattintva csak a szó-lap nyílik meg; azt, hogy hányszor és hol áll még a fejezetben, nem látni."));
  $("jl").prepend(d);
});
