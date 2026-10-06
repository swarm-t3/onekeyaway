"""Scan TVL-holding contracts of recently listed protocols, using DefiLlama adapter addresses."""
import json, re, os, time, collections, concurrent.futures as cf
from scan import scan, code, RPC
d = json.load(open('/tmp/protocols.json'))
CH = {"Ethereum": "ethereum", "Arbitrum": "arbitrum", "Base": "base", "BSC": "bsc", "Binance": "bsc", "Optimism": "optimism",
      "OP Mainnet": "optimism", "Polygon": "polygon", "Avalanche": "avax", "Sonic": "sonic", "Linea": "linea", "Blast": "blast",
      "Berachain": "berachain", "Hyperliquid L1": "hyperliquid", "zkSync Era": "era"}
cut = 0
DONE = {x['protocol'] for x in json.load(open('results2.json'))}
prots = [p for p in d if (p.get('listedAt') or 0) > cut and 1e6 < (p.get('tvl') or 0) < 5e9 and p['name'] not in DONE and set(p.get('chains', [])) & set(CH)
         and p.get('category') not in ('CEX', 'Chain')]
ADDR = re.compile(r'0x[a-fA-F0-9]{40}\b')
per = {}
for p in prots:
    dd = '/tmp/dla/projects/' + p['module'].split('/')[0]
    if not os.path.isdir(dd): continue
    s = []
    for root, _, fs in os.walk(dd):
        for f in fs:
            if f.endswith(('.js', '.ts', '.json')):
                s += ADDR.findall(open(os.path.join(root, f), errors='ignore').read())
    per[p['name']] = (p, list(dict.fromkeys(a.lower() for a in s)))
freq = collections.Counter(a for _, (p, al) in per.items() for a in set(al))
jobs = []
for name, (p, al) in per.items():
    al = [a for a in al if freq[a] <= 2][:8]
    chains = [CH[c] for c in p['chains'] if c in CH]
    for a in al: jobs.append((p, a, chains))
print(len(per), "protocols,", len(jobs), "addresses", flush=True)
def work(j):
    p, a, chains = j
    for ch in chains:
        c = code(ch, a)
        if c and c != '0x' and not c.startswith('0xef0100'):
            r = scan(ch, a)
            r.update({"protocol": p["name"], "tvl": p.get("tvl"), "url": p.get("url"), "twitter": p.get("twitter"),
                      "category": p.get("category"), "listedAt": p.get("listedAt"), "github": p.get("github")})
            return r
    return None
out = []
with cf.ThreadPoolExecutor(16) as ex:
    for i, r in enumerate(ex.map(work, jobs)):
        if r: out.append(r)
        if i % 100 == 0: print(i, flush=True)
json.dump(out, open('results3.json', 'w'), indent=1)
print(collections.Counter(r.get('verdict', r.get('error')) for r in out))
