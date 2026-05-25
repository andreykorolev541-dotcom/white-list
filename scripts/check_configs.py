#!/usr/bin/env python3
"""
Собирает VLESS конфиги из публичных источников,
проверяет каждый и оставляет топ-150 самых быстрых.
"""
import base64, socket, ssl, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
import json, os, time, random

SOURCES = [
    "https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/Splitted-By-Protocol/vless.txt",
    "https://raw.githubusercontent.com/mahdibland/V2RayAggregator/master/Eternity.txt",
    "https://raw.githubusercontent.com/yebekhe/TelegramV2rayCollector/main/sub/normal/vless",
    "https://raw.githubusercontent.com/mfuu/v2ray/master/v2ray",
    "https://raw.githubusercontent.com/aiboboxx/v2rayfree/main/v2",
    "https://raw.githubusercontent.com/freefq/free/master/v2",
    "https://raw.githubusercontent.com/Pawdroid/Free-servers/main/sub",
    "https://raw.githubusercontent.com/peasoft/NoMoreVPN/master/subscriptions/raw.txt",
    "https://raw.githubusercontent.com/vveg26/chromego_merge/main/sub/merged_proxies_new.txt",
    "https://raw.githubusercontent.com/ALIILAPRO/v2ray/main/sub.txt",
    "https://raw.githubusercontent.com/ermaozi/get_subscribe/main/subscribe/v2ray.txt",
    "https://raw.githubusercontent.com/Leon406/SubCrawler/main/sub/share/vless",
    "https://raw.githubusercontent.com/ssrsub/ssr/master/V2Ray",
    "https://raw.githubusercontent.com/ts-sf/v2ray/main/v",
    "https://raw.githubusercontent.com/tbbatbb/Proxy/master/dist/v2ray.config.txt",
    "https://raw.githubusercontent.com/w1770946460/v2ray_free_node/main/sub",
    "https://raw.githubusercontent.com/1904240202/v2rayShare/main/v2ray",
    "https://raw.githubusercontent.com/yebekhe/TelegramV2rayCollector/main/sub/base64/mix",
    "https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/All_Configs_Sub.txt",
    "https://raw.githubusercontent.com/mahdibland/ShadowsocksAggregator/master/Eternity.txt",
]

OUTPUT_DIR  = "configs"
TIMEOUT     = 4      # секунд на проверку
MAX_WORKERS = 100    # параллельных потоков
TOP_N       = 150    # максимум конфигов в итоге


def fetch_url(url: str) -> str:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.read().decode("utf-8", errors="ignore")
    except Exception as e:
        print(f"  [WARN] {url.split('/')[-1]}: {e}")
        return ""


def decode_lines(text: str) -> list:
    text = text.strip()
    if not text:
        return []
    try:
        decoded = base64.b64decode(text + "==").decode("utf-8", errors="ignore")
        lines = [l.strip() for l in decoded.splitlines() if l.strip()]
        if any(l.startswith(("vless://", "vmess://", "trojan://")) for l in lines):
            return lines
    except Exception:
        pass
    return [l.strip() for l in text.splitlines() if l.strip()]


def parse_vless(uri: str):
    try:
        rest = uri[len("vless://"):]
        at = rest.rfind("@")
        if at == -1:
            return None
        host_part = rest[at + 1:]
        for sep in ("?", "#", "/"):
            i = host_part.find(sep)
            if i != -1:
                host_part = host_part[:i]
        if host_part.startswith("["):
            b = host_part.find("]")
            return host_part[1:b], int(host_part[b + 2:])
        if ":" in host_part:
            h, p = host_part.rsplit(":", 1)
            return h, int(p)
    except Exception:
        pass
    return None


def measure_tcp(host: str, port: int) -> float:
    """Возвращает время подключения (сек) или None если недоступен."""
    try:
        t0 = time.monotonic()
        with socket.create_connection((host, port), timeout=TIMEOUT):
            return time.monotonic() - t0
    except Exception:
        return None


def measure_tls(host: str, port: int) -> float:
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        t0 = time.monotonic()
        with socket.create_connection((host, port), timeout=TIMEOUT) as sock:
            with ctx.wrap_socket(sock, server_hostname=host):
                return time.monotonic() - t0
    except Exception:
        return None


def check_config(uri: str):
    """Возвращает (uri, latency_ms) или (uri, None) если недоступен."""
    parsed = parse_vless(uri)
    if not parsed:
        return uri, None
    host, port = parsed
    t = measure_tcp(host, port)
    if t is None:
        t = measure_tls(host, port)
    return uri, (round(t * 1000) if t is not None else None)


def is_reality(uri: str) -> bool:
    return "security=reality" in uri or "reality" in uri.lower()


def top_n(results: list, n: int) -> list:
    """Отсортировать по задержке и вернуть топ-N."""
    working = [(uri, lat) for uri, lat in results if lat is not None]
    working.sort(key=lambda x: x[1])
    return [uri for uri, _ in working[:n]]


def save_txt(name: str, lines: list):
    path = f"{OUTPUT_DIR}/{name}"
    with open(path, "w") as f:
        f.write("\n".join(lines) + "\n" if lines else "")
    print(f"  {name}: {len(lines)} конфигов")


def save_sub(name: str, lines: list):
    if not lines:
        return
    enc = base64.b64encode("\n".join(lines).encode()).decode()
    with open(f"{OUTPUT_DIR}/{name}", "w") as f:
        f.write(enc)
    print(f"  {name}: base64 подписка ({len(lines)} конфигов)")


def main():
    print(f"=== VLESS Checker | top-{TOP_N} самых быстрых ===\n")
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # ── 1. Сбор ───────────────────────────────────────────────────────────
    print(f"[1/3] Сбор конфигов из {len(SOURCES)} источников...")
    all_vless: set = set()
    for url in SOURCES:
        raw = fetch_url(url)
        if not raw:
            continue
        lines = decode_lines(raw)
        vless = [l for l in lines if l.startswith("vless://")]
        if vless:
            print(f"  +{len(vless):4d}  {url.split('github.com/')[-1][:60]}")
        all_vless.update(vless)

    configs = list(all_vless)
    # Перемешиваем чтобы не было перекоса в сторону одного источника
    random.shuffle(configs)

    reality = [c for c in configs if is_reality(c)]
    regular = [c for c in configs if not is_reality(c)]
    print(f"\n  Всего уникальных: {len(configs)} (reality={len(reality)}, regular={len(regular)})\n")

    if not configs:
        print("Конфиги не найдены.")
        sys.exit(0)

    # ── 2. Проверка с замером задержки ────────────────────────────────────
    print(f"[2/3] Проверка {len(configs)} конфигов...")
    results_reality, results_regular = [], []
    done = 0
    start = time.time()

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(check_config, uri): uri for uri in configs}
        for future in as_completed(futures):
            uri, lat = future.result()
            done += 1
            if is_reality(uri):
                results_reality.append((uri, lat))
            else:
                results_regular.append((uri, lat))
            if done % 500 == 0 or done == len(configs):
                wr = sum(1 for _, l in results_reality if l)
                wg = sum(1 for _, l in results_regular if l)
                print(f"  {done}/{len(configs)} | Рабочих: {wr + wg}")

    elapsed = round(time.time() - start, 1)

    # ── 3. Выбор топ-N и сохранение ───────────────────────────────────────
    print(f"\n[3/3] Отбор топ-{TOP_N} самых быстрых и сохранение...")

    best_reality = top_n(results_reality, TOP_N)
    best_regular = top_n(results_regular, TOP_N)
    best_all     = top_n(results_reality + results_regular, TOP_N)

    save_txt("working.txt",              best_all)
    save_sub("working_sub.txt",          best_all)
    save_txt("working_reality.txt",      best_reality)
    save_sub("working_reality_sub.txt",  best_reality)
    save_txt("working_regular.txt",      best_regular)
    save_sub("working_regular_sub.txt",  best_regular)

    stats = {
        "last_updated":      time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "sources":           len(SOURCES),
        "total_checked":     len(configs),
        "working_total":     len([u for u, l in results_reality + results_regular if l]),
        "saved_top":         len(best_all),
        "saved_reality_top": len(best_reality),
        "saved_regular_top": len(best_regular),
        "elapsed_seconds":   elapsed,
    }
    with open(f"{OUTPUT_DIR}/stats.json", "w") as f:
        json.dump(stats, f, indent=2)

    print(f"\nГотово за {elapsed}с.")


if __name__ == "__main__":
    main()
