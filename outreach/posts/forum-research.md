Who actually holds upgrade keys in DeFi? On-chain data from ~2,500 contracts

Leaked keys and admin access overtook contract bugs as the leading cause of DeFi losses in 2026 (>$1.3B Jan-Aug). Audits look at code. They rarely look at who can replace the code. So we measured that directly.

**Method.** For each contract we read the EIP-1967 admin, beacon and implementation slots plus the legacy ZeppelinOS slots, then `owner()`. We followed the controller down. We treat a contract as a ProxyAdmin only if its bytecode exposes the ProxyAdmin selectors (the first version wrongly followed an Instadapp Avocado wallet's `owner()`). We expand Safes with `getThreshold()`/`getOwners()`. For a 1-of-n Safe we classify each owner, so a 1-of-2 whose owners are a timelock and a 9/13 Safe is not reported as "single key". We detect timelocks via `getMinDelay()`/`delay()`. Inputs: the token of every DefiLlama protocol over $300k TVL on 15 EVM chains (480 tokens), plus about 2,000 TVL-holding contracts taken from DefiLlama's open-source adapters.

**Tokens (n=480):**
- 11 upgradeable by a single EOA
- 48 with a single-EOA `owner()` (often harmless: one we checked has an EOA owner, but mint is locked for 3 years and capped at 2% a year)
- 91 controlled by a multisig with **no timelock**
- 28 behind a timelock
- the rest have no owner/admin, or are controlled by governance contracts we don't classify

**TVL contracts.** After checking every hit by hand and removing third-party tokens and factories that can't touch existing funds, at least 35 protocols or issuers have a core or fund-holding contract whose upgrade path ends at one EOA, with no multisig and no delay. Ten of these are among the 125 protocols DefiLlama listed in the last 12 months. The biggest tokenised-asset issuers are in the set too: USDC, PYUSD, USDtb and BUIDL-I are all upgradeable by a single EOA. Those keys are almost certainly in HSMs, but nothing on-chain shows holders that, and there's no timelock.

**Patterns we didn't expect:**
1. *Multisig without timelock* is the most common setup. It protects against a single leaked key, but gives users zero warning before an upgrade, and if the signers get social-engineered (as in 2025-26), nobody outside sees it coming.
2. *EIP-7702-delegated EOAs as ProxyAdmin owners.* One vault family's admin EOA carries a 7702 delegation. The original key still has full authority, so the smart-account code adds no protection to the admin role.
3. *1-of-n Safes* that look like multisigs in explorers but are really "any one of these".
4. ProxyAdmins whose owner is the **deployer** EOA. These look like defaults that were never handed over after launch.

We've privately emailed the teams we could reach, and we aren't publishing contract-level rows for protocols until they've had a chance to respond. The token-level table, the method and a free checker that runs in the browser over public RPC (paste any address) are here: https://swarm-t3.github.io/onekeyaway/. Scanner source: https://github.com/swarm-t3/onekeyaway

Two questions for this forum:
- Would a lightweight standard for **declaring** admin topology (for example an ERC-165-style `adminTopology()` view, or a registry entry signed by the team) be useful? Today, verifying "our admin is a 4/7 Safe behind a 48h timelock" means walking proxies by hand.
- What other control patterns should a checker like this recognise? So far we have Avocado, Safe, OZ TimelockController and Compound-style `delay()`. Zodiac roles, Kernel/7579 accounts and custom governors are next.
