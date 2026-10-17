// 6. Vers-elemző táblázat (Logos Exegetical Guide)
function v6Html(v){
  const d = versDoc(v);
  const par = [...d.querySelectorAll('[data-blokk="vers.par"] tbody tr')].map(tr => [...tr.querySelectorAll("td")].map(td => td.textContent.trim()));
  const morf = [...d.querySelectorAll('[data-blokk="vers.morf_hu"] tbody tr')].map(tr => [...tr.querySelectorAll("td")].map(td => td.textContent.trim()));
  const ered = [...d.querySelectorAll('[data-blokk="vers.eredeti"] tbody tr')].map(tr => [...tr.querySelectorAll("td")].map(td => td.textContent.trim()));
  const morfSzo = {}; morf.forEach(m => { (morfSzo[m[0]] = morfSzo[m[0]] || []).push(m[2]); });
  const kiejt = {}; ered.forEach(e => { kiejt[e[1]] = e[2]; });
  const esc = s => (s || "").replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
  let sorok = "";
  par.forEach(([n, hu, heb, st, biz]) => {
    const nyelvtani = /^H9\d{3}/.test(st);
    const x = D.szoindex[st];
    const igealak = (morfSzo[heb] || []).shift() || "";
    sorok += `<tr class="${nyelvtani ? "ny" : ""}"><td class="n">${esc(n)}</td><td class="hu">${esc(hu)}</td><td class="he"><span class="heb" lang="he" dir="rtl">${esc(heb)}</span><br><small>${esc(kiejt[heb] || "")}</small></td>`
      + `<td>${x ? `<a href="/szo/${esc(st)}">${esc(st)}</a>` : esc(st)}</td><td class="aj">${esc(x ? x[1] : (nyelvtani ? "nyelvtani elem" : ""))}</td><td class="ia">${esc(igealak)}</td><td class="bz">${esc(biz)}</td></tr>`;
  });
  return `<article class="verslap"><h2 class="igehely">Ez 37:${v} — szavanként</h2>
  <p class="megj">A vers minden Károli-szava a héber párjával, a magyar BDB-alapjelentéssel és az igealak magyar feloldásával. A sor a Strong-számra kattintva a szó-lapot nyitja meg. A halvány sorok nyelvtani elemek (kötőszó, névelő, elöljáró).</p>
  <div class="v6g"><table class="adat v6t"><thead><tr><th>#</th><th>Károli</th><th>Héber</th><th>Strong</th><th>Alapjelentés (BDB, magyar)</th><th>Igealak</th><th>Pár</th></tr></thead><tbody>${sorok}</tbody></table></div>
  <p class="forras">vers.par (Károli–Strong, modell-kimenet) · vers.eredeti (TAHOT, kiejtés) · szó-lap alapjelentés (magyar BDB, gépi tisztítás) · vers.morf_hu (gépi feldolgozás)</p></article>`;
}
EXTRA_FUL.push({k:"elemzes", c:"Elemzés", html: v6Html});
on("betoltve", () => {
  ful = "elemzes"; valaszt("1", "elemzes");
  const d = h("div"); d.append(h("span","uj","ÚJ"), h("b",null,"Vers-elemző táblázat (Elemzés fül)"), h("span","ih","Logos Exegetical Guide: a kijelölt vers minden szava egy sorban: Károli-szó, héber alak és kiejtés, Strong, magyar BDB-alapjelentés, az igealak magyar feloldása és a párosítás bizonyossága. A változatban ez a nyitó fül."), h("span","ma","Ma: ugyanez az adat négy külön blokkban (párosítás, eredeti szavak, igealak, szó-lap) van, egymás alatt."));
  $("jl").prepend(d);
});
