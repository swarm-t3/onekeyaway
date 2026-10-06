import json, concurrent.futures as cf
from scan import scan, RPC
d = json.load(open('/tmp/protocols.json'))
ALIAS = {"Ethereum": "ethereum", "Multi-Chain": "ethereum", "Arbitrum": "arbitrum", "Base": "base", "BSC": "bsc",
         "Binance": "bsc", "Optimism": "optimism", "OP Mainnet": "optimism", "Polygon": "polygon", "Avalanche": "avax",
         "Sonic": "sonic", "Linea": "linea", "Blast": "blast", "Berachain": "berachain", "Fantom": "fantom", "Celo": "celo",
         "zkSync Era": "era", "Hyperliquid L1": "hyperliquid"}
jobs = []
seen = set()
for p in d:
    a = p.get("address"); tvl = p.get("tvl") or 0
    if not a or tvl < 3e5: continue
    if ":" in a: ch, addr = a.split(":", 1)
    else: ch, addr = ALIAS.get(p.get("chain"), None), a
    if ch not in RPC or not addr.startswith("0x") or len(addr) != 42: continue
    k = (ch, addr.lower())
    if k in seen: continue
    seen.add(k)
    jobs.append((p, ch, addr))
print(len(jobs), flush=True)
out = []
def work(j):
    p, ch, addr = j
    r = scan(ch, addr)
    r.update({"protocol": p["name"], "slug": p.get("slug"), "tvl": p.get("tvl"), "mcap": p.get("mcap"), "url": p.get("url"),
              "twitter": p.get("twitter"), "category": p.get("category"), "symbol": p.get("symbol"), "listedAt": p.get("listedAt"),
              "audits": p.get("audits")})
    return r
with cf.ThreadPoolExecutor(12) as ex:
    for i, r in enumerate(ex.map(work, jobs)):
        out.append(r)
        if i % 50 == 0: print(i, flush=True)
json.dump(out, open("results.json", "w"), indent=1)
import collections
print(collections.Counter(r.get("verdict", r.get("error")) for r in out))
