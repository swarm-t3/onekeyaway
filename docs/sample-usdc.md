---
title: "Sample Permission Map: USDC"
---
# Permission Map: USDC (sample)

> This is a sample of the $99 OneKeyAway Permission Map, run on a public, well-known contract set. Circle is widely understood to keep these keys in HSMs with off-chain controls, so "single EOA" here means *no on-chain multisig or delay*, not "a hot wallet". For a newer protocol without Circle's off-chain controls, the same table is the attack surface. [Order one for your protocol](https://swarm-t3.github.io/onekeyaway/#pricing).


Generated 2026-10-06 16:59 UTC by OneKeyAway from on-chain reads. Every address links to an explorer.

**17 privileged roles across 3 contracts. 14 end at a single EOA.**

| Risk | Contract | Role | Held by | Signer setup |
|---|---|---|---|---|
| 🔴 single EOA | [USDC-Arbitrum](https://arbiscan.io/address/0xaf88d065e77c8cc2239327c5edb3a432268e5831) (arbitrum) | `upgrade (proxy admin)` | [0x2e0a6758…](https://arbiscan.io/address/0x2e0a67588cfbcad40f9e4dd76052436190a77a68) | EOA |
| 🔴 single EOA | [USDC-Arbitrum](https://arbiscan.io/address/0xaf88d065e77c8cc2239327c5edb3a432268e5831) (arbitrum) | `owner()` | [0xc7a59903…](https://arbiscan.io/address/0xc7a599037fda4ff8029df9a042af6053d061ebc9) | EOA |
| 🔴 single EOA | [USDC-Arbitrum](https://arbiscan.io/address/0xaf88d065e77c8cc2239327c5edb3a432268e5831) (arbitrum) | `admin()` | [0x2e0a6758…](https://arbiscan.io/address/0x2e0a67588cfbcad40f9e4dd76052436190a77a68) | EOA |
| 🔴 single EOA | [USDC-Arbitrum](https://arbiscan.io/address/0xaf88d065e77c8cc2239327c5edb3a432268e5831) (arbitrum) | `pauser()` | [0x36e3b4db…](https://arbiscan.io/address/0x36e3b4db327d9e66f5ae5a0200dcdbef0d2e240b) | EOA |
| 🔴 single EOA | [USDC-Arbitrum](https://arbiscan.io/address/0xaf88d065e77c8cc2239327c5edb3a432268e5831) (arbitrum) | `blacklister()` | [0xac5b4946…](https://arbiscan.io/address/0xac5b4946a8c29eafb42e1742b3ab82e6d5771329) | EOA |
| 🔴 single EOA | [USDC-Base](https://basescan.org/address/0x833589fcd6edb6e08f4c7c32d4f71b54bda02913) (base) | `upgrade (proxy admin)` | [0x4fc78503…](https://basescan.org/address/0x4fc7850364958d97b4d3f5a08f79db2493f8ca44) | EOA |
| 🔴 single EOA | [USDC-Base](https://basescan.org/address/0x833589fcd6edb6e08f4c7c32d4f71b54bda02913) (base) | `owner()` | [0x3abd6f64…](https://basescan.org/address/0x3abd6f64a422225e61e435bae41db12096106df7) | EOA |
| 🔴 single EOA | [USDC-Base](https://basescan.org/address/0x833589fcd6edb6e08f4c7c32d4f71b54bda02913) (base) | `admin()` | [0x4fc78503…](https://basescan.org/address/0x4fc7850364958d97b4d3f5a08f79db2493f8ca44) | EOA |
| 🔴 single EOA | [USDC-Base](https://basescan.org/address/0x833589fcd6edb6e08f4c7c32d4f71b54bda02913) (base) | `pauser()` | [0xd3571b3b…](https://basescan.org/address/0xd3571b3bc51cecff49194ad67afffc648d5e07b4) | EOA |
| 🔴 single EOA | [USDC-Base](https://basescan.org/address/0x833589fcd6edb6e08f4c7c32d4f71b54bda02913) (base) | `blacklister()` | [0x1f2e3a64…](https://basescan.org/address/0x1f2e3a640175d20ac31ed523b6733b977173e277) | EOA |
| 🔴 single EOA | [USDC-Ethereum](https://etherscan.io/address/0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48) (ethereum) | `upgrade (proxy admin)` | [0x807a9628…](https://etherscan.io/address/0x807a96288a1a408dbc13de2b1d087d10356395d2) | EOA |
| 🔴 single EOA | [USDC-Ethereum](https://etherscan.io/address/0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48) (ethereum) | `owner()` | [0xfcb19e6a…](https://etherscan.io/address/0xfcb19e6a322b27c06842a71e8c725399f049ae3a) | EOA |
| 🔴 single EOA | [USDC-Ethereum](https://etherscan.io/address/0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48) (ethereum) | `pauser()` | [0x4914f61d…](https://etherscan.io/address/0x4914f61d25e5c567143774b76edbf4d5109a8566) | EOA |
| 🔴 single EOA | [USDC-Ethereum](https://etherscan.io/address/0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48) (ethereum) | `blacklister()` | [0x0a06be16…](https://etherscan.io/address/0x0a06be16275b95a7d2567fbdae118b36c7da78f9) | EOA |
| ⚪ contract (review) | [USDC-Arbitrum](https://arbiscan.io/address/0xaf88d065e77c8cc2239327c5edb3a432268e5831) (arbitrum) | `masterMinter()` | [0x8aff09e2…](https://arbiscan.io/address/0x8aff09e2259cacbf4fc4e3e53f3bf799efeeab36) | Contract (unknown) |
| ⚪ contract (review) | [USDC-Base](https://basescan.org/address/0x833589fcd6edb6e08f4c7c32d4f71b54bda02913) (base) | `masterMinter()` | [0x2230393e…](https://basescan.org/address/0x2230393edad0299b7e7b59f20aa856cd1bed52e1) | Contract (unknown) |
| ⚪ contract (review) | [USDC-Ethereum](https://etherscan.io/address/0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48) (ethereum) | `masterMinter()` | [0xe982615d…](https://etherscan.io/address/0xe982615d461dd5cd06575bbea87624fda4e3de17) | Contract (unknown) |

## What to fix first
1. Move every upgrade right and every role that can move or mint funds off single EOAs, onto a Safe with at least 3 signers on separate devices.
2. Put upgrades and parameter changes behind a TimelockController (24-72h), and keep a separate fast guardian that can only pause.
3. Give pause/guardian roles to a different multisig than upgrades, so one compromised set can't both act and hide.
4. Set up alerts on Upgraded, AdminChanged, OwnershipTransferred and RoleGranted events.

_Limits: this reads common getters, EIP-1967/legacy proxy slots and enumerable AccessControl. Non-enumerable roles and custom auth need the manual review that is part of the Key Hardening Sprint. An EOA may be MPC- or HSM-backed off-chain, which cannot be checked on-chain._
