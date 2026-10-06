import sys, json, time
sys.path.insert(0, '../tools'); from mail import send
SITE = "https://swarm-t3.github.io/onekeyaway/"
FOOT = f"""
Why we flag this: in 2026, leaked keys and admin access overtook contract bugs as the biggest cause of DeFi losses (>$1.3B Jan-Aug). Wasabi lost ~$4.5M in April through one deployer EOA that could upgrade its contracts. The usual fix is to move the admin role to a Safe (for example 3-of-5 on separate devices) behind a TimelockController, so any upgrade is visible on-chain for 24-48h before it runs.

If the EOA is MPC- or HSM-backed, that lowers the risk but still leaves no timelock. Feel free to ignore this if you already have it covered.

You can check any contract yourself, free, in the browser: {SITE}
If you'd like us to map the rest of your contracts (every role traced to its signers), just reply.

OneKeyAway (on-chain admin-key checks)
This is a one-off note, not a list. Reply "no" and we won't write again."""
M = [
 ("admin@snuggle.fi", "Snuggle vaults: upgrade path ends at a single EOA", """Hi Snuggle team,

We run free on-chain checks of who controls DeFi contracts, and your vaults came up. These are facts read from chain today:

- Base vault 0xd3923beccb6e1ddb048ed00a0a9bd602d16b7470 (also 0x43ca8d32…f043 and 0x7d27cdfb…fd55): each proxy's ProxyAdmin is owned by 0x6ac51a706539d4f5a326da2892520180858e25ff, which is an EOA (with an EIP-7702 delegation), and the same address is owner().
  https://basescan.org/address/0x6ac51a706539d4f5a326da2892520180858e25ff
- Arbitrum vault 0x413ca90d38d964546c2fe03cb103df57372630f6: same owner, same pattern.

So one signer can replace the code of vaults that hold user deposits, immediately, with no multisig or timelock in the path.
"""),
 ("support@dgld.ch", "DGLD token: upgrade path ends at a single EOA", """Hi DGLD team,

We run free on-chain checks of who controls tokenised assets and DeFi contracts. Your token came up. These are facts read from Ethereum today:

- DGLD token 0xa9299c296d7830a99414d1e5546f5171fa01e9c8 is an upgradeable proxy. Its ProxyAdmin 0xd8b4395aafd4076ad7fa5b8c0bcd6da79750e629 is owned by 0xb1c1bc081e49b8f4bb4e1960c2f7d9cd9dff8b9d, which is an EOA.
  https://etherscan.io/address/0xd8b4395aafd4076ad7fa5b8c0bcd6da79750e629

So one signer can replace the token's code, including balances and transfer logic, immediately. There is no multisig or timelock in the path.
"""),
 ("hello@harmonix.fi", "HAR token on HyperEVM: upgrade path ends at a single EOA", """Hi Harmonix team,

We run free on-chain checks of who controls DeFi contracts, and HAR came up. These are facts read from HyperEVM today:

- HAR 0x391121d817da42ed3434d281aedbbcc416a2af18 is an upgradeable proxy. Its ProxyAdmin 0x7c95d4c96c410a6e7dedf4bc78eb93b916706ada is owned by 0xdcd170471e522fd729793e3431502a868dbb43a5, which is an EOA.

So one signer can replace the token's code, balances included, immediately. There is no multisig or timelock in the path.
"""),
 ("dev@rain.one", "Rain factory on Arbitrum: UUPS owner is a single EOA", """Hi Rain team,

We run free on-chain checks of who controls DeFi contracts, and Rain came up. These are facts read from Arbitrum today:

- The factory 0xcccb3c03d9355b01883779ef15c1be09cf3623f1 (the one DefiLlama's adapter lists as v1) is a UUPS proxy whose owner() is 0xc6b56a36405c879a4703ee49b8c5d741be2c7dc2, an EOA.
  https://arbiscan.io/address/0xcccb3c03d9355b01883779ef15c1be09cf3623f1

We haven't checked whether a factory upgrade can reach funds in markets that already exist. You'll know that better than we do. As written, though, one signer can replace the factory's code immediately.
"""),
]
log = []
for to, subj, body in M:
    send(to, subj, body + FOOT)
    log.append({"to": to, "subject": subj, "sent": time.strftime("%Y-%m-%dT%H:%MZ", time.gmtime())})
    time.sleep(20)
json.dump(log, open("sent.json", "a")); print("done")
