import sys, json, time
sys.path.insert(0, '../tools'); from mail import send
from common import FOOT
body = """Hi VNX team,

We run free on-chain checks of who controls tokenised assets and DeFi contracts. VNX tokens came up across several chains. These are facts read from chain today:

- Ethereum VCHF 0x79d4f0232a66c4c91b89c76362016a1707cfbf4f and VGBP 0x34c9c643becd939c950bb9f141e35777559817cb: each proxy's ProxyAdmin is owned by EOA 0x45a149f42ff0b77d148d05904dd7577df36a545a, which is also owner().
- Ethereum VEUR 0x6ba75d640bebfe5da1197bb5a2aff3327789b5d3 and VNXAU 0x6d57b2e05f26c26b549231c866bdd39779e4a488: ProxyAdmin owned by EOA 0x7b0c15f39cd987a7d3f5d8d10b57ac6d633e9403.
- Arbitrum VEUR and VCHF: ProxyAdmin owner and owner() are EOA 0xd5086f514af5d820ee58a73e9628b5d21f3ba54a. Avalanche VEUR: EOA 0xe13eb54fc8bcd06aed4c1ea13692ba85dc94fd8c. Polygon VEUR and VNXAU: EOA 0x88f239d6629e98d6828fdba8f8f415d4b903af4a.

So on each chain, one signer can replace the token implementation (balances, mint and burn logic) in a single transaction, with no on-chain multisig and no timelock. If those keys sit in an HSM or MPC setup, the on-chain picture still shows holders no delay and no second signer, and due-diligence teams increasingly ask about exactly that.
"""
send("support@vnx.li", "VNX tokens: upgrade path ends at a single EOA on each chain", body + FOOT)
open("sent.jsonl", "a").write(json.dumps({"to": "support@vnx.li", "subject": "VNX tokens: upgrade path ends at a single EOA on each chain", "sent": time.strftime("%Y-%m-%dT%H:%MZ", time.gmtime())}) + "\n")
