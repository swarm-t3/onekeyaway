import json, re, urllib.request, concurrent.futures as cf
EM = re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}')
BAD = ('example','sentry','wixpress','.png','.jpg','.svg','.webp','domain.com','email.com','u003e','@2x','yourname','company.com','godaddy','w3.org','schema.org')
DOMS = {"CIAN": "cian.app", "BitFi": "bitfi.one", "River": "river.inc", "Treehouse": "treehouse.finance", "YieldFi": "yield.fi",
        "Saturn": "saturn.credit", "Avalon": "avalonfinance.xyz", "TurboFlow": "tf.xyz", "Antarctic": "antarctic.exchange",
        "KAIO": "kaio.xyz", "HexTrust": "hextrust.com", "Lair": "lair.fi", "SoSoValue": "sosovalue.com", "Mitosis": "mitosis.org",
        "Peapods": "peapods.finance", "Parasail": "parasail.network", "AllBlue": "allbluedex.io", "Kipseli": "kipseli.xyz",
        "XSY": "xsy.fi", "Koi": "koi.finance", "HLP0": "hlp0.to", "Spectra": "spectra.finance", "Libre": "librecapital.com",
        "Tangible": "tangible.store", "Blueshift": "blueshift.fi", "Hyperlane": "hyperlane.xyz", "Ethena": "ethena.fi"}
PATHS = ["", "/terms", "/privacy", "/privacy-policy", "/terms-of-service", "/terms-of-use", "/legal", "/tos", "/contact", "/about"]
def get(u):
    try: return urllib.request.urlopen(urllib.request.Request(u, headers={"user-agent": "Mozilla/5.0"}), timeout=10).read(800000).decode('utf8', 'ignore')
    except Exception: return ""
def one(item):
    k, d = item; ems = set()
    for host in (d, "www." + d, "docs." + d):
        for p in PATHS:
            ems |= {e.lower().rstrip('.') for e in EM.findall(get(f"https://{host}{p}")) if not any(b in e.lower() for b in BAD)}
    return k, sorted(ems)
with cf.ThreadPoolExecutor(10) as ex:
    res = dict(ex.map(one, DOMS.items()))
json.dump(res, open('contacts_tos.json', 'w'), indent=1)
for k, v in res.items(): print(k, v)
