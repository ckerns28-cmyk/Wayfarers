#!/usr/bin/env node
import { spawn } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const projectRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const outDir = process.argv[2]
  ? path.resolve(process.argv[2])
  : path.join(projectRoot, "artifacts", "screenshots", "g418d3");
const reviewUrl = process.argv[3] || "http://127.0.0.1:8765/index.html";
const chromePath = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
const debuggingPort = Number(process.env.G418D3_CHROME_DEBUG_PORT || 9339);
const chromeProfile = path.join(projectRoot, "artifacts", `chrome-g418d3-profile-${Date.now()}`);

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
  let closed = false;

  await new Promise((resolve, reject) => {
    ws.addEventListener("open", resolve, { once: true });
    ws.addEventListener("error", reject, { once: true });
  });

  async function readMessageData(data) {
    if (typeof data === "string") {
      return data;
    }
    if (data instanceof ArrayBuffer) {
      return Buffer.from(data).toString("utf8");
    }
    if (ArrayBuffer.isView(data)) {
      return Buffer.from(data.buffer, data.byteOffset, data.byteLength).toString("utf8");
    }
    if (data && typeof data.text === "function") {
      return data.text();
    }
    return String(data);
  }

  function rejectAll(error) {
    for (const { reject, timeout } of pending.values()) {
      clearTimeout(timeout);
      reject(error);
    }
    pending.clear();
  }

  ws.addEventListener("message", async (event) => {
    const message = JSON.parse(await readMessageData(event.data));
    if (message.id && pending.has(message.id)) {
      const { resolve, reject, timeout } = pending.get(message.id);
      clearTimeout(timeout);
      pending.delete(message.id);
      if (message.error) {
        reject(new Error(`${message.error.message}: ${message.error.data || ""}`));
      } else {
        resolve(message.result || {});
      }
    }
  });
  ws.addEventListener("close", () => {
    closed = true;
    rejectAll(new Error("Chrome DevTools WebSocket closed"));
  });
  ws.addEventListener("error", () => {
    rejectAll(new Error("Chrome DevTools WebSocket error"));
  });

  return {
    send(method, params = {}) {
      if (closed) {
        return Promise.reject(new Error(`Chrome DevTools WebSocket is closed before ${method}`));
      }
      const id = nextId++;
      ws.send(JSON.stringify({ id, method, params }));
      return new Promise((resolve, reject) => {
        const timeout = setTimeout(() => {
          pending.delete(id);
          reject(new Error(`Timed out waiting for CDP response to ${method}`));
        }, 15000);
        pending.set(id, { resolve, reject, timeout });
      });
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

function copyAtelierImages() {
  const proofRoot = path.join(projectRoot, "art_pipeline", "newport_green_origin", "contact_sheets");
  for (const [source, dest] of [
    ["g418d3_isolated_sprite_1x.png", "isolated_sprite_1x.png"],
    ["g418d3_enlarged_grid_8x.png", "enlarged_grid_8x.png"],
    ["g418d3_before_after_pixel_atelier.png", "before_after_pixel_atelier.png"],
    ["g418d3_palette_sheet.png", "palette_sheet.png"],
    ["g418d3_lab_in_world_comparison.png", "lab_in_world_comparison.png"],
    ["g418d3_standard_comparison_chandlery_wharf.png", "standard_comparison_chandlery_wharf.png"],
    ["g418d3_prop_readability_studies.png", "prop_readability_studies.png"],
    ["g418d3_pixel_sprite_atelier_board.png", "pixel_sprite_atelier_board.png"],
  ]) {
    fs.copyFileSync(path.join(proofRoot, source), path.join(outDir, dest));
  }
}

const chrome = spawn(chromePath, [
  "--headless=new",
  "--disable-crash-reporter",
  "--disable-extensions",
  "--enable-unsafe-swiftshader",
  "--use-angle=swiftshader",
  "--use-gl=angle",
  "--no-first-run",
  "--window-size=1400,900",
  "--force-device-scale-factor=1",
  `--remote-debugging-port=${debuggingPort}`,
  `--user-data-dir=${chromeProfile}`,
  "about:blank",
], { stdio: "ignore" });

let cdp;
try {
  const target = await waitForTarget();
  cdp = await connectCdp(target.webSocketDebuggerUrl);
  await cdp.send("Page.enable");
  await cdp.send("Runtime.enable");
  await cdp.send("Page.bringToFront");
  await cdp.send("Page.navigate", { url: reviewUrl });
  await sleep(12000);
  await cdp.send("Input.dispatchMouseEvent", { type: "mousePressed", x: 700, y: 450, button: "left", clickCount: 1 });
  await cdp.send("Input.dispatchMouseEvent", { type: "mouseReleased", x: 700, y: 450, button: "left", clickCount: 1 });
  await sleep(500);

  await screenshot(cdp, "normal_review_full_harbor.png");
  await screenshot(cdp, "normal_review_dock_without_pixel_art.png", { x: 760, y: 420, width: 560, height: 360 });

  await pressKey(cdp, "F4", 115);
  await sleep(800);
  await screenshot(cdp, "normal_review_no_hud_full_harbor.png");

  await pressKey(cdp, "F4", 115);
  await sleep(500);
  await pressKey(cdp, "F6", 117);
  await sleep(900);
  await screenshot(cdp, "green_origin_lab_pixel_atelier_full.png");
  await screenshot(cdp, "pixel_atelier_board_hud.png", { x: 260, y: 0, width: 1120, height: 500 });
  await screenshot(cdp, "lab_in_world_pixel_atelier_closeup.png", { x: 840, y: 300, width: 560, height: 520 });
  await pressKey(cdp, "F4", 115);
  await sleep(500);
  await screenshot(cdp, "lab_in_world_pixel_atelier_no_hud_closeup.png", { x: 840, y: 300, width: 560, height: 520 });

  copyAtelierImages();
  fs.writeFileSync(
    path.join(outDir, "g418d3_pixel_sprite_atelier_review_notes.txt"),
    [
      "G-4.18D.3 screenshot review packet",
      "",
      "normal_review_full_harbor.png proves the player-facing baseline remains clean except for G-4.18D.3 build metadata.",
      "normal_review_no_hud_full_harbor.png proves F4 no-HUD mode still works.",
      "normal_review_dock_without_pixel_art.png proves the D3 pixel sprite is not drawn in default review.",
      "green_origin_lab_pixel_atelier_full.png proves the pixel atelier board appears only in Green-Origin Lab mode.",
      "pixel_atelier_board_hud.png shows the DEFER verdict, 7.1/10 rating, and lab-only status.",
      "isolated_sprite_1x.png, enlarged_grid_8x.png, before_after_pixel_atelier.png, palette_sheet.png, prop_readability_studies.png, and standard_comparison_chandlery_wharf.png show the required art review artifacts.",
      "lab_in_world_pixel_atelier_closeup.png shows the deferred D3 sprite beside the current Newport row at actual scale.",
      "lab_in_world_pixel_atelier_no_hud_closeup.png repeats that comparison with HUD/lab board hidden.",
    ].join("\n"),
    "utf8",
  );
  console.log(`Wrote G-4.18D.3 browser review screenshots to ${outDir}`);
} finally {
  if (cdp) {
    cdp.close();
  }
  chrome.kill();
}
