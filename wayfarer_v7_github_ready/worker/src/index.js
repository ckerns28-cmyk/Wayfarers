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
      gap: 11px;
      min-width: 0;
      padding-right: 2px;
    }

    #brand, #stats, #objective, #logPanel {
      padding: 16px 18px;
      border: 1px solid rgba(255,255,255,0.05);
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
      grid-template-columns: minmax(72px, 1fr) auto;
      gap: 10px 14px;
      align-items: center;
      font-size: 14px;
      line-height: 1.35;
      letter-spacing: 0.1px;
    }

    .muted {
      color: var(--muted);
      letter-spacing: 0.15px;
    }

    #chat {
      background: rgba(0,0,0,0.26);
      border-radius: 16px;
      padding: 14px 15px;
      min-height: 180px;
      max-height: 280px;
      overflow: auto;
      white-space: pre-line;
      font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
      font-size: 12px;
      line-height: 1.6;
      border: 1px solid rgba(255,255,255,0.08);
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
      background: rgba(8,13,20,0.86);
      border: 1px solid rgba(166,200,255,0.28);
      border-radius: 10px;
      padding: 12px 14px;
      font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
      font-size: 12px;
      line-height: 1.62;
      letter-spacing: 0.24px;
      pointer-events: none;
      white-space: pre-line;
      max-width: 320px;
      text-shadow: 0 1px 0 rgba(0,0,0,0.5);
    }

    #dialogue {
      position: absolute;
      left: 24px;
      right: 24px;
      bottom: 24px;
      background: rgba(9, 11, 17, 0.97);
      border: 1px solid rgba(255,255,255,0.24);
      border-radius: 12px;
      padding: 14px 16px 12px;
      display: none;
      box-shadow: 0 16px 44px rgba(0,0,0,0.42), inset 0 0 0 2px rgba(83,100,138,0.4);
    }

    #dialogueName {
      font-weight: 700;
      color: var(--accent);
      margin-bottom: 8px;
    }

    #dialogueText {
      white-space: pre-line;
      line-height: 1.56;
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

    // trees - dense edge containment with open town center
    const treeData = [
      // west outer wall (irregular clusters and lane openings)
      [1,2,"a"], [2,2,"b"], [3,3,"a"], [2,5,"c"], [1,6,"a"],
      [3,7,"b"], [2,9,"a"], [1,11,"c"], [3,12,"a"], [2,14,"b"],
      [1,17,"a"], [2,19,"b"], [3,21,"a"], [1,22,"c"], [4,23,"a"],

      // north boundary (heavier on corners, sparse above town center)
      [2,1,"a"], [4,2,"c"], [7,1,"b"], [10,2,"a"], [13,2,"c"],
      [27,2,"a"], [30,1,"b"], [33,2,"a"], [35,1,"c"], [37,2,"a"],

      // east outer wall (dense, varied spacing)
      [36,2,"a"], [35,4,"b"], [37,5,"a"], [36,7,"c"], [35,9,"a"],
      [36,11,"b"], [37,13,"a"], [35,15,"c"], [36,17,"a"], [37,19,"b"],
      [35,21,"a"], [36,23,"c"], [34,22,"a"],

      // south boundary (broken wall feel, path pockets left clear)
      [4,22,"b"], [6,23,"a"], [9,22,"c"], [12,23,"a"], [15,22,"b"],
      [24,23,"a"], [27,22,"c"], [30,23,"a"], [33,22,"b"],

      // medium-density mid-range containment bands
      [5,5,"a"], [6,8,"b"], [7,19,"a"], [9,4,"c"],
      [31,5,"a"], [32,8,"b"], [31,19,"a"], [29,21,"c"],

      // pond framing clusters (shoreline stays readable)
      [21,15,"a"], [22,18,"c"], [29,16,"b"], [28,19,"c"]
    ];

    function scaledTree(x, y, type) {
      const centerX = 19;
      const centerY = 12;
      const dx = x - centerX;
      const dy = y - centerY;
      const dist = Math.sqrt(dx * dx + dy * dy);
      const edgeWeight = Math.min(1, dist / 16);
      const rand = (((x * 97 + y * 57 + x * y * 13) % 1000) / 1000) - 0.5;
      const scale = Math.max(0.9, Math.min(1.2, 0.95 + edgeWeight * 0.22 + rand * 0.12));
      const variantSeed = (x * 23 + y * 31 + x * y * 7) % 9;
      return { x, y, type, scale, variantSeed };
    }

    treeData.forEach(([x,y,type]) => {
      const tree = scaledTree(x, y, type);
      world.trees.push({
        x: tree.x,
        y: tree.y,
        type: tree.type,
        scale: tree.scale,
        variantSeed: tree.variantSeed,
        toneShift: (((x * 61 + y * 41) % 9) - 4) / 100,
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
      facing: "down",
      palette: {
        skin: "#d9c2a1",
        skinShade: "#b89c7e",
        hair: "#dbe6f8",
        hairShade: "#8f9bb2",
        tunic: "#5f4db1",
        tunicShade: "#46378d",
        cloak: "#3f2f72",
        boots: "#35261d"
      }
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
      speed: 110,
      facing: "left"
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
        "WASD / Arrows : Move\n" +
        "Click Edrin Vale : Talk\n" +
        "Wolf nearby : Keep distance\n" +
        "Current Zone : " + currentZoneName();
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
          if (stepX !== 0) wolf.facing = stepX > 0 ? "right" : "left";
        } else if (canWolfMoveTo(optionB.x, optionB.y)) {
          wolf.targetX = optionB.x;
          wolf.targetY = optionB.y;
        }
      } else {
        const backX = wolf.targetX < wolf.homeX ? 1 : wolf.targetX > wolf.homeX ? -1 : 0;
        const backY = wolf.targetY < wolf.homeY ? 1 : wolf.targetY > wolf.homeY ? -1 : 0;

        if (Math.abs(wolf.targetX - wolf.homeX) > wolf.roam && canWolfMoveTo(wolf.targetX + backX, wolf.targetY)) {
          wolf.targetX += backX;
          if (backX !== 0) wolf.facing = backX > 0 ? "right" : "left";
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

    function drawSoftShadow(cx, cy, rx, ry, alpha = 0.2, offsetX = 3, offsetY = 4) {
      const grad = ctx.createRadialGradient(
        cx + offsetX,
        cy + offsetY,
        Math.max(1, rx * 0.3),
        cx + offsetX,
        cy + offsetY,
        Math.max(rx, ry) * 1.2
      );
      grad.addColorStop(0, "rgba(0,0,0," + (alpha * 0.8).toFixed(3) + ")");
      grad.addColorStop(1, "rgba(0,0,0,0)");
      ctx.fillStyle = grad;
      ctx.beginPath();
      ctx.ellipse(cx + offsetX, cy + offsetY, rx, ry, 0, 0, Math.PI * 2);
      ctx.fill();
    }

    function animationPose(moving, stepMs, amplitude = 1) {
      const t = performance.now();
      if (moving) {
        const frame = Math.floor(t / stepMs) % 4;
        const legSwing = [0.85, -0.65, -0.9, 0.6][frame] * amplitude;
        const armSwing = [-0.65, 0.75, 0.7, -0.55][frame] * amplitude;
        const bob = [0, 1, 0, -1][frame] * Math.max(0.6, amplitude * 0.9);
        return { moving: true, frame, legSwing, armSwing, bob, breath: 0, stance: 0 };
      }

      const breath = Math.sin(t / 560) * 0.7 * amplitude;
      const stance = Math.cos(t / 900) * 0.5 * amplitude;
      const bob = Math.sin(t / 700) * 0.35 * amplitude;
      return { moving: false, frame: 0, legSwing: 0, armSwing: 0, bob, breath, stance };
    }

    function drawShoreWater() {
      const t = performance.now() * 0.0016;
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

          const layerA = (Math.sin(t * 3.4 + x * 0.92 + y * 0.33) + 1) * 0.5;
          const layerB = (Math.cos(t * 2.8 + x * 0.43 - y * 1.08) + 1) * 0.5;
          const translucency = 0.03 + layerA * 0.045;
          ctx.fillStyle = "rgba(120,174,232," + translucency.toFixed(3) + ")";
          ctx.fillRect(p.x + 1, p.y + 1, TILE - 2, TILE - 2);
          ctx.fillStyle = "rgba(72,128,196," + (0.018 + layerB * 0.03).toFixed(3) + ")";
          ctx.fillRect(p.x + 2, p.y + 2, TILE - 4, TILE - 4);

          // reflection band near shoreline
          if (world.pondNearEdge.has(key)) {
            const shimmer = 0.08 + ((Math.sin(t * 3.8 + x * 0.84 + y * 0.54) + 1) * 0.03);
            ctx.fillStyle = "rgba(214,235,255," + shimmer.toFixed(3) + ")";
            ctx.fillRect(p.x + 2, p.y + 3, TILE - 4, 3);
          }

          // depth readability gradient
          const depthAlpha = Math.max(0, Math.min(0.24, (0.72 - d) * 0.34));
          if (depthAlpha > 0) {
            ctx.fillStyle = "rgba(18,46,96," + depthAlpha.toFixed(3) + ")";
            ctx.fillRect(p.x, p.y, TILE, TILE);
          }

          const deepCore = Math.max(0, Math.min(0.2, (0.52 - d) * 0.42));
          if (deepCore > 0) {
            ctx.fillStyle = "rgba(11,29,68," + deepCore.toFixed(3) + ")";
            ctx.fillRect(p.x + 1, p.y + 1, TILE - 2, TILE - 2);
          }

          // interior animated depth pulse
          const pulse = Math.max(0, (Math.sin(t * 2.6 + x * 0.55 - y * 0.41) + 1) * 0.5 - 0.45);
          if (pulse > 0.015) {
            ctx.fillStyle = "rgba(136,182,236," + (pulse * 0.14).toFixed(3) + ")";
            ctx.fillRect(p.x + 1, p.y + 1, TILE - 2, TILE - 2);
          }

          // ripple lines to keep pond visually alive
          const rippleA = (Math.sin(t * 5.2 + x * 1.16 + y * 0.83) + 1) * 0.5;
          const rippleB = (Math.sin(t * 4.4 + x * 0.71 - y * 1.19) + 1) * 0.5;
          const alphaA = 0.03 + rippleA * 0.05;
          const alphaB = 0.02 + rippleB * 0.04;
          ctx.fillStyle = "rgba(197,228,255," + alphaA.toFixed(3) + ")";
          ctx.fillRect(p.x + 3, p.y + 7 + ((x + y) % 3), TILE - 10, 1);
          ctx.fillStyle = "rgba(143,190,241," + alphaB.toFixed(3) + ")";
          ctx.fillRect(p.x + 5, p.y + 18 + ((x * 2 + y) % 2), TILE - 13, 1);

          const colorFlux = (Math.sin(t * 2.3 + x * 0.6 + y * 0.44) + 1) * 0.5;
          const fluxAlpha = 0.02 + colorFlux * 0.035;
          ctx.fillStyle = "rgba(98,163,224," + fluxAlpha.toFixed(3) + ")";
          ctx.fillRect(p.x + 2, p.y + 2, TILE - 4, TILE - 4);

          if (world.pondNearEdge.has(key)) {
            const edgeSweep = (Math.sin(t * 6.1 + x * 1.5 - y * 0.9) + 1) * 0.5;
            const edgeAlpha = 0.04 + edgeSweep * 0.08;
            ctx.fillStyle = "rgba(227,243,255," + edgeAlpha.toFixed(3) + ")";
            ctx.fillRect(p.x + 1, p.y + 1, TILE - 2, 1);
            ctx.fillRect(p.x + 1, p.y + TILE - 2, TILE - 2, 1);
            ctx.fillRect(p.x + 1 + ((x + y) % 4), p.y + 3, TILE - 8, 1);
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
          ctx.fillStyle = "rgba(102,138,88,0.11)";
          ctx.fillRect(p.x + 1, p.y + 1, TILE - 2, TILE - 2);

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
      drawSoftShadow(
        groundShadow.x + (b.w * TILE) / 2,
        groundShadow.y + 2,
        b.w * TILE * 0.54,
        7,
        0.2,
        4,
        2
      );

      // wall
      for (let x = b.x; x < b.x + b.w; x++) {
        for (let y = b.y + 1; y < b.y + b.h; y++) {
          const p = tileToScreen(x, y);
          const wallShift = ((x * 13 + y * 7) % 3) - 1;
          ctx.fillStyle = b.wall;
          ctx.fillRect(p.x, p.y, TILE, TILE);
          if (wallShift === 1) {
            ctx.fillStyle = "rgba(255,255,255,0.05)";
            ctx.fillRect(p.x + 1, p.y + 1, TILE - 2, TILE - 2);
          } else if (wallShift === -1) {
            ctx.fillStyle = "rgba(0,0,0,0.08)";
            ctx.fillRect(p.x + 1, p.y + 1, TILE - 2, TILE - 2);
          }
          ctx.fillStyle = "rgba(255,255,255,0.04)";
          ctx.fillRect(p.x + 2, p.y + 2, TILE - 4, 3);
          ctx.fillStyle = "rgba(0,0,0,0.14)";
          ctx.fillRect(p.x + TILE - 3, p.y + 1, 2, TILE - 2);
          ctx.fillStyle = "rgba(0,0,0,0.10)";
          ctx.fillRect(p.x + 1, p.y + TILE - 3, TILE - 2, 2);
        }
      }

      // roof top
      for (let x = b.x; x < b.x + b.w; x++) {
        const p = tileToScreen(x, b.y);
        const tone = ((x * 17 + b.y * 13) % 3) - 1;
        const tint = tone === 1 ? "rgba(255,255,255,0.07)" : tone === -1 ? "rgba(0,0,0,0.08)" : "rgba(255,255,255,0.03)";
        ctx.fillStyle = b.roofTop;
        ctx.fillRect(p.x, p.y, TILE, TILE);
        ctx.fillStyle = tint;
        ctx.fillRect(p.x + 1, p.y + 1, TILE - 2, TILE - 2);
        ctx.fillStyle = "rgba(255,255,255,0.08)";
        ctx.fillRect(p.x, p.y + 1, TILE, 2);
        ctx.fillStyle = "rgba(0,0,0,0.26)";
        ctx.fillRect(p.x, p.y + 10, TILE, 10);
        ctx.fillStyle = b.roofSide;
        ctx.fillRect(p.x, p.y + TILE - 7, TILE, 7);
        ctx.fillStyle = "rgba(245,230,199,0.12)";
        ctx.fillRect(p.x + 2, p.y + TILE - 6, TILE - 4, 1);
      }

      // stronger roof overhang shadow (directional)
      for (let x = b.x; x < b.x + b.w; x++) {
        const p = tileToScreen(x, b.y + 1);
        ctx.fillStyle = "rgba(0,0,0,0.3)";
        ctx.fillRect(p.x + 1, p.y + 1, TILE - 1, 6);
      }

      // door
      {
        const d = tileToScreen(b.doorX, b.doorY - 1);
        ctx.fillStyle = "#4f3825";
        ctx.fillRect(d.x + 9, d.y + 13, 14, 19);
        ctx.fillStyle = "#3b2518";
        ctx.fillRect(d.x + 10, d.y + 14, 12, 18);
        ctx.fillStyle = "#23140d";
        ctx.fillRect(d.x + 10, d.y + 14, 2, 18);
        ctx.fillStyle = "rgba(0,0,0,0.28)";
        ctx.fillRect(d.x + 21, d.y + 14, 1, 18);
        ctx.fillStyle = "rgba(235,181,96,0.13)";
        ctx.fillRect(d.x + 11, d.y + 15, 9, 7);
        ctx.fillStyle = "#9a7542";
        ctx.fillRect(d.x + 10, d.y + 12, 12, 2);
      }

      // window
      {
        const w = tileToScreen(b.x + 1, b.y + 1);
        ctx.fillStyle = "#4b3e2f";
        ctx.fillRect(w.x + 6, w.y + 7, 14, 12);
        ctx.fillStyle = "#d7c76d";
        ctx.fillRect(w.x + 8, w.y + 9, 10, 8);
        ctx.fillStyle = "rgba(72,52,34,0.72)";
        ctx.fillRect(w.x + 12, w.y + 9, 1, 8);
        ctx.fillRect(w.x + 8, w.y + 12, 10, 1);
        ctx.fillStyle = "rgba(255,255,255,0.18)";
        ctx.fillRect(w.x + 9, w.y + 10, 8, 2);
      }
      if (b.w >= 4) {
        const w2 = tileToScreen(b.x + b.w - 2, b.y + 1);
        ctx.fillStyle = "#4b3e2f";
        ctx.fillRect(w2.x + 6, w2.y + 7, 13, 12);
        ctx.fillStyle = "#cabd72";
        ctx.fillRect(w2.x + 8, w2.y + 9, 9, 8);
        ctx.fillStyle = "rgba(72,52,34,0.72)";
        ctx.fillRect(w2.x + 12, w2.y + 9, 1, 8);
        ctx.fillRect(w2.x + 8, w2.y + 12, 9, 1);
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
      drawSoftShadow(
        p.x + 16 + t.jitterX * 0.35,
        p.y + 25,
        8 + scale * 4,
        4 + scale * 1.6,
        0.2,
        3,
        3
      );

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

      const variantPulse = 0.07 + (t.variantSeed % 4) * 0.02;
      if (t.toneShift > 0) {
        ctx.fillStyle = "rgba(190,225,168," + variantPulse.toFixed(3) + ")";
      } else {
        ctx.fillStyle = "rgba(34,63,41," + (variantPulse + 0.02).toFixed(3) + ")";
      }
      ctx.fillRect(drawX + 2, drawY + 2, drawW - 4, drawH - 7);

      if (t.variantSeed <= 2) {
        ctx.fillStyle = "rgba(120,92,62,0.22)";
        ctx.fillRect(p.x + 14, p.y + 18, 4, 11);
      }
    }

    function drawZoneLabel(text, tx, ty) {
      const p = tileToScreen(tx, ty);
      const nearPlayer = Math.abs(player.targetX - tx) + Math.abs(player.targetY - ty) <= 3;
      const width = text.length * 7 + 12;
      const labelY = nearPlayer ? p.y - 34 : p.y - 18;
      ctx.fillStyle = "rgba(7,11,18,0.85)";
      ctx.fillRect(p.x - 3, labelY - 13, width, 16);
      ctx.strokeStyle = "rgba(204,216,236,0.62)";
      ctx.lineWidth = 1;
      ctx.strokeRect(p.x - 3.5, labelY - 13.5, width, 16);
      ctx.fillStyle = "#eff4ff";
      ctx.font = "bold 11px monospace";
      ctx.fillText(text, p.x + 2, labelY - 1);
    }

    function drawHumanoidSprite(tileX, tileY, facing, palette, label, scale = 1, isMoving = false) {
      const p = tileToScreen(tileX, tileY);
      const unit = Math.max(1, Math.round(scale));
      const s = v => Math.round(v * scale);
      const pose = animationPose(isMoving, 160, 1);
      const anchorX = p.x + Math.round((TILE - TILE * scale) / 2);
      const anchorY = p.y + Math.round((TILE - TILE * scale));

      drawSoftShadow(p.x + 16, p.y + 29, s(8), s(4), 0.24, 3, 3);

      const bx = anchorX + s(7) + Math.round(pose.stance * 0.35);
      const by = anchorY + s(4) + Math.round(pose.bob);
      const legShiftA = Math.round(pose.legSwing);
      const legShiftB = -legShiftA;

      ctx.fillStyle = palette.boots;
      if (facing === "left" || facing === "right") {
        ctx.fillRect(bx + s(4), by + s(22) + legShiftA, s(4), s(6));
        ctx.fillRect(bx + s(10), by + s(22) + legShiftB, s(4), s(6));
      } else {
        ctx.fillRect(bx + s(3), by + s(22) + legShiftA, s(4), s(6));
        ctx.fillRect(bx + s(10), by + s(22) + legShiftB, s(4), s(6));
      }

      const breathLift = Math.round(pose.breath);
      ctx.fillStyle = palette.tunic;
      ctx.fillRect(bx + s(2), by + s(11) - breathLift, s(13), s(12));
      ctx.fillStyle = palette.tunicShade;
      ctx.fillRect(bx + s(2), by + s(20) - breathLift, s(13), s(3));

      const armA = Math.round(pose.armSwing);
      const armB = -armA;
      if (facing === "up") {
        ctx.fillStyle = palette.cloak;
        ctx.fillRect(bx + s(1), by + s(12) - breathLift, s(15), s(9));
      } else if (facing === "left") {
        ctx.fillStyle = palette.cloak;
        ctx.fillRect(bx + s(1), by + s(12) + armA, s(4), s(9));
      } else if (facing === "right") {
        ctx.fillStyle = palette.cloak;
        ctx.fillRect(bx + s(12), by + s(12) + armB, s(4), s(9));
      } else {
        ctx.fillStyle = palette.cloak;
        ctx.fillRect(bx + s(1), by + s(12) + armA, s(2), s(8));
        ctx.fillRect(bx + s(14), by + s(12) + armB, s(2), s(8));
      }

      ctx.fillStyle = palette.skin;
      if (facing === "left") {
        ctx.fillRect(bx + s(2), by + s(4) - breathLift, s(9), s(9));
      } else if (facing === "right") {
        ctx.fillRect(bx + s(6), by + s(4) - breathLift, s(9), s(9));
      } else {
        ctx.fillRect(bx + s(4), by + s(3) - breathLift, s(9), s(9));
      }
      ctx.fillStyle = palette.skinShade;
      if (facing === "up") {
        ctx.fillRect(bx + s(4), by + s(10) - breathLift, s(9), s(3));
      } else if (facing === "left") {
        ctx.fillRect(bx + s(2), by + s(11) - breathLift, s(9), s(2));
      } else if (facing === "right") {
        ctx.fillRect(bx + s(6), by + s(11) - breathLift, s(9), s(2));
      } else {
        ctx.fillRect(bx + s(4), by + s(11) - breathLift, s(9), s(2));
      }

      ctx.fillStyle = palette.hair;
      if (facing === "up") {
        ctx.fillRect(bx + s(3), by + s(2) - breathLift, s(11), s(5));
      } else if (facing === "left") {
        ctx.fillRect(bx + s(2), by + s(3) - breathLift, s(8), s(5));
      } else if (facing === "right") {
        ctx.fillRect(bx + s(7), by + s(3) - breathLift, s(8), s(5));
      } else {
        ctx.fillRect(bx + s(3), by + s(2) - breathLift, s(11), s(4));
      }
      ctx.fillStyle = palette.hairShade;
      ctx.fillRect(bx + s(4), by + s(7) - breathLift, s(9), unit);

      ctx.strokeStyle = "rgba(12,20,30,0.65)";
      ctx.lineWidth = Math.max(1, Math.round(scale * 0.9));
      ctx.strokeRect(bx + s(2), by + s(3) - breathLift, s(13), s(20));

      if (facing === "down") {
        ctx.fillStyle = "#1b1e28";
        ctx.fillRect(bx + s(6), by + s(8) - breathLift, unit, unit);
        ctx.fillRect(bx + s(9), by + s(8) - breathLift, unit, unit);
      } else if (facing === "left") {
        ctx.fillStyle = "#1b1e28";
        ctx.fillRect(bx + s(4), by + s(8) - breathLift, unit, unit);
      } else if (facing === "right") {
        ctx.fillStyle = "#1b1e28";
        ctx.fillRect(bx + s(11), by + s(8) - breathLift, unit, unit);
      }

      if (label) {
        ctx.fillStyle = "rgba(7,11,18,0.86)";
        ctx.fillRect(p.x - 12, p.y - 20, Math.max(56, label.length * 7 + 8), 14);
        ctx.strokeStyle = "rgba(213,224,242,0.45)";
        ctx.strokeRect(p.x - 12.5, p.y - 20.5, Math.max(56, label.length * 7 + 8), 14);
        ctx.fillStyle = "#f5f8ff";
        ctx.font = "bold 11px monospace";
        ctx.fillText(label, p.x - 8, p.y - 10);
      }
    }

    function drawWolfSprite(tileX, tileY, facing, scale = 1, isMoving = false) {
      const p = tileToScreen(tileX, tileY);
      const pose = animationPose(isMoving, 170, 1.05);
      const s = v => Math.round(v * scale);
      const anchorX = p.x + Math.round((TILE - TILE * scale) / 2);
      const anchorY = p.y + Math.round((TILE - TILE * scale));

      drawSoftShadow(p.x + 16, p.y + 28, s(10), s(4), 0.22, 4, 3);

      const bx = anchorX + s(5) + Math.round(pose.stance * 0.4);
      const by = anchorY + s(9) + Math.round(pose.bob);

      ctx.fillStyle = "#8f98a5";
      ctx.fillRect(bx + s(3), by + s(4), s(16), s(9));
      ctx.fillStyle = "#757e89";
      ctx.fillRect(bx + s(4), by + s(4), s(15), s(3));

      const headOffset = facing === "right" ? s(18) : 0;
      ctx.fillStyle = "#909aa9";
      ctx.fillRect(bx + headOffset, by + s(1) + Math.round(pose.breath * 0.6), s(9), s(7));
      ctx.fillStyle = "#6f7783";
      ctx.fillRect(bx + headOffset + (facing === "right" ? s(5) : 0), by + s(6), s(4), s(2));
      ctx.fillStyle = "#9fa8b4";
      ctx.fillRect(bx + headOffset + s(1), by, s(2), s(3));
      ctx.fillRect(bx + headOffset + s(5), by, s(2), s(3));

      ctx.fillStyle = "#7f8995";
      if (facing === "right") ctx.fillRect(bx + s(1), by + s(7), s(5), s(2));
      else ctx.fillRect(bx + s(18), by + s(7), s(5), s(2));

      const legA = Math.round(pose.legSwing);
      const legB = -legA;
      ctx.fillStyle = "#747d88";
      ctx.fillRect(bx + s(6), by + s(13) + legA, s(3), s(6));
      ctx.fillRect(bx + s(14), by + s(13) + legB, s(3), s(6));
      ctx.fillStyle = "rgba(16,20,27,0.42)";
      ctx.strokeRect(bx + s(3), by + s(1), s(23), s(18));

      ctx.fillStyle = "rgba(0,0,0,0.45)";
      ctx.fillRect(p.x + 2, p.y - 10, Math.max(22, s(22)), 4);
      ctx.fillStyle = "#92de76";
      ctx.fillRect(p.x + 2, p.y - 10, Math.max(22, s(22)) * (wolf.hp / wolf.maxHp), 4);
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

          const noiseA = ((x * 97 + y * 31 + x * y * 7) % 1000) / 1000;
          const noiseB = ((x * 29 + y * 113 + x * y * 3) % 1000) / 1000;
          if (noiseA > 0.73) {
            ctx.fillStyle = "rgba(125,168,93,0.11)";
            ctx.fillRect(p.x + 4, p.y + 5, 2, 2);
            ctx.fillRect(p.x + 10, p.y + 14, 2, 2);
            ctx.fillRect(p.x + 20, p.y + 9, 2, 2);
          } else if (noiseB < 0.2) {
            ctx.fillStyle = "rgba(44,82,39,0.14)";
            ctx.fillRect(p.x + 6, p.y + 7, 2, 2);
            ctx.fillRect(p.x + 18, p.y + 18, 2, 2);
          }

          const dirtNoise = ((x * 71 + y * 43 + x * y * 11) % 997) / 997;
          if (dirtNoise > 0.79) {
            ctx.fillStyle = "rgba(95,74,52,0.16)";
            ctx.fillRect(p.x + 3 + ((x + y) % 9), p.y + 4 + ((x * 2 + y) % 12), 1, 1);
            ctx.fillRect(p.x + 15 + ((x + y * 3) % 7), p.y + 6 + ((x * 3 + y) % 11), 1, 1);
          }
          if (dirtNoise < 0.14) {
            ctx.fillStyle = "rgba(134,171,106,0.08)";
            ctx.fillRect(p.x + 5, p.y + 12, 3, 2);
            ctx.fillRect(p.x + 19, p.y + 20, 2, 2);
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
      drawHumanoidSprite(
        npc.x,
        npc.y,
        npc.facing,
        npc.palette,
        Math.abs(player.targetX - npc.x) + Math.abs(player.targetY - npc.y) <= 5 ? npc.name : "",
        1.5,
        false
      );

      // wolf
      {
        const sx = wolf.px / TILE;
        const sy = wolf.py / TILE;
        drawWolfSprite(sx, sy, wolf.facing, 1.52, wolf.moving);
      }

      const playerPalette = {
        skin: "#e3c7a4",
        skinShade: "#c8a887",
        hair: "#4d3d2f",
        hairShade: "#2f241b",
        tunic: "#2f67d2",
        tunicShade: "#1f4d9c",
        cloak: "#cad2db",
        boots: "#5c4028"
      };

      // player
      {
        const sx = player.px / TILE;
        const sy = player.py / TILE;
        drawHumanoidSprite(sx, sy, player.facing, playerPalette, "Wayfarer", 1.58, player.moving);
      }

      // subtle atmospheric tint
      const phase = (performance.now() / 12000) % (Math.PI * 2);
      const tint = 0.07 + Math.max(0, Math.sin(phase)) * 0.08;
      ctx.fillStyle = "rgba(10,18,32," + tint.toFixed(3) + ")";
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      // viewport edge fade to reduce hard map boundaries
      const edgeFade = ctx.createRadialGradient(
        canvas.width * 0.5,
        canvas.height * 0.5,
        Math.min(canvas.width, canvas.height) * 0.32,
        canvas.width * 0.5,
        canvas.height * 0.5,
        Math.max(canvas.width, canvas.height) * 0.66
      );
      edgeFade.addColorStop(0, "rgba(0,0,0,0)");
      edgeFade.addColorStop(0.76, "rgba(2,7,12,0.1)");
      edgeFade.addColorStop(1, "rgba(2,7,12,0.44)");
      ctx.fillStyle = edgeFade;
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      const leftFog = ctx.createLinearGradient(0, 0, canvas.width * 0.2, 0);
      leftFog.addColorStop(0, "rgba(4,10,16,0.35)");
      leftFog.addColorStop(1, "rgba(4,10,16,0)");
      ctx.fillStyle = leftFog;
      ctx.fillRect(0, 0, canvas.width * 0.2, canvas.height);

      const rightFog = ctx.createLinearGradient(canvas.width, 0, canvas.width * 0.8, 0);
      rightFog.addColorStop(0, "rgba(4,10,16,0.35)");
      rightFog.addColorStop(1, "rgba(4,10,16,0)");
      ctx.fillStyle = rightFog;
      ctx.fillRect(canvas.width * 0.8, 0, canvas.width * 0.2, canvas.height);
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
