import vm from 'node:vm';

const targetUrl = process.argv[2];
if (!targetUrl) {
  console.error('Usage: node scripts/validate-served-bundle.mjs <url>');
  process.exit(1);
}

const response = await fetch(targetUrl, {
  headers: { 'user-agent': 'wayfarer-parse-gate' }
});

if (!response.ok) {
  console.error(`[served-bundle-check] fetch failed status=${response.status} url=${targetUrl}`);
  process.exit(2);
}

const html = await response.text();
const scripts = [...html.matchAll(/<script[^>]*>([\s\S]*?)<\/script>/gi)]
  .map((match) => match[1])
  .filter((body) => body && body.trim().length > 0);

if (scripts.length === 0) {
  console.error('[served-bundle-check] no inline scripts found');
  process.exit(3);
}

for (let idx = 0; idx < scripts.length; idx += 1) {
  try {
    new vm.Script(scripts[idx], { filename: `inline-script-${idx + 1}.js` });
  } catch (error) {
    console.error(`[served-bundle-check] parse failed scriptIndex=${idx + 1}`);
    console.error(error.stack || String(error));
    process.exit(4);
  }
}

console.log(`[served-bundle-check] PASS inlineScripts=${scripts.length} url=${targetUrl}`);
