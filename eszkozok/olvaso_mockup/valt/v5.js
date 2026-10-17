// 5. Fejezet-kalauz (Logos Passage Guide)
const v5Box = h("details","v5"); v5Box.open = true;
document.querySelector(".szurok").before(v5Box);
function v5Kartya(cim, forras){ const k = h("section","v5k"); k.append(h("h3",null,cim)); const t = h("div","v5t"); k.append(t, h("div","v5f", forras)); return [k, t]; }
function v5Sav(t, sorok, max, kattint){
  sorok.forEach(([fo, al, n, adat]) => {
    const b = h(kattint ? "button" : "div", "v5s"); const l = h("span","l"); l.innerHTML = fo; if(al) l.append(" ", h("small", null, al));
    const tr = h("span","tr"); const f = h("span","fi"); f.style.width = (100 * n / max) + "%"; tr.append(f);
    b.append(l, tr, h("span","n", n)); if(kattint) b.onclick = () => kattint(adat); t.append(b); });
}
on("betoltve", () => {
  const ossz = Object.keys(D.versek);
  v5Box.innerHTML = ""; const s = h("summary"); s.append(h("span","uj","ÚJ"), " Fejezet-kalauz: ", h("b", null, D.cim)); v5Box.append(s);
  const racs = h("div","v5racs"); v5Box.append(racs);
  // kulcsszavak: a folyó szöveg pontozott szavai Strong-szám szerint
  const c = {}, vk = {};
  olvRoot.querySelectorAll("a.szo").forEach(a => { const st = a.dataset.strong; if(!st || /^H9\d{3}/.test(st)) return; c[st] = (c[st] || 0) + 1; (vk[st] = vk[st] || new Set()).add(a.closest(".vers").id); });
  const kulcs = Object.entries(c).sort((a, b) => b[1] - a[1]).slice(0, 10);
  let [k1, t1] = v5Kartya("Kulcsszavak", "a Károli-szöveg pontozott szavai (Károli–Strong párosítás, modell-kimenet) · alapjelentés: magyar BDB");
  v5Sav(t1, kulcs.map(([st, n]) => { const x = D.szoindex[st] || [st, ""]; return [x[0].replace(/^(\S+)\s+(.*)$/, '<span class="heb">$2</span> <span class="mono">$1</span>'), x[1], n, st]; }), kulcs[0]?.[1] || 1,
    st => { selSzo = {v: [...vk[st]][0].slice(1), strong: st, el: null}; selVers = selSzo.v; ful = "szo"; jelolSzoveg(); panel(); });
  racs.append(k1);
  // személyek és helyek (TIPNR-blokkok)
  const nev = {};
  ossz.forEach(v => versDoc(v).querySelectorAll('[data-blokk="vers.tipnr"] tbody tr').forEach(tr => { const td = tr.querySelectorAll("td"); const k = td[0].textContent.trim() + "|" + td[2].textContent.trim(); (nev[k] = nev[k] || new Set()).add(v); }));
  const nl = Object.entries(nev).sort((a, b) => b[1].size - a[1].size);
  let [k2, t2] = v5Kartya("Személyek és helyek", "vers.tipnr (TIPNR, angol névalak) · versek száma");
  if(nl.length) v5Sav(t2, nl.map(([k, s]) => { const [n, st] = k.split("|"); return [n, st, s.size, [...s][0]]; }), nl[0][1].size, v => { valaszt(v); olvRoot.getElementById("v" + v)?.scrollIntoView({block:"center"}); });
  else t2.append(h("p", "ures", "Nincs tulajdonnév ebben a fejezetben."));
  racs.append(k2);
  // témák (Nave)
  const tem = {};
  ossz.forEach(v => versDoc(v).querySelectorAll('[data-blokk="vers.nave"] tbody tr').forEach(tr => { const t = tr.querySelector("td").textContent.trim(); (tem[t] = tem[t] || new Set()).add(v); }));
  const tl = Object.entries(tem).sort((a, b) => b[1].size - a[1].size).slice(0, 10);
  let [k3, t3] = v5Kartya("Témák", "vers.nave (Nave's Topical Bible, angol címszavak) · versek száma");
  v5Sav(t3, tl.map(([t, s]) => [t, "", s.size, [...s][0]]), tl[0]?.[1].size || 1, v => valaszt(v, "temak"));
  racs.append(k3);
  // motívumok
  const mot = {};
  ossz.forEach(v => versDoc(v).querySelectorAll('[data-blokk="vers.motivum"] tbody tr').forEach(tr => { const t = tr.querySelector("td").textContent.trim(); (mot[t] = mot[t] || new Set()).add(v); }));
  let [k4, t4] = v5Kartya("Motívumok", "vers.motivum (adat/elofordulasok.tsv)");
  const ml = Object.entries(mot);
  if(ml.length) v5Sav(t4, ml.map(([t, s]) => [t, "", s.size, [...s][0]]), Math.max(...ml.map(x => x[1].size)), v => valaszt(v, "motivum"));
  else t4.append(h("p","ures","Ebben a fejezetben nincs lezárt motívum-előfordulás. Üres eredmény, nem negatív lelet."));
  racs.append(k4);
  // a kereszthivatkozások célkönyvei
  const kv = {};
  ossz.forEach(v => { const d = versDoc(v); ["vers.kh","vers.tsk"].forEach(b => d.querySelectorAll(`[data-blokk="${b}"] a.igehely`).forEach(a => { const kk = a.textContent.trim().replace(/\s+\d.*$/, ""); kv[kk] = (kv[kk] || 0) + 1; })); });
  const kl = Object.entries(kv).sort((a, b) => b[1] - a[1]).slice(0, 10);
  let [k5, t5] = v5Kartya("Hová mutatnak a kereszthivatkozások?", "vers.kh (Károli-KH) + vers.tsk (TSK) · hivatkozások száma könyvenként");
  v5Sav(t5, kl.map(([k, n]) => [k, "", n, k]), kl[0]?.[1] || 1, null);
  racs.append(k5);
  const d = h("div"); d.append(h("span","uj","ÚJ"), h("b",null,"Fejezet-kalauz"), h("span","ih","Logos Passage Guide: a fejezet fölött egy pillantásra a kulcsszavak, a személyek és helyek, a témák, a motívumok és a kereszthivatkozások célkönyvei; mindegyik a szerver mostani blokkjaiból összesítve, kattintásra a vershez vagy a szó-laphoz visz."), h("span","ma","Ma: az adat versenként, a panel blokkjaiban van; fejezet-szintű összesítés csak a négy számláló-címke."));
  $("jl").prepend(d);
});
