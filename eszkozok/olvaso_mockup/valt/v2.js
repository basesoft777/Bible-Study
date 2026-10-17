// 2. Kereszthivatkozás-előnézet (Logos, Olive Tree)
const v2Pop = h("div","v2pop"); v2Pop.hidden = true; document.body.append(v2Pop);
let v2Ido;
function v2Mutat(href, a, rogzit){
  const k = VA.kh[href.replace(/[?#].*$/, "")];
  v2Pop.innerHTML = "";
  const fej = h("div","v2fej"); fej.append(h("span","uj","ÚJ"), h("b", null, k ? k[0] : (a.textContent || href)));
  v2Pop.append(fej);
  if(k){ v2Pop.append(h("div","v2sz", k[1])); v2Pop.append(h("div","v2f","Károli 1908 · a célvers a pardes.db-ből")); }
  else v2Pop.append(h("div","v2f","A célvers szövege nem található: valószínűleg versszámozási eltérés (Károli ↔ KJV)."));
  if(rogzit){ const z = h("button","linkgomb","bezár"); z.onclick = () => v2Pop.hidden = true; v2Pop.append(z); }
  v2Pop.hidden = false;
  const r = a.getBoundingClientRect();
  const x = Math.min(window.scrollX + r.left, window.scrollX + document.documentElement.clientWidth - v2Pop.offsetWidth - 16);
  v2Pop.style.left = Math.max(16, x) + "px"; v2Pop.style.top = (window.scrollY + r.bottom + 6) + "px";
}
on2("hivatkozas", (href, a) => { if(!/^\/[^/]+\/\d+\/\d+/.test(href)) return false; v2Mutat(href, a, true); return true; });
on("panel", (f, root) => {
  root.querySelectorAll("a.igehely").forEach(a => {
    a.addEventListener("mouseenter", () => { clearTimeout(v2Ido); v2Ido = setTimeout(() => v2Mutat(a.getAttribute("href"), a, false), 250); });
    a.addEventListener("mouseleave", () => { clearTimeout(v2Ido); });
  });
  if(f === "kh"){
    const gomb = h("button","v2kapcs","Szövegek megjelenítése a hivatkozások alatt");
    const holder = h("div"); holder.style.cssText = "padding:8px 0 4px"; const u = h("span","uj","ÚJ"); u.style.cssText = "display:inline-block;margin-right:6px;font-size:.62rem;padding:1px 6px;border-radius:9px;background:var(--accent);color:var(--panel);font-weight:700";
    holder.append(u, gomb); root.querySelector(".verslap")?.prepend(holder);
    let nyitva = false;
    gomb.onclick = () => { nyitva = !nyitva; gomb.textContent = nyitva ? "Szövegek elrejtése" : "Szövegek megjelenítése a hivatkozások alatt";
      root.querySelectorAll("a.igehely").forEach(a => { const ki = a.parentElement.querySelector(".v2inline");
        if(!nyitva){ ki?.remove(); return; } if(ki) return;
        const k = VA.kh[a.getAttribute("href").replace(/[?#].*$/, "")]; const d = document.createElement("div"); d.className = "v2inline"; d.textContent = k ? k[1] : "(a célvers szövege nem található)"; a.after(d); }); };
  }
});
document.addEventListener("click", e => { if(!e.composedPath().some(x => x === v2Pop || (x.classList && x.classList.contains("igehely")))) v2Pop.hidden = true; });
on("betoltve", () => {
  const d = h("div"); d.append(h("span","uj","ÚJ"), h("b",null,"Kereszthivatkozás-előnézet"), h("span","ih","Logos, Olive Tree: a Kereszthiv. fülön (és minden blokkban) a hivatkozott vers szövege rámutatásra megjelenik; kattintásra rögzül; egy gombbal az összes célvers szövege kibontható a lista alatt. 272 célvers szövege beágyazva."), h("span","ma","Ma: a hivatkozás átvisz a másik lapra; a szöveget csak oda-vissza lapozva lehet összevetni."));
  $("jl").prepend(d);
});
