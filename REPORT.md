# REPORT r01-a5: OneKeyAway

_Draft, updated through the round. Final numbers are in Results._

## Idea

**Problem:** in 2026, stolen or leaked admin keys overtook smart-contract bugs as the biggest cause of DeFi losses: at least $1.3B in Jan-Aug 2026 ([hackmag](https://hackmag.com/news/defi-private-keys)). Wasabi Protocol lost ~$4.5M in April because a single deployer EOA could upgrade its contracts ([CoinDesk](https://www.coindesk.com/tech/2026/04/30/wasabi-protocol-drained-for-usd4-5-million-in-apparent-admin-key-compromise), [Halborn](https://halborn.com/blog/post/explained-the-wasabi-protocol-hack-april-2026)). Audits check code. They don't check **who holds the keys**.

**Who has it:** DeFi teams and tokenised-asset (RWA) issuers whose upgrade or admin rights sit on one EOA with no multisig or timelock. They pay in crypto natively, so USDT on Arbitrum works with no processor. Secondary buyers are LPs, curators and funds who need to know when a contract they depend on changes.

**Evidence from our own scan (all on-chain and checkable):**
- 480 protocol tokens (every DefiLlama protocol over $300k TVL on 15 EVM chains): 11 upgradeable by a single EOA, 48 with a single-EOA owner, 91 held by a multisig with no timelock, 28 behind a timelock. Data: `docs/data.json` and the site table.
- About 2,000 TVL-holding contracts (addresses taken from DefiLlama's open-source adapters), checked by hand afterwards: **at least 35 protocols and issuers** have a core or fund-holding contract whose upgrade path ends at one EOA. Examples: a ~$157M PYUSD wrapper, a ~$142M BTC vault, a perps bridge holding user deposits, and VNX's regulated stablecoins on 4 chains.

**Why this bet:** contrarian and in a niche (on-chain ops security, not AI tooling). It fits Sami's background (Xord since 2018, A51 DeFi). The payment rail (USDT) needs no approval.

## What I shipped

| What | URL | How to verify |
|---|---|---|
| Site with free in-browser checker, findings table, pricing and order form | https://swarm-t3.github.io/onekeyaway/ | Paste any contract (e.g. arbitrum `0x3d75f2bb8abcdbd1e27443cb5cbce8a668046c81`) and press Check |
| Sample paid deliverable (Permission Map, USDC on 3 chains) | https://swarm-t3.github.io/onekeyaway/sample-usdc.html | 17 roles, each with explorer links |
| Scanner source plus scan results | https://github.com/swarm-t3/onekeyaway | `scanner/scan.py <chain> <addr>`, `scanner/permmap.py` |
| Payment | USDT on Arbitrum One to `0x36c37d1b47737ba2b2a2cf1b5bc38509516b222f` | https://arbiscan.io/address/0x36c37d1b47737ba2b2a2cf1b5bc38509516b222f#tokentxns |
| Order and waitlist form | FormSubmit to megafi.app1+onekeyaway@gmail.com | Brand inbox |

Offers: Permission Map $99, Key Hardening Sprint $490, admin-change alerts $19/mo (waitlist).

## Results

_(Filled in at the end of the round.)_

## Assets left live

_(Filled in at the end of the round.)_

## Learnings

_(Filled in at the end of the round.)_
