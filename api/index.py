import os, json, base64, urllib.request
from flask import Flask, request, jsonify
from x402 import x402ResourceServer, ResourceConfig
from x402.http import HTTPFacilitatorClient
from x402.mechanisms.evm.exact import ExactEvmServerScheme

app = Flask(__name__)

# Aligned with main project autotasker-hub-aevum production config.
PAY_TO = os.getenv("PAY_TO", "0xb9A9E6d9C4Ad1635aA685bba2e235A515A94773C")
NETWORK = os.getenv("X402_NETWORK", "eip155:8453")
USDC = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
FACILITATOR_URL = os.getenv("FACILITATOR_URL", "https://facilitator.payai.network")
PRICE = os.getenv("PRICE", "0.05 USD")
UPSTREAM = "https://autotasker.highkingflower.com"

facilitator = HTTPFacilitatorClient({"url": FACILITATOR_URL})
server = x402ResourceServer(facilitator)
server.register(NETWORK, ExactEvmServerScheme())
server.initialize()
config = ResourceConfig(scheme="exact", network=NETWORK, pay_to=PAY_TO, price=PRICE)


def upstream_sample(limit=5):
    """Fetch REAL public sample data from the main project free endpoint. No demo/fake data."""
    try:
        url = UPSTREAM + "/api/x402/sample?limit=" + str(limit)
        with urllib.request.urlopen(url, timeout=8) as r:
            return json.loads(r.read().decode("utf-8"))
    except Exception as exc:
        return {"error": "upstream unavailable", "detail": str(exc)[:120]}


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "service": "AutoTasker Hub paywall mirror",
        "upstream": UPSTREAM,
        "payTo": PAY_TO, "network": NETWORK, "asset": USDC,
        "facilitator": FACILITATOR_URL,
        "endpoints": ["/pay/<tool>", "/health"],
        "note": "Discovery mirror of the main project; real paid data is served by upstream.",
    })


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"ok": True, "payTo": PAY_TO, "network": NETWORK, "facilitator": FACILITATOR_URL})


@app.route("/pay/<tool>", methods=["GET"])
def pay(tool):
    proof = request.headers.get("x402-payment", "") or request.headers.get("PAYMENT-SIGNATURE", "")
    if not proof:
        payreq = {
            "x402Version": 2,
            "error": "PAYMENT-SIGNATURE header is required",
            "facilitator": FACILITATOR_URL,
            "resource": {"url": request.url, "description": tool + " query", "mimeType": "application/json"},
            "accepts": [{
                "scheme": "exact", "network": NETWORK, "asset": USDC,
                "payTo": PAY_TO, "amount": "50000", "maxTimeoutSeconds": 60,
                "facilitator": FACILITATOR_URL,
            }],
        }
        b = base64.b64encode(json.dumps(payreq).encode()).decode()
        return jsonify({"paymentRequired": payreq}), 402, {
            "Content-Type": "application/json; charset=utf-8",
            "PAYMENT-REQUIRED": b, "X-PAYMENT-REQUIRED": b,
            "Access-Control-Expose-Headers": "PAYMENT-REQUIRED,PAYMENT-RESPONSE,X-PAYMENT,X-PAYMENT-RESPONSE",
        }
    try:
        from x402.schemas import PaymentPayload
        payload = PaymentPayload.model_validate_json(proof)
        reqs = server.build_payment_requirements(config)
        resp = server.verify_payment(payload, reqs[0])
        ok = bool(getattr(resp, "valid", resp))
    except Exception as exc:
        return jsonify({"error": "verify failed: " + repr(exc)}), 400
    if not ok:
        return jsonify({"error": "Payment not valid"}), 402
    sample = upstream_sample()
    return jsonify({
        "tool": tool,
        "source": "autotasker.highkingflower.com (live public sample)",
        "sample": sample,
        "fullPaidData": UPSTREAM + "/api/x402/" + tool,
        "settlementProof": UPSTREAM + "/api/x402/proof",
        "payTo": PAY_TO, "network": NETWORK,
    })


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8765)
