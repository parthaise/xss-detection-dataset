import random
import pandas as pd

xss_payloads = [
    "<script>alert(1)</script>",
    "<img src=x onerror=alert(1)>",
    "<svg onload=alert(1)>",
    "<iframe src=javascript:alert(1)>",
    "<body onload=alert(1)>",
    "<input onfocus=alert(1) autofocus>",
    "<script>document.cookie</script>"
]

benign = [
    "GET /home HTTP/1.1",
    "POST /login HTTP/1.1",
    "GET /products?id=123 HTTP/1.1",
    "GET /search?q=books HTTP/1.1",
    "POST /checkout HTTP/1.1",
    "GET /about HTTP/1.1"
]

def encode(payload):
    return random.choice([
        payload,
        payload.replace("<", "&lt;").replace(">", "&gt;"),
        ''.join(['%' + hex(ord(c))[2:] if random.random() < 0.3 else c for c in payload])
    ])

data = []

# 4000 malicious
for _ in range(4000):
    data.append([encode(random.choice(xss_payloads)), 1])

# 4000 benign
for _ in range(4000):
    data.append([random.choice(benign), 0])

random.shuffle(data)

df = pd.DataFrame(data, columns=["payload", "label"])
df.to_csv("xss_dataset.csv", index=False)

print("DONE: 8000 dataset created")
