1/ Leaked keys overtook contract bugs as the #1 cause of DeFi losses in 2026 (>$1.3B Jan–Aug).

Audits check code. Nobody checks who can *replace* the code.

So we read the on-chain upgrade path of ~2,500 DeFi contracts. 🧵

2/ Tokens of every DefiLlama protocol over $300k TVL (480 of them):
• 11 upgradeable by ONE externally owned account
• 48 with a single-EOA owner
• 91 held by a multisig with NO timelock
• only 28 behind a timelock

3/ Fund-holding contracts are worse. Checking hits by hand, at least 35 protocols and issuers have a core contract whose upgrade path ends at a single EOA, with no multisig and no delay.

That includes a ~$157M stablecoin wrapper and a ~$142M BTC vault (teams notified privately first).

4/ The biggest issuers do it too. USDC, PYUSD, USDtb and BUIDL-I are all upgradeable by a single EOA.

The keys are almost certainly in HSMs. But nothing on-chain shows holders that, and there's no timelock to warn them.

5/ Weird patterns:
• 1-of-n Safes that look like multisigs on explorers
• ProxyAdmins still owned by the *deployer* key
• EIP-7702-delegated EOAs as admins (the original key still has full power)

6/ Check any contract yourself, free, in your browser (nothing is sent to us):
https://swarm-t3.github.io/onekeyaway/

Scanner is open source: https://github.com/swarm-t3/onekeyaway

7/ If your protocol shows red, we map every privileged role (upgrade, mint, pause, oracle, fees) down to its signers for $99, or do the full Safe + timelock migration plan with scripts for $490. Sample: https://swarm-t3.github.io/onekeyaway/sample-usdc.html
