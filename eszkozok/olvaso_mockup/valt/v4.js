// 4. Szövegbeállítások (YouVersion, Olive Tree)
const V4 = {meret:20, sorkoz:1.85, betu:"serif", szel:"60ch", vszam:true, sor:false};
try { Object.assign(V4, JSON.parse(localStorage.getItem("v4beall") || "{}")); } catch(e){}
// V4_ALAP: a szövegbeállítások az alap része (minden lapon); csak a 4. változat jelöli újként
const V4_UJ = typeof V4_ALAP === "undefined";
const v4Gomb = h("button","ib"); v4Gomb.id = "v4gomb"; v4Gomb.setAttribute("aria-expanded","false"); v4Gomb.setAttribute("aria-label","Szövegbeállítások"); v4Gomb.title = "Szövegbeállítások";
if(V4_UJ) v4Gomb.append(h("span","uj","ÚJ")); v4Gomb.append("Aa");
$("beall").before(v4Gomb);
const v4P = h("div","menu v4menu"); v4P.hidden = true; document.querySelector("header.top").append(v4P);
v4P.innerHTML = `
<div class="eyebrow">Betűméret <output id="v4mo"></output></div>
<input type="range" id="v4meret" min="14" max="30" step="1">
<div class="eyebrow">Sorköz <output id="v4so"></output></div>
<input type="range" id="v4sorkoz" min="1.3" max="2.4" step="0.05">
<div class="eyebrow">Betűcsalád</div>
<div class="seg" id="v4betu"><button data-v="serif">Source Serif</button><button data-v="noto">Noto Serif</button><button data-v="sans">IBM Plex Sans</button></div>
<div class="eyebrow">Sorszélesség</div>
<div class="seg" id="v4szel"><button data-v="48ch">keskeny</button><button data-v="60ch">közepes</button><button data-v="80ch">széles</button></div>
<div class="eyebrow">Elrendezés</div>
<div class="seg" id="v4sor"><button data-v="0">folyó szöveg</button><button data-v="1">versenként új sor</button></div>
<label for="v4vszam" style="font-size:.84rem;display:flex;gap:8px;align-items:center"><input type="checkbox" id="v4vszam"> versszámok</label>
<button class="linkgomb" id="v4alap">Alapértékek visszaállítása</button>
<p style="margin:0;font-size:.74rem;color:var(--muted)">A beállítás ebben a böngészőben megmarad.</p>`;
const BETU = {serif:'"Source Serif 4","Noto Serif",Georgia,serif', noto:'"Noto Serif",Georgia,serif', sans:'"IBM Plex Sans",system-ui,sans-serif'};
function v4Alkalmaz(){
  const host = $("olvHost");
  host.style.setProperty("--v4-meret", V4.meret + "px"); host.style.setProperty("--v4-sorkoz", V4.sorkoz);
  host.style.setProperty("--v4-betu", BETU[V4.betu]); host.style.setProperty("--v4-szel", V4.szel);
  host.classList.toggle("v4-vszamki", !V4.vszam); host.classList.toggle("v4-sor", !!V4.sor);
  $("v4meret").value = V4.meret; $("v4mo").textContent = V4.meret + " px"; $("v4sorkoz").value = V4.sorkoz; $("v4so").textContent = (+V4.sorkoz).toFixed(2);
  $("v4vszam").checked = V4.vszam;
  [["v4betu", V4.betu], ["v4szel", V4.szel], ["v4sor", V4.sor ? "1" : "0"]].forEach(([id, v]) => $(id).querySelectorAll("button").forEach(b => b.setAttribute("aria-pressed", String(b.dataset.v === v))));
  try { localStorage.setItem("v4beall", JSON.stringify(V4)); } catch(e){}
}
$("v4meret").oninput = e => { V4.meret = +e.target.value; v4Alkalmaz(); };
$("v4sorkoz").oninput = e => { V4.sorkoz = +e.target.value; v4Alkalmaz(); };
$("v4vszam").onchange = e => { V4.vszam = e.target.checked; v4Alkalmaz(); };
$("v4betu").onclick = e => { const b = e.target.closest("button"); if(b){ V4.betu = b.dataset.v; v4Alkalmaz(); } };
$("v4szel").onclick = e => { const b = e.target.closest("button"); if(b){ V4.szel = b.dataset.v; v4Alkalmaz(); } };
$("v4sor").onclick = e => { const b = e.target.closest("button"); if(b){ V4.sor = b.dataset.v === "1"; v4Alkalmaz(); } };
$("v4alap").onclick = () => { Object.assign(V4, {meret:20, sorkoz:1.85, betu:"serif", szel:"60ch", vszam:true, sor:false}); v4Alkalmaz(); };
v4Gomb.onclick = () => { v4P.hidden = !v4P.hidden; v4Gomb.setAttribute("aria-expanded", String(!v4P.hidden)); };
document.addEventListener("click", e => { if(!e.target.closest(".v4menu") && !e.target.closest("#v4gomb")){ v4P.hidden = true; v4Gomb.setAttribute("aria-expanded","false"); } });
v4Alkalmaz();
on("betoltve", () => {
  const d = h("div"); d.append(V4_UJ ? h("span","uj","ÚJ") : h("span","num","Aa"), h("b",null,"Szövegbeállítások (Aa)"), h("span","ih","YouVersion, Olive Tree: betűméret, sorköz, betűcsalád, sorszélesség, versszámok ki-be, folyó szöveg vagy versenként új sor; a választás a böngészőben megmarad."), h("span","ma","Ma: csak a téma (rendszer, világos, sötét) állítható; a méretek a Tervezőben, de az az arculatot írja át, nem az olvasó saját beállítása."));
  if(V4_UJ) $("jl").prepend(d); else $("jl").append(d);
});
