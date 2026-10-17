// 8. Párhuzamos oszlopok (Bible Gateway, Accordance)
const V8OSZ = [["karoli","Károli 1908"],["heber","Héber (TAHOT)"],["lxx","LXX (Rahlfs)"],["bsb","BSB (angol)"],["kjv","KJV (angol)"]];
const v8Be = {karoli:true, heber:true, lxx:true, bsb:true, kjv:false};
const v8Box = h("div","v8"); v8Box.hidden = true;
$("olvHost").after(v8Box);
const v8Sav = h("div","v8sav"); document.querySelector(".szurok").after(v8Sav);
let v8Mod = true;
function v8Szoveg(v){
  const d = versDoc(v), t = sel => [...d.querySelectorAll(sel)].map(x => x.textContent.trim()).filter(Boolean).join(" ");
  return { karoli: D.versszoveg[v],
    heber: [...d.querySelectorAll('[data-blokk="vers.eredeti"] tbody tr')].map(tr => tr.querySelectorAll("td")[1]?.textContent.trim()).join(" ").replace(/([־])\s/g, "$1"),
    lxx: [...d.querySelectorAll('[data-blokk="vers.lxx_szavak"] tbody tr')].map(tr => tr.querySelector("td")?.textContent.trim()).join(" "),
    bsb: t('[data-blokk="vers.bsb"] .ang'), kjv: t('[data-blokk="vers.kjv"] .ang') };
}
function v8Rajz(){
  v8Sav.innerHTML = "";
  const m = h("button","chip"); m.setAttribute("aria-pressed", String(v8Mod)); m.append(h("span","uj","ÚJ"), "párhuzamos nézet"); m.onclick = () => { v8Mod = !v8Mod; v8Rajz(); }; v8Sav.append(m);
  if(v8Mod) V8OSZ.forEach(([k, c]) => { const b = h("button","chip"); b.setAttribute("aria-pressed", String(v8Be[k])); b.textContent = c; b.onclick = () => { v8Be[k] = !v8Be[k]; v8Rajz(); }; v8Sav.append(b); });
  const pk = h("button","chip"); pk.setAttribute("aria-pressed", String(!document.querySelector(".fo").classList.contains("v8szeles"))); pk.textContent = "jobb panel"; pk.onclick = () => { document.querySelector(".fo").classList.toggle("v8szeles"); v8Rajz(); }; v8Sav.append(pk);
  $("olvHost").hidden = v8Mod; v8Box.hidden = !v8Mod; document.querySelector(".szurok").hidden = v8Mod;
  if(!v8Mod) return;
  const osz = V8OSZ.filter(([k]) => v8Be[k]);
  let html = `<table class="v8t"><thead><tr><th class="ih">Vers</th>${osz.map(([k, c]) => `<th class="c-${k}">${c}</th>`).join("")}</tr></thead><tbody>`;
  const esc = s => (s || "").replace(/[&<>]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;"}[c]));
  Object.keys(D.versek).forEach(v => { const sz = v8Szoveg(v);
    html += `<tr data-v="${v}" class="${selVers === v ? "sel" : ""}"><td class="ih">37:${v}</td>${osz.map(([k]) => `<td class="c-${k}"${k === "heber" ? ' dir="rtl" lang="he"' : k === "lxx" ? ' lang="grc"' : k === "bsb" || k === "kjv" ? ' lang="en"' : ""}>${esc(sz[k]) || '<span class="ures">—</span>'}</td>`).join("")}</tr>`; });
  v8Box.innerHTML = html + `</tbody></table><p class="v8f">Károli: vers (Karoli_1908, közkincs) · Héber: vers.eredeti (TAHOT, CC BY 4.0) · LXX: vers.lxx_szavak (LXX_OS, CC BY 4.0) · BSB: vers.bsb · KJV: vers.kjv (a Strong-címkék GPL-eredetűek, nyilvános kiadásból kimarad). A sor a verset jelöli ki a panelen.</p>`;
  v8Box.querySelectorAll("tbody tr").forEach(tr => tr.onclick = () => { valaszt(tr.dataset.v); });
}
on("jelol", () => { if(v8Mod) v8Box.querySelectorAll("tbody tr").forEach(tr => tr.classList.toggle("sel", tr.dataset.v === selVers)); });
on("betoltve", () => {
  v8Rajz();
  const d = h("div"); d.append(h("span","uj","ÚJ"), h("b",null,"Párhuzamos oszlopok"), h("span","ih","Bible Gateway, Accordance: versenként egymás mellett a Károli, a héber, az LXX, a BSB és a KJV; az oszlopok ki-be kapcsolhatók, a jobb panel elrejthető a szélesebb táblázatért; a sor a verset jelöli ki."), h("span","ma","Ma: a héber, az LXX és az angol szöveg csak a kijelölt vers paneljén, blokkonként, szavanként látszik."));
  $("jl").prepend(d);
});
