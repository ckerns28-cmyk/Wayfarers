#!/usr/bin/env node
import { spawn } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const projectRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const outDir = process.argv[2]
  ? path.resolve(process.argv[2])
  : path.join(projectRoot, "artifacts", "screenshots", "g418b");
const reviewUrl = process.argv[3] || "http://127.0.0.1:8765/index.html";
const chromePath = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
const debuggingPort = Number(process.env.G418B_CHROME_DEBUG_PORT || 9335);

fs.mkdirSync(outDir, { recursive: true });

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function fetchJson(url) {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`HTTP ${response.status} for ${url}`);
  }
  return response.json();
}

async function waitForTarget() {
  const deadline = Date.now() + 30000;
  while (Date.now() < deadline) {
    try {
      const targets = await fetchJson(`http://127.0.0.1:${debuggingPort}/json/list`);
      const page = targets.find((target) => target.type === "page" && target.webSocketDebuggerUrl);
      if (page) {
        return page;
      }
    } catch {
      await sleep(250);
    }
    await sleep(250);
  }
  throw new Error("Chrome DevTools target did not become available");
}

async function connectCdp(webSocketUrl) {
  const ws = new WebSocket(webSocketUrl);
  const pending = new Map();
  let nextId = 1;

  await new Promise((resolve, reject) => {
    ws.addEventListener("open", resolve, { once: true });
    ws.addEventListener("error", reject, { once: true });
  });

  ws.addEventListener("message", (event) => {
    const message = JSON.parse(event.data);
    if (message.id && pending.has(message.id)) {
      const { resolve, reject } = pending.get(message.id);
      pending.delete(message.id);
      if (message.error) {
        reject(new Error(`${message.error.message}: ${message.error.data || ""}`));
      } else {
        resolve(message.result || {});
      }
    }
  });

  return {
    send(method, params = {}) {
      const id = nextId++;
      ws.send(JSON.stringify({ id, method, params }));
      return new Promise((resolve, reject) => pending.set(id, { resolve, reject }));
    },
    close() {
      ws.close();
    },
  };
}

async function pressKey(cdp, key, windowsVirtualKeyCode) {
  const params = { key, code: key, windowsVirtualKeyCode, nativeVirtualKeyCode: windowsVirtualKeyCode };
  await cdp.send("Input.dispatchKeyEvent", { type: "keyDown", ...params });
  await cdp.send("Input.dispatchKeyEvent", { type: "keyUp", ...params });
}

async function screenshot(cdp, name, clip = null) {
  const params = { format: "png", captureBeyondViewport: false };
  if (clip) {
    params.clip = { ...clip, scale: 1 };
  }
  const result = await cdp.send("Page.captureScreenshot", params);
  fs.writeFileSync(path.join(outDir, name), Buffer.from(result.data, "base64"));
}

function copyProofImages() {
  const proofRoot = path.join(projectRoot, "art_pipeline", "newport_green_origin", "contact_sheets");
  for (const name of [
    "green_origin_asset_contact_sheet.png",
    "green_origin_palette_shadow_sheet.png",
    "green_origin_dock_before_after_comparison.png",
  ]) {
    fs.copyFileSync(path.join(proofRoot, name), path.join(outDir, name));
  }
}

const chrome = spawn(chromePath, [
  "--headless=new",
  "--disable-gpu",
  "--disable-crash-reporter",
  "--disable-extensions",
  "--enable-unsafe-swiftshader",
  "--no-first-run",
  "--window-size=1400,900",
  "--force-device-scale-factor=1",
  `--remote-debugging-port=${debuggingPort}`,
  `--user-data-dir=${path.join(projectRoot, "artifacts", "chrome-g418b-profile")}`,
  reviewUrl,
], { stdio: "ignore" });

let cdp;
try {
  const target = await waitForTarget();
  cdp = await connectCdp(target.webSocketDebuggerUrl);
  await cdp.send("Page.enable");
  await cdp.send("Runtime.enable");
  await cdp.send("Page.bringToFront");
  await sleep(10000);
  await cdp.send("Input.dispatchMouseEvent", { type: "mousePressed", x: 700, y: 450, button: "left", clickCount: 1 });
  await cdp.send("Input.dispatchMouseEvent", { type: "mouseReleased", x: 700, y: 450, button: "left", clickCount: 1 });
  await pressKey(cdp, "F4", 115);
  await sleep(1000);

  await screenshot(cdp, "no_hud_full_harbor_with_temporary_yellow_buildings.png");
  await screenshot(cdp, "no_hud_green_origin_dock_proof_closeup.png", { x: 700, y: 430, width: 650, height: 350 });
  await screenshot(cdp, "no_hud_working_wharf_context.png", { x: 135, y: 440, width: 1110, height: 405 });

  await pressKey(cdp, "F4", 115);
  await sleep(400);
  await pressKey(cdp, "F3", 114);
  await sleep(1000);
  await screenshot(cdp, "debug_overlay_provenance_proof.png");
  copyProofImages();
  console.log(`Wrote G-4.18B browser review screenshots to ${outDir}`);
} finally {
  if (cdp) {
    cdp.close();
  }
  chrome.kill();
}
