// 7. Személy- és helykártya (Logos Factbook, TIPNR)
function v7Jelol(){ olvRoot.querySelectorAll("a.szo").forEach(a => { if(VA.tipnr[a.dataset.strong]) a.classList.add("nev"); }); }
on("szoveg", () => v7Jelol());
on("szo", (v, strong, el) => {
  const t = VA.tipnr[strong]; if(!t) return;
  const k = $("kartya"); k.innerHTML = ""; k.classList.add("v7");
  const fej = h("div","v7fej"); fej.append(h("span","uj","ÚJ"), h("span","v7tip","Tulajdonnév · TIPNR")); k.append(fej);
  const x = D.szoindex[strong] || [strong, ""];
  const c = h("div","cim"); c.innerHTML = `${t.nev} <span class="heb">${x[0].replace(/^\S+\s+/, "")}</span>`; k.append(c);
  k.append(h("div","sor", `Károliban itt: „${el.textContent.replace(/[.,;:!?]+$/, "")}” · ${strong}${x[1] ? " · " + x[1] : ""}`));
  const g = h("div","v7szam"); g.append(h("b", null, t.db), " vers a Bibliában · első említés: ", h("b", null, t.elso)); k.append(g);
  const max = t.konyvek[0]?.[1] || 1; const bl = h("div","v7konyv");
  t.konyvek.forEach(([kk, n]) => { const r = h("div","v7s"); const tr = h("span","tr"); const f = h("span","fi"); f.style.width = (100 * n / max) + "%"; tr.append(f); r.append(h("span", null, kk), tr, h("span","n", n)); bl.append(r); });
  k.append(h("div","sor","Leggyakrabban ezekben a könyvekben:"), bl);
  const helyek = [...olvRoot.querySelectorAll(`a.szo[data-strong="${strong}"]`)].map(a => a.closest(".vers").id.slice(1));
  const uniq = [...new Set(helyek)];
  const ebben = h("div","sor"); ebben.append(`Ebben a fejezetben: `); uniq.forEach((v, i) => { const b = h("button","linkgomb", `37:${v}`); b.onclick = () => { valaszt(v); olvRoot.getElementById("v" + v)?.scrollIntoView({block:"center"}); }; if(i) ebben.append(", "); ebben.append(b); }); k.append(ebben);
  k.append(h("div","v7f","konkordancia/TIPNR_kivonat.tsv (STEPBible TIPNR, CC BY 4.0): névalak, Strong, igehelyek · a leírást a TIPNR-kivonat nem tartalmazza"));
  const b = h("button","linkgomb","A teljes szó-lap a panelen →"); b.onclick = () => { k.hidden = true; document.querySelector("aside.panel").scrollIntoView({block:"start"}); }; k.append(b);
});
on("szo", (v, strong) => { if(!VA.tipnr[strong]) $("kartya").classList.remove("v7"); });
const v7Chip = h("button","chip"); v7Chip.setAttribute("aria-pressed","true"); v7Chip.append(h("span","uj","ÚJ"), "nevek");
document.querySelector(".szurok").append(v7Chip);
v7Chip.onclick = () => { const on_ = v7Chip.getAttribute("aria-pressed") !== "true"; v7Chip.setAttribute("aria-pressed", String(on_)); $("olvHost").classList.toggle("v7ki", !on_); };
on("betoltve", () => {
  const d = h("div"); d.append(h("span","uj","ÚJ"), h("b",null,"Személy- és helykártya"), h("span","ih","Logos Factbook: a tulajdonnevek (Izráel, Júda, József, Efraim, Dávid, Jákób) a szövegben jelölve; rájuk kattintva névkártya: TIPNR-névalak, hány versben szerepel a Bibliában, első említés, a leggyakoribb könyvek, és hol áll ebben a fejezetben."), h("span","ma","Ma: a nevek a Tulajdonnevek (TIPNR) blokkban, táblázatban; a szövegben nem különböznek a többi szótól."));
  $("jl").prepend(d);
});
