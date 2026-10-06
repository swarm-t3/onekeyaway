import sys, json, time
sys.path.insert(0, '../tools'); from mail import send
from common import FOOT
M = [
("hello@hyperlane.xyz", "HYPER on Arbitrum: upgrade path and owner end at a single EOA", """Hi Hyperlane team,

We run free on-chain checks of who controls DeFi contracts. HYPER on Arbitrum came up. These are facts read from chain today:

- HYPER (Arbitrum) 0xc9d23ed2adb0f551369946bd377f8644ce1ca5c4 is an upgradeable proxy. Its ProxyAdmin 0x478f23b60d1ec4cffe45a7d6a586dba66868cce8 is owned by 0xb4819e005091c10851bd4f5ecfa91f724fe7e83d, an EOA, and the same EOA is the token's owner().
  https://arbiscan.io/address/0xb4819e005091c10851bd4f5ecfa91f724fe7e83d

For a warp-route token, the owner can typically also change the ISM/hook configuration. So one signer can replace the implementation, or change what counts as a valid inbound message, in a single transaction, with no multisig or timelock in the path. It's possible this route is meant to be community-deployed or is legacy. If so, a pointer to the canonical one would help us correct our data.
"""),
("info@kaiolabs.xyz", "KAIO fund tokens on Avalanche: UUPS owner is a single EOA", """Hi KAIO team,

We run free on-chain checks of who controls tokenised assets. KAIO's Avalanche share tokens came up. These are facts read from chain today:

- Libre Institutional USD Money Market A1 0xcf2ca1b21e6f5da7a2744f89667de4e450791c79, plus five Libre SAF VCC share tokens (0xcc777c52…fb3b, 0x1b62f1b8…5d5d, 0xc1cd4ccd…7af3, 0xe5631ccf…7a9f, 0xbee4274f…6f7b), are UUPS proxies whose owner() is 0x55413c13dce4b03dee20ec1dd8351691f0c50bdd, an EOA. The implementations also expose mint.
  https://snowtrace.io/address/0x55413c13dce4b03dee20ec1dd8351691f0c50bdd

So one signer can upgrade these share tokens (balances and transfer and compliance logic) in a single transaction, with no on-chain multisig or timelock. If the key is HSM-backed, holders and allocators still can't see that on-chain, and RWA due-diligence checklists increasingly ask for it.
"""),
]
if __name__ == "__main__":
    for to, subj, body in M:
        send(to, subj, body + FOOT)
        open("sent.jsonl", "a").write(json.dumps({"to": to, "subject": subj, "sent": time.strftime("%Y-%m-%dT%H:%MZ", time.gmtime())}) + "\n")
        time.sleep(15)
