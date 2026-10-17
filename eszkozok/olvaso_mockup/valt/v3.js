// 3. Interlineáris sor a szövegben, kapcsolóval (Logos reverse interlinear)
function v3Elso(s){ return (s || "").split(/[,;]/)[0].trim().split(/\s+/).slice(0, 3).join(" "); }
function v3Epit(){
  olvRoot.querySelectorAll(".vers").forEach(sp => {
    const v = sp.id.slice(1), d = versDoc(v);
    const sorok = [...d.querySelectorAll('[data-blokk="vers.par"] tbody tr')].map(tr => { const td = tr.querySelectorAll("td"); return {n:+td[0].textContent, heb:td[2].textContent.trim(), st:td[3].textContent.trim()}; });
    const szavak = [...sp.querySelectorAll("a.szo, span.szo-nincs")];
    szavak.forEach((w, i) => {
      if(w.querySelector(".ilhu")) return;
      const sajat = sorok.filter(r => r.n === i + 1);
      const heb = sajat.map(r => r.heb).join(" ");
      const tart = sajat.find(r => !/^H9\d{3}/.test(r.st)) || sajat[0];
      const gl = tart ? v3Elso((D.szoindex[tart.st] || [])[1]) : "";
      const hu = document.createElement("span"); hu.className = "ilhu"; hu.textContent = w.textContent;
      const hb = document.createElement("span"); hb.className = "ilhe"; hb.textContent = heb || " "; hb.lang = "he";
      const g = document.createElement("span"); g.className = "ilgl"; g.textContent = gl || (tart ? tart.st : " ");
      w.textContent = ""; w.append(hu, hb, g); w.classList.add("il");
    });
  });
}
const v3Chip = h("button","chip"); v3Chip.setAttribute("aria-pressed","true"); v3Chip.append(h("span","uj","ÚJ"), "interlineáris sor");
document.querySelector(".szurok").append(v3Chip);
v3Chip.onclick = () => { const on = v3Chip.getAttribute("aria-pressed") !== "true"; v3Chip.setAttribute("aria-pressed", String(on)); $("olvHost").classList.toggle("il-be", on); };
$("olvHost").classList.add("il-be");
on("szoveg", () => v3Epit());
on("betoltve", () => {
  const d = h("div"); d.append(h("span","uj","ÚJ"), h("b",null,"Interlineáris sor a szövegben"), h("span","ih","Logos reverse interlinear: a Károli-szó alatt a héber szó (a Károli–Strong párosításból) és a magyar BDB-alapjelentés első tagja; a jelölő-sávban egy kapcsolóval ki-be kapcsolható, külön nézet nélkül."), h("span","ma","Ma: az Interlineáris külön nézet, csempékkel; az Olvasópultban csak a pontozott aláhúzás látszik."));
  $("jl").prepend(d);
});
