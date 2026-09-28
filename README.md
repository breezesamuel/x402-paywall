# x402-paywall

**Pay-per-call API monetized via x402 (HTTP 402 Payment Required, USDC).**

Any tool/skill becomes a paid API endpoint in under 50 lines. No API keys, no subscriptions — agent pays stablecoin per call.

## Live

```
GET https://x402-paywall-bgl2ek1ck-solmount.vercel.app/pay/today
-> HTTP/1.1 402 Payment Required
-> {"requirements":[{scheme,network:"eip155:84532",asset,amount,pay_to}]}
```

## How it works

1. Client requests a paid tool → server responds `402` + payment requirements (per x402 spec).
2. Client pays via x402 facilitator (EIP-3009 `transferWithAuthorization`).
3. Client retries with the payment header → server verifies on-chain → returns real output.

## Stack

- Python `x402` SDK (`x402ResourceServer` + `ExactEvmServerScheme`)
- Flask, deployed as Vercel serverless function
- USDC on Base-Sepolia (testnet proof); mainnet switchable via env

## Files

- `api/index.py` — the paywall endpoint
- `requirements.txt` — deps
- `vercel.json` — serverless config

## Roadmap

- [x] Testnet 402 flow live
- [ ] Base mainnet with real USDC
- [ ] MCP wrapper for agent discovery

_Retrieval: impact micro-grant candidate (up to $3k) per x402 foundation's PROJECT-IDEAS._