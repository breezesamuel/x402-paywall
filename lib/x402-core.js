/**
 * x402 core — aligned mirror of AutoTasker Hub main project core.
 * Self-contained Node handler (no parent-project dependency).
 * Ported from breezesamuel/autotasker-hub-aevum lib/x402-standalone.js;
 * treasury + facilitator corrected to current production values.
 * No private key is held here.
 */
const CFG = {
  network: 'eip155:8453',
  asset: '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913',
  payTo: '0xb9A9E6d9C4Ad1635aA685bba2e235A515A94773C',
  facilitator: 'https://facilitator.payai.network',
  prices: { hotlist: 0.05, search: 0.05, price: 0.10, full: 0.50, daily_report: 0.25 },
};
const ATOMIC = { hotlist: 50000, search: 50000, price: 100000, full: 500000, daily_report: 250000 };
function b64(o) { return Buffer.from(JSON.stringify(o)).toString('base64'); }
async function handleX402(req, res) {
  const url = new URL(req.url, 'http://' + req.headers.host);
  const p = url.pathname;
  if (p === '/health') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    return res.end(JSON.stringify({ ok: true, network: CFG.network, payTo: CFG.payTo, facilitator: CFG.facilitator }));
  }
  if (p === '/api/x402/pricing') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    return res.end(JSON.stringify({ protocol: 'x402', version: 2, network: CFG.network, prices: CFG.prices, facilitator: CFG.facilitator, payTo: CFG.payTo }));
  }
  const m = p.match(/^\/api\/x402\/(\w+)/);
  if (!m) { res.writeHead(404); return res.end('not found'); }
  const tool = m[1];
  const payReq = {
    x402Version: 2,
    error: 'PAYMENT-SIGNATURE header is required',
    facilitator: CFG.facilitator,
    resource: { url: req.headers.host + p, description: tool + ' query', mimeType: 'application/json' },
    accepts: [{
      scheme: 'exact', network: CFG.network, amount: String(ATOMIC[tool] || 50000),
      asset: CFG.asset, payTo: CFG.payTo, maxTimeoutSeconds: 60,
      facilitator: CFG.facilitator, extra: { name: 'USD Coin', version: '2' },
    }],
  };
  const b = b64(payReq);
  res.writeHead(402, {
    'Content-Type': 'application/json; charset=utf-8',
    'PAYMENT-REQUIRED': b, 'X-PAYMENT-REQUIRED': b,
    'Access-Control-Expose-Headers': 'PAYMENT-REQUIRED,PAYMENT-RESPONSE,X-PAYMENT,X-PAYMENT-RESPONSE',
  });
  return res.end(JSON.stringify({ paymentRequired: payReq }));
}
module.exports = { default: handleX402, CFG };
