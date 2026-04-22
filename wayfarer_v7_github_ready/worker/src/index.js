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
  <title>Wayfarer v8 - Broken Marker</title>
  <style>
    :root {
      --bg: #071019;
      --panel: rgba(12, 18, 28, 0.92);
      --panel-border: rgba(255,255,255,0.10);
      --text: #e9eef7;
      --muted: #a7b0c0;
      --accent: #7cc3ff;
      --danger: #ff7a7a;
      --ok: #8fe388;
      --gold: #f5d36a;
    }

    * { box-sizing: border-box; }

    body {
      margin: 0;
      background: var(--bg);
      color: var(--text);
      font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
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
      border-radius: 20px;
      padding: 16px;
      box-shadow: 0 12px 40px rgba(0,0,0,0.28);
    }

    #sidebar {
      display: flex;
      flex-direction: column;
      gap: 16px;
      min-width: 0;
    }

    h1 {
      margin: 0 0 6px;
      font-size: 26px;
      line-height: 1.1;
    }

    .sub {
      color: var(--muted);
      font-size: 14px;
      margin-bottom: 8px;
    }

    .stats {
      display: grid;
      grid-template-columns: 1fr auto;
      gap: 8px 12px;
      font-size: 15px;
      align-items: center;
    }

    .muted { color: var(--muted); }

    .pill {
      display: inline-block;
      padding: 6px 10px;
      border-radius: 999px;
      background: rgba(255,255,255,0.06);
      font-size: 12px;
      color: var(--muted);
      margin-top: 10px;
    }

    #chat {
      background: rgba(0,0,0,0.28);
      border-radius: 14px;
      padding: 12px;
      min-height: 180px;
      max-height: 260px;
      overflow: auto;
      white-space: pre-line;
      font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
      font-size: 13px;
    }

    #gamePanel {
      position: relative;
      min-width: 0;
      overflow: hidden;
      padding: 0;
    }

    #game {
      width: 100%;
      height: 100%;
      display: block;
      image-rendering: pixelated;
      border-radius: 20px;
      background: #0b1621;
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
      background: rgba(10, 12, 18, 0.96);
      border: 1px solid rgba(255,255,255,0.14);
      border-radius: 18px;
      padding: 16px;
      display: none;
      box-shadow: 0 14px 44px rgba(0,0,0,0.4);
    }

    #dialogueName {
      font-weight: 700;
      margin-bottom: 8px;
      color: var(--accent);
    }

    #dialogueText {
      min-height: 76px;
      white-space: pre-line;
      line-height: 1.45;
      color: var(--text);
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
      <section class="panel">
        <h1>Wayfarer</h1>
        <div class="sub">v8 — Broken Marker</div>
        <div class="pill">Exploration + story first</div>
      </section>

      <section class="panel">
        <div class="stats">
          <div class="muted">HP</div><div id="hpVal">50/50</div>
          <div class="muted">XP</div><div id="xpVal">0</div>
          <div class="muted">Coins</div><div id="coinsVal">0</div>
          <div class="muted">Weapon</div><div>Rusty Sword (+2)</div>
          <div class="muted">Quest</div><div id="questVal">None</div>
          <div class="muted">Zone</div><div id="zoneVal">Hearthvale Crossroads</div>
        </div>
      </section>

      <section class="panel">
        <div class="questTitle">Current Objective</div>
        <div id="objectiveText" class="muted">Speak to Edrin Vale near Mirror Pond.</div>
      </section>

      <section class="panel">
        <div style="font-weight:700; margin-bottom:8px;">Log</div>
        <div id="chat"></div>
      </section>
    </aside>

    <main id="gamePanel" class="panel">
      <canvas id="game"></canvas>
      <div id="hud"></div>

      <div id="dialogue">
        <div id="dialogueName"></div>
        <div id="dialogueText"></div>
        <div id="dialogueHint">Click anywhere on the dialogue box to continue.</div>
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

    const TILE = 28;
    const WORLD_W = 60;
    const WORLD_H = 34;

    function resize() {
      const rect = document.getElementById("gamePanel").getBoundingClientRect();
      canvas.width = Math.max(900, Math.floor(rect.width));
      canvas.height = Math.max(620, Math.floor(rect.height));
    }
    resize();
    addEventListener("resize", resize);

    const world = {
      roads: [
        { x: 0, y: 16, w: 60, h: 2 },
        { x: 18, y: 8, w: 2, h: 16 },
        { x: 30, y: 4, w: 2, h: 22 },
        { x: 48, y: 2, w: 2, h: 16 },
      ],
      fields: [
        { x: 0, y: 0, w: 11, h: 8, name: "Western Fields" },
        { x: 18, y: 0, w: 11, h: 8, name: "Central Fields" },
        { x: 35, y: 0, w: 11, h: 8, name: "Eastern Fields" },
      ],
      pond: { x: 33, y: 17, w: 12, h: 7, name: "Mirror Pond" },
      trees: [],
      markers: [
        { x: 52, y: 10, text: "Broken Marker", discovered: false }
      ],
      labels: [
        { x: 2, y: 12, text: "Hearthvale Crossroads" },
        { x: 37, y: 16, text: "Mirror Pond" },
        { x: 23, y: 29, text: "Eastern Fields" },
      ]
    };

    function pushTree(x, y) {
      world.trees.push({ x, y });
    }

    // Tree lines / clusters
    for (let i = 44; i < 60; i += 3) pushTree(i, 4);
    for (let i = 45; i < 60; i += 2) pushTree(i, 30);
    [31,33,35,38,41,46,50].forEach((x, idx) => pushTree(x, 10 + (idx % 3)));
    [34,36,38,40,43,46,48].forEach((x, idx) => pushTree(x, 25 + (idx % 2)));

    const player = {
      x: 30,
      y: 16,
      hp: 50,
      maxHp: 50,
      xp: 0,
      coins: 0,
      facing: "down"
    };

    const npcs = [
      {
        id: "edrin",
        name: "Edrin Vale",
        x: 29,
        y: 16,
        color: "#7e5bef"
      }
    ];

    const creatures = [
      { id: "wolf1", type: "wolf", x: 46, y: 12, hp: 18, maxHp: 18, homeX: 46, homeY: 12, roam: 3 },
      { id: "wolf2", type: "wolf", x: 48, y: 11, hp: 18, maxHp: 18, homeX: 48, homeY: 11, roam: 3 },
      { id: "wolf3", type: "wolf", x: 50, y: 13, hp: 18, maxHp: 18, homeX: 50, homeY: 13, roam: 3 },
      { id: "turkey1", type: "turkey", x: 25, y: 6, hp: 8, maxHp: 8, homeX: 25, homeY: 6, roam: 2 },
      { id: "turkey2", type: "turkey", x: 21, y: 5, hp: 8, maxHp: 8, homeX: 21, homeY: 5, roam: 2 },
      { id: "turkey3", type: "turkey", x: 41, y: 5, hp: 8, maxHp: 8, homeX: 41, homeY: 5, roam: 2 }
    ];

    const quest = {
      id: "broken_marker",
      state: "not_started", // not_started | active | found | complete
    };

    let lastAttackAt = 0;
    let lastCreatureStep = 0;
    let lastWolfHit = 0;

    let activeDialogue = null;
    let activeDialogueIndex = 0;

    const edrinIntro = [
      "You are not from here.",
      "...good.",
      "Most travelers walk roads.",
      "Few question where they lead.",
      "There is a stone beyond the trees.",
      "It should not exist.",
      "Yet it does."
    ];

    const edrinAfterFind = [
      "So. You found it.",
      "Then the stories were not lies after all.",
      "Keep what you felt to yourself, for now.",
      "Take this coin. And remember the shape of that stone."
    ];

    function log(message) {
      chat.textContent = message + "\\n" + chat.textContent;
    }

    log("System: Wayfarer v8 loaded.");
    log("System: Speak to Edrin Vale near Mirror Pond.");

    const keys = new Set();

    addEventListener("keydown", (e) => {
      const key = e.key.toLowerCase();
      if (["arrowup","arrowdown","arrowleft","arrowright","w","a","s","d"," "].includes(key)) {
        e.preventDefault();
      }
      keys.add(key);

      if (key === " " || e.key === " ") {
        manualAttack();
      }
    });

    addEventListener("keyup", (e) => {
      keys.delete(e.key.toLowerCase());
    });

    dialogue.addEventListener("click", () => {
      if (!activeDialogue) return;

      activeDialogueIndex++;
      if (activeDialogueIndex >= activeDialogue.lines.length) {
        dialogue.style.display = "none";

        if (activeDialogue.id === "edrin_intro" && quest.state === "not_started") {
          quest.state = "active";
          log("Quest started: The Broken Marker");
        }

        if (activeDialogue.id === "edrin_complete" && quest.state === "found") {
          quest.state = "complete";
          player.xp += 25;
          player.coins += 10;
          log("Quest complete: The Broken Marker");
          log("Reward: +25 XP, +10 coins");
        }

        activeDialogue = null;
        activeDialogueIndex = 0;
        updateSidebar();
        return;
      }

      renderDialogue();
    });

    canvas.addEventListener("click", (e) => {
      if (activeDialogue) return;

      const { worldX, worldY } = screenToWorld(e.clientX, e.clientY);

      const npc = npcs.find(n => n.x === worldX && n.y === worldY);
      if (npc && npc.id === "edrin") {
        if (quest.state === "found") {
          startDialogue("edrin_complete", "Edrin Vale", edrinAfterFind);
        } else {
          startDialogue("edrin_intro", "Edrin Vale", edrinIntro);
        }
        return;
      }

      const target = creatures.find(c => c.hp > 0 && c.x === worldX && c.y === worldY);
      if (target) {
        attackCreature(target);
      }
    });

    function startDialogue(id, speaker, lines) {
      activeDialogue = { id, speaker, lines };
      activeDialogueIndex = 0;
      renderDialogue();
    }

    function renderDialogue() {
      if (!activeDialogue) return;
      dialogueName.textContent = activeDialogue.speaker;
      dialogueText.textContent = activeDialogue.lines[activeDialogueIndex];
      dialogue.style.display = "block";
    }

    function worldToScreen(x, y) {
      const camX = Math.max(0, Math.min(player.x - 16, WORLD_W - 32));
      const camY = Math.max(0, Math.min(player.y - 10, WORLD_H - 20));
      return {
        x: (x - camX) * TILE + 40,
        y: (y - camY) * TILE + 40,
        camX,
        camY
      };
    }

    function screenToWorld(clientX, clientY) {
      const rect = canvas.getBoundingClientRect();
      const px = clientX - rect.left;
      const py = clientY - rect.top;

      const camX = Math.max(0, Math.min(player.x - 16, WORLD_W - 32));
      const camY = Math.max(0, Math.min(player.y - 10, WORLD_H - 20));

      return {
        worldX: Math.floor((px - 40) / TILE) + camX,
        worldY: Math.floor((py - 40) / TILE) + camY
      };
    }

    function updateSidebar() {
      hpVal.textContent = player.hp + "/" + player.maxHp;
      xpVal.textContent = String(player.xp);
      coinsVal.textContent = String(player.coins);

      let zone = currentZone();
      zoneVal.textContent = zone;

      if (quest.state === "not_started") {
        questVal.textContent = "None";
        objectiveText.textContent = "Speak to Edrin Vale near Mirror Pond.";
      } else if (quest.state === "active") {
        questVal.textContent = "The Broken Marker";
        objectiveText.textContent = "Search beyond the trees for the stone Edrin described.";
      } else if (quest.state === "found") {
        questVal.textContent = "The Broken Marker";
        objectiveText.textContent = "Return to Edrin Vale at Mirror Pond.";
      } else {
        questVal.textContent = "Complete";
        objectiveText.textContent = "Quest complete. More story to come.";
      }

      hud.textContent =
        "Move: WASD / Arrows\\n" +
        "Attack: Space or click creature\\n" +
        "Zone: " + zone + "\\n" +
        "Quest: " + (quest.state === "not_started" ? "None" : "The Broken Marker");
    }

    function currentZone() {
      const p = world.pond;
      if (player.x >= p.x && player.x < p.x + p.w && player.y >= p.y && player.y < p.y + p.h) {
        return p.name;
      }
      if (player.y < 9) {
        return "Eastern Fields";
      }
      return "Hearthvale Crossroads";
    }

    function movePlayer(dx, dy) {
      const nx = Math.max(0, Math.min(WORLD_W - 1, player.x + dx));
      const ny = Math.max(0, Math.min(WORLD_H - 1, player.y + dy));

      // don't walk through Edrin
      if (npcs.some(n => n.x === nx && n.y === ny)) return;

      player.x = nx;
      player.y = ny;

      if (dx < 0) player.facing = "left";
      if (dx > 0) player.facing = "right";
      if (dy < 0) player.facing = "up";
      if (dy > 0) player.facing = "down";

      checkMarkerDiscovery();
    }

    function manualAttack() {
      const nearby = creatures.find(c => c.hp > 0 && Math.abs(c.x - player.x) <= 1 && Math.abs(c.y - player.y) <= 1);
      if (nearby) attackCreature(nearby);
    }

    function attackCreature(creature) {
      const now = performance.now();
      if (now - lastAttackAt < 350) return;
      lastAttackAt = now;

      if (Math.abs(creature.x - player.x) > 2 || Math.abs(creature.y - player.y) > 2) return;

      const damage = creature.type === "wolf" ? 6 : 5;
      creature.hp -= damage;
      log("You hit " + creature.type + " for " + damage + ".");

      if (creature.hp <= 0) {
        if (creature.type === "wolf") {
          player.xp += 20;
          player.coins += 6;
          log("System: Wayfarer defeated a wolf.");
          log("System: +20 XP, +6 coins.");
        } else {
          player.xp += 8;
          player.coins += 2;
          log("System: Wayfarer defeated a turkey.");
          log("System: +8 XP, +2 coins.");
        }

        setTimeout(() => {
          creature.hp = creature.maxHp;
          creature.x = creature.homeX;
          creature.y = creature.homeY;
        }, 4500);
      }

      updateSidebar();
    }

    function updateCreatures(now) {
      if (now - lastCreatureStep < 700) return;
      lastCreatureStep = now;

      creatures.forEach(c => {
        if (c.hp <= 0) return;

        if (c.type === "wolf") {
          const dx = player.x - c.x;
          const dy = player.y - c.y;
          const dist = Math.abs(dx) + Math.abs(dy);

          if (dist <= 6) {
            c.x += dx === 0 ? 0 : dx > 0 ? 1 : -1;
            c.y += dy === 0 ? 0 : dy > 0 ? 1 : -1;
          } else {
            if (Math.abs(c.x - c.homeX) > c.roam) c.x += c.x < c.homeX ? 1 : -1;
            if (Math.abs(c.y - c.homeY) > c.roam) c.y += c.y < c.homeY ? 1 : -1;
          }
        } else {
          const dir = Math.floor(Math.random() * 4);
          const ox = c.x;
          const oy = c.y;
          if (dir === 0) c.x++;
          if (dir === 1) c.x--;
          if (dir === 2) c.y++;
          if (dir === 3) c.y--;
          if (Math.abs(c.x - c.homeX) > c.roam) c.x = ox;
          if (Math.abs(c.y - c.homeY) > c.roam) c.y = oy;
        }
      });
    }

    function wolvesAttack(now) {
      if (now - lastWolfHit < 1000) return;

      const bitingWolf = creatures.find(c => c.type === "wolf" && c.hp > 0 && Math.abs(c.x - player.x) <= 1 && Math.abs(c.y - player.y) <= 1);
      if (!bitingWolf) return;

      lastWolfHit = now;
      player.hp = Math.max(0, player.hp - 6);
      log("A wolf bites you for 6.");

      if (player.hp <= 0) {
        player.hp = player.maxHp;
        player.x = 30;
        player.y = 16;
        log("System: You collapse and wake at Hearthvale Crossroads.");
      }

      updateSidebar();
    }

    function checkMarkerDiscovery() {
      if (quest.state !== "active") return;

      const marker = world.markers[0];
      if (Math.abs(player.x - marker.x) <= 1 && Math.abs(player.y - marker.y) <= 1) {
        marker.discovered = true;
        quest.state = "found";
        log("System: You feel something is wrong here.");
        log("System: Broken Marker discovered.");
        updateSidebar();
      }
    }

    function drawTileRect(x, y, w, h, color) {
      const pos = worldToScreen(x, y);
      ctx.fillStyle = color;
      ctx.fillRect(pos.x, pos.y, w * TILE, h * TILE);
    }

    function drawWorld() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      // grass
      const camX = Math.max(0, Math.min(player.x - 16, WORLD_W - 32));
      const camY = Math.max(0, Math.min(player.y - 10, WORLD_H - 20));

      for (let y = camY; y < camY + 21; y++) {
        for (let x = camX; x < camX + 33; x++) {
          const sx = (x - camX) * TILE + 40;
          const sy = (y - camY) * TILE + 40;
          const checker = (x + y) % 2 === 0;
          ctx.fillStyle = checker ? "#2d6030" : "#2a5630";
          ctx.fillRect(sx, sy, TILE, TILE);
        }
      }

      // roads
      world.roads.forEach(r => drawTileRect(r.x, r.y, r.w, r.h, "#a9916b"));

      // fields
      world.fields.forEach(f => {
        drawTileRect(f.x, f.y, f.w, f.h, "#c9c06a");
        for (let x = f.x; x < f.x + f.w; x++) {
          for (let y = f.y; y < f.y + f.h; y++) {
            const p = worldToScreen(x, y);
            ctx.fillStyle = (x + y) % 2 === 0 ? "#889443" : "#798739";
            ctx.fillRect(p.x + 4, p.y + 4, TILE - 8, TILE - 8);
          }
        }
      });

      // pond
      drawTileRect(world.pond.x, world.pond.y, world.pond.w, world.pond.h, "#3469cc");
      drawTileRect(world.pond.x + 2, world.pond.y + 1, 5, 3, "#5a8de8");

      // trees
      world.trees.forEach(t => {
        const p = worldToScreen(t.x, t.y);
        ctx.fillStyle = "#4a8c45";
        ctx.beginPath();
        ctx.arc(p.x + TILE/2, p.y + TILE/2 - 2, 12, 0, Math.PI * 2);
        ctx.fill();
        ctx.fillStyle = "#5a3d28";
        ctx.fillRect(p.x + 11, p.y + 16, 6, 10);
      });

      // marker (only visible after found or if very close)
      const marker = world.markers[0];
      if (marker.discovered || Math.abs(player.x - marker.x) <= 2 && Math.abs(player.y - marker.y) <= 2) {
        const p = worldToScreen(marker.x, marker.y);
        ctx.fillStyle = "#8a8f9a";
        ctx.fillRect(p.x + 8, p.y + 4, 12, 22);
        ctx.fillStyle = "#b7d8ff";
        ctx.fillRect(p.x + 11, p.y + 7, 6, 6);
      }

      // labels
      world.labels.forEach(label => {
        const p = worldToScreen(label.x, label.y);
        ctx.fillStyle = "rgba(0,0,0,0.45)";
        ctx.fillRect(p.x - 4, p.y - 18, label.text.length * 7 + 8, 18);
        ctx.fillStyle = "#f1f3f5";
        ctx.font = "bold 12px monospace";
        ctx.fillText(label.text, p.x, p.y - 6);
      });

      // NPCs
      npcs.forEach(npc => {
        const p = worldToScreen(npc.x, npc.y);
        ctx.fillStyle = "#6d55de";
        ctx.fillRect(p.x + 7, p.y + 4, 14, 22);
        ctx.fillStyle = "#d7d9ea";
        ctx.fillRect(p.x + 10, p.y + 1, 8, 8);
        ctx.fillStyle = "#ffffff";
        ctx.font = "bold 12px monospace";
        ctx.fillText(npc.name, p.x - 6, p.y - 4);
      });

      // creatures
      creatures.forEach(c => {
        if (c.hp <= 0) return;
        const p = worldToScreen(c.x, c.y);

        if (c.type === "wolf") {
          ctx.fillStyle = "#8a92a0";
          ctx.fillRect(p.x + 4, p.y + 10, 18, 10);
          ctx.fillRect(p.x + 18, p.y + 12, 7, 6);
          ctx.fillRect(p.x + 7, p.y + 18, 3, 7);
          ctx.fillRect(p.x + 16, p.y + 18, 3, 7);
        } else {
          ctx.fillStyle = "#b86a35";
          ctx.fillRect(p.x + 8, p.y + 10, 12, 10);
          ctx.fillRect(p.x + 16, p.y + 7, 6, 6);
          ctx.fillRect(p.x + 11, p.y + 18, 2, 7);
          ctx.fillRect(p.x + 17, p.y + 18, 2, 7);
        }

        // hp bar
        ctx.fillStyle = "rgba(0,0,0,0.5)";
        ctx.fillRect(p.x + 4, p.y - 8, 22, 4);
        ctx.fillStyle = "#89d96b";
        ctx.fillRect(p.x + 4, p.y - 8, 22 * (c.hp / c.maxHp), 4);
      });

      // player
      const pp = worldToScreen(player.x, player.y);
      ctx.fillStyle = "#e3e8f0";
      ctx.fillRect(pp.x + 9, pp.y + 2, 10, 8);  // head
      ctx.fillStyle = "#2d6cdf";
      ctx.fillRect(pp.x + 7, pp.y + 10, 14, 16); // body
      ctx.fillStyle = "#4d311d";
      ctx.fillRect(pp.x + 10, pp.y + 26, 3, 6);
      ctx.fillRect(pp.x + 16, pp.y + 26, 3, 6);
      ctx.fillStyle = "#c9d1dc";
      ctx.fillRect(pp.x + 4, pp.y + 12, 4, 12); // sword/arm silhouette

      ctx.fillStyle = "#ffffff";
      ctx.font = "bold 12px monospace";
      ctx.fillText("Wayfarer", pp.x - 4, pp.y - 4);

      // day/night tint
      const phase = (performance.now() / 10000) % (Math.PI * 2);
      const tint = 0.08 + Math.max(0, Math.sin(phase)) * 0.12;
      ctx.fillStyle = "rgba(15,24,40," + tint.toFixed(3) + ")";
      ctx.fillRect(0, 0, canvas.width, canvas.height);
    }

    function update(now) {
      if (!activeDialogue) {
        if (keys.has("arrowup") || keys.has("w")) movePlayer(0, -1);
        else if (keys.has("arrowdown") || keys.has("s")) movePlayer(0, 1);
        else if (keys.has("arrowleft") || keys.has("a")) movePlayer(-1, 0);
        else if (keys.has("arrowright") || keys.has("d")) movePlayer(1, 0);
      }

      updateCreatures(now);
      wolvesAttack(now);
      updateSidebar();
    }

    function loop(now) {
      update(now);
      drawWorld();
      requestAnimationFrame(loop);
    }

    updateSidebar();
    requestAnimationFrame(loop);
  </script>
</body>
</html>`;
