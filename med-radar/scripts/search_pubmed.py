#!/usr/bin/env python3
"""Search PubMed and medRxiv for recent papers."""

import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import json
import sys
import time
from datetime import datetime, timedelta

def search_pubmed(query, days=7, max_results=20):
    """Search PubMed via E-utilities. Returns list of paper dicts."""
    base = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    date_from = (datetime.now() - timedelta(days=days)).strftime("%Y/%m/%d")
    date_to = datetime.now().strftime("%Y/%m/%d")

    # Step 1: search for IDs
    params = urllib.parse.urlencode({
        "db": "pubmed",
        "term": query,
        "retmax": max_results,
        "datetype": "pdat",
        "mindate": date_from,
        "maxdate": date_to,
        "retmode": "json",
        "sort": "date"
    })
    url = f"{base}/esearch.fcgi?{params}"
    with urllib.request.urlopen(url, timeout=30) as resp:
        data = json.loads(resp.read())

    id_list = data.get("esearchresult", {}).get("idlist", [])
    if not id_list:
        return []

    time.sleep(0.4)  # rate limit

    # Step 2: fetch details
    params = urllib.parse.urlencode({
        "db": "pubmed",
        "id": ",".join(id_list),
        "retmode": "xml"
    })
    url = f"{base}/efetch.fcgi?{params}"
    with urllib.request.urlopen(url, timeout=30) as resp:
        xml_data = resp.read()

    root = ET.fromstring(xml_data)
    papers = []
    for article in root.findall(".//PubmedArticle"):
        med = article.find(".//MedlineCitation")
        art = med.find(".//Article") if med is not None else None
        if art is None:
            continue

        title = art.findtext("ArticleTitle", "")
        abstract_parts = art.findall(".//Abstract/AbstractText")
        abstract = " ".join(a.text or "" for a in abstract_parts) if abstract_parts else ""

        authors_list = []
        for au in art.findall(".//AuthorList/Author"):
            ln = au.findtext("LastName", "")
            fn = au.findtext("ForeName", "")
            if ln:
                authors_list.append(f"{ln} {fn}".strip())

        journal = art.findtext(".//Journal/Title", "")
        pmid = med.findtext("PMID", "")

        # pub date
        pd = art.find(".//Journal/JournalIssue/PubDate")
        pub_date = ""
        if pd is not None:
            y = pd.findtext("Year", "")
            m = pd.findtext("Month", "")
            d = pd.findtext("Day", "")
            pub_date = f"{y}-{m}-{d}".strip("-")

        # DOI
        doi = ""
        for eid in article.findall(".//PubmedData/ArticleIdList/ArticleId"):
            if eid.get("IdType") == "doi":
                doi = eid.text or ""
                break

        papers.append({
            "title": title,
            "authors": ", ".join(authors_list[:5]) + ("..." if len(authors_list) > 5 else ""),
            "journal": journal,
            "pub_date": pub_date,
            "doi": doi,
            "pmid": pmid,
            "abstract": abstract[:1000],
            "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
            "source": "pubmed"
        })

    return papers


def search_medrxiv(query, days=7, max_results=20):
    """Search medRxiv via their API for recent preprints."""
    date_from = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    date_to = datetime.now().strftime("%Y-%m-%d")
    url = f"https://api.medrxiv.org/details/medrxiv/{date_from}/{date_to}/0/json"

    try:
        with urllib.request.urlopen(url, timeout=30) as resp:
            data = json.loads(resp.read())
    except Exception as e:
        print(f"[WARN] medRxiv API error: {e}", file=sys.stderr)
        return []

    query_lower = query.lower().split()
    papers = []
    for item in data.get("collection", []):
        text = f"{item.get('title', '')} {item.get('abstract', '')}".lower()
        if not any(q in text for q in query_lower):
            continue
        papers.append({
            "title": item.get("title", ""),
            "authors": item.get("authors", ""),
            "journal": "medRxiv (preprint)",
            "pub_date": item.get("date", ""),
            "doi": item.get("doi", ""),
            "pmid": "",
            "abstract": (item.get("abstract", "") or "")[:1000],
            "url": f"https://doi.org/{item.get('doi', '')}",
            "source": "medrxiv"
        })
        if len(papers) >= max_results:
            break

    return papers


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Search PubMed/medRxiv")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--days", type=int, default=7)
    parser.add_argument("--max", type=int, default=10)
    parser.add_argument("--source", choices=["pubmed", "medrxiv", "all"], default="all")
    args = parser.parse_args()

    results = []
    if args.source in ("pubmed", "all"):
        print(f"Searching PubMed for '{args.query}' (last {args.days} days)...", file=sys.stderr)
        results.extend(search_pubmed(args.query, args.days, args.max))
        print(f"  Found {len(results)} PubMed results", file=sys.stderr)

    if args.source in ("medrxiv", "all"):
        time.sleep(0.4)
        print(f"Searching medRxiv for '{args.query}' (last {args.days} days)...", file=sys.stderr)
        mr = search_medrxiv(args.query, args.days, args.max)
        print(f"  Found {len(mr)} medRxiv results", file=sys.stderr)
        results.extend(mr)

    print(json.dumps(results, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
