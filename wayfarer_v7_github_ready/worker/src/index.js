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
  <title>Wayfarer — Quality Slice</title>
  <style>
    :root {
      --bg: #071018;
      --panel: rgba(10, 15, 23, 0.94);
      --panel-border: rgba(255,255,255,0.08);
      --text: #e8edf5;
      --muted: #a9b3c2;
      --accent: #9fc7ff;
      --gold: #e3c26a;
    }

    * { box-sizing: border-box; }

    body {
      margin: 0;
      background: radial-gradient(circle at top, #0d1824 0%, #071018 55%);
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

    #brand,
    #stats,
    #objective,
    #logPanel {
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
      background: #0a1520;
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
        <div class="sub">Quality Slice — Town / Pond / Forest Edge</div>
        <span class="tag">Moody mythic rebuild</span>
      </section>

      <section id="stats" class="panel">
        <div class="stats">
          <div class="muted">HP</div><div id="hpVal">50/50</div>
          <div class="muted">XP</div><div id="xpVal">0</div>
          <div class="muted">Coins</div><div id="coinsVal">0</div>
          <div class="muted">Weapon</div><div>Rusty Sword (+2)</div>
          <div class="muted">Quest</div><div id="questVal">None</div>
          <div class="muted">Zone</div><div id="zoneVal">Hearthvale Square</div>
        </div>
      </section>

      <section id="objective" class="panel">
        <div class="questTitle">Current Objective</div>
        <div id="objectiveText" class="muted">Walk the town square and visit Mirror Pond.</div>
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
    const WORLD_W = 36;
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
      grass: new Image(),
      road: new Image(),
      tree: new Image(),
      waterDeep: new Image(),
      waterShallow: new Image()
    };

    assets.grass.src = "./assets/terrain/grass/moss_grass_32.png";
    assets.road.src = "./assets/terrain/roads/worn_path_32.png";
    assets.tree.src = "./assets/terrain/trees/pine_mythic_32.png";
    assets.waterDeep.src = "./assets/terrain/water/deep_water_32.png";
    assets.waterShallow.src = "./assets/terrain/water/shallow_water_32.png";

    const loaded = {
      grass: false,
      road: false,
      tree: false,
      waterDeep: false,
      waterShallow: false
    };

    Object.entries(assets).forEach(([key, img]) => {
      img.onload = () => loaded[key] = true;
      img.onerror = () => loaded[key] = false;
    });

    const world = {
      trees: [],
      buildings: [],
      roads: [],
      ponds: [],
      fences: [],
      zones: [],
      blocked: new Set()
    };

    function keyOf(x, y) {
      return x + "," + y;
    }

    function blockRect(x, y, w, h) {
      for (let ix = x; ix < x + w; ix++) {
        for (let iy = y; iy < y + h; iy++) {
          world.blocked.add(keyOf(ix, iy));
        }
      }
    }

    // -------------------------
    // QUALITY SLICE LAYOUT
    // -------------------------

    // Main square roads
    world.roads.push(
      { x: 6, y: 11, w: 24, h: 2 },
      { x: 17, y: 5, w: 2, h: 14 },
      { x: 9, y: 8, w: 2, h: 8 },
      { x: 24, y: 7, w: 2, h: 8 }
    );

    // Pond
    world.ponds.push({ x: 21, y: 13, w: 7, h: 5, name: "Mirror Pond" });

    // Houses around central town
    world.buildings.push(
      { x: 11, y: 6, w: 4, h: 3, roof: "#5e3f3f", wall: "#6f6a59", doorX: 13, doorY: 9 },
      { x: 20, y: 6, w: 4, h: 3, roof: "#4a4f68", wall: "#746f60", doorX: 22, doorY: 9 },
      { x: 11, y: 14, w: 4, h: 3, roof: "#5b4e39", wall: "#726956", doorX: 13, doorY: 13 }
    );

    world.buildings.forEach(b => blockRect(b.x, b.y, b.w, b.h));

    // Well in town
    const well = { x: 18, y: 11 };

    // Fences near farmland edge
    for (let x = 27; x <= 33; x++) {
      world.fences.push({ x, y: 6 });
      world.fences.push({ x, y: 10 });
    }
    for (let y = 7; y <= 9; y++) {
      world.fences.push({ x: 27, y });
      world.fences.push({ x: 33, y });
    }

    world.fences.forEach(f => world.blocked.add(keyOf(f.x, f.y)));

    // Forest edge trees
    const treePoints = [
      [2,3],[4,4],[6,3],[8,4],[29,3],[31,4],[33,3],
      [29,20],[31,21],[33,20],[6,20],[8,19],[26,19],[28,20],
      [20,3],[22,4],[24,3],[3,16],[4,18],[5,19],[30,15],[31,16],[32,17]
    ];
    treePoints.forEach(([x, y]) => {
      world.trees.push({ x, y });
      world.blocked.add(keyOf(x, y));
    });

    world.zones.push(
      { name: "Hearthvale Square", x: 8, y: 7, w: 18, h: 11 },
      { name: "Mirror Pond", x: 20, y: 12, w: 10, h: 7 },
      { name: "Forest Edge", x: 26, y: 2, w: 10, h: 20 },
      { name: "West Lane", x: 0, y: 8, w: 10, h: 10 }
    );

    const player = {
      x: 17,
      y: 11,
      px: 17 * TILE,
      py: 11 * TILE,
      targetX: 17,
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
      x: 20,
      y: 12,
      name: "Edrin Vale",
      color: "#6e58df"
    };

    const wolf = {
      x: 30,
      y: 13,
      px: 30 * TILE,
      py: 13 * TILE,
      targetX: 30,
      targetY: 13,
      hp: 22,
      maxHp: 22,
      homeX: 30,
      homeY: 13,
      roam: 3,
      speed: 120
    };

    let lastWolfDecision = 0;
    let lastWolfAttack = 0;

    let activeDialogue = null;
    let dialogueIndex = 0;

    const edrinLines = [
      "You are not from here.",
      "...good.",
      "This town still remembers how to be quiet.",
      "The pond remembers more.",
      "Walk slowly. Some places should be learned before they are used."
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
        "Move: WASD / Arrows\\n" +
        "Interact: Click Edrin Vale\\n" +
        "Combat: Avoid or approach the wolf\\n" +
        "Zone: " + currentZoneName();
    }

    function canMoveTo(x, y) {
      if (x < 0 || y < 0 || x >= WORLD_W || y >= WORLD_H) return false;
      if (world.blocked.has(keyOf(x, y))) return false;
      if (x === npc.x && y === npc.y) return false;
      return true;
    }

    const keys = new Set();

    addEventListener("keydown", (e) => {
      const k = e.key.toLowerCase();
      if (["w","a","s","d","arrowup","arrowdown","arrowleft","arrowright"," "].includes(k)) {
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

    function smoothMove(entity, dt) {
      const targetPxX = entity.targetX * TILE;
      const targetPxY = entity.targetY * TILE;

      const dx = targetPxX - entity.px;
      const dy = targetPxY - entity.py;

      const dist = Math.hypot(dx, dy);
      if (dist < 0.5) {
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
    }

    function updateWolf(now) {
      if (now - lastWolfDecision < 600) return;
      lastWolfDecision = now;

      const dx = player.targetX - wolf.targetX;
      const dy = player.targetY - wolf.targetY;
      const dist = Math.abs(dx) + Math.abs(dy);

      if (dist <= 4) {
        const stepX = dx === 0 ? 0 : dx > 0 ? 1 : -1;
        const stepY = dy === 0 ? 0 : dy > 0 ? 1 : -1;

        const tryA = { x: wolf.targetX + stepX, y: wolf.targetY };
        const tryB = { x: wolf.targetX, y: wolf.targetY + stepY };

        if (Math.abs(dx) >= Math.abs(dy) && canWolfMoveTo(tryA.x, tryA.y)) {
          wolf.targetX = tryA.x;
          wolf.targetY = tryA.y;
        } else if (canWolfMoveTo(tryB.x, tryB.y)) {
          wolf.targetX = tryB.x;
          wolf.targetY = tryB.y;
        }
      } else {
        const driftX = wolf.targetX < wolf.homeX ? 1 : wolf.targetX > wolf.homeX ? -1 : 0;
        const driftY = wolf.targetY < wolf.homeY ? 1 : wolf.targetY > wolf.homeY ? -1 : 0;

        if (Math.abs(wolf.targetX - wolf.homeX) > wolf.roam && canWolfMoveTo(wolf.targetX + driftX, wolf.targetY)) {
          wolf.targetX += driftX;
        }
        if (Math.abs(wolf.targetY - wolf.homeY) > wolf.roam && canWolfMoveTo(wolf.targetX, wolf.targetY + driftY)) {
          wolf.targetY += driftY;
        }
      }
    }

    function canWolfMoveTo(x, y) {
      if (x < 0 || y < 0 || x >= WORLD_W || y >= WORLD_H) return false;
      if (world.blocked.has(keyOf(x, y))) return false;
      if (x === npc.x && y === npc.y) return false;
      return true;
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
        player.targetX = 17;
        player.targetY = 11;
        player.px = player.targetX * TILE;
        player.py = player.targetY * TILE;
        log("System: You wake in Hearthvale Square.");
      }
    }

    function drawFallbackTile(x, y, color) {
      const p = tileToScreen(x, y);
      ctx.fillStyle = color;
      ctx.fillRect(p.x, p.y, TILE, TILE);
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

    function drawWorld() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      const cam = getCamera();

      // base grass
      for (let y = cam.tileY; y < cam.tileY + VIEW_TILES_Y; y++) {
        for (let x = cam.tileX; x < cam.tileX + VIEW_TILES_X; x++) {
          drawImageTile(assets.grass, x, y, (x + y) % 2 === 0 ? "#2a5630" : "#2d6030");
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

      // pond with shoreline feel
      world.ponds.forEach(p => {
        for (let x = p.x; x < p.x + p.w; x++) {
          for (let y = p.y; y < p.y + p.h; y++) {
            const edge = (x === p.x || x === p.x + p.w - 1 || y === p.y || y === p.y + p.h - 1);
            drawImageTile(edge ? assets.waterShallow : assets.waterDeep, x, y, edge ? "#5f8fd4" : "#3666c0");
          }
        }
      });

      // buildings
      world.buildings.forEach(b => {
        // wall
        for (let x = b.x; x < b.x + b.w; x++) {
          for (let y = b.y + 1; y < b.y + b.h; y++) {
            const p = tileToScreen(x, y);
            ctx.fillStyle = b.wall;
            ctx.fillRect(p.x, p.y, TILE, TILE);
          }
        }
        // roof
        for (let x = b.x; x < b.x + b.w; x++) {
          const p = tileToScreen(x, b.y);
          ctx.fillStyle = b.roof;
          ctx.fillRect(p.x, p.y, TILE, TILE + 4);
        }
        // door
        const d = tileToScreen(b.doorX, b.doorY - 1);
        ctx.fillStyle = "#3a2416";
        ctx.fillRect(d.x + 9, d.y + 14, 14, 18);
        // window
        const w = tileToScreen(b.x + 1, b.y + 1);
        ctx.fillStyle = "#d8c36f";
        ctx.fillRect(w.x + 8, w.y + 8, 10, 8);
      });

      // well
      {
        const p = tileToScreen(well.x, well.y);
        ctx.fillStyle = "#6f777f";
        ctx.beginPath();
        ctx.arc(p.x + 16, p.y + 16, 11, 0, Math.PI * 2);
        ctx.fill();
        ctx.fillStyle = "#2c4278";
        ctx.beginPath();
        ctx.arc(p.x + 16, p.y + 16, 6, 0, Math.PI * 2);
        ctx.fill();
      }

      // fences
      world.fences.forEach(f => {
        const p = tileToScreen(f.x, f.y);
        ctx.fillStyle = "#8d734f";
        ctx.fillRect(p.x + 2, p.y + 12, 28, 4);
        ctx.fillRect(p.x + 5, p.y + 5, 4, 22);
        ctx.fillRect(p.x + 23, p.y + 5, 4, 22);
      });

      // trees
      world.trees.forEach(t => {
        const p = tileToScreen(t.x, t.y);
        if (assets.tree.complete && assets.tree.naturalWidth > 0) {
          ctx.drawImage(assets.tree, p.x, p.y, TILE, TILE);
        } else {
          ctx.fillStyle = "#4a8c45";
          ctx.beginPath();
          ctx.arc(p.x + 16, p.y + 12, 11, 0, Math.PI * 2);
          ctx.fill();
          ctx.fillStyle = "#5a3d28";
          ctx.fillRect(p.x + 13, p.y + 16, 6, 10);
        }
      });

      // zone labels
      world.zones.forEach(z => {
        const p = tileToScreen(z.x, z.y);
        ctx.fillStyle = "rgba(0,0,0,0.45)";
        ctx.fillRect(p.x - 2, p.y - 18, z.name.length * 7 + 8, 18);
        ctx.fillStyle = "#f2f5f9";
        ctx.font = "bold 12px monospace";
        ctx.fillText(z.name, p.x + 2, p.y - 5);
      });

      // NPC
      {
        const p = tileToScreen(npc.x, npc.y);
        ctx.fillStyle = "#d8d9e8";
        ctx.fillRect(p.x + 10, p.y + 2, 12, 9);
        ctx.fillStyle = npc.color;
        ctx.fillRect(p.x + 8, p.y + 11, 16, 15);
        ctx.fillStyle = "#ffffff";
        ctx.font = "bold 12px monospace";
        ctx.fillText(npc.name, p.x - 10, p.y - 4);
      }

      // Wolf
      {
        const sx = wolf.px / TILE;
        const sy = wolf.py / TILE;
        const p = tileToScreen(sx, sy);
        ctx.fillStyle = "#8a92a0";
        ctx.fillRect(p.x + 5, p.y + 12, 18, 9);
        ctx.fillRect(p.x + 18, p.y + 10, 9, 7);
        ctx.fillRect(p.x + 8, p.y + 19, 3, 7);
        ctx.fillRect(p.x + 17, p.y + 19, 3, 7);

        ctx.fillStyle = "rgba(0,0,0,0.45)";
        ctx.fillRect(p.x + 4, p.y - 8, 22, 4);
        ctx.fillStyle = "#92de76";
        ctx.fillRect(p.x + 4, p.y - 8, 22 * (wolf.hp / wolf.maxHp), 4);
      }

      // Player
      {
        const sx = player.px / TILE;
        const sy = player.py / TILE;
        const p = tileToScreen(sx, sy);

        ctx.fillStyle = "rgba(0,0,0,0.25)";
        ctx.beginPath();
        ctx.ellipse(p.x + 16, p.y + 28, 9, 4, 0, 0, Math.PI * 2);
        ctx.fill();

        ctx.fillStyle = "#e1e7ef";
        ctx.fillRect(p.x + 11, p.y + 2, 10, 9);

        ctx.fillStyle = "#2f67d2";
        ctx.fillRect(p.x + 9, p.y + 11, 14, 16);

        ctx.fillStyle = "#5d4027";
        ctx.fillRect(p.x + 12, p.y + 27, 3, 6);
        ctx.fillRect(p.x + 18, p.y + 27, 3, 6);

        // sword arm
        ctx.fillStyle = "#c5ced7";
        ctx.fillRect(p.x + 5, p.y + 13, 4, 12);

        ctx.fillStyle = "#ffffff";
        ctx.font = "bold 12px monospace";
        ctx.fillText("Wayfarer", p.x - 8, p.y - 4);
      }

      // atmosphere
      const phase = (performance.now() / 12000) % (Math.PI * 2);
      const tint = 0.08 + Math.max(0, Math.sin(phase)) * 0.10;
      ctx.fillStyle = "rgba(10,18,32," + tint.toFixed(3) + ")";
      ctx.fillRect(0, 0, canvas.width, canvas.height);
    }

    function update(dt, now) {
      updateInput();
      smoothMove(player, dt);

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

    log("System: Quality slice loaded.");
    log("System: Visit Mirror Pond and speak to Edrin Vale.");

    updateSidebar();
    requestAnimationFrame(loop);
  </script>
</body>
</html>`;
