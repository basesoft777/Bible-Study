-- GENERÁLT: python eszkozok/olvaso_szerver/teszt_tervor.py --sema-ment (PARDES_DB=<a valódi pardes.db>) — kézzel nem szerkesztendő (F235).
-- A pardes.db táblái és indexei adat nélkül; a tervellenőr (teszt_tervor.py) ebből építi a memória-adatbázist. A tagokat a `-- ;;` sor választja el.
CREATE TABLE "auditok" ("id" TEXT, "lepes" TEXT, "proveniencia" TEXT, "datum" TEXT)
-- ;;
CREATE TABLE "bdb" ("strong_padded" TEXT, "strong_eredeti" TEXT, "teljes_szocikk" TEXT, "strong" TEXT)
-- ;;
CREATE TABLE "bdb_alias" ("masodlagos_strong" TEXT, "tabla_strong" TEXT, "bdb_id" TEXT, "nyelv" TEXT, "cimszo" TEXT, "szoveg_hasonlosag" TEXT)
-- ;;
CREATE TABLE "bdb_aranyminta" ("strong" TEXT, "szakasz" TEXT, "resz" TEXT, "utvonal" TEXT, "szint" TEXT, "jel" TEXT, "okkod" TEXT, "kezdet_en" TEXT, "kezdet_hu" TEXT, "cim" TEXT, "megjegyzes" TEXT, "ellenorzes" TEXT, "proveniencia" TEXT)
-- ;;
CREATE TABLE "bdb_forras_javitas" ("strong" TEXT, "sorszam" TEXT, "bdb_id" TEXT, "hiba" TEXT, "szo_sorszam" TEXT, "elofordulas" TEXT, "forras_alak" TEXT, "javitott_alak" TEXT, "allapot" TEXT, "indok" TEXT, "proveniencia" TEXT, "tanu" TEXT)
-- ;;
CREATE TABLE "bdb_igehely_javitas" ("strong" TEXT, "forras_hivatkozas" TEXT, "javitott_hivatkozas" TEXT, "allapot" TEXT, "indok" TEXT, "proveniencia" TEXT)
-- ;;
CREATE TABLE "bdb_jp_sefaria" ("strong" TEXT, "sorszam" TEXT, "mt_vers" TEXT, "sefaria_rid" TEXT, "illesztes" TEXT, "sefaria_ut" TEXT, "proveniencia" TEXT)
-- ;;
CREATE TABLE "bdb_karoli" ("strong" TEXT, "tipus" TEXT, "karoli_alak" TEXT, "magas" TEXT, "alacsony" TEXT, "pelda_versek" TEXT, "tahot_elofordulas" TEXT, "par_db" TEXT, "proveniencia" TEXT)
-- ;;
CREATE TABLE "bdb_szakasz_hu" ("strong" TEXT, "sorszam" TEXT, "bdb_id" TEXT, "szakasz" TEXT, "resz" TEXT, "utvonal" TEXT, "jel" TEXT, "kategoria" TEXT, "horgony" TEXT, "hu_kezdet" TEXT, "hu_hossz" TEXT, "szoveg_hu" TEXT, "forditas_forras_hash" TEXT, "proveniencia" TEXT)
-- ;;
CREATE TABLE "bdb_szakaszok" ("strong" TEXT, "bdb_id" TEXT, "sorszam" TEXT, "alszocikk" TEXT, "szakasz" TEXT, "resz" TEXT, "utvonal" TEXT, "jelolo" TEXT, "jel" TEXT, "gyakorisag" TEXT, "szoveg" TEXT, "illesztes" TEXT, "forras" TEXT, "forras_hash" TEXT, "proveniencia" TEXT, "belso_fejek" TEXT)
-- ;;
CREATE TABLE "bdb_vers_jelentes" ("strong" TEXT, "bdb_id" TEXT, "sorszam" TEXT, "poz" TEXT, "nyers" TEXT, "konyv_feloldas" TEXT, "mt_vers" TEXT, "karoli_vers" TEXT, "vers_feloldas" TEXT, "szakasz" TEXT, "resz" TEXT, "utvonal" TEXT, "okkod" TEXT, "szurt" TEXT, "csoport" TEXT, "csoport_jel" TEXT, "proveniencia" TEXT, "bizonyossag" TEXT)
-- ;;
CREATE TABLE "bsb" ("igehely" TEXT, "sorszam" INTEGER, "strong" TEXT, "angol_szo" TEXT, "morf" TEXT, "angol_szo_allapot" TEXT, "szamozas" TEXT, "step_nyers" TEXT, "kk_leképezés" TEXT, "szosorszam_nyers" TEXT)
-- ;;
CREATE TABLE "datasetek" ("study_tipus" TEXT, "dataset" TEXT, "fajl" TEXT, "kotelezoseg" TEXT, "feltetel" TEXT, "allapot" TEXT, "megjegyzes" TEXT)
-- ;;
CREATE TABLE "dontes_hatas" ("dontes_forras" TEXT, "datum" TEXT, "erintett_fajl" TEXT, "tilos_minta" TEXT, "atmeneti_jeloles" TEXT, "tovabbvivo_feladat" TEXT, "megjegyzes" TEXT)
-- ;;
CREATE TABLE "elofordulasok" ("id" TEXT, "igehely" TEXT, "kapcsolodas" TEXT, "pardes_szint" TEXT, "funkcio" TEXT, "gerinc_elem" TEXT, "strong" TEXT, "lexikon_szotar" TEXT, "lexikon_entry_id" TEXT, "jelentes_szam" TEXT, "jelentes_en" TEXT, "jelentes_hu" TEXT, "karoli_szo" TEXT, "azonositas_modja" TEXT, "megbizhatosag" TEXT, "proveniencia" TEXT, "igazolas" TEXT, "fo_elofordulas" TEXT, "felmerult_tanulmany" TEXT, "forras_tanulmany" TEXT)
-- ;;
CREATE TABLE "elutasitasi_okok" ("sorrend" TEXT, "id" TEXT, "minta" TEXT, "cimke" TEXT, "megjegyzes" TEXT, "proveniencia" TEXT)
-- ;;
CREATE TABLE "forditasok" ("szotar" TEXT, "strong" TEXT, "entry_id" TEXT, "jelentes_szam" TEXT, "mezo" TEXT, "forras_hash" TEXT, "forditas_hu" TEXT, "allapot" TEXT, "modell" TEXT, "datum" TEXT, "terminologia_verzio" TEXT, "megjegyzes" TEXT)
-- ;;
CREATE TABLE "frazis_pozicio" ("igehely" TEXT, "oldal" TEXT, "sorszam" INTEGER, "strong" TEXT, "szo" TEXT)
-- ;;
CREATE VIRTUAL TABLE fts_motivum USING fts5(szoveg, motivum_id UNINDEXED, rovat UNINDEXED, forras_fajl UNINDEXED, regi_forras UNINDEXED, tokenize="unicode61 remove_diacritics 2")
-- ;;
CREATE TABLE "funkcio_kapcsolok" ("kapcsolo" TEXT, "id" TEXT, "allapot" TEXT, "szerep_cim_resz" TEXT, "indok" TEXT, "proveniencia" TEXT)
-- ;;
CREATE TABLE "generalt_nezetek" ("id" TEXT, "utvonal" TEXT, "leiras" TEXT, "parancs" TEXT, "bemenetek" TEXT, "utana" TEXT, "orzes" TEXT, "determinizmus" TEXT, "kapuk" TEXT, "gazda" TEXT, "futtato" TEXT, "allapot" TEXT, "forras" TEXT)
-- ;;
CREATE TABLE "glosszak_heber_hu" ("strong" TEXT, "entry_id" TEXT, "kapcsolat" TEXT, "fo" TEXT, "glossza_en" TEXT, "forras_hash" TEXT, "glossza_hu" TEXT, "allapot" TEXT, "modell" TEXT, "datum" TEXT, "megjegyzes" TEXT)
-- ;;
CREATE TABLE "grammatikai_strongok" ("strong" TEXT, "rovid_jelentes" TEXT, "kategoria" TEXT, "kizaras_oka" TEXT)
-- ;;
CREATE TABLE "heti_keret" ("het" TEXT, "sav" TEXT, "elhasznalt_szazalek" TEXT, "ts" TEXT, "forras" TEXT)
-- ;;
CREATE TABLE "heti_keret_meres" ("ts" TEXT, "heti_szazalek" TEXT, "fable_szazalek" TEXT, "forras" TEXT)
-- ;;
CREATE TABLE "heti_terv" ("het" TEXT, "sav" TEXT, "sorrend" TEXT, "tetel" TEXT, "cel_a_het_vegere" TEXT, "modell" TEXT, "becsult_keret_szazalek" TEXT, "allapot_kezi" TEXT, "jovahagyva" TEXT, "eredeti_keret_szazalek" TEXT, "session_minta" TEXT, "megjegyzes" TEXT)
-- ;;
CREATE TABLE "igehely_tartomany" ("forras_tabla" TEXT, "forras_kulcs" TEXT, "oszlop" TEXT, "ertek" TEXT, "igehely" TEXT)
-- ;;
CREATE TABLE "jeloltek" ("id" TEXT, "igehely" TEXT, "forras_kereses" TEXT, "dontes" TEXT, "indoklas" TEXT, "karoli_szo" TEXT, "azonositas_modja" TEXT, "megbizhatosag" TEXT, "datum" TEXT, "jelolt_tipus" TEXT, "cel_id" TEXT, "cel_igehely" TEXT, "cel_alpont" TEXT, "dontes_ref" TEXT)
-- ;;
CREATE TABLE "kapcsolatok" ("forras_igehely" TEXT, "cel_igehely" TEXT, "id" TEXT, "tipus" TEXT, "funkcio" TEXT, "bizonyossag" TEXT, "pardes_szint" TEXT, "indoklas" TEXT)
-- ;;
CREATE TABLE "karoli_strong_kivonat" ("igehely" TEXT, "step_nyers" TEXT, "strong" TEXT, "strong_nyers" TEXT, "karoli_szo" TEXT, "azonositas_modja" TEXT, "forras_tanulmany" TEXT, "megbizhatosag" TEXT, "szofaj" TEXT, "gyok_szarmaztatas" TEXT)
-- ;;
CREATE TABLE "karoli_variancia" ("tipus" TEXT, "konyv" TEXT, "kulcs" TEXT, "ertek" TEXT, "darab" TEXT, "bizonyossag" TEXT, "id" TEXT, "igehely" TEXT, "karoli_szo" TEXT, "reszleges" TEXT, "nincs_gepi_par" TEXT, "mas_strong" TEXT, "proveniencia" TEXT)
-- ;;
CREATE TABLE "keret_munkamappa" ("munkamappa" TEXT, "sav" TEXT, "megjegyzes" TEXT)
-- ;;
CREATE TABLE "keret_sulyok" ("modell" TEXT, "csalad" TEXT, "input" TEXT, "cache_5m" TEXT, "cache_1h" TEXT, "cache_olvasas" TEXT, "output" TEXT, "forras" TEXT)
-- ;;
CREATE TABLE "kh" ("igehely" TEXT, "step_nyers" TEXT, "cel_tol" TEXT, "cel_ig" TEXT, "cel_step_nyers" TEXT, "van_vers" INTEGER)
-- ;;
CREATE TABLE "kiadasok" ("id" TEXT, "kiadas" TEXT, "datum" TEXT, "valtozas" TEXT, "proza_modell" TEXT, "forras" TEXT)
-- ;;
CREATE TABLE "kiejtes_heber_jeloltszabalyok" ("sorszam" TEXT, "minta" TEXT, "csere" TEXT, "megjegyzes" TEXT)
-- ;;
CREATE TABLE "kiejtes_heber_kivetelek" ("strong" TEXT, "ertek" TEXT, "indok" TEXT, "datum" TEXT)
-- ;;
CREATE TABLE "kiejtes_kivetelek" ("nyelv" TEXT, "alak" TEXT, "kiejtes" TEXT, "megjegyzes" TEXT)
-- ;;
CREATE TABLE "kiejtes_szabalyok" ("sorszam" TEXT, "minta" TEXT, "csere" TEXT, "megjegyzes" TEXT)
-- ;;
CREATE TABLE "kjv" ("igehely" TEXT, "sorszam" INTEGER, "strong" TEXT, "strong_nyers" TEXT, "angol_szo" TEXT, "morf" TEXT, "step_nyers" TEXT, "kk_leképezés" TEXT, "szosorszam_nyers" TEXT)
-- ;;
CREATE TABLE "konyv" ("kk_kod" TEXT, "sorrend" INTEGER, "step_kod" TEXT, "teljes_nev" TEXT, "normalizalo_kod" TEXT)
-- ;;
CREATE TABLE "kozel_keleti_hatar" ("id" TEXT, "proza_emlites" TEXT, "forras" TEXT)
-- ;;
CREATE TABLE "kulcsszavak" ("tanulmany" TEXT, "igehely" TEXT, "szo" TEXT, "strong" TEXT, "datum" TEXT)
-- ;;
CREATE TABLE "lap_atnezesek" ("id" TEXT, "lap_commit" TEXT, "datum" TEXT, "ki" TEXT, "idezet" TEXT, "forras" TEXT)
-- ;;
CREATE TABLE "lap_befagyasztas" ("id" TEXT, "ok" TEXT, "dontes" TEXT, "datum" TEXT)
-- ;;
CREATE TABLE "lap_javitasok" ("id" TEXT, "hely" TEXT, "tipus" TEXT, "gond" TEXT, "regi" TEXT, "uj" TEXT, "javasolta" TEXT, "jovahagyta" TEXT, "datum" TEXT, "proveniencia" TEXT)
-- ;;
CREATE TABLE "lapgen_bemenetek" ("id" TEXT, "utvonal" TEXT, "leiras" TEXT, "kotelezo" TEXT, "javitas" TEXT, "frissesseg" TEXT, "allapot" TEXT, "licenc_kulcs" TEXT, "olvasoi_nev_kulcs" TEXT, "irodalom" TEXT, "forras" TEXT)
-- ;;
CREATE TABLE "lapgen_sablonok" ("kulcs" TEXT, "mondat" TEXT, "parameterek" TEXT, "szakasz" TEXT, "eredet" TEXT, "dontes" TEXT)
-- ;;
CREATE TABLE "lexikon_hivatkozasok" ("strong" TEXT, "szotar" TEXT, "entry_id" TEXT, "jelentes_szam" TEXT, "szoveg_en" TEXT, "forrasfajl" TEXT)
-- ;;
CREATE TABLE "licencek" ("dataset" TEXT, "licenc" TEXT, "verzio_vagy_commit" TEXT, "forras_hely" TEXT, "forras_kereskedelmi" TEXT, "share_alike" TEXT, "kotelezo_megjeloles" TEXT, "allapot" TEXT, "megjegyzes" TEXT, "cimke" TEXT)
-- ;;
CREATE TABLE "lsj" ("strong_padded" TEXT, "strong_eredeti" TEXT, "teljes_szocikk" TEXT, "strong" TEXT)
-- ;;
CREATE TABLE "lxx_bridge" ("hebrew_strong" TEXT, "greek_strong" TEXT, "count" TEXT, "strong" TEXT)
-- ;;
CREATE TABLE "lxx_dontesek" ("id" TEXT, "igehely" TEXT, "lxx_igehely" TEXT, "heber_strong" TEXT, "gorog_lemma" TEXT, "gorog_strong" TEXT, "lxx_pozicio" TEXT, "tipus" TEXT, "megjegyzes" TEXT, "bizonyossag" TEXT, "proveniencia" TEXT)
-- ;;
CREATE TABLE "lxx_token" ("lxx_igehely" TEXT, "kjv_vers" TEXT, "karoli_igehely" TEXT, "karoli_ok" TEXT, "pozicio" INTEGER, "szoalak" TEXT, "lemma" TEXT, "morf" TEXT, "strong" TEXT, "strong_ok" TEXT, "szovegforma" TEXT)
-- ;;
CREATE TABLE "lxx_versszam" ("karoli_igehely" TEXT, "lxx_igehely" TEXT, "kjv_vers" TEXT, "forras" TEXT, "megjegyzes" TEXT, "szovegforma" TEXT, "terkep_ertek" TEXT)
-- ;;
CREATE TABLE "lxx_versszintu_parok" ("heber_strong" TEXT, "igehely" TEXT, "lxx_igehely" TEXT, "gorog_strong" TEXT, "proveniencia" TEXT, "strong" TEXT)
-- ;;
CREATE TABLE "mcged" ("strong" TEXT, "gk_szam" TEXT, "lemma_gorog" TEXT, "atirat" TEXT, "gyakorisag" TEXT, "glossza" TEXT)
-- ;;
CREATE TABLE "meta" ("kulcs" TEXT, "ertek" TEXT)
-- ;;
CREATE TABLE "morf_kulcs_heber" ("pozicio" TEXT, "nyelv" TEXT, "kod" TEXT, "jelentes_forras" TEXT, "jelentes_hu" TEXT, "forras" TEXT, "proveniencia" TEXT)
-- ;;
CREATE TABLE "morf_nyelv_aramai" ("xml_id" TEXT, "ref" TEXT, "morf" TEXT, "nyelv" TEXT)
-- ;;
CREATE TABLE "motivum_kapcsolatok" ("id_a" TEXT, "igehely_a" TEXT, "alpont_a" TEXT, "id_b" TEXT, "igehely_b" TEXT, "alpont_b" TEXT, "tipus" TEXT, "funkcio" TEXT, "bizonyossag" TEXT, "pardes_szint" TEXT, "indoklas" TEXT, "dontes_ref" TEXT, "proveniencia" TEXT)
-- ;;
CREATE TABLE "motivumok" ("id" TEXT, "cim" TEXT, "ui_cimke" TEXT, "tema" TEXT, "pardes_szint" TEXT, "statusz" TEXT, "statusz_verzio" TEXT, "statusz_datum" TEXT, "azonossag_tipusa" TEXT, "negativ_kriterium" TEXT, "folerendelt_fogalom" TEXT, "sablon_verzio" TEXT, "forras_study" TEXT, "meghatarozas" TEXT)
-- ;;
CREATE TABLE "nave_basokant" ("tema_id" TEXT, "tema" TEXT, "sor" TEXT, "sor_jel" TEXT, "tetel" TEXT, "cimke" TEXT, "kapcsolat" TEXT, "igehely" TEXT, "igehely_osis" TEXT, "hely_tipus" TEXT, "karoli_allapot" TEXT, "igehely_karoli" TEXT, "cel_tema" TEXT, "megjegyzes" TEXT)
-- ;;
CREATE TABLE "nave_tema_hu" ("tema_id" TEXT, "cimke_en" TEXT, "angol" TEXT, "magyar" TEXT, "forras_hash" TEXT, "allapot" TEXT, "modell" TEXT, "datum" TEXT, "proveniencia" TEXT)
-- ;;
CREATE TABLE "nave_vers" ("forras_sor" INTEGER, "tema_id" TEXT, "tema" TEXT, "cimke" TEXT, "kapcsolat" TEXT, "nave_hely" TEXT, "igehely" TEXT, "tartomanyos" INTEGER)
-- ;;
CREATE TABLE "normalizalas_jelentes" ("tabla" TEXT, "nyers" TEXT, "ok" TEXT, "darab" INTEGER)
-- ;;
CREATE TABLE "nyilt_angol" ("tabla" TEXT, "oszlop" TEXT, "sorkulcs" TEXT, "forras_hash" TEXT, "forras_hu" TEXT, "angol" TEXT, "modell" TEXT, "datum" TEXT)
-- ;;
CREATE TABLE "nyilt_kodkonyv" ("tabla" TEXT, "oszlop" TEXT, "ertek" TEXT, "leiras_hu" TEXT, "leiras_en" TEXT, "cimke_en" TEXT, "proveniencia" TEXT)
-- ;;
CREATE TABLE "olvasoi_nevtabla" ("tipus" TEXT, "kulcs" TEXT, "olvasoi_nev" TEXT, "eredet" TEXT)
-- ;;
CREATE TABLE "oshl_bdb_igehelyek" ("strong" TEXT, "bdb_id" TEXT, "sorszam" TEXT, "konyv" TEXT, "fejezet" TEXT, "vers" TEXT)
-- ;;
CREATE TABLE "oshl_lexikalis_index" ("strong" TEXT, "strong_eredeti" TEXT, "twot" TEXT, "bdb_id" TEXT, "nyelv" TEXT, "oshl_id" TEXT, "lemma" TEXT, "atiras" TEXT, "szofaj" TEXT, "def_en" TEXT, "etym_tipus" TEXT, "etym_cel" TEXT, "gyok" TEXT)
-- ;;
CREATE TABLE "otlettar" ("id" TEXT, "sav" TEXT, "cim" TEXT, "forras" TEXT, "allapot" TEXT, "megjegyzes" TEXT)
-- ;;
CREATE TABLE "res_forras" ("id" TEXT, "res" TEXT, "fejlec" TEXT, "forras" TEXT, "tanulmany" TEXT)
-- ;;
CREATE TABLE "sdbh_domenek" ("strong" TEXT, "strong_kod" TEXT, "osszetett" TEXT, "nyelv" TEXT, "szotar" TEXT, "entry_id" TEXT, "lemma" TEXT, "lexid" TEXT, "entry_kod" TEXT, "domen_kod" TEXT, "domen" TEXT, "glossza" TEXT, "hivatkozas_n" TEXT)
-- ;;
CREATE TABLE "sdgnt_domenek" ("strong" TEXT, "strong_kod" TEXT, "osszetett" TEXT, "nyelv" TEXT, "szotar" TEXT, "entry_id" TEXT, "lemma" TEXT, "lexid" TEXT, "entry_kod" TEXT, "domen_kod" TEXT, "domen" TEXT, "glossza" TEXT, "hivatkozas_n" TEXT)
-- ;;
CREATE TABLE "sece_g" ("strong_padded" TEXT, "strong_eredeti" TEXT, "teljes_szocikk" TEXT, "strong" TEXT)
-- ;;
CREATE TABLE "sece_h" ("strong_padded" TEXT, "strong_eredeti" TEXT, "teljes_szocikk" TEXT, "strong" TEXT)
-- ;;
CREATE TABLE "strong_parok" ("a" TEXT, "b" TEXT, "n" INTEGER)
-- ;;
CREATE TABLE "strong_szotar" ("strong_szam" TEXT, "szoto" TEXT, "kiejtes" TEXT, "szofaj" TEXT, "gyok_szarmaztatas" TEXT, "jelentes" TEXT, "strong" TEXT)
-- ;;
CREATE TABLE "szotar_szakasz_cimke" ("szotar" TEXT, "strong" TEXT, "bdb_id" TEXT, "szakasz" TEXT, "lexikon_jelentes_szam" TEXT, "cimke_hu" TEXT, "proveniencia" TEXT, "megjegyzes" TEXT)
-- ;;
CREATE TABLE "szotar_szerepek" ("nyelv" TEXT, "sorrend" TEXT, "szerep" TEXT, "forras" TEXT, "allapot" TEXT)
-- ;;
CREATE TABLE "szotari_alak" ("alak" TEXT, "szotari_alak" TEXT, "szotari_alak_mai" TEXT, "alapige" TEXT, "tovabbi_elfogadhato" TEXT, "modszer" TEXT, "szabaly_forras" TEXT, "regies_jegy" TEXT)
-- ;;
CREATE TABLE "szotari_kereso" ("keresoalak" TEXT, "alak" TEXT, "mezok" TEXT)
-- ;;
CREATE TABLE "szotari_token_kotojeles" ("igehely" TEXT, "sorszam" INTEGER, "alak" TEXT, "pontos_talalat" INTEGER)
-- ;;
CREATE TABLE "szoveg_kjv" ("igehely" TEXT, "sorrend" INTEGER, "step_nyers" TEXT, "kk_lekepezes" TEXT, "szoveg" TEXT, "szoveg_jelolt" TEXT)
-- ;;
CREATE TABLE "szoveg_modern" ("igehely" TEXT, "szoveg" TEXT, "valtozott" TEXT)
-- ;;
CREATE TABLE "tabla_licenc" ("tabla" TEXT, "licenc_allapot" TEXT, "kereskedelmi" TEXT, "licenc_dataset" TEXT, "cimke" TEXT)
-- ;;
CREATE TABLE "tanulmany" ("tanulmany_id" TEXT, "fajl" TEXT, "tipus" TEXT, "cim" TEXT, "tartomany" TEXT, "sorrend" INTEGER)
-- ;;
CREATE TABLE "tanulmany_hivatkozas" ("tanulmany_id" TEXT, "szakasz_horgony" TEXT, "szakasz_cim" TEXT, "igehely" TEXT, "fokozat" TEXT, "hivatkozas" TEXT, "tartomanyban" INTEGER)
-- ;;
CREATE TABLE "tanulmany_szoveg" ("tanulmany_id" TEXT, "szoveg" TEXT)
-- ;;
CREATE TABLE "tanulmany_tartomany" ("tanulmany_id" TEXT, "resz" INTEGER, "kezdo" TEXT, "veg" TEXT, "kezdo_sorrend" INTEGER, "veg_sorrend" INTEGER)
-- ;;
CREATE TABLE "tbesg" ("strong" TEXT, "estrong_nyers" TEXT, "dstrong" TEXT, "ustrong" TEXT, "szo" TEXT, "atiras" TEXT, "morf" TEXT, "gloss" TEXT, "jelentes" TEXT)
-- ;;
CREATE TABLE "tbesh" ("strong" TEXT, "estrong_nyers" TEXT, "dstrong" TEXT, "ustrong" TEXT, "szo" TEXT, "atiras" TEXT, "morf" TEXT, "gloss" TEXT, "jelentes" TEXT)
-- ;;
CREATE TABLE "tematikus_sajat_szo" ("id" TEXT, "igehely" TEXT, "strong" TEXT, "forras" TEXT)
-- ;;
CREATE TABLE "tematikus_temak" ("id" TEXT, "forras" TEXT, "tema_id" TEXT, "tema" TEXT, "dontes" TEXT, "indok" TEXT, "proveniencia" TEXT)
-- ;;
CREATE TABLE "terminologia" ("angol" TEXT, "magyar" TEXT, "megjegyzes" TEXT, "verzio" TEXT, "kapu" TEXT)
-- ;;
CREATE TABLE "thayer" ("strong_padded" TEXT, "strong_eredeti" TEXT, "teljes_szocikk" TEXT, "strong" TEXT)
-- ;;
CREATE TABLE "thayer_aranyminta" ("seed" TEXT, "azon" TEXT, "reteg" TEXT, "strong" TEXT, "sorszam" TEXT, "gep_konyv_vers" TEXT, "gep_utvonal" TEXT, "a_konyv_vers" TEXT, "a_jelentespont" TEXT, "a_melyebb" TEXT, "b_konyv_vers" TEXT, "b_jelentespont" TEXT, "b_melyebb" TEXT, "arany_konyv_vers" TEXT, "arany_utvonal" TEXT, "itelet" TEXT, "osztaly" TEXT, "indoklas" TEXT, "kitolto_modell" TEXT, "proveniencia" TEXT)
-- ;;
CREATE TABLE "thayer_forras_javitas" ("strong" TEXT, "sorszam" TEXT, "hiba" TEXT, "tsv_poz" TEXT, "sor_poz" TEXT, "elotte" TEXT, "javitott_alak" TEXT, "utana" TEXT, "hossz" TEXT, "allapot" TEXT, "indok" TEXT, "proveniencia" TEXT)
-- ;;
CREATE TABLE "thayer_sigla" ("forrasalak" TEXT, "gyujtes" TEXT, "tipus" TEXT, "jelentes" TEXT, "magyar_alak" TEXT, "elofordulas" TEXT, "szocikk" TEXT, "gerinc_elofordulas" TEXT, "pelda" TEXT, "allapot" TEXT, "besorolas_proveniencia" TEXT, "proveniencia" TEXT)
-- ;;
CREATE TABLE "thayer_szakaszok" ("strong" TEXT, "sorszam" TEXT, "utvonal" TEXT, "jel" TEXT, "szoveg" TEXT, "illesztes" TEXT, "forras" TEXT, "forras_hash" TEXT, "proveniencia" TEXT)
-- ;;
CREATE TABLE "thayer_vers_jelentes" ("strong" TEXT, "sorszam" TEXT, "szakasz" TEXT, "konyv" TEXT, "fejezet" TEXT, "vers" TEXT, "karoli_vers" TEXT, "utvonal" TEXT, "proveniencia" TEXT)
-- ;;
CREATE TABLE "tiltott_fordulatok" ("magyar_alak" TEXT, "minta" TEXT, "ertelem" TEXT, "helyette" TEXT, "indoklas" TEXT, "verzio" TEXT, "proveniencia" TEXT)
-- ;;
CREATE TABLE "tipnr" ("nev" TEXT, "nevvaltozat" TEXT, "strong" TEXT, "utotag" TEXT, "strong_nyers" TEXT, "nyelv" TEXT, "igehely" TEXT, "step_nyers" TEXT)
-- ;;
CREATE TABLE "token_eredeti" ("igehely" TEXT, "sorszam" INTEGER, "nyelv" TEXT, "strong_lanc" TEXT, "strong_nyers" TEXT, "alak" TEXT, "kiejtes" TEXT, "szoto" TEXT, "rovid_jelentes" TEXT, "angol_tukorford" TEXT, "kritikai_kiadas" TEXT, "forras_fajl" TEXT, "van_vers" INTEGER)
-- ;;
CREATE TABLE "token_karoli" ("igehely" TEXT, "oldal" TEXT, "sorszam" INTEGER, "szo" TEXT, "allapot" TEXT, "partner_sorszam" TEXT, "strong" TEXT, "bizonyossag" TEXT, "forras" TEXT, "szo_kis" TEXT)
-- ;;
CREATE TABLE "token_macula" ("xml_id" TEXT, "igehely" TEXT, "sorszam" INTEGER, "kk_mod" TEXT, "allapot" TEXT, "szo" TEXT, "lemma" TEXT, "strong" TEXT, "strong_nyers" TEXT, "strong_poz" INTEGER, "strong_n" INTEGER, "morf" TEXT, "szofaj" TEXT, "gloss" TEXT, "lxx_szo" TEXT, "lxx_strong" TEXT, "lxx_szo_forras" TEXT, "lxx_szo_rahlfs" TEXT)
-- ;;
CREATE TABLE "token_modern" ("igehely" TEXT, "sorszam" INTEGER, "alak" TEXT)
-- ;;
CREATE TABLE "token_par" ("igehely" TEXT, "hu_sorszam" INTEGER, "hu_szo" TEXT, "er_sorszam" INTEGER, "er_szo" TEXT, "strong" TEXT, "bizonyossag" TEXT, "forras" TEXT, "hu_szo_kis" TEXT)
-- ;;
CREATE TABLE "token_strong" ("igehely" TEXT, "sorszam" INTEGER, "strong" TEXT)
-- ;;
CREATE TABLE "tsk" ("igehely" TEXT, "cel_igehely" TEXT, "votes" INTEGER)
-- ;;
CREATE TABLE "tw_szocikkek" ("tw_id" TEXT, "kategoria" TEXT, "cim" TEXT, "strong" TEXT, "szoveg" TEXT, "forras_commit" TEXT)
-- ;;
CREATE TABLE "ubs_dbh_jelentesek" ("strong" TEXT, "strong_kod" TEXT, "lemma" TEXT, "main_id" TEXT, "lexid" TEXT, "entry_kod" TEXT, "domen_kod" TEXT, "domen" TEXT, "definicio_rovid" TEXT, "definicio_hosszu" TEXT, "glosszak" TEXT, "megjegyzes" TEXT)
-- ;;
CREATE TABLE "ubs_dbh_referenciak" ("lexid" TEXT, "strong" TEXT, "igehely" TEXT, "szopozicio" TEXT, "ref_kod" TEXT)
-- ;;
CREATE TABLE "ubs_dntg_jelentesek" ("strong" TEXT, "strong_kod" TEXT, "lemma" TEXT, "main_id" TEXT, "lexid" TEXT, "entry_kod" TEXT, "domen_kod" TEXT, "domen" TEXT, "definicio_rovid" TEXT, "definicio_hosszu" TEXT, "glosszak" TEXT, "megjegyzes" TEXT)
-- ;;
CREATE TABLE "ubs_dntg_referenciak" ("lexid" TEXT, "strong" TEXT, "igehely" TEXT, "szopozicio" TEXT, "ref_kod" TEXT)
-- ;;
CREATE TABLE "vers" ("igehely" TEXT, "konyv" TEXT, "fejezet" INTEGER, "vers" INTEGER, "sorrend" INTEGER, "karoli_szoveg" TEXT)
-- ;;
CREATE TABLE "vers_szamozas" ("igehely" TEXT, "osztaly" TEXT, "kjv_igehely" TEXT, "mt_igehely" TEXT, "szamozas" TEXT, "szamozas_forras" TEXT, "megfeleltetes_forras" TEXT)
-- ;;
CREATE TABLE "visszhang_megfelelok" ("motivum" TEXT, "strong" TEXT, "igehely" TEXT, "forras" TEXT, "alak" TEXT, "lemma" TEXT, "kiejtes" TEXT, "jelentes" TEXT, "betoldas" TEXT, "megjegyzes" TEXT, "kinyeres" TEXT, "modell" TEXT, "ellenorzes" TEXT, "proveniencia" TEXT)
-- ;;
CREATE TABLE "visszhang_tanuk" ("motivum" TEXT, "igehely" TEXT, "tanu_hely" TEXT, "hagyomany" TEXT, "tanu" TEXT, "mu" TEXT, "kor" TEXT, "kapcsolat" TEXT, "forras" TEXT, "forras_url" TEXT, "lekerdezve" TEXT, "biblindex" TEXT, "kinyeres" TEXT, "modell" TEXT, "ellenorzes" TEXT, "proveniencia" TEXT)
-- ;;
CREATE TABLE "vitatott_forrasok" ("motivum" TEXT, "pont" TEXT, "szerzo" TEXT, "cim" TEXT, "megjelenes" TEXT, "ev" TEXT, "doi" TEXT, "url" TEXT, "nyilt_eleres" TEXT, "osszefoglalo" TEXT, "lekerdezes" TEXT, "lekerdezve" TEXT, "kinyeres" TEXT, "modell" TEXT, "ellenorzes" TEXT, "proveniencia" TEXT)
-- ;;
CREATE INDEX "ix_bdb_0" ON "bdb" (strong)
-- ;;
CREATE INDEX "ix_bdb_alias_0" ON "bdb_alias" (masodlagos_strong)
-- ;;
CREATE INDEX "ix_bsb_0" ON "bsb" (igehely, sorszam)
-- ;;
CREATE INDEX "ix_bsb_1" ON "bsb" (strong)
-- ;;
CREATE INDEX "ix_frazis_pozicio_0" ON "frazis_pozicio" (igehely, oldal, sorszam)
-- ;;
CREATE INDEX "ix_frazis_pozicio_1" ON "frazis_pozicio" (strong)
-- ;;
CREATE INDEX "ix_igehely_tartomany_0" ON "igehely_tartomany" (igehely)
-- ;;
CREATE INDEX "ix_igehely_tartomany_1" ON "igehely_tartomany" (forras_tabla, forras_kulcs)
-- ;;
CREATE INDEX "ix_karoli_strong_kivonat_0" ON "karoli_strong_kivonat" (igehely)
-- ;;
CREATE INDEX "ix_karoli_strong_kivonat_1" ON "karoli_strong_kivonat" (strong)
-- ;;
CREATE INDEX "ix_kh_0" ON "kh" (igehely)
-- ;;
CREATE INDEX "ix_kh_1" ON "kh" (cel_tol)
-- ;;
CREATE INDEX "ix_kjv_0" ON "kjv" (igehely, sorszam)
-- ;;
CREATE INDEX "ix_kjv_1" ON "kjv" (strong)
-- ;;
CREATE INDEX "ix_konyv_0" ON "konyv" (kk_kod)
-- ;;
CREATE INDEX "ix_lsj_0" ON "lsj" (strong)
-- ;;
CREATE INDEX "ix_lxx_bridge_0" ON "lxx_bridge" (strong)
-- ;;
CREATE INDEX "ix_lxx_token_0" ON "lxx_token" (lxx_igehely, pozicio)
-- ;;
CREATE INDEX "ix_lxx_token_1" ON "lxx_token" (karoli_igehely, szovegforma, pozicio)
-- ;;
CREATE INDEX "ix_lxx_token_2" ON "lxx_token" (strong)
-- ;;
CREATE INDEX "ix_lxx_versszam_0" ON "lxx_versszam" (karoli_igehely)
-- ;;
CREATE INDEX "ix_lxx_versszam_1" ON "lxx_versszam" (lxx_igehely)
-- ;;
CREATE INDEX "ix_lxx_versszintu_parok_0" ON "lxx_versszintu_parok" (strong)
-- ;;
CREATE INDEX "ix_lxx_versszintu_parok_1" ON "lxx_versszintu_parok" (igehely)
-- ;;
CREATE INDEX "ix_mcged_0" ON "mcged" (strong)
-- ;;
CREATE INDEX "ix_nave_vers_0" ON "nave_vers" (igehely)
-- ;;
CREATE INDEX "ix_nave_vers_1" ON "nave_vers" (tema_id)
-- ;;
CREATE INDEX "ix_nave_vers_2" ON "nave_vers" (forras_sor)
-- ;;
CREATE INDEX "ix_normalizalas_jelentes_0" ON "normalizalas_jelentes" (tabla)
-- ;;
CREATE INDEX "ix_oshl_bdb_igehelyek_0" ON "oshl_bdb_igehelyek" (strong)
-- ;;
CREATE INDEX "ix_oshl_lexikalis_index_0" ON "oshl_lexikalis_index" (strong)
-- ;;
CREATE INDEX "ix_oshl_lexikalis_index_1" ON "oshl_lexikalis_index" (oshl_id)
-- ;;
CREATE INDEX "ix_sdbh_domenek_0" ON "sdbh_domenek" (strong)
-- ;;
CREATE INDEX "ix_sdgnt_domenek_0" ON "sdgnt_domenek" (strong)
-- ;;
CREATE INDEX "ix_sece_g_0" ON "sece_g" (strong)
-- ;;
CREATE INDEX "ix_sece_h_0" ON "sece_h" (strong)
-- ;;
CREATE INDEX "ix_strong_parok_0" ON "strong_parok" (a, b)
-- ;;
CREATE INDEX "ix_strong_parok_1" ON "strong_parok" (n)
-- ;;
CREATE INDEX "ix_strong_szotar_0" ON "strong_szotar" (strong)
-- ;;
CREATE INDEX "ix_szotari_alak_0" ON "szotari_alak" (szotari_alak)
-- ;;
CREATE INDEX "ix_szotari_kereso_0" ON "szotari_kereso" (keresoalak, alak)
-- ;;
CREATE INDEX "ix_szotari_token_kotojeles_0" ON "szotari_token_kotojeles" (igehely, sorszam)
-- ;;
CREATE INDEX "ix_szotari_token_kotojeles_1" ON "szotari_token_kotojeles" (alak)
-- ;;
CREATE INDEX "ix_szoveg_kjv_0" ON "szoveg_kjv" (igehely)
-- ;;
CREATE INDEX "ix_szoveg_modern_0" ON "szoveg_modern" (igehely)
-- ;;
CREATE INDEX "ix_tabla_licenc_0" ON "tabla_licenc" (tabla)
-- ;;
CREATE INDEX "ix_tanulmany_0" ON "tanulmany" (tanulmany_id)
-- ;;
CREATE INDEX "ix_tanulmany_hivatkozas_0" ON "tanulmany_hivatkozas" (igehely)
-- ;;
CREATE INDEX "ix_tanulmany_hivatkozas_1" ON "tanulmany_hivatkozas" (tanulmany_id, szakasz_horgony)
-- ;;
CREATE INDEX "ix_tanulmany_szoveg_0" ON "tanulmany_szoveg" (tanulmany_id)
-- ;;
CREATE INDEX "ix_tanulmany_tartomany_0" ON "tanulmany_tartomany" (kezdo_sorrend, veg_sorrend)
-- ;;
CREATE INDEX "ix_tanulmany_tartomany_1" ON "tanulmany_tartomany" (tanulmany_id)
-- ;;
CREATE INDEX "ix_tbesg_0" ON "tbesg" (strong)
-- ;;
CREATE INDEX "ix_tbesh_0" ON "tbesh" (strong)
-- ;;
CREATE INDEX "ix_thayer_0" ON "thayer" (strong)
-- ;;
CREATE INDEX "ix_tipnr_0" ON "tipnr" (igehely)
-- ;;
CREATE INDEX "ix_tipnr_1" ON "tipnr" (strong)
-- ;;
CREATE INDEX "ix_token_eredeti_0" ON "token_eredeti" (igehely, sorszam)
-- ;;
CREATE INDEX "ix_token_eredeti_1" ON "token_eredeti" (strong_lanc)
-- ;;
CREATE INDEX "ix_token_karoli_0" ON "token_karoli" (igehely, oldal, sorszam)
-- ;;
CREATE INDEX "ix_token_karoli_1" ON "token_karoli" (strong)
-- ;;
CREATE INDEX "ix_token_karoli_2" ON "token_karoli" (szo_kis, igehely, oldal, sorszam)
-- ;;
CREATE INDEX "ix_token_karoli_szo_hu" ON "token_karoli" (szo, igehely, sorszam) WHERE oldal='hu'
-- ;;
CREATE INDEX "ix_token_macula_0" ON "token_macula" (igehely, sorszam)
-- ;;
CREATE INDEX "ix_token_macula_1" ON "token_macula" (strong)
-- ;;
CREATE INDEX "ix_token_macula_2" ON "token_macula" (xml_id)
-- ;;
CREATE INDEX "ix_token_modern_0" ON "token_modern" (igehely, sorszam)
-- ;;
CREATE INDEX "ix_token_par_0" ON "token_par" (strong)
-- ;;
CREATE INDEX "ix_token_par_1" ON "token_par" (hu_szo)
-- ;;
CREATE INDEX "ix_token_par_2" ON "token_par" (igehely, hu_sorszam)
-- ;;
CREATE INDEX "ix_token_par_3" ON "token_par" (hu_szo_kis)
-- ;;
CREATE INDEX "ix_token_strong_0" ON "token_strong" (strong)
-- ;;
CREATE INDEX "ix_token_strong_1" ON "token_strong" (igehely, sorszam)
-- ;;
CREATE INDEX "ix_tsk_0" ON "tsk" (igehely)
-- ;;
CREATE INDEX "ix_tsk_1" ON "tsk" (cel_igehely)
-- ;;
CREATE INDEX "ix_ubs_dbh_jelentesek_0" ON "ubs_dbh_jelentesek" (strong)
-- ;;
CREATE INDEX "ix_ubs_dbh_referenciak_0" ON "ubs_dbh_referenciak" (strong)
-- ;;
CREATE INDEX "ix_ubs_dbh_referenciak_1" ON "ubs_dbh_referenciak" (igehely)
-- ;;
CREATE INDEX "ix_ubs_dntg_jelentesek_0" ON "ubs_dntg_jelentesek" (strong)
-- ;;
CREATE INDEX "ix_ubs_dntg_referenciak_0" ON "ubs_dntg_referenciak" (strong)
-- ;;
CREATE INDEX "ix_ubs_dntg_referenciak_1" ON "ubs_dntg_referenciak" (igehely)
-- ;;
CREATE INDEX "ix_vers_0" ON "vers" (igehely)
-- ;;
CREATE INDEX "ix_vers_1" ON "vers" (konyv, fejezet, vers)
-- ;;
CREATE INDEX "ix_vers_szamozas_0" ON "vers_szamozas" (igehely)
-- ;;
CREATE UNIQUE INDEX "ux_szotari_alak_alak" ON "szotari_alak" (alak)
