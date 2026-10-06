import sys, json, time
sys.path.insert(0, '../tools'); from mail import send
from common import FOOT
M = [
("contact@bitfi.org", "bfBTC: UUPS owner is a single EOA on Ethereum and BNB Chain", """Hi BitFi team,

We run free on-chain checks of who controls DeFi contracts. bfBTC came up. These are facts read from chain today:

- bfBTC on Ethereum 0xcdfb58c8c859cb3f62ebe9cf2767f9e036c7fb15 and on BNB Chain 0x623f2774d9f27b59bc6b954544487532ce79d9df are UUPS proxies whose owner() is the same address, 0xd931401b37c3a368505e7ae6de700f2b0ad14ac6, an EOA.
  https://etherscan.io/address/0xd931401b37c3a368505e7ae6de700f2b0ad14ac6

So one signer can upgrade bfBTC on both chains (balances, mint and burn logic) in a single transaction, with no multisig or timelock in the path.
"""),
("contacts@tf.xyz", "TurboFlow bridge contract on BNB Chain: ProxyAdmin owned by a single EOA", """Hi TurboFlow team,

We run free on-chain checks of who controls DeFi contracts. TurboFlow came up. These are facts read from chain today:

- The bridge contract that holds user deposits on BNB Chain, 0x145cd0d5c3dd0ef1405dcf1b4d2bce7c611625db (it's labelled that way in DefiLlama's adapter), is a transparent proxy. Its ProxyAdmin 0xcd43379650cfe58ff73a1db0bdfa2863cd8afbcb is owned by 0xec5641314547eb9cac37620bbb39b97f6b2c5dfc, an EOA.
  https://bscscan.com/address/0xcd43379650cfe58ff73a1db0bdfa2863cd8afbcb

So one signer can replace the code of the deposit contract in a single transaction. We see that your treasury vaults use Fireblocks MPC. If this EOA is also an MPC key, that's a big mitigation, but there is still no timelock giving users notice of an upgrade.
"""),
]
if __name__ == "__main__":
    for to, subj, body in M:
        send(to, subj, body + FOOT)
        open("sent.jsonl", "a").write(json.dumps({"to": to, "subject": subj, "sent": time.strftime("%Y-%m-%dT%H:%MZ", time.gmtime())}) + "\n")
        time.sleep(15)
