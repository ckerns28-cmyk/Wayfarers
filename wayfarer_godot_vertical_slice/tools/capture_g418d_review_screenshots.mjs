#!/usr/bin/env node
import { spawn } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const projectRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const outDir = process.argv[2]
  ? path.resolve(process.argv[2])
  : path.join(projectRoot, "artifacts", "screenshots", "g418d1");
const reviewUrl = process.argv[3] || "http://127.0.0.1:8765/index.html";
const chromePath = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
const debuggingPort = Number(process.env.G418D1_CHROME_DEBUG_PORT || 9337);
const chromeProfile = path.join(projectRoot, "artifacts", `chrome-g418d1-profile-${Date.now()}`);

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

function copyBakeoffImages() {
  const proofRoot = path.join(projectRoot, "art_pipeline", "newport_green_origin", "contact_sheets");
  for (const name of [
    "g418d1_corrected_bakeoff_board.png",
    "g418d1_candidate_comparison_strip.png",
    "g418d1_m01b_isolated_proof.png",
    "g418d1_m01b_in_world_comparison_frame.png",
  ]) {
    fs.copyFileSync(path.join(proofRoot, name), path.join(outDir, name));
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
  await screenshot(cdp, "normal_review_dock_without_bakeoff_art.png", { x: 700, y: 430, width: 650, height: 350 });

  await pressKey(cdp, "F4", 115);
  await sleep(800);
  await screenshot(cdp, "normal_review_no_hud_full_harbor.png");

  await pressKey(cdp, "F4", 115);
  await sleep(500);
  await pressKey(cdp, "F6", 117);
  await sleep(900);
  await screenshot(cdp, "green_origin_lab_corrected_verdicts_full.png");
  await screenshot(cdp, "corrected_bakeoff_board.png", { x: 260, y: 0, width: 1120, height: 500 });
  await screenshot(cdp, "m01b_lab_in_world_comparison_closeup.png", { x: 500, y: 380, width: 860, height: 460 });

  copyBakeoffImages();
  fs.writeFileSync(
    path.join(outDir, "g418d1_bakeoff_review_notes.txt"),
    [
      "G-4.18D.1 screenshot review packet",
      "",
      "normal_review_full_harbor.png proves the player-facing baseline remains clean except for G-4.18D.1 build metadata.",
      "normal_review_no_hud_full_harbor.png proves F4 no-HUD mode still works.",
      "green_origin_lab_corrected_verdicts_full.png proves the corrected bakeoff appears only in Green-Origin Lab mode.",
      "corrected_bakeoff_board.png shows M01 no longer PASS and no candidate below 8.5 promoted.",
      "m01b_lab_in_world_comparison_closeup.png shows M01B evaluated in-world beside current Newport wharf art at actual scale.",
      "normal_review_dock_without_bakeoff_art.png proves experimental bakeoff art is not drawn in the default harbor.",
    ].join("\n"),
    "utf8",
  );
  console.log(`Wrote G-4.18D.1 browser review screenshots to ${outDir}`);
} finally {
  if (cdp) {
    cdp.close();
  }
  chrome.kill();
}
