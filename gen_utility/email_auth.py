import dns.resolver
import smtplib
import socket


def verify_email(email):
    try:
        addressToVerify = email
        domain = addressToVerify.split("@")[1]
        records = dns.resolver.resolve(domain, "MX")
        mxRecord = str(records[0].exchange)
        server = smtplib.SMTP(timeout=10)
        server.connect(mxRecord)
        server.helo(socket.getfqdn())
        server.mail("test@domain.com")
        code, message = server.rcpt(email)
        server.quit()
        if code == 250:
            return True
        else:
            return False
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
