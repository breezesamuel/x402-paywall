> ## 🔗 已整合入 AutoTasker Hub（主项目）
>
> 本仓库现作为主项目 **AutoTasker Hub** 的发现/接入入口维护，原有内容保留作历史参考。
>
> | 项 | 当前生产事实（均可公开核实） |
> |---|---|
> | 生产服务 | https://autotasker.highkingflower.com — streamable-HTTP MCP，84 工具，无账号；免费发现 + `/api/x402/sample` |
> | 收款协议 | x402 v2 · Base 主网 `eip155:8453` · USDC `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` |
> | 唯一金库 | `0xb9A9E6d9C4Ad1635aA685bba2e235A515A94773C`（私钥外部持有） |
> | 真实结算凭证 | https://autotasker.highkingflower.com/api/x402/proof — 2 笔 / $0.10，可在 BaseScan 按 payTo 核对 |
> | 主项目源码 | https://github.com/breezesamuel/autotasker-hub-aevum |
>
> 如本仓库原有描述与上方冲突，一律以主项目生产端点为准。本 banner 不含任何未核实或历史数字。

---

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