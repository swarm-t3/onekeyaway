import sys, json, time
sys.path.insert(0, '../tools'); from mail import send
body = """Hi Tim, Aleks,

A data tip you may find useful, given that key compromise has been the theme of 2026 DeFi losses.

We read the on-chain control path (proxy admin, ProxyAdmin owner, owner(), Safe thresholds, timelocks) of 1,000+ contracts: the token of every DefiLlama protocol over $300k TVL, plus the TVL-holding contracts of 125 protocols listed in the last 12 months. Some findings, all checkable on a block explorer:

- At least 13 recently listed protocols have a core or fund-holding contract whose upgrade path ends at one externally owned account (EOA), with no multisig and no timelock. Whoever controls that key can replace the contract's code in one transaction. That is the same pattern behind Wasabi's ~$4.5M loss in April.
- The largest by protocol TVL are a PYUSD-based stablecoin wrapper (Saturn's PYUSDx, ~$157M; ProxyAdmin 0xb8a874137df3d4b0f19490eb06cfbe6b6d35e581 is owned by EOA 0x3141…b78e), a BTC yield vault (Avalon Superearn, ~$142M; vault 0xf297…d659, ProxyAdmin owner EOA 0x2557…beb1), and a perps bridge that holds user deposits on BNB Chain (TurboFlow, 0x145c…25db).
- Of 480 protocol tokens: 12 are upgradeable by one EOA, 56 have a single-EOA owner, 104 are held by a multisig with no timelock, and only 37 sit behind a timelock.

Caveats we'd stress: an EOA can be MPC- or HSM-backed off-chain, so "one EOA" does not always mean "one private key on a laptop". It does always mean no on-chain multisig and no delay. We've emailed the teams we could find addresses for. Most publish none.

The method, the token-level table and a free in-browser checker (paste any contract) are at https://swarm-t3.github.io/onekeyaway/, and the scanner source is at https://github.com/swarm-t3/onekeyaway. Happy to send the full contract list with explorer links, or walk through the method.

OneKeyAway
"""
send("tim@dlnews.com, aleks@dlnews.com", "Data tip: 13 newer DeFi protocols can be upgraded by a single EOA (incl. ~$157M PYUSDx wrapper)", body)
json.dump({"to": "tim@dlnews.com, aleks@dlnews.com", "subject": "press tip", "sent": time.strftime("%Y-%m-%dT%H:%MZ", time.gmtime())}, open("sent.json", "a"))
