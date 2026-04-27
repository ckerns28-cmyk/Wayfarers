export class WorldRoom {
  constructor(state, env) {
    this.state = state;
    this.env = env;
  }

  async fetch() {
    return new Response("WorldRoom active");
  }
}

export default {
  async fetch() {
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
  <title>Wayfarer — Artistic Rebuild Slice</title>
  <style>
    :root {
      --ink:#0b111a;
      --panel:#0f1722;
      --panel-edge:#3a4657;
      --text:#e6ecf5;
      --muted:#9eacbe;
      --gold:#d6bc7f;
      --accent:#8fb6ff;
    }
    * { box-sizing: border-box; }
    #gamePanel, #game, #hud, #dialogue, #vendorPanel, #inventoryPanel, #stats, #objective, #logPanel, #brand {
      user-select: none;
      -webkit-user-select: none;
    }
    body {
      margin:0;
      background: radial-gradient(circle at 30% -10%, #1a2333 0%, #070d14 58%);
      color: var(--text);
      font-family: "Trebuchet MS", Verdana, sans-serif;
      overflow: hidden;
    }
    #wrap {
      display:grid;
      grid-template-columns: 320px 1fr;
      gap:14px;
      height:100vh;
      padding:14px;
    }
    .panel {
      background: linear-gradient(#111a27, #0c131d);
      border: 1px solid #2f3b4e;
      border-radius: 12px;
      box-shadow: 0 14px 40px rgba(0,0,0,.46), inset 0 0 0 1px rgba(255,255,255,.03);
    }
    #sidebar { display:flex; flex-direction:column; gap:10px; min-width:0; }
    #brand,#stats,#objective,#inventoryPanel,#logPanel{padding:14px;}
    h1{margin:0 0 6px;font-size:24px;letter-spacing:.4px}
    .sub{font-size:13px;color:var(--muted)}
    .tag{display:inline-block;margin-top:8px;padding:5px 9px;border:1px solid #435065;border-radius:999px;font-size:11px;color:#c7d6ec}
    .stats{display:grid;grid-template-columns:minmax(72px,1fr) auto;gap:6px 12px;font-size:13px}
    .muted{color:var(--muted)}
    .questTitle{color:var(--gold);font-weight:700;margin-bottom:6px}
    #chat {
      background:#0a1018;
      border:1px solid #2e3b4f;
      border-radius:8px;
      min-height:160px;
      max-height:280px;
      overflow:auto;
      padding:10px;
      white-space:pre-line;
      font:12px/1.45 ui-monospace,SFMono-Regular,Menlo,monospace;
      color:#d2dded;
    }
    #gamePanel{position:relative;overflow:hidden}
    #game{width:100%;height:100%;display:block;border-radius:12px;image-rendering:pixelated;background:#081017}
    #hud {
      position:absolute;top:12px;left:12px;white-space:pre-line;
      pointer-events:none;
      font:12px/1.5 ui-monospace,SFMono-Regular,Menlo,monospace;
      background:rgba(7,11,18,.84);
      border:1px solid #4c6281;
      border-radius:8px;
      padding:10px 12px;
      text-shadow:0 1px 0 #000;
    }
    #dialogue {
      position:fixed;
      left:50%;
      transform:translateX(-50%);
      bottom:max(24px, env(safe-area-inset-bottom));
      width:min(860px, 78vw);
      display:none;
      z-index:25;
      max-height:min(220px, 30vh);
      overflow:auto;
      overscroll-behavior:contain;
      background:linear-gradient(#121a25,#0b1018);
      border:1px solid #51637d;
      border-radius:10px;
      box-shadow:0 12px 34px rgba(0,0,0,.5), inset 0 0 0 1px rgba(255,255,255,.06);
      padding:12px 14px;
    }
    #dialogueName{font-weight:700;color:var(--accent);margin-bottom:8px;letter-spacing:.4px}
    #dialogueText{white-space:pre-wrap;overflow-wrap:anywhere;min-height:62px;line-height:1.5}
    #dialogueChoices{
      margin-top:10px;
      display:grid;
      gap:6px;
    }
    .dialogue-choice{
      border:1px solid #4c6281;
      border-radius:8px;
      background:#162435;
      color:#e6ecf5;
      text-align:left;
      font:12px ui-monospace,SFMono-Regular,Menlo,monospace;
      padding:7px 9px;
      cursor:pointer;
    }
    .dialogue-choice:hover{background:#1b2d44}
    #dialogueHint{margin-top:8px;color:var(--muted);font-size:12px}
    #vendorPanel{
      position:absolute;left:50%;transform:translateX(-50%);bottom:20px;display:none;
      z-index:30;
      width:min(700px, calc(100% - 40px));
      background:linear-gradient(#121a25,#0b1018);
      border:1px solid #51637d;
      border-radius:10px;
      box-shadow:0 12px 34px rgba(0,0,0,.5), inset 0 0 0 1px rgba(255,255,255,.06);
      padding:12px 14px;
    }
    #vendorHeader{display:flex;justify-content:space-between;align-items:center;margin-bottom:8px}
    #vendorName{font-weight:700;color:var(--accent);letter-spacing:.4px}
    #vendorList{max-height:210px;overflow:auto;line-height:1.5}
    #vendorHint{margin-top:8px;color:var(--muted);font-size:12px}
    .vendor-item{display:grid;grid-template-columns:1fr auto auto auto;gap:10px;align-items:center;padding:6px 0;border-bottom:1px solid rgba(158,172,190,.18)}
    .vendor-item:last-child{border-bottom:none}
    .vendor-pill{font-size:11px;border:1px solid #435065;border-radius:999px;padding:2px 8px;color:#c7d6ec}
    .vendor-btn,.vendor-close{
      border:1px solid #4c6281;border-radius:6px;background:#162435;color:#e6ecf5;
      font:12px ui-monospace,SFMono-Regular,Menlo,monospace;padding:4px 8px;cursor:pointer;
    }
    .vendor-btn:disabled{opacity:.55;cursor:not-allowed}
    #saveNotice{
      position:absolute;top:16px;right:16px;opacity:0;transform:translateY(-6px);
      transition:opacity .2s ease,transform .2s ease;
      pointer-events:none;
      font:12px/1.4 ui-monospace,SFMono-Regular,Menlo,monospace;
      background:rgba(14,24,36,.92);
      border:1px solid #4c6281;
      border-radius:8px;
      padding:8px 10px;
      box-shadow:0 8px 22px rgba(0,0,0,.45);
    }
    #saveNotice.visible{opacity:1;transform:translateY(0)}
    #transitionFade{
      position:absolute;inset:0;pointer-events:none;z-index:35;
      background:rgba(2,6,10,0);
    }
  </style>
</head>
<body>
  <div id="wrap">
    <aside id="sidebar">
      <section id="brand" class="panel">
        <h1>Wayfarer</h1>
        <div class="sub">Artistic Rebuild — Hearthvale Slice</div>
        <span class="tag">Mythic Pixel Vertical Slice</span>
      </section>
      <section id="stats" class="panel">
        <div class="stats">
          <div class="muted">HP</div><div id="hpVal">50/50</div>
          <div class="muted">XP</div><div id="xpVal">0</div>
          <div class="muted">Coins</div><div id="coinsVal">0</div>
          <div class="muted">Weapon</div><div id="weaponVal">Rusty Sword (+2)</div>
          <div class="muted">Quest</div><div id="questVal">Town Slice</div>
          <div class="muted">Zone</div><div id="zoneVal">Hearthvale Square</div>
        </div>
      </section>
      <section id="objective" class="panel">
        <div class="questTitle">Current Objective</div>
        <div id="objectiveText" class="muted">Walk Hearthvale, visit Mirror Pond, and speak to Edrin Vale.</div>
      </section>
      <section id="inventoryPanel" class="panel">
        <div class="questTitle">Inventory</div>
        <div id="inventoryList" class="muted">Empty</div>
        <div class="questTitle" style="margin-top:10px;">Equipment</div>
        <div id="equipmentList" class="muted"></div>
      </section>
      <section id="logPanel" class="panel">
        <div class="questTitle">Chronicle</div>
        <div id="chat"></div>
      </section>
    </aside>

    <main id="gamePanel" class="panel">
      <canvas id="game"></canvas>
      <div id="hud"></div>
      <div id="dialogue">
        <div id="dialogueName"></div>
        <div id="dialogueText"></div>
        <div id="dialogueChoices"></div>
        <div id="dialogueHint">Click to continue. Press number keys for choices.</div>
      </div>
      <div id="vendorPanel">
        <div id="vendorHeader">
          <div id="vendorName">Merchant Rowan — Vendor Menu</div>
          <button type="button" id="vendorClose" class="vendor-close">Close</button>
        </div>
        <div id="vendorList"></div>
        <div id="vendorHint">Buy supplies and sell loot. Buying and selling happen one item per click.</div>
      </div>
      <div id="saveNotice">Game Saved</div>
      <div id="transitionFade"></div>
      <script id="dialogueData" type="application/json">
{
  "characters": {
    "edrin": {
      "name": "Edrin Vale",
      "root": "greeting",
      "rootByCondition": [
        { "if": { "questId": "mirror_pond_listening", "state": "Completed" }, "next": "after_pond_rite" },
        { "if": { "questId": "mirror_pond_listening", "state": "Active", "progress": "heard_whispers" }, "next": "pond_whispers_heard" },
        { "if": { "objectiveId": "hunters_request:open_chest", "completed": true }, "next": "cave_relic_observed" },
        { "if": { "questId": "mirror_pond_listening", "state": "Active" }, "next": "pond_listening_active" }
      ],
      "nodes": {
        "greeting": {
          "lines": [
            "You walk like someone called by old water.",
            "I am Edrin Vale. Mirror Pond remembers names before they are spoken.",
            "What do you seek, Wayfarer?"
          ],
          "choices": [
            { "text": "What is Mirror Pond?", "next": "mirror_pond_lore" },
            { "text": "What do you know about the cave?", "next": "mirror_cave_lore" },
            { "text": "Why do people call me Wayfarer?", "next": "wayfarer_title" },
            { "text": "Goodbye.", "next": "end" }
          ]
        },
        "mirror_pond_lore": {
          "lines": [
            "Mirror Pond is older than Hearthvale, older than the roads, older than the names we use.",
            "The surface reflects faces. The depths remember choices."
          ],
          "next": "greeting"
        },
        "mirror_cave_lore": {
          "lines": [
            "Mirror Cave was carved by fear and devotion in equal measure.",
            "Most who enter hear only echoes. A few hear answers."
          ],
          "next": "greeting"
        },
        "wayfarer_title": {
          "lines": [
            "Wayfarer is not a rank. It is a warning.",
            "Some arrive in Hearthvale by road. Others are brought by history."
          ],
          "next": "greeting"
        },
        "pond_listening_active": {
          "lines": [
            "The pond is waiting. Stand at the water in silence and listen."
          ],
          "choices": [
            { "text": "What is Mirror Pond?", "next": "mirror_pond_lore" },
            { "text": "What do you know about the cave?", "next": "mirror_cave_lore" },
            { "text": "Goodbye.", "next": "end" }
          ]
        },
        "pond_whispers_heard": {
          "lines": [
            "The water answered you.",
            "Tell me what the stillness carried."
          ],
          "choices": [
            { "text": "I heard the whispers.", "next": "pond_whispers_turn_in" },
            { "text": "Not yet.", "next": "end" }
          ]
        },
        "pond_whispers_turn_in": {
          "lines": [
            "Then the old vow is stirring again.",
            "You have done what few could."
          ],
          "onCompleteEvents": ["quest:report:mirror_pond"],
          "next": "after_pond_rite"
        },
        "cave_relic_observed": {
          "lines": [
            "You took something from Mirror Cave, didn't you?",
            "The pond's surface has changed since that relic was disturbed."
          ],
          "choices": [
            { "text": "What is Mirror Pond?", "next": "mirror_pond_lore" },
            { "text": "Why do people call me Wayfarer?", "next": "wayfarer_title" },
            { "text": "Goodbye.", "next": "end" }
          ]
        },
        "after_pond_rite": {
          "lines": [
            "Hearthvale heard your step, Wayfarer.",
            "The world is older than it looks, and now it knows you."
          ],
          "choices": [
            { "text": "What do you know about the cave?", "next": "mirror_cave_lore" },
            { "text": "Why do people call me Wayfarer?", "next": "wayfarer_title" },
            { "text": "Goodbye.", "next": "end" }
          ]
        },
        "quest_active_followup": {
          "lines": [
            "The pond is waiting. Go there and be still."
          ],
          "next": "end"
        }
      }
    },
    "hunter_garran": {
      "name": "Hunter Garran",
      "root": "hunters_request_offer",
      "rootByCondition": [
        { "if": { "questId": "hunters_request", "state": "Completed" }, "next": "hunters_request_complete" },
        { "if": { "questId": "hunters_request", "state": "Ready To Turn In" }, "next": "hunters_request_turn_in_ready" },
        { "if": { "questId": "hunters_request", "state": "Active" }, "next": "hunters_request_active" }
      ],
      "nodes": {
        "hunters_request_offer": {
          "lines": [
            "You want to survive out there? Then earn it.",
            "Wolves are ranging near the pond and bandits are watching the trails.",
            "Take Hunter's Request: thin the wolves, enter Mirror Cave, and bring back proof."
          ],
          "choices": [
            { "text": "Accept Hunter's Request", "event": "quest:activate:hunters_request", "next": "hunters_request_active" },
            { "text": "Any survival advice?", "next": "garran_survival_advice" },
            { "text": "Goodbye.", "next": "end" }
          ]
        },
        "hunters_request_active": {
          "lines": [
            "Keep your blade ready and your eyes up.",
            "Report once every objective is done."
          ],
          "choices": [
            { "text": "How are the woods lately?", "next": "garran_woods_flavor" },
            { "text": "Remind me of the objective.", "next": "hunters_request_active" },
            { "text": "Goodbye.", "next": "end" }
          ]
        },
        "hunters_request_turn_in_ready": {
          "lines": [
            "You made it back. That's what matters.",
            "Looks like you've done the work."
          ],
          "choices": [
            { "text": "Complete Hunter's Request", "next": "hunters_request_turn_in" },
            { "text": "One more question first.", "next": "garran_woods_flavor" },
            { "text": "Goodbye.", "next": "end" }
          ]
        },
        "hunters_request_turn_in": {
          "lines": [
            "Good work. You stayed alive, stayed focused, and came back."
          ],
          "onCompleteEvents": ["quest:turn_in:hunters_request"],
          "next": "hunters_request_complete"
        },
        "hunters_request_complete": {
          "lines": [
            "You've proven yourself.",
            "Eastern Woods will still test you, but now you know how to read it."
          ],
          "choices": [
            { "text": "Any survival advice?", "next": "garran_survival_advice" },
            { "text": "How are the woods lately?", "next": "garran_woods_flavor" },
            { "text": "Goodbye.", "next": "end" }
          ]
        },
        "garran_survival_advice": {
          "lines": [
            "Wolves circle before they strike. Keep moving and don't over-commit.",
            "Bandits rush when they smell panic.",
            "In the Eastern Woods, patience keeps you breathing."
          ],
          "next": "hunters_request_offer"
        },
        "garran_woods_flavor": {
          "lines": [
            "Wolves keep to the low brush at dawn. Bandits like the old road bends.",
            "Eastern Woods sound quiet right before trouble starts."
          ],
          "next": "hunters_request_active"
        }
      }
    },
    "merchant_rowan": {
      "name": "Merchant Rowan",
      "root": "rowan_greeting",
      "rootByCondition": [
        { "if": { "itemId": "iron_sword", "minimumOwned": 1 }, "next": "rowan_iron_sword_greeting" }
      ],
      "nodes": {
        "rowan_greeting": {
          "lines": [
            "Welcome, friend. Coin, stories, and practical supplies — that's my trade.",
            "What can I do for you?"
          ],
          "choices": [
            { "text": "Show me your goods.", "event": "vendor:open", "next": "end" },
            { "text": "Any advice?", "next": "rowan_advice" },
            { "text": "Tell me about Hearthvale.", "next": "rowan_hearthvale" },
            { "text": "Goodbye.", "next": "end" }
          ]
        },
        "rowan_iron_sword_greeting": {
          "lines": [
            "That Iron Sword suits you. Mirror Cave doesn't give up steel to just anyone.",
            "Need fresh supplies?"
          ],
          "choices": [
            { "text": "Show me your goods.", "event": "vendor:open", "next": "end" },
            { "text": "Any advice?", "next": "rowan_advice" },
            { "text": "Tell me about Hearthvale.", "next": "rowan_hearthvale" },
            { "text": "Goodbye.", "next": "end" }
          ]
        },
        "rowan_advice": {
          "lines": [
            "Keep at least one potion on hand and sell spare loot often.",
            "If your pack gets heavy, your choices get expensive."
          ],
          "next": "rowan_greeting"
        },
        "rowan_hearthvale": {
          "lines": [
            "Hearthvale looks peaceful until dusk. Then hunters hurry in and mystics get quiet.",
            "If you need rumors, listen near the well at sundown."
          ],
          "next": "rowan_greeting"
        }
      }
    }
  }
}
      </script>
      <script id="questData" type="application/json">
{
  "quests": [
    {
      "id": "mirror_pond_listening",
      "name": "Listening at Mirror Pond",
      "description": "Travel to Mirror Pond and listen in silence.",
      "startEvents": ["quest:activate:mirror_pond_listening"],
      "initialProgress": "go_to_pond",
      "rewards": { "xp": 20, "coins": 6 }
    },
    {
      "id": "hunters_request",
      "questId": "hunters_request",
      "title": "Hunter's Request",
      "name": "Hunter's Request",
      "description": "Defeat wolves, enter Mirror Cave, recover the cave relic, then report back to Hunter Garran.",
      "startEvents": ["quest:activate:hunters_request"],
      "status": "Not Started",
      "objectives": [
        { "id": "wolves", "label": "Defeat 3 wolves", "summaryLabel": "Wolves defeated", "type": "kill", "targetId": "wolf", "requiredAmount": 3, "currentAmount": 0, "completed": false },
        { "id": "enter_cave", "label": "Enter Mirror Cave", "type": "reach", "targetId": "mirror_cave", "requiredAmount": 1, "currentAmount": 0, "completed": false },
        { "id": "open_chest", "label": "Open Mirror Cave chest", "type": "interact", "targetId": "mirror_cave_chest", "requiredAmount": 1, "currentAmount": 0, "completed": false },
        { "id": "return_hunter", "label": "Return to Hunter Garran", "type": "interact", "targetId": "npc_hunter_garran", "requiredAmount": 1, "currentAmount": 0, "completed": false }
      ],
      "rewards": { "xp": 60, "coins": 50, "items": [{ "itemId": "small_potion", "count": 2 }] }
    }
  ]
}
      </script>
    </main>
  </div>
<script>
const canvas = document.getElementById("game");
const gamePanel = document.getElementById("gamePanel");
const ctx = canvas.getContext("2d");
const hud = document.getElementById("hud");
const chat = document.getElementById("chat");
const hpVal = document.getElementById("hpVal");
const xpVal = document.getElementById("xpVal");
const coinsVal = document.getElementById("coinsVal");
const zoneVal = document.getElementById("zoneVal");
const questVal = document.getElementById("questVal");
const weaponVal = document.getElementById("weaponVal");
const objectiveText = document.getElementById("objectiveText");
const inventoryList = document.getElementById("inventoryList");
const equipmentList = document.getElementById("equipmentList");
const dialogue = document.getElementById("dialogue");
const dialogueName = document.getElementById("dialogueName");
const dialogueText = document.getElementById("dialogueText");
const dialogueChoices = document.getElementById("dialogueChoices");
const dialogueHint = document.getElementById("dialogueHint");
const vendorPanel = document.getElementById("vendorPanel");
const vendorList = document.getElementById("vendorList");
const vendorClose = document.getElementById("vendorClose");
const saveNotice = document.getElementById("saveNotice");
const transitionFade = document.getElementById("transitionFade");

function parseJsonScript(id){
  const node=document.getElementById(id);
  if(!node) return {};
  try { return JSON.parse(node.textContent || "{}"); }
  catch(err){ console.error("Invalid JSON in", id, err); return {}; }
}

function updateDialogueViewportConstraints(){
  const panelRect=gamePanel?.getBoundingClientRect();
  if(!panelRect || panelRect.width<=0 || panelRect.height<=0) return;
  const viewportHeight=window.innerHeight || document.documentElement.clientHeight || 0;
  const safeBottomPadding=24;
  const safeTopPadding=24;
  const bottomOffsetFromViewport=Math.max(safeBottomPadding, Math.round(viewportHeight-panelRect.bottom+safeBottomPadding));
  const availableWidth=Math.max(220, Math.floor(panelRect.width-24));
  const maxWidth=Math.min(860, Math.floor(panelRect.width*0.78));
  const preferredWidth=Math.min(760, Math.floor(panelRect.width*0.74));
  const width=Math.min(availableWidth, Math.max(220, Math.min(maxWidth, preferredWidth)));
  const viewportBasedMaxHeight=Math.min(220, Math.floor(viewportHeight*0.30));
  const panelBasedMaxHeight=Math.max(140, Math.floor(panelRect.height-safeTopPadding-bottomOffsetFromViewport-36));
  let maxHeight=Math.max(130, Math.min(viewportBasedMaxHeight, panelBasedMaxHeight));

  dialogue.style.left=Math.round(panelRect.left+(panelRect.width/2)) + "px";
  dialogue.style.bottom=bottomOffsetFromViewport + "px";
  dialogue.style.width=width + "px";
  dialogue.style.maxHeight=maxHeight + "px";
  dialogue.style.overflowY="auto";

  if(dialogue.style.display==="none") return;
  let rect=dialogue.getBoundingClientRect();
  if(rect.bottom>viewportHeight-safeBottomPadding){
    const overlap=Math.ceil(rect.bottom-(viewportHeight-safeBottomPadding));
    dialogue.style.bottom=(bottomOffsetFromViewport+overlap) + "px";
    rect=dialogue.getBoundingClientRect();
  }
  if(rect.top<safeTopPadding){
    const currentBottom=parseFloat(dialogue.style.bottom || "0");
    const safeHeight=Math.max(120, Math.floor(viewportHeight-currentBottom-safeTopPadding));
    maxHeight=Math.min(maxHeight, safeHeight);
    dialogue.style.maxHeight=maxHeight + "px";
  }
}

const TILE = 32;
const WORLD_W = 38;
const WORLD_H = 24;
const OUTDOOR_REGION_DEFS = {
  hearthvale_square: {
    id: "hearthvale_square",
    name: "Hearthvale Square",
    bounds: { x:0, y:0, w:27, h:WORLD_H }
  },
  eastern_woods: {
    id: "eastern_woods",
    name: "Eastern Woods",
    bounds: { x:27, y:0, w:WORLD_W-27, h:WORLD_H }
  }
};
const INTERIOR_REGION_DEFS = {
  mirror_cave: {
    id:"mirror_cave",
    name:"Mirror Cave"
  }
};
const HARD_ZONE_TRANSITIONS = Object.freeze([]);
let currentZoneId = "hearthvale_square";
let zoneTransitionLockedUntil = 0;
const DIRECTION_KEYS = Object.freeze(["w","a","s","d","arrowup","arrowdown","arrowleft","arrowright"]);
let blockedDirectionalKeysUntilRelease = new Set();
let lastLoggedZoneEntryId = currentZoneId;
const VIEW_TILES_X = 22;
const VIEW_TILES_Y = 14;
const ITEM_REGISTRY = Object.freeze({
  rusty_sword: { id:"rusty_sword", name:"Rusty Sword", type:"weapon", attackBonus:2, description:"A worn but dependable blade.", stackable:false, value:8 },
  iron_sword: { id:"iron_sword", name:"Iron Sword", type:"weapon", attackBonus:4, description:"A sharpened iron blade forged for close cave fights.", stackable:false, value:20 },
  leather_armor: { id:"leather_armor", name:"Leather Armor", type:"armor", defenseBonus:2, description:"Sturdy leather armor that softens incoming blows.", stackable:false, value:25 },
  wolf_pelt: { id:"wolf_pelt", name:"Wolf Pelt", type:"material", description:"A coarse pelt taken from a wild wolf.", stackable:true, value:5 },
  small_fang: { id:"small_fang", name:"Small Fang", type:"material", description:"A sharp fang useful for craftwork.", stackable:true, value:3 },
  old_coin: { id:"old_coin", name:"Old Coin", type:"trinket", description:"A worn coin from a forgotten mint.", stackable:true, value:2 },
  cloth_scrap: { id:"cloth_scrap", name:"Cloth Scrap", type:"material", description:"Rough cloth torn from worn travel gear.", stackable:true, value:3 },
  healing_herb: { id:"healing_herb", name:"Healing Herb", type:"consumable", description:"A medicinal herb with a clean scent.", stackable:true, healAmount:10, value:5 },
  small_potion: { id:"small_potion", name:"Small Potion", type:"consumable", description:"A compact tonic that restores vitality.", stackable:true, healAmount:25, value:12 }
});
const WOLF_LOOT_TABLE = Object.freeze([
  { itemId:"wolf_pelt", chance:0.85, min:1, max:1 },
  { itemId:"small_fang", chance:0.65, min:1, max:2 }
]);
const BANDIT_LOOT_TABLE = Object.freeze([
  { itemId:"old_coin", chance:0.9, min:1, max:2 },
  { itemId:"cloth_scrap", chance:0.8, min:1, max:2 }
]);
const VENDOR_BUY_INVENTORY = Object.freeze(["healing_herb","small_potion","leather_armor"]);

function resize() {
  const rect = gamePanel.getBoundingClientRect();
  canvas.width = Math.floor(rect.width);
  canvas.height = Math.floor(rect.height);
  updateDialogueViewportConstraints();
}
resize();
addEventListener("resize", resize);

const palette = {
  grass: ["#415f35", "#39562e", "#4a6c3e", "#2f4828"],
  road: ["#8f7651", "#7c6546", "#9b8260", "#624f37"],
  water: ["#264a72", "#1f3e60", "#2f618f", "#3f7eb5", "#82b8dc"],
  wood: ["#7a573b", "#5a3f2a", "#9b7450", "#c8a37a"],
  roof: ["#7a3e3f", "#5e2d2f", "#9b5c5b", "#3f1f22"],
  wall: ["#88806d", "#6a6354", "#a39a85"],
  fence: ["#7a5b3d", "#5c432c", "#ad8960"],
  uiInk: "#0d141f",
};

function log(message){ chat.textContent = message + "\n" + chat.textContent; }
const logThrottleState=new Map();
function logThrottled(key,message,cooldownMs){
  const now=performance.now();
  const lastAt=logThrottleState.get(key)||0;
  if(now-lastAt<cooldownMs) return false;
  logThrottleState.set(key, now);
  log(message);
  return true;
}
function keyOf(x,y){ return x + "," + y; }
function rng(x,y,s=1){ return (((x*73856093)^(y*19349663)^(s*83492791))>>>0)%1000/1000; }

function makeTile(drawFn){
  const c = document.createElement("canvas"); c.width = TILE; c.height = TILE;
  const p = c.getContext("2d"); p.imageSmoothingEnabled = false; drawFn(p);
  const img = new Image(); img.src = c.toDataURL("image/png"); return img;
}

const assets = {
  grass: [], road: [], roadEdge: [], water: {}, shore: [], detail: [],
  tree: {}, propWell: null, fence: [],
  shadow: {},
  props: { sheet:null, sprites:{}, meta:{} },
  building: {}, sprites: { player:null, npc:null, wolf:null }
};

function buildTerrainTiles() {
  const grassBases = ["#44663a", "#3f6035", "#4a6f40", "#3a5a31", "#507747", "#35542e"];
  for (let i=0;i<6;i++) {
    assets.grass.push(makeTile((p)=>{
      p.fillStyle = grassBases[i]; p.fillRect(0,0,32,32);
      for (let y=0;y<32;y+=2){
        for (let x=0;x<32;x+=2){
          const n=rng(x+i*11,y+i*7,13+i);
          p.fillStyle = n>0.76?"rgba(178,214,138,.2)":n<0.15?"rgba(31,53,24,.3)":"rgba(0,0,0,0)";
          if (n>0.76||n<0.15) p.fillRect(x,y,2,2);
        }
      }
      p.fillStyle = "rgba(204,235,168,.1)";
      for (let k=0;k<8;k++) {
        const gx = ((k*7+i*5)%28)+2, gy = ((k*13+i*3)%25)+3;
        p.fillRect(gx,gy,1,3);
      }
      p.fillStyle="rgba(255,255,255,.03)"; p.fillRect(0,0,32,2);
      p.fillStyle="rgba(0,0,0,.11)"; p.fillRect(0,30,32,2);
    }));

    if(i<5) {
    assets.road.push(makeTile((p)=>{
      p.fillStyle = i%2? "#8b7350" : "#836b49"; p.fillRect(0,0,32,32);
      p.fillStyle = i%2? "#785f43" : "#6f583e";
      for(let y=0;y<32;y+=4){ for(let x=((y+i*2)%5);x<32;x+=7) p.fillRect(x,y,2,2); }
      p.fillStyle = i%2? "#a28a67" : "#9a815f";
      for(let k=0;k<8;k++){ const x=((k*9+i*7)%24)+3; const y=((k*11+i*5)%24)+3; p.fillRect(x,y,3,2); }
      p.fillStyle = "rgba(0,0,0,.18)"; p.fillRect(0,29,32,3);
      p.fillStyle = "rgba(255,255,255,.06)"; p.fillRect(0,0,32,2);
    }));
    }

    assets.shore.push(makeTile((p)=>{
      p.fillStyle = i%2?"#5d7547":"#667e4d"; p.fillRect(0,0,32,32);
      p.fillStyle = "rgba(147,117,78,.46)"; p.fillRect(0,22,32,10);
      p.fillStyle = "rgba(108,140,90,.36)"; p.fillRect(0,0,32,10);
      p.fillStyle = "rgba(230,216,175,.22)"; p.fillRect(0,20,32,2);
      for(let x=3;x<30;x+=5){ p.fillStyle="#4a7140"; p.fillRect(x,15+(x%4),2,8); }
    }));
  }

  for(let i=0;i<4;i++) {
    assets.roadEdge.push(makeTile((p)=>{
      p.fillStyle="rgba(0,0,0,0)"; p.fillRect(0,0,32,32);
      p.fillStyle=i%2? "rgba(121,101,74,.72)" : "rgba(134,112,84,.68)";
      for(let x=0;x<32;x+=2){
        const h = 3 + Math.floor(rng(x,i,77) * 3);
        p.fillRect(x,32-h,2,h);
      }
      p.fillStyle="rgba(66,96,52,.3)"; p.fillRect(0,0,32,2);
    }));
  }

  assets.detail = [
    makeTile((p)=>{ p.fillStyle="rgba(0,0,0,0)"; p.fillRect(0,0,32,32); p.fillStyle="#7f7a71"; p.fillRect(12,18,2,2); p.fillRect(15,17,2,2); p.fillStyle="#9c988d"; p.fillRect(13,16,1,1); }),
    makeTile((p)=>{ p.fillStyle="rgba(0,0,0,0)"; p.fillRect(0,0,32,32); p.fillStyle="#704f35"; p.fillRect(8,20,7,3); p.fillRect(14,19,5,2); p.fillStyle="rgba(156,124,86,.42)"; p.fillRect(10,20,5,1); }),
    makeTile((p)=>{ p.fillStyle="rgba(0,0,0,0)"; p.fillRect(0,0,32,32); p.fillStyle="#587e45"; p.fillRect(18,17,1,5); p.fillRect(20,16,1,6); p.fillRect(22,18,1,4); p.fillStyle="#8fb871"; p.fillRect(19,16,1,2); p.fillRect(21,15,1,2); })
  ];

  assets.water.deep = makeTile((p)=>{
    p.fillStyle = palette.water[1]; p.fillRect(0,0,32,32);
    const g = p.createLinearGradient(0,0,0,32);
    g.addColorStop(0,"#2f6291"); g.addColorStop(.55,palette.water[1]); g.addColorStop(1,palette.water[0]);
    p.fillStyle = g; p.fillRect(0,0,32,32);
    p.fillStyle = "rgba(98,164,214,.2)";
    for(let y=3;y<28;y+=5) p.fillRect(3+(y%4),y,24,1);
    p.fillStyle = "rgba(179,226,255,.13)"; p.fillRect(2,3,17,2);
  });
  assets.water.shallow = makeTile((p)=>{
    const g = p.createLinearGradient(0,0,0,32);
    g.addColorStop(0,"#5e9fca"); g.addColorStop(.35,palette.water[2]); g.addColorStop(1,"#346a99");
    p.fillStyle = g; p.fillRect(0,0,32,32);
    p.fillStyle = "rgba(170,220,245,.22)"; p.fillRect(1,1,30,5);
    p.fillStyle = "rgba(63,115,165,.28)"; p.fillRect(0,24,32,8);
    p.fillStyle = "rgba(210,242,255,.26)"; p.fillRect(3,12,24,2);
  });
  assets.water.edge = makeTile((p)=>{
    p.fillStyle="rgba(0,0,0,0)"; p.fillRect(0,0,32,32);
    const g = p.createLinearGradient(0,0,0,32);
    g.addColorStop(0,"rgba(236,225,179,.28)");
    g.addColorStop(.4,"rgba(185,198,149,.18)");
    g.addColorStop(1,"rgba(84,124,155,0)");
    p.fillStyle=g; p.fillRect(0,0,32,32);
    p.fillStyle="rgba(245,245,220,.2)"; p.fillRect(1,1,30,1);
  });
}

function makeBuildingTiles(){
  assets.building.roofL = makeTile((p)=>{
    p.fillStyle=palette.roof[0]; p.fillRect(0,0,32,32);
    p.fillStyle=palette.roof[1]; for(let y=0;y<32;y++) p.fillRect(0,y,Math.max(0,10-Math.floor(y/4)),1);
    p.fillStyle=palette.roof[2]; for(let y=2;y<28;y+=5) p.fillRect(3,y,26,1);
    p.fillStyle=palette.roof[3]; p.fillRect(0,25,32,7);
  });
  assets.building.roofC = makeTile((p)=>{
    p.fillStyle=palette.roof[0]; p.fillRect(0,0,32,32);
    p.fillStyle=palette.roof[2]; for(let y=2;y<28;y+=5) p.fillRect(2,y,28,1);
    p.fillStyle=palette.roof[3]; p.fillRect(0,25,32,7);
  });
  assets.building.roofR = makeTile((p)=>{
    p.fillStyle=palette.roof[0]; p.fillRect(0,0,32,32);
    p.fillStyle=palette.roof[1]; for(let y=0;y<32;y++){const w=Math.max(0,10-Math.floor(y/4)); p.fillRect(32-w,y,w,1);} 
    p.fillStyle=palette.roof[2]; for(let y=2;y<28;y+=5) p.fillRect(2,y,28,1);
    p.fillStyle=palette.roof[3]; p.fillRect(0,25,32,7);
  });
  assets.building.wall = makeTile((p)=>{
    p.fillStyle=palette.wall[0]; p.fillRect(0,0,32,32);
    p.fillStyle=palette.wall[2]; p.fillRect(0,0,32,2);
    p.fillStyle=palette.wall[1]; p.fillRect(0,30,32,2);
    for(let y=4;y<30;y+=6) for(let x=(y%4);x<32;x+=8){ p.fillStyle="rgba(255,255,255,.06)"; p.fillRect(x,y,1,1); }
  });
  assets.building.window = makeTile((p)=>{
    p.drawImage(assets.building.wall,0,0);
    p.fillStyle="#3b3025"; p.fillRect(8,7,16,14);
    p.fillStyle="#d9bd79"; p.fillRect(10,9,12,10);
    p.fillStyle="rgba(255,246,200,.45)"; p.fillRect(11,10,10,2);
    p.fillStyle="#2a2219"; p.fillRect(15,9,1,10); p.fillRect(10,13,12,1);
  });
  assets.building.door = makeTile((p)=>{
    p.drawImage(assets.building.wall,0,0);
    p.fillStyle="#4b3223"; p.fillRect(9,10,14,21);
    p.fillStyle="#2f1f15"; p.fillRect(10,11,12,19);
    p.fillStyle="#9d7748"; p.fillRect(9,10,14,2);
    p.fillStyle="#d8a55f"; p.fillRect(20,21,1,1);
  });
}

function makeTreeSprites(){
  function tree(canopy,shade,trunk){
    return makeTile((p)=>{
      p.fillStyle=trunk; p.fillRect(14,17,4,12);
      p.fillStyle=shade; p.fillRect(9,10,14,9);
      p.fillStyle=canopy; p.fillRect(6,6,20,9);
      p.fillStyle="rgba(220,255,196,.14)"; p.fillRect(8,8,8,2);
      p.fillStyle="rgba(0,0,0,.2)"; p.fillRect(9,15,14,3);
    });
  }
  assets.tree.a = tree("#5f864b", "#3d5f34", "#6c4c32");
  assets.tree.b = tree("#4f7640", "#324f2b", "#5e422c");
  assets.tree.c = tree("#73945b", "#4c6d40", "#775338");
}

function makeFenceTiles(){
  for(let i=0;i<3;i++) assets.fence.push(makeTile((p)=>{
    const rail = i===1 ? "#876448" : i===2 ? "#7b5a3f" : palette.fence[0];
    p.fillStyle = rail; p.fillRect(2,11,28,4); p.fillRect(2,17,28,3);
    p.fillStyle = palette.fence[1]; p.fillRect(5,4,4,24); p.fillRect(23,4,4,24);
    p.fillStyle = palette.fence[2]; p.fillRect(2,10,28,1); p.fillRect(2,16,28,1);
    p.fillStyle = "rgba(255,229,189,.16)"; p.fillRect(3,11,26,1);
    p.fillStyle = "rgba(0,0,0,.16)"; p.fillRect(2,20,28,1);
  }));
}

function makeShadowTiles(){
  assets.shadow.softTile = makeTile((p)=>{
    p.clearRect(0,0,32,32);
    const g = p.createRadialGradient(12,12,2,17,17,15);
    g.addColorStop(0,"rgba(8,12,18,.2)");
    g.addColorStop(.55,"rgba(8,12,18,.12)");
    g.addColorStop(1,"rgba(8,12,18,0)");
    p.fillStyle = g;
    p.fillRect(0,0,32,32);
  });

  assets.shadow.treeCircle = makeTile((p)=>{
    p.clearRect(0,0,32,32);
    p.fillStyle = "rgba(7,11,16,.11)";
    p.beginPath();
    p.ellipse(18,24,8,4,0,0,Math.PI*2);
    p.fill();
    p.fillStyle = "rgba(7,11,16,.06)";
    p.beginPath();
    p.ellipse(19,24,10,5,0,0,Math.PI*2);
    p.fill();
  });

  assets.shadow.oval = makeTile((p)=>{
    p.clearRect(0,0,32,32);
    p.fillStyle = "rgba(7,11,16,.17)";
    p.beginPath();
    p.ellipse(18,25,8,4,0,0,Math.PI*2);
    p.fill();
    p.fillStyle = "rgba(7,11,16,.09)";
    p.beginPath();
    p.ellipse(19,25,10,5,0,0,Math.PI*2);
    p.fill();
  });

  assets.shadow.buildingRight = makeTile((p)=>{
    p.clearRect(0,0,32,32);
    const g = p.createLinearGradient(0,0,32,0);
    g.addColorStop(0,"rgba(8,12,18,0)");
    g.addColorStop(.55,"rgba(8,12,18,.08)");
    g.addColorStop(1,"rgba(8,12,18,.18)");
    p.fillStyle = g;
    p.fillRect(0,2,32,30);
  });

  assets.shadow.buildingBottom = makeTile((p)=>{
    p.clearRect(0,0,32,32);
    const g = p.createLinearGradient(0,0,0,32);
    g.addColorStop(0,"rgba(8,12,18,0)");
    g.addColorStop(.52,"rgba(8,12,18,.08)");
    g.addColorStop(1,"rgba(8,12,18,.2)");
    p.fillStyle = g;
    p.fillRect(0,0,32,32);
  });
}

function makePropSprites(){
  const sheet = document.createElement("canvas");
  sheet.width = 320;
  sheet.height = 32;
  const p = sheet.getContext("2d");
  p.imageSmoothingEnabled = false;
  p.clearRect(0,0,320,32);

  function cell(col, drawFn){
    p.save();
    p.translate(col*32,0);
    drawFn(p);
    p.restore();
  }

  cell(0,(q)=>{ // barrel
    q.fillStyle="#6f4d31"; q.fillRect(8,7,16,20);
    q.fillStyle="#8e6645"; q.fillRect(10,9,12,16);
    q.fillStyle="#3f2b1c"; q.fillRect(8,11,16,2); q.fillRect(8,20,16,2);
    q.fillStyle="rgba(255,225,184,.18)"; q.fillRect(11,10,3,12);
    q.fillStyle="rgba(0,0,0,.2)"; q.fillRect(8,27,16,1);
  });
  cell(1,(q)=>{ // crate
    q.fillStyle="#7a583a"; q.fillRect(7,9,18,16);
    q.fillStyle="#9b7852"; q.fillRect(8,10,16,14);
    q.fillStyle="#5e412a"; q.fillRect(7,9,18,1); q.fillRect(7,24,18,1);
    q.fillStyle="#6b4a2f"; q.fillRect(15,10,2,14); q.fillRect(8,16,16,2);
  });
  cell(2,(q)=>{ // sack
    q.fillStyle="#b59a72"; q.fillRect(9,10,14,15);
    q.fillStyle="#d2bc95"; q.fillRect(10,11,12,13);
    q.fillStyle="#8b7352"; q.fillRect(13,9,6,3); q.fillRect(14,12,4,1);
    q.fillStyle="rgba(0,0,0,.15)"; q.fillRect(9,25,14,1);
  });
  cell(3,(q)=>{ // lantern post
    q.fillStyle="#6a4c33"; q.fillRect(15,6,3,21);
    q.fillStyle="#8f6c48"; q.fillRect(14,6,5,2);
    q.fillStyle="#2b2622"; q.fillRect(11,9,11,8);
    q.fillStyle="#d7b769"; q.fillRect(13,11,7,5);
    q.fillStyle="rgba(255,232,152,.26)"; q.fillRect(12,10,9,1);
  });
  cell(4,(q)=>{ // sign post
    q.fillStyle="#664a31"; q.fillRect(15,10,3,17);
    q.fillStyle="#8a6445"; q.fillRect(8,8,16,7);
    q.fillStyle="#b28963"; q.fillRect(9,9,14,5);
    q.fillStyle="#5a3f2a"; q.fillRect(11,11,10,1);
  });
  cell(5,(q)=>{ // fence segment
    q.fillStyle="#7a593b"; q.fillRect(4,14,24,3); q.fillRect(4,19,24,2);
    q.fillStyle="#5d432b"; q.fillRect(7,9,3,16); q.fillRect(22,9,3,16);
    q.fillStyle="#ad8960"; q.fillRect(4,13,24,1); q.fillRect(4,18,24,1);
  });
  cell(6,(q)=>{ // bush cluster
    q.fillStyle="#4a6e3c"; q.fillRect(7,15,18,11);
    q.fillStyle="#5c8448"; q.fillRect(9,13,14,8); q.fillRect(6,17,7,7); q.fillRect(19,17,7,7);
    q.fillStyle="rgba(186,225,144,.2)"; q.fillRect(11,15,3,2); q.fillRect(17,16,3,2);
  });
  cell(7,(q)=>{ // grass tuft
    q.fillStyle="#5d8747"; q.fillRect(12,18,2,8); q.fillRect(16,16,2,10); q.fillRect(20,19,2,7);
    q.fillStyle="#84ad61"; q.fillRect(13,17,1,3); q.fillRect(17,15,1,3); q.fillRect(21,18,1,2);
  });
  cell(8,(q)=>{ // well
    q.fillStyle="#6f7782"; q.fillRect(7,14,18,12);
    q.fillStyle="#9099a4"; q.fillRect(9,15,14,10);
    q.fillStyle="#2f557f"; q.fillRect(12,18,8,5);
    q.fillStyle="#8b6f4d"; q.fillRect(9,8,2,8); q.fillRect(21,8,2,8); q.fillRect(10,8,12,2);
  });
  cell(9,(q)=>{ // stone pile
    q.fillStyle="#70756f"; q.fillRect(10,20,4,3); q.fillRect(14,18,5,4); q.fillRect(19,20,3,3);
    q.fillStyle="#8c928b"; q.fillRect(11,19,2,1); q.fillRect(15,17,2,1); q.fillRect(20,19,1,1);
  });

  const sheetImg = new Image();
  sheetImg.src = sheet.toDataURL("image/png");
  assets.props.sheet = sheetImg;

  const names = ["barrel","crate","sack","lanternPost","signPost","fenceSeg","bush","grassTuft","well","stonePile"];
  names.forEach((name, i)=>{
    assets.props.sprites[name] = makeTile((q)=>{ q.drawImage(sheet, i*32, 0, 32, 32, 0, 0, 32, 32); });
  });
}

function paintHumanoidSheet(colors, variant = "adventurer") {
  const size = 64;
  const c = document.createElement("canvas");
  c.width = size * 4;
  c.height = size * 4;
  const p = c.getContext("2d"); p.imageSmoothingEnabled=false;

  const dirs = ["down","left","right","up"];
  const gait = [0,1,0,-1];

  function drawFrame(baseX, baseY, dir, step){
    const px = 2;
    const ox = baseX + 10;
    const oy = baseY + 8;
    const elder = variant === "elder";
    const bob = step === 0 ? 0 : 1;
    const lean = elder ? 1 : 0;
    const armSwing = elder ? Math.round(step * .5) : -step;
    const outline = "rgba(8,12,18,.84)";
    const skinShadow = elder ? "#b59a7a" : "#d3b38f";

    const dot = (x,y,w=1,h=1,color=outline) => { p.fillStyle=color; p.fillRect(ox+x*px, oy+y*px, w*px, h*px); };

    if (elder) {
      dot(8,18+step,4,3,colors.boots);
      dot(14,19-step,4,3,colors.boots);
      dot(9,15,10,6,colors.tunicShade);
      dot(8,11+lean+bob,12,9,colors.tunic);
      dot(9,12+lean+bob,10,2,"rgba(255,255,255,.12)");
      dot(7,13+lean+bob,13,8,colors.cloak);
      dot(12,15+lean+bob,3,4,colors.tunicShade);
    } else {
      dot(9,19+step,3,3,colors.boots);
      dot(15,19-step,3,3,colors.boots);
      dot(10,16+step,2,4,colors.tunicShade);
      dot(16,16-step,2,4,colors.tunicShade);
      dot(8,11+bob,12,8,colors.tunic);
      dot(9,12+bob,10,2,"rgba(255,255,255,.16)");
      dot(7,13+bob,13,7,colors.cloak);
      dot(11,17+bob,6,2,colors.tunicShade);
    }

    if (dir==="left") {
      dot(7,13+armSwing+lean,2,4,skinShadow);
      dot(6,14+armSwing+lean,1,3,colors.tunicShade);
    } else if (dir==="right") {
      dot(19,13+armSwing+lean,2,4,skinShadow);
      dot(21,14+armSwing+lean,1,3,colors.tunicShade);
    } else {
      dot(7,13+armSwing+lean,2,4,skinShadow);
      dot(19,13-armSwing+lean,2,4,skinShadow);
      dot(6,14+armSwing+lean,1,3,colors.tunicShade);
      dot(21,14-armSwing+lean,1,3,colors.tunicShade);
    }

    if (dir==="left"){
      dot(9,5+bob+lean,8,6,colors.skin);
      dot(8,4+bob+lean,6,4,colors.hair);
      dot(12,9+bob+lean,3,2,skinShadow);
      dot(10,9+bob+lean,1,1,"#1b2632");
    } else if (dir==="right"){
      dot(11,5+bob+lean,8,6,colors.skin);
      dot(14,4+bob+lean,6,4,colors.hair);
      dot(13,9+bob+lean,3,2,skinShadow);
      dot(17,9+bob+lean,1,1,"#1b2632");
    } else if (dir==="up"){
      dot(10,5+bob+lean,8,6,colors.skin);
      dot(9,4+bob+lean,10,4,colors.hair);
      if (elder) dot(12,9+bob+lean,4,2,"#ebeef5");
    } else {
      dot(10,5+bob+lean,8,6,colors.skin);
      dot(9,4+bob+lean,10,3,colors.hair);
      dot(11,9+bob+lean,1,1,"#1b2632");
      dot(15,9+bob+lean,1,1,"#1b2632");
      if (elder) dot(12,10+bob+lean,4,1,"#ebeef5");
    }

    dot(8,5+bob+lean,1,6); dot(18,5+bob+lean,1,6); dot(9,4+bob+lean,9,1); dot(9,11+bob+lean,9,1);
    dot(7,12+bob+lean,1,8); dot(19,12+bob+lean,1,8); dot(8,20+lean,11,1);
  }

  dirs.forEach((d,row)=> gait.forEach((s,col)=> drawFrame(col*size,row*size,d,s)));
  const img = new Image(); img.src = c.toDataURL("image/png"); return img;
}

function paintWolfSheet() {
  const size = 64;
  const c = document.createElement("canvas"); c.width = size*4; c.height = size*4;
  const p = c.getContext("2d"); p.imageSmoothingEnabled=false;

  function frame(baseX,baseY,dir,step){
    const px = 2;
    const ox = baseX + 8;
    const oy = baseY + 11;
    const dot = (x,y,w=1,h=1,color="rgba(8,12,18,.82)") => { p.fillStyle=color; p.fillRect(ox+x*px, oy+y*px, w*px, h*px); };

    const fur = "#7a8590";
    const furShade = "#5c6672";
    const furHi = "#a2acb7";
    const muzzle = "#cac2b3";
    const nose = "#2a3340";

    if (dir==="left" || dir==="right") {
      const left = dir==="left";
      const headX = left ? 6 : 18;
      const neckX = left ? 10 : 14;
      const tailBaseX = left ? 22 : 7;

      dot(10,12,10,6,fur); dot(11,12,7,2,furHi); dot(10,15,10,3,furShade); dot(neckX,12,3,3,furShade); dot(11,17,8,1,furHi);
      dot(10,18+step,2,4,furShade); dot(16,18-step,2,4,furShade); dot(8,18-step,2,4,fur); dot(19,18+step,2,4,fur);
      dot(headX,9,5,5,fur); dot(headX+(left?0:1),8,1,2,furShade); dot(headX+(left?3:4),8,1,2,furShade);
      dot(headX+1,11,3,2,muzzle); dot(headX+(left?0:4),11,1,1,nose); dot(headX+(left?1:3),10,1,1,nose);
      dot(tailBaseX,13,3,2,furShade); dot(tailBaseX+(left?2:-2),12,2,1,furShade); dot(tailBaseX+(left?3:-3),11,1,1,furShade); dot(tailBaseX+(left?4:-4),10,1,1,furShade);
      dot(9,12,1,6); dot(20,12,1,6); dot(10,11,10,1); dot(10,18,10,1);
    } else {
      const back = dir==="up";
      dot(11,10,8,3,back ? furShade : furHi);
      dot(10,13,10,6,fur);
      dot(12,19+step,2,3,furShade); dot(16,19-step,2,3,furShade);
      dot(10,19-step,2,3,fur); dot(18,19+step,2,3,fur);
      dot(12,8,6,3,back ? furShade : muzzle);
      if (!back){ dot(13,9,1,1,nose); dot(15,9,1,1,nose); }
      dot(11,7,1,2,furShade); dot(17,7,1,2,furShade);
      dot(10,12,1,7); dot(19,12,1,7); dot(11,11,8,1); dot(11,19,8,1);
      if(back){ dot(9,14,1,2,furShade); dot(20,14,1,2,furShade); dot(14,20,2,1,furShade); }
    }
  }

  ["down","left","right","up"].forEach((dir,row)=>[0,1,0,-1].forEach((s,col)=>frame(col*size,row*size,dir,s)));
  const img = new Image(); img.src = c.toDataURL("image/png"); return img;
}

buildTerrainTiles();
makeBuildingTiles();
makeTreeSprites();
makeFenceTiles();
makeShadowTiles();
makePropSprites();
assets.sprites.player = paintHumanoidSheet({ skin:"#e4c8a2", hair:"#4f3a2c", tunic:"#5f7890", tunicShade:"#3f5265", cloak:"#c2c7cf", boots:"#4f3826" }, "adventurer");
assets.sprites.npc = paintHumanoidSheet({ skin:"#c9b093", hair:"#d9dde5", tunic:"#4d473f", tunicShade:"#322d28", cloak:"#262229", boots:"#2f2418" }, "elder");
assets.sprites.wolf = paintWolfSheet();

const world = { blocked:new Set(), trees:[], fences:[], buildings:[], roads:[], roadTiles:new Set(), props:[], zones:[], pondBlocked:new Set(), pondWater:new Set(), pondShore:new Set(), pondNearEdge:new Set() };
function blockRect(x,y,w,h){ for(let ix=x;ix<x+w;ix++)for(let iy=y;iy<y+h;iy++) world.blocked.add(keyOf(ix,iy)); }
const OVERWORLD_CAVE_ENTRY = Object.freeze({ x:30, y:13 });
const MIRROR_CAVE_EXIT = Object.freeze({ x:13, y:16 });
const MIRROR_CAVE_CHEST_TILE = Object.freeze({ x:13, y:2 });
const mirrorCave = {
  width:26,
  height:18,
  floor:new Set(),
  blocked:new Set(),
  walls:new Set(),
  spawn:{ x:13, y:16 },
  exit:{ ...MIRROR_CAVE_EXIT },
  chest:{ ...MIRROR_CAVE_CHEST_TILE, opened:false },
  cleared:false,
  returnTile:{ ...OVERWORLD_CAVE_ENTRY }
};
function carveMirrorCaveRoom(x,y,w,h){
  for(let tx=x;tx<x+w;tx++){
    for(let ty=y;ty<y+h;ty++){
      mirrorCave.floor.add(keyOf(tx,ty));
      mirrorCave.blocked.delete(keyOf(tx,ty));
    }
  }
}
for(let x=0;x<mirrorCave.width;x++) for(let y=0;y<mirrorCave.height;y++) mirrorCave.blocked.add(keyOf(x,y));
carveMirrorCaveRoom(11,14,5,3);
carveMirrorCaveRoom(12,11,3,3);
carveMirrorCaveRoom(12,8,3,3);
carveMirrorCaveRoom(11,5,5,3);
carveMirrorCaveRoom(8,5,3,2);
carveMirrorCaveRoom(13,3,2,2);
carveMirrorCaveRoom(9,2,9,3);
for(let x=0;x<mirrorCave.width;x++){
  for(let y=0;y<mirrorCave.height;y++){
    if(!mirrorCave.blocked.has(keyOf(x,y))) continue;
    const neighbors=[[1,0],[-1,0],[0,1],[0,-1]];
    if(neighbors.some(([dx,dy])=>!mirrorCave.blocked.has(keyOf(x+dx,y+dy)))) mirrorCave.walls.add(keyOf(x,y));
  }
}

world.roads.push(
  { x:6,y:11,w:26,h:2 },{ x:17,y:5,w:2,h:15 },{ x:10,y:8,w:2,h:8 },
  { x:24,y:7,w:2,h:8 },{ x:19,y:12,w:5,h:2 },{ x:26,y:12,w:3,h:2 }
);
world.roads.forEach(r=>{ for(let x=r.x;x<r.x+r.w;x++) for(let y=r.y;y<r.y+r.h;y++) world.roadTiles.add(keyOf(x,y)); });

world.buildings.push(
  { x:10,y:6,w:3,h:3,tileRows:[["roofL","roofC","roofR"],["window","wall","window"],["wall","door","wall"]] },
  { x:20,y:6,w:4,h:3,tileRows:[["roofL","roofC","roofC","roofR"],["window","wall","wall","window"],["wall","wall","door","wall"]] },
  { x:12,y:14,w:4,h:3,tileRows:[["roofL","roofC","roofC","roofR"],["window","wall","window","wall"],["wall","door","wall","wall"]] }
);
world.buildings.forEach(b=>blockRect(b.x,b.y,b.w,b.h));

const pond={x:22,y:13,w:7,h:5,cx:25.5,cy:15.5};
for(let x=pond.x;x<pond.x+pond.w;x++){
  for(let y=pond.y;y<pond.y+pond.h;y++){
    const dx=(x+.5-pond.cx)/(pond.w/2), dy=(y+.5-pond.cy)/(pond.h/2);
    const d=dx*dx+dy*dy, wob=(rng(x,y,17)-.5)*.18, lim=.9+wob;
    if(d<=lim){ world.pondWater.add(keyOf(x,y)); world.pondBlocked.add(keyOf(x,y)); }
    if(d>=lim-.16&&d<=lim+.16) world.pondShore.add(keyOf(x,y));
    if(d>=lim-.22&&d<=lim+.05) world.pondNearEdge.add(keyOf(x,y));
  }
}

for(let x=29;x<=35;x++){ world.fences.push({x,y:6},{x,y:10}); }
for(let y=7;y<=9;y++){ world.fences.push({x:29,y},{x:35,y}); }
world.fences.forEach(f=>world.blocked.add(keyOf(f.x,f.y)));

world.props.push(
  {x:9,y:8,type:"crate"},{x:9,y:9,type:"barrel"},{x:13,y:8,type:"crate"},{x:13,y:9,type:"bush"},{x:10,y:9,type:"fenceSeg"},
  {x:19,y:8,type:"crate"},{x:24,y:8,type:"sack"},{x:24,y:9,type:"barrel"},{x:19,y:9,type:"bush"},
  {x:11,y:17,type:"crate"},{x:16,y:17,type:"barrel"},{x:11,y:16,type:"fenceSeg"},{x:16,y:16,type:"bush"},{x:15,y:17,type:"sack"},
  {x:16,y:10,type:"signPost"},{x:25,y:11,type:"signPost"},
  {x:8,y:10,type:"lanternPost"},{x:28,y:10,type:"lanternPost"},
  {x:21,y:14,type:"stonePile"},{x:21,y:16,type:"stonePile"},{x:29,y:15,type:"stonePile"},
  {x:21,y:13,type:"grassTuft"},{x:29,y:17,type:"grassTuft"},{x:24,y:18,type:"grassTuft"},
  {x:5,y:12,type:"bush"},{x:32,y:12,type:"bush"},{x:6,y:11,type:"fenceSeg"},{x:31,y:11,type:"fenceSeg"},
  {x:18,y:11,type:"well"}
);
world.props.push({x:OVERWORLD_CAVE_ENTRY.x,y:OVERWORLD_CAVE_ENTRY.y,type:"stonePile"});

const treeData = [[1,2,"a"],[2,2,"b"],[3,3,"a"],[2,5,"c"],[1,6,"a"],[3,7,"b"],[2,9,"a"],[1,11,"c"],[3,12,"a"],[2,14,"b"],[1,17,"a"],[2,19,"b"],[3,21,"a"],[1,22,"c"],[4,23,"a"],[2,1,"a"],[4,2,"c"],[7,1,"b"],[10,2,"a"],[13,2,"c"],[27,2,"a"],[30,1,"b"],[33,2,"a"],[35,1,"c"],[37,2,"a"],[36,2,"a"],[35,4,"b"],[37,5,"a"],[36,7,"c"],[35,9,"a"],[36,11,"b"],[37,13,"a"],[35,15,"c"],[36,17,"a"],[37,19,"b"],[35,21,"a"],[36,23,"c"],[34,22,"a"],[4,22,"b"],[6,23,"a"],[9,22,"c"],[12,23,"a"],[15,22,"b"],[24,23,"a"],[27,22,"c"],[30,23,"a"],[33,22,"b"],[5,5,"a"],[6,8,"b"],[7,19,"a"],[9,4,"c"],[31,5,"a"],[32,8,"b"],[31,19,"a"],[29,21,"c"],[21,15,"a"],[22,18,"c"],[29,16,"b"],[28,19,"c"]];
treeData.forEach(([x,y,type])=>{ world.trees.push({x,y,type,seed:rng(x,y,91)}); world.blocked.add(keyOf(x,y)); });

world.zones.push(
  {name:"Hearthvale Square",x:9,y:7,w:18,h:11},
  {name:"Mirror Pond",x:21,y:12,w:10,h:8},
  {name:"Eastern Woods",x:27,y:3,w:11,h:19},
  {name:"West Lane",x:0,y:7,w:10,h:12}
);

const player={x:18,y:11,px:18*TILE,py:11*TILE,targetX:18,targetY:11,hp:50,maxHp:50,xp:0,coins:0,inventory:[],equipment:{weapon:"rusty_sword",armor:null,trinket:null},moving:false,facing:"down",speed:180,attackUntil:0,hitUntil:0,hitFlickerUntil:0,attackLungeX:0,attackLungeY:0,recoilX:0,recoilY:0};
const npc={x:21,y:12,name:"Edrin Vale",facing:"down"};
const hunterNpc={x:26,y:9,name:"Hunter Garran",displayLabel:"Hunter Garran",facing:"down"};
const vendorNpc={x:16,y:12,name:"Merchant Rowan",displayLabel:"Merchant Rowan",facing:"down"};
const WOLF_SPAWNS=[{id:1,x:32,y:14},{id:2,x:33,y:17}];
const BANDIT_SPAWNS=[{id:1,x:34,y:15}];
const MIRROR_CAVE_WOLF_SPAWNS=[
  {id:101,x:13,y:13},
  {id:102,x:12,y:9},
  {id:103,x:11,y:6},
  {id:104,x:9,y:3}
];
function createWolf(spawn){
  return {kind:"wolf",id:spawn.id,x:spawn.x,y:spawn.y,px:spawn.x*TILE,py:spawn.y*TILE,targetX:spawn.x,targetY:spawn.y,hp:22,maxHp:22,homeX:spawn.x,homeY:spawn.y,roam:3,speed:110,facing:"left",attackUntil:0,hitUntil:0,hitFlickerUntil:0,attackLungeX:0,attackLungeY:0,recoilX:0,recoilY:0,moving:false,defeated:false};
}
function createBandit(spawn){
  return {kind:"bandit",id:spawn.id,x:spawn.x,y:spawn.y,px:spawn.x*TILE,py:spawn.y*TILE,targetX:spawn.x,targetY:spawn.y,hp:35,maxHp:35,homeX:spawn.x,homeY:spawn.y,roam:2,speed:95,facing:"left",attackUntil:0,hitUntil:0,hitFlickerUntil:0,attackLungeX:0,attackLungeY:0,recoilX:0,recoilY:0,moving:false,defeated:false};
}
const wolves=WOLF_SPAWNS.map(createWolf);
const bandits=BANDIT_SPAWNS.map(createBandit);
const mirrorCaveWolves=MIRROR_CAVE_WOLF_SPAWNS.map(createWolf);
const hostiles=[...wolves, ...bandits, ...mirrorCaveWolves];
let isInMirrorCave=false;
let transitionState={ active:false, start:0, duration:0, switched:false, onSwitch:null };

let lastPlayerAttack=0,hitStopUntil=0,lastNoTargetLogAt=0;
const lastWolfDecisionAt={};
const lastWolfAttackAt={};
const lastBanditDecisionAt={};
const lastBanditAttackAt={};
const wolfRespawnAtById={};
const banditRespawnAtById={};
let missNoticeArmed=true;
const PLAYER_ATTACK_RANGE=1;
const WOLF_ATTACK_COOLDOWN_MS=1800;
const BANDIT_ATTACK_COOLDOWN_MS=2800;
const WOLF_RESPAWN_MS=15000;
const BANDIT_RESPAWN_MS=18000;
const BASE_PLAYER_DAMAGE=6;

function randomInt(min,max){ return min + Math.floor(Math.random() * (max-min+1)); }
function getItemDefinition(itemId){ return ITEM_REGISTRY[itemId] || null; }
function normalizeInventoryEntry(entry){
  if(!entry || typeof entry.itemId!=="string" || !Number.isFinite(entry.quantity)) return null;
  const definition=getItemDefinition(entry.itemId);
  if(!definition) return null;
  const quantity=Math.max(0,Math.floor(entry.quantity));
  if(quantity<=0) return null;
  return { itemId:definition.id, quantity };
}
function normalizeInventory(entries){
  const output=[];
  if(!Array.isArray(entries)) return output;
  entries.forEach((entry)=>{
    const normalized=normalizeInventoryEntry(entry);
    if(!normalized) return;
    addItemToInventory(normalized.itemId, normalized.quantity, output);
  });
  return output;
}
function onInventoryChanged(reason){
  if(typeof questSystem!=="undefined" && questSystem) questSystem.refreshAllItemProgress();
  if(typeof updateSidebar==="function") updateSidebar();
  if(typeof saveGame==="function") saveGame(reason || "inventory_update");
}
function addItemToInventory(itemId, amount, targetInventory=player.inventory){
  const definition=getItemDefinition(itemId);
  if(!definition || !Number.isFinite(amount)) return 0;
  const quantity=Math.max(0,Math.floor(amount));
  if(quantity<=0) return 0;
  if(definition.stackable){
    const existing=targetInventory.find((entry)=>entry.itemId===itemId);
    if(existing){
      existing.quantity += quantity;
      if(targetInventory===player.inventory) onInventoryChanged("inventory_add");
      return quantity;
    }
  }
  targetInventory.push({ itemId, quantity });
  if(targetInventory===player.inventory) onInventoryChanged("inventory_add");
  return quantity;
}
function getItemQuantity(itemId){
  return player.inventory
    .filter((entry)=>entry.itemId===itemId)
    .reduce((sum,entry)=>sum + entry.quantity, 0);
}
function getEquippedItem(slotName){
  const itemId=player.equipment?.[slotName];
  return itemId ? getItemDefinition(itemId) : null;
}
function getEquippedWeaponBonus(){
  const weapon=getEquippedItem("weapon");
  if(!weapon || weapon.type!=="weapon") return 0;
  return Number.isFinite(weapon.attackBonus) ? weapon.attackBonus : 0;
}
function getEquippedDefenseBonus(){
  const armor=getEquippedItem("armor");
  if(!armor || armor.type!=="armor") return 0;
  return Number.isFinite(armor.defenseBonus) ? armor.defenseBonus : 0;
}
function ensureStarterEquipment(){
  if(getItemQuantity("rusty_sword")<=0) addItemToInventory("rusty_sword", 1);
  const currentWeapon=getEquippedItem("weapon");
  if(!currentWeapon || currentWeapon.type!=="weapon") player.equipment.weapon="rusty_sword";
  if(!("armor" in player.equipment)) player.equipment.armor=null;
  if(!("trinket" in player.equipment)) player.equipment.trinket=null;
}
function equipWeapon(itemId){
  const item=getItemDefinition(itemId);
  if(!item || item.type!=="weapon") return false;
  if(getItemQuantity(itemId)<=0) return false;
  const previous=getEquippedItem("weapon");
  player.equipment.weapon=itemId;
  if(previous && previous.id!==itemId) log("Equipped " + item.name + ". Replaced " + previous.name + ".");
  else log("Equipped " + item.name + ".");
  return true;
}
function equipArmor(itemId){
  const item=getItemDefinition(itemId);
  if(!item || item.type!=="armor") return false;
  if(getItemQuantity(itemId)<=0) return false;
  const previous=getEquippedItem("armor");
  player.equipment.armor=itemId;
  if(previous && previous.id!==itemId) log("Equipped " + item.name + ". Replaced " + previous.name + ".");
  else log("Equipped " + item.name + ".");
  return true;
}
function unequipSlot(slotName){
  if(!["weapon","armor","trinket"].includes(slotName)) return false;
  if(slotName==="weapon") return false;
  const currentItem=getEquippedItem(slotName);
  if(!currentItem) return false;
  player.equipment[slotName]=null;
  log("Removed " + currentItem.name + ".");
  return true;
}
function applyIncomingDamage(rawDamage){
  const defense=Math.max(0, getEquippedDefenseBonus());
  const reducedDamage=Math.max(1, Math.floor(rawDamage)-defense);
  player.hp=Math.max(0, player.hp-reducedDamage);
  return reducedDamage;
}
function removeItemFromInventory(itemId, amount){
  if(!Number.isFinite(amount)) return 0;
  let remaining=Math.max(0,Math.floor(amount));
  if(remaining<=0) return 0;
  let removed=0;
  for(let i=player.inventory.length-1; i>=0 && remaining>0; i--){
    const entry=player.inventory[i];
    if(entry.itemId!==itemId) continue;
    const take=Math.min(entry.quantity, remaining);
    entry.quantity-=take;
    remaining-=take;
    removed+=take;
    if(entry.quantity<=0) player.inventory.splice(i,1);
  }
  if(removed>0) onInventoryChanged("inventory_remove");
  return removed;
}
function rollLootFromTable(lootTable){
  const drops=[];
  lootTable.forEach((roll)=>{
    const definition=getItemDefinition(roll.itemId);
    if(!definition) return;
    if(Math.random()>roll.chance) return;
    const amount=randomInt(roll.min, roll.max);
    if(amount>0) drops.push({ itemId:roll.itemId, quantity:amount });
  });
  return drops;
}
function rollWolfLoot(){
  return rollLootFromTable(WOLF_LOOT_TABLE);
}
function rollBanditLoot(){
  return rollLootFromTable(BANDIT_LOOT_TABLE);
}
function formatDropText(drops){
  return drops.map((drop)=>{
    const item=getItemDefinition(drop.itemId);
    return (item?.name || drop.itemId) + " x" + drop.quantity;
  }).join(", ");
}
function isVendorOpen(){ return vendorPanel.style.display==="block"; }
function closeVendorMenu(){ vendorPanel.style.display="none"; }
function canSellItem(item){
  if(!item) return false;
  const equippableSlot=item.type==="weapon"
    ? "weapon"
    : (item.type==="armor"
      ? "armor"
      : (item.type==="trinket" ? "trinket" : null));
  if(!equippableSlot) return true;
  const total=getItemQuantity(item.id);
  const equipped=player.equipment[equippableSlot]===item.id;
  return !equipped || total>1;
}
function getFirstUsableHealingItem(){
  for(const entry of player.inventory){
    if(!entry || entry.quantity<=0) continue;
    const item=getItemDefinition(entry.itemId);
    if(!item || item.type!=="consumable") continue;
    const healAmount=Number.isFinite(item.healAmount) ? Math.floor(item.healAmount) : 0;
    if(healAmount<=0) continue;
    return item;
  }
  return null;
}
function useHealingConsumable(){
  if(player.hp>=player.maxHp){
    log("You are already at full health.");
    return false;
  }
  const item=getFirstUsableHealingItem();
  if(!item){
    log("You have no healing consumables.");
    return false;
  }
  const removed=removeItemFromInventory(item.id, 1);
  if(removed<=0) return false;
  const healAmount=Math.max(0, Math.floor(Number.isFinite(item.healAmount) ? item.healAmount : 0));
  const hpBefore=player.hp;
  player.hp=Math.min(player.maxHp, player.hp + healAmount);
  const restored=player.hp-hpBefore;
  log("Used " + item.name + ". Restored " + restored + " HP.");
  saveGame("consume_item");
  return true;
}
function getVendorBuyCost(item){
  if(!item) return 0;
  if(item.id==="leather_armor") return 25;
  return Math.max(0, Math.floor(Number.isFinite(item.value) ? item.value : 0));
}
function renderVendorMenu(){
  const buyRows = VENDOR_BUY_INVENTORY.map((itemId)=>{
    const item=getItemDefinition(itemId);
    if(!item) return "";
    const cost=getVendorBuyCost(item);
    const canBuy=player.coins>=cost;
    return "<div class=\"vendor-item\">" +
      "<div>" + item.name + "</div>" +
      "<div class=\"vendor-pill\">Cost: " + cost + "</div>" +
      "<div class=\"vendor-pill\">Owned: " + getItemQuantity(item.id) + "</div>" +
      "<button type=\"button\" class=\"vendor-btn\" data-buy-item=\"" + item.id + "\"" + (canBuy ? "" : " disabled") + ">" + (canBuy ? "Buy" : "Need coins") + "</button>" +
    "</div>";
  }).join("");
  const sellRows = player.inventory.map((entry)=>{
    const item=getItemDefinition(entry.itemId);
    if(!item) return "";
    const sellValue=Math.max(0, Math.floor(Number.isFinite(item.value) ? item.value : 0));
    const canSell=canSellItem(item);
    const buttonLabel=canSell ? "Sell" : "Equipped";
    const disabledAttr=canSell ? "" : " disabled";
    return "<div class=\"vendor-item\">" +
      "<div>" + item.name + "</div>" +
      "<div class=\"vendor-pill\">Qty: " + entry.quantity + "</div>" +
      "<div class=\"vendor-pill\">Value: " + sellValue + "</div>" +
      "<button type=\"button\" class=\"vendor-btn\" data-sell-item=\"" + item.id + "\"" + disabledAttr + ">" + buttonLabel + "</button>" +
    "</div>";
  }).join("");
  vendorList.innerHTML =
    "<div class=\"questTitle\">BUY</div>" +
    (buyRows || "<div class=\"muted\">No items available.</div>") +
    "<div class=\"questTitle\" style=\"margin-top:8px;\">SELL</div>" +
    (sellRows || "<div class=\"muted\">Inventory is empty.</div>");
  bindVendorButtons();
}
function handleVendorActionFromTarget(target){
  if(!target) return false;
  const buyButton=target.closest?.("button[data-buy-item]");
  const buyItemId=buyButton?.dataset?.buyItem;
  if(buyItemId){
    return buyOneItemFromVendor(buyItemId);
  }
  const sellButton=target.closest?.("button[data-sell-item]");
  const sellItemId=sellButton?.dataset?.sellItem;
  if(!sellItemId) return false;
  return sellOneItemToVendor(sellItemId);
}
function bindVendorButtons(){
  const buyButtons=vendorList.querySelectorAll("button[data-buy-item]");
  buyButtons.forEach((button)=>{
    button.onclick=(event)=>{
      event.preventDefault();
      event.stopPropagation();
      handleVendorActionFromTarget(event.currentTarget);
    };
  });
  const sellButtons=vendorList.querySelectorAll("button[data-sell-item]");
  sellButtons.forEach((button)=>{
    button.onclick=(event)=>{
      event.preventDefault();
      event.stopPropagation();
      handleVendorActionFromTarget(event.currentTarget);
    };
  });
}
function openVendorMenu(){
  if(dialogueSystem.activeSession) dialogueSystem.close();
  renderVendorMenu();
  vendorPanel.style.display="block";
}
function sellOneItemToVendor(itemId){
  const item=getItemDefinition(itemId);
  if(!item) return false;
  if(getItemQuantity(itemId)<=0) return false;
  if(!canSellItem(item)) return false;
  const removed=removeItemFromInventory(itemId, 1);
  if(removed<=0) return false;
  const sellValue=Math.max(0, Math.floor(Number.isFinite(item.value) ? item.value : 0));
  player.coins += sellValue;
  log("Sold " + item.name + " for " + sellValue + " coin" + (sellValue===1 ? "" : "s") + ".");
  renderVendorMenu();
  if(player.inventory.length===0) closeVendorMenu();
  saveGame("vendor_sale");
  return true;
}
function buyOneItemFromVendor(itemId){
  const item=getItemDefinition(itemId);
  if(!item) return false;
  if(!VENDOR_BUY_INVENTORY.includes(item.id)) return false;
  const cost=getVendorBuyCost(item);
  if(player.coins<cost){
    log("Not enough coins to buy " + item.name + ".");
    return false;
  }
  player.coins-=cost;
  addItemToInventory(item.id, 1);
  const ownedCount=getItemQuantity(item.id);
  log(item.name + " purchased.");
  log("Coins after purchase: " + player.coins + ".");
  log("Inventory update: " + item.name + " owned: " + ownedCount + ".");
  log("Bought " + item.name + " for " + cost + " coin" + (cost===1 ? "" : "s") + ".");
  renderVendorMenu();
  saveGame("vendor_purchase");
  return true;
}

const QuestState = Object.freeze({ NOT_STARTED:"Not Started", ACTIVE:"Active", READY_TO_TURN_IN:"Ready To Turn In", COMPLETED:"Completed" });

class EventTriggerSystem {
  constructor(){ this.handlers=new Map(); this.zoneWatchers=[]; this.lastZone=""; }
  on(eventName, handler){ if(!this.handlers.has(eventName)) this.handlers.set(eventName, []); this.handlers.get(eventName).push(handler); }
  emit(eventName, payload={}){ const handlers=this.handlers.get(eventName)||[]; handlers.forEach((handler)=>handler(payload)); }
  registerZoneTrigger(zoneName, eventName){ this.zoneWatchers.push({zoneName,eventName}); }
  update(zoneName){
    if(zoneName===this.lastZone) return;
    this.lastZone=zoneName;
    this.zoneWatchers.forEach((watcher)=>{ if(watcher.zoneName===zoneName) this.emit(watcher.eventName,{zone:zoneName}); });
  }
}

class QuestStateSystem {
  constructor(definitions, events){
    this.events=events;
    this.quests=new Map(definitions.map((q)=>[q.id,{
      ...q,
      questId:q.questId || q.id,
      title:q.title || q.name,
      state:QuestState.NOT_STARTED,
      status:QuestState.NOT_STARTED,
      progress:"none",
      objectives:this.normalizeObjectives(q.objectives||[]),
      itemProgress:{}
    }]));
    definitions.forEach((quest)=>{
      (quest.startEvents||[]).forEach((eventName)=>this.events.on(eventName,()=>this.activateQuest(quest.id)));
      (quest.completionEvents||[]).forEach((eventName)=>this.events.on(eventName,()=>this.completeQuest(quest.id)));
    });
  }
  activateQuest(questId){
    const quest=this.quests.get(questId); if(!quest||quest.state!==QuestState.NOT_STARTED) return;
    quest.state=QuestState.ACTIVE;
    quest.status=quest.state;
    quest.progress=quest.initialProgress || "active";
    quest.objectives=this.normalizeObjectives(quest.objectives||[]);
    log("Quest started: " + (quest.title || quest.name));
    this.events.emit("quest:state-changed",{questId,state:quest.state});
  }
  updateProgress(questId, progressId){
    const quest=this.quests.get(questId); if(!quest||quest.state!==QuestState.ACTIVE) return;
    if(quest.progress===progressId) return;
    quest.progress=progressId;
    this.events.emit("quest:progressed",{questId,progress:progressId});
    this.events.emit("quest:state-changed",{questId,state:quest.state,progress:progressId});
  }
  completeQuest(questId){
    const quest=this.quests.get(questId); if(!quest||(quest.state!==QuestState.ACTIVE && quest.state!==QuestState.READY_TO_TURN_IN)) return;
    const turnInObjective=this.getObjective(questId, "return_hunter");
    if(turnInObjective && !turnInObjective.completed) this.completeObjective(questId, "return_hunter");
    quest.state=QuestState.COMPLETED;
    quest.status=quest.state;
    quest.progress="completed";
    log("Quest complete: " + (quest.title || quest.name));
    const rewardXp=Math.max(0, Math.floor(Number.isFinite(quest.rewards?.xp) ? quest.rewards.xp : 0));
    const rewardCoins=Math.max(0, Math.floor(Number.isFinite(quest.rewards?.coins) ? quest.rewards.coins : 0));
    const rewardItems=Array.isArray(quest.rewards?.items) ? quest.rewards.items : [];
    if(rewardXp>0) player.xp += rewardXp;
    if(rewardCoins>0) player.coins += rewardCoins;
    rewardItems.forEach((reward)=>{
      if(!reward || typeof reward.itemId!=="string") return;
      const count=Math.max(1, Math.floor(Number.isFinite(reward.count) ? reward.count : 1));
      addItemToInventory(reward.itemId, count);
    });
    if(rewardXp>0 || rewardCoins>0) log("Rewards: +" + rewardXp + " XP, +" + rewardCoins + " Coins.");
    if(rewardItems.length){
      const text=rewardItems.map((reward)=>{
        const itemDef=getItemDefinition(reward.itemId);
        const itemName=itemDef?.name || reward.itemId;
        const count=Math.max(1, Math.floor(Number.isFinite(reward.count) ? reward.count : 1));
        return itemName + " x" + count;
      }).join(", ");
      log("Item Rewards: " + text + ".");
    }
    if(quest.id==="hunters_request") log("Hunter's Request completed.");
    log("Quest Completed.");
    this.events.emit("quest:state-changed",{questId,state:quest.state});
    this.events.emit("quest:completed:" + questId,{questId});
  }
  getQuest(questId){ return this.quests.get(questId) || null; }
  normalizeObjectives(objectives){
    if(!Array.isArray(objectives)) return [];
    return objectives.map((objective)=>({
      ...objective,
      requiredAmount:Math.max(1, Math.floor(Number.isFinite(objective?.requiredAmount) ? objective.requiredAmount : 1)),
      currentAmount:Math.max(0, Math.floor(Number.isFinite(objective?.currentAmount) ? objective.currentAmount : 0)),
      completed:Boolean(objective?.completed)
    })).map((objective)=>({
      ...objective,
      currentAmount:Math.min(objective.requiredAmount, objective.currentAmount),
      completed:Boolean(objective.completed || objective.currentAmount>=objective.requiredAmount)
    }));
  }
  getObjective(questId, objectiveId){
    const quest=this.getQuest(questId);
    if(!quest || !Array.isArray(quest.objectives)) return null;
    return quest.objectives.find((objective)=>objective.id===objectiveId) || null;
  }
  isObjectiveLocked(questId, objectiveId){
    if(objectiveId!=="return_hunter") return false;
    const quest=this.getQuest(questId);
    if(!quest) return true;
    return (quest.objectives||[]).some((objective)=>objective.id!=="return_hunter" && !objective.completed);
  }
  incrementObjective(questId, objectiveId, amount=1){
    const quest=this.getQuest(questId);
    if(!quest || quest.state!==QuestState.ACTIVE) return false;
    const objective=this.getObjective(questId, objectiveId);
    if(!objective || objective.completed || this.isObjectiveLocked(questId, objectiveId)) return false;
    const step=Math.max(1, Math.floor(Number.isFinite(amount) ? amount : 1));
    const prev=objective.currentAmount;
    objective.currentAmount=Math.min(objective.requiredAmount, objective.currentAmount + step);
    if(objective.currentAmount===prev) return false;
    if(objective.summaryLabel){
      log("Objective Updated: " + objective.summaryLabel + " (" + objective.currentAmount + "/" + objective.requiredAmount + ")");
    }
    if(objective.currentAmount>=objective.requiredAmount) this.completeObjective(questId, objectiveId);
    else this.events.emit("quest:state-changed",{questId,state:quest.state});
    return true;
  }
  completeObjective(questId, objectiveId){
    const quest=this.getQuest(questId);
    if(!quest || (quest.state!==QuestState.ACTIVE && quest.state!==QuestState.READY_TO_TURN_IN)) return false;
    const objective=this.getObjective(questId, objectiveId);
    if(!objective || objective.completed || this.isObjectiveLocked(questId, objectiveId)) return false;
    objective.currentAmount=objective.requiredAmount;
    objective.completed=true;
    this.events.emit("quest:objective-completed",{questId,objectiveId});
    this.evaluateQuestReadiness(questId);
    this.events.emit("quest:state-changed",{questId,state:quest.state});
    return true;
  }
  evaluateQuestReadiness(questId){
    const quest=this.getQuest(questId);
    if(!quest || !Array.isArray(quest.objectives)) return false;
    const allNonTurnInComplete=quest.objectives.every((objective)=>objective.id==="return_hunter" || objective.completed);
    if(allNonTurnInComplete && quest.state===QuestState.ACTIVE){
      quest.state=QuestState.READY_TO_TURN_IN;
      quest.status=quest.state;
      log((quest.title || quest.name) + " is ready to turn in.");
      return true;
    }
    if(!allNonTurnInComplete && quest.state===QuestState.READY_TO_TURN_IN){
      quest.state=QuestState.ACTIVE;
      quest.status=quest.state;
      return true;
    }
    return false;
  }
  isReadyToTurnIn(questId){
    const quest=this.getQuest(questId);
    return Boolean(quest && quest.state===QuestState.READY_TO_TURN_IN);
  }
  tryTurnInQuest(questId){
    const quest=this.getQuest(questId);
    if(!quest || quest.state!==QuestState.READY_TO_TURN_IN) return false;
    return this.completeQuest(questId), true;
  }
  refreshAllItemProgress(){ return false; }
  serializeState(){
    const states=[];
    for(const quest of this.quests.values()) states.push({
      id:quest.id,
      state:quest.state,
      status:quest.state,
      progress:quest.progress,
      objectives:(quest.objectives||[]).map((objective)=>({
        id:objective.id,
        currentAmount:objective.currentAmount,
        completed:objective.completed
      })),
      itemProgress:{...(quest.itemProgress||{})}
    });
    return states;
  }
  getCompletedQuestIds(){
    const ids=[];
    for(const quest of this.quests.values()) if(quest.state===QuestState.COMPLETED) ids.push(quest.id);
    return ids;
  }
  getActiveQuestIds(){
    const ids=[];
    for(const quest of this.quests.values()) if(quest.state===QuestState.ACTIVE || quest.state===QuestState.READY_TO_TURN_IN) ids.push(quest.id);
    return ids;
  }
  applyState(stateEntries){
    if(!Array.isArray(stateEntries)) return;
    const validStates=new Set(Object.values(QuestState));
    stateEntries.forEach((entry)=>{
      if(!entry || typeof entry.id!=="string") return;
      const quest=this.quests.get(entry.id);
      if(!quest) return;
      if(typeof entry.state==="string" && validStates.has(entry.state)) quest.state=entry.state;
      if(typeof entry.status==="string" && validStates.has(entry.status)) quest.state=entry.status;
      if(typeof entry.progress==="string") quest.progress=entry.progress;
      if(Array.isArray(entry.objectives)){
        entry.objectives.forEach((savedObjective)=>{
          const objective=quest.objectives.find((candidate)=>candidate.id===savedObjective.id);
          if(!objective) return;
          if(Number.isFinite(savedObjective.currentAmount)){
            objective.currentAmount=Math.max(0,Math.min(objective.requiredAmount,Math.floor(savedObjective.currentAmount)));
          }
          if(typeof savedObjective.completed==="boolean") objective.completed=savedObjective.completed;
          if(objective.currentAmount>=objective.requiredAmount) objective.completed=true;
        });
      }
      if(entry.itemProgress && typeof entry.itemProgress==="object") quest.itemProgress={...entry.itemProgress};
      quest.status=quest.state;
      this.evaluateQuestReadiness(quest.id);
    });
  }
}

class DialogueFramework {
  constructor(data, events){
    this.data=data;
    this.events=events;
    this.activeSession=null;
  }
  getHunterObjectiveSummaryLines(){
    const hunterQuest=questSystem.getQuest("hunters_request");
    if(!hunterQuest) return [];
    const objectiveLines=(hunterQuest.objectives||[]).map((objective)=>{
      const hasCounter=objective.requiredAmount>1;
      const counter=hasCounter ? (" " + objective.currentAmount + "/" + objective.requiredAmount) : "";
      const marker=objective.completed ? "✔" : "•";
      return marker + " " + objective.label + counter;
    });
    return objectiveLines.length ? ["", ...objectiveLines] : [];
  }
  getDisplayLines(node){
    const baseLines=Array.isArray(node?.lines) ? node.lines : [];
    if(!this.activeSession) return baseLines;
    if(this.activeSession.characterId==="hunter_garran" && this.activeSession.nodeId==="hunters_request_active"){
      return [...baseLines, ...this.getHunterObjectiveSummaryLines()];
    }
    return baseLines;
  }
  evaluateCondition(condition){
    if(!condition || typeof condition!=="object") return false;
    if(typeof condition.questId==="string"){
      const quest=questSystem.getQuest(condition.questId);
      if(!quest) return false;
      if(typeof condition.state==="string" && quest.state!==condition.state) return false;
      if(typeof condition.progress==="string" && quest.progress!==condition.progress) return false;
    }
    if(typeof condition.objectiveId==="string"){
      const [questId, objectiveId]=condition.objectiveId.split(":");
      if(!questId || !objectiveId) return false;
      const objective=questSystem.getObjective(questId, objectiveId);
      const needsCompleted=typeof condition.completed==="boolean" ? condition.completed : true;
      if(!objective || objective.completed!==needsCompleted) return false;
    }
    if(typeof condition.itemId==="string"){
      const minimum=Number.isFinite(condition.minimumOwned) ? Math.max(0, Math.floor(condition.minimumOwned)) : 1;
      if(getItemQuantity(condition.itemId)<minimum) return false;
    }
    return true;
  }
  getRootNodeId(characterId, char){
    const conditionalRoots=Array.isArray(char?.rootByCondition) ? char.rootByCondition : [];
    for(const conditionalRoot of conditionalRoots){
      if(!this.evaluateCondition(conditionalRoot?.if)) continue;
      if(typeof conditionalRoot?.next==="string" && conditionalRoot.next) return conditionalRoot.next;
    }
    return char?.root;
  }
  start(characterId){
    const char=this.data.characters?.[characterId];
    if(!char) return false;
    const root=this.getRootNodeId(characterId, char);
    this.activeSession={characterId,nodeId:root,lineIndex:0,pendingChoices:null};
    this.render();
    this.events.emit("dialogue:started:" + characterId,{characterId,nodeId:root});
    return true;
  }
  getNode(){
    if(!this.activeSession) return null;
    const char=this.data.characters?.[this.activeSession.characterId];
    return char?.nodes?.[this.activeSession.nodeId] || null;
  }
  advance(){
    const node=this.getNode();
    if(!node || !this.activeSession) return;
    if(this.activeSession.pendingChoices) return;
    const displayLines=this.getDisplayLines(node);
    this.activeSession.lineIndex += 1;
    if(this.activeSession.lineIndex < displayLines.length){ this.render(); return; }
    if(node.choices?.length){ this.activeSession.pendingChoices=node.choices; this.render(); return; }
    (node.onCompleteEvents||[]).forEach((eventName)=>this.events.emit(eventName,{characterId:this.activeSession.characterId,nodeId:this.activeSession.nodeId}));
    if(node.next && node.next!=="end"){
      this.activeSession.nodeId=node.next;
      this.activeSession.lineIndex=0;
      this.activeSession.pendingChoices=null;
      this.render();
      return;
    }
    this.close();
  }
  choose(index){
    if(!this.activeSession?.pendingChoices) return;
    const choice=this.activeSession.pendingChoices[index];
    if(!choice) return;
    if(choice.event) this.events.emit(choice.event,{characterId:this.activeSession.characterId});
    this.activeSession.nodeId=choice.next;
    this.activeSession.lineIndex=0;
    this.activeSession.pendingChoices=null;
    this.render();
  }
  close(){
    this.activeSession=null;
    dialogueChoices.innerHTML="";
    dialogue.style.display="none";
  }
  render(){
    const session=this.activeSession;
    const node=this.getNode();
    if(!session || !node){ this.close(); return; }
    const char=this.data.characters?.[session.characterId];
    const displayLines=this.getDisplayLines(node);
    updateDialogueViewportConstraints();
    dialogue.style.display="block";
    dialogueName.textContent=char?.name || "Unknown";
    if(session.pendingChoices){
      dialogueText.textContent=displayLines.join("\n");
      dialogueChoices.innerHTML=session.pendingChoices.map((choice, idx)=>(
        "<button type=\"button\" class=\"dialogue-choice\" data-dialogue-choice=\"" + idx + "\">" + (idx+1) + ") " + choice.text + "</button>"
      )).join("");
      dialogueHint.textContent="Press 1-9 to choose an option.";
    } else {
      dialogueChoices.innerHTML="";
      dialogueText.textContent=displayLines[session.lineIndex] || "...";
      dialogueHint.textContent="Click to continue dialogue.";
    }
    updateDialogueViewportConstraints();
  }
}

class InteractionManager {
  constructor(range){ this.range=range; this.interactables=[]; }
  register(interactable){ this.interactables.push(interactable); }
  isInRange(target){ return Math.abs(player.targetX-target.x()) + Math.abs(player.targetY-target.y()) <= this.range; }
  getNearest(){
    let nearest=null;
    for(const target of this.interactables){
      const distance=Math.abs(player.targetX-target.x()) + Math.abs(player.targetY-target.y());
      if(distance>this.range) continue;
      if(!nearest || distance<nearest.distance) nearest={target,distance};
    }
    return nearest?.target || null;
  }
  getPromptText(){
    const target=this.getNearest();
    if(!target) return "E : Interact";
    if(target.promptLabel) return "E : " + target.promptLabel;
    return "E : Interact";
  }
  tryInteract(){
    if(dialogueSystem.activeSession){ dialogueSystem.advance(); return true; }
    if(isVendorOpen()){ closeVendorMenu(); return true; }
    const target=this.getNearest();
    if(!target) return false;
    target.onInteract?.();
    eventSystem.emit("interaction:used",{id:target.id,type:target.type});
    return true;
  }
  interactAt(x,y){
    const target=this.interactables.find((candidate)=>candidate.x()===x && candidate.y()===y && this.isInRange(candidate));
    if(!target) return false;
    target.onInteract?.();
    eventSystem.emit("interaction:used",{id:target.id,type:target.type});
    return true;
  }
}

const dialogueData=parseJsonScript("dialogueData");
const questData=parseJsonScript("questData");
const eventSystem=new EventTriggerSystem();
const questSystem=new QuestStateSystem(questData.quests||[], eventSystem);
const dialogueSystem=new DialogueFramework(dialogueData, eventSystem);
const interactionManager=new InteractionManager(2);

eventSystem.registerZoneTrigger("Mirror Pond", "zone:entered:mirror_pond");
eventSystem.on("dialogue:started:edrin", ()=>eventSystem.emit("npc:interacted:edrin"));
eventSystem.on("dialogue:started:hunter_garran", ()=>eventSystem.emit("npc:interacted:hunter_garran"));
eventSystem.on("dialogue:started:merchant_rowan", ()=>eventSystem.emit("npc:interacted:merchant_rowan"));
eventSystem.on("vendor:open", ()=>openVendorMenu());
eventSystem.on("zone:entered:mirror_pond", ()=>{
  const quest=questSystem.getQuest("mirror_pond_listening");
  if(quest?.state!==QuestState.ACTIVE || quest.progress!=="go_to_pond") return;
  log("You hear strange whispers in the water.");
  questSystem.updateProgress("mirror_pond_listening", "heard_whispers");
});
eventSystem.on("combat:enemy-defeated", ({enemyType})=>{
  const quest=questSystem.getQuest("hunters_request");
  if(quest?.state!==QuestState.ACTIVE || enemyType!=="wolf") return;
  questSystem.incrementObjective("hunters_request", "wolves", 1);
});
eventSystem.on("zone:entered:mirror_cave", ()=>{
  const quest=questSystem.getQuest("hunters_request");
  if(quest?.state!==QuestState.ACTIVE) return;
  if(questSystem.completeObjective("hunters_request", "enter_cave")) log("Objective Complete: Entered Mirror Cave");
});
eventSystem.on("object:opened:mirror_cave_chest", ()=>{
  const quest=questSystem.getQuest("hunters_request");
  if(quest?.state!==QuestState.ACTIVE) return;
  if(questSystem.completeObjective("hunters_request", "open_chest")) log("Objective Complete: Recovered the relic from Mirror Cave");
});
eventSystem.on("npc:interacted:hunter_garran", ()=>{
  const quest=questSystem.getQuest("hunters_request");
  if(quest?.state!==QuestState.READY_TO_TURN_IN) return;
  questSystem.completeObjective("hunters_request", "return_hunter");
});
eventSystem.on("quest:report:mirror_pond", ()=>{
  const quest=questSystem.getQuest("mirror_pond_listening");
  if(quest?.state!==QuestState.ACTIVE || quest.progress!=="heard_whispers") return;
  questSystem.completeQuest("mirror_pond_listening");
});
eventSystem.on("quest:turn_in:hunters_request", ()=>{
  const completed=questSystem.tryTurnInQuest("hunters_request");
  if(!completed) log("Finish all Hunter's Request objectives before turning this in.");
});
eventSystem.on("quest:completed:mirror_pond_listening", ()=>eventSystem.emit("world:pond:awakened"));
let worldEvents={ pondAwakened:false };
const worldTriggeredEvents=new Set();
eventSystem.on("world:pond:awakened", ()=>{
  if(worldEvents.pondAwakened) return;
  worldEvents.pondAwakened=true;
  worldTriggeredEvents.add("world:pond:awakened");
  log("World Event: Mirror Pond awakens and the air goes still.");
});

const SAVE_KEY="wayfarer.save.v1";
const SAVE_SCHEMA_VERSION=1;
const SUPPORTED_SAVE_VERSIONS=new Set([1,2,3,4,5,6,7,8,9]);
const DEV_DEBUG_TOOLS_ENABLED=true;
let saveNoticeTimeout=0;
function showSaveNotice(message){
  saveNotice.textContent=message;
  saveNotice.classList.add("visible");
  if(saveNoticeTimeout) clearTimeout(saveNoticeTimeout);
  saveNoticeTimeout=setTimeout(()=>saveNotice.classList.remove("visible"), 1400);
}
function isFiniteNumber(value){ return typeof value==="number" && Number.isFinite(value); }
function createSaveData(reason){
  updateOutdoorRegionFromPosition(false);
  const wolvesSave=wolves.slice(0, WOLF_SPAWNS.length).map((wolf)=>({
    id:wolf.id,
    hp:wolf.hp,
    defeated:wolf.defeated,
    respawnRemainingMs:Math.max(0, wolfRespawnAtById[wolf.id] ? wolfRespawnAtById[wolf.id]-performance.now() : 0)
  }));
  const banditsSave=bandits.slice(0, BANDIT_SPAWNS.length).map((bandit)=>({
    id:bandit.id,
    hp:bandit.hp,
    defeated:bandit.defeated,
    respawnRemainingMs:Math.max(0, banditRespawnAtById[bandit.id] ? banditRespawnAtById[bandit.id]-performance.now() : 0)
  }));
  return {
    version:9,
    saveSchemaVersion:SAVE_SCHEMA_VERSION,
    reason,
    savedAt:new Date().toISOString(),
    player:{
      zoneId:currentZoneId,
      position:{ x:player.targetX, y:player.targetY },
      hp:player.hp,
      xp:player.xp,
      coins:player.coins,
      inventory:player.inventory.map((entry)=>({ itemId:entry.itemId, quantity:entry.quantity })),
      equipment:{ ...player.equipment }
    },
    quests:{
      questStates:questSystem.serializeState(),
      completedQuests:questSystem.getCompletedQuestIds(),
      activeQuests:questSystem.getActiveQuestIds()
    },
    world:{
      triggeredEvents:Array.from(worldTriggeredEvents),
      stateChanges:{ pondAwakened:worldEvents.pondAwakened },
      mirrorCave:{
        chestOpened:mirrorCave.chest.opened,
        cleared:mirrorCave.cleared
      },
      creatures:{
        wolves:wolvesSave,
        bandits:banditsSave,
        mirrorCaveWolves:mirrorCaveWolves.map((wolf)=>({
          id:wolf.id,
          hp:wolf.hp,
          defeated:wolf.defeated,
          respawnRemainingMs:Math.max(0, wolfRespawnAtById[wolf.id] ? wolfRespawnAtById[wolf.id]-performance.now() : 0)
        }))
      }
    }
  };
}
function validateSaveData(data){
  if(!data || !SUPPORTED_SAVE_VERSIONS.has(data.version)) return false;
  const px=data.player?.position?.x, py=data.player?.position?.y;
  if(!Number.isInteger(px) || !Number.isInteger(py)) return false;
  if(!isFiniteNumber(data.player?.hp) || !isFiniteNumber(data.player?.xp) || !isFiniteNumber(data.player?.coins)) return false;
  return true;
}
function saveGame(reason){
  try {
    const payload=createSaveData(reason);
    localStorage.setItem(SAVE_KEY, JSON.stringify(payload));
    showSaveNotice("Game Saved");
  } catch(err){
    console.error("Save failed", err);
    log("System: Save failed.");
  }
}
function loadGame(){
  const raw=localStorage.getItem(SAVE_KEY);
  if(!raw) return false;
  try {
    const data=JSON.parse(raw);
    if(!validateSaveData(data)) throw new Error("Invalid save payload");
    const saveSchemaVersion=Number.isInteger(data.saveSchemaVersion) ? data.saveSchemaVersion : 0;
    if(saveSchemaVersion>SAVE_SCHEMA_VERSION) log("System: Save schema is newer than this build. Attempting safe load.");
    const savedZoneId=typeof data.player.zoneId==="string" ? data.player.zoneId : getOutdoorRegionIdAt(data.player.position.x, data.player.position.y);
    isInMirrorCave=savedZoneId==="mirror_cave";
    const mapW=isInMirrorCave ? mirrorCave.width : WORLD_W;
    const mapH=isInMirrorCave ? mirrorCave.height : WORLD_H;
    const loadedX=Math.max(0,Math.min(mapW-1,data.player.position.x));
    const loadedY=Math.max(0,Math.min(mapH-1,data.player.position.y));
    setPlayerTilePosition(loadedX, loadedY);
    zoneTransitionLockedUntil=0;
    blockedDirectionalKeysUntilRelease.clear();
    currentZoneId=isInMirrorCave ? "mirror_cave" : getOutdoorRegionIdAt(loadedX, loadedY);
    lastLoggedZoneEntryId=currentZoneId;
    player.hp=Math.max(0,Math.min(player.maxHp,data.player.hp));
    player.xp=Math.max(0,data.player.xp);
    player.coins=Math.max(0,data.player.coins);
    player.inventory=normalizeInventory(data.player.inventory);
    if(data.player.equipment && typeof data.player.equipment==="object"){
      player.equipment={
        weapon:typeof data.player.equipment.weapon==="string" ? data.player.equipment.weapon : null,
        armor:typeof data.player.equipment.armor==="string" ? data.player.equipment.armor : null,
        trinket:typeof data.player.equipment.trinket==="string" ? data.player.equipment.trinket : null
      };
    } else if(data.player.weapon && typeof data.player.weapon==="object"){
      player.equipment={
        weapon:"rusty_sword",
        armor:null,
        trinket:null
      };
    }
    ensureStarterEquipment();
    questSystem.applyState(data.quests?.questStates||[]);
    worldTriggeredEvents.clear();
    (data.world?.triggeredEvents||[]).forEach((eventName)=>{ if(typeof eventName==="string") worldTriggeredEvents.add(eventName); });
    worldEvents.pondAwakened=Boolean(data.world?.stateChanges?.pondAwakened);
    wolves.forEach((wolf)=>{
      wolf.hp=wolf.maxHp;
      wolf.defeated=false;
      wolf.targetX=wolf.homeX;
      wolf.targetY=wolf.homeY;
      wolf.px=wolf.targetX*TILE;
      wolf.py=wolf.targetY*TILE;
      wolfRespawnAtById[wolf.id]=0;
      lastWolfDecisionAt[wolf.id]=0;
      lastWolfAttackAt[wolf.id]=0;
    });
    bandits.forEach((bandit)=>{
      bandit.hp=bandit.maxHp;
      bandit.defeated=false;
      bandit.targetX=bandit.homeX;
      bandit.targetY=bandit.homeY;
      bandit.px=bandit.targetX*TILE;
      bandit.py=bandit.targetY*TILE;
      banditRespawnAtById[bandit.id]=0;
      lastBanditDecisionAt[bandit.id]=0;
      lastBanditAttackAt[bandit.id]=0;
    });
    mirrorCaveWolves.forEach((wolf)=>{
      wolf.hp=wolf.maxHp;
      wolf.defeated=false;
      wolf.targetX=wolf.homeX;
      wolf.targetY=wolf.homeY;
      wolf.px=wolf.targetX*TILE;
      wolf.py=wolf.targetY*TILE;
      wolfRespawnAtById[wolf.id]=0;
      lastWolfDecisionAt[wolf.id]=0;
      lastWolfAttackAt[wolf.id]=0;
    });
    const savedWolves=Array.isArray(data.world?.creatures?.wolves) ? data.world.creatures.wolves : null;
    if(savedWolves){
      savedWolves.forEach((savedWolf)=>{
        if(!savedWolf || typeof savedWolf!=="object") return;
        const wolf=wolves.find((candidate)=>candidate.id===savedWolf.id);
        if(!wolf) return;
        wolf.hp=isFiniteNumber(savedWolf.hp) ? Math.max(0,Math.min(wolf.maxHp,savedWolf.hp)) : wolf.hp;
        wolf.defeated=Boolean(savedWolf.defeated) || wolf.hp<=0;
        const remaining=isFiniteNumber(savedWolf.respawnRemainingMs)?Math.max(0,savedWolf.respawnRemainingMs):0;
        wolfRespawnAtById[wolf.id]=wolf.defeated ? performance.now()+remaining : 0;
      });
    } else {
      const legacyWolf=data.world?.creatures?.wolf;
      if(legacyWolf && typeof legacyWolf==="object"){
        const wolf=wolves[0];
        wolf.hp=isFiniteNumber(legacyWolf.hp) ? Math.max(0,Math.min(wolf.maxHp,legacyWolf.hp)) : wolf.hp;
        wolf.defeated=Boolean(legacyWolf.defeated) || wolf.hp<=0;
        const remaining=isFiniteNumber(legacyWolf.respawnRemainingMs)?Math.max(0,legacyWolf.respawnRemainingMs):0;
        wolfRespawnAtById[wolf.id]=wolf.defeated ? performance.now()+remaining : 0;
      }
    }
    const savedBandits=Array.isArray(data.world?.creatures?.bandits) ? data.world.creatures.bandits : null;
    if(savedBandits){
      savedBandits.forEach((savedBandit)=>{
        if(!savedBandit || typeof savedBandit!=="object") return;
        const bandit=bandits.find((candidate)=>candidate.id===savedBandit.id);
        if(!bandit) return;
        bandit.hp=isFiniteNumber(savedBandit.hp) ? Math.max(0,Math.min(bandit.maxHp,savedBandit.hp)) : bandit.hp;
        bandit.defeated=Boolean(savedBandit.defeated) || bandit.hp<=0;
        const remaining=isFiniteNumber(savedBandit.respawnRemainingMs)?Math.max(0,savedBandit.respawnRemainingMs):0;
        banditRespawnAtById[bandit.id]=bandit.defeated ? performance.now()+remaining : 0;
      });
    }
    const savedMirrorCaveWolves=Array.isArray(data.world?.creatures?.mirrorCaveWolves) ? data.world.creatures.mirrorCaveWolves : null;
    if(savedMirrorCaveWolves){
      savedMirrorCaveWolves.forEach((savedWolf)=>{
        if(!savedWolf || typeof savedWolf!=="object") return;
        const wolf=mirrorCaveWolves.find((candidate)=>candidate.id===savedWolf.id);
        if(!wolf) return;
        wolf.hp=isFiniteNumber(savedWolf.hp) ? Math.max(0,Math.min(wolf.maxHp,savedWolf.hp)) : wolf.hp;
        wolf.defeated=Boolean(savedWolf.defeated) || wolf.hp<=0;
        const remaining=isFiniteNumber(savedWolf.respawnRemainingMs)?Math.max(0,savedWolf.respawnRemainingMs):0;
        wolfRespawnAtById[wolf.id]=wolf.defeated ? performance.now()+remaining : 0;
      });
    }
    mirrorCave.chest.opened=Boolean(data.world?.mirrorCave?.chestOpened);
    mirrorCave.cleared=Boolean(data.world?.mirrorCave?.cleared);
    log("System: Save loaded.");
    return true;
  } catch(err){
    console.error("Load failed", err);
    localStorage.removeItem(SAVE_KEY);
    log("System: Save data was corrupted and has been reset.");
    return false;
  }
}
eventSystem.on("quest:completed:mirror_pond_listening", ()=>saveGame("quest_complete"));
eventSystem.on("quest:completed:hunters_request", ()=>saveGame("quest_complete"));
eventSystem.on("quest:state-changed", ()=>saveGame("quest_state_change"));

interactionManager.register({
  id:"npc_edrin", type:"npc", x:()=>npc.x, y:()=>npc.y,
  promptLabel:"Talk to Edrin Vale",
  onInteract:()=>dialogueSystem.start("edrin")
});
interactionManager.register({
  id:"npc_hunter_garran", type:"npc", x:()=>hunterNpc.x, y:()=>hunterNpc.y,
  promptLabel:"Talk to Hunter Garran",
  onInteract:()=>dialogueSystem.start("hunter_garran")
});
interactionManager.register({
  id:"npc_merchant_rowan", type:"npc", x:()=>vendorNpc.x, y:()=>vendorNpc.y,
  promptLabel:"Talk to Merchant Rowan",
  onInteract:()=>dialogueSystem.start("merchant_rowan")
});
interactionManager.register({
  id:"obj_well", type:"object", x:()=>18, y:()=>11,
  promptLabel:"Inspect well",
  onInteract:()=>{ log("The well water is cold and perfectly still."); eventSystem.emit("object:used:well",{}); }
});
interactionManager.register({
  id:"obj_sign_pond", type:"object", x:()=>25, y:()=>11,
  promptLabel:"Read signpost",
  onInteract:()=>{ log("Signpost: Mirror Pond — Keep silence near the water."); eventSystem.emit("object:used:pond_sign",{}); }
});
interactionManager.register({
  id:"obj_mirror_cave_entrance", type:"object", x:()=>isInMirrorCave ? -999 : OVERWORLD_CAVE_ENTRY.x, y:()=>isInMirrorCave ? -999 : OVERWORLD_CAVE_ENTRY.y,
  promptLabel:"Enter Mirror Cave",
  onInteract:()=>enterMirrorCave()
});
interactionManager.register({
  id:"obj_mirror_cave_exit", type:"object", x:()=>isInMirrorCave ? mirrorCave.exit.x : -999, y:()=>isInMirrorCave ? mirrorCave.exit.y : -999,
  promptLabel:"Exit Mirror Cave",
  onInteract:()=>exitMirrorCave()
});
interactionManager.register({
  id:"obj_mirror_cave_chest", type:"object", x:()=>isInMirrorCave && !mirrorCave.chest.opened ? mirrorCave.chest.x : -999, y:()=>isInMirrorCave && !mirrorCave.chest.opened ? mirrorCave.chest.y : -999,
  promptLabel:"Open chest",
  onInteract:()=>{
    if(mirrorCave.chest.opened) return;
    mirrorCave.chest.opened=true;
    addItemToInventory("iron_sword", 1);
    log("You obtained Iron Sword.");
    mirrorCave.cleared=true;
    log("Mirror Cave cleared.");
    eventSystem.emit("object:opened:mirror_cave_chest");
  }
});

dialogue.addEventListener("click",()=>{
  if(dialogueSystem.activeSession?.pendingChoices) return;
  if(dialogueSystem.activeSession) dialogueSystem.advance();
});
dialogueChoices.addEventListener("click",(event)=>{
  const target=event.target instanceof Element ? event.target.closest("button[data-dialogue-choice]") : null;
  if(!target) return;
  event.preventDefault();
  event.stopPropagation();
  const index=Number.parseInt(target.getAttribute("data-dialogue-choice") || "-1", 10);
  if(Number.isInteger(index) && index>=0) dialogueSystem.choose(index);
});
vendorClose.addEventListener("click", closeVendorMenu);
vendorList.addEventListener("click",(e)=>{
  const target=e.target instanceof Element ? e.target : null;
  if(!target) return;
  const buyButton=target.closest("button[data-buy-item]");
  const buyItemId=buyButton?.dataset?.buyItem;
  if(buyItemId){
    buyOneItemFromVendor(buyItemId);
    return;
  }
  const sellButton=target.closest("button[data-sell-item]");
  const itemId=sellButton?.dataset?.sellItem;
  if(!itemId) return;
  sellOneItemToVendor(itemId);
});

function getZoneDefinition(zoneId){
  return OUTDOOR_REGION_DEFS[zoneId] || INTERIOR_REGION_DEFS[zoneId] || OUTDOOR_REGION_DEFS.hearthvale_square;
}

function getCurrentZoneName(){
  return getZoneDefinition(currentZoneId).name;
}

function isWithinRect(x,y,rect){
  return x>=rect.x && x<rect.x+rect.w && y>=rect.y && y<rect.y+rect.h;
}

function isTileInCurrentZone(x,y){
  const width=isInMirrorCave ? mirrorCave.width : WORLD_W;
  const height=isInMirrorCave ? mirrorCave.height : WORLD_H;
  return x>=0 && y>=0 && x<width && y<height;
}

function isInTransitionSafeBuffer(zoneId,x,y){
  return false;
}

function isEasternWoodsActive(){
  return !isInMirrorCave;
}

function findZoneTransitionAt(){ return null; }

function getActiveHostiles(){
  return isInMirrorCave ? mirrorCaveWolves : [...wolves, ...bandits];
}

function runHardTransition(onSwitch, durationMs=320){
  const now=performance.now();
  zoneTransitionLockedUntil=now+durationMs+80;
  clearDirectionalInput();
  blockedDirectionalKeysUntilRelease = new Set(DIRECTION_KEYS.filter((key)=>keys.has(key)));
  transitionState={
    active:true,
    start:now,
    duration:durationMs,
    switched:false,
    onSwitch
  };
}

function enterMirrorCave(){
  runHardTransition(()=>{
    isInMirrorCave=true;
    currentZoneId="mirror_cave";
    setPlayerTilePosition(mirrorCave.spawn.x, mirrorCave.spawn.y);
    lastLoggedZoneEntryId=currentZoneId;
    logThrottled("transition:entered_mirror_cave", "Entered Mirror Cave.", 1200);
    eventSystem.emit("zone:entered:mirror_cave");
  }, 320);
}

function exitMirrorCave(){
  runHardTransition(()=>{
    isInMirrorCave=false;
    currentZoneId="eastern_woods";
    setPlayerTilePosition(mirrorCave.returnTile.x, mirrorCave.returnTile.y);
    lastLoggedZoneEntryId=currentZoneId;
    logThrottled("transition:exit_mirror_cave", "Returned to Eastern Woods.", 1200);
  }, 320);
}

function setPlayerTilePosition(x,y){
  player.targetX=Math.max(0,Math.min(WORLD_W-1,x));
  player.targetY=Math.max(0,Math.min(WORLD_H-1,y));
  player.px=player.targetX*TILE;
  player.py=player.targetY*TILE;
  player.moving=false;
}

function clearDirectionalInput(){
  DIRECTION_KEYS.forEach((key)=>keys.delete(key));
}

function isDirectionalInputHeld(){
  return DIRECTION_KEYS.some((key)=>keys.has(key));
}

function handleZoneTransitionIfNeeded(){
  if(HARD_ZONE_TRANSITIONS.length===0) return false;
  return true;
}

function getOutdoorRegionIdAt(x,y){
  for(const region of Object.values(OUTDOOR_REGION_DEFS)){
    if(isWithinRect(x,y,region.bounds)) return region.id;
  }
  return "hearthvale_square";
}

function updateOutdoorRegionFromPosition(logEntry){
  if(isInMirrorCave) return;
  const nextZoneId=getOutdoorRegionIdAt(player.targetX, player.targetY);
  if(nextZoneId===currentZoneId) return;
  currentZoneId=nextZoneId;
  if(logEntry && lastLoggedZoneEntryId!==currentZoneId){
    logThrottled("zone_entry:" + currentZoneId, "Entered " + getCurrentZoneName() + ".", 1200);
    lastLoggedZoneEntryId=currentZoneId;
  }
}

function currentLocalAreaName(){
  if(isInMirrorCave) return "Mirror Cave";
  for(const z of world.zones){
    if(player.targetX>=z.x&&player.targetX<z.x+z.w&&player.targetY>=z.y&&player.targetY<z.y+z.h) return z.name;
  }
  return "Outer Road";
}

function getHostileDistance(hostile){
  if(!hostile || hostile.hp<=0) return Infinity;
  return Math.abs(player.targetX-hostile.targetX)+Math.abs(player.targetY-hostile.targetY);
}

function hostileLabel(hostile){
  if(!hostile) return "None";
  return hostile.kind==="bandit" ? ("Bandit #" + hostile.id) : ("Wolf #" + hostile.id);
}

function getHostileAttackCooldownMs(hostile){
  if(!hostile) return 0;
  return hostile.kind==="bandit" ? BANDIT_ATTACK_COOLDOWN_MS : WOLF_ATTACK_COOLDOWN_MS;
}

function getHostileLastAttackAt(hostile){
  if(!hostile) return 0;
  return hostile.kind==="bandit" ? (lastBanditAttackAt[hostile.id]||0) : (lastWolfAttackAt[hostile.id]||0);
}

function getNearestHostile(range=Infinity){
  let nearest=null;
  for(const hostile of getActiveHostiles()){
    const distance=getHostileDistance(hostile);
    if(distance>range) continue;
    if(!nearest || distance<nearest.distance) nearest={entity:hostile,distance};
  }
  return nearest;
}

function respawnPlayerAtSquare(){
  isInMirrorCave=false;
  currentZoneId="hearthvale_square";
  setPlayerTilePosition(18, 11);
  zoneTransitionLockedUntil=0;
  blockedDirectionalKeysUntilRelease.clear();
  lastLoggedZoneEntryId=currentZoneId;
}

function handlePlayerDefeat(){
  log("Defeat: You fall in battle.");
  player.hp=player.maxHp;
  respawnPlayerAtSquare();
  log("System: You awaken at Hearthvale Square.");
}

let sidebarInventoryMarkup="";
let sidebarEquipmentMarkup="";
function updateSidebar(){
  hpVal.textContent = player.hp + "/" + player.maxHp;
  xpVal.textContent = String(player.xp);
  coinsVal.textContent = String(player.coins);
  const equippedWeapon=getEquippedItem("weapon");
  weaponVal.textContent = equippedWeapon ? (equippedWeapon.name + " (+" + getEquippedWeaponBonus() + ")") : "None";
  const zoneName=getCurrentZoneName();
  zoneVal.textContent = zoneName;
  const huntersQuest=questSystem.getQuest("hunters_request");
  const mirrorQuest=questSystem.getQuest("mirror_pond_listening");
  const activeQuest=((huntersQuest?.state===QuestState.ACTIVE || huntersQuest?.state===QuestState.READY_TO_TURN_IN) ? huntersQuest : ((mirrorQuest?.state===QuestState.ACTIVE) ? mirrorQuest : (huntersQuest?.state===QuestState.COMPLETED ? huntersQuest : mirrorQuest)));
  questVal.textContent = activeQuest ? (activeQuest.name + " [" + activeQuest.state + "]") : "Town Slice";
  if(huntersQuest?.state===QuestState.ACTIVE || huntersQuest?.state===QuestState.READY_TO_TURN_IN){
    const objectiveLines=(huntersQuest.objectives||[]).map((objective)=>{
      const checked=objective.completed ? "✔" : " ";
      const hasCounter=objective.requiredAmount>1;
      const counter=hasCounter ? (" (" + objective.currentAmount + "/" + objective.requiredAmount + ")") : "";
      return "[" + checked + "] " + objective.label + counter;
    }).join("\n");
    objectiveText.textContent = "Hunter's Request\n" + objectiveLines;
  } else if(mirrorQuest?.state===QuestState.ACTIVE && mirrorQuest.progress==="go_to_pond"){
    objectiveText.textContent = "Go to Mirror Pond and listen carefully.";
  } else if(mirrorQuest?.state===QuestState.ACTIVE && mirrorQuest.progress==="heard_whispers"){
    objectiveText.textContent = "Return to Edrin Vale and report what you heard.";
  } else if(huntersQuest?.state===QuestState.COMPLETED){
    objectiveText.textContent = "Quest complete: Hunter's Request.";
  } else if(mirrorQuest?.state===QuestState.COMPLETED){
    objectiveText.textContent = "Speak with Hunter Garran near the eastern road.";
  } else {
    objectiveText.textContent = "Speak with Hunter Garran near the eastern road.";
  }
  let nextInventoryMarkup="Empty";
  if(player.inventory.length>0){
    nextInventoryMarkup=player.inventory.map((entry)=>{
      const item=getItemDefinition(entry.itemId);
      const name=item?.name || entry.itemId;
      const equipSlot=item?.type==="weapon"
        ? "weapon"
        : (item?.type==="armor"
          ? "armor"
          : (item?.type==="trinket" ? "trinket" : null));
      const canEquip=Boolean(equipSlot);
      const equipped=Boolean(item?.id && equipSlot && item.id===player.equipment[equipSlot]);
      if(canEquip){
        const actionLabel=equipped ? "[Equipped]" : "Equip";
        const disabledAttr=equipped ? " disabled" : "";
        return name + " x" + entry.quantity + " <button type=\"button\" data-equip-item=\"" + item.id + "\" data-equip-slot=\"" + equipSlot + "\"" + disabledAttr + ">" + actionLabel + "</button>";
      }
      return name + " x" + entry.quantity;
    }).join("<br>");
  }
  if(nextInventoryMarkup!==sidebarInventoryMarkup){
    inventoryList.innerHTML = nextInventoryMarkup;
    sidebarInventoryMarkup=nextInventoryMarkup;
  }
  // Do not re-render vendor rows every sidebar update; replacing DOM each frame
  // can swallow button clicks before click events complete.
  const weaponLine=equippedWeapon ? (equippedWeapon.name + " (+" + getEquippedWeaponBonus() + ")") : "";
  const equippedArmor=getEquippedItem("armor");
  const armorDefense=getEquippedDefenseBonus();
  const armorLine=equippedArmor
    ? (equippedArmor.name + " (+" + armorDefense + " DEF) <span class=\"muted\">Armor active.</span> <button type=\"button\" data-unequip-slot=\"armor\">Remove</button>")
    : "None";
  const nextEquipmentMarkup="Weapon: " + weaponLine + "<br>Armor: " + armorLine + "<br>Trinket: ";
  if(nextEquipmentMarkup!==sidebarEquipmentMarkup){
    equipmentList.innerHTML = nextEquipmentMarkup;
    sidebarEquipmentMarkup=nextEquipmentMarkup;
  }
  const nearbyHostile=getNearestHostile(5);
  const targetHostile=getNearestHostile(PLAYER_ATTACK_RANGE);
  const currentTarget=targetHostile?.entity || null;
  const targetCooldownMs=currentTarget ? Math.max(0, getHostileAttackCooldownMs(currentTarget)-(performance.now()-getHostileLastAttackAt(currentTarget))) : 0;
  const targetCooldownText=!currentTarget ? "N/A" : (currentTarget.hp<=0 ? "Down" : (targetCooldownMs<=0 ? "Ready" : (targetCooldownMs/1000).toFixed(1)+"s"));
  const interactionPrompt=interactionManager.getPromptText();
  hud.textContent = "WASD / Arrows : Move\n" + interactionPrompt + "\nSpace : Attack\nH : Use healing item\nK : Manual Save\n1-9 : Dialogue Choices\nG : Toggle grid\nF6 : Debug Heal\nF7/F8/F9 : Debug Teleport\nF10 : Debug Reset Quest\nShift+F10 : Debug Reset Save\nCurrent Zone : " + zoneName +
    "\nHostile nearby : " + (nearbyHostile ? "Yes (" + hostileLabel(nearbyHostile.entity) + ")" : "No") +
    "\nCurrent target : " + hostileLabel(currentTarget) +
    "\nTarget strike cd : " + targetCooldownText;
}

function canMoveTo(x,y){
  if(!isTileInCurrentZone(x,y)) return false;
  if(isInMirrorCave){
    if(mirrorCave.blocked.has(keyOf(x,y))) return false;
  } else {
    if(world.blocked.has(keyOf(x,y))||world.pondBlocked.has(keyOf(x,y))) return false;
    if(x===npc.x&&y===npc.y) return false;
    if(x===vendorNpc.x&&y===vendorNpc.y) return false;
    if(x===hunterNpc.x&&y===hunterNpc.y) return false;
  }
  if(getActiveHostiles().some((hostile)=>hostile.hp>0&&x===hostile.targetX&&y===hostile.targetY)) return false;
  return true;
}

const keys=new Set();
let showGrid=false;

const questDefinitionById=new Map((questData.quests||[]).map((quest)=>[quest.id, quest]));
function resetQuestToNotStarted(questId){
  const quest=questSystem.getQuest(questId);
  const definition=questDefinitionById.get(questId);
  if(!quest || !definition) return false;
  quest.state=QuestState.NOT_STARTED;
  quest.status=QuestState.NOT_STARTED;
  quest.progress=definition.initialProgress || "";
  quest.objectives=questSystem.normalizeObjectives(definition.objectives||[]);
  eventSystem.emit("quest:state-changed",{questId,state:quest.state,progress:quest.progress});
  return true;
}
function resetCurrentQuestForDebug(){
  const priority=["hunters_request","mirror_pond_listening"];
  const activeOrReady=priority.find((questId)=>{
    const quest=questSystem.getQuest(questId);
    return quest && (quest.state===QuestState.ACTIVE || quest.state===QuestState.READY_TO_TURN_IN || quest.state===QuestState.COMPLETED);
  });
  if(!activeOrReady){
    log("[Debug] No quest state available to reset.");
    return;
  }
  if(resetQuestToNotStarted(activeOrReady)){
    log("[Debug] Reset quest state: " + activeOrReady + ".");
    saveGame("debug_reset_quest");
  }
}
function healPlayerToFullForDebug(){
  player.hp=player.maxHp;
  log("[Debug] Restored HP to full.");
  saveGame("debug_heal");
}
function teleportToZoneForDebug(zoneId){
  if(zoneId==="hearthvale_square"){
    isInMirrorCave=false;
    currentZoneId="hearthvale_square";
    setPlayerTilePosition(18, 11);
    log("[Debug] Teleported to Hearthvale Square.");
  } else if(zoneId==="eastern_woods"){
    isInMirrorCave=false;
    currentZoneId="eastern_woods";
    setPlayerTilePosition(mirrorCave.returnTile.x, mirrorCave.returnTile.y);
    log("[Debug] Teleported to Eastern Woods.");
  } else if(zoneId==="mirror_cave"){
    isInMirrorCave=true;
    currentZoneId="mirror_cave";
    setPlayerTilePosition(mirrorCave.spawn.x, mirrorCave.spawn.y);
    log("[Debug] Teleported to Mirror Cave.");
  }
  lastLoggedZoneEntryId=currentZoneId;
  zoneTransitionLockedUntil=0;
  blockedDirectionalKeysUntilRelease.clear();
  saveGame("debug_teleport");
}
function resetFullSaveForDebug(){
  localStorage.removeItem(SAVE_KEY);
  log("[Debug] Save data cleared. Reloading world state.");
  setTimeout(()=>location.reload(), 120);
}
addEventListener("keydown",(e)=>{
  const k=e.key.toLowerCase();
  if(["w","a","s","d","arrowup","arrowdown","arrowleft","arrowright"," ","e","h","k","1","2","3","4","5","6","7","8","9","f6","f7","f8","f9","f10"].includes(k)) e.preventDefault();
  if(DIRECTION_KEYS.includes(k)){
    if(blockedDirectionalKeysUntilRelease.has(k)) return;
  }
  if(k==="g") showGrid=!showGrid;
  if(k==="e") interactionManager.tryInteract();
  if(k==="h") useHealingConsumable();
  if(k==="k") saveGame("manual");
  if(DEV_DEBUG_TOOLS_ENABLED && k==="f6") healPlayerToFullForDebug();
  if(DEV_DEBUG_TOOLS_ENABLED && k==="f7") teleportToZoneForDebug("hearthvale_square");
  if(DEV_DEBUG_TOOLS_ENABLED && k==="f8") teleportToZoneForDebug("eastern_woods");
  if(DEV_DEBUG_TOOLS_ENABLED && k==="f9") teleportToZoneForDebug("mirror_cave");
  if(DEV_DEBUG_TOOLS_ENABLED && k==="f10" && e.shiftKey) resetFullSaveForDebug();
  else if(DEV_DEBUG_TOOLS_ENABLED && k==="f10") resetCurrentQuestForDebug();
  if(dialogueSystem.activeSession?.pendingChoices && /^[1-9]$/.test(k)) dialogueSystem.choose(Number(k)-1);
  keys.add(k);
});
addEventListener("keyup",(e)=>{
  const k=e.key.toLowerCase();
  keys.delete(k);
  if(DIRECTION_KEYS.includes(k)){
    blockedDirectionalKeysUntilRelease.delete(k);
  }
  if(k===" "||k==="space") missNoticeArmed=true;
});
canvas.addEventListener("click",(e)=>{ const clicked=screenToWorld(e.clientX,e.clientY); interactionManager.interactAt(clicked.x, clicked.y); });
inventoryList.addEventListener("click",(e)=>{
  const target=e.target instanceof Element ? e.target.closest("button[data-equip-item]") : null;
  if(!(target instanceof HTMLElement)) return;
  const itemId=target.dataset?.equipItem;
  const slotName=target.dataset?.equipSlot;
  if(!itemId || !slotName) return;
  if(slotName==="weapon" && equipWeapon(itemId)) updateSidebar();
  if(slotName==="armor" && equipArmor(itemId)) updateSidebar();
  if(slotName==="trinket"){
    const item=getItemDefinition(itemId);
    if(item && item.type==="trinket" && getItemQuantity(itemId)>0){
      player.equipment.trinket=itemId;
      log("Equipped " + item.name + ".");
      updateSidebar();
    }
  }
});
equipmentList.addEventListener("click",(e)=>{
  const target=e.target instanceof Element ? e.target.closest("button[data-unequip-slot]") : null;
  if(!(target instanceof HTMLElement)) return;
  const slotName=target.dataset?.unequipSlot;
  if(!slotName) return;
  if(unequipSlot(slotName)) updateSidebar();
});

function getCamera(){
  const mapW=isInMirrorCave ? mirrorCave.width : WORLD_W;
  const mapH=isInMirrorCave ? mirrorCave.height : WORLD_H;
  const tileX=Math.max(0,Math.min(player.targetX-Math.floor(VIEW_TILES_X/2),Math.max(0,mapW-VIEW_TILES_X)));
  const tileY=Math.max(0,Math.min(player.targetY-Math.floor(VIEW_TILES_Y/2),Math.max(0,mapH-VIEW_TILES_Y)));
  const viewPxW=VIEW_TILES_X*TILE, viewPxH=VIEW_TILES_Y*TILE;
  const offsetX=Math.floor((canvas.width-viewPxW)/2), offsetY=Math.floor((canvas.height-viewPxH)/2);
  return {tileX,tileY,offsetX,offsetY};
}
function tileToScreen(tx,ty){ const cam=getCamera(); return {x:(tx-cam.tileX)*TILE+cam.offsetX,y:(ty-cam.tileY)*TILE+cam.offsetY}; }
function screenToWorld(clientX,clientY){ const rect=canvas.getBoundingClientRect(); const mx=clientX-rect.left,my=clientY-rect.top; const cam=getCamera(); return {x:Math.floor((mx-cam.offsetX)/TILE)+cam.tileX,y:Math.floor((my-cam.offsetY)/TILE)+cam.tileY}; }

function smoothMove(entity,dt){ const tx=entity.targetX*TILE, ty=entity.targetY*TILE; const dx=tx-entity.px, dy=ty-entity.py; const dist=Math.hypot(dx,dy); if(dist<.35){ entity.px=tx; entity.py=ty; entity.moving=false; return; } entity.moving=true; const step=entity.speed*dt; entity.px += (dx/dist)*Math.min(step,dist); entity.py += (dy/dist)*Math.min(step,dist); }
function tryPlayerStep(dx,dy,facing){
  if(player.moving||dialogueSystem.activeSession) return;
  if(performance.now()<zoneTransitionLockedUntil) return;
  const nx=player.targetX+dx, ny=player.targetY+dy;
  player.facing=facing;
  if(!canMoveTo(nx,ny)) return;
  player.targetX=nx;
  player.targetY=ny;
}
const moveIntent={dx:0,dy:0,facing:"down"};
function updateInput(){
  if(keys.has("w")||keys.has("arrowup")) tryPlayerStep(0,-1,"up");
  else if(keys.has("s")||keys.has("arrowdown")) tryPlayerStep(0,1,"down");
  else if(keys.has("a")||keys.has("arrowleft")) tryPlayerStep(-1,0,"left");
  else if(keys.has("d")||keys.has("arrowright")) tryPlayerStep(1,0,"right");
  moveIntent.dx=0; moveIntent.dy=0;
  if(keys.has("w")||keys.has("arrowup")){ moveIntent.dy=-1; moveIntent.facing="up"; }
  else if(keys.has("s")||keys.has("arrowdown")){ moveIntent.dy=1; moveIntent.facing="down"; }
  else if(keys.has("a")||keys.has("arrowleft")){ moveIntent.dx=-1; moveIntent.facing="left"; }
  else if(keys.has("d")||keys.has("arrowright")){ moveIntent.dx=1; moveIntent.facing="right"; }
}

function canHostileMoveTo(x,y,self){
  if(!isTileInCurrentZone(x,y)) return false;
  if(isInMirrorCave){
    if(mirrorCave.blocked.has(keyOf(x,y))) return false;
  } else {
    if(world.blocked.has(keyOf(x,y))) return false;
    if(x===npc.x&&y===npc.y) return false;
    if(x===vendorNpc.x&&y===vendorNpc.y) return false;
    if(x===hunterNpc.x&&y===hunterNpc.y) return false;
  }
  if(getActiveHostiles().some((hostile)=>hostile!==self && hostile.hp>0 && hostile.targetX===x && hostile.targetY===y)) return false;
  return true;
}
function isHostileAggroBlocked(now){
  return false;
}
function updateWolf(wolf,now){
  if(wolf.hp<=0){
    const respawnAt=wolfRespawnAtById[wolf.id]||0;
    if(respawnAt!==0&&now>=respawnAt){
      wolf.hp=wolf.maxHp;
      wolf.defeated=false;
      wolf.targetX=wolf.homeX; wolf.targetY=wolf.homeY; wolf.px=wolf.targetX*TILE; wolf.py=wolf.targetY*TILE;
      wolfRespawnAtById[wolf.id]=0;
      log("Wolf #" + wolf.id + " prowls back into the clearing.");
    }
    return;
  }
  if(now-(lastWolfDecisionAt[wolf.id]||0)<650) return;
  lastWolfDecisionAt[wolf.id]=now;
  if(isHostileAggroBlocked(now)) return;
  const dx=player.targetX-wolf.targetX, dy=player.targetY-wolf.targetY, dist=Math.abs(dx)+Math.abs(dy);
  if(dist<=4){
    const sx=dx===0?0:dx>0?1:-1, sy=dy===0?0:dy>0?1:-1;
    const a={x:wolf.targetX+sx,y:wolf.targetY}, b={x:wolf.targetX,y:wolf.targetY+sy};
    if(Math.abs(dx)>=Math.abs(dy)&&canHostileMoveTo(a.x,a.y,wolf)){ wolf.targetX=a.x; wolf.targetY=a.y; if(sx!==0) wolf.facing=sx>0?"right":"left"; }
    else if(canHostileMoveTo(b.x,b.y,wolf)){ wolf.targetY=b.y; if(sy!==0) wolf.facing=sy>0?"down":"up"; }
  } else {
    const backX=wolf.targetX<wolf.homeX?1:wolf.targetX>wolf.homeX?-1:0;
    const backY=wolf.targetY<wolf.homeY?1:wolf.targetY>wolf.homeY?-1:0;
    if(Math.abs(wolf.targetX-wolf.homeX)>wolf.roam&&canHostileMoveTo(wolf.targetX+backX,wolf.targetY,wolf)){ wolf.targetX+=backX; if(backX!==0) wolf.facing=backX>0?"right":"left"; }
    if(Math.abs(wolf.targetY-wolf.homeY)>wolf.roam&&canHostileMoveTo(wolf.targetX,wolf.targetY+backY,wolf)){ wolf.targetY+=backY; if(backY!==0) wolf.facing=backY>0?"down":"up"; }
  }
}
function updateBandit(bandit,now){
  if(bandit.hp<=0){
    const respawnAt=banditRespawnAtById[bandit.id]||0;
    if(respawnAt!==0&&now>=respawnAt){
      bandit.hp=bandit.maxHp;
      bandit.defeated=false;
      bandit.targetX=bandit.homeX; bandit.targetY=bandit.homeY; bandit.px=bandit.targetX*TILE; bandit.py=bandit.targetY*TILE;
      banditRespawnAtById[bandit.id]=0;
      log("Bandit #" + bandit.id + " stalks back toward Mirror Pond.");
    }
    return;
  }
  if(now-(lastBanditDecisionAt[bandit.id]||0)<850) return;
  lastBanditDecisionAt[bandit.id]=now;
  if(isHostileAggroBlocked(now)) return;
  const dx=player.targetX-bandit.targetX, dy=player.targetY-bandit.targetY, dist=Math.abs(dx)+Math.abs(dy);
  if(dist<=4){
    const sx=dx===0?0:dx>0?1:-1, sy=dy===0?0:dy>0?1:-1;
    const a={x:bandit.targetX+sx,y:bandit.targetY}, b={x:bandit.targetX,y:bandit.targetY+sy};
    if(Math.abs(dx)>=Math.abs(dy)&&canHostileMoveTo(a.x,a.y,bandit)){ bandit.targetX=a.x; bandit.targetY=a.y; if(sx!==0) bandit.facing=sx>0?"right":"left"; }
    else if(canHostileMoveTo(b.x,b.y,bandit)){ bandit.targetY=b.y; if(sy!==0) bandit.facing=sy>0?"down":"up"; }
  } else {
    const backX=bandit.targetX<bandit.homeX?1:bandit.targetX>bandit.homeX?-1:0;
    const backY=bandit.targetY<bandit.homeY?1:bandit.targetY>bandit.homeY?-1:0;
    if(Math.abs(bandit.targetX-bandit.homeX)>bandit.roam&&canHostileMoveTo(bandit.targetX+backX,bandit.targetY,bandit)){ bandit.targetX+=backX; if(backX!==0) bandit.facing=backX>0?"right":"left"; }
    if(Math.abs(bandit.targetY-bandit.homeY)>bandit.roam&&canHostileMoveTo(bandit.targetX,bandit.targetY+backY,bandit)){ bandit.targetY+=backY; if(backY!==0) bandit.facing=backY>0?"down":"up"; }
  }
}
function wolfAttack(now){
  if(isHostileAggroBlocked(now)) return;
  for(const wolf of getActiveHostiles().filter((hostile)=>hostile.kind==="wolf")){
    if(wolf.hp<=0) continue;
    const dist=Math.abs(player.targetX-wolf.targetX)+Math.abs(player.targetY-wolf.targetY);
    if(dist>1||now-(lastWolfAttackAt[wolf.id]||0)<WOLF_ATTACK_COOLDOWN_MS) continue;
    lastWolfAttackAt[wolf.id]=now;
    wolf.attackUntil=now+350;
    const damageDealt=applyIncomingDamage(5); player.hitUntil=now+300; player.hitFlickerUntil=now+220; hitStopUntil=now+55;
    const wx=player.targetX-wolf.targetX, wy=player.targetY-wolf.targetY, len=Math.max(1,Math.hypot(wx,wy));
    wolf.attackLungeX=(wx/len)*2; wolf.attackLungeY=(wy/len)*1.2; player.recoilX=(wx/len)*2.5; player.recoilY=(wy/len)*1.6;
    logThrottled("combat:wolf_bite:" + wolf.id, "Wolf #" + wolf.id + " bites you for " + damageDealt + " damage.", 1500);
    if(player.hp<=0){ handlePlayerDefeat(); break; }
  }
}
function banditAttack(now){
  if(isHostileAggroBlocked(now)) return;
  for(const bandit of bandits){
    if(bandit.hp<=0) continue;
    const dist=Math.abs(player.targetX-bandit.targetX)+Math.abs(player.targetY-bandit.targetY);
    if(dist>1||now-(lastBanditAttackAt[bandit.id]||0)<BANDIT_ATTACK_COOLDOWN_MS) continue;
    lastBanditAttackAt[bandit.id]=now;
    bandit.attackUntil=now+350;
    const damageDealt=applyIncomingDamage(7); player.hitUntil=now+320; player.hitFlickerUntil=now+260; hitStopUntil=now+60;
    const wx=player.targetX-bandit.targetX, wy=player.targetY-bandit.targetY, len=Math.max(1,Math.hypot(wx,wy));
    bandit.attackLungeX=(wx/len)*2.2; bandit.attackLungeY=(wy/len)*1.3; player.recoilX=(wx/len)*2.8; player.recoilY=(wy/len)*1.8;
    logThrottled("combat:bandit_slash:" + bandit.id, "Bandit #" + bandit.id + " slashes you for " + damageDealt + " damage.", 1700);
    if(player.hp<=0){ handlePlayerDefeat(); break; }
  }
}
function defeatWolf(wolf,now){
  wolf.defeated=true;
  player.xp+=12;
  player.coins+=4;
  const lootDrops=rollWolfLoot();
  lootDrops.forEach((drop)=>addItemToInventory(drop.itemId, drop.quantity));
  wolfRespawnAtById[wolf.id]=now+WOLF_RESPAWN_MS;
  log("Wolf #" + wolf.id + " defeated. Rewards: +12 XP, +4 coins.");
  eventSystem.emit("combat:enemy-defeated",{ enemyType:"wolf", enemyId:wolf.id });
  if(lootDrops.length) log("Loot acquired: " + formatDropText(lootDrops) + ".");
  else log("No loot dropped this time.");
}
function defeatBandit(bandit,now){
  bandit.defeated=true;
  player.xp+=16;
  player.coins+=6;
  const lootDrops=rollBanditLoot();
  lootDrops.forEach((drop)=>addItemToInventory(drop.itemId, drop.quantity));
  banditRespawnAtById[bandit.id]=now+BANDIT_RESPAWN_MS;
  log("Bandit #" + bandit.id + " defeated. Rewards: +16 XP, +6 coins.");
  if(lootDrops.length) log("Loot acquired: " + formatDropText(lootDrops) + ".");
  else log("No loot dropped this time.");
}
function tryPlayerAttack(now){
  if(dialogueSystem.activeSession) return;
  if(now<zoneTransitionLockedUntil) return;
  if(!(keys.has(" ")||keys.has("space"))) return;
  if(now-lastPlayerAttack<420) return;
  lastPlayerAttack=now; player.attackUntil=now+350;
  const targetHostile=getNearestHostile(PLAYER_ATTACK_RANGE);
  if(!targetHostile){
    if(missNoticeArmed && now-lastNoTargetLogAt>900){
      logThrottled("combat:miss_no_target", "Attack misses: no hostile in range.", 1800);
      lastNoTargetLogAt=now;
      missNoticeArmed=false;
    }
    return;
  }
  missNoticeArmed=false;
  const tx=targetHostile.entity.targetX-player.targetX;
  const ty=targetHostile.entity.targetY-player.targetY;
  const len=Math.max(1,Math.hypot(tx,ty));
  player.attackLungeX=(tx/len)*2.4;
  player.attackLungeY=(ty/len)*1.4;
  const totalDamage=BASE_PLAYER_DAMAGE + getEquippedWeaponBonus();
  targetHostile.entity.hp=Math.max(0,targetHostile.entity.hp-totalDamage);
  targetHostile.entity.hitUntil=now+320;
  targetHostile.entity.hitFlickerUntil=now+240;
  targetHostile.entity.recoilX=(tx/len)*2.3;
  targetHostile.entity.recoilY=(ty/len)*1.5;
  hitStopUntil=now+65;
  const label=targetHostile.entity.kind==="bandit" ? "Bandit" : "Wolf";
  log("Hit " + label + " #" + targetHostile.entity.id + " for " + totalDamage + " damage.");
  if(targetHostile.entity.hp<=0 && !targetHostile.entity.defeated){
    if(targetHostile.entity.kind==="bandit") defeatBandit(targetHostile.entity, now);
    else defeatWolf(targetHostile.entity, now);
  }
}

// Keep color construction backtick-free inside this String.raw payload to avoid
// terminating the outer template literal used for the HTML document.
function rgba(r,g,b,a){ return "rgba(" + r + "," + g + "," + b + "," + a + ")"; }

function drawSoftShadow(cx,cy,rx,ry,a=.2){
  const g=ctx.createRadialGradient(cx+3,cy+3,Math.max(1,rx*.35),cx+3,cy+3,Math.max(rx,ry)*1.3);
  g.addColorStop(0,"rgba(0,0,0," + (a*.86).toFixed(3) + ")"); g.addColorStop(1,"rgba(0,0,0,0)");
  ctx.fillStyle=g; ctx.beginPath(); ctx.ellipse(cx+3,cy+3,rx,ry,0,0,Math.PI*2); ctx.fill();
}

function frameFromSprite(dir,moving){
  const row = dir==="down"?0:dir==="left"?1:dir==="right"?2:3;
  if(!moving) return {sx:0, sy:row*64};
  const col = (Math.floor(performance.now()/110)%3) + 1;
  return {sx:col*64, sy:row*64};
}

function drawHumanoid(sheet, tx, ty, facing, moving, scale, label, hitAlpha, recoil, attackData){
  const p = tileToScreen(tx,ty);
  const shiftX = Math.round((recoil?.x||0) + ((attackData&&attackData.active)?attackData.thrust:0));
  const shiftY = Math.round((recoil?.y||0) - ((attackData&&attackData.active)?Math.abs(attackData.thrust)*.2:0));
  const drawW = Math.round(64*scale), drawH = Math.round(64*scale);
  const dx = p.x + Math.round((32-drawW)/2) + shiftX;
  const dy = p.y - Math.round(drawH-32) + shiftY;
  drawShadowTile(assets.shadow.oval, p.x+3, p.y+4, .82);

  const fr = frameFromSprite(facing, moving);
  if (sheet.complete && sheet.naturalWidth>0) {
    ctx.drawImage(sheet, fr.sx, fr.sy, 64, 64, dx, dy, drawW, drawH);
  }

  if (label) {
    const w = Math.max(56,label.length*7+9);
    ctx.fillStyle = "rgba(7,11,18,.86)"; ctx.fillRect(p.x-12,p.y-20,w,14);
    ctx.strokeStyle = "rgba(211,224,242,.45)"; ctx.strokeRect(p.x-12.5,p.y-20.5,w,14);
    ctx.fillStyle = "#f6fbff"; ctx.font = "bold 11px monospace"; ctx.fillText(label,p.x-8,p.y-10);
  }
  if (hitAlpha>0) {
    ctx.fillStyle="rgba(255,86,86," + Math.min(.45,hitAlpha).toFixed(3) + ")"; ctx.fillRect(dx+8,dy+7,drawW-16,drawH-12);
  }
  if (attackData && attackData.active) {
    ctx.strokeStyle = "rgba(231,247,255,.35)"; ctx.lineWidth = 2;
    ctx.beginPath();
    if (facing==="left") ctx.arc(dx+20,dy+35,16,Math.PI*.64,Math.PI*1.24);
    else if (facing==="right") ctx.arc(dx+drawW-20,dy+35,16,Math.PI*-.25,Math.PI*.38);
    else if (facing==="up") ctx.arc(dx+drawW/2,dy+24,15,Math.PI*1.12,Math.PI*1.84);
    else ctx.arc(dx+drawW/2,dy+44,15,Math.PI*.16,Math.PI*.84);
    ctx.stroke();
  }
}

function rectsOverlap(a,b){
  return a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y;
}

function drawWorldLabels(entries){
  const occupied=[];
  entries
    .filter((entry)=>Boolean(entry?.text))
    .sort((a,b)=>(b.priority||0)-(a.priority||0))
    .forEach((entry)=>{
      const text=entry.text;
      const w=Math.max(56,text.length*7+9);
      const h=14;
      const p=tileToScreen(entry.tx, entry.ty);
      let y=p.y-20;
      const x=p.x-12;
      for(let i=0;i<8;i++){
        const rect={x,y,w,h};
        if(!occupied.some((other)=>rectsOverlap(rect, other))){
          occupied.push(rect);
          ctx.fillStyle="rgba(7,11,18,.86)"; ctx.fillRect(rect.x,rect.y,rect.w,rect.h);
          ctx.strokeStyle="rgba(211,224,242,.45)"; ctx.strokeRect(rect.x-.5,rect.y-.5,rect.w,rect.h);
          ctx.fillStyle="#f6fbff"; ctx.font="bold 11px monospace"; ctx.fillText(text,rect.x+4,rect.y+10);
          return;
        }
        y -= 16;
      }
    });
}

function drawWolf(wolf,tx,ty,facing,moving,scale,hitAlpha,recoil){
  const row = ({down:0,left:1,right:2,up:3})[facing] ?? 0;
  const p=tileToScreen(tx,ty);
  const col=!moving?0:((Math.floor(performance.now()/120)%3)+1);
  const drawW=Math.round(64*scale),drawH=Math.round(64*scale);
  const dx=p.x+Math.round((32-drawW)/2)+Math.round(recoil?.x||0), dy=p.y-Math.round(drawH-32)+Math.round(recoil?.y||0);
  drawShadowTile(assets.shadow.oval, p.x+4, p.y+4, .76);
  if(assets.sprites.wolf.complete&&assets.sprites.wolf.naturalWidth>0) ctx.drawImage(assets.sprites.wolf,col*64,row*64,64,64,dx,dy,drawW,drawH);
  ctx.fillStyle=rgba(0,0,0,.5); ctx.fillRect(p.x+2,p.y-10,24,4);
  ctx.fillStyle="#8fdb73"; ctx.fillRect(p.x+2,p.y-10,24*(wolf.hp/wolf.maxHp),4);
  if(hitAlpha>0){ ctx.fillStyle="rgba(255,255,255," + Math.min(.4,hitAlpha).toFixed(3) + ")"; ctx.fillRect(dx+8,dy+8,drawW-14,drawH-16); }
}

function hitVisualAlpha(e){ const now=performance.now(); if(now>=e.hitUntil) return 0; const left=e.hitUntil-now; const base=Math.min(.52,.2+left/300); const flick=now<e.hitFlickerUntil&&Math.floor(now/36)%2===0?.24:0; return Math.max(0,base+flick); }
function attackPose(entity){ const now=performance.now(); const total=350; const left=Math.max(0,entity.attackUntil-now); if(left<=0) return {active:false,thrust:0}; const t=(total-left)/total; return {active:true,thrust:Math.sin(t*Math.PI)*3.5}; }

function drawAlignmentGrid(){ const cam=getCamera(); const sx=cam.offsetX, sy=cam.offsetY, ex=sx+VIEW_TILES_X*TILE, ey=sy+VIEW_TILES_Y*TILE; ctx.save(); ctx.strokeStyle="rgba(221,233,255,.16)"; ctx.lineWidth=1; ctx.beginPath(); for(let x=0;x<=VIEW_TILES_X;x++){ const px=sx+x*TILE+.5; ctx.moveTo(px,sy); ctx.lineTo(px,ey);} for(let y=0;y<=VIEW_TILES_Y;y++){ const py=sy+y*TILE+.5; ctx.moveTo(sx,py); ctx.lineTo(ex,py);} ctx.stroke(); ctx.restore(); }
function drawTileRotated(img, x, y, turns){
  if(!img||!img.complete||img.naturalWidth<=0) return;
  ctx.save();
  ctx.translate(x+16,y+16);
  ctx.rotate((Math.PI/2)*turns);
  ctx.drawImage(img,-16,-16,32,32);
  ctx.restore();
}
function drawShadowTile(img, x, y, alpha=1){
  if(!img || !img.complete || img.naturalWidth<=0) return;
  const oldAlpha = ctx.globalAlpha;
  ctx.globalAlpha = oldAlpha * alpha;
  ctx.drawImage(img, x, y, 32, 32);
  ctx.globalAlpha = oldAlpha;
}

function drawTransitionFade(now){
  if(!transitionFade) return;
  if(!transitionState.active){
    transitionFade.style.background="rgba(2,6,10,0)";
    return;
  }
  const elapsed=now-transitionState.start;
  const half=Math.max(1, transitionState.duration/2);
  const t=Math.min(1, elapsed/half);
  let alpha=transitionState.switched ? (1-t) : t;
  alpha=Math.max(0,Math.min(1,alpha));
  transitionFade.style.background="rgba(2,6,10," + alpha.toFixed(3) + ")";
}

function drawMirrorCaveScene(now){
  ctx.clearRect(0,0,canvas.width,canvas.height);
  const cam=getCamera();
  for(let y=cam.tileY;y<cam.tileY+VIEW_TILES_Y;y++) for(let x=cam.tileX;x<cam.tileX+VIEW_TILES_X;x++){
    const p=tileToScreen(x,y);
    const k=keyOf(x,y);
    if(!isTileInCurrentZone(x,y)) continue;
    const noise=rng(x,y,222);
    if(mirrorCave.blocked.has(k)){
      ctx.fillStyle=noise>0.5 ? "#1b1f28" : "#161a22";
    } else {
      ctx.fillStyle=noise>0.5 ? "#3c4048" : "#353941";
    }
    ctx.fillRect(p.x,p.y,32,32);
    if(mirrorCave.walls.has(k)){
      ctx.fillStyle="rgba(112,119,133,.22)";
      ctx.fillRect(p.x,p.y,32,6);
    }
  }
  if(!mirrorCave.chest.opened){
    const cp=tileToScreen(mirrorCave.chest.x, mirrorCave.chest.y);
    drawSoftShadow(cp.x+16,cp.y+26,10,4,.2);
    ctx.fillStyle="#6b4c2f"; ctx.fillRect(cp.x+6,cp.y+10,20,14);
    ctx.fillStyle="#b58f56"; ctx.fillRect(cp.x+6,cp.y+10,20,4);
    ctx.fillStyle="#d6bc7f"; ctx.fillRect(cp.x+14,cp.y+14,4,6);
  }
  const ep=tileToScreen(mirrorCave.exit.x, mirrorCave.exit.y);
  ctx.fillStyle="rgba(155,170,189,.2)"; ctx.fillRect(ep.x+4,ep.y+4,24,24);
  ctx.strokeStyle="rgba(199,214,236,.5)"; ctx.strokeRect(ep.x+4.5,ep.y+4.5,23,23);
  ctx.fillStyle="#c7d6ec"; ctx.font="bold 10px monospace"; ctx.fillText("EXIT", ep.x+6, ep.y+19);

  mirrorCaveWolves.forEach((wolf)=>{
    if(wolf.hp<=0) return;
    drawWolf(wolf, wolf.px/TILE, wolf.py/TILE, wolf.facing, wolf.moving, 0.82, hitVisualAlpha(wolf), {x:wolf.recoilX+wolf.attackLungeX,y:wolf.recoilY+wolf.attackLungeY});
  });
  drawHumanoid(assets.sprites.player, player.px/TILE, player.py/TILE, player.facing, player.moving, 0.84, "Wayfarer", hitVisualAlpha(player), {x:player.recoilX+player.attackLungeX,y:player.recoilY+player.attackLungeY}, attackPose(player));
  ctx.fillStyle="rgba(8,10,14,.2)"; ctx.fillRect(0,0,canvas.width,canvas.height);
  drawTransitionFade(now);
}

function drawWorld(){
  const now=performance.now();
  if(isInMirrorCave){
    drawMirrorCaveScene(now);
    return;
  }
  ctx.clearRect(0,0,canvas.width,canvas.height);
  const cam=getCamera();
  for(let y=cam.tileY;y<cam.tileY+VIEW_TILES_Y;y++) for(let x=cam.tileX;x<cam.tileX+VIEW_TILES_X;x++){
    const mix=Math.floor(rng(x,y,4)*assets.grass.length);
    const p=tileToScreen(x,y);
    const img=assets.grass[mix];
    if(img.complete&&img.naturalWidth>0) ctx.drawImage(img,p.x,p.y,TILE,TILE);
  }

  world.roads.forEach(r=>{ for(let x=r.x;x<r.x+r.w;x++) for(let y=r.y;y<r.y+r.h;y++){
    const p=tileToScreen(x,y);
    const img=assets.road[Math.floor(rng(x,y,22)*assets.road.length)];
    if(img.complete&&img.naturalWidth>0) ctx.drawImage(img,p.x,p.y,32,32);

    const north = world.roadTiles.has(keyOf(x,y-1));
    const south = world.roadTiles.has(keyOf(x,y+1));
    const east = world.roadTiles.has(keyOf(x+1,y));
    const west = world.roadTiles.has(keyOf(x-1,y));
    if(!north) drawTileRotated(assets.roadEdge[Math.floor(rng(x,y,62)*assets.roadEdge.length)], p.x, p.y, 0);
    if(!east) drawTileRotated(assets.roadEdge[Math.floor(rng(x,y,64)*assets.roadEdge.length)], p.x, p.y, 1);
    if(!south) drawTileRotated(assets.roadEdge[Math.floor(rng(x,y,66)*assets.roadEdge.length)], p.x, p.y, 2);
    if(!west) drawTileRotated(assets.roadEdge[Math.floor(rng(x,y,68)*assets.roadEdge.length)], p.x, p.y, 3);
  } });

  for(let x=pond.x-1;x<=pond.x+pond.w;x++) for(let y=pond.y-1;y<=pond.y+pond.h;y++){
    const k=keyOf(x,y); if(!world.pondWater.has(k)) continue;
    const p=tileToScreen(x,y); const edge=world.pondNearEdge.has(k);
    const img=edge?assets.water.shallow:assets.water.deep; if(img.complete&&img.naturalWidth>0) ctx.drawImage(img,p.x,p.y,32,32);
    const t=performance.now()*0.002, rip=(Math.sin(t*3+x*1.1+y*.8)+1)*.5;
    ctx.fillStyle="rgba(188,228,255," + (.02+rip*.05).toFixed(3) + ")"; ctx.fillRect(p.x+3,p.y+6,TILE-10,1);
    if(edge){
      ctx.fillStyle="rgba(224,244,255," + (.05+rip*.05).toFixed(3) + ")"; ctx.fillRect(p.x+1,p.y+1,TILE-2,1);
      if(assets.water.edge.complete&&assets.water.edge.naturalWidth>0) ctx.drawImage(assets.water.edge,p.x,p.y,32,32);
    }
  }
  for(let x=pond.x-1;x<=pond.x+pond.w;x++) for(let y=pond.y-1;y<=pond.y+pond.h;y++){
    const k=keyOf(x,y); if(!world.pondShore.has(k)) continue;
    const p=tileToScreen(x,y); const img=assets.shore[Math.floor(rng(x,y,33)*assets.shore.length)]; if(img.complete&&img.naturalWidth>0) ctx.drawImage(img,p.x,p.y,32,32);
  }

  world.buildings.forEach(b=>{
    for(let ry=0; ry<b.h; ry++){
      const right = tileToScreen(b.x+b.w, b.y+ry);
      drawShadowTile(assets.shadow.buildingRight, right.x+4, right.y+3, .9);
    }
    for(let rx=0; rx<b.w; rx++){
      const bottom = tileToScreen(b.x+rx, b.y+b.h);
      drawShadowTile(assets.shadow.buildingBottom, bottom.x+4, bottom.y+3, .88);
    }
    b.tileRows.forEach((row,ry)=> row.forEach((key,rx)=> { const p=tileToScreen(b.x+rx,b.y+ry); const img=assets.building[key]; if(img&&img.complete&&img.naturalWidth>0) ctx.drawImage(img,p.x,p.y,32,32); }));
  });

  world.props.forEach((prop)=>{
    const p = tileToScreen(prop.x,prop.y);
    const img = assets.props.sprites[prop.type];
    if(!img || !img.complete || img.naturalWidth<=0) return;
    if(prop.type==="barrel"||prop.type==="crate") drawShadowTile(assets.shadow.softTile,p.x+3,p.y+4,.78);
    if(prop.type==="sack"||prop.type==="stonePile") drawSoftShadow(p.x+16,p.y+26,8,3,.16);
    if(prop.type==="bush"||prop.type==="grassTuft") drawSoftShadow(p.x+16,p.y+26,9,4,.14);
    if(prop.type==="well"||prop.type==="lanternPost"||prop.type==="signPost") drawSoftShadow(p.x+16,p.y+27,10,4,.19);
    ctx.drawImage(img,p.x,p.y,32,32);
  });
  const caveEntrancePos=tileToScreen(OVERWORLD_CAVE_ENTRY.x, OVERWORLD_CAVE_ENTRY.y);
  ctx.fillStyle="rgba(26,30,38,.86)";
  ctx.beginPath();
  ctx.moveTo(caveEntrancePos.x+6,caveEntrancePos.y+26);
  ctx.lineTo(caveEntrancePos.x+16,caveEntrancePos.y+8);
  ctx.lineTo(caveEntrancePos.x+26,caveEntrancePos.y+26);
  ctx.closePath();
  ctx.fill();
  ctx.strokeStyle="rgba(151,164,182,.65)";
  ctx.stroke();

  world.fences.forEach((f,i)=>{
    const p=tileToScreen(f.x,f.y);
    drawShadowTile(assets.shadow.softTile,p.x+4,p.y+4,.56);
    const img=assets.fence[i%assets.fence.length];
    if(img.complete&&img.naturalWidth>0) ctx.drawImage(img,p.x,p.y,32,32);
  });
  world.trees.forEach(t=>{
    const p=tileToScreen(t.x,t.y);
    const sway=Math.sin(performance.now()*0.0012+t.seed*8)*0.8;
    drawShadowTile(assets.shadow.treeCircle,p.x+2,p.y+2,.72);
    const img=assets.tree[t.type]||assets.tree.a;
    if(img.complete&&img.naturalWidth>0) ctx.drawImage(img,p.x+Math.round(sway),p.y-4,32,36);
  });

  for(let y=cam.tileY;y<cam.tileY+VIEW_TILES_Y;y++) for(let x=cam.tileX;x<cam.tileX+VIEW_TILES_X;x++){
    const k = keyOf(x,y);
    if(world.roadTiles.has(k) || world.pondWater.has(k) || world.pondShore.has(k) || world.pondNearEdge.has(k) || world.blocked.has(k)) continue;
    const chance = rng(x,y,131);
    if(chance > 0.085) continue;
    const p = tileToScreen(x,y);
    const detail = assets.detail[Math.floor(rng(x,y,137)*assets.detail.length)];
    if(detail && detail.complete && detail.naturalWidth>0) ctx.drawImage(detail,p.x,p.y,32,32);
  }

  if(showGrid) drawAlignmentGrid();

  function zoneLabel(text,tx,ty){ const p=tileToScreen(tx,ty); const w=text.length*7+12; ctx.fillStyle="rgba(7,11,18,.85)"; ctx.fillRect(p.x-3,p.y-31,w,16); ctx.strokeStyle="rgba(204,216,236,.62)"; ctx.strokeRect(p.x-3.5,p.y-31.5,w,16); ctx.fillStyle="#eff4ff"; ctx.font="bold 11px monospace"; ctx.fillText(text,p.x+2,p.y-19); }
  const zoneName=currentLocalAreaName();
  if(zoneName==="Hearthvale Square") zoneLabel("Hearthvale Square",12,7);
  if(zoneName==="Mirror Pond") zoneLabel("Mirror Pond",23,12);
  if(zoneName==="Eastern Woods") zoneLabel("Eastern Woods",30,4);

  drawHumanoid(assets.sprites.npc, npc.x, npc.y, npc.facing, false, 0.78, "", 0, null, null);
  drawHumanoid(assets.sprites.npc, hunterNpc.x, hunterNpc.y, hunterNpc.facing, false, 0.78, "", 0, null, null);
  drawHumanoid(assets.sprites.npc, vendorNpc.x, vendorNpc.y, vendorNpc.facing, false, 0.78, "", 0, null, null);
  wolves.forEach((wolf)=>{
    if(wolf.hp<=0) return;
    drawWolf(wolf, wolf.px/TILE, wolf.py/TILE, wolf.facing, wolf.moving, 0.82, hitVisualAlpha(wolf), {x:wolf.recoilX+wolf.attackLungeX,y:wolf.recoilY+wolf.attackLungeY});
  });
  bandits.forEach((bandit)=>{
    if(bandit.hp<=0) return;
    drawWolf(bandit, bandit.px/TILE, bandit.py/TILE, bandit.facing, bandit.moving, 0.84, hitVisualAlpha(bandit), {x:bandit.recoilX+bandit.attackLungeX,y:bandit.recoilY+bandit.attackLungeY});
  });
  drawHumanoid(assets.sprites.player, player.px/TILE, player.py/TILE, player.facing, player.moving, 0.84, "", hitVisualAlpha(player), {x:player.recoilX+player.attackLungeX,y:player.recoilY+player.attackLungeY}, attackPose(player));
  drawWorldLabels([
    {text:Math.abs(player.targetX-npc.x)+Math.abs(player.targetY-npc.y)<=5 ? npc.name : "", tx:npc.x, ty:npc.y, priority:3},
    {text:Math.abs(player.targetX-hunterNpc.x)+Math.abs(player.targetY-hunterNpc.y)<=5 ? hunterNpc.displayLabel : "", tx:hunterNpc.x, ty:hunterNpc.y, priority:3},
    {text:Math.abs(player.targetX-vendorNpc.x)+Math.abs(player.targetY-vendorNpc.y)<=5 ? vendorNpc.displayLabel : "", tx:vendorNpc.x, ty:vendorNpc.y, priority:3},
    {text:"Wayfarer", tx:player.px/TILE, ty:player.py/TILE, priority:1}
  ]);

  const tint=0.08+Math.max(0,Math.sin(performance.now()/9000))*.07;
  ctx.fillStyle="rgba(9,16,26," + tint.toFixed(3) + ")"; ctx.fillRect(0,0,canvas.width,canvas.height);
  const edge=ctx.createRadialGradient(canvas.width*.5,canvas.height*.5,Math.min(canvas.width,canvas.height)*.35,canvas.width*.5,canvas.height*.5,Math.max(canvas.width,canvas.height)*.68);
  edge.addColorStop(0,"rgba(0,0,0,0)"); edge.addColorStop(.78,"rgba(1,6,10,.1)"); edge.addColorStop(1,"rgba(1,6,10,.46)");
  ctx.fillStyle=edge; ctx.fillRect(0,0,canvas.width,canvas.height);
  drawTransitionFade(now);
}

function update(dt,now){
  if(transitionState.active){
    const elapsed=now-transitionState.start;
    if(!transitionState.switched && elapsed>=transitionState.duration/2){
      transitionState.switched=true;
      transitionState.onSwitch?.();
    }
    if(elapsed>=transitionState.duration){
      transitionState.active=false;
    }
  }
  player.recoilX*=.8; player.recoilY*=.8; player.attackLungeX*=.74; player.attackLungeY*=.74;
  wolves.forEach((wolf)=>{
    wolf.recoilX*=.82; wolf.recoilY*=.82; wolf.attackLungeX*=.78; wolf.attackLungeY*=.78;
  });
  bandits.forEach((bandit)=>{
    bandit.recoilX*=.82; bandit.recoilY*=.82; bandit.attackLungeX*=.78; bandit.attackLungeY*=.78;
  });
  if(now<hitStopUntil){ updateSidebar(); return; }
  eventSystem.update(currentLocalAreaName());
  const isTransitionLocked=now<zoneTransitionLockedUntil;
  if(!isTransitionLocked) updateInput();
  tryPlayerAttack(now);
  smoothMove(player,dt);
  if(!player.moving) handleZoneTransitionIfNeeded();
  if(!isTransitionLocked && !player.moving && (moveIntent.dx!==0||moveIntent.dy!==0)) tryPlayerStep(moveIntent.dx,moveIntent.dy,moveIntent.facing);
  updateOutdoorRegionFromPosition(true);
  if(!isTransitionLocked){
    if(isInMirrorCave){
      mirrorCaveWolves.forEach((wolf)=>{ updateWolf(wolf,now); smoothMove(wolf,dt); });
    } else {
      wolves.forEach((wolf)=>{ updateWolf(wolf,now); smoothMove(wolf,dt); });
      bandits.forEach((bandit)=>{ updateBandit(bandit,now); smoothMove(bandit,dt); });
      banditAttack(now);
    }
    wolfAttack(now);
  }
  updateSidebar();
}

let last=performance.now();
function loop(now){ const dt=Math.min(.033,(now-last)/1000); last=now; update(dt,now); drawWorld(); requestAnimationFrame(loop); }

const loadedFromSave=loadGame();
updateDialogueViewportConstraints();
ensureStarterEquipment();
log("System: Artistic rebuild slice loaded.");
if(loadedFromSave) log("System: Continuing from saved progress.");
else log("System: New journey started.");
log("System: Press K at any time to save manually.");
log("System: Speak to Edrin Vale and use E to interact with nearby objects.");
log("System: Hunter Garran waits near Hearthvale's eastern road.");
log("System: Merchant Rowan now buys and sells survival goods.");
updateSidebar();
requestAnimationFrame(loop);
</script>
</body>
</html>`;
