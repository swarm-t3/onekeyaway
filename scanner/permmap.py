"""Permission Map: every common admin role on a set of contracts, traced to its signers.
usage: python3 permmap.py "Title" chain:0xaddr[:label] ... > report.md"""
import sys, json, time
from scan import rpc, call, code, scan, classify_controller, weakest, addr_from_word, EXPLORER
GETTERS = {"owner": "0x8da5cb5b", "admin": "0xf851a440", "pendingOwner": "0xe30c3978", "guardian": "0x452a9320",
           "pauser": "0x9fd0506d", "masterMinter": "0x35d99f35", "blacklister": "0xbd102430", "rescuer": "0x38a63183",
           "minter": "0x07546172", "governance": "0x5aa6e675", "governor": "0x0c340a24", "timelock": "0xd33219b4",
           "keeper": "0xaced1661", "operator": "0x570ca735", "manager": "0x481c6a75", "strategist": "0x1fe4a686",
           "treasury": "0x61d027b3", "emergencyAdmin": "0x70905dce", "gov": "0x12d43a51", "controller": "0xf77c4791",
           "oracle": "0x7dc0d1d0", "priceOracle": "0x2630c12f", "upgrader": "0xaf269745", "multisig": "0x4783c35b",
           "securityCouncil": "0x27eb6c0f", "feeCollector": "0xc415b95c", "feeRecipient": "0x46904840"}
ROLES = {"DEFAULT_ADMIN_ROLE": "00" * 32,
         "MINTER_ROLE": "9f2df0fed2c77648de5860a4cc508cd0818c85b8b8a1ab4ceeef8d981c8956a6",
         "PAUSER_ROLE": "65d7a28e3265b37a6474929f336521b332c1681b933f6cb9f3376673440d862a",
         "UPGRADER_ROLE": "189ab7a9244df0848122154315af71fe140f3db0fe014031783b0946b8c9d2e3",
         "ADMIN_ROLE": "a49807205ce4d355092ef5a8a18f56e8913cf4a201fbe287825b095693c21775",
         "OPERATOR_ROLE": "97667070c54ef182b0f5858b034beac1b6f3089aa2d3188bb1e8929f4fa9b929",
         "MANAGER_ROLE": "241ecf16d79d0f8dbfb92cbc07fe17840425976cf0667f022fe9877caa831b08",
         "BURNER_ROLE": "3c11d16cbaffd01df69ce1c404f6340ee057498f5f00246190ea54220576a848",
         "GUARDIAN_ROLE": "55435dd261a4b9b3364963f7738a7a662ad9c84396d64be3365284bb7f0a5041",
         "KEEPER_ROLE": "fc8737ab85eb45125971625a9ebdb75cc78e01d5c1fa80c4c6e5203f47bc4fab",
         "BLACKLISTER_ROLE": "98db8a220cd0f09badce9f22d0ba7e93edb3d404448cc3560d391ab096ad16e9",
         "UPGRADE_ROLE": "88aa719609f728b0c5e7fb8dd3608d5c25d497efbb3b9dd64e9251ebba101508"}
SEV = {"single-key": "🔴 single EOA", "multisig": "🟠 multisig, no delay", "timelock": "🟢 timelock", "unknown": "⚪ contract (review)"}

def desc(ch, c):
    t = c["type"]; s = t
    if c.get("threshold"): s += f" {c['threshold']}-of-{c.get('owners') or '?'}"
    if c.get("delay_s") is not None: s += f" ({c['delay_s']/3600:.0f}h delay)"
    if "via" in c: s = "ProxyAdmin → " + desc(ch, c["via"])
    return s

def roles_of(ch, a):
    out = []
    for n, sel in GETTERS.items():
        r = call(ch, a, sel)
        if r and len(r) == 66:
            x = addr_from_word(r)
            if x and x != a and r[2:26] == "0" * 24: out.append((n + "()", x))
    for n, h in ROLES.items():
        cnt = call(ch, a, "0xca15c873" + h)
        if cnt and len(cnt) == 66 and 0 < int(cnt, 16) < 20:
            for i in range(int(cnt, 16)):
                m = addr_from_word(call(ch, a, "0x9010d07c" + h + hex(i)[2:].rjust(64, "0")))
                if m: out.append((n, m))
    return out

def run(title, targets):
    rows, cache = [], {}
    for ch, a, label in targets:
        base = scan(ch, a)
        for c in base.get("controls", []):
            if "upgrade" in c["role"]:
                rows.append((label, ch, a, "upgrade (" + c["role"].split(" (")[0] + ")", c["controller"]["address"], c["controller"], c["risk"]))
        for role, x in roles_of(ch, a):
            if (ch, x) not in cache:
                cl = classify_controller(ch, x); cache[(ch, x)] = (cl, weakest(cl))
            cl, rk = cache[(ch, x)]
            rows.append((label, ch, a, role, x, cl, rk))
    order = {"single-key": 0, "unknown": 1, "multisig": 2, "timelock": 3}
    rows.sort(key=lambda r: (order[r[6]], r[0]))
    L = [f"# Permission Map: {title}", "", f"Generated {time.strftime('%Y-%m-%d %H:%M UTC', time.gmtime())} by OneKeyAway from on-chain reads. Every address links to an explorer.", ""]
    n1 = sum(1 for r in rows if r[6] == "single-key")
    L += [f"**{len(rows)} privileged roles across {len(targets)} contracts. {n1} end at a single EOA.**", "",
          "| Risk | Contract | Role | Held by | Signer setup |", "|---|---|---|---|---|"]
    for label, ch, a, role, x, cl, rk in rows:
        e = EXPLORER.get(ch, "")
        L.append(f"| {SEV[rk]} | [{label}]({e}{a}) ({ch}) | `{role}` | [{x[:10]}…]({e}{x}) | {desc(ch, cl)} |")
    L += ["", "## What to fix first",
          "1. Move every upgrade right and every role that can move or mint funds off single EOAs, onto a Safe with at least 3 signers on separate devices.",
          "2. Put upgrades and parameter changes behind a TimelockController (24-72h), and keep a separate fast guardian that can only pause.",
          "3. Give pause/guardian roles to a different multisig than upgrades, so one compromised set can't both act and hide.",
          "4. Set up alerts on Upgraded, AdminChanged, OwnershipTransferred and RoleGranted events.", "",
          "_Limits: this reads common getters, EIP-1967/legacy proxy slots and enumerable AccessControl. Non-enumerable roles and custom auth need the manual review that is part of the Key Hardening Sprint. An EOA may be MPC- or HSM-backed off-chain, which cannot be checked on-chain._"]
    return "\n".join(L)

if __name__ == "__main__":
    title = sys.argv[1]; t = []
    for s in sys.argv[2:]:
        p = s.split(":"); t.append((p[0], p[1].lower(), p[2] if len(p) > 2 else p[1][:10]))
    print(run(title, t))
