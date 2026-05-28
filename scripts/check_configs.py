#!/usr/bin/env python3
import urllib.request, os, time, json, random, re

CIDR_SOURCES = [
    ("igareck [all CIDR]",
     "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/main/WHITE-CIDR-RU-all.txt"),
    ("igareck [checked CIDR]",
     "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/main/WHITE-CIDR-RU-checked.txt"),
    ("antifilter.download [IP list]",
     "https://community.antifilter.download/list/ip.lst"),
    ("antifilter.download [summarized]",
     "https://community.antifilter.download/list/summarized.lst"),
    ("1andrevich Re-filter-lists [ipsets]",
     "https://raw.githubusercontent.com/1andrevich/Re-filter-lists/main/ipsets_all.lst"),
    ("nicklvsa russia-blocked [CIDR]",
     "https://raw.githubusercontent.com/nicklvsa/russia-blocked/main/russia.cidr"),
    ("zhongfly runet-ip [CIDR]",
     "https://raw.githubusercontent.com/zhongfly/runet-ip/main/russia-cidr.txt"),
    ("ipverse ru [CIDR]",
     "https://raw.githubusercontent.com/ipverse/rir-ip/master/country/ru/ipv4-aggregated.txt"),
]

SNI_SOURCES = [
    ("igareck [all SNI]",
     "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/main/WHITE-SNI-RU-all.txt"),
    ("antifilter.download [domains]",
     "https://community.antifilter.download/list/domains.lst"),
    ("1andrevich Re-filter-lists [domains all]",
     "https://raw.githubusercontent.com/1andrevich/Re-filter-lists/main/domains_all.lst"),
    ("1andrevich Re-filter-lists [domains lite]",
     "https://raw.githubusercontent.com/1andrevich/Re-filter-lists/main/lists/domains_lite.lst"),
    ("nicklvsa russia-blocked [domains]",
     "https://raw.githubusercontent.com/nicklvsa/russia-blocked/main/russia-domains.txt"),
    ("dartraiden no-Russia-hosts",
     "https://raw.githubusercontent.com/dartraiden/no-Russia-hosts/master/hosts.txt"),
    ("zapret-info z-i [csv]",
     "https://raw.githubusercontent.com/zapret-info/z-i/master/dump.csv"),
]

OUTPUT_DIR = "configs"
PER_SOURCE = 300


def fetch(url: str) -> str:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.read().decode("utf-8", errors="ignore")
    except Exception as e:
        print(f"  [WARN] {url.split('/')[-1]}: {e}")
        return ""


def is_cidr(line: str) -> bool:
    return bool(re.match(r"^\d{1,3}(\.\d{1,3}){3}/\d{1,2}$", line.strip()))


def is_domain(line: str) -> bool:
    line = line.strip().lstrip(".")
    return bool(re.match(r"^(?!\-)([a-zA-Z0-9\-]{1,63}\.)+[a-zA-Z]{2,}$", line)) and not line.startswith("#")


def parse_domains_from_csv(text: str) -> list:
    domains = []
    for line in text.splitlines():
        parts = line.split(";")
        if len(parts) >= 2:
            raw = parts[1].strip().strip('"').lower()
            for d in raw.split("|"):
                d = d.strip().lstrip("*.")
                if is_domain(d):
                    domains.append(d)
    return domains


def collect(sources: list, mode: str) -> set:
    result = set()
    for name, url in sources:
        raw = fetch(url)
        if not raw:
            continue
        lines = raw.splitlines()

        if "dump.csv" in url:
            items = parse_domains_from_csv(raw)
        elif mode == "cidr":
            items = [l.strip() for l in lines if is_cidr(l)]
        else:
            items = []
            for l in lines:
                l = l.strip().lstrip("*.").lower()
                if l.startswith("#") or not l:
                    continue
                parts = l.split()
                candidate = parts[-1] if len(parts) > 1 else l
                if is_domain(candidate):
                    items.append(candidate)

        if len(items) > PER_SOURCE:
            items = random.sample(items, PER_SOURCE)

        print(f"  +{len(items):5d}  {name}")
        result.update(items)

    return result


def save(filename: str, items: set) -> int:
    lines = sorted(items)
    with open(f"{OUTPUT_DIR}/{filename}", "w") as f:
        f.write("\n".join(lines) + "\n")
    print(f"  {filename}: {len(lines)} записей")
    return len(lines)


def main():
    print(f"=== CIDR + SNI Collector | до {PER_SOURCE} с каждого источника ===\n")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    start = time.time()

    print(f"[1/2] Сбор CIDR из {len(CIDR_SOURCES)} источников...")
    cidr = collect(CIDR_SOURCES, "cidr")
    print(f"  Итого уникальных CIDR: {len(cidr)}\n")

    print(f"[2/2] Сбор SNI из {len(SNI_SOURCES)} источников...")
    sni = collect(SNI_SOURCES, "sni")
    print(f"  Итого уникальных доменов: {len(sni)}\n")

    print("Сохранение...")
    n_cidr = save("CIDR-RU-all.txt", cidr)
    n_sni  = save("SNI-RU-all.txt",  sni)

    stats = {
        "last_updated":    time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "cidr_sources":    len(CIDR_SOURCES),
        "sni_sources":     len(SNI_SOURCES),
        "per_source_limit": PER_SOURCE,
        "cidr_total":      n_cidr,
        "sni_total":       n_sni,
        "elapsed_seconds": round(time.time() - start, 1),
    }
    with open(f"{OUTPUT_DIR}/stats.json", "w") as f:
        json.dump(stats, f, indent=2)

    print(f"\nГотово. CIDR: {n_cidr}, SNI: {n_sni}")


if __name__ == "__main__":
    main()
