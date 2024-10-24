import dns.resolver
import threading
import time

TARGET = "facebook.com"
THREADS = 50

with open("nameservers_50k.txt", "r") as file:
    nameservers = file.read().splitlines()
    file.close()

def dns_resolve(qname: str, nameserver: str):
    resolver = dns.resolver.Resolver()
    resolver.timeout = 1
    resolver.nameservers = [nameserver]

    try:
        answer = resolver.resolve(qname=qname, rdtype="A")
    except Exception as e:
        return

    print(f"{nameserver}{' ' * int(16 - len(nameserver))}: {answer.response.answer}")

def main():
    for nameserver in nameservers:
        while True:
            if threading.active_count() > THREADS:
                time.sleep(0.05)
                continue
            break

        threading.Thread(target=dns_resolve, args=[TARGET, nameserver]).start()

    while True:
        time.sleep(0.05)
        if threading.active_count() <= 1:
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit()
