SITE = "https://swarm-t3.github.io/onekeyaway/"
FOOT = f"""
Why we flag this: in 2026, leaked keys and admin access overtook contract bugs as the biggest cause of DeFi losses (>$1.3B Jan-Aug). Wasabi lost ~$4.5M in April through one deployer EOA that could upgrade its contracts. The usual fix is to move the admin role to a Safe (for example 3-of-5 on separate devices) behind a TimelockController, so any upgrade is visible on-chain for 24-48h before it runs.

If the EOA is MPC- or HSM-backed, that lowers the risk but still leaves no timelock. Feel free to ignore this if you already have it covered.

You can check any contract yourself, free, in the browser: {SITE}
If you'd like us to map the rest of your contracts (every role traced to its signers), just reply.

OneKeyAway (on-chain admin-key checks)
This is a one-off note, not a list. Reply "no" and we won't write again."""
