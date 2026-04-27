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
    #gamePanel, #game, #hud, #dialogue, #vendorPanel, #inventoryPanel, #equipmentPanel, #stats, #logPanel, #brand {
      user-select: none;
      -webkit-user-select: none;
    }
    body {
      margin:0;
      background: radial-gradient(circle at 26% -12%, #263248 0%, #0a1119 56%);
      color: var(--text);
      font-family: "Trebuchet MS", Verdana, sans-serif;
      overflow: hidden;
    }
    #wrap {
      display:grid;
      grid-template-columns: 320px 1fr;
      gap:14px;
      height:100dvh;
      padding:14px;
    }
    .panel {
      background: linear-gradient(#141f2f, #0e1621);
      border: 1px solid #3b4d66;
      border-radius: 12px;
      box-shadow: 0 14px 40px rgba(0,0,0,.46), inset 0 0 0 1px rgba(255,255,255,.03);
    }
    #sidebar {
      display:flex;
      flex-direction:column;
      gap:8px;
      min-width:0;
      min-height:0;
      height:100%;
      overflow:hidden;
      position:relative;
      z-index:5;
    }
    #brand,#stats{padding:12px;}
    #sidebarLower{
      display:flex;
      flex-direction:column;
      flex:1 1 auto;
      min-height:0;
      overflow:hidden;
      padding:10px;
      gap:10px;
    }
    #sidebarTabs{
      display:grid;
      grid-template-columns:repeat(4, minmax(0, 1fr));
      gap:6px;
      flex:0 0 auto;
      position:relative;
      z-index:2;
    }
    .sidebar-tab{
      border:1px solid #607798;
      border-radius:7px;
      background:#172436;
      color:#c7d6ec;
      font:11px ui-monospace,SFMono-Regular,Menlo,monospace;
      padding:5px 6px;
      cursor:pointer;
      white-space:nowrap;
    }
    .sidebar-tab.active{
      background:#29415f;
      color:#f0f6ff;
      border-color:#6d87ab;
    }
    #sidebarTabPanels{
      flex:1 1 auto;
      min-height:0;
      overflow:hidden;
      position:relative;
      z-index:1;
    }
    .sidebar-tab-panel{
      display:none;
      flex-direction:column;
      min-height:0;
      height:100%;
      padding:2px;
    }
    .sidebar-tab-panel.active{display:flex;}
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
      min-height:0;
      max-height:none;
      overflow-y:auto;
      padding:8px 9px;
      white-space:pre-line;
      font:12px/1.5 ui-monospace,SFMono-Regular,Menlo,monospace;
      color:#d2dded;
      flex:1 1 auto;
    }
    #objectiveText{
      line-height:1.4;
      white-space:normal;
      overflow-wrap:anywhere;
    }
    #inventoryPanel,#equipmentPanel,#skillsPanel,#logPanel{
      flex-direction:column;
      min-height:0;
      height:100%;
      overflow:hidden;
      padding:10px;
    }
    #inventoryList{
      line-height:1.45;
      flex:1 1 auto;
      min-height:0;
      overflow-y:auto;
      padding-right:2px;
      display:flex;
      flex-direction:column;
      gap:6px;
    }
    .inventory-row{
      display:flex;
      align-items:center;
      justify-content:space-between;
      gap:8px;
      border-bottom:1px solid rgba(158,172,190,.14);
      padding-bottom:4px;
    }
    .inventory-row:last-child{border-bottom:none}
    .inventory-item-name{
      flex:1 1 auto;
      min-width:0;
      overflow-wrap:anywhere;
      color:#d8e3f3;
    }
    .inventory-actions{
      display:flex;
      align-items:center;
      gap:6px;
      flex:0 0 auto;
    }
    .inventory-btn{
      border:1px solid #4c6281;
      border-radius:6px;
      background:#162435;
      color:#e6ecf5;
      font:11px ui-monospace,SFMono-Regular,Menlo,monospace;
      padding:2px 7px;
      cursor:pointer;
      white-space:nowrap;
    }
    .inventory-btn:disabled{opacity:.55;cursor:not-allowed}
    .equipped-tag{
      border:1px solid #5d7899;
      border-radius:999px;
      padding:2px 7px;
      color:#cfe1fb;
      font-size:11px;
      white-space:nowrap;
    }
    #equipmentList,#skillsList{
      line-height:1.45;
      display:flex;
      flex-direction:column;
      gap:7px;
      flex:1 1 auto;
      min-height:0;
      overflow-y:auto;
      padding-right:2px;
    }
    .equipment-slot{
      display:flex;
      align-items:center;
      justify-content:space-between;
      gap:8px;
      border-bottom:1px solid rgba(158,172,190,.14);
      padding-bottom:4px;
    }
    .equipment-slot:last-child{border-bottom:none}
    .equipment-slot-label{color:#9eacbe}
    .equipment-slot-value{color:#d8e3f3;flex:1 1 auto;overflow-wrap:anywhere}
    .equipment-slot button{margin-left:8px}
    #logPanel{padding:10px;}
    #gamePanel{position:relative;overflow:hidden}
    #game{width:100%;height:100%;display:block;border-radius:12px;image-rendering:pixelated;background:#081017}
    #hud {
      box-shadow:0 8px 22px rgba(0,0,0,.32), inset 0 0 0 1px rgba(255,255,255,.05);
      position:absolute;top:12px;left:12px;white-space:pre-line;
      pointer-events:none;
      font:12px/1.5 ui-monospace,SFMono-Regular,Menlo,monospace;
      background:rgba(7,11,18,.84);
      border:1px solid #4c6281;
      border-radius:8px;
      padding:10px 12px;
      text-shadow:0 1px 0 #000;
      max-width:min(340px, calc(100% - 24px));
    }
    #debugPanel{
      position:absolute;top:12px;right:12px;white-space:pre-line;
      pointer-events:none;
      font:12px/1.45 ui-monospace,SFMono-Regular,Menlo,monospace;
      background:rgba(31,16,16,.9);
      border:1px solid #8d5964;
      border-radius:8px;
      padding:10px 12px;
      text-shadow:0 1px 0 #000;
      color:#f4d8de;
      max-width:min(320px, calc(100% - 24px));
      display:none;
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
    #dialogueActions{margin-top:8px;display:flex;gap:8px;justify-content:flex-end;flex-wrap:wrap}
    .dialogue-action{border:1px solid #4c6281;border-radius:8px;background:#162435;color:#e6ecf5;font:12px ui-monospace,SFMono-Regular,Menlo,monospace;padding:6px 10px;cursor:pointer}
    .dialogue-action:hover{background:#1b2d44}
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
    #rewardToast{
      position:absolute;
      left:50%;
      bottom:18px;
      transform:translateX(-50%) translateY(8px);
      opacity:0;
      pointer-events:none;
      z-index:36;
      transition:opacity .18s ease, transform .18s ease;
      font:12px/1.35 ui-monospace,SFMono-Regular,Menlo,monospace;
      background:rgba(10,18,27,.92);
      border:1px solid #4d6888;
      border-radius:8px;
      padding:7px 10px;
      box-shadow:0 8px 24px rgba(0,0,0,.4);
      white-space:pre-wrap;
      text-align:center;
    }
    #rewardToast.visible{
      opacity:1;
      transform:translateX(-50%) translateY(0);
    }
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
        <div class="stats" style="margin-top:10px;">
          <div class="muted">Current Objective</div><div id="objectiveText">Explore Hearthvale and the surrounding roads.</div>
          <div class="muted">Current Zone</div><div id="zoneVal">Hearthvale Square</div>
          <div class="muted">Quest</div><div id="questVal">Town Slice</div>
        </div>
      </section>
      <section id="stats" class="panel">
        <div class="stats">
          <div class="muted">Level</div><div id="levelVal">1</div>
          <div class="muted">HP</div><div id="hpVal">50/50</div>
          <div class="muted">XP</div><div id="xpVal">0 / 100</div>
          <div class="muted">Coins</div><div id="coinsVal">0</div>
          <div class="muted">Weapon</div><div id="weaponVal">Rusty Sword (+2)</div>
          <div class="muted">Armor</div><div id="armorVal">None</div>
          <div class="muted">Trinket</div><div id="trinketVal">None</div>
        </div>
      </section>
      <section id="sidebarLower" class="panel">
        <div id="sidebarTabs" role="tablist" aria-label="Sidebar sections">
          <button type="button" class="sidebar-tab active" data-sidebar-tab="inventory" role="tab" aria-selected="true">Inventory</button>
          <button type="button" class="sidebar-tab" data-sidebar-tab="equipment" role="tab" aria-selected="false">Equipment</button>
          <button type="button" class="sidebar-tab" data-sidebar-tab="skills" role="tab" aria-selected="false">Skills</button>
          <button type="button" class="sidebar-tab" data-sidebar-tab="chronicle" role="tab" aria-selected="false">Chronicle</button>
        </div>
        <div id="sidebarTabPanels">
          <section id="inventoryPanel" class="sidebar-tab-panel active" data-sidebar-panel="inventory" role="tabpanel">
            <div class="questTitle">Inventory</div>
            <div id="inventoryList" class="muted">Empty</div>
          </section>
          <section id="equipmentPanel" class="sidebar-tab-panel" data-sidebar-panel="equipment" role="tabpanel">
            <div class="questTitle">Equipment</div>
            <div id="equipmentList" class="muted">Weapon: Iron Sword (+5)<br>Armor: Leather Armor (+2 DEF)<br>Trinket: None</div>
          </section>
          <section id="skillsPanel" class="sidebar-tab-panel" data-sidebar-panel="skills" role="tabpanel">
            <div class="questTitle">Skills</div>
            <div id="skillsList" class="muted">Swordsmanship Lv 1 — 0 / 50<br>Defense Lv 1 — 0 / 50<br>Survival Lv 1 — 0 / 50</div>
          </section>
          <section id="logPanel" class="sidebar-tab-panel" data-sidebar-panel="chronicle" role="tabpanel">
            <div class="questTitle">Chronicle</div>
            <div id="chat"></div>
          </section>
        </div>
      </section>
    </aside>

    <main id="gamePanel" class="panel">
      <canvas id="game"></canvas>
      <div id="hud"></div>
      <div id="debugPanel"></div>
      <div id="dialogue">
        <div id="dialogueName"></div>
        <div id="dialogueText"></div>
        <div id="dialogueChoices"></div>
        <div id="dialogueHint">Click to continue. Press number keys for choices.</div>
        <div id="dialogueActions"></div>
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
      <div id="rewardToast" aria-live="polite"></div>
      <div id="transitionFade"></div>
      <script id="dialogueData" type="application/json">
{
  "characters": {
    "edrin": {
      "name": "Edrin Vale",
      "root": "greeting",
      "rootByCondition": [
        { "if": { "questId": "the_still_water", "state": "Completed" }, "next": "still_water_complete" },
        { "if": { "questId": "the_still_water", "state": "Ready To Turn In", "progress": "stage_6_return_to_edrin" }, "next": "still_water_final_turn_in" },
        { "if": { "questId": "the_still_water", "state": "Active", "progress": "stage_6_return_to_edrin" }, "next": "still_water_final_turn_in" },
        { "if": { "questId": "the_still_water", "state": "Active", "progress": "stage_3_return_to_edrin" }, "next": "still_water_stage_3_turn_in" },
        { "if": { "questId": "the_still_water", "state": "Ready To Turn In" }, "next": "still_water_active" },
        { "if": { "questId": "the_still_water", "state": "Active" }, "next": "still_water_active" },
        { "if": { "questId": "mirror_pond_listening", "state": "Completed" }, "next": "after_pond_rite" },
        { "if": { "questId": "mirror_pond_listening", "state": "Active", "progress": "heard_whispers" }, "next": "pond_whispers_heard" },
        { "if": { "objectiveId": "hunters_request:open_chest", "completed": true }, "next": "cave_relic_observed" },
        { "if": { "questId": "mirror_pond_listening", "state": "Active" }, "next": "pond_listening_active" }
      ],
      "nodes": {
        "greeting": {
          "lines": [
            "The pond has been still for years. Today, it moved."
          ],
          "choices": [
            { "text": "What do you mean?", "event": "quest:activate:the_still_water", "next": "still_water_begin" },
            { "text": "What is Mirror Pond?", "next": "mirror_pond_lore" },
            { "text": "What do you know about the cave?", "next": "mirror_cave_lore" },
            { "text": "Why do people call me Wayfarer?", "next": "wayfarer_title" },
            { "text": "Goodbye.", "next": "end" }
          ]
        },
        "still_water_begin": {
          "lines": [
            "Go to the water. Do not look only at the surface."
          ],
          "next": "end"
        },
        "still_water_active": {
          "lines": [
            "Go to the water. Do not look only at the surface."
          ],
          "choices": [
            { "text": "Goodbye.", "next": "end" }
          ]
        },
        "still_water_stage_3_turn_in": {
          "lines": [
            "Then the surface delayed itself for you.",
            "The pond is not just water. It remembers."
          ],
          "choices": [
            { "text": "I'll go into the cave.", "next": "still_water_stage_3_advance" },
            { "text": "Goodbye.", "next": "end" }
          ]
        },
        "still_water_stage_3_advance": {
          "lines": [
            "Enter Mirror Cave again. Bring back the fragment that answers to you."
          ],
          "onCompleteEvents": ["quest:still_water:report_pond"],
          "next": "end"
        },
        "still_water_final_turn_in": {
          "lines": [
            "You brought the Echo Fragment."
          ],
          "choices": [
            { "text": "Give Edrin the Echo Fragment", "next": "still_water_complete_turn_in" },
            { "text": "Goodbye.", "next": "end" }
          ]
        },
        "still_water_complete_turn_in": {
          "lines": [
            "Then it remembers you. That is not a gift given lightly."
          ],
          "onCompleteEvents": ["quest:still_water:final_turn_in"],
          "next": "still_water_complete"
        },
        "still_water_complete": {
          "lines": [
            "Then it remembers you. That is not a gift given lightly."
          ],
          "choices": [
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
        { "if": { "questId": "hunters_request", "progress": "stage_4_return_with_relic" }, "next": "hunters_request_final_turn_in_ready" },
        { "if": { "questId": "hunters_request", "progress": "stage_3_mirror_cave" }, "next": "hunters_request_stage_3_active" },
        { "if": { "questId": "hunters_request", "progress": "stage_2_return_to_hunter" }, "next": "hunters_request_stage_2_turn_in" },
        { "if": { "questId": "hunters_request", "progress": "stage_1_prove_yourself" }, "next": "hunters_request_stage_1_active" }
      ],
      "nodes": {
        "hunters_request_offer": {
          "lines": [
            "You want to survive out there? Then earn it.",
            "Wolves are ranging near the pond. Bring me proof you can hold your ground.",
            "Take Hunter's Request: defeat 3 wolves and collect 3 Wolf Pelts."
          ],
          "choices": [
            { "text": "Accept Hunter's Request", "event": "quest:activate:hunters_request", "next": "end" },
            { "text": "Not now.", "next": "end" }
          ]
        },
        "hunters_request_stage_1_active": {
          "lines": [
            "Prove yourself first. Defeat 3 wolves and bring me 3 Wolf Pelts."
          ],
          "choices": [
            { "text": "Goodbye.", "next": "end" }
          ]
        },
        "hunters_request_stage_2_turn_in": {
          "lines": [
            "You handled yourself. Good. Now there is something deeper I need you to see."
          ],
          "choices": [
            { "text": "Hand over 3 Wolf Pelts", "next": "hunters_request_pelt_turn_in" },
            { "text": "Goodbye.", "next": "end" }
          ]
        },
        "hunters_request_pelt_turn_in": {
          "lines": [
            "Enter Mirror Cave and recover what waits inside. Bring it back to me."
          ],
          "onCompleteEvents": ["quest:hunter:turn_in_pelts"],
          "next": "end"
        },
        "hunters_request_stage_3_active": {
          "lines": [
            "Mirror Cave is waiting. Recover what rests in the old chest and come back."
          ],
          "choices": [
            { "text": "Goodbye.", "next": "end" }
          ]
        },
        "hunters_request_final_turn_in_ready": {
          "lines": [
            "You came back with it. Then Hearthvale may remember your name yet."
          ],
          "choices": [
            { "text": "Give Hunter Garran the Mirror Relic", "next": "hunters_request_final_turn_in" },
            { "text": "Goodbye.", "next": "end" }
          ]
        },
        "hunters_request_final_turn_in": {
          "lines": [
            "Good. You did what I asked, in order, and you came back standing."
          ],
          "onCompleteEvents": ["quest:hunter:final_turn_in"],
          "next": "hunters_request_complete"
        },
        "hunters_request_complete": {
          "lines": [
            "You came back with it. Then Hearthvale may remember your name yet."
          ],
          "choices": [
            { "text": "Goodbye.", "next": "end" }
          ]
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
            "That Iron Sword suits you. Hunter Garran doesn't hand out steel lightly.",
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
            "Old tollhouse up north used to take coin from every wagon. Now it takes blood, from what I hear.",
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
      "rewards": { "xp": 15, "coins": 5 }
    },
    {
      "id": "the_still_water",
      "questId": "the_still_water",
      "title": "The Still Water",
      "name": "The Still Water",
      "description": "Follow Edrin Vale's guidance at Mirror Pond and recover the Echo Fragment from Mirror Cave.",
      "startEvents": ["quest:activate:the_still_water"],
      "initialProgress": "stage_1_speak_with_edrin",
      "status": "Not Started",
      "objectives": [
        { "id": "inspect_pond", "label": "Inspect Mirror Pond", "type": "interact", "targetId": "mirror_pond", "requiredAmount": 1, "currentAmount": 0, "completed": false },
        { "id": "enter_cave", "label": "Enter Mirror Cave", "type": "reach", "targetId": "mirror_cave", "requiredAmount": 1, "currentAmount": 0, "completed": false },
        { "id": "recover_echo_fragment", "label": "Recover the Echo Fragment from Mirror Cave", "type": "interact", "targetId": "echo_fragment", "requiredAmount": 1, "currentAmount": 0, "completed": false },
        { "id": "return_edrin", "label": "Return to Edrin Vale", "type": "interact", "targetId": "npc_edrin", "requiredAmount": 1, "currentAmount": 0, "completed": false }
      ],
      "rewards": { "xp": 45, "coins": 4, "items": [{ "itemId": "small_potion", "count": 1 }] }
    },
    {
      "id": "hunters_request",
      "questId": "hunters_request",
      "title": "Hunter's Request",
      "name": "Hunter's Request",
      "description": "Prove yourself to Hunter Garran, recover the Mirror Relic from Mirror Cave, then return for your reward.",
      "startEvents": ["quest:activate:hunters_request"],
      "initialProgress": "stage_1_prove_yourself",
      "status": "Not Started",
      "objectives": [
        { "id": "wolves", "label": "Defeat 3 wolves", "summaryLabel": "Wolves defeated", "type": "kill", "targetId": "wolf", "requiredAmount": 3, "currentAmount": 0, "completed": false },
        { "id": "pelts", "label": "Collect 3 Wolf Pelts", "summaryLabel": "Wolf Pelts", "type": "item", "targetId": "wolf_pelt", "requiredAmount": 3, "currentAmount": 0, "completed": false },
        { "id": "enter_cave", "label": "Enter Mirror Cave", "type": "reach", "targetId": "mirror_cave", "requiredAmount": 1, "currentAmount": 0, "completed": false },
        { "id": "open_chest", "label": "Open Mirror Cave chest", "type": "interact", "targetId": "mirror_cave_chest", "requiredAmount": 1, "currentAmount": 0, "completed": false },
        { "id": "return_hunter", "label": "Return to Hunter Garran", "type": "interact", "targetId": "npc_hunter_garran", "requiredAmount": 1, "currentAmount": 0, "completed": false }
      ],
      "rewards": { "xp": 35, "coins": 0, "items": [] }
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
const debugPanel = document.getElementById("debugPanel");
const chat = document.getElementById("chat");
const levelVal = document.getElementById("levelVal");
const hpVal = document.getElementById("hpVal");
const xpVal = document.getElementById("xpVal");
const coinsVal = document.getElementById("coinsVal");
const zoneVal = document.getElementById("zoneVal");
const questVal = document.getElementById("questVal");
const weaponVal = document.getElementById("weaponVal");
const armorVal = document.getElementById("armorVal");
const trinketVal = document.getElementById("trinketVal");
const objectiveText = document.getElementById("objectiveText");
const inventoryList = document.getElementById("inventoryList");
const equipmentList = document.getElementById("equipmentList");
const skillsList = document.getElementById("skillsList");
const dialogue = document.getElementById("dialogue");
const dialogueName = document.getElementById("dialogueName");
const dialogueText = document.getElementById("dialogueText");
const dialogueChoices = document.getElementById("dialogueChoices");
const dialogueHint = document.getElementById("dialogueHint");
const dialogueActions = document.getElementById("dialogueActions");
const vendorPanel = document.getElementById("vendorPanel");
const vendorList = document.getElementById("vendorList");
const vendorClose = document.getElementById("vendorClose");
const saveNotice = document.getElementById("saveNotice");
const rewardToast = document.getElementById("rewardToast");
const transitionFade = document.getElementById("transitionFade");
const sidebarTabs = Array.from(document.querySelectorAll(".sidebar-tab"));
const sidebarPanels = Array.from(document.querySelectorAll(".sidebar-tab-panel"));

function setActiveSidebarTab(tabId){
  sidebarTabs.forEach((tab)=>{
    const isActive=tab.dataset.sidebarTab===tabId;
    tab.classList.toggle("active", isActive);
    tab.setAttribute("aria-selected", isActive ? "true" : "false");
  });
  sidebarPanels.forEach((panel)=>{
    panel.classList.toggle("active", panel.dataset.sidebarPanel===tabId);
  });
}
if(sidebarTabs.length>0){
  const tabsHost=document.getElementById("sidebarTabs");
  tabsHost?.addEventListener("click", (event)=>{
    const tabButton=event.target.closest(".sidebar-tab");
    if(!tabButton) return;
    setActiveSidebarTab(tabButton.dataset.sidebarTab || "inventory");
  });
}

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
  north_road: {
    id: "north_road",
    name: "North Road",
    bounds: { x:10, y:0, w:14, h:7 }
  },
  hearthvale_square: {
    id: "hearthvale_square",
    name: "Hearthvale Square",
    bounds: { x:0, y:7, w:27, h:WORLD_H-7 }
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
  },
  abandoned_tollhouse: {
    id:"abandoned_tollhouse",
    name:"Abandoned Tollhouse"
  }
};
const BALANCE = Object.freeze({
  player: {
    startingMaxHp: 52,
    baseDamage: 6,
    levelProgression: Object.freeze([
      { level:1, xpRequired:0, maxHp:52, baseAttackBonus:0, baseDefenseBonus:0 },
      { level:2, xpRequired:90, maxHp:62, baseAttackBonus:1, baseDefenseBonus:0 },
      { level:3, xpRequired:210, maxHp:74, baseAttackBonus:2, baseDefenseBonus:1 },
      { level:4, xpRequired:420, maxHp:86, baseAttackBonus:3, baseDefenseBonus:1 },
      { level:5, xpRequired:720, maxHp:98, baseAttackBonus:3, baseDefenseBonus:2 }
    ])
  },
  items: {
    healingHerbHealAmount: 10,
    smallPotionHealAmount: 25,
    leatherArmorDefense: 2,
    rustySwordAttack: 2,
    ironSwordAttack: 5,
    travelersCharmDefense: 1
  },
  enemies: {
    wolf: {
      hp:24,
      damage:6,
      xp:9,
      coinReward:2,
      attackCooldownMs:2000,
      respawnMs:14000,
      lootTable: Object.freeze([
        { itemId:"wolf_pelt", chance:0.55, min:1, max:1 },
        { itemId:"small_fang", chance:0.4, min:1, max:1 }
      ])
    },
    bandit: {
      hp:34,
      damage:8,
      xp:18,
      coinReward:7,
      attackCooldownMs:2600,
      respawnMs:18000,
      lootTable: Object.freeze([
        { itemId:"old_coin", chance:0.85, min:1, max:2 },
        { itemId:"cloth_scrap", chance:0.55, min:1, max:1 }
      ])
    },
    rook_tollkeeper: {
      hp:72,
      damage:11,
      xp:62,
      coinReward:22,
      attackCooldownMs:3000,
      respawnMs:0,
      lootTable: Object.freeze([])
    },
    cave_wolf: {
      hp:28,
      damage:7,
      xp:13,
      coinReward:3,
      attackCooldownMs:2200,
      respawnMs:16000,
      lootTable: Object.freeze([
        { itemId:"wolf_pelt", chance:0.75, min:1, max:1 },
        { itemId:"small_fang", chance:0.65, min:1, max:2 }
      ])
    }
  },
  combatLog: {
    repeatWindowMs:1200
  },
  death: {
    respawnSafetyMs:2600
  }
});
const SKILL_LEVEL_THRESHOLDS = Object.freeze([0,50,125,250,450]);
const SKILL_MAX_LEVEL = SKILL_LEVEL_THRESHOLDS.length;
const SKILL_DISPLAY_NAMES = Object.freeze({
  swordsmanship:"Swordsmanship",
  defense:"Defense",
  survival:"Survival"
});
const HARD_ZONE_TRANSITIONS = Object.freeze([]);
let currentZoneId = "hearthvale_square";
let zoneTransitionLockedUntil = 0;
const DIRECTION_KEYS = Object.freeze(["w","a","s","d","arrowup","arrowdown","arrowleft","arrowright"]);
let blockedDirectionalKeysUntilRelease = new Set();
let lastLoggedZoneEntryId = currentZoneId;
const VIEW_TILES_X = 22;
const VIEW_TILES_Y = 14;
const ITEM_REGISTRY = Object.freeze({
  rusty_sword: { id:"rusty_sword", name:"Rusty Sword", type:"weapon", attackBonus:BALANCE.items.rustySwordAttack, description:"A worn but dependable blade.", stackable:false, value:8 },
  iron_sword: { id:"iron_sword", name:"Iron Sword", type:"weapon", attackBonus:BALANCE.items.ironSwordAttack, description:"A sharpened iron blade forged for close cave fights.", stackable:false, value:24 },
  leather_armor: { id:"leather_armor", name:"Leather Armor", type:"armor", defenseBonus:BALANCE.items.leatherArmorDefense, description:"Sturdy leather armor that softens incoming blows.", stackable:false, value:28 },
  wolf_pelt: { id:"wolf_pelt", name:"Wolf Pelt", type:"material", description:"A coarse pelt taken from a wild wolf.", stackable:true, value:3 },
  small_fang: { id:"small_fang", name:"Small Fang", type:"material", description:"A sharp fang useful for craftwork.", stackable:true, value:2 },
  old_coin: { id:"old_coin", name:"Old Coin", type:"material", description:"A worn coin from a forgotten mint.", stackable:true, value:2 },
  old_toll_key: { id:"old_toll_key", name:"Old Toll Key", type:"quest", description:"A heavy iron key stamped with the old tollhouse seal.", stackable:false, value:0 },
  travelers_charm: { id:"travelers_charm", name:"Traveler's Charm", type:"trinket", defenseBonus:BALANCE.items.travelersCharmDefense, description:"A weathered charm favored by caravan guards. Grants +1 DEF.", stackable:false, value:32 },
  mirror_relic: { id:"mirror_relic", name:"Mirror Relic", type:"quest", description:"An old relic recovered from the Mirror Cave chest.", stackable:false, value:0 },
  echo_fragment: { id:"echo_fragment", name:"Echo Fragment", type:"quest", description:"A dim fragment that seems to hold a delayed reflection.", stackable:false, value:0 },
  cloth_scrap: { id:"cloth_scrap", name:"Cloth Scrap", type:"material", description:"Rough cloth torn from worn travel gear.", stackable:true, value:2 },
  healing_herb: { id:"healing_herb", name:"Healing Herb", type:"consumable", description:"A medicinal herb with a clean scent.", stackable:true, healAmount:BALANCE.items.healingHerbHealAmount, value:4 },
  small_potion: { id:"small_potion", name:"Small Potion", type:"consumable", description:"A compact tonic that restores vitality.", stackable:true, healAmount:BALANCE.items.smallPotionHealAmount, value:10 }
});
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
  grass: ["#4e7045", "#4a6b42", "#55784d", "#43633d"],
  forestGrass: ["#39583a", "#324f35", "#416444", "#2a452d"],
  road: ["#8b724d", "#755f40", "#9f8560", "#594733"],
  water: ["#2a4b73", "#1d3554", "#35628f", "#4d84b6", "#9bc8e6"],
  shore: ["#75835a", "#5c6c49", "#ccb78a"],
  wood: ["#7b5a3f", "#5a412c", "#9e7754", "#ccac7f"],
  roof: ["#875048", "#6c3d36", "#aa6f64", "#4b2c27"],
  wall: ["#9b907c", "#746a58", "#b5ab97"],
  cave: ["#404753", "#313742", "#596474", "#222833"],
  tollhouse: ["#73573d", "#5d462f", "#8f6d4c", "#453222"],
  fence: ["#7b5d40", "#5d442d", "#b08c62"],
  uiInk: "#0d141f",
};

let lastCombatLog={ message:"", at:0 };
let lastLogMessage="";
let lastLogRepeatCount=1;
let lastLogRepeatElement=null;
let rewardToastTimeout=0;
const floatingTexts=[];
let cameraShakeUntil=0;
let cameraShakeStrength=0;
function log(message){
  if(!message) return;
  if(message===lastLogMessage && lastLogRepeatElement){
    lastLogRepeatCount+=1;
    lastLogRepeatElement.textContent=message + " (x" + lastLogRepeatCount + ")";
    chat.scrollTop=chat.scrollHeight;
    return;
  }
  lastLogMessage=message;
  lastLogRepeatCount=1;
  const line=document.createElement("div");
  line.textContent=message;
  chat.appendChild(line);
  lastLogRepeatElement=line;
  while(chat.childElementCount>220){
    chat.removeChild(chat.firstElementChild);
  }
  chat.scrollTop=chat.scrollHeight;
}
function showRewardToast(message, durationMs=1400){
  if(!rewardToast || !message) return;
  rewardToast.textContent=message;
  rewardToast.classList.add("visible");
  if(rewardToastTimeout) clearTimeout(rewardToastTimeout);
  rewardToastTimeout=setTimeout(()=>{
    rewardToast.classList.remove("visible");
  }, Math.max(800, durationMs));
}
function showRewardToasts(messages){
  if(!Array.isArray(messages) || !messages.length) return;
  let delay=0;
  messages.forEach((message)=>{
    if(typeof message!=="string" || !message) return;
    setTimeout(()=>showRewardToast(message), delay);
    delay+=750;
  });
}
function spawnFloatingText(tx,ty,text,{color="#f4f8ff",durationMs=850,rise=14,size=12}={}){
  if(!text && text!==0) return;
  floatingTexts.push({ tx, ty, text:String(text), color, size, durationMs, rise, startedAt:performance.now() });
}
function triggerCameraShake(durationMs=120,strength=2){
  cameraShakeUntil=Math.max(cameraShakeUntil, performance.now()+Math.max(60,durationMs));
  cameraShakeStrength=Math.max(cameraShakeStrength, Math.max(0.5,strength));
}
function drawFloatingTexts(now){
  for(let i=floatingTexts.length-1;i>=0;i--){
    const entry=floatingTexts[i];
    const age=now-entry.startedAt;
    if(age>=entry.durationMs){
      floatingTexts.splice(i,1);
      continue;
    }
    const progress=Math.max(0, Math.min(1, age/entry.durationMs));
    const alpha=(1-progress);
    const p=tileToScreen(entry.tx, entry.ty);
    const yOffset=Math.round(progress*entry.rise);
    ctx.save();
    ctx.globalAlpha=alpha;
    ctx.fillStyle="rgba(10,12,18,.85)";
    const textW=Math.max(24, entry.text.length*7+8);
    ctx.fillRect(p.x+16-Math.floor(textW/2), p.y-20-yOffset, textW, 13);
    ctx.fillStyle=entry.color;
    ctx.font="bold " + entry.size + "px monospace";
    ctx.textAlign="center";
    ctx.fillText(entry.text, p.x+16, p.y-10-yOffset);
    ctx.restore();
  }
}
function logCombat(message){
  const now=performance.now();
  if(lastCombatLog.message===message && now-lastCombatLog.at<BALANCE.combatLog.repeatWindowMs) return;
  lastCombatLog={ message, at:now };
  log(message);
}
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
function layeredNoise(x,y){
  const broad = rng(Math.floor(x*0.34), Math.floor(y*0.34), 401);
  const medium = rng(Math.floor(x*0.72), Math.floor(y*0.72), 487);
  const fine = rng(x,y,509);
  const micro = rng(Math.floor((x+13)*1.35), Math.floor((y+9)*1.35), 521);
  return broad*0.36 + medium*0.31 + fine*0.18 + micro*0.15;
}

function makeTile(drawFn){
  const c = document.createElement("canvas"); c.width = TILE; c.height = TILE;
  const p = c.getContext("2d"); p.imageSmoothingEnabled = false; drawFn(p);
  const img = new Image(); img.src = c.toDataURL("image/png"); return img;
}

const assets = {
  grass: [], forestGrass: [], road: [], roadEdge: [], water: {}, shore: [], detail: [],
  tree: {}, propWell: null, fence: [],
  shadow: {},
  props: { sheet:null, sprites:{}, meta:{} },
  building: {}, sprites: { player:null, npc:null, edrin:null, hunter:null, merchant:null, wolf:null, bandit:null, rook:null }
};

function buildTerrainTiles() {
  const grassBases = ["#4f7347", "#527849", "#4c7044", "#557a4d", "#486c41", "#507448"];
  const forestBases = [palette.forestGrass[0], "#3f6540", palette.forestGrass[1], "#314f34"];
  for (let i=0;i<6;i++) {
    assets.grass.push(makeTile((p)=>{
      p.fillStyle = grassBases[i]; p.fillRect(0,0,32,32);
      for (let y=0;y<32;y+=2){
        for (let x=0;x<32;x+=2){
          const n=rng(x+i*7,y+i*5,31+i);
          if(n>0.9){ p.fillStyle = "rgba(198,226,162,.055)"; p.fillRect(x,y,2,1); }
          else if(n<0.07){ p.fillStyle = "rgba(29,47,28,.085)"; p.fillRect(x,y+1,2,1); }
        }
      }
      p.fillStyle = "rgba(220,239,180,.045)";
      for (let k=0;k<16;k++) {
        const gx = ((k*5+i*6)%30)+1;
        const gy = ((k*7+i*3)%25)+3;
        const dotW = rng(k+i,gy,145)>0.72 ? 2 : 1;
        p.fillRect(gx,gy,dotW,1);
      }
      p.fillStyle="rgba(255,255,255,.018)"; p.fillRect(0,0,32,1);
      p.fillStyle="rgba(0,0,0,.065)"; p.fillRect(0,30,32,2);
    }));
    if(i<4){
      assets.forestGrass.push(makeTile((p)=>{
        p.fillStyle=forestBases[i]; p.fillRect(0,0,32,32);
        for(let y=0;y<32;y+=2){
          for(let x=0;x<32;x+=2){
            const n=rng(x+i*8,y+i*6,53+i);
            if(n>0.83){ p.fillStyle="rgba(112,152,96,.1)"; p.fillRect(x,y,2,1); }
            else if(n<0.14){ p.fillStyle="rgba(18,31,20,.2)"; p.fillRect(x,y,2,1); }
          }
        }
        p.fillStyle="rgba(0,0,0,.15)"; p.fillRect(0,29,32,3);
      }));
    }

    if(i<5) {
      assets.road.push(makeTile((p)=>{
        const base = i%2? "#836a48" : "#7b6343";
        p.fillStyle = base; p.fillRect(0,0,32,32);
        p.fillStyle = "rgba(98,78,53,.22)";
        for(let y=0;y<32;y+=3){
          const wob=Math.floor((Math.sin((y+i)*0.45)+1.3)*1.5);
          p.fillRect((y+i*3)%10, y, 9+wob, 1);
        }
        p.fillStyle = "rgba(196,166,128,.16)";
        for(let k=0;k<10;k++){
          const x=((k*7+i*5)%26)+2;
          const y=((k*6+i*8)%24)+4;
          p.fillRect(x,y,2+(k%2),1);
        }
        p.fillStyle="rgba(0,0,0,.1)";
        p.fillRect(0,0,32,2);
        p.fillStyle = "rgba(0,0,0,.16)"; p.fillRect(0,29,32,3);
      }));
    }

    assets.shore.push(makeTile((p)=>{
      p.fillStyle = i%2?palette.shore[0]:palette.shore[1]; p.fillRect(0,0,32,32);
      p.fillStyle = "rgba(132,111,79,.46)"; p.fillRect(0,22,32,10);
      p.fillStyle = "rgba(194,178,132,.22)"; p.fillRect(0,20,32,2);
      for(let x=3;x<30;x+=6){ p.fillStyle="rgba(90,116,72,.45)"; p.fillRect(x,14+(x%5),2,8); }
    }));
  }

  for(let i=0;i<4;i++) {
    assets.roadEdge.push(makeTile((p)=>{
      p.fillStyle="rgba(0,0,0,0)"; p.fillRect(0,0,32,32);
      p.fillStyle=i%2? "rgba(123,102,74,.72)" : "rgba(138,114,84,.68)";
      for(let x=0;x<32;x+=2){
        const h = 2 + Math.floor(rng(x,i,77) * 4);
        p.fillRect(x,32-h,2,h);
      }
      p.fillStyle="rgba(78,104,57,.36)"; p.fillRect(0,0,32,2);
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
    g.addColorStop(0,"#3a6b99"); g.addColorStop(.55,palette.water[1]); g.addColorStop(1,palette.water[0]);
    p.fillStyle = g; p.fillRect(0,0,32,32);
    p.fillStyle = "rgba(126,187,226,.17)";
    for(let y=3;y<28;y+=5) p.fillRect(3+(y%4),y,24,1);
    p.fillStyle = "rgba(201,235,255,.12)"; p.fillRect(2,4,19,2);
  });
  assets.water.shallow = makeTile((p)=>{
    const g = p.createLinearGradient(0,0,0,32);
    g.addColorStop(0,"#79acd2"); g.addColorStop(.35,palette.water[2]); g.addColorStop(1,"#356996");
    p.fillStyle = g; p.fillRect(0,0,32,32);
    p.fillStyle = "rgba(195,230,248,.24)"; p.fillRect(1,1,30,5);
    p.fillStyle = "rgba(63,115,165,.28)"; p.fillRect(0,24,32,8);
    p.fillStyle = "rgba(225,246,255,.24)"; p.fillRect(3,12,24,2);
  });
  assets.water.edge = makeTile((p)=>{
    p.fillStyle="rgba(0,0,0,0)"; p.fillRect(0,0,32,32);
    const g = p.createLinearGradient(0,0,0,32);
    g.addColorStop(0,"rgba(235,222,176,.32)");
    g.addColorStop(.4,"rgba(185,198,149,.2)");
    g.addColorStop(1,"rgba(84,124,155,0)");
    p.fillStyle=g; p.fillRect(0,0,32,32);
    p.fillStyle="rgba(245,245,220,.22)"; p.fillRect(1,1,30,1);
  });
}

function makeBuildingTiles(){
  assets.building.roofL = makeTile((p)=>{
    p.fillStyle=palette.roof[0]; p.fillRect(0,0,32,32);
    p.fillStyle=palette.roof[1]; for(let y=0;y<30;y++) p.fillRect(0,y,Math.max(0,11-Math.floor(y/3)),1);
    p.fillStyle=palette.roof[2]; for(let y=3;y<28;y+=4) p.fillRect(3,y,26,1);
    p.fillStyle="rgba(255,226,199,.12)"; p.fillRect(2,3,20,2);
    p.fillStyle=palette.roof[3]; p.fillRect(0,24,32,8);
  });
  assets.building.roofC = makeTile((p)=>{
    p.fillStyle=palette.roof[0]; p.fillRect(0,0,32,32);
    p.fillStyle=palette.roof[2]; for(let y=2;y<28;y+=4) p.fillRect(2,y,28,1);
    p.fillStyle="rgba(255,226,199,.1)"; p.fillRect(5,3,22,2);
    p.fillStyle="rgba(64,37,26,.28)"; for(let x=3;x<30;x+=6) p.fillRect(x,6,2,16);
    p.fillStyle="rgba(89,48,32,.2)"; for(let x=2;x<30;x+=4) p.fillRect(x,11,1,10);
    p.fillStyle=palette.roof[3]; p.fillRect(0,24,32,8);
    p.fillStyle="rgba(231,196,152,.2)"; p.fillRect(2,24,28,1);
    p.fillStyle="rgba(0,0,0,.19)"; p.fillRect(0,25,32,2);
  });
  assets.building.roofR = makeTile((p)=>{
    p.fillStyle=palette.roof[0]; p.fillRect(0,0,32,32);
    p.fillStyle=palette.roof[1]; for(let y=0;y<30;y++){const w=Math.max(0,11-Math.floor(y/3)); p.fillRect(32-w,y,w,1);}
    p.fillStyle=palette.roof[2]; for(let y=2;y<28;y+=4) p.fillRect(2,y,28,1);
    p.fillStyle="rgba(255,226,199,.12)"; p.fillRect(10,3,20,2);
    p.fillStyle=palette.roof[3]; p.fillRect(0,24,32,8);
  });
  assets.building.wall = makeTile((p)=>{
    p.fillStyle=palette.wall[0]; p.fillRect(0,0,32,32);
    p.fillStyle=palette.wall[2]; p.fillRect(0,0,32,4);
    p.fillStyle=palette.wall[1]; p.fillRect(0,28,32,4);
    p.fillStyle="rgba(97,74,48,.16)"; for(let x=0;x<32;x+=8) p.fillRect(x,4,1,24);
    p.fillStyle="rgba(255,255,255,.05)";
    for(let y=5;y<29;y+=5) for(let x=(y%5)+2;x<30;x+=7){ p.fillRect(x,y,1,1); }
    p.fillStyle="rgba(35,28,20,.14)"; p.fillRect(29,0,3,32);
    p.fillStyle="rgba(255,232,189,.06)"; p.fillRect(2,5,2,20);
    p.fillStyle="rgba(0,0,0,.08)"; p.fillRect(0,27,32,1);
  });
  assets.building.window = makeTile((p)=>{
    p.drawImage(assets.building.wall,0,0);
    p.fillStyle="#5a3f28"; p.fillRect(6,6,20,17);
    p.fillStyle="#37291d"; p.fillRect(7,7,18,15);
    p.fillStyle="#98b7ca"; p.fillRect(9,9,14,11);
    p.fillStyle="rgba(231,248,255,.42)"; p.fillRect(10,10,12,2);
    p.fillStyle="rgba(66,97,122,.4)"; p.fillRect(9,16,14,4);
    p.fillStyle="#503822"; p.fillRect(15,9,2,11); p.fillRect(9,14,14,2);
    p.fillStyle="rgba(247,214,153,.32)"; p.fillRect(8,22,16,1);
    p.fillStyle="rgba(255,243,203,.24)"; p.fillRect(9,8,14,1);
  });
  assets.building.door = makeTile((p)=>{
    p.drawImage(assets.building.wall,0,0);
    p.fillStyle="#664531"; p.fillRect(8,7,16,24);
    p.fillStyle="#3c291b"; p.fillRect(9,8,14,22);
    p.fillStyle="#916746"; p.fillRect(8,7,16,2);
    p.fillStyle="#b98856"; p.fillRect(15,10,2,20);
    p.fillStyle="#e3ba86"; p.fillRect(20,21,2,2);
    p.fillStyle="rgba(246,222,171,.2)"; p.fillRect(10,10,4,18);
    p.fillStyle="rgba(0,0,0,.25)"; p.fillRect(8,30,16,1);
    p.fillStyle="rgba(246,211,162,.18)"; p.fillRect(9,9,3,20);
    p.fillStyle="rgba(15,10,7,.18)"; p.fillRect(21,8,1,22);
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
  sheet.width = 416;
  sheet.height = 32;
  const p = sheet.getContext("2d");
  p.imageSmoothingEnabled = false;
  p.clearRect(0,0,416,32);

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
  cell(10,(q)=>{ // bench
    q.fillStyle="#6f5035"; q.fillRect(6,17,20,3); q.fillRect(8,12,16,2);
    q.fillStyle="#9c734d"; q.fillRect(7,16,18,1); q.fillRect(9,11,14,1);
    q.fillStyle="#4e3827"; q.fillRect(8,20,2,6); q.fillRect(22,20,2,6);
  });
  cell(11,(q)=>{ // notice board
    q.fillStyle="#5f432d"; q.fillRect(8,8,2,19); q.fillRect(22,8,2,19);
    q.fillStyle="#8f6948"; q.fillRect(9,8,14,12);
    q.fillStyle="#d3be96"; q.fillRect(10,9,12,10);
    q.fillStyle="#826247"; q.fillRect(12,11,7,1); q.fillRect(11,14,8,1); q.fillRect(13,16,6,1);
  });
  cell(12,(q)=>{ // handcart
    q.fillStyle="#6f4e35"; q.fillRect(7,14,18,9);
    q.fillStyle="#8f6847"; q.fillRect(8,15,16,7);
    q.fillStyle="#523927"; q.fillRect(9,13,14,1); q.fillRect(9,23,14,1);
    q.fillStyle="#503626"; q.fillRect(3,16,4,2); q.fillRect(25,16,4,2);
    q.fillStyle="#3b2a1f"; q.fillRect(5,22,3,3); q.fillRect(24,22,3,3);
    q.fillStyle="#9f9a8f"; q.fillRect(5,23,3,1); q.fillRect(24,23,3,1);
  });

  const sheetImg = new Image();
  sheetImg.src = sheet.toDataURL("image/png");
  assets.props.sheet = sheetImg;

  const names = ["barrel","crate","sack","lanternPost","signPost","fenceSeg","bush","grassTuft","well","stonePile","bench","noticeBoard","handcart"];
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
assets.sprites.player = paintHumanoidSheet({ skin:"#e4c8a2", hair:"#4f3a2c", tunic:"#5c80a2", tunicShade:"#3d5978", cloak:"#d2d8e2", boots:"#4f3826" }, "adventurer");
assets.sprites.npc = paintHumanoidSheet({ skin:"#ccb79b", hair:"#e3e8f4", tunic:"#64617a", tunicShade:"#49465d", cloak:"#313547", boots:"#2f2418" }, "elder");
assets.sprites.edrin = paintHumanoidSheet({ skin:"#c8ae8d", hair:"#f0f4fc", tunic:"#70708a", tunicShade:"#55556c", cloak:"#34384b", boots:"#2f2418" }, "elder");
assets.sprites.hunter = paintHumanoidSheet({ skin:"#d3b999", hair:"#4d3a2b", tunic:"#5c744c", tunicShade:"#45573b", cloak:"#3f3225", boots:"#312519" }, "adventurer");
assets.sprites.merchant = paintHumanoidSheet({ skin:"#dabf9e", hair:"#61452f", tunic:"#7a4f38", tunicShade:"#5b3b2a", cloak:"#a4824f", boots:"#3b2a1d" }, "adventurer");
assets.sprites.bandit = paintHumanoidSheet({ skin:"#b99b7b", hair:"#2a2320", tunic:"#5b3d3f", tunicShade:"#412b2d", cloak:"#1f1c24", boots:"#241a13" }, "adventurer");
assets.sprites.rook = paintHumanoidSheet({ skin:"#b4916c", hair:"#131116", tunic:"#6f2f36", tunicShade:"#4f2127", cloak:"#2e1116", boots:"#1f1310" }, "adventurer");
assets.sprites.wolf = paintWolfSheet();

const world = { blocked:new Set(), trees:[], fences:[], buildings:[], roads:[], roadTiles:new Set(), props:[], zones:[], pondBlocked:new Set(), pondWater:new Set(), pondShore:new Set(), pondNearEdge:new Set() };
function blockRect(x,y,w,h){ for(let ix=x;ix<x+w;ix++)for(let iy=y;iy<y+h;iy++) world.blocked.add(keyOf(ix,iy)); }
const OVERWORLD_CAVE_ENTRY = Object.freeze({ x:30, y:13 });
const MIRROR_CAVE_EXIT = Object.freeze({ x:13, y:16 });
const MIRROR_CAVE_CHEST_TILE = Object.freeze({ x:13, y:2 });
const NORTH_ROAD_TOLLHOUSE_ENTRY = Object.freeze({ x:22, y:2 });
const TOLLHOUSE_EXIT = Object.freeze({ x:13, y:18 });
const TOLLHOUSE_CHEST_TILE = Object.freeze({ x:22, y:4 });
const WORLD_OBJECT_TYPE = Object.freeze({
  CAVE_ENTRANCE:"caveEntrance",
  DUNGEON_EXIT:"dungeonExit",
  CHEST:"chest",
  SIGN:"sign",
  DOOR:"door",
  DECORATION:"decoration"
});
const mirrorCave = {
  width:26,
  height:18,
  floor:new Set(),
  blocked:new Set(),
  walls:new Set(),
  spawn:{ x:13, y:15 },
  exit:{ ...MIRROR_CAVE_EXIT },
  chest:{ ...MIRROR_CAVE_CHEST_TILE, opened:false },
  cleared:false,
  returnTile:{ x:OVERWORLD_CAVE_ENTRY.x, y:OVERWORLD_CAVE_ENTRY.y+1 }
};
const abandonedTollhouse = {
  width:24,
  height:20,
  floor:new Set(),
  blocked:new Set(),
  walls:new Set(),
  spawn:{ x:13, y:17 },
  exit:{ ...TOLLHOUSE_EXIT },
  chest:{ ...TOLLHOUSE_CHEST_TILE },
  returnTile:{ x:NORTH_ROAD_TOLLHOUSE_ENTRY.x, y:NORTH_ROAD_TOLLHOUSE_ENTRY.y+1 }
};
function carveMirrorCaveRoom(x,y,w,h){
  for(let tx=x;tx<x+w;tx++){
    for(let ty=y;ty<y+h;ty++){
      mirrorCave.floor.add(keyOf(tx,ty));
      mirrorCave.blocked.delete(keyOf(tx,ty));
    }
  }
}
function carveTollhouseRoom(x,y,w,h){
  for(let tx=x;tx<x+w;tx++){
    for(let ty=y;ty<y+h;ty++){
      abandonedTollhouse.floor.add(keyOf(tx,ty));
      abandonedTollhouse.blocked.delete(keyOf(tx,ty));
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
for(let x=0;x<abandonedTollhouse.width;x++) for(let y=0;y<abandonedTollhouse.height;y++) abandonedTollhouse.blocked.add(keyOf(x,y));
carveTollhouseRoom(12,17,3,2);
carveTollhouseRoom(12,14,3,3);
carveTollhouseRoom(11,10,5,4);
carveTollhouseRoom(7,8,4,4);
carveTollhouseRoom(11,6,10,4);
carveTollhouseRoom(20,4,3,2);
carveTollhouseRoom(17,8,4,2);
for(let x=0;x<abandonedTollhouse.width;x++){
  for(let y=0;y<abandonedTollhouse.height;y++){
    if(!abandonedTollhouse.blocked.has(keyOf(x,y))) continue;
    const neighbors=[[1,0],[-1,0],[0,1],[0,-1]];
    if(neighbors.some(([dx,dy])=>!abandonedTollhouse.blocked.has(keyOf(x+dx,y+dy)))) abandonedTollhouse.walls.add(keyOf(x,y));
  }
}

world.roads.push(
  { x:6,y:11,w:25,h:2 },
  { x:17,y:0,w:3,h:21 },
  { x:13,y:9,w:11,h:5 },
  { x:15,y:14,w:8,h:3 },
  { x:9,y:12,w:3,h:7 },
  { x:23,y:10,w:3,h:4 },
  { x:25,y:11,w:6,h:2 },
  { x:20,y:3,w:3,h:6 },
  { x:28,y:13,w:3,h:2 }
);
world.roads.forEach(r=>{ for(let x=r.x;x<r.x+r.w;x++) for(let y=r.y;y<r.y+r.h;y++) world.roadTiles.add(keyOf(x,y)); });

world.buildings.push(
  { x:9,y:6,w:7,h:4,tileRows:[["roofL","roofC","roofC","roofC","roofC","roofC","roofR"],["window","wall","window","wall","window","wall","window"],["wall","wall","wall","door","wall","wall","wall"],["wall","window","wall","wall","wall","window","wall"]] },
  { x:20,y:6,w:5,h:4,tileRows:[["roofL","roofC","roofC","roofC","roofR"],["window","wall","window","wall","window"],["wall","door","wall","wall","wall"],["wall","window","wall","window","wall"]] },
  { x:12,y:15,w:4,h:3,tileRows:[["roofL","roofC","roofC","roofR"],["window","wall","window","wall"],["wall","door","wall","wall"]] },
  { x:17,y:16,w:6,h:3,tileRows:[["roofL","roofC","roofC","roofC","roofC","roofR"],["window","wall","window","window","wall","window"],["wall","wall","door","wall","wall","wall"]] },
  { x:25,y:7,w:4,h:3,tileRows:[["roofL","roofC","roofC","roofR"],["window","wall","window","wall"],["wall","door","wall","wall"]] },
  { x:6,y:15,w:4,h:3,tileRows:[["roofL","roofC","roofC","roofR"],["window","wall","window","wall"],["wall","door","wall","wall"]] }
);
world.buildings.forEach(b=>blockRect(b.x,b.y,b.w,b.h));

const pond={x:23,y:11,w:10,h:8,cx:28,cy:15};
for(let x=pond.x;x<pond.x+pond.w;x++){
  for(let y=pond.y;y<pond.y+pond.h;y++){
    const dx=(x+.5-pond.cx)/(pond.w/2), dy=(y+.5-pond.cy)/(pond.h/2);
    const d=dx*dx+dy*dy;
    const wob=(rng(x,y,17)-.5)*.2 + (rng(x,y,19)-.5)*.08;
    const lim=.84+wob;
    if(d<=lim){ world.pondWater.add(keyOf(x,y)); world.pondBlocked.add(keyOf(x,y)); }
    if(d>=lim-.18&&d<=lim+.2) world.pondShore.add(keyOf(x,y));
    if(d>=lim-.25&&d<=lim+.1) world.pondNearEdge.add(keyOf(x,y));
  }
}

for(let x=5;x<=11;x++){ world.fences.push({x,y:19}); }
for(let y=16;y<=19;y++){ world.fences.push({x:5,y}); }
for(let x=24;x<=34;x++){ world.fences.push({x,y:6}); }
for(let y=7;y<=11;y++){ world.fences.push({x:34,y}); }
for(let x=23;x<=31;x++){ world.fences.push({x,y:19}); }
for(let y=16;y<=19;y++){ world.fences.push({x:31,y}); }
for(let x=13;x<=17;x++){ world.fences.push({x,y:3}); }
for(let x=20;x<=24;x++){ world.fences.push({x,y:3}); }
for(let x=14;x<=22;x++){ if(x!==18 && x!==19) world.fences.push({x,y:14}); }
world.fences.forEach(f=>world.blocked.add(keyOf(f.x,f.y)));

world.props.push(
  {x:10,y:10,type:"lanternPost"},{x:14,y:10,type:"lanternPost"},{x:9,y:10,type:"signPost"},
  {x:20,y:10,type:"crate"},{x:21,y:10,type:"crate"},{x:22,y:10,type:"sack"},{x:23,y:10,type:"barrel"},
  {x:24,y:10,type:"handcart"},{x:24,y:9,type:"signPost"},
  {x:16,y:11,type:"bench"},{x:21,y:11,type:"bench"},
  {x:18,y:12,type:"well"},{x:17,y:11,type:"noticeBoard"},{x:19,y:11,type:"lanternPost"},
  {x:15,y:13,type:"crate"},{x:20,y:13,type:"barrel"},
  {x:7,y:18,type:"barrel"},{x:8,y:18,type:"crate"},{x:9,y:18,type:"sack"},{x:6,y:18,type:"bush"},
  {x:12,y:18,type:"crate"},{x:13,y:18,type:"sack"},{x:14,y:18,type:"barrel"},{x:11,y:18,type:"bush"},
  {x:18,y:19,type:"crate"},{x:19,y:19,type:"sack"},{x:20,y:19,type:"barrel"},
  {x:25,y:10,type:"barrel"},{x:26,y:10,type:"crate"},{x:27,y:10,type:"sack"},{x:28,y:10,type:"stonePile"},
  {x:26,y:12,type:"signPost"},{x:27,y:12,type:"fenceSeg"},
  {x:25,y:13,type:"stonePile"},{x:24,y:16,type:"stonePile"},{x:31,y:17,type:"stonePile"},
  {x:26,y:18,type:"grassTuft"},{x:29,y:17,type:"grassTuft"},{x:30,y:14,type:"grassTuft"},
  {x:8,y:12,type:"bush"},{x:30,y:12,type:"bush"},{x:6,y:11,type:"fenceSeg"},{x:31,y:11,type:"fenceSeg"},
  {x:16,y:14,type:"fenceSeg"},{x:17,y:14,type:"fenceSeg"},{x:20,y:14,type:"fenceSeg"},{x:21,y:14,type:"fenceSeg"},
  {x:18,y:4,type:"signPost"},{x:21,y:4,type:"signPost"},{x:22,y:2,type:"fenceSeg"},
  {x:14,y:4,type:"fenceSeg"},{x:24,y:4,type:"fenceSeg"},
  {x:14,y:2,type:"bush"},{x:23,y:2,type:"bush"},
  {x:12,y:1,type:"stonePile"},{x:24,y:1,type:"stonePile"}
);
world.props.push({x:OVERWORLD_CAVE_ENTRY.x,y:OVERWORLD_CAVE_ENTRY.y,type:"stonePile"});

const treeData = [
  [1,1,"a"],[2,2,"b"],[3,3,"a"],[1,5,"c"],[2,7,"a"],[3,9,"b"],[1,11,"a"],[2,14,"c"],[1,17,"a"],[2,20,"b"],[3,22,"a"],
  [5,2,"a"],[7,2,"c"],[9,1,"b"],[11,2,"a"],[26,1,"c"],[28,2,"a"],[31,1,"b"],[34,2,"a"],[36,3,"c"],[37,6,"a"],[36,9,"b"],
  [37,12,"a"],[35,14,"c"],[36,17,"a"],[37,20,"b"],[35,22,"a"],[32,22,"c"],[29,23,"a"],[26,22,"b"],[22,23,"a"],[17,23,"c"],
  [13,23,"a"],[10,22,"b"],[7,23,"a"],[5,22,"c"],
  [30,5,"a"],[31,7,"b"],[30,9,"a"],[32,10,"c"],[31,16,"a"],[29,20,"c"],
  [6,6,"a"],[7,8,"b"],[6,18,"a"],[8,20,"c"],[9,5,"c"],[27,19,"b"],[24,20,"c"],[22,19,"a"],[19,21,"b"]
];
treeData.forEach(([x,y,type])=>{ world.trees.push({x,y,type,seed:rng(x,y,91)}); world.blocked.add(keyOf(x,y)); });

world.zones.push(
  {name:"North Road",x:10,y:0,w:14,h:7},
  {name:"Hearthvale Square",x:9,y:6,w:18,h:13},
  {name:"Mirror Pond",x:23,y:11,w:10,h:9},
  {name:"Eastern Woods",x:27,y:3,w:11,h:19},
  {name:"West Lane",x:0,y:7,w:10,h:12}
);

const LEVEL_PROGRESSION=BALANCE.player.levelProgression;
const MAX_DEFINED_LEVEL=LEVEL_PROGRESSION[LEVEL_PROGRESSION.length-1].level;
const player={x:18,y:11,px:18*TILE,py:11*TILE,targetX:18,targetY:11,hp:BALANCE.player.startingMaxHp,maxHp:BALANCE.player.startingMaxHp,level:1,xp:0,baseAttackBonus:0,baseDefenseBonus:0,coins:0,inventory:[],equipment:{weapon:"rusty_sword",armor:null,trinket:null},skills:createDefaultSkills(),moving:false,facing:"down",speed:180,attackUntil:0,hitUntil:0,hitFlickerUntil:0,attackLungeX:0,attackLungeY:0,recoilX:0,recoilY:0};
const npc={x:18,y:11,name:"Edrin Vale",facing:"down"};
const hunterNpc={x:27,y:11,name:"Hunter Garran",displayLabel:"Hunter Garran",facing:"left"};
const vendorNpc={x:22,y:11,name:"Merchant Rowan",displayLabel:"Merchant Rowan",facing:"left"};
const WOLF_SPAWNS=[{id:1,x:32,y:14},{id:2,x:33,y:17},{id:3,x:12,y:1}];
const BANDIT_SPAWNS=[{id:1,x:34,y:15},{id:2,x:16,y:1},{id:3,x:21,y:2}];
const MIRROR_CAVE_WOLF_SPAWNS=[
  {id:101,x:13,y:13},
  {id:102,x:12,y:9},
  {id:103,x:11,y:6},
  {id:104,x:9,y:3}
];
const TOLLHOUSE_BANDIT_SPAWNS=[
  {id:201,x:9,y:9},
  {id:202,x:19,y:8},
  {id:203,x:21,y:5}
];
const ROOK_TOLLKEEPER_SPAWN={id:301,x:21,y:8};
function getEnemyConfig(enemyType){
  return BALANCE.enemies[enemyType] || BALANCE.enemies.wolf;
}
function createWolf(spawn,enemyType="wolf"){
  const enemyConfig=getEnemyConfig(enemyType);
  return {kind:"wolf",enemyType,id:spawn.id,x:spawn.x,y:spawn.y,px:spawn.x*TILE,py:spawn.y*TILE,targetX:spawn.x,targetY:spawn.y,hp:enemyConfig.hp,maxHp:enemyConfig.hp,homeX:spawn.x,homeY:spawn.y,roam:3,speed:110,facing:"left",attackUntil:0,hitUntil:0,hitFlickerUntil:0,attackLungeX:0,attackLungeY:0,recoilX:0,recoilY:0,moving:false,defeated:false};
}
function createBandit(spawn,enemyType="bandit",extras={}){
  const enemyConfig=getEnemyConfig(enemyType);
  return {
    kind:"bandit",
    enemyType,
    id:spawn.id,
    x:spawn.x,
    y:spawn.y,
    px:spawn.x*TILE,
    py:spawn.y*TILE,
    targetX:spawn.x,
    targetY:spawn.y,
    hp:enemyConfig.hp,
    maxHp:enemyConfig.hp,
    homeX:spawn.x,
    homeY:spawn.y,
    roam:extras.roam ?? 2,
    speed:extras.speed ?? 95,
    facing:extras.facing || "left",
    attackUntil:0,
    hitUntil:0,
    hitFlickerUntil:0,
    attackLungeX:0,
    attackLungeY:0,
    recoilX:0,
    recoilY:0,
    moving:false,
    defeated:false,
    isMiniBoss:Boolean(extras.isMiniBoss),
    displayName:extras.displayName || null,
    noRespawn:Boolean(extras.noRespawn)
  };
}
const wolves=WOLF_SPAWNS.map(createWolf);
const bandits=BANDIT_SPAWNS.map((spawn)=>createBandit(spawn,"bandit"));
const mirrorCaveWolves=MIRROR_CAVE_WOLF_SPAWNS.map((spawn)=>createWolf(spawn, "cave_wolf"));
const tollhouseBandits=TOLLHOUSE_BANDIT_SPAWNS.map((spawn)=>createBandit(spawn,"bandit",{ roam:1, speed:92 }));
const rookTollkeeper=createBandit(ROOK_TOLLKEEPER_SPAWN,"rook_tollkeeper",{ roam:1, speed:88, isMiniBoss:true, displayName:"Rook the Tollkeeper", noRespawn:true });
let isInMirrorCave=false;
let isInAbandonedTollhouse=false;
let rookEncounterAnnounced=false;
let transitionState={ active:false, start:0, duration:0, switched:false, onSwitch:null };
const worldObjects=[];
const worldObjectsById=new Map();
const persistentObjects={};
let worldInfoPanel=null;

function createWorldObject(config){
  return {
    objectId:config.objectId,
    type:config.type,
    zone:config.zone || null,
    region:config.region || null,
    dungeon:config.dungeon || null,
    x:config.x,
    y:config.y,
    state:config.state || "default",
    interactable:config.interactable!==false,
    collision:Boolean(config.collision),
    requiredQuestStage:config.requiredQuestStage || null,
    onInteract:typeof config.onInteract==="function" ? config.onInteract : null,
    persistence:config.persistence!==false,
    walkInTrigger:Boolean(config.walkInTrigger),
    promptLabel:config.promptLabel || null
  };
}
function registerWorldObject(config){
  const object=createWorldObject(config);
  worldObjects.push(object);
  worldObjectsById.set(object.objectId, object);
  if(object.persistence && !persistentObjects[object.objectId]) persistentObjects[object.objectId]={ state:object.state };
  return object;
}
function getPersistentObject(objectId){
  if(!persistentObjects[objectId]) persistentObjects[objectId]={};
  return persistentObjects[objectId];
}
function patchPersistentObject(objectId, patch, shouldSave=true){
  const existing=getPersistentObject(objectId);
  persistentObjects[objectId]={ ...existing, ...patch };
  if(shouldSave && typeof saveGame==="function") saveGame("object_state_change");
}
function getWorldObjectTile(object){
  const tx=typeof object.x==="function" ? object.x() : object.x;
  const ty=typeof object.y==="function" ? object.y() : object.y;
  return { x:tx, y:ty };
}
function isWorldObjectInCurrentZone(object){
  if(object.zone==="mirror_cave") return isInMirrorCave;
  if(object.zone==="abandoned_tollhouse") return isInAbandonedTollhouse;
  if(object.zone==="overworld") return !isInMirrorCave && !isInAbandonedTollhouse;
  return true;
}
function getActiveWorldObjects(){
  return worldObjects.filter((object)=>isWorldObjectInCurrentZone(object));
}
function isWorldObjectBlockingTile(x,y){
  return getActiveWorldObjects().some((object)=>{
    if(!object.collision) return false;
    const tile=getWorldObjectTile(object);
    return tile.x===x && tile.y===y;
  });
}
function createDefaultSkills(){
  return {
    swordsmanship:{ level:1, xp:0 },
    defense:{ level:1, xp:0 },
    survival:{ level:1, xp:0 }
  };
}
const DEFAULT_EQUIPMENT=Object.freeze({ weapon:"rusty_sword", armor:null, trinket:null });
const SAVE_OBJECT_ID_ALIASES=Object.freeze({
  tollhouse_reward_chest:"tollhouse_chest",
  mirror_pond_interaction:"mirror_pond",
  echo_fragment:"echo_fragment_object",
  east_road_sign:"north_road_notice",
  abandoned_tollhouse_state:"abandoned_tollhouse_state",
  rook_tollkeeper_state:"rook_tollkeeper_state"
});
const CANONICAL_SAVE_OBJECT_IDS=Object.freeze([
  "mirror_cave_chest",
  "echo_fragment_object",
  "tollhouse_chest",
  "north_road_notice",
  "mirror_pond",
  "abandoned_tollhouse_state",
  "rook_tollkeeper_state",
  "mirror_pond_sign"
]);
function canonicalizePersistentObjectId(objectId){
  if(typeof objectId!=="string") return null;
  return SAVE_OBJECT_ID_ALIASES[objectId] || objectId;
}
function normalizePersistentObjects(rawPersistentObjects){
  const normalized={};
  if(rawPersistentObjects && typeof rawPersistentObjects==="object"){
    Object.entries(rawPersistentObjects).forEach(([objectId, objectState])=>{
      const canonicalId=canonicalizePersistentObjectId(objectId);
      if(!canonicalId || !objectState || typeof objectState!=="object") return;
      normalized[canonicalId]={ ...(normalized[canonicalId]||{}), ...objectState };
    });
  }
  CANONICAL_SAVE_OBJECT_IDS.forEach((objectId)=>{
    if(!normalized[objectId]) normalized[objectId]={ state:"default" };
  });
  return normalized;
}
function getSkillLevelFromXp(totalXp){
  const normalizedXp=Math.max(0, Math.floor(Number.isFinite(totalXp) ? totalXp : 0));
  let level=1;
  for(let i=0; i<SKILL_LEVEL_THRESHOLDS.length; i++){
    if(normalizedXp>=SKILL_LEVEL_THRESHOLDS[i]) level=i+1;
  }
  return Math.min(SKILL_MAX_LEVEL, level);
}
function getSkillXpThresholdForLevel(level){
  const normalizedLevel=Math.max(1, Math.min(SKILL_MAX_LEVEL, Math.floor(Number.isFinite(level) ? level : 1)));
  return SKILL_LEVEL_THRESHOLDS[normalizedLevel-1];
}
function normalizeSkills(rawSkills){
  const defaults=createDefaultSkills();
  const normalized={};
  Object.keys(defaults).forEach((skillId)=>{
    const saved=rawSkills?.[skillId];
    const savedXp=Math.max(0, Math.floor(Number.isFinite(saved?.xp) ? saved.xp : 0));
    const levelFromXp=getSkillLevelFromXp(savedXp);
    const savedLevel=Math.max(1, Math.min(SKILL_MAX_LEVEL, Math.floor(Number.isFinite(saved?.level) ? saved.level : 1)));
    const resolvedLevel=Math.max(levelFromXp, savedLevel);
    const minXpForResolved=getSkillXpThresholdForLevel(resolvedLevel);
    normalized[skillId]={
      xp:Math.max(savedXp, minXpForResolved),
      level:resolvedLevel
    };
  });
  return normalized;
}
function getSkillLevel(skillId){
  return Math.max(1, Math.min(SKILL_MAX_LEVEL, Math.floor(Number.isFinite(player.skills?.[skillId]?.level) ? player.skills[skillId].level : 1)));
}
function gainSkillXp(skillId, amount){
  if(!player.skills?.[skillId]) return 0;
  const gained=Math.max(0, Math.floor(Number.isFinite(amount) ? amount : 0));
  if(gained<=0) return 0;
  const skill=player.skills[skillId];
  const beforeLevel=getSkillLevel(skillId);
  skill.xp=Math.max(0, Math.floor(Number.isFinite(skill.xp) ? skill.xp : 0)) + gained;
  skill.level=getSkillLevelFromXp(skill.xp);
  if(skill.level>beforeLevel){
    log(SKILL_DISPLAY_NAMES[skillId] + " increased to Level " + skill.level + ".");
    showRewardToast("Skill Up: " + SKILL_DISPLAY_NAMES[skillId] + " Lv " + skill.level, 1500);
  }
  return gained;
}
function getSwordsmanshipAttackBonus(){
  const level=getSkillLevel("swordsmanship");
  if(level>=4) return 2;
  if(level>=2) return 1;
  return 0;
}
function getDefenseSkillBonus(){
  const level=getSkillLevel("defense");
  if(level>=4) return 2;
  if(level>=2) return 1;
  return 0;
}
function getSurvivalHealingBonus(){
  const level=getSkillLevel("survival");
  if(level>=5) return 8;
  if(level===4) return 6;
  if(level===3) return 4;
  if(level===2) return 2;
  return 0;
}
function getTotalAttackDamage(){
  return BASE_PLAYER_DAMAGE + getEquippedWeaponBonus() + Math.max(0, player.baseAttackBonus||0) + getSwordsmanshipAttackBonus();
}
function getTotalDefenseRating(){
  return Math.max(0, getEquippedDefenseBonus() + Math.max(0, player.baseDefenseBonus||0) + getDefenseSkillBonus());
}

let lastPlayerAttack=0,hitStopUntil=0,lastNoTargetLogAt=0;
const lastWolfDecisionAt={};
const lastWolfAttackAt={};
const lastBanditDecisionAt={};
const lastBanditAttackAt={};
const wolfRespawnAtById={};
const banditRespawnAtById={};
let missNoticeArmed=true;
let hostileAggroBlockedUntil=0;
const PLAYER_ATTACK_RANGE=1;
const BASE_PLAYER_DAMAGE=BALANCE.player.baseDamage;

function getLevelProfile(level){
  const normalized=Math.max(1, Math.floor(Number.isFinite(level) ? level : 1));
  const found=LEVEL_PROGRESSION.find((entry)=>entry.level===normalized);
  return found || LEVEL_PROGRESSION[LEVEL_PROGRESSION.length-1];
}
function getLevelFromXp(totalXp){
  const normalizedXp=Math.max(0, Math.floor(Number.isFinite(totalXp) ? totalXp : 0));
  let resolvedLevel=1;
  for(const entry of LEVEL_PROGRESSION){
    if(normalizedXp>=entry.xpRequired) resolvedLevel=entry.level;
    else break;
  }
  return resolvedLevel;
}
function getNextLevelXpThreshold(level){
  const next=LEVEL_PROGRESSION.find((entry)=>entry.level===level+1);
  return next ? next.xpRequired : null;
}
function getXpProgressText(){
  const nextThreshold=getNextLevelXpThreshold(player.level);
  if(nextThreshold===null){
    return player.xp + " / MAX";
  }
  return player.xp + " / " + nextThreshold;
}
function applyProgressionForLevel(targetLevel,{announce=false}={}){
  const beforeLevel=player.level;
  const beforeProfile=getLevelProfile(beforeLevel);
  const beforeMaxHp=player.maxHp;
  const beforeAttack=player.baseAttackBonus;
  const beforeDefense=player.baseDefenseBonus;
  const profile=getLevelProfile(targetLevel);
  player.level=profile.level;
  player.maxHp=profile.maxHp;
  player.baseAttackBonus=profile.baseAttackBonus;
  player.baseDefenseBonus=profile.baseDefenseBonus;
  const gainedMaxHp=Math.max(0, player.maxHp-beforeMaxHp);
  if(gainedMaxHp>0) player.hp=Math.min(player.maxHp, player.hp + gainedMaxHp);
  if(announce && player.level>beforeLevel){
    const levelUpLines=["LEVEL UP — Level " + player.level];
    log(levelUpLines[0] + ".");
    if(player.maxHp>beforeProfile.maxHp){
      log("Max HP increased.");
      levelUpLines.push("Max HP +" + (player.maxHp-beforeProfile.maxHp));
    }
    if(player.baseAttackBonus>beforeAttack){
      log("Attack increased.");
      levelUpLines.push("Attack +" + (player.baseAttackBonus-beforeAttack));
    }
    if(player.baseDefenseBonus>beforeDefense){
      log("Defense increased.");
      levelUpLines.push("Defense +" + (player.baseDefenseBonus-beforeDefense));
    }
    showRewardToasts(levelUpLines);
  }
}
function syncLevelFromXp({announce=false}={}){
  let targetLevel=getLevelFromXp(player.xp);
  targetLevel=Math.min(MAX_DEFINED_LEVEL, targetLevel);
  while(player.level<targetLevel){
    applyProgressionForLevel(player.level+1,{announce});
  }
}
function grantPlayerXp(amount){
  const gained=Math.max(0, Math.floor(Number.isFinite(amount) ? amount : 0));
  if(gained<=0) return 0;
  player.xp += gained;
  syncLevelFromXp({announce:true});
  return gained;
}

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
  if(typeof updateHunterStageOneReadiness==="function") updateHunterStageOneReadiness();
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
function getArmorDefenseBonus(){
  const armor=getEquippedItem("armor");
  return (!armor || armor.type!=="armor") ? 0 : (Number.isFinite(armor.defenseBonus) ? armor.defenseBonus : 0);
}
function getTrinketDefenseBonus(){
  const trinket=getEquippedItem("trinket");
  return (!trinket || trinket.type!=="trinket") ? 0 : (Number.isFinite(trinket.defenseBonus) ? trinket.defenseBonus : 0);
}
function getEquippedDefenseBonus(){
  return getArmorDefenseBonus() + getTrinketDefenseBonus();
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
  const currentItem=getEquippedItem(slotName);
  if(!currentItem) return false;
  if(slotName==="weapon"){
    if(currentItem.id==="rusty_sword") return false;
    player.equipment.weapon="rusty_sword";
    log("Removed " + currentItem.name + ". Re-equipped Rusty Sword.");
    return true;
  }
  player.equipment[slotName]=null;
  log("Removed " + currentItem.name + ".");
  return true;
}
function applyIncomingDamage(rawDamage){
  const defense=getTotalDefenseRating();
  const reducedDamage=Math.max(1, Math.floor(rawDamage)-defense);
  player.hp=Math.max(0, player.hp-reducedDamage);
  if(reducedDamage>0 && getArmorDefenseBonus()>0){
    gainSkillXp("defense", 2);
  }
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
function rollEnemyLoot(enemyType){
  const config=getEnemyConfig(enemyType);
  return rollLootFromTable(config.lootTable || []);
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
function getBestUsableHealingItem(){
  const missingHp=Math.max(0, player.maxHp-player.hp);
  let herbCandidate=null;
  let potionCandidate=null;
  let fallbackCandidate=null;
  for(const entry of player.inventory){
    if(!entry || entry.quantity<=0) continue;
    const item=getItemDefinition(entry.itemId);
    if(!item || item.type!=="consumable") continue;
    const healAmount=Number.isFinite(item.healAmount) ? Math.floor(item.healAmount) : 0;
    if(healAmount<=0) continue;
    const candidate={ item, healAmount };
    if(item.id==="healing_herb"){
      if(!herbCandidate || healAmount<herbCandidate.healAmount) herbCandidate=candidate;
      continue;
    }
    if(item.id==="small_potion"){
      if(!potionCandidate || healAmount>potionCandidate.healAmount) potionCandidate=candidate;
      continue;
    }
    if(!fallbackCandidate || healAmount>fallbackCandidate.healAmount || (healAmount===fallbackCandidate.healAmount && item.value<fallbackCandidate.item.value)){
      fallbackCandidate=candidate;
    }
  }
  if(herbCandidate && missingHp<=herbCandidate.healAmount) return herbCandidate.item;
  if(potionCandidate && missingHp>=potionCandidate.healAmount) return potionCandidate.item;
  if(herbCandidate) return herbCandidate.item;
  if(potionCandidate) return potionCandidate.item;
  return fallbackCandidate?.item || null;
}
function useHealingConsumable(){
  if(player.hp>=player.maxHp){
    log("HP is already full.");
    return false;
  }
  const item=getBestUsableHealingItem();
  if(!item){
    log("No healing items available.");
    return false;
  }
  return consumeHealingItem(item);
}
function consumeHealingItem(item){
  if(!item || item.type!=="consumable") return false;
  if(player.hp>=player.maxHp){
    log("HP is already full.");
    return false;
  }
  const healAmount=Math.max(0, Math.floor(Number.isFinite(item.healAmount) ? item.healAmount : 0)) + getSurvivalHealingBonus();
  if(healAmount<=0) return false;
  const removed=removeItemFromInventory(item.id, 1);
  if(removed<=0) return false;
  const hpBefore=player.hp;
  player.hp=Math.min(player.maxHp, player.hp + healAmount);
  const restored=player.hp-hpBefore;
  if(restored<=0) return false;
  let survivalGain=0;
  if(item.id==="healing_herb") survivalGain=gainSkillXp("survival", 5);
  if(item.id==="small_potion") survivalGain=gainSkillXp("survival", 8);
  log("Used " + item.name + ". Restored " + restored + " HP.");
  spawnFloatingText(player.px/TILE, player.py/TILE, "+" + restored, { color:"#7df7a2", durationMs:1000, rise:18 });
  showRewardToast("Used " + item.name + "  +" + restored + " HP", 1300);
  if(survivalGain>0) log("Survival experience gained.");
  saveGame("consume_item");
  return true;
}
function getVendorBuyCost(item){
  if(!item) return 0;
  if(item.id==="leather_armor") return 30;
  if(item.id==="small_potion") return 14;
  if(item.id==="healing_herb") return 5;
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
const HunterQuestStage = Object.freeze({
  NOT_STARTED:"not_started",
  STAGE_1_PROVE_YOURSELF:"stage_1_prove_yourself",
  STAGE_2_RETURN_TO_HUNTER:"stage_2_return_to_hunter",
  STAGE_3_MIRROR_CAVE:"stage_3_mirror_cave",
  STAGE_4_RETURN_WITH_RELIC:"stage_4_return_with_relic",
  COMPLETED:"completed"
});
const StillWaterQuestStage = Object.freeze({
  NOT_STARTED:"not_started",
  STAGE_1_SPEAK_WITH_EDRIN:"stage_1_speak_with_edrin",
  STAGE_2_INSPECT_MIRROR_POND:"stage_2_inspect_mirror_pond",
  STAGE_3_RETURN_TO_EDRIN:"stage_3_return_to_edrin",
  STAGE_4_ENTER_MIRROR_CAVE:"stage_4_enter_mirror_cave",
  STAGE_5_RECOVER_ECHO_FRAGMENT:"stage_5_recover_echo_fragment",
  STAGE_6_RETURN_TO_EDRIN:"stage_6_return_to_edrin",
  COMPLETED:"completed"
});
let mirrorCaveChestDiscovered=false;
let rookTollkeeperDefeated=false;
let abandonedTollhouseDiscovered=false;
let abandonedTollhouseCleared=false;
let hunterQuestRewardClaimed=false;

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
    if(rewardXp>0) grantPlayerXp(rewardXp);
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
  refreshAllItemProgress(){
    const quest=this.getQuest("hunters_request");
    if(!quest || quest.state===QuestState.NOT_STARTED || quest.state===QuestState.COMPLETED) return false;
    const peltObjective=this.getObjective("hunters_request", "pelts");
    if(!peltObjective) return false;
    const before=peltObjective.currentAmount;
    const currentPelts=Math.max(0, Math.min(peltObjective.requiredAmount, getItemQuantity("wolf_pelt")));
    peltObjective.currentAmount=currentPelts;
    peltObjective.completed=currentPelts>=peltObjective.requiredAmount;
    if(before!==peltObjective.currentAmount){
      this.events.emit("quest:state-changed",{questId:"hunters_request",state:quest.state,progress:quest.progress});
      return true;
    }
    return false;
  }
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
    const stage=getHunterQuestStage();
    const wolvesObjective=questSystem.getObjective("hunters_request", "wolves");
    if(stage===HunterQuestStage.STAGE_1_PROVE_YOURSELF){
      const wolves=Math.max(0, Math.min(3, wolvesObjective?.currentAmount || 0));
      const pelts=Math.max(0, Math.min(3, getItemQuantity("wolf_pelt")));
      return ["", "• Defeat Wolves: " + wolves + "/3", "• Wolf Pelts: " + pelts + "/3"];
    }
    if(stage===HunterQuestStage.STAGE_2_RETURN_TO_HUNTER) return ["", "• Return to Hunter Garran"];
    if(stage===HunterQuestStage.STAGE_3_MIRROR_CAVE) return ["", "• Enter Mirror Cave", "• Recover the Mirror Relic"];
    if(stage===HunterQuestStage.STAGE_4_RETURN_WITH_RELIC) return ["", "• Return to Hunter Garran"];
    return [];
  }
  getDisplayLines(node){
    const baseLines=Array.isArray(node?.lines) ? node.lines : [];
    if(!this.activeSession) return baseLines;
    if(this.activeSession.characterId==="hunter_garran" && (this.activeSession.nodeId==="hunters_request_stage_1_active" || this.activeSession.nodeId==="hunters_request_stage_3_active")){
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
    dialogueActions.innerHTML="";
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
      dialogueHint.textContent="Press 1-9 to choose an option. Press Esc or E to close.";
      dialogueActions.innerHTML="<button type=\"button\" class=\"dialogue-action\" data-dialogue-close>Close</button>";
    } else {
      dialogueChoices.innerHTML="";
      dialogueText.textContent=displayLines[session.lineIndex] || "...";
      dialogueHint.textContent="Click Continue, click dialogue text, or press E. Press Esc to close.";
      dialogueActions.innerHTML="<button type=\"button\" class=\"dialogue-action\" data-dialogue-advance>Continue</button><button type=\"button\" class=\"dialogue-action\" data-dialogue-close>Close</button>";
    }
    updateDialogueViewportConstraints();
  }
}

function getMirrorCaveChestState(){
  const persistent=getPersistentObject("mirror_cave_chest");
  if(persistent.opened || mirrorCave.chest.opened) return "open";
  const stage=getHunterQuestStage();
  if(stage===HunterQuestStage.STAGE_3_MIRROR_CAVE) return "closed";
  return "sealed";
}
function syncMirrorCaveChestState(shouldSave=false){
  const state=getMirrorCaveChestState();
  mirrorCave.chest.opened=state==="open";
  patchPersistentObject("mirror_cave_chest", {
    state,
    opened:state==="open"
  }, shouldSave);
  return state;
}
function getTollhouseChestState(){
  const persistent=getPersistentObject("tollhouse_chest");
  if(persistent.opened) return "open";
  if(rookTollkeeperDefeated) return "closed";
  return "locked";
}
function isTollhouseChestOpened(){
  return getTollhouseChestState()==="open";
}
function evaluateAbandonedTollhouseCleared(){
  return Boolean(rookTollkeeperDefeated && isTollhouseChestOpened());
}
function markAbandonedTollhouseDiscovered(shouldSave=false, showToast=false){
  if(abandonedTollhouseDiscovered) return false;
  abandonedTollhouseDiscovered=true;
  patchPersistentObject("abandoned_tollhouse_state", { discovered:true, state:"discovered" }, false);
  log("Discovered: Abandoned Tollhouse.");
  if(showToast) showRewardToast("Abandoned Tollhouse discovered.");
  if(shouldSave && typeof saveGame==="function") saveGame("object_state_change");
  return true;
}
function syncAbandonedTollhouseClearedState(shouldSave=false, announce=false){
  const cleared=evaluateAbandonedTollhouseCleared();
  const wasCleared=abandonedTollhouseCleared;
  abandonedTollhouseCleared=cleared;
  patchPersistentObject("abandoned_tollhouse_state", {
    discovered:abandonedTollhouseDiscovered,
    cleared,
    state:cleared ? "cleared" : (abandonedTollhouseDiscovered ? "discovered" : "active")
  }, shouldSave);
  if(announce && cleared && !wasCleared) log("Abandoned Tollhouse cleared.");
  return cleared;
}
function syncTollhouseChestState(shouldSave=false){
  const state=getTollhouseChestState();
  patchPersistentObject("tollhouse_chest", {
    state,
    opened:state==="open"
  }, shouldSave);
  syncAbandonedTollhouseClearedState(false, false);
  return state;
}
function grantTollhouseChestRewards(){
  const rewardsGranted=[];
  const rewardToasts=[];
  if(getItemQuantity("old_toll_key")<=0){
    addItemToInventory("old_toll_key", 1);
    rewardsGranted.push("Old Toll Key x1");
    rewardToasts.push("+ Old Toll Key");
  }
  if(getItemQuantity("travelers_charm")<=0 && player.equipment.trinket!=="travelers_charm"){
    addItemToInventory("travelers_charm", 1);
    rewardsGranted.push("Traveler's Charm x1");
    rewardToasts.push("+ Traveler's Charm");
  }
  addItemToInventory("small_potion", 1);
  rewardsGranted.push("Small Potion x1");
  rewardToasts.push("+ Small Potion");
  player.coins += 25;
  rewardsGranted.push("25 coins");
  rewardToasts.push("+25 Coins");
  return { rewardsGranted, rewardToasts };
}
function openWorldInfoPanel(title,text){
  worldInfoPanel={ title, text };
  dialogue.style.display="block";
  dialogueName.textContent=title;
  dialogueText.textContent=text;
  dialogueChoices.innerHTML="";
  dialogueHint.textContent="Press Esc or E to close.";
  dialogueActions.innerHTML="<button type=\"button\" class=\"dialogue-action\" data-world-info-close>Close</button>";
  updateDialogueViewportConstraints();
}
function closeWorldInfoPanel(){
  worldInfoPanel=null;
  dialogueChoices.innerHTML="";
  dialogueActions.innerHTML="";
  dialogue.style.display="none";
}

class InteractionManager {
  constructor(range){ this.range=range; this.interactables=[]; }
  register(interactable){ this.interactables.push(interactable); }
  getRangeForTarget(target){
    const configuredRange=Number.isFinite(target?.range) ? Math.max(1, Math.floor(target.range)) : this.range;
    return configuredRange;
  }
  resolvePromptLabel(target){
    if(!target) return "";
    if(typeof target.promptLabel==="function") return target.promptLabel() || "";
    return target.promptLabel || "";
  }
  isInRange(target){
    return Math.abs(player.targetX-target.x()) + Math.abs(player.targetY-target.y()) <= this.getRangeForTarget(target);
  }
  getNearest(){
    let nearest=null;
    for(const target of this.interactables){
      const distance=Math.abs(player.targetX-target.x()) + Math.abs(player.targetY-target.y());
      if(distance>this.getRangeForTarget(target)) continue;
      if(!nearest || distance<nearest.distance) nearest={target,distance};
    }
    return nearest?.target || null;
  }
  getPromptText(){
    const target=this.getNearest();
    if(!target) return "";
    const promptLabel=this.resolvePromptLabel(target);
    if(promptLabel) return "E : " + promptLabel;
    return "";
  }
  tryInteract(){
    if(worldInfoPanel){ closeWorldInfoPanel(); return true; }
    if(dialogueSystem.activeSession){ dialogueSystem.close(); return true; }
    if(isVendorOpen()){ closeVendorMenu(); return true; }
    const target=this.getNearest();
    if(!target) return false;
    target.onInteract?.();
    eventSystem.emit("interaction:used",{id:target.id,type:target.type});
    return true;
  }
  interactAt(x,y){
    if(worldInfoPanel){ closeWorldInfoPanel(); return true; }
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

function getHunterQuestStage(){
  const quest=questSystem.getQuest("hunters_request");
  if(!quest) return HunterQuestStage.NOT_STARTED;
  if(quest.state===QuestState.COMPLETED) return HunterQuestStage.COMPLETED;
  const progress=typeof quest.progress==="string" ? quest.progress : "";
  if(Object.values(HunterQuestStage).includes(progress)) return progress;
  return quest.state===QuestState.NOT_STARTED ? HunterQuestStage.NOT_STARTED : HunterQuestStage.STAGE_1_PROVE_YOURSELF;
}
function setHunterQuestStage(stage){
  const quest=questSystem.getQuest("hunters_request");
  if(!quest) return;
  if(stage===HunterQuestStage.NOT_STARTED){
    quest.state=QuestState.NOT_STARTED;
    quest.status=quest.state;
    quest.progress=HunterQuestStage.NOT_STARTED;
  } else if(stage===HunterQuestStage.COMPLETED){
    quest.state=QuestState.COMPLETED;
    quest.status=quest.state;
    quest.progress=HunterQuestStage.COMPLETED;
  } else {
    if(quest.state===QuestState.NOT_STARTED || quest.state===QuestState.COMPLETED) quest.state=QuestState.ACTIVE;
    if(quest.state===QuestState.READY_TO_TURN_IN) quest.state=QuestState.ACTIVE;
    quest.status=quest.state;
    quest.progress=stage;
  }
  eventSystem.emit("quest:state-changed",{questId:"hunters_request",state:quest.state,progress:quest.progress});
}
function isHunterStageOneReady(){
  const wolvesObjective=questSystem.getObjective("hunters_request", "wolves");
  return Boolean(wolvesObjective && wolvesObjective.currentAmount>=3 && getItemQuantity("wolf_pelt")>=3);
}
function updateHunterStageOneReadiness(){
  const stage=getHunterQuestStage();
  if(stage!==HunterQuestStage.STAGE_1_PROVE_YOURSELF) return;
  if(!isHunterStageOneReady()) return;
  setHunterQuestStage(HunterQuestStage.STAGE_2_RETURN_TO_HUNTER);
  log("Objective Complete: Return to Hunter Garran with 3 Wolf Pelts.");
}
function getStillWaterQuestStage(){
  const quest=questSystem.getQuest("the_still_water");
  if(!quest) return StillWaterQuestStage.NOT_STARTED;
  if(quest.state===QuestState.COMPLETED) return StillWaterQuestStage.COMPLETED;
  const progress=typeof quest.progress==="string" ? quest.progress : "";
  if(Object.values(StillWaterQuestStage).includes(progress)) return progress;
  return quest.state===QuestState.NOT_STARTED ? StillWaterQuestStage.NOT_STARTED : StillWaterQuestStage.STAGE_1_SPEAK_WITH_EDRIN;
}
function setStillWaterQuestStage(stage){
  const quest=questSystem.getQuest("the_still_water");
  if(!quest) return;
  if(stage===StillWaterQuestStage.NOT_STARTED){
    quest.state=QuestState.NOT_STARTED;
    quest.status=quest.state;
    quest.progress=StillWaterQuestStage.NOT_STARTED;
  } else if(stage===StillWaterQuestStage.COMPLETED){
    quest.state=QuestState.COMPLETED;
    quest.status=quest.state;
    quest.progress=StillWaterQuestStage.COMPLETED;
  } else {
    if(quest.state===QuestState.NOT_STARTED || quest.state===QuestState.COMPLETED) quest.state=QuestState.ACTIVE;
    if(quest.state===QuestState.READY_TO_TURN_IN) quest.state=QuestState.ACTIVE;
    quest.status=quest.state;
    quest.progress=stage;
  }
  eventSystem.emit("quest:state-changed",{questId:"the_still_water",state:quest.state,progress:quest.progress});
}
function isStillWaterEchoFragmentCollected(){
  const persistent=getPersistentObject("echo_fragment_object");
  return Boolean(persistent.collected) || getItemQuantity("echo_fragment")>0;
}
function syncEchoFragmentState(shouldSave=false){
  const collected=isStillWaterEchoFragmentCollected();
  patchPersistentObject("echo_fragment_object", { state:collected ? "collected" : "inert", collected }, shouldSave);
  return collected;
}
function getStillWaterObjectiveText(){
  const quest=questSystem.getQuest("the_still_water");
  const stage=getStillWaterQuestStage();
  const fallbackText="The Still Water\nObjective: Return to Edrin Vale";
  if(stage===StillWaterQuestStage.COMPLETED || quest?.state===QuestState.COMPLETED){
    return getContextualObjectiveText();
  }
  if(stage===StillWaterQuestStage.NOT_STARTED || stage===StillWaterQuestStage.STAGE_1_SPEAK_WITH_EDRIN){
    return "The Still Water\nObjective: Speak with Edrin Vale";
  }
  if(stage===StillWaterQuestStage.STAGE_2_INSPECT_MIRROR_POND){
    return "The Still Water\nObjective: Inspect Mirror Pond";
  }
  if(stage===StillWaterQuestStage.STAGE_3_RETURN_TO_EDRIN){
    return "The Still Water\nObjective: Return to Edrin Vale";
  }
  if(stage===StillWaterQuestStage.STAGE_4_ENTER_MIRROR_CAVE){
    return "The Still Water\nObjective: Enter Mirror Cave";
  }
  if(stage===StillWaterQuestStage.STAGE_5_RECOVER_ECHO_FRAGMENT){
    return "The Still Water\nObjective: Recover the Echo Fragment";
  }
  if(stage===StillWaterQuestStage.STAGE_6_RETURN_TO_EDRIN){
    if(quest?.state===QuestState.READY_TO_TURN_IN){
      return "The Still Water\nObjective: Speak with Edrin Vale";
    }
    return "The Still Water\nObjective: Return to Edrin Vale with the Echo Fragment";
  }
  if((quest?.state===QuestState.ACTIVE || quest?.state===QuestState.READY_TO_TURN_IN) && DEV_MODE){
    console.warn("Unknown objective stage for The Still Water: " + String(stage));
  }
  return fallbackText;
}
function hasActiveGuidedQuest(){
  const hunterQuest=questSystem.getQuest("hunters_request");
  const stillWaterQuest=questSystem.getQuest("the_still_water");
  const hunterActive=hunterQuest && hunterQuest.state!==QuestState.NOT_STARTED && hunterQuest.state!==QuestState.COMPLETED;
  const stillWaterActive=stillWaterQuest && stillWaterQuest.state!==QuestState.NOT_STARTED && stillWaterQuest.state!==QuestState.COMPLETED;
  return Boolean(hunterActive || stillWaterActive);
}
function hasCompletedVerticalSliceCoreQuests(){
  const hunterQuest=questSystem.getQuest("hunters_request");
  const stillWaterQuest=questSystem.getQuest("the_still_water");
  return hunterQuest?.state===QuestState.COMPLETED && stillWaterQuest?.state===QuestState.COMPLETED;
}
function isVerticalSliceCleared(){
  return hasCompletedVerticalSliceCoreQuests() && abandonedTollhouseCleared && isTollhouseChestOpened();
}
function maybeAnnounceVerticalSliceEndpoint(){
  if(!isVerticalSliceCleared()) return;
  const persistent=getPersistentObject("vertical_slice_endpoint");
  if(persistent.announced) return;
  patchPersistentObject("vertical_slice_endpoint", { state:"announced", announced:true }, false);
  log("For now, Hearthvale is safer. But Mirror Pond has not gone still.");
  showRewardToast("Vertical Slice Complete", 2200);
  saveGame("vertical_slice_endpoint");
}
function getContextualObjectiveText(){
  if(isVerticalSliceCleared()) return "For now, Hearthvale is safer. But Mirror Pond has not gone still.";
  if(!abandonedTollhouseDiscovered) return "Explore Hearthvale and the surrounding roads.";
  if(!rookTollkeeperDefeated) return "Defeat Rook the Tollkeeper in the Abandoned Tollhouse.";
  if(!isTollhouseChestOpened()) return "Open the tollhouse chest.";
  return "Explore Hearthvale and the surrounding roads.";
}
function handleNorthRoadArrivalAtmosphere(){
  const persistent=getPersistentObject("north_road_intro");
  if(!persistent.entered){
    patchPersistentObject("north_road_intro", { entered:true, state:"entered" }, false);
    log("Entered North Road.");
    if(!hasActiveGuidedQuest()) log("The road continues north, but Hearthvale feels far behind.");
    saveGame("object_state_change");
    return;
  }
  if(!hasActiveGuidedQuest()) logThrottled("north_road_atmosphere", "The road continues north, but Hearthvale feels far behind.", 3000);
}
function migrateStillWaterStateFromSave(){
  const quest=questSystem.getQuest("the_still_water");
  if(!quest || quest.state===QuestState.NOT_STARTED || quest.state===QuestState.COMPLETED) return;
  const stage=getStillWaterQuestStage();
  const hasFragment=isStillWaterEchoFragmentCollected();
  if(!hasFragment) return;
  if(stage===StillWaterQuestStage.STAGE_6_RETURN_TO_EDRIN) return;
  questSystem.completeObjective("the_still_water", "recover_echo_fragment");
  setStillWaterQuestStage(StillWaterQuestStage.STAGE_6_RETURN_TO_EDRIN);
}

eventSystem.registerZoneTrigger("Mirror Pond", "zone:entered:mirror_pond");
eventSystem.registerZoneTrigger("North Road", "zone:entered:north_road");
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
eventSystem.on("zone:entered:north_road", ()=>handleNorthRoadArrivalAtmosphere());
eventSystem.on("combat:enemy-defeated", ({enemyType})=>{
  const stage=getHunterQuestStage();
  if((stage!==HunterQuestStage.STAGE_1_PROVE_YOURSELF && stage!==HunterQuestStage.STAGE_2_RETURN_TO_HUNTER) || enemyType!=="wolf") return;
  questSystem.incrementObjective("hunters_request", "wolves", 1);
  updateHunterStageOneReadiness();
});
eventSystem.on("zone:entered:mirror_cave", ()=>{
  if(getHunterQuestStage()!==HunterQuestStage.STAGE_3_MIRROR_CAVE) return;
  if(questSystem.completeObjective("hunters_request", "enter_cave")) log("Objective Complete: Entered Mirror Cave");
});
eventSystem.on("zone:entered:mirror_cave", ()=>{
  if(getStillWaterQuestStage()!==StillWaterQuestStage.STAGE_4_ENTER_MIRROR_CAVE) return;
  questSystem.completeObjective("the_still_water", "enter_cave");
  setStillWaterQuestStage(StillWaterQuestStage.STAGE_5_RECOVER_ECHO_FRAGMENT);
  log("Objective Updated: Recover the Echo Fragment from Mirror Cave.");
});
eventSystem.on("object:opened:mirror_cave_chest", ()=>{
  if(getHunterQuestStage()!==HunterQuestStage.STAGE_3_MIRROR_CAVE) return;
  if(questSystem.completeObjective("hunters_request", "open_chest")) log("Objective Complete: Recovered the relic from Mirror Cave");
  setHunterQuestStage(HunterQuestStage.STAGE_4_RETURN_WITH_RELIC);
});
eventSystem.on("quest:activate:hunters_request", ()=>{
  const quest=questSystem.getQuest("hunters_request");
  if(!quest || quest.state===QuestState.COMPLETED) return;
  setHunterQuestStage(HunterQuestStage.STAGE_1_PROVE_YOURSELF);
  questSystem.refreshAllItemProgress();
  updateHunterStageOneReadiness();
});
eventSystem.on("quest:activate:the_still_water", ()=>{
  const quest=questSystem.getQuest("the_still_water");
  if(!quest || quest.state===QuestState.COMPLETED) return;
  setStillWaterQuestStage(StillWaterQuestStage.STAGE_2_INSPECT_MIRROR_POND);
  log("Edrin Vale sent you to inspect Mirror Pond.");
});
eventSystem.on("quest:still_water:report_pond", ()=>{
  if(getStillWaterQuestStage()!==StillWaterQuestStage.STAGE_3_RETURN_TO_EDRIN) return;
  if(getHunterQuestStage()===HunterQuestStage.COMPLETED || mirrorCave.chest.opened){
    log("Edrin: You already walked the cave once. Go again — now with eyes open.");
  }
  setStillWaterQuestStage(StillWaterQuestStage.STAGE_4_ENTER_MIRROR_CAVE);
});
eventSystem.on("object:collected:echo_fragment", ()=>{
  if(getStillWaterQuestStage()!==StillWaterQuestStage.STAGE_5_RECOVER_ECHO_FRAGMENT) return;
  questSystem.completeObjective("the_still_water", "recover_echo_fragment");
  setStillWaterQuestStage(StillWaterQuestStage.STAGE_6_RETURN_TO_EDRIN);
  log("Objective Updated: Return to Edrin Vale with the Echo Fragment.");
});
eventSystem.on("quest:still_water:final_turn_in", ()=>{
  if(getStillWaterQuestStage()!==StillWaterQuestStage.STAGE_6_RETURN_TO_EDRIN){
    log("Return after recovering the Echo Fragment.");
    return;
  }
  if(getItemQuantity("echo_fragment")<1 && !isStillWaterEchoFragmentCollected()){
    log("You need the Echo Fragment first.");
    return;
  }
  removeItemFromInventory("echo_fragment", 1);
  questSystem.completeObjective("the_still_water", "return_edrin");
  questSystem.completeQuest("the_still_water");
});
eventSystem.on("quest:hunter:turn_in_pelts", ()=>{
  if(getHunterQuestStage()!==HunterQuestStage.STAGE_2_RETURN_TO_HUNTER) return;
  if(getItemQuantity("wolf_pelt")<3){
    log("Bring me 3 Wolf Pelts first.");
    return;
  }
  removeItemFromInventory("wolf_pelt", 3);
  if(mirrorCaveChestDiscovered) log("You found the old chest, then. Good. Now you know why I needed proof first.");
  questSystem.completeObjective("hunters_request", "pelts");
  setHunterQuestStage(HunterQuestStage.STAGE_3_MIRROR_CAVE);
  log("Hunter Garran sent you to Mirror Cave to recover the Mirror Relic.");
});
eventSystem.on("quest:hunter:final_turn_in", ()=>{
  if(getHunterQuestStage()!==HunterQuestStage.STAGE_4_RETURN_WITH_RELIC){
    log("Recover the Mirror Relic from Mirror Cave first.");
    return;
  }
  if(getItemQuantity("mirror_relic")<1){
    log("You need the Mirror Relic before this can be completed.");
    return;
  }
  removeItemFromInventory("mirror_relic", 1);
  if(!hunterQuestRewardClaimed){
    if(getItemQuantity("iron_sword")<=0){
      addItemToInventory("iron_sword", 1);
      log("You obtained Iron Sword.");
    }
    player.coins += 24;
    grantPlayerXp(65);
    addItemToInventory("small_potion", 2);
    log("Rewards: +65 XP, +24 Coins, Small Potion x2.");
    showRewardToasts(["Hunter's Request Complete", "+65 XP", "+24 Coins", "+ Iron Sword", "+ Small Potion x2"]);
    hunterQuestRewardClaimed=true;
  }
  questSystem.completeObjective("hunters_request", "return_hunter");
  questSystem.completeQuest("hunters_request");
});
eventSystem.on("quest:report:mirror_pond", ()=>{
  const quest=questSystem.getQuest("mirror_pond_listening");
  if(quest?.state!==QuestState.ACTIVE || quest.progress!=="heard_whispers") return;
  questSystem.completeQuest("mirror_pond_listening");
});
eventSystem.on("quest:completed:mirror_pond_listening", ()=>eventSystem.emit("world:pond:awakened"));
eventSystem.on("quest:completed:the_still_water", ()=>syncEchoFragmentState(false));
eventSystem.on("quest:completed:hunters_request", ()=>maybeAnnounceVerticalSliceEndpoint());
eventSystem.on("quest:completed:the_still_water", ()=>maybeAnnounceVerticalSliceEndpoint());
let worldEvents={ pondAwakened:false };
const worldTriggeredEvents=new Set();
eventSystem.on("world:pond:awakened", ()=>{
  if(worldEvents.pondAwakened) return;
  worldEvents.pondAwakened=true;
  worldTriggeredEvents.add("world:pond:awakened");
  log("World Event: Mirror Pond awakens and the air goes still.");
});

const SAVE_KEY="wayfarer.save.v1";
const SAVE_BACKUP_KEY="wayfarer.save.v1.backup";
const SAVE_SCHEMA_VERSION=2;
const SUPPORTED_SAVE_VERSIONS=new Set([1,2,3,4,5,6,7,8,9,10,11,12,13]);
const DEFAULT_DEV_MODE=false;
let DEV_MODE=DEFAULT_DEV_MODE;
let saveNoticeTimeout=0;
function showSaveNotice(message){
  saveNotice.textContent=message;
  saveNotice.classList.add("visible");
  if(saveNoticeTimeout) clearTimeout(saveNoticeTimeout);
  saveNoticeTimeout=setTimeout(()=>saveNotice.classList.remove("visible"), 1400);
}
function isFiniteNumber(value){ return typeof value==="number" && Number.isFinite(value); }
function cloneValue(value){
  return JSON.parse(JSON.stringify(value));
}
function createDefaultSave(reason="default"){
  const questStates=(questData.quests||[]).map((definition)=>({
    id:definition.id,
    state:QuestState.NOT_STARTED,
    status:QuestState.NOT_STARTED,
    progress:definition.initialProgress || "",
    objectives:questSystem.normalizeObjectives(definition.objectives||[]).map((objective)=>({
      id:objective.id,
      currentAmount:0,
      completed:false
    }))
  }));
  return {
    version:13,
    saveSchemaVersion:SAVE_SCHEMA_VERSION,
    reason,
    savedAt:new Date().toISOString(),
    player:{
      zoneId:"hearthvale_square",
      position:{ x:18, y:11 },
      level:1,
      hp:BALANCE.player.startingMaxHp,
      maxHp:BALANCE.player.startingMaxHp,
      xp:0,
      baseAttackBonus:0,
      baseDefenseBonus:0,
      coins:0,
      skills:createDefaultSkills(),
      inventory:[{ itemId:"rusty_sword", quantity:1 }],
      equipment:{ ...DEFAULT_EQUIPMENT }
    },
    quests:{
      questStates,
      completedQuests:[],
      activeQuests:[]
    },
    world:{
      triggeredEvents:[],
      stateChanges:{ pondAwakened:false },
      persistentObjects:normalizePersistentObjects({}),
      mirrorCave:{ chestDiscovered:false, chestOpened:false, cleared:false },
      tollhouse:{
        abandonedTollhouseDiscovered:false,
        rookTollkeeperDefeated:false,
        chestState:"closed",
        abandonedTollhouseCleared:false
      },
      hunterQuest:{
        hunterQuestStage:HunterQuestStage.NOT_STARTED,
        hunterQuestRewardClaimed:false
      },
      creatures:{
        wolves:[],
        bandits:[],
        tollhouseBandits:[],
        rookTollkeeper:{ hp:getEnemyConfig("rook_tollkeeper").hp, defeated:false },
        mirrorCaveWolves:[]
      }
    },
    systems:{
      currentObjective:getContextualObjectiveText(),
      discoveredLocations:["hearthvale_square"],
      devMode:DEFAULT_DEV_MODE
    }
  };
}
function migrateSave(rawSave){
  const base=createDefaultSave("migration");
  const incoming=(rawSave && typeof rawSave==="object") ? rawSave : {};
  const migrated=cloneValue(base);
  migrated.version=SUPPORTED_SAVE_VERSIONS.has(incoming.version) ? incoming.version : base.version;
  const incomingSchema=Number.isInteger(incoming.saveSchemaVersion) ? incoming.saveSchemaVersion : 1;
  migrated.saveSchemaVersion=Math.max(1, Math.min(SAVE_SCHEMA_VERSION, incomingSchema));
  migrated.savedAt=typeof incoming.savedAt==="string" ? incoming.savedAt : base.savedAt;
  migrated.reason=typeof incoming.reason==="string" ? incoming.reason : base.reason;
  const rawPlayer=incoming.player && typeof incoming.player==="object" ? incoming.player : {};
  migrated.player.position={
    x:Number.isInteger(rawPlayer.position?.x) ? rawPlayer.position.x : base.player.position.x,
    y:Number.isInteger(rawPlayer.position?.y) ? rawPlayer.position.y : base.player.position.y
  };
  migrated.player.zoneId=typeof rawPlayer.zoneId==="string" ? rawPlayer.zoneId : base.player.zoneId;
  migrated.player.xp=Math.max(0, Math.floor(Number.isFinite(rawPlayer.xp) ? rawPlayer.xp : base.player.xp));
  const xpResolvedLevel=getLevelFromXp(migrated.player.xp);
  const savedLevel=Math.max(1, Math.floor(Number.isFinite(rawPlayer.level) ? rawPlayer.level : xpResolvedLevel));
  migrated.player.level=Math.max(xpResolvedLevel, Math.min(MAX_DEFINED_LEVEL, savedLevel));
  const levelProfile=getLevelProfile(migrated.player.level);
  migrated.player.maxHp=Math.max(levelProfile.maxHp, Math.floor(Number.isFinite(rawPlayer.maxHp) ? rawPlayer.maxHp : levelProfile.maxHp));
  migrated.player.baseAttackBonus=Math.max(levelProfile.baseAttackBonus, Math.floor(Number.isFinite(rawPlayer.baseAttackBonus) ? rawPlayer.baseAttackBonus : levelProfile.baseAttackBonus));
  migrated.player.baseDefenseBonus=Math.max(levelProfile.baseDefenseBonus, Math.floor(Number.isFinite(rawPlayer.baseDefenseBonus) ? rawPlayer.baseDefenseBonus : levelProfile.baseDefenseBonus));
  migrated.player.hp=Math.max(0, Math.min(migrated.player.maxHp, Math.floor(Number.isFinite(rawPlayer.hp) ? rawPlayer.hp : migrated.player.maxHp)));
  migrated.player.coins=Math.max(0, Math.floor(Number.isFinite(rawPlayer.coins) ? rawPlayer.coins : base.player.coins));
  migrated.player.skills=normalizeSkills(rawPlayer.skills);
  migrated.player.inventory=normalizeInventory(rawPlayer.inventory);
  if(rawPlayer.equipment && typeof rawPlayer.equipment==="object"){
    migrated.player.equipment={
      weapon:typeof rawPlayer.equipment.weapon==="string" ? rawPlayer.equipment.weapon : DEFAULT_EQUIPMENT.weapon,
      armor:typeof rawPlayer.equipment.armor==="string" ? rawPlayer.equipment.armor : DEFAULT_EQUIPMENT.armor,
      trinket:typeof rawPlayer.equipment.trinket==="string" ? rawPlayer.equipment.trinket : DEFAULT_EQUIPMENT.trinket
    };
  } else if(rawPlayer.weapon && typeof rawPlayer.weapon==="object"){
    migrated.player.equipment={ ...DEFAULT_EQUIPMENT };
  }
  const rawQuests=incoming.quests && typeof incoming.quests==="object" ? incoming.quests : {};
  migrated.quests.questStates=Array.isArray(rawQuests.questStates) ? rawQuests.questStates : base.quests.questStates;
  migrated.quests.completedQuests=Array.isArray(rawQuests.completedQuests) ? rawQuests.completedQuests : [];
  migrated.quests.activeQuests=Array.isArray(rawQuests.activeQuests) ? rawQuests.activeQuests : [];
  const rawWorld=incoming.world && typeof incoming.world==="object" ? incoming.world : {};
  migrated.world.triggeredEvents=Array.isArray(rawWorld.triggeredEvents) ? rawWorld.triggeredEvents.filter((name)=>typeof name==="string") : [];
  migrated.world.stateChanges.pondAwakened=Boolean(rawWorld.stateChanges?.pondAwakened);
  migrated.world.persistentObjects=normalizePersistentObjects(rawWorld.persistentObjects);
  migrated.world.mirrorCave.chestDiscovered=Boolean(rawWorld.mirrorCave?.chestDiscovered || migrated.world.persistentObjects?.mirror_cave_chest?.discovered);
  migrated.world.mirrorCave.chestOpened=Boolean(rawWorld.mirrorCave?.chestOpened || migrated.world.persistentObjects?.mirror_cave_chest?.opened);
  migrated.world.mirrorCave.cleared=Boolean(rawWorld.mirrorCave?.cleared);
  const rookDefeated=Boolean(rawWorld.tollhouse?.rookTollkeeperDefeated || migrated.world.persistentObjects?.rook_tollkeeper_state?.defeated);
  const tollhouseChestOpened=Boolean(rawWorld.tollhouse?.chestState==="open" || migrated.world.persistentObjects?.tollhouse_chest?.opened);
  migrated.world.tollhouse.abandonedTollhouseDiscovered=Boolean(
    rawWorld.tollhouse?.abandonedTollhouseDiscovered ||
    migrated.world.persistentObjects?.abandoned_tollhouse_state?.discovered ||
    migrated.player.zoneId==="abandoned_tollhouse" ||
    rookDefeated ||
    tollhouseChestOpened
  );
  migrated.world.tollhouse.rookTollkeeperDefeated=rookDefeated;
  migrated.world.tollhouse.chestState=tollhouseChestOpened ? "open" : (rookDefeated ? "closed" : "sealed");
  migrated.world.tollhouse.abandonedTollhouseCleared=Boolean(
    rawWorld.tollhouse?.abandonedTollhouseCleared ||
    migrated.world.persistentObjects?.abandoned_tollhouse_state?.cleared ||
    (rookDefeated && tollhouseChestOpened)
  );
  migrated.world.hunterQuest.hunterQuestStage=typeof rawWorld.hunterQuest?.hunterQuestStage==="string" ? rawWorld.hunterQuest.hunterQuestStage : HunterQuestStage.NOT_STARTED;
  migrated.world.hunterQuest.hunterQuestRewardClaimed=Boolean(rawWorld.hunterQuest?.hunterQuestRewardClaimed);
  migrated.world.creatures.wolves=Array.isArray(rawWorld.creatures?.wolves) ? rawWorld.creatures.wolves : [];
  migrated.world.creatures.bandits=Array.isArray(rawWorld.creatures?.bandits) ? rawWorld.creatures.bandits : [];
  migrated.world.creatures.tollhouseBandits=Array.isArray(rawWorld.creatures?.tollhouseBandits) ? rawWorld.creatures.tollhouseBandits : [];
  migrated.world.creatures.mirrorCaveWolves=Array.isArray(rawWorld.creatures?.mirrorCaveWolves) ? rawWorld.creatures.mirrorCaveWolves : [];
  migrated.world.creatures.rookTollkeeper={
    hp:Number.isFinite(rawWorld.creatures?.rookTollkeeper?.hp) ? rawWorld.creatures.rookTollkeeper.hp : base.world.creatures.rookTollkeeper.hp,
    defeated:Boolean(rawWorld.creatures?.rookTollkeeper?.defeated || rookDefeated)
  };
  const rawSystems=incoming.systems && typeof incoming.systems==="object" ? incoming.systems : {};
  migrated.systems.currentObjective=typeof rawSystems.currentObjective==="string" ? rawSystems.currentObjective : base.systems.currentObjective;
  migrated.systems.discoveredLocations=Array.isArray(rawSystems.discoveredLocations) ? rawSystems.discoveredLocations : [migrated.player.zoneId];
  migrated.systems.devMode=Boolean(rawSystems.devMode);
  migrated.saveSchemaVersion=SAVE_SCHEMA_VERSION;
  return migrated;
}
function repairSave(save){
  const repaired=cloneValue(save);
  let changed=false;
  const warnings=[];
  const zoneId=typeof repaired.player?.zoneId==="string" ? repaired.player.zoneId : "hearthvale_square";
  const isMirror=zoneId==="mirror_cave";
  const isTollhouse=zoneId==="abandoned_tollhouse";
  const maxX=(isMirror ? mirrorCave.width : (isTollhouse ? abandonedTollhouse.width : WORLD_W)) - 1;
  const maxY=(isMirror ? mirrorCave.height : (isTollhouse ? abandonedTollhouse.height : WORLD_H)) - 1;
  const clampedX=Math.max(0, Math.min(maxX, Math.floor(Number.isFinite(repaired.player.position?.x) ? repaired.player.position.x : 18)));
  const clampedY=Math.max(0, Math.min(maxY, Math.floor(Number.isFinite(repaired.player.position?.y) ? repaired.player.position.y : 11)));
  if(clampedX!==repaired.player.position.x || clampedY!==repaired.player.position.y){
    repaired.player.position={ x:clampedX, y:clampedY };
    changed=true;
    warnings.push("Player position was out of bounds and has been clamped.");
  }
  const xpResolvedLevel=getLevelFromXp(repaired.player.xp);
  const safeLevel=Math.max(xpResolvedLevel, Math.min(MAX_DEFINED_LEVEL, Math.floor(Number.isFinite(repaired.player.level) ? repaired.player.level : xpResolvedLevel)));
  if(safeLevel!==repaired.player.level){
    repaired.player.level=safeLevel;
    changed=true;
    warnings.push("Player level did not match XP and was repaired.");
  }
  repaired.player.maxHp=Math.max(1, Math.floor(Number.isFinite(repaired.player.maxHp) ? repaired.player.maxHp : BALANCE.player.startingMaxHp));
  const clampedHp=Math.max(0, Math.min(repaired.player.maxHp, Math.floor(Number.isFinite(repaired.player.hp) ? repaired.player.hp : repaired.player.maxHp)));
  if(clampedHp!==repaired.player.hp){
    repaired.player.hp=clampedHp;
    changed=true;
    warnings.push("Player HP was out of bounds and has been clamped.");
  }
  repaired.player.inventory=normalizeInventory(repaired.player.inventory);
  repaired.player.equipment={
    weapon:typeof repaired.player.equipment?.weapon==="string" ? repaired.player.equipment.weapon : "rusty_sword",
    armor:typeof repaired.player.equipment?.armor==="string" ? repaired.player.equipment.armor : null,
    trinket:typeof repaired.player.equipment?.trinket==="string" ? repaired.player.equipment.trinket : null
  };
  ["weapon","armor","trinket"].forEach((slotName)=>{
    const itemId=repaired.player.equipment[slotName];
    if(!itemId) return;
    const definition=getItemDefinition(itemId);
    if(!definition){
      repaired.player.equipment[slotName]=slotName==="weapon" ? "rusty_sword" : null;
      changed=true;
      warnings.push("Invalid equipped " + slotName + " was repaired.");
      return;
    }
    if(!repaired.player.inventory.some((entry)=>entry.itemId===itemId)){
      repaired.player.inventory.push({ itemId, quantity:1 });
      changed=true;
      warnings.push("Missing equipped " + slotName + " was restored to inventory.");
    }
  });
  repaired.world.persistentObjects=normalizePersistentObjects(repaired.world?.persistentObjects);
  if(repaired.world?.tollhouse?.rookTollkeeperDefeated && repaired.world?.tollhouse?.chestState!=="open" && repaired.world?.tollhouse?.abandonedTollhouseCleared){
    repaired.world.tollhouse.chestState="closed";
    changed=true;
  }
  if(Array.isArray(repaired.quests?.questStates)){
    repaired.quests.questStates=repaired.quests.questStates.map((questEntry)=>{
      if(questEntry?.state!==QuestState.COMPLETED || !Array.isArray(questEntry.objectives)) return questEntry;
      return {
        ...questEntry,
        objectives:questEntry.objectives.map((objective)=>({
          ...objective,
          completed:true
        }))
      };
    });
  }
  return { save:repaired, changed, warnings };
}
function createSaveData(reason){
  updateOutdoorRegionFromPosition(false);
  syncMirrorCaveChestState(false);
  syncTollhouseChestState(false);
  syncAbandonedTollhouseClearedState(false, false);
  syncEchoFragmentState(false);
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
  const tollhouseBanditsSave=tollhouseBandits.map((bandit)=>({
    id:bandit.id,
    hp:bandit.hp,
    defeated:bandit.defeated,
    respawnRemainingMs:Math.max(0, banditRespawnAtById[bandit.id] ? banditRespawnAtById[bandit.id]-performance.now() : 0)
  }));
  return {
    version:13,
    saveSchemaVersion:SAVE_SCHEMA_VERSION,
    reason,
    savedAt:new Date().toISOString(),
    player:{
      zoneId:currentZoneId,
      position:{ x:player.targetX, y:player.targetY },
      level:player.level,
      hp:player.hp,
      maxHp:player.maxHp,
      xp:player.xp,
      baseAttackBonus:player.baseAttackBonus,
      baseDefenseBonus:player.baseDefenseBonus,
      coins:player.coins,
      skills:{
        swordsmanship:{ ...player.skills.swordsmanship },
        defense:{ ...player.skills.defense },
        survival:{ ...player.skills.survival }
      },
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
      persistentObjects:normalizePersistentObjects(persistentObjects),
      mirrorCave:{
        chestDiscovered:mirrorCaveChestDiscovered,
        chestOpened:mirrorCave.chest.opened,
        cleared:mirrorCave.cleared
      },
      tollhouse:{
        abandonedTollhouseDiscovered:abandonedTollhouseDiscovered,
        rookTollkeeperDefeated:rookTollkeeperDefeated,
        chestState:getTollhouseChestState(),
        abandonedTollhouseCleared:abandonedTollhouseCleared
      },
      hunterQuest:{
        hunterQuestStage:getHunterQuestStage(),
        hunterQuestRewardClaimed:hunterQuestRewardClaimed
      },
      creatures:{
        wolves:wolvesSave,
        bandits:banditsSave,
        tollhouseBandits:tollhouseBanditsSave,
        rookTollkeeper:{
          hp:rookTollkeeper.hp,
          defeated:rookTollkeeperDefeated || rookTollkeeper.defeated
        },
        mirrorCaveWolves:mirrorCaveWolves.map((wolf)=>({
          id:wolf.id,
          hp:wolf.hp,
          defeated:wolf.defeated,
          respawnRemainingMs:Math.max(0, wolfRespawnAtById[wolf.id] ? wolfRespawnAtById[wolf.id]-performance.now() : 0)
        }))
      }
    },
    systems:{
      currentObjective:getContextualObjectiveText(),
      discoveredLocations:[currentZoneId],
      devMode:DEV_MODE
    }
  };
}
function validateSaveData(data){
  if(!data || typeof data!=="object") return false;
  if(data.version!==undefined && !SUPPORTED_SAVE_VERSIONS.has(data.version)) return false;
  const px=data.player?.position?.x, py=data.player?.position?.y;
  if(!Number.isInteger(px) || !Number.isInteger(py)) return false;
  if(!isFiniteNumber(data.player?.hp) || !isFiniteNumber(data.player?.xp) || !isFiniteNumber(data.player?.coins)) return false;
  return true;
}
function saveGame(reason){
  try {
    const payload=createSaveData(reason);
    const existingRaw=localStorage.getItem(SAVE_KEY);
    if(existingRaw) localStorage.setItem(SAVE_BACKUP_KEY, existingRaw);
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
    let parsed;
    try {
      parsed=JSON.parse(raw);
    } catch(parseError){
      localStorage.setItem(SAVE_BACKUP_KEY, raw);
      throw parseError;
    }
    const migrated=migrateSave(parsed);
    const repaired=repairSave(migrated);
    const data=repaired.save;
    if(!validateSaveData(data)) throw new Error("Invalid save payload");
    if(repaired.changed){
      repaired.warnings.forEach((message)=>console.warn("[Save Repair] " + message));
    }
    if(parsed.saveSchemaVersion!==SAVE_SCHEMA_VERSION || repaired.changed){
      localStorage.setItem(SAVE_BACKUP_KEY, raw);
      localStorage.setItem(SAVE_KEY, JSON.stringify(data));
      log("System: Save migrated to schema v" + String(SAVE_SCHEMA_VERSION) + ".");
    }
    const saveSchemaVersion=Number.isInteger(parsed.saveSchemaVersion) ? parsed.saveSchemaVersion : 0;
    if(saveSchemaVersion>SAVE_SCHEMA_VERSION) log("System: Save schema is newer than this build. Attempting safe load.");
    const savedZoneId=typeof data.player.zoneId==="string" ? data.player.zoneId : getOutdoorRegionIdAt(data.player.position.x, data.player.position.y);
    isInMirrorCave=savedZoneId==="mirror_cave";
    isInAbandonedTollhouse=savedZoneId==="abandoned_tollhouse";
    const mapW=isInMirrorCave ? mirrorCave.width : (isInAbandonedTollhouse ? abandonedTollhouse.width : WORLD_W);
    const mapH=isInMirrorCave ? mirrorCave.height : (isInAbandonedTollhouse ? abandonedTollhouse.height : WORLD_H);
    const loadedX=Math.max(0,Math.min(mapW-1,data.player.position.x));
    const loadedY=Math.max(0,Math.min(mapH-1,data.player.position.y));
    setPlayerTilePosition(loadedX, loadedY);
    zoneTransitionLockedUntil=0;
    blockedDirectionalKeysUntilRelease.clear();
    currentZoneId=isInMirrorCave ? "mirror_cave" : (isInAbandonedTollhouse ? "abandoned_tollhouse" : getOutdoorRegionIdAt(loadedX, loadedY));
    lastLoggedZoneEntryId=currentZoneId;
    player.xp=Math.max(0,Math.floor(Number.isFinite(data.player.xp) ? data.player.xp : 0));
    const xpResolvedLevel=getLevelFromXp(player.xp);
    const hasSavedLevel=Number.isFinite(data.player.level);
    const savedLevel=hasSavedLevel ? Math.max(1,Math.floor(data.player.level)) : xpResolvedLevel;
    const targetLevel=Math.max(xpResolvedLevel, Math.min(MAX_DEFINED_LEVEL, savedLevel));
    const targetProfile=getLevelProfile(targetLevel);
    player.level=targetLevel;
    player.maxHp=Math.max(targetProfile.maxHp, Math.floor(Number.isFinite(data.player.maxHp) ? data.player.maxHp : targetProfile.maxHp));
    player.baseAttackBonus=Math.max(targetProfile.baseAttackBonus, Math.floor(Number.isFinite(data.player.baseAttackBonus) ? data.player.baseAttackBonus : targetProfile.baseAttackBonus));
    player.baseDefenseBonus=Math.max(targetProfile.baseDefenseBonus, Math.floor(Number.isFinite(data.player.baseDefenseBonus) ? data.player.baseDefenseBonus : targetProfile.baseDefenseBonus));
    player.hp=Math.max(0,Math.min(player.maxHp,Math.floor(Number.isFinite(data.player.hp) ? data.player.hp : player.maxHp)));
    player.coins=Math.max(0,Math.floor(Number.isFinite(data.player.coins) ? data.player.coins : 0));
    player.skills=normalizeSkills(data.player.skills);
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
    Object.keys(persistentObjects).forEach((objectId)=>{ delete persistentObjects[objectId]; });
    if(data.world?.persistentObjects && typeof data.world.persistentObjects==="object"){
      Object.entries(data.world.persistentObjects).forEach(([objectId, objectState])=>{
        if(!objectState || typeof objectState!=="object") return;
        persistentObjects[objectId]={ ...objectState };
      });
    }
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
    tollhouseBandits.forEach((bandit)=>{
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
    rookTollkeeper.hp=rookTollkeeper.maxHp;
    rookTollkeeper.defeated=false;
    rookTollkeeper.targetX=rookTollkeeper.homeX;
    rookTollkeeper.targetY=rookTollkeeper.homeY;
    rookTollkeeper.px=rookTollkeeper.targetX*TILE;
    rookTollkeeper.py=rookTollkeeper.targetY*TILE;
    banditRespawnAtById[rookTollkeeper.id]=0;
    rookTollkeeperDefeated=false;
    abandonedTollhouseDiscovered=false;
    abandonedTollhouseCleared=false;
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
    const savedTollhouseBandits=Array.isArray(data.world?.creatures?.tollhouseBandits) ? data.world.creatures.tollhouseBandits : null;
    if(savedTollhouseBandits){
      savedTollhouseBandits.forEach((savedBandit)=>{
        if(!savedBandit || typeof savedBandit!=="object") return;
        const bandit=tollhouseBandits.find((candidate)=>candidate.id===savedBandit.id);
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
    const mirrorCaveChestState=persistentObjects?.mirror_cave_chest || {};
    const tollhouseChestState=persistentObjects?.tollhouse_chest || persistentObjects?.tollhouse_reward_chest || {};
    const echoFragmentState=persistentObjects?.echo_fragment_object || persistentObjects?.echo_fragment || {};
    mirrorCaveChestDiscovered=Boolean(data.world?.mirrorCave?.chestDiscovered || mirrorCaveChestState.discovered);
    mirrorCave.chest.opened=Boolean(data.world?.mirrorCave?.chestOpened || mirrorCaveChestState.opened);
    mirrorCave.cleared=Boolean(data.world?.mirrorCave?.cleared);
    abandonedTollhouseDiscovered=Boolean(
      data.world?.tollhouse?.abandonedTollhouseDiscovered ||
      persistentObjects?.abandoned_tollhouse_state?.discovered ||
      savedZoneId==="abandoned_tollhouse" ||
      data.world?.tollhouse?.rookTollkeeperDefeated ||
      tollhouseChestState.opened
    );
    rookTollkeeperDefeated=Boolean(data.world?.tollhouse?.rookTollkeeperDefeated || persistentObjects?.rook_tollkeeper_state?.defeated);
    abandonedTollhouseCleared=Boolean(data.world?.tollhouse?.abandonedTollhouseCleared || persistentObjects?.abandoned_tollhouse_state?.cleared);
    rookTollkeeper.defeated=rookTollkeeperDefeated;
    if(rookTollkeeperDefeated) rookTollkeeper.hp=0;
    hunterQuestRewardClaimed=Boolean(data.world?.hunterQuest?.hunterQuestRewardClaimed);
    const hunterQuest=questSystem.getQuest("hunters_request");
    if(hunterQuest?.state===QuestState.COMPLETED){
      setHunterQuestStage(HunterQuestStage.COMPLETED);
      mirrorCave.chest.opened=true;
      hunterQuestRewardClaimed=true;
    } else if(hunterQuest){
      const savedStage=data.world?.hunterQuest?.hunterQuestStage;
      if(typeof savedStage==="string" && Object.values(HunterQuestStage).includes(savedStage) && savedStage!==HunterQuestStage.NOT_STARTED){
        setHunterQuestStage(savedStage);
      } else if(mirrorCave.chest.opened || getItemQuantity("mirror_relic")>0){
        if(getItemQuantity("mirror_relic")<=0) addItemToInventory("mirror_relic", 1);
        questSystem.completeObjective("hunters_request", "enter_cave");
        questSystem.completeObjective("hunters_request", "open_chest");
        setHunterQuestStage(HunterQuestStage.STAGE_4_RETURN_WITH_RELIC);
      } else if(hunterQuest.state!==QuestState.NOT_STARTED){
        setHunterQuestStage(HunterQuestStage.STAGE_1_PROVE_YOURSELF);
        updateHunterStageOneReadiness();
      }
    }
    syncMirrorCaveChestState(false);
    syncTollhouseChestState(false);
    syncAbandonedTollhouseClearedState(false, false);
    if(echoFragmentState.collected && getItemQuantity("echo_fragment")<=0) addItemToInventory("echo_fragment", 1);
    syncEchoFragmentState(false);
    migrateStillWaterStateFromSave();
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
eventSystem.on("quest:completed:the_still_water", ()=>saveGame("quest_complete"));
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
registerWorldObject({
  objectId:"town_well",
  type:WORLD_OBJECT_TYPE.DECORATION,
  zone:"overworld",
  x:18, y:12,
  state:"default",
  interactable:true,
  collision:false,
  persistence:false,
  promptLabel:"Inspect well",
  onInteract:()=>{ log("The well water is cold and perfectly still."); eventSystem.emit("object:used:well",{}); }
});
registerWorldObject({
  objectId:"north_road_notice",
  type:WORLD_OBJECT_TYPE.SIGN,
  zone:"overworld",
  x:26, y:11,
  state:"unread",
  interactable:true,
  collision:true,
  persistence:true,
  promptLabel:"Read sign",
  onInteract:()=>{
    patchPersistentObject("north_road_notice", { state:"read", read:true });
    openWorldInfoPanel("Signpost", "East Road — Eastern Woods");
  }
});
registerWorldObject({
  objectId:"north_road_sign",
  type:WORLD_OBJECT_TYPE.SIGN,
  zone:"overworld",
  x:16, y:4,
  state:"unread",
  interactable:true,
  collision:true,
  persistence:true,
  promptLabel:"Read sign",
  onInteract:()=>{
    patchPersistentObject("north_road_sign", { state:"read", read:true });
    openWorldInfoPanel("Signpost", "North Road — Old stones, older paths.");
  }
});
registerWorldObject({
  objectId:"north_road_crate",
  type:WORLD_OBJECT_TYPE.CHEST,
  zone:"overworld",
  region:"north_road",
  x:22, y:1,
  state:"closed",
  interactable:true,
  collision:true,
  persistence:true,
  promptLabel:()=>{
    const persistent=getPersistentObject("north_road_crate");
    return persistent.opened ? "Inspect crate" : "Open roadside crate";
  },
  onInteract:()=>{
    const persistent=getPersistentObject("north_road_crate");
    if(persistent.opened){
      log("The roadside crate hangs open and empty.");
      return;
    }
    patchPersistentObject("north_road_crate", { state:"open", opened:true }, false);
    addItemToInventory("small_potion", 1);
    log("You found a Small Potion in the roadside crate.");
    saveGame("object_state_change");
  }
});
registerWorldObject({
  objectId:"mirror_pond_sign",
  type:WORLD_OBJECT_TYPE.SIGN,
  zone:"overworld",
  x:26, y:11,
  state:"unread",
  interactable:true,
  collision:true,
  persistence:true,
  promptLabel:"Read sign",
  onInteract:()=>{
    patchPersistentObject("mirror_pond_sign", { state:"read", read:true });
    openWorldInfoPanel("Signpost", "Mirror Pond — Still water, old stories.");
  }
});
registerWorldObject({
  objectId:"mirror_pond",
  type:WORLD_OBJECT_TYPE.DECORATION,
  zone:"overworld",
  x:27, y:14,
  state:"still",
  interactable:true,
  collision:false,
  persistence:true,
  promptLabel:()=>{
    const stage=getStillWaterQuestStage();
    return stage===StillWaterQuestStage.STAGE_2_INSPECT_MIRROR_POND ? "Inspect Mirror Pond" : "Inspect still water";
  },
  onInteract:()=>{
    const stage=getStillWaterQuestStage();
    if(stage===StillWaterQuestStage.STAGE_2_INSPECT_MIRROR_POND){
      log("For a moment, your reflection moves half a breath late.");
      log("Mirror Pond stirs beneath your reflection.");
      patchPersistentObject("mirror_pond", { inspected:true, state:"inspected" }, false);
      questSystem.completeObjective("the_still_water", "inspect_pond");
      setStillWaterQuestStage(StillWaterQuestStage.STAGE_3_RETURN_TO_EDRIN);
      eventSystem.emit("object:used:mirror_pond",{ stage });
      saveGame("object_state_change");
      return;
    }
    if(stage===StillWaterQuestStage.NOT_STARTED || stage===StillWaterQuestStage.STAGE_1_SPEAK_WITH_EDRIN){
      log("The water is still.");
      return;
    }
    if(stage===StillWaterQuestStage.STAGE_3_RETURN_TO_EDRIN || stage===StillWaterQuestStage.STAGE_4_ENTER_MIRROR_CAVE || stage===StillWaterQuestStage.STAGE_5_RECOVER_ECHO_FRAGMENT || stage===StillWaterQuestStage.STAGE_6_RETURN_TO_EDRIN || stage===StillWaterQuestStage.COMPLETED){
      log("The pond is still again, but not empty.");
      return;
    }
    log("The water is still.");
  }
});
registerWorldObject({
  objectId:"mirror_cave_sign",
  type:WORLD_OBJECT_TYPE.SIGN,
  zone:"overworld",
  x:31, y:12,
  state:"unread",
  interactable:true,
  collision:true,
  persistence:true,
  promptLabel:"Read sign",
  onInteract:()=>{
    patchPersistentObject("mirror_cave_sign", { state:"read", read:true });
    openWorldInfoPanel("Signpost", "Mirror Cave");
  }
});
registerWorldObject({
  objectId:"mirror_cave_entrance",
  type:WORLD_OBJECT_TYPE.CAVE_ENTRANCE,
  zone:"overworld",
  region:"eastern_woods",
  x:OVERWORLD_CAVE_ENTRY.x, y:OVERWORLD_CAVE_ENTRY.y,
  state:"active",
  interactable:true,
  collision:false,
  persistence:false,
  walkInTrigger:true,
  promptLabel:"Enter Mirror Cave",
  onInteract:()=>enterMirrorCave()
});
registerWorldObject({
  objectId:"tollhouse_warning_sign",
  type:WORLD_OBJECT_TYPE.SIGN,
  zone:"overworld",
  region:"north_road",
  x:21, y:2,
  state:"unread",
  interactable:true,
  collision:true,
  persistence:true,
  promptLabel:"Read notice",
  onInteract:()=>{
    patchPersistentObject("tollhouse_warning_sign", { state:"read", read:true });
    openWorldInfoPanel("Weathered Notice", "Old Toll Road — Closed by order of Hearthvale.");
  }
});
registerWorldObject({
  objectId:"abandoned_tollhouse_entrance",
  type:WORLD_OBJECT_TYPE.DOOR,
  zone:"overworld",
  region:"north_road",
  x:NORTH_ROAD_TOLLHOUSE_ENTRY.x, y:NORTH_ROAD_TOLLHOUSE_ENTRY.y,
  state:"active",
  interactable:true,
  collision:false,
  persistence:false,
  walkInTrigger:true,
  promptLabel:"Enter Abandoned Tollhouse",
  onInteract:()=>enterAbandonedTollhouse()
});
registerWorldObject({
  objectId:"mirror_cave_exit",
  type:WORLD_OBJECT_TYPE.DUNGEON_EXIT,
  zone:"mirror_cave",
  dungeon:"mirror_cave",
  x:mirrorCave.exit.x, y:mirrorCave.exit.y,
  state:"active",
  interactable:true,
  collision:false,
  persistence:false,
  walkInTrigger:true,
  promptLabel:"Exit Mirror Cave",
  onInteract:()=>exitMirrorCave()
});
registerWorldObject({
  objectId:"abandoned_tollhouse_exit",
  type:WORLD_OBJECT_TYPE.DUNGEON_EXIT,
  zone:"abandoned_tollhouse",
  dungeon:"abandoned_tollhouse",
  x:abandonedTollhouse.exit.x, y:abandonedTollhouse.exit.y,
  state:"active",
  interactable:true,
  collision:false,
  persistence:false,
  walkInTrigger:true,
  promptLabel:"Exit Abandoned Tollhouse",
  onInteract:()=>exitAbandonedTollhouse()
});
registerWorldObject({
  objectId:"mirror_cave_chest",
  type:WORLD_OBJECT_TYPE.CHEST,
  zone:"mirror_cave",
  dungeon:"mirror_cave",
  x:mirrorCave.chest.x, y:mirrorCave.chest.y,
  state:"sealed",
  interactable:true,
  collision:true,
  requiredQuestStage:HunterQuestStage.STAGE_3_MIRROR_CAVE,
  persistence:true,
  promptLabel:"Open chest",
  onInteract:()=>{
    const state=syncMirrorCaveChestState(false);
    if(state==="open"){
      log("The chest is empty.");
      return;
    }
    if(state==="sealed"){
      mirrorCaveChestDiscovered=true;
      patchPersistentObject("mirror_cave_chest", { discovered:true }, false);
      log("The chest is sealed.");
      saveGame("object_state_change");
      return;
    }
    mirrorCave.chest.opened=true;
    mirrorCave.cleared=true;
    patchPersistentObject("mirror_cave_chest", { state:"open", opened:true }, false);
    if(getItemQuantity("mirror_relic")<=0) addItemToInventory("mirror_relic", 1);
    log("You recovered the Mirror Relic.");
    showRewardToast("+ Mirror Relic", 1800);
    eventSystem.emit("object:opened:mirror_cave_chest");
    saveGame("object_state_change");
  }
});
registerWorldObject({
  objectId:"echo_fragment_object",
  type:WORLD_OBJECT_TYPE.DECORATION,
  zone:"mirror_cave",
  dungeon:"mirror_cave",
  x:12, y:5,
  state:"inert",
  interactable:true,
  collision:false,
  persistence:true,
  promptLabel:"Take Echo Fragment",
  onInteract:()=>{
    const persistent=getPersistentObject("echo_fragment_object");
    const stage=getStillWaterQuestStage();
    if(persistent.collected || getItemQuantity("echo_fragment")>0){
      syncEchoFragmentState(false);
      log("Only a faint chill remains where the fragment rested.");
      saveGame("object_state_change");
      return;
    }
    if(stage!==StillWaterQuestStage.STAGE_5_RECOVER_ECHO_FRAGMENT){
      log("A pale shard rests in silence, as if waiting.");
      return;
    }
    if(getItemQuantity("echo_fragment")<=0) addItemToInventory("echo_fragment", 1);
    patchPersistentObject("echo_fragment_object", { state:"collected", collected:true }, false);
    log("You recovered the Echo Fragment.");
    showRewardToast("+ Echo Fragment", 1800);
    eventSystem.emit("object:collected:echo_fragment");
    saveGame("object_state_change");
  }
});
registerWorldObject({
  objectId:"tollhouse_chest",
  type:WORLD_OBJECT_TYPE.CHEST,
  zone:"abandoned_tollhouse",
  dungeon:"abandoned_tollhouse",
  x:abandonedTollhouse.chest.x, y:abandonedTollhouse.chest.y,
  state:"locked",
  interactable:true,
  collision:true,
  persistence:true,
  promptLabel:"Open tollhouse chest",
  onInteract:()=>{
    const state=syncTollhouseChestState(false);
    if(state==="locked"){
      log("The tollhouse chest is locked.");
      showRewardToast("Chest locked — defeat Rook", 1200);
      return;
    }
    if(state==="open"){
      log("The tollhouse chest is empty.");
      return;
    }
    patchPersistentObject("tollhouse_chest", { state:"open", opened:true }, false);
    const rewardResult=grantTollhouseChestRewards();
    if(!rewardResult.rewardsGranted.length){
      log("The tollhouse chest is empty.");
    } else {
      log("Opened the tollhouse chest.");
      log("Loot acquired:");
      rewardResult.rewardsGranted.forEach((entry)=>log("- " + entry));
      showRewardToast("Tollhouse chest opened", 1300);
      showRewardToasts(rewardResult.rewardToasts);
    }
    syncTollhouseChestState(false);
    syncAbandonedTollhouseClearedState(false, true);
    maybeAnnounceVerticalSliceEndpoint();
    saveGame("object_state_change");
  }
});
worldObjects
  .filter((object)=>object.interactable)
  .forEach((object)=>{
    interactionManager.register({
      id:object.objectId,
      type:object.type,
      x:()=>isWorldObjectInCurrentZone(object) ? getWorldObjectTile(object).x : -999,
      y:()=>isWorldObjectInCurrentZone(object) ? getWorldObjectTile(object).y : -999,
      range:object.objectId==="mirror_pond" ? 3 : undefined,
      promptLabel:object.promptLabel || "Interact",
      onInteract:()=>object.onInteract?.()
    });
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
dialogueActions.addEventListener("click",(event)=>{
  const target=event.target instanceof Element ? event.target.closest("button") : null;
  if(!target) return;
  event.preventDefault();
  event.stopPropagation();
  if(target.hasAttribute("data-world-info-close")){ closeWorldInfoPanel(); return; }
  if(target.hasAttribute("data-dialogue-close")){ dialogueSystem.close(); return; }
  if(target.hasAttribute("data-dialogue-advance")) dialogueSystem.advance();
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
  const width=isInMirrorCave ? mirrorCave.width : (isInAbandonedTollhouse ? abandonedTollhouse.width : WORLD_W);
  const height=isInMirrorCave ? mirrorCave.height : (isInAbandonedTollhouse ? abandonedTollhouse.height : WORLD_H);
  return x>=0 && y>=0 && x<width && y<height;
}

function isInTransitionSafeBuffer(zoneId,x,y){
  return false;
}

function isEasternWoodsActive(){
  return !isInMirrorCave && !isInAbandonedTollhouse;
}

function findZoneTransitionAt(){ return null; }

function getActiveHostiles(){
  if(isInMirrorCave) return mirrorCaveWolves;
  if(isInAbandonedTollhouse) return rookTollkeeperDefeated ? tollhouseBandits : [...tollhouseBandits, rookTollkeeper];
  return [...wolves, ...bandits];
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
    isInAbandonedTollhouse=false;
    isInMirrorCave=true;
    currentZoneId="mirror_cave";
    setPlayerTilePosition(mirrorCave.spawn.x, mirrorCave.spawn.y);
    lastLoggedZoneEntryId=currentZoneId;
    logThrottled("transition:entered_mirror_cave", "Entered Mirror Cave.", 1200);
    eventSystem.emit("zone:entered:mirror_cave");
  }, 320);
}
function enterAbandonedTollhouse(){
  runHardTransition(()=>{
    isInMirrorCave=false;
    isInAbandonedTollhouse=true;
    currentZoneId="abandoned_tollhouse";
    setPlayerTilePosition(abandonedTollhouse.spawn.x, abandonedTollhouse.spawn.y);
    lastLoggedZoneEntryId=currentZoneId;
    rookEncounterAnnounced=false;
    hostileAggroBlockedUntil=performance.now()+900;
    markAbandonedTollhouseDiscovered(true, true);
    logThrottled("transition:entered_abandoned_tollhouse", "Entered Abandoned Tollhouse.", 1200);
  }, 320);
}

function exitMirrorCave(){
  runHardTransition(()=>{
    isInMirrorCave=false;
    isInAbandonedTollhouse=false;
    currentZoneId="eastern_woods";
    setPlayerTilePosition(mirrorCave.returnTile.x, mirrorCave.returnTile.y);
    lastLoggedZoneEntryId=currentZoneId;
    logThrottled("transition:exit_mirror_cave", "Returned to Eastern Woods.", 1200);
  }, 320);
}
function exitAbandonedTollhouse(){
  runHardTransition(()=>{
    isInAbandonedTollhouse=false;
    isInMirrorCave=false;
    currentZoneId="north_road";
    setPlayerTilePosition(abandonedTollhouse.returnTile.x, abandonedTollhouse.returnTile.y);
    lastLoggedZoneEntryId=currentZoneId;
    logThrottled("transition:exit_abandoned_tollhouse", "Returned to North Road.", 1200);
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
function triggerWalkInWorldObject(){
  if(transitionState.active || performance.now()<zoneTransitionLockedUntil) return false;
  return getActiveWorldObjects().some((object)=>{
    if(!object.walkInTrigger || !object.interactable) return false;
    const tile=getWorldObjectTile(object);
    if(tile.x!==player.targetX || tile.y!==player.targetY) return false;
    object.onInteract?.();
    eventSystem.emit("interaction:used",{id:object.objectId,type:object.type});
    return true;
  });
}

function getOutdoorRegionIdAt(x,y){
  for(const region of Object.values(OUTDOOR_REGION_DEFS)){
    if(isWithinRect(x,y,region.bounds)) return region.id;
  }
  return "hearthvale_square";
}

function updateOutdoorRegionFromPosition(logEntry){
  if(isInMirrorCave || isInAbandonedTollhouse) return;
  const nextZoneId=getOutdoorRegionIdAt(player.targetX, player.targetY);
  if(nextZoneId===currentZoneId) return;
  currentZoneId=nextZoneId;
  if(logEntry && currentZoneId!=="north_road" && lastLoggedZoneEntryId!==currentZoneId){
    logThrottled("zone_entry:" + currentZoneId, "Entered " + getCurrentZoneName() + ".", 1200);
    lastLoggedZoneEntryId=currentZoneId;
  } else if(currentZoneId==="north_road"){
    lastLoggedZoneEntryId=currentZoneId;
  }
}

function currentLocalAreaName(){
  if(isInMirrorCave) return "Mirror Cave";
  if(isInAbandonedTollhouse) return "Abandoned Tollhouse";
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
  if(hostile.displayName) return hostile.displayName;
  if(hostile.kind==="bandit") return "Bandit #" + hostile.id;
  if(hostile.enemyType==="cave_wolf") return "Cave Wolf #" + hostile.id;
  return "Wolf #" + hostile.id;
}

function getHostileAttackCooldownMs(hostile){
  if(!hostile) return 0;
  return getEnemyConfig(hostile.enemyType || hostile.kind).attackCooldownMs;
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
function getCurrentCombatTarget(range=4){
  const nearest=getNearestHostile(range);
  return nearest?.entity || null;
}

function respawnPlayerAtSquare(){
  isInMirrorCave=false;
  isInAbandonedTollhouse=false;
  currentZoneId="hearthvale_square";
  setPlayerTilePosition(18, 11);
  zoneTransitionLockedUntil=0;
  blockedDirectionalKeysUntilRelease.clear();
  lastLoggedZoneEntryId=currentZoneId;
}

function handlePlayerDefeat(){
  log("You fall in battle. You awaken at Hearthvale Square.");
  showRewardToast("Defeat — Returning to Hearthvale", 2200);
  player.hp=player.maxHp;
  hitStopUntil=performance.now()+220;
  hostileAggroBlockedUntil=performance.now()+BALANCE.death.respawnSafetyMs;
  respawnPlayerAtSquare();
  spawnFloatingText(player.px/TILE, player.py/TILE, "Recovered", { color:"#b9d3ff", durationMs:1200 });
}

let sidebarInventoryMarkup="";
let sidebarEquipmentMarkup="";
let sidebarSkillsMarkup="";
function updateSidebar(){
  levelVal.textContent = String(player.level);
  hpVal.textContent = player.hp + "/" + player.maxHp;
  xpVal.textContent = getXpProgressText();
  coinsVal.textContent = String(player.coins);
  const equippedWeapon=getEquippedItem("weapon");
  weaponVal.textContent = equippedWeapon ? (equippedWeapon.name + " (+" + getEquippedWeaponBonus() + ")") : "None";
  const equippedArmor=getEquippedItem("armor");
  const armorDefense=getArmorDefenseBonus();
  armorVal.textContent = equippedArmor ? (equippedArmor.name + " (+" + armorDefense + " DEF)") : "None";
  const equippedTrinket=getEquippedItem("trinket");
  const trinketDefense=getTrinketDefenseBonus();
  trinketVal.textContent = equippedTrinket ? (equippedTrinket.name + (trinketDefense>0 ? " (+" + trinketDefense + " DEF)" : "")) : "None";
  const zoneName=getCurrentZoneName();
  zoneVal.textContent = zoneName;
  const huntersQuest=questSystem.getQuest("hunters_request");
  const mirrorQuest=questSystem.getQuest("mirror_pond_listening");
  const stillWaterQuest=questSystem.getQuest("the_still_water");
  const activeQuest=(
    (stillWaterQuest?.state===QuestState.ACTIVE || stillWaterQuest?.state===QuestState.READY_TO_TURN_IN) ? stillWaterQuest :
    ((huntersQuest?.state===QuestState.ACTIVE || huntersQuest?.state===QuestState.READY_TO_TURN_IN) ? huntersQuest :
    ((mirrorQuest?.state===QuestState.ACTIVE) ? mirrorQuest :
    (stillWaterQuest?.state===QuestState.COMPLETED ? stillWaterQuest :
    (huntersQuest?.state===QuestState.COMPLETED ? huntersQuest : mirrorQuest))))
  );
  questVal.textContent = activeQuest ? (activeQuest.name + " [" + activeQuest.state + "]") : "Town Slice";
  if(stillWaterQuest?.state===QuestState.ACTIVE || stillWaterQuest?.state===QuestState.READY_TO_TURN_IN || stillWaterQuest?.state===QuestState.COMPLETED){
    objectiveText.textContent = getStillWaterObjectiveText();
  } else {
    const hunterStage=getHunterQuestStage();
    if(hunterStage===HunterQuestStage.STAGE_1_PROVE_YOURSELF){
      const wolves=Math.max(0, Math.min(3, questSystem.getObjective("hunters_request", "wolves")?.currentAmount || 0));
      const pelts=Math.max(0, Math.min(3, getItemQuantity("wolf_pelt")));
      objectiveText.textContent = "Hunter's Request\n- Defeat Wolves: " + wolves + "/3\n- Wolf Pelts: " + pelts + "/3";
    } else if(hunterStage===HunterQuestStage.STAGE_2_RETURN_TO_HUNTER){
      objectiveText.textContent = "Hunter's Request\n- Return to Hunter Garran";
    } else if(hunterStage===HunterQuestStage.STAGE_3_MIRROR_CAVE){
      objectiveText.textContent = "Hunter's Request\n- Enter Mirror Cave\n- Recover the Mirror Relic";
    } else if(hunterStage===HunterQuestStage.STAGE_4_RETURN_WITH_RELIC){
      objectiveText.textContent = "Hunter's Request\n- Return to Hunter Garran";
    } else if(hunterStage===HunterQuestStage.COMPLETED){
      objectiveText.textContent = getContextualObjectiveText();
    } else if(mirrorQuest?.state===QuestState.ACTIVE && mirrorQuest.progress==="go_to_pond"){
      objectiveText.textContent = "Go to Mirror Pond and listen carefully.";
    } else if(mirrorQuest?.state===QuestState.ACTIVE && mirrorQuest.progress==="heard_whispers"){
      objectiveText.textContent = "Return to Edrin Vale and report what you heard.";
    } else if(mirrorQuest?.state===QuestState.COMPLETED){
      objectiveText.textContent = getContextualObjectiveText();
    } else {
      objectiveText.textContent = getContextualObjectiveText();
    }
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
      const itemText="<span class=\"inventory-item-name\">" + name + " x" + entry.quantity + "</span>";
      if(canEquip){
        const actionMarkup=equipped
          ? "<span class=\"equipped-tag\">Equipped</span>"
          : "<button type=\"button\" class=\"inventory-btn\" data-equip-item=\"" + item.id + "\" data-equip-slot=\"" + equipSlot + "\">Equip</button>";
        return "<div class=\"inventory-row\">" + itemText + "<span class=\"inventory-actions\">" + actionMarkup + "</span></div>";
      }
      const canUse=Boolean(item && item.type==="consumable" && Number.isFinite(item.healAmount) && Math.floor(item.healAmount)>0);
      if(canUse){
        return "<div class=\"inventory-row\">" + itemText + "<span class=\"inventory-actions\"><button type=\"button\" class=\"inventory-btn\" data-use-item=\"" + item.id + "\">Use</button></span></div>";
      }
      const trinketEquipped=Boolean(item?.id && item.type==="trinket" && player.equipment.trinket===item.id);
      const trinketTag=trinketEquipped ? "<span class=\"inventory-actions\"><span class=\"equipped-tag\">Equipped</span></span>" : "";
      return "<div class=\"inventory-row\">" + itemText + trinketTag + "</div>";
    }).join("");
  }
  if(nextInventoryMarkup!==sidebarInventoryMarkup){
    inventoryList.innerHTML = nextInventoryMarkup;
    sidebarInventoryMarkup=nextInventoryMarkup;
  }
  // Do not re-render vendor rows every sidebar update; replacing DOM each frame
  // can swallow button clicks before click events complete.
  const weaponLine=equippedWeapon ? (equippedWeapon.name + " (+" + getEquippedWeaponBonus() + ")") : "None";
  const armorLine=equippedArmor ? (equippedArmor.name + " (+" + armorDefense + " DEF)") : "None";
  const trinketLine=equippedTrinket ? (equippedTrinket.name + (trinketDefense>0 ? " (+" + trinketDefense + " DEF)" : "")) : "None";
  const weaponButton=equippedWeapon && equippedWeapon.id!=="rusty_sword" ? " <button type=\"button\" class=\"inventory-btn\" data-unequip-slot=\"weapon\">Remove</button>" : "";
  const armorButton=equippedArmor ? " <button type=\"button\" class=\"inventory-btn\" data-unequip-slot=\"armor\">Remove</button>" : "";
  const trinketButton=equippedTrinket ? " <button type=\"button\" class=\"inventory-btn\" data-unequip-slot=\"trinket\">Remove</button>" : "";
  const totalAttack=getTotalAttackDamage();
  const totalDefense=getTotalDefenseRating();
  const maxHp=player.maxHp;
  const nextEquipmentMarkup=
    "<div class=\"equipment-slot\"><span class=\"equipment-slot-label\">Weapon:</span><span class=\"equipment-slot-value\">" + weaponLine + weaponButton + "</span></div>" +
    "<div class=\"equipment-slot\"><span class=\"equipment-slot-label\">Armor:</span><span class=\"equipment-slot-value\">" + armorLine + armorButton + "</span></div>" +
    "<div class=\"equipment-slot\"><span class=\"equipment-slot-label\">Trinket:</span><span class=\"equipment-slot-value\">" + trinketLine + trinketButton + "</span></div>" +
    "<div class=\"equipment-slot\"><span class=\"equipment-slot-label\">Total Attack:</span><span class=\"equipment-slot-value\">" + totalAttack + "</span></div>" +
    "<div class=\"equipment-slot\"><span class=\"equipment-slot-label\">Total Defense:</span><span class=\"equipment-slot-value\">" + totalDefense + "</span></div>" +
    "<div class=\"equipment-slot\"><span class=\"equipment-slot-label\">Max HP:</span><span class=\"equipment-slot-value\">" + maxHp + "</span></div>";
  if(nextEquipmentMarkup!==sidebarEquipmentMarkup){
    equipmentList.innerHTML = nextEquipmentMarkup;
    sidebarEquipmentMarkup=nextEquipmentMarkup;
  }
  const nextSkillsMarkup=["swordsmanship","defense","survival"].map((skillId)=>{
    const skill=player.skills?.[skillId] || { level:1, xp:0 };
    const nextThreshold=getSkillXpThresholdForLevel(skill.level+1);
    const progressText=skill.level>=SKILL_MAX_LEVEL
      ? "MAX"
      : (skill.xp + " / " + nextThreshold);
    return "<div class=\"equipment-slot\"><span class=\"equipment-slot-label\">" + SKILL_DISPLAY_NAMES[skillId] + "</span><span class=\"equipment-slot-value\">Lv " + skill.level + " — " + progressText + "</span></div>";
  }).join("");
  if(nextSkillsMarkup!==sidebarSkillsMarkup){
    skillsList.innerHTML=nextSkillsMarkup;
    sidebarSkillsMarkup=nextSkillsMarkup;
  }
  const targetHostile=getNearestHostile(PLAYER_ATTACK_RANGE);
  const currentTarget=targetHostile?.entity || null;
  const targetCooldownMs=currentTarget ? Math.max(0, getHostileAttackCooldownMs(currentTarget)-(performance.now()-getHostileLastAttackAt(currentTarget))) : 0;
  const targetCooldownText=!currentTarget ? "N/A" : (currentTarget.hp<=0 ? "Down" : (targetCooldownMs<=0 ? "Ready" : (targetCooldownMs/1000).toFixed(1)+"s"));
  const interactionPrompt=interactionManager.getPromptText();
  const hudLines=[
    "WASD / Arrows : Move",
    "E : contextual action",
    "Space : Attack",
    "H : Quick-use healing item",
    "K : Manual Save",
    "1-9 : Dialogue Choices",
    "G : Toggle grid"
  ];
  if(interactionPrompt) hudLines.splice(1, 0, interactionPrompt);
  hud.textContent=hudLines.join("\n");
  if(DEV_MODE){
    debugPanel.style.display="block";
    debugPanel.textContent = "DEV TOOLS\n" +
      "~ : Toggle Debug Panel\n" +
      "F6 : Debug Heal\n" +
      "F7/F8/F9 : Debug Teleport\n" +
      "F10 : Debug Reset Quest\n" +
      "Shift+F10 : Debug Reset Save\n" +
      "Debug Lv/ATK/DEF : " + player.level + " / " + totalAttack + " / " + totalDefense + "\n" +
      "Skills S/D/Sv : " + getSkillLevel("swordsmanship") + " / " + getSkillLevel("defense") + " / " + getSkillLevel("survival") + "\n" +
      "Target HP : " + (currentTarget ? (currentTarget.hp + "/" + currentTarget.maxHp) : "N/A") + "\n" +
      "Target cooldown : " + targetCooldownText;
  } else {
    debugPanel.style.display="none";
    debugPanel.textContent="";
  }
}

function canMoveTo(x,y){
  if(!isTileInCurrentZone(x,y)) return false;
  if(isWorldObjectBlockingTile(x,y)) return false;
  if(isInMirrorCave){
    if(mirrorCave.blocked.has(keyOf(x,y))) return false;
  } else if(isInAbandonedTollhouse){
    if(abandonedTollhouse.blocked.has(keyOf(x,y))) return false;
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
  const priority=["the_still_water","hunters_request","mirror_pond_listening"];
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
    isInAbandonedTollhouse=false;
    currentZoneId="hearthvale_square";
    setPlayerTilePosition(18, 11);
    log("[Debug] Teleported to Hearthvale Square.");
  } else if(zoneId==="eastern_woods"){
    isInMirrorCave=false;
    isInAbandonedTollhouse=false;
    currentZoneId="eastern_woods";
    setPlayerTilePosition(mirrorCave.returnTile.x, mirrorCave.returnTile.y);
    log("[Debug] Teleported to Eastern Woods.");
  } else if(zoneId==="mirror_cave"){
    isInAbandonedTollhouse=false;
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
  const isDevToggleKey=e.code==="Backquote";
  if(["w","a","s","d","arrowup","arrowdown","arrowleft","arrowright"," ","e","escape","h","k","1","2","3","4","5","6","7","8","9","f6","f7","f8","f9","f10"].includes(k) || isDevToggleKey) e.preventDefault();
  if(DIRECTION_KEYS.includes(k)){
    if(blockedDirectionalKeysUntilRelease.has(k)) return;
  }
  if(isDevToggleKey){
    DEV_MODE=!DEV_MODE;
    log(DEV_MODE ? "Dev mode enabled" : "Dev mode disabled");
    updateSidebar();
  }
  if(k==="g") showGrid=!showGrid;
  if(k==="escape" && worldInfoPanel) closeWorldInfoPanel();
  else if(k==="escape" && dialogueSystem.activeSession) dialogueSystem.close();
  if(k==="e") interactionManager.tryInteract();
  if(k==="h") useHealingConsumable();
  if(k==="k") saveGame("manual");
  if(DEV_MODE && k==="f6") healPlayerToFullForDebug();
  if(DEV_MODE && k==="f7") teleportToZoneForDebug("hearthvale_square");
  if(DEV_MODE && k==="f8") teleportToZoneForDebug("eastern_woods");
  if(DEV_MODE && k==="f9") teleportToZoneForDebug("mirror_cave");
  if(DEV_MODE && k==="f10" && e.shiftKey) resetFullSaveForDebug();
  else if(DEV_MODE && k==="f10") resetCurrentQuestForDebug();
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
  const useTarget=e.target instanceof Element ? e.target.closest("button[data-use-item]") : null;
  if(useTarget instanceof HTMLElement){
    const itemId=useTarget.dataset?.useItem;
    const item=getItemDefinition(itemId || "");
    if(item && item.type==="consumable" && Number.isFinite(item.healAmount) && Math.floor(item.healAmount)>0){
      consumeHealingItem(item);
    }
    return;
  }
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
  const mapW=isInMirrorCave ? mirrorCave.width : (isInAbandonedTollhouse ? abandonedTollhouse.width : WORLD_W);
  const mapH=isInMirrorCave ? mirrorCave.height : (isInAbandonedTollhouse ? abandonedTollhouse.height : WORLD_H);
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
  if(isWorldObjectBlockingTile(x,y)) return false;
  if(isInMirrorCave){
    if(mirrorCave.blocked.has(keyOf(x,y))) return false;
  } else if(isInAbandonedTollhouse){
    if(abandonedTollhouse.blocked.has(keyOf(x,y))) return false;
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
  return now<hostileAggroBlockedUntil;
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
    if(bandit.noRespawn) return;
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
    if(dist>1||now-(lastWolfAttackAt[wolf.id]||0)<getHostileAttackCooldownMs(wolf)) continue;
    lastWolfAttackAt[wolf.id]=now;
    wolf.attackUntil=now+350;
    const damageDealt=applyIncomingDamage(getEnemyConfig(wolf.enemyType || "wolf").damage); player.hitUntil=now+300; player.hitFlickerUntil=now+220; hitStopUntil=now+55;
    const wx=player.targetX-wolf.targetX, wy=player.targetY-wolf.targetY, len=Math.max(1,Math.hypot(wx,wy));
    wolf.attackLungeX=(wx/len)*2; wolf.attackLungeY=(wy/len)*1.2; player.recoilX=(wx/len)*2.5; player.recoilY=(wy/len)*1.6;
    spawnFloatingText(player.px/TILE, player.py/TILE, "-" + damageDealt, { color:"#ff9b9b", durationMs:900 });
    logCombat(hostileLabel(wolf) + " bites you for " + damageDealt + " damage.");
    if(player.hp<=0){ handlePlayerDefeat(); break; }
  }
}
function banditAttack(now){
  if(isHostileAggroBlocked(now)) return;
  for(const bandit of getActiveHostiles().filter((hostile)=>hostile.kind==="bandit")){
    if(bandit.hp<=0) continue;
    const dist=Math.abs(player.targetX-bandit.targetX)+Math.abs(player.targetY-bandit.targetY);
    if(dist>1||now-(lastBanditAttackAt[bandit.id]||0)<getHostileAttackCooldownMs(bandit)) continue;
    lastBanditAttackAt[bandit.id]=now;
    bandit.attackUntil=now+350;
    const damageDealt=applyIncomingDamage(getEnemyConfig(bandit.enemyType || "bandit").damage); player.hitUntil=now+320; player.hitFlickerUntil=now+260; hitStopUntil=now+60;
    const wx=player.targetX-bandit.targetX, wy=player.targetY-bandit.targetY, len=Math.max(1,Math.hypot(wx,wy));
    bandit.attackLungeX=(wx/len)*2.2; bandit.attackLungeY=(wy/len)*1.3; player.recoilX=(wx/len)*2.8; player.recoilY=(wy/len)*1.8;
    spawnFloatingText(player.px/TILE, player.py/TILE, "-" + damageDealt, { color:"#ff8888", durationMs:900 });
    logCombat(hostileLabel(bandit) + " slashes you for " + damageDealt + " damage.");
    if(player.hp<=0){ handlePlayerDefeat(); break; }
  }
}
function defeatWolf(wolf,now){
  const enemyConfig=getEnemyConfig(wolf.enemyType || "wolf");
  wolf.defeated=true;
  grantPlayerXp(enemyConfig.xp);
  if(getEquippedItem("weapon")?.type==="weapon") gainSkillXp("swordsmanship", 10);
  if(getArmorDefenseBonus()>0 && player.hp>0) gainSkillXp("defense", 5);
  player.coins+=enemyConfig.coinReward;
  const lootDrops=rollEnemyLoot(wolf.enemyType || "wolf");
  lootDrops.forEach((drop)=>addItemToInventory(drop.itemId, drop.quantity));
  wolfRespawnAtById[wolf.id]=now+enemyConfig.respawnMs;
  log(hostileLabel(wolf) + " defeated. Rewards: +" + enemyConfig.xp + " XP, +" + enemyConfig.coinReward + " coins.");
  showRewardToasts(["+" + enemyConfig.xp + " XP", "+" + enemyConfig.coinReward + " Coins"]);
  eventSystem.emit("combat:enemy-defeated",{ enemyType:"wolf", enemyId:wolf.id });
  if(lootDrops.length){
    log("Loot acquired: " + formatDropText(lootDrops) + ".");
    showRewardToasts(lootDrops.map((drop)=>{
      const item=getItemDefinition(drop.itemId);
      return "+ " + (item?.name || drop.itemId) + " x" + drop.quantity;
    }));
  }
  else log("No loot dropped this time.");
}
function defeatBandit(bandit,now){
  const enemyConfig=getEnemyConfig(bandit.enemyType || "bandit");
  bandit.defeated=true;
  grantPlayerXp(enemyConfig.xp);
  if(getEquippedItem("weapon")?.type==="weapon") gainSkillXp("swordsmanship", 10);
  if(getArmorDefenseBonus()>0 && player.hp>0) gainSkillXp("defense", 5);
  player.coins+=enemyConfig.coinReward;
  const lootDrops=rollEnemyLoot(bandit.enemyType || "bandit");
  lootDrops.forEach((drop)=>addItemToInventory(drop.itemId, drop.quantity));
  banditRespawnAtById[bandit.id]=bandit.noRespawn ? 0 : now+enemyConfig.respawnMs;
  if(bandit.isMiniBoss){
    rookTollkeeperDefeated=true;
    patchPersistentObject("rook_tollkeeper_state", { defeated:true, state:"defeated" }, false);
    const bossRewardLines=["+ " + enemyConfig.xp + " XP", "+ " + enemyConfig.coinReward + " Coins"];
    const bossRewardToasts=["ROOK DEFEATED", "Rook the Tollkeeper falls.", "+" + enemyConfig.xp + " XP", "+" + enemyConfig.coinReward + " Coins", "Tollhouse chest unlocked"];
    log("Rook the Tollkeeper falls. The old road is safer.");
    log("Boss rewards:");
    bossRewardLines.forEach((line)=>log(line));
    showRewardToasts(bossRewardToasts);
    triggerCameraShake(220, 3.6);
    syncTollhouseChestState(false);
    syncAbandonedTollhouseClearedState(false, false);
    saveGame("rook_defeated");
  } else {
    log(hostileLabel(bandit) + " defeated. Rewards: +" + enemyConfig.xp + " XP, +" + enemyConfig.coinReward + " coins.");
    showRewardToasts(["+" + enemyConfig.xp + " XP", "+" + enemyConfig.coinReward + " Coins"]);
  }
  if(lootDrops.length){
    log("Loot acquired: " + formatDropText(lootDrops) + ".");
    showRewardToasts(lootDrops.map((drop)=>{
      const item=getItemDefinition(drop.itemId);
      return "+ " + (item?.name || drop.itemId) + " x" + drop.quantity;
    }));
  }
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
      logThrottled("combat:miss_no_target", "Attack misses — no hostile in range.", 1800);
      lastNoTargetLogAt=now;
      missNoticeArmed=false;
      showRewardToast("Miss", 700);
    }
    return;
  }
  missNoticeArmed=false;
  const tx=targetHostile.entity.targetX-player.targetX;
  const ty=targetHostile.entity.targetY-player.targetY;
  const len=Math.max(1,Math.hypot(tx,ty));
  player.attackLungeX=(tx/len)*2.4;
  player.attackLungeY=(ty/len)*1.4;
  const totalDamage=getTotalAttackDamage();
  targetHostile.entity.hp=Math.max(0,targetHostile.entity.hp-totalDamage);
  targetHostile.entity.hitUntil=now+320;
  targetHostile.entity.hitFlickerUntil=now+240;
  targetHostile.entity.recoilX=(tx/len)*2.3;
  targetHostile.entity.recoilY=(ty/len)*1.5;
  hitStopUntil=now+65;
  if(totalDamage>=10) triggerCameraShake(95, 1.4);
  if(totalDamage>=14) triggerCameraShake(130, 2.4);
  spawnFloatingText(targetHostile.entity.px/TILE, targetHostile.entity.py/TILE, "-" + totalDamage, { color:"#ffe29b", durationMs:950 });
  if(getEquippedItem("weapon")?.type==="weapon") gainSkillXp("swordsmanship", 3);
  logCombat("Hit " + hostileLabel(targetHostile.entity) + " for " + totalDamage + " damage.");
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
          ctx.fillStyle="rgba(9,15,22,.82)"; ctx.fillRect(rect.x,rect.y,rect.w,rect.h);
          ctx.strokeStyle=entry.priority>=4 ? "rgba(255,226,159,.85)" : "rgba(211,224,242,.42)"; ctx.strokeRect(rect.x-.5,rect.y-.5,rect.w,rect.h);
          ctx.fillStyle=entry.priority>=4 ? "#ffe8b0" : "#f4fbff"; ctx.font="bold 11px monospace"; ctx.fillText(text,rect.x+4,rect.y+10);
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
function drawMirrorPondInspectionMarker(now){
  const screenPos=tileToScreen(Math.floor(pond.cx), Math.floor(pond.cy)-1);
  const pulse=(Math.sin(now*0.006)+1)*0.5;
  ctx.save();
  ctx.strokeStyle="rgba(161,210,255," + (0.35 + pulse*0.25).toFixed(3) + ")";
  ctx.fillStyle="rgba(142,202,255," + (0.12 + pulse*0.1).toFixed(3) + ")";
  ctx.lineWidth=1.2;
  ctx.beginPath();
  ctx.ellipse(screenPos.x+16, screenPos.y+16, 8+pulse*2, 4+pulse*1.5, 0, 0, Math.PI*2);
  ctx.fill();
  ctx.stroke();
  ctx.fillStyle="rgba(217,241,255," + (0.52 + pulse*0.3).toFixed(3) + ")";
  ctx.beginPath();
  ctx.arc(screenPos.x+16, screenPos.y+12, 1.8+pulse*1.2, 0, Math.PI*2);
  ctx.fill();
  ctx.restore();
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

function drawEntityRing(tx,ty,color,alpha=0.35,radius=9){
  const p=tileToScreen(tx,ty);
  ctx.save();
  ctx.fillStyle=color.replace("__A__", (alpha*0.12).toFixed(3));
  ctx.beginPath();
  ctx.ellipse(p.x+16,p.y+23,radius*1.25,radius*0.72,0,0,Math.PI*2);
  ctx.fill();
  ctx.strokeStyle=color.replace("__A__", alpha.toFixed(3));
  ctx.lineWidth=1.4;
  ctx.beginPath();
  ctx.ellipse(p.x+16,p.y+26,radius,radius*0.45,0,0,Math.PI*2);
  ctx.stroke();
  ctx.fillStyle=color.replace("__A__", (alpha*0.35).toFixed(3));
  ctx.beginPath();
  ctx.ellipse(p.x+16,p.y+26,radius*0.65,radius*0.24,0,0,Math.PI*2);
  ctx.fill();
  ctx.restore();
}

function drawOutdoorBackdrop(cam, now){
  const sx=cam.offsetX;
  const sy=cam.offsetY;
  const ex=sx+VIEW_TILES_X*TILE;
  const ey=sy+VIEW_TILES_Y*TILE;
  const bg=ctx.createLinearGradient(0,0,0,canvas.height);
  bg.addColorStop(0,"#203525");
  bg.addColorStop(0.55,"#274332");
  bg.addColorStop(1,"#17291f");
  ctx.fillStyle=bg;
  ctx.fillRect(0,0,canvas.width,canvas.height);

  const padX=Math.ceil(Math.max(sx, canvas.width-ex)/TILE)+4;
  const padY=Math.ceil(Math.max(sy, canvas.height-ey)/TILE)+4;
  for(let y=cam.tileY-padY;y<cam.tileY+VIEW_TILES_Y+padY;y++){
    for(let x=cam.tileX-padX;x<cam.tileX+VIEW_TILES_X+padX;x++){
      if(x>=0&&x<WORLD_W&&y>=0&&y<WORLD_H) continue;
      const p=tileToScreen(x,y);
      const v=Math.floor(rng(x,y,603)*assets.forestGrass.length);
      const img=assets.forestGrass[v];
      if(img.complete&&img.naturalWidth>0) ctx.drawImage(img,p.x,p.y,TILE,TILE);
      if(rng(x,y,612)>0.92){
        ctx.fillStyle="rgba(86,126,72,.18)";
        ctx.fillRect(p.x+6,p.y+8,20,12);
      }
    }
  }

  const mist=ctx.createRadialGradient(canvas.width*.5,canvas.height*.46,Math.min(canvas.width,canvas.height)*.2,canvas.width*.5,canvas.height*.5,Math.max(canvas.width,canvas.height)*.85);
  mist.addColorStop(0,"rgba(196,219,184,0)");
  mist.addColorStop(.7,"rgba(74,105,84,.08)");
  mist.addColorStop(1,"rgba(8,14,12,.54)");
  ctx.fillStyle=mist;
  ctx.fillRect(0,0,canvas.width,canvas.height);

  const pulse=(Math.sin(now*0.0005)+1)*0.5;
  ctx.strokeStyle="rgba(43,65,48," + (0.45+pulse*0.1).toFixed(3) + ")";
  ctx.lineWidth=2;
  ctx.strokeRect(sx-1,sy-1,ex-sx+2,ey-sy+2);
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
      ctx.fillStyle=noise>0.5 ? palette.cave[1] : palette.cave[3];
    } else {
      ctx.fillStyle=noise>0.5 ? palette.cave[0] : "#39414d";
    }
    ctx.fillRect(p.x,p.y,32,32);
    if(mirrorCave.walls.has(k)){
      ctx.fillStyle="rgba(144,156,176,.24)";
      ctx.fillRect(p.x,p.y,32,6);
    }
  }
  const cp=tileToScreen(mirrorCave.chest.x, mirrorCave.chest.y);
  const chestState=getMirrorCaveChestState();
  drawSoftShadow(cp.x+16,cp.y+26,10,4,.2);
  ctx.fillStyle="#6b4c2f"; ctx.fillRect(cp.x+6,cp.y+10,20,14);
  if(chestState==="open"){
    ctx.fillStyle="#4c3927"; ctx.fillRect(cp.x+6,cp.y+8,20,4);
    ctx.fillStyle="#d6bc7f"; ctx.fillRect(cp.x+6,cp.y+11,20,2);
  } else {
    ctx.fillStyle="#b58f56"; ctx.fillRect(cp.x+6,cp.y+10,20,4);
    ctx.fillStyle="#d6bc7f"; ctx.fillRect(cp.x+14,cp.y+14,4,6);
    if(chestState==="sealed"){
      ctx.fillStyle="#7ea8dc";
      ctx.fillRect(cp.x+9,cp.y+15,14,2);
      ctx.fillRect(cp.x+15,cp.y+12,2,8);
    }
  }
  const ep=tileToScreen(mirrorCave.exit.x, mirrorCave.exit.y);
  ctx.fillStyle="rgba(155,170,189,.2)"; ctx.fillRect(ep.x+4,ep.y+4,24,24);
  ctx.strokeStyle="rgba(199,214,236,.5)"; ctx.strokeRect(ep.x+4.5,ep.y+4.5,23,23);
  ctx.fillStyle="#c7d6ec"; ctx.font="bold 10px monospace"; ctx.fillText("EXIT", ep.x+6, ep.y+19);
  const echoPersistent=getPersistentObject("echo_fragment_object");
  const echoCollected=Boolean(echoPersistent.collected) || getItemQuantity("echo_fragment")>0;
  const stillWaterStage=getStillWaterQuestStage();
  if(!echoCollected && stillWaterStage===StillWaterQuestStage.STAGE_5_RECOVER_ECHO_FRAGMENT){
    const fp=tileToScreen(12,5);
    const pulse=0.45+Math.sin(now*0.006)*0.2;
    ctx.fillStyle="rgba(146,192,246," + pulse.toFixed(3) + ")";
    ctx.beginPath();
    ctx.moveTo(fp.x+16,fp.y+7);
    ctx.lineTo(fp.x+22,fp.y+17);
    ctx.lineTo(fp.x+16,fp.y+25);
    ctx.lineTo(fp.x+10,fp.y+17);
    ctx.closePath();
    ctx.fill();
    ctx.strokeStyle="rgba(214,234,255,.82)";
    ctx.stroke();
  }

  mirrorCaveWolves.forEach((wolf)=>{
    if(wolf.hp<=0) return;
    drawEntityRing(wolf.px/TILE,wolf.py/TILE,"rgba(255,149,122,__A__)",0.25,8);
    drawWolf(wolf, wolf.px/TILE, wolf.py/TILE, wolf.facing, wolf.moving, 0.82, hitVisualAlpha(wolf), {x:wolf.recoilX+wolf.attackLungeX,y:wolf.recoilY+wolf.attackLungeY});
  });
  drawEntityRing(player.px/TILE,player.py/TILE,"rgba(186,218,255,__A__)",0.5,9.8);
  drawHumanoid(assets.sprites.player, player.px/TILE, player.py/TILE, player.facing, player.moving, 0.88, "Wayfarer", hitVisualAlpha(player), {x:player.recoilX+player.attackLungeX,y:player.recoilY+player.attackLungeY}, attackPose(player));
  ctx.fillStyle="rgba(8,10,14,.2)"; ctx.fillRect(0,0,canvas.width,canvas.height);
  drawTransitionFade(now);
}
function drawAbandonedTollhouseScene(now){
  ctx.clearRect(0,0,canvas.width,canvas.height);
  const cam=getCamera();
  for(let y=cam.tileY;y<cam.tileY+VIEW_TILES_Y;y++) for(let x=cam.tileX;x<cam.tileX+VIEW_TILES_X;x++){
    const p=tileToScreen(x,y);
    const k=keyOf(x,y);
    if(!isTileInCurrentZone(x,y)) continue;
    const noise=rng(x,y,377);
    if(abandonedTollhouse.blocked.has(k)){
      ctx.fillStyle=noise>0.5 ? palette.tollhouse[3] : "#392b1f";
    } else {
      ctx.fillStyle=noise>0.5 ? palette.tollhouse[0] : palette.tollhouse[1];
    }
    ctx.fillRect(p.x,p.y,32,32);
    if(abandonedTollhouse.walls.has(k)){
      ctx.fillStyle="rgba(34,25,18,.44)";
      ctx.fillRect(p.x,p.y,32,6);
    }
  }
  const barrelTiles=[{x:8,y:9},{x:9,y:11},{x:18,y:7},{x:20,y:6},{x:14,y:11}];
  barrelTiles.forEach((tile,idx)=>{
    const bp=tileToScreen(tile.x,tile.y);
    const type=idx%2===0 ? "barrel" : "crate";
    const sprite=assets.props.sprites[type];
    if(sprite && sprite.complete && sprite.naturalWidth>0) ctx.drawImage(sprite,bp.x,bp.y,32,32);
  });
  const chestState=getTollhouseChestState();
  const cp=tileToScreen(abandonedTollhouse.chest.x, abandonedTollhouse.chest.y);
  drawSoftShadow(cp.x+16,cp.y+26,10,4,.2);
  ctx.fillStyle="#5f4228"; ctx.fillRect(cp.x+6,cp.y+10,20,14);
  if(chestState==="open"){
    ctx.fillStyle="#3f2e20"; ctx.fillRect(cp.x+6,cp.y+8,20,4);
  } else {
    ctx.fillStyle="#b58f56"; ctx.fillRect(cp.x+6,cp.y+10,20,4);
    if(chestState==="locked"){
      ctx.fillStyle="#d9d0af"; ctx.fillRect(cp.x+14,cp.y+14,4,6);
    }
  }
  const ep=tileToScreen(abandonedTollhouse.exit.x, abandonedTollhouse.exit.y);
  ctx.fillStyle="rgba(190,162,133,.2)"; ctx.fillRect(ep.x+4,ep.y+4,24,24);
  ctx.strokeStyle="rgba(226,208,186,.6)"; ctx.strokeRect(ep.x+4.5,ep.y+4.5,23,23);
  ctx.fillStyle="#efdac2"; ctx.font="bold 10px monospace"; ctx.fillText("EXIT", ep.x+6, ep.y+19);
  tollhouseBandits.forEach((bandit)=>{
    if(bandit.hp<=0) return;
    drawEntityRing(bandit.px/TILE,bandit.py/TILE,"rgba(255,120,120,__A__)",0.28,8.5);
    drawHumanoid(assets.sprites.bandit, bandit.px/TILE, bandit.py/TILE, bandit.facing, bandit.moving, 0.83, "", hitVisualAlpha(bandit), {x:bandit.recoilX+bandit.attackLungeX,y:bandit.recoilY+bandit.attackLungeY}, attackPose(bandit));
  });
  if(!rookTollkeeperDefeated && rookTollkeeper.hp>0){
    drawEntityRing(rookTollkeeper.px/TILE,rookTollkeeper.py/TILE,"rgba(255,84,84,__A__)",0.45,10.5);
    drawHumanoid(assets.sprites.rook, rookTollkeeper.px/TILE, rookTollkeeper.py/TILE, rookTollkeeper.facing, rookTollkeeper.moving, 0.92, "", hitVisualAlpha(rookTollkeeper), {x:rookTollkeeper.recoilX+rookTollkeeper.attackLungeX,y:rookTollkeeper.recoilY+rookTollkeeper.attackLungeY}, attackPose(rookTollkeeper));
  }
  drawEntityRing(player.px/TILE,player.py/TILE,"rgba(186,218,255,__A__)",0.5,9.8);
  drawHumanoid(assets.sprites.player, player.px/TILE, player.py/TILE, player.facing, player.moving, 0.88, "Wayfarer", hitVisualAlpha(player), {x:player.recoilX+player.attackLungeX,y:player.recoilY+player.attackLungeY}, attackPose(player));
  const currentTarget=getCurrentCombatTarget(5);
  const hostileLabelEntries=[...tollhouseBandits, rookTollkeeper]
    .filter((hostile)=>hostile.hp>0 && Math.abs(player.targetX-hostile.targetX)+Math.abs(player.targetY-hostile.targetY)<=4)
    .map((hostile)=>({
      text:(hostile===currentTarget ? "[Target] " : "") + hostileLabel(hostile) + " " + hostile.hp + "/" + hostile.maxHp,
      tx:hostile.px/TILE,
      ty:hostile.py/TILE,
      priority:hostile===currentTarget ? 4 : 1
    }));
  drawWorldLabels([{text:"Wayfarer", tx:player.px/TILE, ty:player.py/TILE, priority:2}, ...hostileLabelEntries, {text:"Abandoned Tollhouse", tx:12, ty:16, priority:0}]);
  drawTransitionFade(now);
}

function drawWorld(){
  const now=performance.now();
  const shakeActive=now<cameraShakeUntil;
  const shakeMagnitude=shakeActive ? cameraShakeStrength*Math.max(0.15, (cameraShakeUntil-now)/180) : 0;
  const shakeX=shakeActive ? (Math.random()*2-1)*shakeMagnitude : 0;
  const shakeY=shakeActive ? (Math.random()*2-1)*shakeMagnitude : 0;
  ctx.save();
  if(shakeActive){
    ctx.translate(Math.round(shakeX), Math.round(shakeY));
  } else {
    cameraShakeStrength=0;
  }
  if(isInMirrorCave){
    drawMirrorCaveScene(now);
    drawFloatingTexts(now);
    ctx.restore();
    return;
  }
  if(isInAbandonedTollhouse){
    drawAbandonedTollhouseScene(now);
    drawFloatingTexts(now);
    ctx.restore();
    return;
  }
  ctx.clearRect(0,0,canvas.width,canvas.height);
  const cam=getCamera();
  drawOutdoorBackdrop(cam, now);
  const padX=Math.ceil(Math.max(cam.offsetX, canvas.width-(cam.offsetX+VIEW_TILES_X*TILE))/TILE)+3;
  const padY=Math.ceil(Math.max(cam.offsetY, canvas.height-(cam.offsetY+VIEW_TILES_Y*TILE))/TILE)+3;
  for(let y=cam.tileY-padY;y<cam.tileY+VIEW_TILES_Y+padY;y++) for(let x=cam.tileX-padX;x<cam.tileX+VIEW_TILES_X+padX;x++){
    const p=tileToScreen(x,y);
    if(x<0 || y<0 || x>=WORLD_W || y>=WORLD_H) continue;
    const n=layeredNoise(x,y);
    const n2=layeredNoise(x+2.2,y+1.6)*0.35 + layeredNoise(x-3.4,y-0.8)*0.25;
    const tone=Math.max(0, Math.min(0.999, n*0.75 + n2));
    const mix=Math.min(assets.grass.length-1, Math.floor(tone*assets.grass.length));
    const region=getOutdoorRegionIdAt(x,y);
    const inForest=region==="eastern_woods" || (region==="north_road" && rng(x,y,211)>0.45);
    const forestMix=Math.min(assets.forestGrass.length-1, Math.floor((layeredNoise(x+5,y+3)+rng(x,y,212)*0.2)*assets.forestGrass.length)%assets.forestGrass.length);
    const img=inForest ? assets.forestGrass[forestMix] : assets.grass[mix];
    if(img.complete&&img.naturalWidth>0) ctx.drawImage(img,p.x,p.y,TILE,TILE);
    if(!inForest && layeredNoise(x+13,y+7)>0.74){
      ctx.fillStyle="rgba(188,216,151,.02)";
      ctx.fillRect(p.x+1,p.y+1,30,30);
    }
    if(world.roadTiles.has(keyOf(x,y))){
      ctx.fillStyle="rgba(77,109,63,.06)";
      ctx.fillRect(p.x,p.y,32,32);
    }
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

    if(!north || !south || !east || !west){
      ctx.fillStyle="rgba(84,118,64,.16)";
      if(!north) ctx.fillRect(p.x+2,p.y+1,28,2);
      if(!south) ctx.fillRect(p.x+2,p.y+29,28,2);
      if(!east) ctx.fillRect(p.x+29,p.y+2,2,28);
      if(!west) ctx.fillRect(p.x+1,p.y+2,2,28);
    }
    if((north&&south&&east&&west) || ((!north&&!south)&&(east||west)) || ((!east&&!west)&&(north||south))){
      ctx.fillStyle="rgba(121,95,64,.18)";
      ctx.fillRect(p.x+11,p.y+11,10,10);
      ctx.fillStyle="rgba(203,176,138,.07)";
      ctx.fillRect(p.x+13,p.y+13,6,2);
    }
  } });

  for(let x=pond.x-1;x<=pond.x+pond.w;x++) for(let y=pond.y-1;y<=pond.y+pond.h;y++){
    const k=keyOf(x,y); if(!world.pondWater.has(k)) continue;
    const p=tileToScreen(x,y); const edge=world.pondNearEdge.has(k);
    const img=edge?assets.water.shallow:assets.water.deep; if(img.complete&&img.naturalWidth>0) ctx.drawImage(img,p.x,p.y,32,32);
    const t=performance.now()*0.002, rip=(Math.sin(t*3+x*1.1+y*.8)+1)*.5;
    const mirrorAura=(x>=25&&x<=30&&y>=12&&y<=17) ? 0.1 : 0.02;
    ctx.fillStyle="rgba(188,228,255," + (.02+rip*.05+mirrorAura).toFixed(3) + ")"; ctx.fillRect(p.x+3,p.y+6,TILE-10,1);
    if(edge){
      ctx.fillStyle="rgba(224,244,255," + (.05+rip*.05).toFixed(3) + ")"; ctx.fillRect(p.x+1,p.y+1,TILE-2,1);
      if(assets.water.edge.complete&&assets.water.edge.naturalWidth>0) ctx.drawImage(assets.water.edge,p.x,p.y,32,32);
    }
    if(rng(x,y,402)>0.84){
      ctx.fillStyle="rgba(201,240,255,.25)";
      ctx.fillRect(p.x+10,p.y+10,4,1);
      ctx.fillRect(p.x+14,p.y+9,2,1);
    }
    if(rng(x,y,409)>0.77){
      ctx.fillStyle="rgba(176,225,255,.2)";
      ctx.fillRect(p.x+7,p.y+20,8,1);
    }
  }
  for(let x=pond.x-1;x<=pond.x+pond.w;x++) for(let y=pond.y-1;y<=pond.y+pond.h;y++){
    const k=keyOf(x,y); if(!world.pondShore.has(k)) continue;
    const p=tileToScreen(x,y); const img=assets.shore[Math.floor(rng(x,y,33)*assets.shore.length)]; if(img.complete&&img.naturalWidth>0) ctx.drawImage(img,p.x,p.y,32,32);
    if(rng(x,y,491)>0.62){
      ctx.fillStyle="rgba(86,121,74,.55)";
      ctx.fillRect(p.x+5,p.y+14,2,8);
      ctx.fillRect(p.x+8,p.y+15,1,7);
    }
    if(rng(x,y,529)>0.72){
      ctx.fillStyle="rgba(198,214,162,.18)";
      ctx.fillRect(p.x+11,p.y+10,4,1);
    }
    if(rng(x,y,535)>0.8){
      ctx.fillStyle="rgba(116,149,94,.65)";
      ctx.fillRect(p.x+21,p.y+15,1,6);
      ctx.fillRect(p.x+23,p.y+14,1,7);
    }
  }

  world.buildings.forEach((b,bIndex)=>{
    for(let ry=0; ry<b.h; ry++){
      const right = tileToScreen(b.x+b.w, b.y+ry);
      drawShadowTile(assets.shadow.buildingRight, right.x+4, right.y+3, .9);
    }
    for(let rx=0; rx<b.w; rx++){
      const bottom = tileToScreen(b.x+rx, b.y+b.h);
      drawShadowTile(assets.shadow.buildingBottom, bottom.x+4, bottom.y+3, .88);
    }
    b.tileRows.forEach((row,ry)=> row.forEach((key,rx)=> { const p=tileToScreen(b.x+rx,b.y+ry); const img=assets.building[key]; if(img&&img.complete&&img.naturalWidth>0) ctx.drawImage(img,p.x,p.y,32,32); }));
    b.tileRows.forEach((row,ry)=>row.forEach((key,rx)=>{
      if(key!=="door") return;
      const p=tileToScreen(b.x+rx,b.y+ry+1);
      ctx.fillStyle="rgba(96,74,49,.42)";
      ctx.fillRect(p.x+7,p.y+1,18,5);
      ctx.fillStyle="rgba(192,164,123,.28)";
      ctx.fillRect(p.x+8,p.y+1,16,1);
      ctx.fillStyle="rgba(63,44,28,.38)";
      ctx.fillRect(p.x+6,p.y+5,20,2);
    }));
    const chimney=tileToScreen(b.x + (bIndex%2 ? b.w-2 : 1), b.y);
    ctx.fillStyle="rgba(94,72,54,.9)";
    ctx.fillRect(chimney.x+10,chimney.y-7,6,9);
    ctx.fillStyle="rgba(138,113,88,.85)";
    ctx.fillRect(chimney.x+9,chimney.y-8,8,2);
    if(rng(b.x,b.y,602)>0.4){
      ctx.fillStyle="rgba(255,244,226,.18)";
      ctx.fillRect(chimney.x+13,chimney.y-11,2,2);
    }
    const planter=tileToScreen(b.x+1,b.y+b.h-1);
    ctx.fillStyle="rgba(94,70,46,.7)";
    ctx.fillRect(planter.x+7,planter.y+24,18,3);
    ctx.fillStyle="rgba(121,157,90,.78)";
    ctx.fillRect(planter.x+8,planter.y+22,16,2);
  });

  world.props.forEach((prop)=>{
    const p = tileToScreen(prop.x,prop.y);
    const img = assets.props.sprites[prop.type];
    if(!img || !img.complete || img.naturalWidth<=0) return;
    if(prop.type==="barrel"||prop.type==="crate") drawShadowTile(assets.shadow.softTile,p.x+3,p.y+4,.78);
    if(prop.type==="handcart"||prop.type==="bench"||prop.type==="noticeBoard") drawShadowTile(assets.shadow.softTile,p.x+3,p.y+5,.72);
    if(prop.type==="sack"||prop.type==="stonePile") drawSoftShadow(p.x+16,p.y+26,8,3,.16);
    if(prop.type==="bush"||prop.type==="grassTuft") drawSoftShadow(p.x+16,p.y+26,9,4,.14);
    if(prop.type==="well"||prop.type==="lanternPost"||prop.type==="signPost") drawSoftShadow(p.x+16,p.y+27,10,4,.19);
    ctx.drawImage(img,p.x,p.y,32,32);
  });
  if(getStillWaterQuestStage()===StillWaterQuestStage.STAGE_2_INSPECT_MIRROR_POND){
    drawMirrorPondInspectionMarker(now);
  }
  const pondFocus=tileToScreen(pond.cx, pond.cy);
  const pondGlow=ctx.createRadialGradient(pondFocus.x+16,pondFocus.y+12,8,pondFocus.x+16,pondFocus.y+12,96);
  pondGlow.addColorStop(0,"rgba(173,214,255,.16)");
  pondGlow.addColorStop(.55,"rgba(120,174,220,.09)");
  pondGlow.addColorStop(1,"rgba(120,174,220,0)");
  ctx.fillStyle=pondGlow;
  ctx.fillRect(pondFocus.x-96,pondFocus.y-80,210,180);
  const caveEntrancePos=tileToScreen(OVERWORLD_CAVE_ENTRY.x, OVERWORLD_CAVE_ENTRY.y);
  ctx.fillStyle="rgba(23,29,38,.9)";
  ctx.beginPath();
  ctx.moveTo(caveEntrancePos.x+6,caveEntrancePos.y+26);
  ctx.lineTo(caveEntrancePos.x+16,caveEntrancePos.y+8);
  ctx.lineTo(caveEntrancePos.x+26,caveEntrancePos.y+26);
  ctx.closePath();
  ctx.fill();
  ctx.strokeStyle="rgba(168,186,204,.78)";
  ctx.stroke();
  const tollhouseDoorPos=tileToScreen(NORTH_ROAD_TOLLHOUSE_ENTRY.x, NORTH_ROAD_TOLLHOUSE_ENTRY.y);
  ctx.fillStyle="rgba(71,49,32,.92)";
  ctx.fillRect(tollhouseDoorPos.x+7,tollhouseDoorPos.y+6,18,22);
  ctx.strokeStyle="rgba(196,164,128,.75)";
  ctx.strokeRect(tollhouseDoorPos.x+7.5,tollhouseDoorPos.y+6.5,17,21);

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

  const zoneName=currentLocalAreaName();
  const zoneLabelEntries=[];
  if(zoneName==="North Road") zoneLabelEntries.push({ text:"North Road", tx:13, ty:1, priority:0 });
  if(zoneName==="Hearthvale Square") zoneLabelEntries.push({ text:"Hearthvale Square", tx:12, ty:7, priority:0 });
  if(zoneName==="Mirror Pond") zoneLabelEntries.push({ text:"Mirror Pond", tx:26, ty:12, priority:0 });
  if(zoneName==="Eastern Woods") zoneLabelEntries.push({ text:"Eastern Woods", tx:30, ty:4, priority:0 });

  drawEntityRing(npc.x,npc.y,"rgba(201,227,255,__A__)",0.4,8.8);
  drawHumanoid(assets.sprites.edrin, npc.x, npc.y, npc.facing, false, 0.84, "", 0, null, null);
  drawEntityRing(hunterNpc.x,hunterNpc.y,"rgba(208,232,184,__A__)",0.38,8.8);
  drawHumanoid(assets.sprites.hunter, hunterNpc.x, hunterNpc.y, hunterNpc.facing, false, 0.84, "", 0, null, null);
  drawEntityRing(vendorNpc.x,vendorNpc.y,"rgba(250,221,164,__A__)",0.38,8.8);
  drawHumanoid(assets.sprites.merchant, vendorNpc.x, vendorNpc.y, vendorNpc.facing, false, 0.84, "", 0, null, null);
  wolves.forEach((wolf)=>{
    if(wolf.hp<=0) return;
    drawEntityRing(wolf.px/TILE,wolf.py/TILE,"rgba(255,149,122,__A__)",0.25,8);
    drawWolf(wolf, wolf.px/TILE, wolf.py/TILE, wolf.facing, wolf.moving, 0.82, hitVisualAlpha(wolf), {x:wolf.recoilX+wolf.attackLungeX,y:wolf.recoilY+wolf.attackLungeY});
  });
  bandits.forEach((bandit)=>{
    if(bandit.hp<=0) return;
    drawEntityRing(bandit.px/TILE,bandit.py/TILE,"rgba(255,120,120,__A__)",0.28,8.5);
    drawHumanoid(assets.sprites.bandit, bandit.px/TILE, bandit.py/TILE, bandit.facing, bandit.moving, 0.83, "", hitVisualAlpha(bandit), {x:bandit.recoilX+bandit.attackLungeX,y:bandit.recoilY+bandit.attackLungeY}, attackPose(bandit));
  });
  drawEntityRing(player.px/TILE,player.py/TILE,"rgba(186,218,255,__A__)",0.5,9.8);
  drawHumanoid(assets.sprites.player, player.px/TILE, player.py/TILE, player.facing, player.moving, 0.88, "", hitVisualAlpha(player), {x:player.recoilX+player.attackLungeX,y:player.recoilY+player.attackLungeY}, attackPose(player));
  const currentTarget=getCurrentCombatTarget(5);
  const hostileLabelEntries=[...wolves, ...bandits]
    .filter((hostile)=>hostile.hp>0 && Math.abs(player.targetX-hostile.targetX)+Math.abs(player.targetY-hostile.targetY)<=4)
    .map((hostile)=>({
      text:(hostile===currentTarget ? "[Target] " : "") + hostileLabel(hostile) + " " + hostile.hp + "/" + hostile.maxHp,
      tx:hostile.px/TILE,
      ty:hostile.py/TILE,
      priority:hostile===currentTarget ? 4 : 1
    }));
  drawWorldLabels([
    {text:Math.abs(player.targetX-npc.x)+Math.abs(player.targetY-npc.y)<=5 ? npc.name : "", tx:npc.x, ty:npc.y, priority:3},
    {text:Math.abs(player.targetX-hunterNpc.x)+Math.abs(player.targetY-hunterNpc.y)<=5 ? hunterNpc.displayLabel : "", tx:hunterNpc.x, ty:hunterNpc.y, priority:3},
    {text:Math.abs(player.targetX-vendorNpc.x)+Math.abs(player.targetY-vendorNpc.y)<=5 ? vendorNpc.displayLabel : "", tx:vendorNpc.x, ty:vendorNpc.y, priority:3},
    {text:"Wayfarer", tx:player.px/TILE, ty:player.py/TILE, priority:2},
    ...hostileLabelEntries,
    ...zoneLabelEntries
  ]);

  const area=currentLocalAreaName();
  const baseTint=area==="Hearthvale Square" ? 0.045 : area==="Mirror Pond" ? 0.065 : area==="Eastern Woods" ? 0.095 : area==="North Road" ? 0.09 : 0.08;
  const tint=baseTint+Math.max(0,Math.sin(performance.now()/9000))*.04;
  const tintColor=area==="Hearthvale Square" ? "rgba(35,24,14," : area==="Mirror Pond" ? "rgba(18,26,42," : "rgba(9,16,26,";
  ctx.fillStyle=tintColor + tint.toFixed(3) + ")"; ctx.fillRect(0,0,canvas.width,canvas.height);
  const edge=ctx.createRadialGradient(canvas.width*.5,canvas.height*.5,Math.min(canvas.width,canvas.height)*.35,canvas.width*.5,canvas.height*.5,Math.max(canvas.width,canvas.height)*.68);
  edge.addColorStop(0,"rgba(0,0,0,0)"); edge.addColorStop(.78,"rgba(1,6,10,.1)"); edge.addColorStop(1,"rgba(1,6,10,.46)");
  ctx.fillStyle=edge; ctx.fillRect(0,0,canvas.width,canvas.height);
  drawTransitionFade(now);
  drawFloatingTexts(now);
  ctx.restore();
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
  tollhouseBandits.forEach((bandit)=>{
    bandit.recoilX*=.82; bandit.recoilY*=.82; bandit.attackLungeX*=.78; bandit.attackLungeY*=.78;
  });
  rookTollkeeper.recoilX*=.82; rookTollkeeper.recoilY*=.82; rookTollkeeper.attackLungeX*=.78; rookTollkeeper.attackLungeY*=.78;
  if(now<hitStopUntil){ updateSidebar(); return; }
  eventSystem.update(currentLocalAreaName());
  const isTransitionLocked=now<zoneTransitionLockedUntil;
  if(!isTransitionLocked) updateInput();
  tryPlayerAttack(now);
  smoothMove(player,dt);
  if(!player.moving){
    triggerWalkInWorldObject();
    handleZoneTransitionIfNeeded();
  }
  if(!isTransitionLocked && !player.moving && (moveIntent.dx!==0||moveIntent.dy!==0)) tryPlayerStep(moveIntent.dx,moveIntent.dy,moveIntent.facing);
  updateOutdoorRegionFromPosition(true);
  if(!isInMirrorCave && !isInAbandonedTollhouse && currentZoneId==="north_road"){
    const tollhouseDistance=Math.abs(player.targetX-NORTH_ROAD_TOLLHOUSE_ENTRY.x)+Math.abs(player.targetY-NORTH_ROAD_TOLLHOUSE_ENTRY.y);
    if(tollhouseDistance<=2) markAbandonedTollhouseDiscovered(true, true);
  }
  if(!isTransitionLocked){
    if(isInMirrorCave){
      mirrorCaveWolves.forEach((wolf)=>{ updateWolf(wolf,now); smoothMove(wolf,dt); });
    } else if(isInAbandonedTollhouse){
      tollhouseBandits.forEach((bandit)=>{ updateBandit(bandit,now); smoothMove(bandit,dt); });
      if(!rookTollkeeperDefeated){
        updateBandit(rookTollkeeper,now);
        smoothMove(rookTollkeeper,dt);
        if(!rookEncounterAnnounced && Math.abs(player.targetX-rookTollkeeper.targetX)+Math.abs(player.targetY-rookTollkeeper.targetY)<=4){
          rookEncounterAnnounced=true;
          log("Rook the Tollkeeper blocks the old road.");
          showRewardToast("Mini-Boss: Rook the Tollkeeper", 1700);
        }
      }
      banditAttack(now);
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
maybeAnnounceVerticalSliceEndpoint();
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
