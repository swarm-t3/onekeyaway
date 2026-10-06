import json, re, urllib.request, concurrent.futures as cf, urllib.parse
r = json.load(open('results.json'))
EM = re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}')
BAD = ('example', 'sentry', 'wixpress', '.png', '.jpg', '.svg', '.webp', 'domain.com', 'email.com', 'u003e', '@2x', 'yourname')
def get(u):
    try:
        req = urllib.request.Request(u, headers={"user-agent": "Mozilla/5.0"})
        return urllib.request.urlopen(req, timeout=12).read(400000).decode('utf8', 'ignore')
    except Exception:
        return ""
def find(x):
    u = x.get('url')
    if not u: return x['protocol'], []
    p = urllib.parse.urlparse(u); base = f"{p.scheme}://{p.netloc}"
    root = '.'.join(p.netloc.split('.')[-2:])
    pages = [u, base, base + "/.well-known/security.txt", base + "/security.txt", f"https://docs.{root}", f"https://{root}"]
    ems = set()
    for pg in pages:
        for e in EM.findall(get(pg)):
            if not any(b in e.lower() for b in BAD): ems.add(e.lower())
    return x['protocol'], sorted(ems)
cands = [x for x in r if x.get('verdict', '').startswith('SINGLE') or x.get('verdict') == 'multisig, no timelock']
out = {}
with cf.ThreadPoolExecutor(16) as ex:
    for name, ems in ex.map(find, cands):
        out[name] = ems
json.dump(out, open('contacts.json', 'w'), indent=1)
print(sum(1 for v in out.values() if v), "of", len(out))
for k, v in out.items():
    if v: print(k, v)
