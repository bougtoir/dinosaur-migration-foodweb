"""Ecology and Evolution reference list + audit.

Fetches Crossref/DataCite metadata for every DOI in
manuscript/ECOEVO/reference_keys.csv (key, doi, cite_as), stores the raw
JSON (manuscript/ECOEVO/reference_metadata_raw.json; fetched once, reused
offline thereafter), and writes
  manuscript/ECOEVO/bibliography_ecoevo.md   (Harvard-style, alphabetical)
  manuscript/ECOEVO/reference_audit_ecoevo.csv
Citation coverage against the manuscript text is checked by the builder.
"""
import csv
import json
import re
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
E = ROOT / "manuscript" / "ECOEVO"
RAW = E / "reference_metadata_raw.json"
UA = {"User-Agent": "beta-bias-reference-audit (mailto:bougtoir@gmail.com)"}


def fetch(doi):
    for api in (f"https://api.crossref.org/works/{doi}",
                f"https://api.datacite.org/dois/{doi}"):
        try:
            with urllib.request.urlopen(urllib.request.Request(api, headers=UA),
                                        timeout=30) as r:
                return api.split("/")[2], json.load(r)
        except Exception:
            continue
    return None, None


def clean(s):
    s = re.sub(r"<[^>]+>", "", s or "")
    s = s.replace("&amp;", "&").replace("\u2010", "-").replace("‐", "-")
    return re.sub(r"\s+", " ", s).strip()


def title_case_fix(t):
    return t[0] + t[1:].lower() if t.isupper() else t


def name(a):
    fam = a.get("family") or a.get("familyName") or a.get("name", "")
    if fam.isupper():
        fam = fam.title()
    if re.match(r"^Mc[A-Z]{2,}$", fam):
        fam = "Mc" + fam[2:].title()
    giv = a.get("given") or a.get("givenName") or ""
    ini = " ".join(p[0] + "." for p in re.split(r"[\s\-]+", giv.replace(".", " ")) if p)
    return f"{fam}, {ini}".strip().rstrip(",")


def authors_str(names):
    if len(names) == 1:
        return names[0]
    return ", ".join(names[:-1]) + ", & " + names[-1]


keys = list(csv.DictReader(open(E / "reference_keys.csv")))
raw = json.loads(RAW.read_text()) if RAW.exists() else {}
for k in keys:
    if k["doi"] not in raw:
        src, j = fetch(k["doi"])
        raw[k["doi"]] = {"source": src, "data": j,
                         "retrieved_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
        time.sleep(0.3)
RAW.write_text(json.dumps(raw, indent=1, ensure_ascii=False))

entries, audit = [], []
for k in keys:
    rec = raw[k["doi"]]
    j = rec["data"]
    if j is None:
        audit.append({**k, "status": "FAIL"})
        continue
    if "message" in j:
        m = j["message"]
        auth = [name(a) for a in m.get("author", [])]
        eds = [name(a) for a in m.get("editor", [])]
        year = (m.get("published-print") or m.get("issued"))["date-parts"][0][0]
        if k.get("year_override"):
            year = int(k["year_override"])
        title = k.get("title_override") or title_case_fix(clean((m.get("title") or [""])[0]))
        cont = [clean(c) for c in m.get("container-title", [])]
        typ = m.get("type")
        vol, iss, pg = m.get("volume"), m.get("issue"), m.get("page") or m.get("article-number")
        if not auth and k.get("authors_override"):
            auth = k["authors_override"].split(";")
        if typ == "book-chapter":
            book = k.get("book_title") or (cont[-1] if cont else "")
            ed = k.get("book_editors") or (authors_str(eds) if eds else "")
            series = k.get("series", "")
            s = f"{authors_str(auth)} ({year}). {title}. In "
            s += (f"{ed} (Eds.), " if ed else "")
            s += f"*{book}*"
            s += (f" ({series})" if series else "")
            s += (f" (pp. {pg.replace('-', '–')})" if pg else "")
            s += f". {k.get('publisher') or m.get('publisher')}."
        else:
            jt = cont[0] if cont else ""
            s = f"{authors_str(auth)} ({year}). {title}{'' if title.endswith(('?', '!')) else '.'} *{jt}*"
            s += f", {vol}" if vol else ""
            s += f"({iss})" if iss and not str(iss).startswith("supplement") else ""
            s += f", {str(pg).replace('-', '–')}" if pg else ""
            s += "."
        first = auth[0].split(",")[0] if auth else "?"
        audit.append({**k, "status": "OK", "source": rec["source"],
                      "first_author_registry": first, "year_registry": year,
                      "title_registry": title, "container_registry": "; ".join(cont),
                      "type": typ})
    else:
        a = j["data"]["attributes"]
        auth = [name({"family": c.get("familyName", c.get("name", "")),
                      "given": c.get("givenName", "")}) for c in a["creators"]]
        year = a["publicationYear"]
        title = clean(a["titles"][0]["title"])
        s = f"{authors_str(auth)} ({year}). *{title}* [Dataset]. {a.get('publisher')}."
        audit.append({**k, "status": "OK", "source": rec["source"],
                      "first_author_registry": auth[0].split(",")[0],
                      "year_registry": year, "title_registry": title,
                      "container_registry": a.get("publisher"), "type": "dataset"})
    s += f" https://doi.org/{k['doi']}"
    entries.append((auth[0].split(",")[0].lower() if auth else "", str(year), s, k["key"]))

import unicodedata
entries.sort(key=lambda e: (unicodedata.normalize("NFKD", e[0]).encode("ascii", "ignore"), e[1], e[2]))
lines = ["# References (Ecology and Evolution; Harvard-style author–year, "
         "metadata from Crossref/DataCite)", ""]
lines += [f"- **{key}** — {s}" for _, _, s, key in entries]
(E / "bibliography_ecoevo.md").write_text("\n".join(lines) + "\n")
with open(E / "reference_audit_ecoevo.csv", "w", newline="") as fh:
    cols = sorted({c for r in audit for c in r})
    w = csv.DictWriter(fh, fieldnames=cols)
    w.writeheader()
    w.writerows(audit)
print(len(entries), "references;", sum(r["status"] != "OK" for r in audit), "failures")
