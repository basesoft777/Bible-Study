# F121.7: az ISTENTISZT-001 UBS-csomag fordítási tervezete (44 egység) -- még NEM rögzített; ⛔ jóváhagyásra vár.
# Kimenet: naplok/F121_ubs_csomag_tervezet.tsv (kulcs, angol forrás, javasolt magyar, kapu-eredmény).
import sys, os
sys.stdout.reconfigure(encoding='utf-8'); sys.path.insert(0, 'eszkozok')
import glossza_lexikon_forditas as G, forditas_kapuk as K
EM = '\u2014'; T = '\t'
H = {  # (strong, lexid-vég) -> (glosszak_hu, definicio_hu | None ha kész)
 ('H7121','001001000'): ('kiáltani', None),
 ('H7121','001002000'): ('olvasni; felmondani', '= olyan cselekvés, amellyel emberek leírt szavakat hangosan kimondanak'),
 ('H7121','001003000'): ('híresnek lenni', 'szó szerint: (néven) hívatni; innen: = olyan állapot, amelyben embereknek nagy a hírnevük, aminek következtében a nevüket rendszeresen kiejtik'),
 ('H7121','001004000'): ('neveztetni; ismertnek lenni', 'szó szerint: hívatni; innen: = olyan állapot, amelyben valakit bizonyos tulajdonságokkal ismernek, és eszerint kezelnek'),
 ('H7121','001005000'): ('kihirdetni; kihirdetést tenni', 'szó szerint: kiáltani; innen: = olyan műveltető cselekvés, amellyel emberek vagy istenségek nyilvános bejelentést tesznek'),
 ('H7121','001006000'): ('hívni; magához hívni; meghívni', 'szó szerint: kiáltani; innen: = olyan műveltető cselekvés, amellyel emberek vagy istenségek tudtára adják (más) embereknek, hogy jöjjenek, akár közvetlenül megszólítva őket, akár üzenetet küldve nekik'),
 ('H7121','001007000'): ('megidézni; (eseményt) előhívni', 'szó szerint: hívni, megidézni; innen: = olyan műveltető cselekvés, amellyel istenségek bizonyos dolgokat idéznek elő, ◄ mintha azok megidézett személyek volnának'),
 ('H7121','001008000'): ('nevezni; nevet adni', 'szó szerint: kiáltani; innen: = olyan cselekvés, amellyel emberek vagy istenségek nevet adnak egy személynek, helynek, tárgynak vagy jelenségnek'),
 ('H7121','001009000'): ('nevezni; nevet adni', None),
 ('H7121','001010000'): ('(valakinek a nevén) neveztetni', 'szó szerint: (valakinek) a nevét (valaki fölött) kiáltják; innen: = olyan állapot, amelyben egy személy vagy egy épület szorosan kötődik egy másik személyhez vagy egy istenséghez'),
 ('H7121','001011000'): ('(istenséget) elismerni', None),
 ('H7121','001012000'): ('választani; megválasztani', 'szó szerint: kiáltani; innen: = olyan műveltető cselekvés, amellyel egy közösség vezetőt választ azáltal, hogy kikiáltja a nevét'),
 ('H7121','002001000'): ('találkozni', '= olyan cselekvés, amellyel emberek célzatosan egy (másik) ember, istenség vagy tárgy irányába mozdulnak, hogy kapcsolatba lépjenek vele'),
 ('H7121','002002000'): ('(valakivel) megtörténni', 'szó szerint: találkozni; innen: = olyan folyamat, amelynek során egy esemény elkezd hatni valakire'),
 ('H7121','002003000'): ('(valakivel) megtörténtetni', 'szó szerint: találkoztatni; innen: = olyan műveltető folyamat, amelynek során egy istenség elindítja, hogy egy esemény hasson valakire'),
 ('H7121','002004000'): ('megtörténni', 'szó szerint: találkozni; innen: = olyan folyamat, amelynek során egy esemény elkezdődik'),
 ('H7121','002005000'): ('(valahol) éppen lenni', '= olyan állapot, amelyben emberek történetesen egy bizonyos helyen vannak'),
 ('H7121','002006000'): ('keresni', 'szó szerint: találkozni; innen: = olyan cselekvés, amellyel emberek aktívan körülnéznek, hogy bizonyos dolgok bekövetkezzenek'),
 ('H7121','002007000'): ('szemben', 'szó szerint: találkozni; innen: = olyan állapot, amelyben két élettelen tárgy egy bizonyos helyen egymással szemben van'),
 ('H8034','001001000'): ('név', None),
 ('H8034','001002000'): ('név; felhatalmazás', 'szó szerint: név; innen: = olyan állapot, amelyben valaki másvalaki felhatalmazásával jár el'),
 ('H8034','001003000'): ('név; hírnév; megítélés', 'szó szerint: név; innen: = az a közismert információ egy személyről vagy istenségről, amely lehet jó vagy rossz, és közvetlen hatással van arra, hogyan tekintenek erre a személyre vagy istenségre'),
 ('H8034','001004000'): ('név; önmaga', None),
 ('H8034','002001000'): ('Sém', '= férfi; ◄ {L:Noah<SDBH:נֹחַ>} fia'),
}
PREF = {'H7121': '006562', 'H8034': '007442'}
rows = []
idx = G.dbh_forras_idx()
for (st, vég), (gl, df) in H.items():
    lex = PREF[st] + vég
    rows.append(('UBS_DBH', st, lex, EM, 'glosszak_hu', idx[(st, lex, 'glosszak_hu')], gl))
    if df: rows.append(('UBS_DBH', st, lex, EM, 'definicio_hu', idx[(st, lex, 'definicio_hu')], df))
dn = [r for r in G.tsv_sorok('konkordancia/UBS_DNTG_jelentesek.tsv') if r['strong'] == 'G1941' and r['entry_kod'] == '56.15'][0]
rows.append(('UBS_DNTG', 'G1941', dn['lexid'], '56.15', 'definicio_hu', dn['definicio_rovid'],
             'azt a törvényes jogot érvényesíteni, hogy ügyét egy magasabb bíróság újra megvizsgálja'))
if __name__ == '__main__':
    with open('naplok/F121_ubs_csomag_tervezet.tsv', 'w', encoding='utf-8', newline='') as f:
        f.write(T.join(['szotar','strong','entry_id','jelentes_szam','mezo','angol','javasolt_magyar','kapuk']) + '\n')
        for r in rows:
            er = K.kapuk_futtat(r[0], r[5], r[6])
            rossz = '; '.join('%s %s' % (n, e) for n, e, _ in er if e == 'SERTES')
            f.write(T.join(list(r) + ['ATMENT' if K.atment(er) else 'BUKOTT: ' + rossz]) + '\n')
            if not K.atment(er): print('BUKOTT', r[2], r[4], rossz)
    print(len(rows), 'egység')
