export class WorldRoom {
  constructor(state, env) {
    this.state = state;
    this.env = env;
  }

  async fetch(request) {
    return new Response("WorldRoom active");
  }
}

export default {
  async fetch(request) {
    return new Response(html, {
      headers: {
        "content-type": "text/html; charset=UTF-8",
        "cache-control": "no-store",
      },
    });
  },
};

const html = String.raw`<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Wayfarer — Polished Town Slice</title>
  <style>
    :root {
      --bg: #071018;
      --panel: rgba(10, 15, 23, 0.95);
      --panel-border: rgba(255,255,255,0.08);
      --text: #e8edf5;
      --muted: #a9b3c2;
      --accent: #a6c8ff;
      --gold: #e0c26d;
    }

    * { box-sizing: border-box; }

    body {
      margin: 0;
      background: radial-gradient(circle at top, #0d1824 0%, #071018 58%);
      color: var(--text);
      font-family: Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      overflow: hidden;
    }

    #wrap {
      display: grid;
      grid-template-columns: 320px 1fr;
      height: 100vh;
      gap: 16px;
      padding: 16px;
    }

    .panel {
      background: var(--panel);
      border: 1px solid var(--panel-border);
      border-radius: 22px;
      box-shadow: 0 14px 50px rgba(0,0,0,0.35);
      backdrop-filter: blur(8px);
    }

    #sidebar {
      display: flex;
      flex-direction: column;
      gap: 16px;
      min-width: 0;
    }

    #brand, #stats, #objective, #logPanel {
      padding: 18px;
    }

    h1 {
      margin: 0 0 8px;
      font-size: 26px;
      line-height: 1.05;
    }

    .sub {
      color: var(--muted);
      font-size: 14px;
      margin-bottom: 10px;
    }

    .tag {
      display: inline-block;
      padding: 7px 11px;
      border-radius: 999px;
      background: rgba(255,255,255,0.06);
      color: var(--muted);
      font-size: 12px;
    }

    .stats {
      display: grid;
      grid-template-columns: 1fr auto;
      gap: 10px 12px;
      align-items: center;
      font-size: 15px;
    }

    .muted { color: var(--muted); }

    #chat {
      background: rgba(0,0,0,0.26);
      border-radius: 16px;
      padding: 14px;
      min-height: 180px;
      max-height: 280px;
      overflow: auto;
      white-space: pre-line;
      font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
      font-size: 13px;
      line-height: 1.42;
    }

    #gamePanel {
      position: relative;
      overflow: hidden;
      padding: 0;
    }

    #game {
      width: 100%;
      height: 100%;
      display: block;
      border-radius: 22px;
      image-rendering: pixelated;
      background: #08131d;
    }

    #hud {
      position: absolute;
      top: 16px;
      left: 16px;
      background: rgba(0,0,0,0.34);
      border: 1px solid rgba(255,255,255,0.08);
      border-radius: 14px;
      padding: 10px 12px;
      font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
      font-size: 13px;
      line-height: 1.45;
      pointer-events: none;
      white-space: pre-line;
    }

    #dialogue {
      position: absolute;
      left: 24px;
      right: 24px;
      bottom: 24px;
      background: rgba(9, 11, 17, 0.97);
      border: 1px solid rgba(255,255,255,0.12);
      border-radius: 18px;
      padding: 16px;
      display: none;
      box-shadow: 0 16px 44px rgba(0,0,0,0.42);
    }

    #dialogueName {
      font-weight: 700;
      color: var(--accent);
      margin-bottom: 8px;
    }

    #dialogueText {
      white-space: pre-line;
      line-height: 1.48;
      min-height: 72px;
    }

    #dialogueHint {
      margin-top: 10px;
      color: var(--muted);
      font-size: 13px;
    }

    .questTitle {
      color: var(--gold);
      font-weight: 700;
      margin-bottom: 8px;
    }
  </style>
</head>
<body>
  <div id="wrap">
    <aside id="sidebar">
      <section id="brand" class="panel">
        <h1>Wayfarer</h1>
        <div class="sub">Visual Polish Pass — Hearthvale Slice</div>
        <span class="tag">Moody mythic quality rebuild</span>
      </section>

      <section id="stats" class="panel">
        <div class="stats">
          <div class="muted">HP</div><div id="hpVal">50/50</div>
          <div class="muted">XP</div><div id="xpVal">0</div>
          <div class="muted">Coins</div><div id="coinsVal">0</div>
          <div class="muted">Weapon</div><div>Rusty Sword (+2)</div>
          <div class="muted">Quest</div><div id="questVal">Town Slice</div>
          <div class="muted">Zone</div><div id="zoneVal">Hearthvale Square</div>
        </div>
      </section>

      <section id="objective" class="panel">
        <div class="questTitle">Current Objective</div>
        <div id="objectiveText" class="muted">Walk Hearthvale, visit Mirror Pond, and speak to Edrin Vale.</div>
      </section>

      <section id="logPanel" class="panel">
        <div class="questTitle">Log</div>
        <div id="chat"></div>
      </section>
    </aside>

    <main id="gamePanel" class="panel">
      <canvas id="game"></canvas>
      <div id="hud"></div>

      <div id="dialogue">
        <div id="dialogueName"></div>
        <div id="dialogueText"></div>
        <div id="dialogueHint">Click this dialogue box to continue.</div>
      </div>
    </main>
  </div>

  <script>
    const canvas = document.getElementById("game");
    const ctx = canvas.getContext("2d");

    const hud = document.getElementById("hud");
    const chat = document.getElementById("chat");
    const hpVal = document.getElementById("hpVal");
    const xpVal = document.getElementById("xpVal");
    const coinsVal = document.getElementById("coinsVal");
    const zoneVal = document.getElementById("zoneVal");
    const questVal = document.getElementById("questVal");
    const objectiveText = document.getElementById("objectiveText");

    const dialogue = document.getElementById("dialogue");
    const dialogueName = document.getElementById("dialogueName");
    const dialogueText = document.getElementById("dialogueText");

    const TILE = 32;
    const WORLD_W = 38;
    const WORLD_H = 24;
    const VIEW_TILES_X = 22;
    const VIEW_TILES_Y = 14;

    function resize() {
      const rect = document.getElementById("gamePanel").getBoundingClientRect();
      canvas.width = Math.floor(rect.width);
      canvas.height = Math.floor(rect.height);
    }
    resize();
    addEventListener("resize", resize);

    function log(message) {
      chat.textContent = message + "\\n" + chat.textContent;
    }

    const assets = {
      grassA: new Image(),
      grassB: new Image(),
      grassC: new Image(),
      road: new Image(),
      treeA: new Image(),
      treeB: new Image(),
      treeC: new Image(),
      waterDeep: new Image(),
      waterShallow: new Image()
    };

    assets.grassA.src = "./assets/terrain/grass/moss_grass_32.png";
    assets.grassB.src = "./assets/terrain/grass/shadow_grass_32.png";
    assets.grassC.src = "./assets/terrain/grass/moss_grass_32.png";
    assets.road.src = "./assets/terrain/roads/worn_path_32.png";
    assets.treeA.src = "./assets/terrain/trees/pine_mythic_32.png";
    assets.treeB.src = "./assets/terrain/trees/oak_mythic_32.png";
    assets.treeC.src = "./assets/terrain/trees/pine_bright_32.png";
    assets.waterDeep.src = "./assets/terrain/water/deep_water_32.png";
    assets.waterShallow.src = "./assets/terrain/water/shallow_water_32.png";

    function keyOf(x, y) {
      return x + "," + y;
    }

    const world = {
      blocked: new Set(),
      trees: [],
      fences: [],
      buildings: [],
      roads: [],
      zones: [],
      pondBlocked: new Set(),
      pondWater: new Set(),
      pondShore: new Set(),
      pondNearEdge: new Set()
    };

    function blockRect(x, y, w, h) {
      for (let ix = x; ix < x + w; ix++) {
        for (let iy = y; iy < y + h; iy++) {
          world.blocked.add(keyOf(ix, iy));
        }
      }
    }

    // ---------- Layout ----------
    // central roads
    world.roads.push(
      { x: 6, y: 11, w: 26, h: 2 },
      { x: 17, y: 5, w: 2, h: 15 },
      { x: 10, y: 8, w: 2, h: 8 },
      { x: 24, y: 7, w: 2, h: 8 },
      { x: 19, y: 12, w: 5, h: 2 },
      { x: 26, y: 12, w: 3, h: 2 }
    );

    // buildings
    world.buildings.push(
      { x: 11, y: 6, w: 4, h: 3, roofTop: "#745048", roofSide: "#5b3c35", wall: "#807862", doorX: 13, doorY: 9 },
      { x: 20, y: 6, w: 4, h: 3, roofTop: "#56617f", roofSide: "#434b66", wall: "#847c68", doorX: 22, doorY: 9 },
      { x: 12, y: 14, w: 4, h: 3, roofTop: "#6e6248", roofSide: "#54493a", wall: "#7e7460", doorX: 14, doorY: 13 }
    );
    world.buildings.forEach(b => blockRect(b.x, b.y, b.w, b.h));

    // pond
    const pond = {
      x: 22,
      y: 13,
      w: 7,
      h: 5,
      cx: 25.5,
      cy: 15.5
    };

    function terrainNoise(x, y) {
      return ((x * 928371 + y * 123457 + x * y * 3343) % 1000) / 1000;
    }

    for (let x = pond.x; x < pond.x + pond.w; x++) {
      for (let y = pond.y; y < pond.y + pond.h; y++) {
        const dx = (x + 0.5 - pond.cx) / (pond.w / 2);
        const dy = (y + 0.5 - pond.cy) / (pond.h / 2);
        const d = dx * dx + dy * dy;

        const edgeWobble = (terrainNoise(x, y) - 0.5) * 0.18;
        const waterLimit = 0.92 + edgeWobble;

        if (d <= waterLimit) {
          world.pondWater.add(keyOf(x, y));
          world.pondBlocked.add(keyOf(x, y));
        }

        if (d >= waterLimit - 0.16 && d <= waterLimit + 0.16) {
          world.pondShore.add(keyOf(x, y));
        }

        if (d >= waterLimit - 0.22 && d <= waterLimit + 0.05) {
          world.pondNearEdge.add(keyOf(x, y));
        }
      }
    }

    // fences / field edge
    for (let x = 29; x <= 35; x++) {
      world.fences.push({ x, y: 6 });
      world.fences.push({ x, y: 10 });
    }
    for (let y = 7; y <= 9; y++) {
      world.fences.push({ x: 29, y });
      world.fences.push({ x: 35, y });
    }
    world.fences.forEach(f => world.blocked.add(keyOf(f.x, f.y)));

    // trees - more intentional framing
    const treeData = [
      [2,4,"a",1.08], [4,5,"b",1.02], [6,4,"a",1.12], [8,5,"c",0.92],
      [9,3,"b",1.04], [13,3,"a",1.1], [17,3,"b",1.16], [21,3,"c",0.94], [25,3,"a",1.07],
      [31,4,"a",1.03], [34,4,"b",1.12], [36,5,"c",0.9],
      [2,19,"a",1.06], [4,20,"c",0.9], [7,21,"b",1.18], [10,20,"a",1.01],
      [30,20,"a",1.02], [32,21,"b",1.15], [34,22,"c",0.88], [36,21,"a",0.98],
      [29,11,"a",0.96], [31,13,"c",0.93], [33,15,"b",1.14], [35,17,"a",1.05]
    ];
    treeData.forEach(([x,y,type,scale]) => {
      world.trees.push({
        x,
        y,
        type,
        scale,
        jitterX: ((x * 37 + y * 19) % 7) - 3,
        jitterY: ((x * 11 + y * 23) % 5) - 2
      });
      world.blocked.add(keyOf(x, y));
    });

    // zones
    world.zones.push(
      { name: "Hearthvale Square", x: 9, y: 7, w: 18, h: 11 },
      { name: "Mirror Pond", x: 21, y: 12, w: 10, h: 8 },
      { name: "Forest Edge", x: 27, y: 3, w: 11, h: 19 },
      { name: "West Lane", x: 0, y: 7, w: 10, h: 12 }
    );

    const player = {
      x: 18,
      y: 11,
      px: 18 * TILE,
      py: 11 * TILE,
      targetX: 18,
      targetY: 11,
      hp: 50,
      maxHp: 50,
      xp: 0,
      coins: 0,
      moving: false,
      facing: "down",
      speed: 180
    };

    const npc = {
      x: 21,
      y: 12,
      name: "Edrin Vale",
      color: "#6f58df",
      scale: 0.93
    };

    const wolf = {
      x: 31,
      y: 13,
      px: 31 * TILE,
      py: 13 * TILE,
      targetX: 31,
      targetY: 13,
      hp: 22,
      maxHp: 22,
      homeX: 31,
      homeY: 13,
      roam: 3,
      speed: 110
    };

    let lastWolfDecision = 0;
    let lastWolfAttack = 0;

    let activeDialogue = null;
    let dialogueIndex = 0;

    const edrinLines = [
      "You are not from here.",
      "...good.",
      "This town is older than it lets itself appear.",
      "Mirror Pond listens longer than most people do.",
      "Walk slowly. Some places reveal themselves only when you stop trying to rush them."
    ];

    function startDialogue(name, lines) {
      activeDialogue = { name, lines };
      dialogueIndex = 0;
      renderDialogue();
    }

    function renderDialogue() {
      if (!activeDialogue) return;
      dialogue.style.display = "block";
      dialogueName.textContent = activeDialogue.name;
      dialogueText.textContent = activeDialogue.lines[dialogueIndex];
    }

    dialogue.addEventListener("click", () => {
      if (!activeDialogue) return;
      dialogueIndex++;
      if (dialogueIndex >= activeDialogue.lines.length) {
        activeDialogue = null;
        dialogue.style.display = "none";
        return;
      }
      renderDialogue();
    });

    function currentZoneName() {
      for (const z of world.zones) {
        if (
          player.targetX >= z.x &&
          player.targetX < z.x + z.w &&
          player.targetY >= z.y &&
          player.targetY < z.y + z.h
        ) return z.name;
      }
      return "Outer Road";
    }

    function updateSidebar() {
      hpVal.textContent = player.hp + "/" + player.maxHp;
      xpVal.textContent = String(player.xp);
      coinsVal.textContent = String(player.coins);
      zoneVal.textContent = currentZoneName();
      questVal.textContent = "Town Slice";
      objectiveText.textContent = "Walk Hearthvale, visit Mirror Pond, and speak to Edrin Vale.";

      hud.textContent =
        "Move: WASD / Arrows\n" +
        "Interact: Click Edrin Vale\n" +
        "Combat: Avoid or approach the wolf\n" +
        "Zone: " + currentZoneName();
    }

    function canMoveTo(x, y) {
      if (x < 0 || y < 0 || x >= WORLD_W || y >= WORLD_H) return false;
      if (world.blocked.has(keyOf(x, y))) return false;
      if (world.pondBlocked.has(keyOf(x, y))) return false;
      if (x === npc.x && y === npc.y) return false;
      return true;
    }

    const keys = new Set();

    addEventListener("keydown", (e) => {
      const k = e.key.toLowerCase();
      if (["w","a","s","d","arrowup","arrowdown","arrowleft","arrowright"].includes(k)) {
        e.preventDefault();
      }
      keys.add(k);
    });

    addEventListener("keyup", (e) => {
      keys.delete(e.key.toLowerCase());
    });

    canvas.addEventListener("click", (e) => {
      if (activeDialogue) return;

      const clicked = screenToWorld(e.clientX, e.clientY);

      if (clicked.x === npc.x && clicked.y === npc.y) {
        startDialogue(npc.name, edrinLines);
      }
    });

    function getCamera() {
      const tileX = Math.max(0, Math.min(player.targetX - Math.floor(VIEW_TILES_X / 2), WORLD_W - VIEW_TILES_X));
      const tileY = Math.max(0, Math.min(player.targetY - Math.floor(VIEW_TILES_Y / 2), WORLD_H - VIEW_TILES_Y));
      const viewPxW = VIEW_TILES_X * TILE;
      const viewPxH = VIEW_TILES_Y * TILE;
      const offsetX = Math.floor((canvas.width - viewPxW) / 2);
      const offsetY = Math.floor((canvas.height - viewPxH) / 2);
      return { tileX, tileY, offsetX, offsetY };
    }

    function tileToScreen(tx, ty) {
      const cam = getCamera();
      return {
        x: (tx - cam.tileX) * TILE + cam.offsetX,
        y: (ty - cam.tileY) * TILE + cam.offsetY
      };
    }

    function screenToWorld(clientX, clientY) {
      const rect = canvas.getBoundingClientRect();
      const mx = clientX - rect.left;
      const my = clientY - rect.top;
      const cam = getCamera();
      return {
        x: Math.floor((mx - cam.offsetX) / TILE) + cam.tileX,
        y: Math.floor((my - cam.offsetY) / TILE) + cam.tileY
      };
    }

    function smoothMove(entity, dt) {
      const targetPxX = entity.targetX * TILE;
      const targetPxY = entity.targetY * TILE;
      const dx = targetPxX - entity.px;
      const dy = targetPxY - entity.py;
      const dist = Math.hypot(dx, dy);

      if (dist < 0.35) {
        entity.px = targetPxX;
        entity.py = targetPxY;
        entity.moving = false;
        return;
      }

      entity.moving = true;
      const step = entity.speed * dt;
      const nx = dx / dist;
      const ny = dy / dist;

      entity.px += nx * Math.min(step, dist);
      entity.py += ny * Math.min(step, dist);
    }

    const moveIntent = { dx: 0, dy: 0, facing: "down" };

    function tryPlayerStep(dx, dy, facing) {
      if (player.moving || activeDialogue) return;
      const nx = player.targetX + dx;
      const ny = player.targetY + dy;
      player.facing = facing;
      if (!canMoveTo(nx, ny)) return;
      player.targetX = nx;
      player.targetY = ny;
    }

    function updateInput() {
      if (keys.has("w") || keys.has("arrowup")) tryPlayerStep(0, -1, "up");
      else if (keys.has("s") || keys.has("arrowdown")) tryPlayerStep(0, 1, "down");
      else if (keys.has("a") || keys.has("arrowleft")) tryPlayerStep(-1, 0, "left");
      else if (keys.has("d") || keys.has("arrowright")) tryPlayerStep(1, 0, "right");

      moveIntent.dx = 0;
      moveIntent.dy = 0;
      if (keys.has("w") || keys.has("arrowup")) {
        moveIntent.dy = -1;
        moveIntent.facing = "up";
      } else if (keys.has("s") || keys.has("arrowdown")) {
        moveIntent.dy = 1;
        moveIntent.facing = "down";
      } else if (keys.has("a") || keys.has("arrowleft")) {
        moveIntent.dx = -1;
        moveIntent.facing = "left";
      } else if (keys.has("d") || keys.has("arrowright")) {
        moveIntent.dx = 1;
        moveIntent.facing = "right";
      }
    }

    function canWolfMoveTo(x, y) {
      if (x < 0 || y < 0 || x >= WORLD_W || y >= WORLD_H) return false;
      if (world.blocked.has(keyOf(x, y))) return false;
      if (x === npc.x && y === npc.y) return false;
      return true;
    }

    function updateWolf(now) {
      if (now - lastWolfDecision < 650) return;
      lastWolfDecision = now;

      const dx = player.targetX - wolf.targetX;
      const dy = player.targetY - wolf.targetY;
      const dist = Math.abs(dx) + Math.abs(dy);

      if (dist <= 4) {
        const stepX = dx === 0 ? 0 : dx > 0 ? 1 : -1;
        const stepY = dy === 0 ? 0 : dy > 0 ? 1 : -1;

        const optionA = { x: wolf.targetX + stepX, y: wolf.targetY };
        const optionB = { x: wolf.targetX, y: wolf.targetY + stepY };

        if (Math.abs(dx) >= Math.abs(dy) && canWolfMoveTo(optionA.x, optionA.y)) {
          wolf.targetX = optionA.x;
          wolf.targetY = optionA.y;
        } else if (canWolfMoveTo(optionB.x, optionB.y)) {
          wolf.targetX = optionB.x;
          wolf.targetY = optionB.y;
        }
      } else {
        const backX = wolf.targetX < wolf.homeX ? 1 : wolf.targetX > wolf.homeX ? -1 : 0;
        const backY = wolf.targetY < wolf.homeY ? 1 : wolf.targetY > wolf.homeY ? -1 : 0;

        if (Math.abs(wolf.targetX - wolf.homeX) > wolf.roam && canWolfMoveTo(wolf.targetX + backX, wolf.targetY)) {
          wolf.targetX += backX;
        }
        if (Math.abs(wolf.targetY - wolf.homeY) > wolf.roam && canWolfMoveTo(wolf.targetX, wolf.targetY + backY)) {
          wolf.targetY += backY;
        }
      }
    }

    function wolfAttack(now) {
      const dist = Math.abs(player.targetX - wolf.targetX) + Math.abs(player.targetY - wolf.targetY);
      if (dist > 1) return;
      if (now - lastWolfAttack < 1100) return;

      lastWolfAttack = now;
      player.hp = Math.max(0, player.hp - 5);
      log("A wolf bites you for 5.");

      if (player.hp <= 0) {
        player.hp = player.maxHp;
        player.targetX = 18;
        player.targetY = 11;
        player.px = player.targetX * TILE;
        player.py = player.targetY * TILE;
        log("System: You wake in Hearthvale Square.");
      }
    }

    function drawImageTile(img, x, y, fallback) {
      const p = tileToScreen(x, y);
      if (img && img.complete && img.naturalWidth > 0) {
        ctx.drawImage(img, p.x, p.y, TILE, TILE);
      } else {
        ctx.fillStyle = fallback;
        ctx.fillRect(p.x, p.y, TILE, TILE);
      }
    }

    function drawShoreWater() {
      for (let x = pond.x - 1; x <= pond.x + pond.w; x++) {
        for (let y = pond.y - 1; y <= pond.y + pond.h; y++) {
          const key = keyOf(x, y);
          if (!world.pondWater.has(key)) continue;

          const dx = (x + 0.5 - pond.cx) / (pond.w / 2);
          const dy = (y + 0.5 - pond.cy) / (pond.h / 2);
          const d = dx * dx + dy * dy;

          const isEdgeWater = d > 0.54 || world.pondNearEdge.has(key);
          drawImageTile(isEdgeWater ? assets.waterShallow : assets.waterDeep, x, y, isEdgeWater ? "#6d97d7" : "#3b67bf");

          const p = tileToScreen(x, y);

          // reflection band near shoreline
          if (world.pondNearEdge.has(key)) {
            ctx.fillStyle = "rgba(214,235,255,0.12)";
            ctx.fillRect(p.x + 2, p.y + 3, TILE - 4, 3);
          }

          // depth readability gradient
          const depthAlpha = Math.max(0, Math.min(0.24, (0.72 - d) * 0.34));
          if (depthAlpha > 0) {
            ctx.fillStyle = "rgba(18,46,96," + depthAlpha.toFixed(3) + ")";
            ctx.fillRect(p.x, p.y, TILE, TILE);
          }
        }
      }

      // shoreline color variation and reeds
      for (let x = pond.x - 1; x <= pond.x + pond.w; x++) {
        for (let y = pond.y - 1; y <= pond.y + pond.h; y++) {
          if (!world.pondShore.has(keyOf(x, y))) continue;
          const p = tileToScreen(x, y);
          const seed = (x * 13 + y * 17) % 7;

          ctx.fillStyle = seed % 2 === 0 ? "rgba(178,151,112,0.15)" : "rgba(142,165,108,0.14)";
          ctx.fillRect(p.x, p.y, TILE, TILE);

          if (seed <= 2) {
            ctx.fillStyle = "rgba(76,118,66,0.62)";
            ctx.fillRect(p.x + 6 + seed * 3, p.y + 20, 2, 8);
            ctx.fillRect(p.x + 11 + seed * 2, p.y + 18, 2, 10);
          }
        }
      }
    }

    function drawBuilding(b) {
      const groundShadow = tileToScreen(b.x, b.y + b.h);
      ctx.fillStyle = "rgba(0,0,0,0.15)";
      ctx.fillRect(groundShadow.x - 3, groundShadow.y - 2, b.w * TILE + 6, 8);

      // wall
      for (let x = b.x; x < b.x + b.w; x++) {
        for (let y = b.y + 1; y < b.y + b.h; y++) {
          const p = tileToScreen(x, y);
          ctx.fillStyle = b.wall;
          ctx.fillRect(p.x, p.y, TILE, TILE);
          ctx.fillStyle = "rgba(255,255,255,0.04)";
          ctx.fillRect(p.x + 2, p.y + 2, TILE - 4, 3);
        }
      }

      // roof top
      for (let x = b.x; x < b.x + b.w; x++) {
        const p = tileToScreen(x, b.y);
        ctx.fillStyle = b.roofTop;
        ctx.fillRect(p.x, p.y, TILE, TILE);
        ctx.fillStyle = "rgba(255,255,255,0.08)";
        ctx.fillRect(p.x, p.y + 1, TILE, 2);
        ctx.fillStyle = "rgba(0,0,0,0.2)";
        ctx.fillRect(p.x, p.y + 12, TILE, 8);
        ctx.fillStyle = b.roofSide;
        ctx.fillRect(p.x, p.y + TILE - 6, TILE, 6);
      }

      // stronger roof overhang shadow (directional)
      for (let x = b.x; x < b.x + b.w; x++) {
        const p = tileToScreen(x, b.y + 1);
        ctx.fillStyle = "rgba(0,0,0,0.25)";
        ctx.fillRect(p.x + 1, p.y + 1, TILE - 1, 5);
      }

      // door
      {
        const d = tileToScreen(b.doorX, b.doorY - 1);
        ctx.fillStyle = "#3b2518";
        ctx.fillRect(d.x + 10, d.y + 14, 12, 18);
        ctx.fillStyle = "#23140d";
        ctx.fillRect(d.x + 10, d.y + 14, 2, 18);
        ctx.fillStyle = "rgba(235,181,96,0.13)";
        ctx.fillRect(d.x + 11, d.y + 15, 9, 7);
      }

      // window
      {
        const w = tileToScreen(b.x + 1, b.y + 1);
        ctx.fillStyle = "#d7c76d";
        ctx.fillRect(w.x + 8, w.y + 9, 10, 8);
        ctx.fillStyle = "rgba(255,255,255,0.18)";
        ctx.fillRect(w.x + 9, w.y + 10, 8, 2);
      }
      if (b.w >= 4) {
        const w2 = tileToScreen(b.x + b.w - 2, b.y + 1);
        ctx.fillStyle = "#cabd72";
        ctx.fillRect(w2.x + 8, w2.y + 9, 9, 8);
        ctx.fillStyle = "rgba(255,255,255,0.12)";
        ctx.fillRect(w2.x + 9, w2.y + 10, 7, 2);
      }
    }

    function drawTree(t) {
      const p = tileToScreen(t.x, t.y);
      const img = t.type === "b" ? assets.treeB : t.type === "c" ? assets.treeC : assets.treeA;
      const scale = t.scale || 1;
      const drawW = TILE * scale;
      const drawH = (TILE + 4) * scale;
      const drawX = p.x + t.jitterX - (drawW - TILE) / 2;
      const drawY = p.y - 4 + t.jitterY - (drawH - (TILE + 4));

      // larger shadow
      ctx.fillStyle = "rgba(0,0,0,0.18)";
      ctx.beginPath();
      ctx.ellipse(p.x + 16 + t.jitterX * 0.35, p.y + 27, 8 + scale * 4, 4 + scale * 1.6, 0, 0, Math.PI * 2);
      ctx.fill();

      if (img && img.complete && img.naturalWidth > 0) {
        ctx.drawImage(img, drawX, drawY, drawW, drawH);
      } else {
        ctx.fillStyle = "#4a8c45";
        ctx.beginPath();
        ctx.arc(p.x + 16, p.y + 12, 8 + scale * 3, 0, Math.PI * 2);
        ctx.fill();
        ctx.fillStyle = "#5a3d28";
        ctx.fillRect(p.x + 13, p.y + 16, 6, 10);
      }
    }

    function drawZoneLabel(text, tx, ty) {
      const p = tileToScreen(tx, ty);
      ctx.fillStyle = "rgba(0,0,0,0.42)";
      ctx.fillRect(p.x - 2, p.y - 16, text.length * 7 + 10, 18);
      ctx.fillStyle = "#eef2f7";
      ctx.font = "bold 12px monospace";
      ctx.fillText(text, p.x + 3, p.y - 3);
    }

    function drawWorld() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      const cam = getCamera();

      // base grass
      for (let y = cam.tileY; y < cam.tileY + VIEW_TILES_Y; y++) {
        for (let x = cam.tileX; x < cam.tileX + VIEW_TILES_X; x++) {
          const p = tileToScreen(x, y);
          const mix = (x * 17 + y * 23 + x * y * 5) % 9;
          const grassImg = mix <= 2 ? assets.grassB : mix <= 5 ? assets.grassA : assets.grassC;
          drawImageTile(grassImg, x, y, mix % 2 === 0 ? "#2a5630" : "#2d6030");

          if (mix === 1 || mix === 6) {
            ctx.fillStyle = "rgba(88,130,72,0.12)";
            ctx.fillRect(p.x + 1, p.y + 1, TILE - 2, TILE - 2);
          } else if (mix === 4) {
            ctx.fillStyle = "rgba(52,86,46,0.10)";
            ctx.fillRect(p.x + 2, p.y + 2, TILE - 4, TILE - 4);
          }
        }
      }

      // roads
      world.roads.forEach(r => {
        for (let x = r.x; x < r.x + r.w; x++) {
          for (let y = r.y; y < r.y + r.h; y++) {
            drawImageTile(assets.road, x, y, "#9f8764");
          }
        }
      });

      // buildings
      world.buildings.forEach(drawBuilding);

      // pond
      drawShoreWater();

      // well
      {
        const p = tileToScreen(18, 11);
        ctx.fillStyle = "#6e757e";
        ctx.beginPath();
        ctx.arc(p.x + 16, p.y + 16, 11, 0, Math.PI * 2);
        ctx.fill();

        ctx.fillStyle = "#2f477e";
        ctx.beginPath();
        ctx.arc(p.x + 16, p.y + 16, 6, 0, Math.PI * 2);
        ctx.fill();

        ctx.fillStyle = "#8f7551";
        ctx.fillRect(p.x + 6, p.y + 4, 3, 10);
        ctx.fillRect(p.x + 23, p.y + 4, 3, 10);
        ctx.fillRect(p.x + 8, p.y + 4, 16, 3);
      }

      // fences
      world.fences.forEach(f => {
        const p = tileToScreen(f.x, f.y);
        ctx.fillStyle = "#8b7350";
        ctx.fillRect(p.x + 2, p.y + 12, 28, 4);
        ctx.fillRect(p.x + 5, p.y + 5, 4, 22);
        ctx.fillRect(p.x + 23, p.y + 5, 4, 22);
      });

      // trees
      world.trees.forEach(drawTree);

      // labels (fewer, cleaner)
      const zoneName = currentZoneName();
      if (zoneName === "Hearthvale Square") drawZoneLabel("Hearthvale Square", 12, 7);
      if (zoneName === "Mirror Pond") drawZoneLabel("Mirror Pond", 23, 12);
      if (zoneName === "Forest Edge") drawZoneLabel("Forest Edge", 30, 4);

      // NPC
      {
        const p = tileToScreen(npc.x, npc.y);
        ctx.fillStyle = "rgba(0,0,0,0.22)";
        ctx.beginPath();
        ctx.ellipse(p.x + 16, p.y + 29, 8, 4, 0, 0, Math.PI * 2);
        ctx.fill();

        ctx.fillStyle = "#e1e4ee";
        ctx.fillRect(p.x + 10, p.y + 2, 12, 10);
        ctx.fillStyle = npc.color;
        ctx.fillRect(p.x + 8, p.y + 12, 16, 17);
        ctx.fillStyle = "#4a2f78";
        ctx.fillRect(p.x + 8, p.y + 25, 16, 4);

        if (Math.abs(player.targetX - npc.x) + Math.abs(player.targetY - npc.y) <= 5) {
          ctx.fillStyle = "rgba(0,0,0,0.55)";
          ctx.fillRect(p.x - 14, p.y - 16, 78, 14);
          ctx.fillStyle = "#ffffff";
          ctx.font = "bold 11px monospace";
          ctx.fillText(npc.name, p.x - 10, p.y - 5);
        }
      }

      // wolf
      {
        const sx = wolf.px / TILE;
        const sy = wolf.py / TILE;
        const p = tileToScreen(sx, sy);

        ctx.fillStyle = "rgba(0,0,0,0.18)";
        ctx.beginPath();
        ctx.ellipse(p.x + 16, p.y + 28, 9, 4, 0, 0, Math.PI * 2);
        ctx.fill();

        ctx.fillStyle = "#8f98a5";
        ctx.fillRect(p.x + 5, p.y + 12, 18, 9);
        ctx.fillRect(p.x + 18, p.y + 10, 8, 7);
        ctx.fillStyle = "#737c88";
        ctx.fillRect(p.x + 6, p.y + 13, 10, 3);
        ctx.fillStyle = "#8f98a5";
        ctx.fillRect(p.x + 8, p.y + 20, 3, 7);
        ctx.fillRect(p.x + 17, p.y + 20, 3, 7);

        ctx.fillStyle = "rgba(0,0,0,0.45)";
        ctx.fillRect(p.x + 4, p.y - 8, 22, 4);
        ctx.fillStyle = "#92de76";
        ctx.fillRect(p.x + 4, p.y - 8, 22 * (wolf.hp / wolf.maxHp), 4);
      }

      // player (larger / clearer)
      {
        const sx = player.px / TILE;
        const sy = player.py / TILE;
        const p = tileToScreen(sx, sy);

        ctx.fillStyle = "rgba(0,0,0,0.22)";
        ctx.beginPath();
        ctx.ellipse(p.x + 16, p.y + 29, 8, 4, 0, 0, Math.PI * 2);
        ctx.fill();

        ctx.fillStyle = "#e4e9f1";
        ctx.fillRect(p.x + 10, p.y + 2, 12, 10);

        ctx.fillStyle = "#2f67d2";
        ctx.fillRect(p.x + 8, p.y + 12, 16, 17);

        ctx.fillStyle = "#5c4028";
        ctx.fillRect(p.x + 11, p.y + 29, 3, 5);
        ctx.fillRect(p.x + 18, p.y + 29, 3, 5);

        ctx.fillStyle = "#cad2db";
        ctx.fillRect(p.x + 4, p.y + 14, 4, 12);

        ctx.fillStyle = "rgba(0,0,0,0.52)";
        ctx.fillRect(p.x - 10, p.y - 16, 62, 14);
        ctx.fillStyle = "#ffffff";
        ctx.font = "bold 11px monospace";
        ctx.fillText("Wayfarer", p.x - 6, p.y - 5);
      }

      // subtle atmospheric tint
      const phase = (performance.now() / 12000) % (Math.PI * 2);
      const tint = 0.07 + Math.max(0, Math.sin(phase)) * 0.08;
      ctx.fillStyle = "rgba(10,18,32," + tint.toFixed(3) + ")";
      ctx.fillRect(0, 0, canvas.width, canvas.height);
    }

    function update(dt, now) {
      updateInput();
      smoothMove(player, dt);
      if (!player.moving && (moveIntent.dx !== 0 || moveIntent.dy !== 0)) {
        tryPlayerStep(moveIntent.dx, moveIntent.dy, moveIntent.facing);
      }
      updateWolf(now);
      smoothMove(wolf, dt);
      wolfAttack(now);
      updateSidebar();
    }

    let last = performance.now();

    function loop(now) {
      const dt = Math.min(0.033, (now - last) / 1000);
      last = now;

      update(dt, now);
      drawWorld();
      requestAnimationFrame(loop);
    }

    log("System: Visual polish slice loaded.");
    log("System: Walk Hearthvale, visit Mirror Pond, and speak to Edrin Vale.");

    updateSidebar();
    requestAnimationFrame(loop);
  </script>
</body>
</html>`;
