"""OneKeyAway scanner: who controls a contract? EOA, Safe (m/n), timelock, or nobody."""
import json, sys, time, concurrent.futures as cf, urllib.request

RPC = {
    "ethereum": "https://ethereum-rpc.publicnode.com",
    "arbitrum": "https://arbitrum-one-rpc.publicnode.com",
    "base": "https://base-rpc.publicnode.com",
    "bsc": "https://bsc-rpc.publicnode.com",
    "optimism": "https://optimism-rpc.publicnode.com",
    "polygon": "https://polygon-bor-rpc.publicnode.com",
    "avax": "https://avalanche-c-chain-rpc.publicnode.com",
    "sonic": "https://sonic-rpc.publicnode.com",
    "linea": "https://linea-rpc.publicnode.com",
    "blast": "https://blast-rpc.publicnode.com",
    "berachain": "https://berachain-rpc.publicnode.com",
    "fantom": "https://fantom-rpc.publicnode.com",
    "celo": "https://celo-rpc.publicnode.com",
    "era": "https://mainnet.era.zksync.io",
    "hyperliquid": "https://rpc.hyperliquid.xyz/evm",
}
EXPLORER = {
    "ethereum": "https://etherscan.io/address/", "arbitrum": "https://arbiscan.io/address/",
    "base": "https://basescan.org/address/", "bsc": "https://bscscan.com/address/",
    "optimism": "https://optimistic.etherscan.io/address/", "polygon": "https://polygonscan.com/address/",
    "avax": "https://snowtrace.io/address/", "sonic": "https://sonicscan.org/address/",
    "linea": "https://lineascan.build/address/", "blast": "https://blastscan.io/address/",
    "berachain": "https://berascan.com/address/", "fantom": "https://ftmscan.com/address/",
    "celo": "https://celoscan.io/address/", "era": "https://era.zksync.network/address/",
    "hyperliquid": "https://hyperevmscan.io/address/",
}
IMPL = "0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc"
ADMIN = "0xb53127684a568b3173ae13b9f8a6016e243e63b6e8ee1178d6a717850b5d6103"
BEACON = "0xa3f0ad74e5423aebfd80d3ef4346578335a9a72aeaee59ff6cb3582b35133d50"
SEL = {"owner": "0x8da5cb5b", "admin": "0xf851a440", "getThreshold": "0xe75235b8",
       "getOwners": "0xa0e67e2b", "getMinDelay": "0xf27a0c92", "delay": "0x6a42b8f8"}
ZERO = "0x" + "0" * 40
POWERS = {"mint": ["6340c10f19"], "pause": ["638456cb59"], "blacklist": ["63f9f92be4", "6344337ea1", "631a895266", "63e4997dc5"],
          "burnFrom": ["6379cc6790"], "setFee/tax": ["6369fe0e2d", "63c0246668"]}
OZOS_IMPL = "0x7050c9e0f4ca769c69bd3a8ef740bc37934f8e2c036e5a723fd8ee048ed3f8c3"
OZOS_ADMIN = "0x10d6a54a4754c8869d6886b5f5d7fbfa5b4522237ea5c60d11bc4e7a1ff9390b"


def rpc(chain, method, params, tries=3):
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}).encode()
    for i in range(tries):
        try:
            req = urllib.request.Request(RPC[chain], body, {"content-type": "application/json", "user-agent": "onekeyaway/0.1"})
            r = json.load(urllib.request.urlopen(req, timeout=20))
            if "error" in r:
                return None
            return r.get("result")
        except Exception:
            time.sleep(1 + i)
    return None


def addr_from_word(w):
    if not w or len(w) < 66:
        return None
    a = "0x" + w[-40:]
    return None if a == ZERO else a


def call(chain, to, sel):
    return rpc(chain, "eth_call", [{"to": to, "data": sel}, "latest"])


def code(chain, a):
    return rpc(chain, "eth_getCode", [a, "latest"]) or "0x"


def classify_controller(chain, a, depth=0):
    """Return dict describing an address that holds control."""
    c = code(chain, a)
    if c in ("0x", "0x0", None):
        return {"type": "EOA", "address": a}
    if c.startswith("0xef0100"):
        return {"type": "EOA (7702)", "address": a}
    t = call(chain, a, SEL["getThreshold"])
    if t and t != "0x" and len(t) >= 66:
        th = int(t, 16)
        o = call(chain, a, SEL["getOwners"])
        n, owners = None, []
        if o and len(o) >= 130:
            n = int(o[66:130], 16)
            owners = ["0x" + o[130 + 64 * i + 24:130 + 64 * (i + 1)] for i in range(n)]
        res = {"type": "Safe", "address": a, "threshold": th, "owners": n}
        if th <= 1 and depth < 2 and owners:
            res["owner_types"] = [classify_controller(chain, x, depth + 1) for x in owners[:5]]
        return res
    for s in ("getMinDelay", "delay"):
        d = call(chain, a, SEL[s])
        if d and d != "0x" and len(d) >= 66:
            return {"type": "Timelock", "address": a, "delay_s": int(d, 16)}
    if depth < 2:  # e.g. ProxyAdmin -> owner
        o = addr_from_word(call(chain, a, SEL["owner"]))
        if o:
            inner = classify_controller(chain, o, depth + 1)
            return {"type": "Contract->" + inner["type"], "address": a, "via": inner}
    return {"type": "Contract (unknown)", "address": a}


def weakest(ctrl):
    """Effective risk of a controller chain."""
    t = ctrl["type"]
    if "via" in ctrl:
        return weakest(ctrl["via"])
    if t.startswith("EOA"):
        return "single-key"
    if t == "Safe":
        if ctrl.get("threshold", 0) > 1:
            return "multisig"
        subs = [weakest(x) for x in ctrl.get("owner_types", [])]
        if not subs or "single-key" in subs:
            return "single-key"
        return "unknown" if "unknown" in subs else ("multisig" if "multisig" in subs else "timelock")
    if t == "Timelock":
        return "timelock"
    return "unknown"


def scan(chain, a):
    a = a.lower()
    res = {"chain": chain, "address": a}
    c = code(chain, a)
    if c in ("0x", None):
        res["error"] = "no code"
        return res
    impl = addr_from_word(rpc(chain, "eth_getStorageAt", [a, IMPL, "latest"]))
    beacon = addr_from_word(rpc(chain, "eth_getStorageAt", [a, BEACON, "latest"]))
    admin = addr_from_word(rpc(chain, "eth_getStorageAt", [a, ADMIN, "latest"]))
    if not impl:
        impl = addr_from_word(rpc(chain, "eth_getStorageAt", [a, OZOS_IMPL, "latest"]))
        if impl:
            admin = admin or addr_from_word(rpc(chain, "eth_getStorageAt", [a, OZOS_ADMIN, "latest"]))
    res["upgradeable"] = bool(impl or beacon)
    if beacon and not impl:
        impl = addr_from_word(call(chain, beacon, "0x5c60da1b"))
    body = (code(chain, impl) if impl else c).lower()
    res["powers"] = [k for k, v in POWERS.items() if any(x in body for x in v)]
    controls = []
    if admin:
        controls.append(("proxy admin (can upgrade)", admin))
    elif beacon:
        bo = addr_from_word(call(chain, beacon, SEL["owner"]))
        if bo:
            controls.append(("beacon owner (can upgrade)", bo))
    own = addr_from_word(call(chain, a, SEL["owner"]))
    if own:
        controls.append(("owner()" + (" (UUPS: can upgrade)" if impl and not admin else ""), own))
    res["controls"] = []
    for role, ca in controls:
        cl = classify_controller(chain, ca)
        res["controls"].append({"role": role, "controller": cl, "risk": weakest(cl)})
    risks = [x["risk"] for x in res["controls"]]
    if not risks:
        res["verdict"] = "no owner/admin found" + (" (upgradeable, admin unknown)" if res["upgradeable"] else "")
    elif "single-key" in risks:
        upg = any("upgrade" in x["role"] and x["risk"] == "single-key" for x in res["controls"])
        res["verdict"] = "SINGLE KEY can upgrade" if upg else "SINGLE KEY owner"
    elif "unknown" in risks:
        res["verdict"] = "controlled by unrecognised contract"
    elif "multisig" in risks and "timelock" not in risks:
        res["verdict"] = "multisig, no timelock"
    else:
        res["verdict"] = "timelock / multisig"
    return res


if __name__ == "__main__":
    print(json.dumps(scan(sys.argv[1], sys.argv[2]), indent=1))
