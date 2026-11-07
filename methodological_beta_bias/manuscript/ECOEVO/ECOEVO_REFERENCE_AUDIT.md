# ECOEVO reference audit

Every DOI was resolved against Crossref (DataCite for the Dryad dataset) by `analysis/27_ecoevo_references.py`; raw metadata are archived in `manuscript/ECOEVO/reference_metadata_raw.json`. The reference list is generated from that metadata (Harvard author–year, alphabetical; E&E applies its own style in production). Citation coverage is enforced by the builder: every reference is cited and every in-text citation has a reference.

References: 55; resolution failures: 0; uncited: 0.

**Status: PASS**

## Corrections made in this audit

| Problem found | Correction |
|---|---|
| In-text 'Kidwell & Behrensmeyer, 1991' had no matching entry; the listed chapter (DOI 10.1007/978-1-4899-5034-5_4) is by Kidwell & Bosence | Citation changed to Kidwell & Bosence (1991); editors (Allison & Briggs) and series added from Crossref |
| 'Kowalewski, 1999': DOI 10.1017/cbo9780511612381.006 is chapter 6 of Martin (1999) *Taphonomy*, a single-author Cambridge book (Crossref book record lists R. E. Martin as sole author) | Citation and entry changed to Martin (1999) |
| Whittaker (1960) DOI 10.2307/1948435 resolves to a one-page item in issue 30(4) | Replaced by the monograph DOI 10.2307/1943563 (30(3), 279–338) |
| Maidment (2024) Dryad dataset has a single DataCite creator but was cited as 'Maidment et al.' | Cited as Maidment (2024) |
| Peters & McClennen: issue year 2016 (online 2015) | Cited by issue year, 2016 |
| Baselga (2012) and Noto & Grossman (2010) were in the JBI list but uncited | Cited where substantively relevant (replacement vs richness difference; prior Morrison palaeoecology) |
| Evidence audit attributed the *Hispanosauropus* paper to 'Lockley et al. 2015' | Corrected to Foster (2015) (sole Crossref author) in `INDEPENDENT_EVIDENCE_AUDIT.md`; manuscript cites it only as non-diagnostic trackway evidence, not for diet |
| Internal bibliography keys did not match authors (e.g. `gaston2008` for McGeoch & Gaston 2002) | Keys renamed (cosmetic) |

Note: Crossref lists only the first page for Wiens (1989) (Functional Ecology 3(4), 385); the entry is left as registered.

## Entries

| key | cited as | in-text hits | DOI | registry first author | year | container | status |
|---|---|---|---|---|---|---|---|
| whittaker1960 | Whittaker, 1960 | 1 | 10.2307/1943563 | Whittaker | 1960 | Ecological Monographs | OK |
| tuomisto2010 | Tuomisto, 2010 | 1 | 10.1111/j.1600-0587.2009.06148.x | Tuomisto | 2010 | Ecography | OK |
| moreno2010 | Moreno & Rodríguez, 2010 | 1 | 10.1007/s00442-010-1591-7 | Moreno | 2010 | Oecologia | OK |
| baselga2010 | Baselga, 2010 | 3 | 10.1111/j.1466-8238.2009.00490.x | Baselga | 2010 | Global Ecology and Biogeography | OK |
| baselga2012 | Baselga, 2012 | 1 | 10.1111/j.1466-8238.2011.00756.x | Baselga | 2012 | Global Ecology and Biogeography | OK |
| anderson2011 | Anderson et al., 2011 | 1 | 10.1111/j.1461-0248.2010.01552.x | Anderson | 2011 | Ecology Letters | OK |
| legendre2014 | Legendre, 2014 | 3 | 10.1111/geb.12207 | Legendre | 2014 | Global Ecology and Biogeography | OK |
| kraft2011 | Kraft et al., 2011 | 2 | 10.1126/science.1208584 | Kraft | 2011 | Science | OK |
| chase2011 | Chase et al., 2011 | 2 | 10.1890/es10-00117.1 | Chase | 2011 | Ecosphere | OK |
| chase2018 | Chase et al., 2018 | 2 | 10.1111/ele.13151 | Chase | 2018 | Ecology Letters | OK |
| nekolawhite1999 | Nekola & White, 1999 | 2 | 10.1046/j.1365-2699.1999.00305.x | Nekola | 1999 | Journal of Biogeography | OK |
| soininen2007 | Soininen et al., 2007 | 2 | 10.1111/j.0906-7590.2007.04817.x | Soininen | 2007 | Ecography | OK |
| morlon2008 | Morlon et al., 2008 | 2 | 10.1111/j.1461-0248.2008.01202.x | Morlon | 2008 | Ecology Letters | OK |
| barton2013 | Barton et al., 2013 | 1 | 10.1111/geb.12031 | Barton | 2013 | Global Ecology and Biogeography | OK |
| wiens1989 | Wiens, 1989 | 1 | 10.2307/2389612 | Wiens | 1989 | Functional Ecology | OK |
| avolio2019 | Avolio et al., 2019 | 1 | 10.1002/ecs2.2881 | Avolio | 2019 | Ecosphere | OK |
| lennon2004 | Lennon et al., 2004 | 2 | 10.1046/j.1461-0248.2004.00548.x | Lennon | 2004 | Ecology Letters | OK |
| mcgeoch2002 | McGeoch & Gaston, 2002 | 2 | 10.1017/s1464793101005887 | McGeoch | 2002 | Biological Reviews | OK |
| bertrand2006 | Bertrand et al., 2006 | 2 | 10.1017/s1477200005001908 | Bertrand | 2006 | Systematics and Biodiversity | OK |
| bevilacqua2009 | Bevilacqua et al., 2009 | 2 | 10.1016/j.marpolbul.2009.07.018 | Bevilacqua | 2009 | Marine Pollution Bulletin | OK |
| olszewski1999 | Olszewski, 1999 | 3 | 10.1017/s009483730002652x | Olszewski | 1999 | Paleobiology | OK |
| kidwell1991 | Kidwell & Bosence, 1991 | 2 | 10.1007/978-1-4899-5034-5_4 | Kidwell | 1991 | Topics in Geobiology; Taphonomy | OK |
| tomasovych2010 | Tomašových & Kidwell, 2010 | 1 | 10.1666/08092.1 | Tomašových | 2010 | Paleobiology | OK |
| blowes2019 | Blowes et al., 2019 | 2 | 10.1126/science.aaw1620 | Blowes | 2019 | Science | OK |
| korhonen2010 | Korhonen et al., 2010 | 1 | 10.1890/09-0392.1 | Korhonen | 2010 | Ecology | OK |
| gotelli2001 | Gotelli & Colwell, 2001 | 1 | 10.1046/j.1461-0248.2001.00230.x | Gotelli | 2001 | Ecology Letters | OK |
| chao2014 | Chao et al., 2014 | 1 | 10.1890/13-0133.1 | Chao | 2014 | Ecological Monographs | OK |
| mackenzie2002 | MacKenzie et al., 2002 | 1 | 10.1890/0012-9658(2002)083[2248:esorwd]2.0.co;2 | MacKenzie | 2002 | Ecology | OK |
| colwell2012 | Colwell et al., 2012 | 1 | 10.1093/jpe/rtr044 | Colwell | 2012 | Journal of Plant Ecology | OK |
| shaffer1998 | Shaffer et al., 1998 | 2 | 10.1016/s0169-5347(97)01177-4 | Shaffer | 1998 | Trends in Ecology & Evolution | OK |
| pyke2010 | Pyke & Ehrlich, 2010 | 2 | 10.1111/j.1469-185x.2009.00098.x | Pyke | 2010 | Biological Reviews | OK |
| lavoie2013 | Lavoie, 2013 | 2 | 10.1016/j.ppees.2012.10.002 | Lavoie | 2013 | Perspectives in Plant Ecology, Evolution and Systematics | OK |
| graham2004 | Graham et al., 2004 | 2 | 10.1016/j.tree.2004.07.006 | Graham | 2004 | Trends in Ecology & Evolution | OK |
| maidment2024 | Maidment, 2024 | 2 | 10.5061/dryad.6m905qg77 | Maidment | 2024 | Dryad | OK |
| alroy2008 | Alroy, 2008 | 1 | 10.1073/pnas.0802597105 | Alroy | 2008 | Proceedings of the National Academy of Sciences | OK |
| behrensmeyer2000 | Behrensmeyer et al., 2000 | 1 | 10.1666/0094-8373(2000)26[103:tap]2.0.co;2 | Behrensmeyer | 2000 | Paleobiology | OK |
| vilhena2013 | Vilhena & Smith, 2013 | 2 | 10.1371/journal.pone.0074470 | Vilhena | 2013 | PLoS ONE | OK |
| noto2010 | Noto & Grossman, 2010 | 1 | 10.1371/journal.pone.0012553 | Noto | 2010 | PLoS ONE | OK |
| foster2015 | Foster, 2015 | 1 | 10.1080/10420940.2015.1059335 | Foster | 2015 | Ichnos | OK |
| drumheller2020 | Drumheller et al., 2020 | 1 | 10.1371/journal.pone.0233115 | Drumheller | 2020 | PLOS ONE | OK |
| martin1999 | Martin, 1999 | 1 | 10.1017/cbo9780511612381.006 | Martin | 1999 | Taphonomy | OK |
| heino2015 | Heino et al., 2015 | 1 | 10.1002/ece3.1460 | Heino | 2015 | Ecology and Evolution | OK |
| mcgill2007 | McGill et al., 2007 | 1 | 10.1111/j.1461-0248.2007.01094.x | McGill | 2007 | Ecology Letters | OK |
| socolar2016 | Socolar et al., 2016 | 2 | 10.1016/j.tree.2015.11.005 | Socolar | 2016 | Trends in Ecology & Evolution | OK |
| hillebrand2008 | Hillebrand et al., 2008 | 2 | 10.1890/07-1053.1 | Hillebrand | 2008 | Ecology | OK |
| partel2011 | Pärtel et al., 2011 | 1 | 10.1016/j.tree.2010.12.004 | Pärtel | 2011 | Trends in Ecology & Evolution | OK |
| zobel2016 | Zobel, 2016 | 1 | 10.1111/jvs.12333 | Zobel | 2016 | Journal of Vegetation Science | OK |
| uhen2013 | Uhen et al., 2013 | 1 | 10.1080/02724634.2012.716114 | Uhen | 2013 | Journal of Vertebrate Paleontology | OK |
| peters2016 | Peters & McClennen, 2016 | 2 | 10.1017/pab.2015.39 | Peters | 2016 | Paleobiology | OK |
| badgley2010 | Badgley, 2010 | 1 | 10.1111/j.1600-0587.2010.06282.x | Badgley | 2010 | Ecography | OK |
| lane2003 | Lane & Benton, 2003 | 1 | 10.1086/377188 | Lane | 2003 | The American Naturalist | OK |
| smith2007 | Smith & McGowan, 2007 | 2 | 10.1111/j.1475-4983.2007.00693.x | Smith | 2007 | Palaeontology | OK |
| keil2012 | Keil et al., 2012 | 1 | 10.1111/j.1365-2699.2012.02701.x | Keil | 2012 | Journal of Biogeography | OK |
| sfenthourakis2012 | Sfenthourakis & Panitsa, 2012 | 1 | 10.1111/j.1365-2699.2011.02639.x | Sfenthourakis | 2012 | Journal of Biogeography | OK |
| stigall2006 | Stigall & Lieberman, 2006 | 1 | 10.1111/j.1365-2699.2006.01585.x | Stigall | 2006 | Journal of Biogeography | OK |
