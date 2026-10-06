"""Brand inbox helper. Reads creds from ~/.config/swarm/secrets.env; never prints them."""
import imaplib, smtplib, email, os, sys, ssl
from email.message import EmailMessage
from email.header import decode_header, make_header
env = {}
for l in open(os.path.expanduser("~/.config/swarm/secrets.env")):
    if "=" in l and not l.startswith("#"):
        k, v = l.strip().split("=", 1); env[k] = v.strip().strip('"').strip("'")
USER = env["BRAND_GMAIL_ADDRESS"]; PW = env["BRAND_GMAIL_APP_PASSWORD"].replace(" ", "")
ALIAS = USER.replace("@", "+onekeyaway@")

def search(q='X-GM-RAW "onekeyaway"', n=20, body=False):
    m = imaplib.IMAP4_SSL("imap.gmail.com", 993); m.login(USER, PW); m.select('"[Gmail]/All Mail"', readonly=True)
    typ, d = m.search(None, q) if not q.startswith("X-GM-RAW") else m.search(None, "X-GM-RAW", q.split(" ", 1)[1])
    ids = d[0].split()[-n:]
    for i in ids:
        typ, md = m.fetch(i, "(RFC822)"); msg = email.message_from_bytes(md[0][1])
        print("---", msg["Date"], "|", msg["From"], "->", msg["To"], "|", str(make_header(decode_header(msg["Subject"] or ""))))
        if body:
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    print(part.get_payload(decode=True).decode("utf8", "ignore")[:3000]); break
            else:
                for part in msg.walk():
                    if part.get_content_type() == "text/html":
                        print(part.get_payload(decode=True).decode("utf8", "ignore")[:4000]); break
    m.logout()

def send(to, subject, text, reply_to=None):
    msg = EmailMessage(); msg["From"] = f"OneKeyAway <{ALIAS}>"; msg["To"] = to; msg["Subject"] = subject
    msg["Reply-To"] = reply_to or ALIAS; msg.set_content(text)
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl.create_default_context()) as s:
        s.login(USER, PW); s.send_message(msg)
    print("sent", to)

if __name__ == "__main__":
    if sys.argv[1] == "search": search(sys.argv[2] if len(sys.argv) > 2 else 'X-GM-RAW "onekeyaway"', body="--body" in sys.argv)
