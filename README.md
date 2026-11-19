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
> 如本仓库原有描述与上方冲突，一律以主项目生产端点为准。

---

# x402-paywall — AutoTasker Hub 镜像

本仓库是主项目 x402 收款端点的**精简镜像**，已从测试网零地址占位符模板改造为对齐生产配置。

## 当前配置（可核实）

- 收款地址：金库 `0xb9A9E6d9C4Ad1635aA685bba2e235A515A94773C`（主项目唯一收款地址）
- 网络：`eip155:8453`（Base 主网，非测试网）
- 资产：USDC `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`
- Facilitator：`https://facilitator.payai.network`
- 默认价格：`$0.05`/次（对齐主项目 hotlist）

## 文件

- `api/index.py` — Flask 收款端点（Vercel serverless）
- `lib/x402-core.js` — Node.js 自包含核心收款处理器（移植自主项目 `lib/x402-standalone.js`，已修正金库与 facilitator）
- `config/treasury-policy.json` — 主项目资金策略副本
- `.well-known/x402.json` — x402 发现清单

## 数据来源（重要）

付款验证成功后，本端点从主项目**公开免费端点** `/api/x402/sample` 实时拉取真实样本数据，并附完整付费数据端点链接。**不再返回任何 demo/假数据**。

## 生效说明

修改 GitHub 仓库不会自动更新已部署的 Vercel 实例；需重新部署（`vercel --prod`）后生产 URL 才使用上述配置。

## 诚实声明

所有配置与数字均可通过生产 proof 端点核实；本仓库不是独立盈利主体，收入统一进入主项目金库。
