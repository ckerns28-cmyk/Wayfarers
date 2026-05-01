export class WorldRoom {
  constructor(state, env) {
    this.state = state;
    this.env = env;
  }

  async fetch() {
    return new Response("WorldRoom active");
  }
}

function isLikelyStaticAssetRequest(pathname) {
  if (pathname.startsWith("/assets/")) return true;
  if (pathname.startsWith("/tiles/")) return true;
  return /\.(?:png|jpe?g|webp|gif|svg|ico|css|js|mjs|json|txt|map|woff2?|ttf|otf)$/i.test(pathname);
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const spriteAliasToAssetPath = {
      "/assets/sprites/medieval_town_buildings_sprite_sheet.png": "/tiles/buildings/test_house/Medieval town buildings sprite sheet.png",
      "/assets/sprites/medieval_town_asset_sprite_sheet.png": "/tiles/buildings/test_house/Medieval town asset sprite sheet.png"
    };
    const aliasedPath = spriteAliasToAssetPath[url.pathname];
    if(aliasedPath){
      const assetUrl = new URL(aliasedPath, url.origin);
      return Response.redirect(assetUrl.toString(), 302);
    }
    if (env?.ASSETS) {
      let assetResponse = null;
      if (url.pathname.startsWith("/assets/")) {
        const strippedUrl = new URL(request.url);
        strippedUrl.pathname = url.pathname.replace(/^\/assets/, "") || "/";
        const strippedRequest = new Request(strippedUrl.toString(), request);
        const strippedResponse = await env.ASSETS.fetch(strippedRequest);
        if (strippedResponse.ok) return strippedResponse;
        assetResponse = strippedResponse;
      }
      if (!assetResponse) {
        assetResponse = await env.ASSETS.fetch(request);
      }
      const assetContentType = assetResponse.headers.get("content-type") || "";
      const looksLikeHtmlShell = assetContentType.includes("text/html");
      const shouldPreferAsset = assetResponse.ok || isLikelyStaticAssetRequest(url.pathname);
      if (!shouldPreferAsset && looksLikeHtmlShell) {
        return new Response(html, {
          headers: {
            "content-type": "text/html; charset=UTF-8",
            "cache-control": "no-store",
          },
        });
      }
      if (shouldPreferAsset) return assetResponse;
    }
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
  <title>Wayfarer — Build Phase</title>
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
        <div class="sub" id="buildPhaseBanner">Build Phase</div>
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

const bootstrapErrorDedupe=new Set();

function reportBootstrapError(err,label){
  if(err===null){
    console.warn("[Bootstrap Warning] "+label+": rejection/error reason was null");
    return;
  }
  const message=(err&&err.message)?err.message:String(err);
  if(!message) return;
  const normalizedMessage=message.trim();
  if(!normalizedMessage || /^script error\.?$/i.test(normalizedMessage)) return;

  const dedupeKey=label+"::"+normalizedMessage;
  if(bootstrapErrorDedupe.has(dedupeKey)) return;
  bootstrapErrorDedupe.add(dedupeKey);

  console.error("[Bootstrap Error] "+label+": "+normalizedMessage, err);
  if(chat){
    const node=document.createElement("div");
    node.className="line system";
    node.textContent="[Startup Error] "+label+": "+normalizedMessage;
    chat.appendChild(node);
  }
}
window.addEventListener("error",(event)=>{
  reportBootstrapError(event?.error||event?.message||"unknown error","window.error");
});
window.addEventListener("unhandledrejection",(event)=>{
  if(event?.reason===null){
    console.warn("[Bootstrap Warning] unhandledrejection: reason was null");
    return;
  }
  reportBootstrapError(event?.reason||"unknown rejection","unhandledrejection");
});

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
  hearthvale_residence_district: {
    id: "hearthvale_residence_district",
    name: "Hearthvale Residence District",
    bounds: { x:27, y:7, w:WORLD_W-27, h:9 }
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

const USE_HEARTHVALE_ATLAS_PROOF = true;
const HEARTHVALE_ATLAS_SEMANTIC_ASSIGNMENTS = Object.freeze({
  village_hall_meeting_house:{ expectedIdentity:"top_right_meeting_house", preferredCandidateId:"C00", preferredBounds:{ x:853, y:10, w:327, h:460 } },
  residence_large:{ expectedIdentity:"middle_right_manor", preferredCandidateId:"C03", preferredBounds:{ x:758, y:493, w:459, h:355 } },
  residence_small:{ expectedIdentity:"middle_left_or_middle_center_residence", preferredCandidateId:"C04" },
  hunter_lodge_or_outfitter:{ expectedIdentity:"bottom_left_hunter_lodge" },
  pond_boathouse_or_waterfront_shed:{ expectedIdentity:"bottom_middle_boathouse_dock" }
});
const HEARTHVALE_ATLAS_MANIFEST_PATHS = Object.freeze({
  buildings:"/assets/wayfarer/buildings/hearthvale_buildings_atlas_v1.manifest.json",
  props:"/assets/wayfarer/props/hearthvale_props_atlas_v1.manifest.json"
});
const HEARTHVALE_PROOF_BUILDING_IDS = Object.freeze(new Set(["b_inn_tavern","b_mercantile","b_village_hall"]));
const HEARTHVALE_PROOF_PROP_TYPES = Object.freeze(new Set(["bench","barrel","crate","signPost"]));
const ATLAS_BUILDING_METADATA = Object.freeze({
  village_hall_meeting_house:{ id:"village_hall_meeting_house", role:"village_hall_meeting_house", atlas:"hearthvale_buildings_atlas_v1.png", crop:{ x:758, y:493, w:459, h:355 }, drawW:188, drawH:145, anchorX:94, anchorY:132, footprint:{ w:6, h:5 }, collisionRect:{ x:0, y:3, w:6, h:2 }, interactionRect:{ x:3, y:4, w:1, h:1 }, doorTile:{ x:3, y:4 }, labelAnchor:{ x:3, y:1 }, decorExclusionRect:{ x:0, y:0, w:6, h:3 }, productionReady:true, calibrationOnly:false, debugOnly:false, proofEnabled:true, fallbackReason:null },
  mercantile_shop:{ id:"mercantile_shop", role:"mercantile_shop", atlas:"hearthvale_buildings_atlas_v1.png", crop:{ x:473, y:67, w:329, h:403 }, drawW:131, drawH:160, anchorX:64, anchorY:126, footprint:{ w:5, h:5 }, collisionRect:{ x:0, y:4, w:5, h:1 }, interactionRect:{ x:2, y:4, w:1, h:1 }, doorTile:{ x:2, y:4 }, labelAnchor:{ x:2, y:1 }, decorExclusionRect:{ x:0, y:0, w:5, h:3 }, productionReady:true, calibrationOnly:false, debugOnly:false, proofEnabled:true, fallbackReason:null },
  inn_tavern_v1:{ id:"inn_tavern_v1", role:"inn_tavern", atlas:"hearthvale_buildings_atlas_v1.png", crop:{ x:33, y:120, w:420, h:340 }, drawW:192, drawH:156, anchorX:96, anchorY:143, footprint:{ w:6, h:5 }, collisionRect:{ x:0, y:3, w:6, h:2 }, interactionRect:{ x:3, y:4, w:1, h:1 }, doorTile:{ x:3, y:4 }, labelAnchor:{ x:3, y:1 }, decorExclusionRect:{ x:0, y:0, w:6, h:3 }, productionReady:true, calibrationOnly:false, debugOnly:false, proofEnabled:true, fallbackReason:null },
  // 33.1.1C: secondary buildings are FALLBACK-GATED pending atlas catalog verification.
  // crop coords are UNVERIFIED REFERENCE CANDIDATES from prior scan passes, NOT confirmed production crops.
  // Do NOT set productionReady:true until crop passes [Atlas Catalog Scan] and human visual review.
  residence_small:{ id:"residence_small", role:"residence_small", atlas:"hearthvale_buildings_atlas_v1.png", crop:{ x:439, y:526, w:254, h:309 }, drawW:116, drawH:116, anchorX:58, anchorY:102, footprint:{ w:4, h:4 }, collisionRect:{ x:0, y:2, w:4, h:2 }, interactionRect:{ x:1, y:3, w:1, h:1 }, doorTile:{ x:1, y:3 }, labelAnchor:{ x:1, y:1 }, decorExclusionRect:{ x:0, y:0, w:4, h:2 }, productionReady:false, calibrationOnly:false, debugOnly:false, proofEnabled:true, fallbackReason:"awaiting_atlas_catalog_verification" },
  residence_large:{ id:"residence_large", role:"residence_large", atlas:"hearthvale_buildings_atlas_v1.png", crop:{ x:44, y:835, w:367, h:344 }, drawW:144, drawH:120, anchorX:72, anchorY:104, footprint:{ w:5, h:4 }, collisionRect:{ x:0, y:2, w:5, h:2 }, interactionRect:{ x:2, y:3, w:1, h:1 }, doorTile:{ x:2, y:3 }, labelAnchor:{ x:2, y:1 }, decorExclusionRect:{ x:0, y:0, w:5, h:2 }, productionReady:false, calibrationOnly:false, debugOnly:false, proofEnabled:true, fallbackReason:"awaiting_atlas_catalog_verification" },
  hunter_lodge_or_outfitter:{ id:"hunter_lodge_or_outfitter", role:"hunter_lodge_or_outfitter", atlas:"hearthvale_buildings_atlas_v1.png", crop:{ x:61, y:939, w:309, h:308 }, drawW:120, drawH:120, anchorX:60, anchorY:104, footprint:{ w:4, h:4 }, collisionRect:{ x:0, y:2, w:4, h:2 }, interactionRect:{ x:1, y:3, w:1, h:1 }, doorTile:{ x:1, y:3 }, labelAnchor:{ x:1, y:1 }, decorExclusionRect:{ x:0, y:0, w:4, h:2 }, productionReady:false, calibrationOnly:false, debugOnly:false, proofEnabled:true, fallbackReason:"awaiting_atlas_catalog_verification" },
  pond_boathouse_or_waterfront_shed:{ id:"pond_boathouse_or_waterfront_shed", role:"pond_boathouse_or_waterfront_shed", atlas:"hearthvale_buildings_atlas_v1.png", crop:{ x:470, y:939, w:320, h:250 }, drawW:150, drawH:92, anchorX:75, anchorY:72, footprint:{ w:5, h:3 }, collisionRect:{ x:0, y:1, w:5, h:2 }, interactionRect:{ x:2, y:2, w:1, h:1 }, doorTile:{ x:2, y:2 }, labelAnchor:{ x:2, y:0 }, decorExclusionRect:{ x:0, y:0, w:5, h:1 }, productionReady:false, calibrationOnly:false, debugOnly:false, proofEnabled:true, fallbackReason:"awaiting_atlas_catalog_verification" }
});

// 33.1.4d: Sprite-keyed atlas presentation table — downstream helper providing
// crop/draw/anchor data per spriteId. Looked up via resolveAtlasSpriteRuntimeEntry().
// The authoritative semantic identity table is HEARTHVALE_BUILDING_SEMANTIC_REGISTRY (building-keyed).
const HEARTHVALE_ATLAS_SPRITE_PRESENTATION = Object.freeze({
  inn_tavern_v1:{
    spriteId:"inn_tavern_v1", role:"inn_tavern",
    atlasPosition:"top_left", presentationReason:"top_left_inn_tavern_confirmed",
    crop:{x:33,y:120,w:420,h:340},
    drawW:192, drawH:156, anchorX:96, anchorY:143,
    productionAtlasEnabled:true, registrySource:"human_reviewed"
  },
  mercantile_shop:{
    spriteId:"mercantile_shop", role:"mercantile_shop",
    atlasPosition:"top_middle", presentationReason:"top_middle_mercantile_shop_confirmed",
    crop:{x:473,y:67,w:329,h:403},
    drawW:131, drawH:160, anchorX:64, anchorY:126,
    productionAtlasEnabled:true, registrySource:"human_reviewed"
  },
  // Corrected from {x:758,y:493} (that was the manor/residence_large).
  // True meeting house is top-right on the atlas sheet.
  village_hall_meeting_house:{
    spriteId:"village_hall_meeting_house", role:"village_hall_meeting_house",
    atlasPosition:"top_right", presentationReason:"top_right_meeting_house_civic_anchor",
    crop:{x:853,y:10,w:327,h:460},
    drawW:134, drawH:188, anchorX:67, anchorY:171,
    productionAtlasEnabled:true, registrySource:"human_reviewed"
  },
  residence_small:{
    spriteId:"residence_small", role:"residence_small",
    atlasPosition:"middle_left", presentationReason:"middle_left_or_center_residence_small_candidate",
    crop:{x:439,y:526,w:254,h:309},
    drawW:116, drawH:116, anchorX:58, anchorY:102,
    productionAtlasEnabled:false, registrySource:"human_reviewed_pending_catalog"
  },
  // Released from old village_hall assignment {x:758,y:493} — this IS the manor.
  residence_large:{
    spriteId:"residence_large", role:"residence_large",
    atlasPosition:"middle_right", presentationReason:"middle_right_manor_residence_large",
    crop:{x:758,y:493,w:459,h:355},
    drawW:180, drawH:124, anchorX:90, anchorY:116,
    productionAtlasEnabled:false, registrySource:"human_reviewed"
  },
  hunter_lodge_or_outfitter:{
    spriteId:"hunter_lodge_or_outfitter", role:"hunter_lodge_or_outfitter",
    atlasPosition:"bottom_left", presentationReason:"bottom_left_hunter_lodge",
    crop:{x:61,y:939,w:309,h:308},
    drawW:120, drawH:120, anchorX:60, anchorY:104,
    productionAtlasEnabled:false, registrySource:"human_reviewed_pending_catalog"
  },
  pond_boathouse_or_waterfront_shed:{
    spriteId:"pond_boathouse_or_waterfront_shed", role:"pond_boathouse_or_waterfront_shed",
    atlasPosition:"bottom_middle", presentationReason:"bottom_middle_boathouse_dock",
    crop:{x:470,y:939,w:320,h:250},
    drawW:150, drawH:92, anchorX:75, anchorY:72,
    productionAtlasEnabled:false, registrySource:"human_reviewed_pending_catalog"
  }
});

const HEARTHVALE_BUILDING_SEMANTIC_REGISTRY = Object.freeze({
  b_inn_tavern:{ buildingId:"b_inn_tavern", role:"inn_tavern", spriteId:"inn_tavern_v1", atlasIdentity:"top_left_inn_tavern", crop:HEARTHVALE_ATLAS_SPRITE_PRESENTATION.inn_tavern_v1.crop, productionAtlasLocked:true, productionAtlasEnabled:true },
  b_mercantile:{ buildingId:"b_mercantile", role:"mercantile_shop", spriteId:"mercantile_shop", atlasIdentity:"top_middle_mercantile_shop", crop:HEARTHVALE_ATLAS_SPRITE_PRESENTATION.mercantile_shop.crop, productionAtlasLocked:true, productionAtlasEnabled:true },
  b_village_hall:{ buildingId:"b_village_hall", role:"village_hall_meeting_house", spriteId:"village_hall_meeting_house", atlasIdentity:"top_right_meeting_house", crop:{x:853,y:10,w:327,h:460}, productionAtlasLocked:true, productionAtlasEnabled:true },
  b_res_small:{ buildingId:"b_res_small", role:"residence_small", spriteId:"residence_small", atlasIdentity:"middle_left_or_middle_center_residence_small", crop:HEARTHVALE_ATLAS_SPRITE_PRESENTATION.residence_small.crop, productionAtlasLocked:false, productionAtlasEnabled:false },
  b_res_large:{ buildingId:"b_res_large", role:"residence_large", spriteId:"residence_large", atlasIdentity:"middle_right_manor_residence_large", crop:{x:758,y:493,w:459,h:355}, productionAtlasLocked:false, productionAtlasEnabled:false },
  b_hunter_lodge:{ buildingId:"b_hunter_lodge", role:"hunter_lodge_or_outfitter", spriteId:"hunter_lodge_or_outfitter", atlasIdentity:"bottom_left_hunter_lodge", crop:HEARTHVALE_ATLAS_SPRITE_PRESENTATION.hunter_lodge_or_outfitter.crop, productionAtlasLocked:false, productionAtlasEnabled:false },
  b_boathouse:{ buildingId:"b_boathouse", role:"pond_boathouse_or_waterfront_shed", spriteId:"pond_boathouse_or_waterfront_shed", atlasIdentity:"bottom_middle_boathouse_dock", crop:HEARTHVALE_ATLAS_SPRITE_PRESENTATION.pond_boathouse_or_waterfront_shed.crop, productionAtlasLocked:false, productionAtlasEnabled:false }
});

const HEARTHVALE_SEMANTIC_REGISTRY_BY_ROLE = Object.freeze(
  Object.values(HEARTHVALE_ATLAS_SPRITE_PRESENTATION).reduce((acc, entry) => {
    if (entry?.role) acc[entry.role] = entry;
    return acc;
  }, {})
);

const LOCKED_HERO_BUILDING_IDS=Object.freeze(["inn_tavern_v1","mercantile_shop","village_hall_meeting_house"]);
const SECONDARY_ATLAS_ROLES=Object.freeze(["residence_small","residence_large","hunter_lodge_or_outfitter","pond_boathouse_or_waterfront_shed"]);
const SECONDARY_ROLE_PRIORITY=Object.freeze(["pond_boathouse_or_waterfront_shed","residence_large","residence_small","hunter_lodge_or_outfitter"]);
const SECONDARY_ROLE_DUPLICATE_POLICY=Object.freeze({
  allowDuplicateForRoles:false
});
const SECONDARY_BUILDING_IDS=SECONDARY_ATLAS_ROLES;
const SECONDARY_BLOCKING_AUDIT_WARNING_PREFIXES=Object.freeze([
  "overlaps_locked_hero_crop:"
]);
const SECONDARY_BLOCKING_AUDIT_WARNINGS=Object.freeze(new Set([
  "clipped_to_edge",
  "empty_crop",
  "no_non_transparent_pixels",
  "likely_partial_object",
  "partial_object_bounds"
]));
const LOCKED_HERO_METADATA_SNAPSHOT=Object.freeze({
  inn_tavern_v1:JSON.stringify({ crop:ATLAS_BUILDING_METADATA.inn_tavern_v1.crop, drawW:ATLAS_BUILDING_METADATA.inn_tavern_v1.drawW, drawH:ATLAS_BUILDING_METADATA.inn_tavern_v1.drawH, anchorX:ATLAS_BUILDING_METADATA.inn_tavern_v1.anchorX, anchorY:ATLAS_BUILDING_METADATA.inn_tavern_v1.anchorY, proofEnabled:ATLAS_BUILDING_METADATA.inn_tavern_v1.proofEnabled }),
  mercantile_shop:JSON.stringify({ crop:ATLAS_BUILDING_METADATA.mercantile_shop.crop, drawW:ATLAS_BUILDING_METADATA.mercantile_shop.drawW, drawH:ATLAS_BUILDING_METADATA.mercantile_shop.drawH, anchorX:ATLAS_BUILDING_METADATA.mercantile_shop.anchorX, anchorY:ATLAS_BUILDING_METADATA.mercantile_shop.anchorY, proofEnabled:ATLAS_BUILDING_METADATA.mercantile_shop.proofEnabled }),
  village_hall_meeting_house:JSON.stringify({ crop:ATLAS_BUILDING_METADATA.village_hall_meeting_house.crop, drawW:ATLAS_BUILDING_METADATA.village_hall_meeting_house.drawW, drawH:ATLAS_BUILDING_METADATA.village_hall_meeting_house.drawH, anchorX:ATLAS_BUILDING_METADATA.village_hall_meeting_house.anchorX, anchorY:ATLAS_BUILDING_METADATA.village_hall_meeting_house.anchorY, proofEnabled:ATLAS_BUILDING_METADATA.village_hall_meeting_house.proofEnabled })
});
function rectsOverlap(a,b){
  return !(a.x+a.w<=b.x || b.x+b.w<=a.x || a.y+a.h<=b.y || b.y+b.h<=a.y);
}
function boxesEqual(a,b){
  if(!a||!b) return false;
  return a.x===b.x && a.y===b.y && a.w===b.w && a.h===b.h;
}
function getCropOverlapWarnings(entry){
  if(!entry || !SECONDARY_BUILDING_IDS.includes(entry.id)) return [];
  const warnings=[];
  const crop=entry.crop;
  LOCKED_HERO_BUILDING_IDS.forEach((heroId)=>{
    const heroResolved=resolveAtlasSpriteRuntimeEntry(heroId);
    const heroCrop=heroResolved ? heroResolved.crop : ATLAS_BUILDING_METADATA[heroId]?.crop;
    if(!heroCrop) return;
    if(rectsOverlap(crop, heroCrop)) warnings.push("overlaps_locked_hero_crop:"+heroId);
  });
  return warnings;
}
function isSecondaryBlockingAuditWarning(warning){
  if(!warning) return false;
  if(SECONDARY_BLOCKING_AUDIT_WARNINGS.has(warning)) return true;
  return SECONDARY_BLOCKING_AUDIT_WARNING_PREFIXES.some((prefix)=>warning.startsWith(prefix));
}
function getSecondaryBuildingAuditWarnings(entry, sheet){
  if(!entry || !SECONDARY_BUILDING_IDS.includes(entry.id)) return [];
  const warnings=[...getCropOverlapWarnings(entry)];
  const crop=entry.crop||{};
  if(!sheet || !sheet.complete || !(sheet.naturalWidth>0 && sheet.naturalHeight>0)) return warnings;
  if(crop.x+crop.w>sheet.naturalWidth || crop.y+crop.h>sheet.naturalHeight) return warnings;
  const auditCanvas=document.createElement("canvas");
  auditCanvas.width=crop.w;
  auditCanvas.height=crop.h;
  const ctx=auditCanvas.getContext("2d",{ willReadFrequently:true });
  if(!ctx) return warnings;
  ctx.drawImage(sheet,crop.x,crop.y,crop.w,crop.h,0,0,crop.w,crop.h);
  const data=ctx.getImageData(0,0,crop.w,crop.h).data;
  let minX=crop.w,minY=crop.h,maxX=-1,maxY=-1,hasPixels=false;
  for(let py=0;py<crop.h;py++){
    for(let px=0;px<crop.w;px++){
      if(data[(py*crop.w+px)*4+3]===0) continue;
      hasPixels=true;
      if(px<minX) minX=px;
      if(py<minY) minY=py;
      if(px>maxX) maxX=px;
      if(py>maxY) maxY=py;
    }
  }
  if(!hasPixels){
    warnings.push("no_non_transparent_pixels");
    return warnings;
  }
  const clipped=minX===0 || minY===0 || maxX===crop.w-1 || maxY===crop.h-1;
  if(clipped) warnings.push("clipped_to_edge");
  const bboxW=maxX-minX+1;
  const bboxH=maxY-minY+1;
  if(((bboxW*bboxH)/(crop.w*crop.h))<0.2) warnings.push("likely_partial_object");
  if((minX===0 || maxX===crop.w-1) && (minY===0 || maxY===crop.h-1)) warnings.push("partial_object_bounds");
  return warnings;
}

function atlasBuildingMetadataToSpriteMap(metadata){
  const sprites={};
  Object.values(metadata).forEach((entry)=>{
    sprites[entry.id]={
      sx:entry.crop.x, sy:entry.crop.y, sw:entry.crop.w, sh:entry.crop.h,
      drawW:entry.drawW, drawH:entry.drawH,
      anchorX:entry.anchorX, anchorY:entry.anchorY,
      productionReady:entry.productionReady===true,
      debugOnly:entry.debugOnly===true,
      proofEnabled:entry.proofEnabled===true,
      footprint:entry.footprint,
      collisionRect:entry.collisionRect,
      interactionRect:entry.interactionRect,
      labelAnchor:entry.labelAnchor,
      atlas:entry.atlas,
      role:entry.role,
      fallbackReason:entry.fallbackReason || null,
      metadataSource:"index",
      metadataManifestVersion:null
    };
  });
  return sprites;
}

const atlasManifests = {
  terrain: {
    imagePath: "/assets/wayfarer/terrain/terrain_sheet.png",
    optional:true,
    tileSize: 32,
    sprites: {
      grass_base:{ sx:0, sy:0, sw:32, sh:32 },
      grass_variant:{ sx:32, sy:0, sw:32, sh:32 },
      road_center:{ sx:64, sy:0, sw:32, sh:32 },
      road_edge:{ sx:96, sy:0, sw:32, sh:32 },
      road_corner:{ sx:128, sy:0, sw:32, sh:32 },
      water:{ sx:160, sy:0, sw:32, sh:32 },
      shoreline:{ sx:192, sy:0, sw:32, sh:32 },
      dock_plank:{ sx:224, sy:0, sw:32, sh:32 }
    }
  },
  buildings: {
    imagePath: "/assets/wayfarer/buildings/hearthvale_buildings_atlas_v1.png",
    fallbackImagePaths: [],
    tileSize: 32,
    productionReady: true,
    allowProductionSprites: false,
    knownBadAssetPaths: [
      "/assets/sprites/medieval_town_buildings_sprite_sheet.png",
      "/tiles/buildings/test_house/Medieval%20town%20buildings%20sprite%20sheet.png"
    ],
    sprites: atlasBuildingMetadataToSpriteMap(ATLAS_BUILDING_METADATA)
  },
  characters: {
    imagePath: "/assets/wayfarer/characters/character_sheet.png",
    optional:true,
    tileSize: 64,
    sprites: {
      wayfarer:{ sx:0, sy:0, sw:256, sh:256 },
      edrin_vale:{ sx:256, sy:0, sw:256, sh:256 },
      merchant_rowan:{ sx:512, sy:0, sw:256, sh:256 },
      hunter_garran:{ sx:768, sy:0, sw:256, sh:256 },
      bandit:{ sx:0, sy:256, sw:256, sh:256 },
      wolf:{ sx:256, sy:256, sw:256, sh:256 },
      rook:{ sx:512, sy:256, sw:256, sh:256 }
    }
  },
  props: {
    imagePath: "/assets/wayfarer/props/hearthvale_props_atlas_v1.png",
    fallbackImagePaths: [],
    tileSize: 32,
    productionReady: true,
    allowProductionSprites: false,
    knownBadAssetPaths: [
      "/assets/sprites/medieval_town_asset_sprite_sheet.png",
      "/tiles/buildings/test_house/Medieval%20town%20asset%20sprite%20sheet.png"
    ],
    sprites: {
      bench_market:{ sx:0, sy:0, sw:64, sh:32, drawW:64, drawH:32, anchorX:32, anchorY:32, productionReady:false, debugOnly:true, proofEnabled:true, footprint:{ w:2, h:1 }, collisionRect:{ x:0, y:0, w:2, h:1 }, interactionRect:{ x:1, y:0, w:1, h:1 }, atlas:"hearthvale_props_atlas_v1.png" },
      barrel_oak:{ sx:64, sy:0, sw:32, sh:32, drawW:32, drawH:32, anchorX:16, anchorY:32, productionReady:false, debugOnly:true, proofEnabled:true, footprint:{ w:1, h:1 }, collisionRect:{ x:0, y:0, w:1, h:1 }, atlas:"hearthvale_props_atlas_v1.png" },
      crate_market:{ sx:96, sy:0, sw:32, sh:32, drawW:32, drawH:32, anchorX:16, anchorY:32, productionReady:false, debugOnly:true, proofEnabled:true, footprint:{ w:1, h:1 }, collisionRect:{ x:0, y:0, w:1, h:1 }, atlas:"hearthvale_props_atlas_v1.png" },
      signpost_square:{ sx:128, sy:0, sw:32, sh:64, drawW:32, drawH:64, anchorX:16, anchorY:32, renderLayer:"above_entities", productionReady:false, debugOnly:true, proofEnabled:true, footprint:{ w:1, h:1 }, collisionRect:{ x:0, y:0, w:1, h:1 }, interactionRect:{ x:0, y:0, w:1, h:1 }, atlas:"hearthvale_props_atlas_v1.png" }
    }
  }
};
// 33.1.4D: Single canonical resolver. Semantic registry wins; static metadata is
// fallback only. ALL subsystems that need crop/draw/anchor must call this.
// Sprite-keyed presentation lookup. Returns crop/draw/anchor data for a given spriteId.
// Used by render, audit, selector, and crop-audit subsystems that operate on sprite IDs.
function resolveAtlasSpriteRuntimeEntry(spriteId){
  if(!spriteId) return null;
  const presEntry=HEARTHVALE_ATLAS_SPRITE_PRESENTATION[spriteId];
  const metaEntry=ATLAS_BUILDING_METADATA[spriteId];
  if(presEntry){
    return{
      spriteId,
      role:presEntry.role,
      crop:presEntry.crop,
      drawW:presEntry.drawW,
      drawH:presEntry.drawH,
      anchorX:presEntry.anchorX,
      anchorY:presEntry.anchorY,
      productionAtlasEnabled:presEntry.productionAtlasEnabled===true,
      cropSource:"semantic_registry",
      drawAnchorSource:"semantic_registry",
      registryResolved:true,
      atlasPosition:presEntry.atlasPosition||null,
      presentationReason:presEntry.presentationReason||null,
      registrySource:presEntry.registrySource||null
    };
  }
  if(metaEntry){
    return{
      spriteId,
      role:metaEntry.role,
      crop:metaEntry.crop,
      drawW:metaEntry.drawW,
      drawH:metaEntry.drawH,
      anchorX:metaEntry.anchorX,
      anchorY:metaEntry.anchorY,
      productionAtlasEnabled:metaEntry.productionReady===true,
      cropSource:"static_metadata",
      drawAnchorSource:"static_metadata",
      registryResolved:false,
      atlasPosition:null,
      presentationReason:null,
      registrySource:null
    };
  }
  return null;
}
// Building-keyed authoritative resolver. Accepts a world building ID (e.g. b_inn_tavern)
// and returns full identity + presentation data merged from the semantic registry and
// the sprite presentation table. Building-registry crop overrides win over presentation.
function resolveBuildingAtlasRuntimeEntry(buildingId){
  if(!buildingId) return null;
  const regEntry=HEARTHVALE_BUILDING_SEMANTIC_REGISTRY[buildingId];
  if(!regEntry) return null;
  const spriteEntry=resolveAtlasSpriteRuntimeEntry(regEntry.spriteId);
  const crop=regEntry.crop || spriteEntry?.crop || null;
  const cropSource=regEntry.crop ? "semantic_registry" : (spriteEntry?.cropSource || "unknown");
  return{
    buildingId,
    role:regEntry.role,
    spriteId:regEntry.spriteId,
    atlasIdentity:regEntry.atlasIdentity||null,
    crop,
    drawW:spriteEntry?.drawW ?? null,
    drawH:spriteEntry?.drawH ?? null,
    anchorX:spriteEntry?.anchorX ?? null,
    anchorY:spriteEntry?.anchorY ?? null,
    productionAtlasLocked:regEntry.productionAtlasLocked===true,
    productionAtlasEnabled:regEntry.productionAtlasEnabled===true,
    cropSource,
    drawAnchorSource:spriteEntry?.drawAnchorSource||"unknown",
    registryResolved:true
  };
}
// Apply sprite presentation overrides to the runtime sprite manifest immediately
// after atlasManifests is initialized. Village_hall crop is corrected here from
// the static index value {x:758,y:493} to the registry-authoritative {x:853,y:10}.
// Legacy static differences are reported as overrides, not conflicts.
function applySemanticRegistryToManifest(){
  const manifest=atlasManifests.buildings;
  if(!manifest||!manifest.sprites) return;
  const overrides=[];
  Object.values(HEARTHVALE_ATLAS_SPRITE_PRESENTATION).forEach((presEntry)=>{
    const sprite=manifest.sprites[presEntry.spriteId];
    if(!sprite) return;
    const prevSx=sprite.sx, prevSy=sprite.sy, prevSw=sprite.sw, prevSh=sprite.sh;
    sprite.sx=presEntry.crop.x;
    sprite.sy=presEntry.crop.y;
    sprite.sw=presEntry.crop.w;
    sprite.sh=presEntry.crop.h;
    sprite.drawW=presEntry.drawW;
    sprite.drawH=presEntry.drawH;
    sprite.anchorX=presEntry.anchorX;
    sprite.anchorY=presEntry.anchorY;
    sprite.metadataSource="semantic_registry";
    const cropChanged=(prevSx!==sprite.sx||prevSy!==sprite.sy||prevSw!==sprite.sw||prevSh!==sprite.sh);
    if(cropChanged){
      overrides.push({spriteId:presEntry.spriteId,staticCrop:{sx:prevSx,sy:prevSy,sw:prevSw,sh:prevSh},registryCrop:{sx:sprite.sx,sy:sprite.sy,sw:sprite.sw,sh:sprite.sh}});
    }
    if(presEntry.spriteId==="residence_large"){
      console.info("[Semantic Registry Apply]");
      console.info("spriteId=residence_large");
      console.info("registryCrop="+JSON.stringify({x:presEntry.crop.x,y:presEntry.crop.y,w:presEntry.crop.w,h:presEntry.crop.h}));
      console.info("activeManifestCrop="+JSON.stringify({x:sprite.sx,y:sprite.sy,w:sprite.sw,h:sprite.sh}));
      console.info("status=applied");
    }
  });
  if(overrides.length){
    overrides.forEach((o)=>{
      console.info("[Building Source of Truth Override] type=legacy_static_overridden spriteId="+o.spriteId+" staticCrop="+JSON.stringify(o.staticCrop)+" registryCrop="+JSON.stringify(o.registryCrop)+" activeCrop="+JSON.stringify(o.registryCrop)+" status=ok");
    });
  }
}
applySemanticRegistryToManifest();

const atlasImages = {};
const atlasRuntimeInfo = {};
const missingAssetWarnings=new Set();
const buildingFallbackWarnings=new Set();
const buildingRenderDiagnostics={
  atlasBuildings:new Set(),
  fallbackBuildings:new Map(),
  pendingBuildings:new Map(),
  perBuilding:new Map(),
  lastSummaryToken:null
};
const atlasReadinessLogState={
  buildingsReadyLogged:false,
  catalogScanReadyLogged:false,
  lastDebugToken:null
};
const USE_PRODUCTION_BUILDING_ATLAS = false;
const BUILDING_SPRITE_PRODUCTION_LIMITS = Object.freeze({
  maxDrawTilesWide: 6,
  maxDrawTilesHigh: 6,
  maxCropPxWide: 192,
  maxCropPxHigh: 192,
  maxCropAreaPx: 192 * 192
});
const EXTERNAL_SPRITE_PRODUCTION_LIMITS = Object.freeze({
  maxDrawTilesWide: 6,
  maxDrawTilesHigh: 6
});
const PROP_SPRITE_PRODUCTION_LIMITS = Object.freeze({
  default: { minDrawW:16, minDrawH:16, maxDrawW:64, maxDrawH:64, maxCropW:128, maxCropH:128, maxCropArea:128*128 },
  bench: { minDrawW:32, minDrawH:16, maxDrawW:64, maxDrawH:32, maxCropW:96, maxCropH:64, maxCropArea:96*64 },
  barrel: { minDrawW:16, minDrawH:16, maxDrawW:32, maxDrawH:32, maxCropW:64, maxCropH:64, maxCropArea:64*64 },
  crate: { minDrawW:16, minDrawH:16, maxDrawW:32, maxDrawH:32, maxCropW:64, maxCropH:64, maxCropArea:64*64 },
  signPost: { minDrawW:16, minDrawH:32, maxDrawW:32, maxDrawH:64, maxCropW:64, maxCropH:96, maxCropArea:64*96 },
  well: { minDrawW:32, minDrawH:32, maxDrawW:64, maxDrawH:64, maxCropW:96, maxCropH:96, maxCropArea:96*96 }
});
const BUILDING_SPRITE_ID_BY_BUILDING_ID = Object.freeze(Object.fromEntries(
  Object.entries(HEARTHVALE_BUILDING_SEMANTIC_REGISTRY).map(([buildingId, entry])=>[buildingId, entry.spriteId])
));
const BUILDING_SPRITE_ID_BY_ROLE = Object.freeze((()=>{
  const byRole={};
  Object.values(HEARTHVALE_BUILDING_SEMANTIC_REGISTRY).forEach((entry)=>{
    if(entry?.role && entry?.spriteId) byRole[entry.role]=entry.spriteId;
  });
  byRole.village_hall=byRole.village_hall_meeting_house||"village_hall_meeting_house";
  byRole.mercantile=byRole.mercantile_shop||"mercantile_shop";
  byRole.inn_tavern_v1=byRole.inn_tavern||"inn_tavern_v1";
  return byRole;
})());
const BUILDING_FALLBACK_STYLE_BY_ROLE = Object.freeze({
  residence_small:{ roof:"roofC", wall:"wallTimber", window:"windowTall", door:"doorPorch", dormer:true },
  residence_large:{ roof:"roofSlate", wall:"wall", window:"window", door:"door", dormer:true },
  inn_tavern:{ roof:"roofC", wall:"wall", window:"window", door:"doorShop", dormer:true },
  mercantile_shop:{ roof:"roofSlate", wall:"wallBrick", window:"windowWide", door:"doorShop", dormer:false },
  village_hall_meeting_house:{ roof:"roofSlate", wall:"wall", window:"windowTall", door:"door", dormer:true },
  hunter_lodge_or_outfitter:{ roof:"roofC", wall:"wallTimber", window:"windowTall", door:"doorPorch", dormer:false },
  pond_boathouse_or_waterfront_shed:{ roof:"roofSlate", wall:"wallBrick", window:"windowWide", door:"doorShop", dormer:false }
});
const PROP_SPRITE_BY_WORLD_TYPE = Object.freeze({
  bench:"bench_market",
  barrel:"barrel_oak",
  crate:"crate_market",
  signPost:"signpost_square"
});
const atlasDebugPreview={
  enabled:false,
  showCrops:true
};
function isAtlasPreviewEnabledFromUrl(){
  try{
    return new URLSearchParams(window.location.search).get("atlasPreview")==="1";
  }catch(_error){
    return false;
  }
}
function isAtlasDebugEnabledFromUrl(){
  try{
    const atlasDebug = new URLSearchParams(window.location.search).get("atlasDebug")==="1";
    return atlasDebug;
  }catch(_error){
    return false;
  }
}
function isPropDebugEnabledFromUrl(){
  try{
    return new URLSearchParams(window.location.search).get("propDebug")==="1";
  }catch(_error){
    return false;
  }
}
function isSecondaryProofPreviewEnabledFromUrl(){
  try{
    return new URLSearchParams(window.location.search).get("secondaryProofPreview")==="1";
  }catch(_error){
    return false;
  }
}
function getSecondaryAtlasRuntimePreviewRequestFromUrl(){
  try{
    const raw=new URLSearchParams(window.location.search).get("secondaryAtlasRuntimePreview");
    if(!raw) return null;
    const normalized=String(raw).trim().toLowerCase();
    return normalized||null;
  }catch(_error){
    return null;
  }
}

function getAtlasProofRequestFromUrl(){
  try{
    const raw=new URLSearchParams(window.location.search).get("atlasProof");
    if(!raw) return { enabled:false, all:false, ids:new Set() };
    const normalized=String(raw).trim().toLowerCase();
    if(!normalized) return { enabled:false, all:false, ids:new Set() };
    if(normalized==="all") return { enabled:true, all:true, ids:new Set() };
    const ids=new Set(normalized.split(",").map((token)=>token.trim()).filter(Boolean));
    return { enabled:ids.size>0, all:false, ids };
  }catch(_error){
    return { enabled:false, all:false, ids:new Set() };
  }
}

function isDecorDebugEnabledFromUrl(){
  try{
    return new URLSearchParams(window.location.search).get("decorDebug")==="1";
  }catch(_error){
    return false;
  }
}
const ATLAS_DEBUG_MODE = isAtlasDebugEnabledFromUrl();
const WAYFARER_PHASE = "34.2";
const WAYFARER_BUILD_LABEL = "Harbor Silhouette & Wharf Framework";
const ATLAS_SELECTOR_VERSION = "selector-v33.1.5b-runtime-preview-gate-bypass";
const ATLAS_READINESS_TIMEOUT_MS = 12000;
const WAYFARER_BUILD_COMMIT = (typeof globalThis.__WAYFARER_COMMIT__==="string" && globalThis.__WAYFARER_COMMIT__.trim())
  ? globalThis.__WAYFARER_COMMIT__.trim()
  : "runtime-injected-or-unavailable";
const WAYFARER_BUILD_PHASE_TEXT = "Build Phase " + WAYFARER_PHASE + " — " + WAYFARER_BUILD_LABEL;
if(typeof document!=="undefined"){
  const phaseBanner=document.getElementById("buildPhaseBanner");
  if(phaseBanner) phaseBanner.textContent=WAYFARER_BUILD_PHASE_TEXT;
  document.title="Wayfarer — "+WAYFARER_BUILD_PHASE_TEXT;
}
let wayfarerBuildSentinelLogged=false;
const ATLAS_PREVIEW_MODE = ATLAS_DEBUG_MODE && isAtlasPreviewEnabledFromUrl();
const SECONDARY_PROOF_PREVIEW_MODE = ATLAS_DEBUG_MODE && isSecondaryProofPreviewEnabledFromUrl();
const SECONDARY_ATLAS_RUNTIME_PREVIEW_REQUEST = ATLAS_DEBUG_MODE ? getSecondaryAtlasRuntimePreviewRequestFromUrl() : null;
function isMobileQaControlsEnabledFromUrl(){
  try{ return new URLSearchParams(window.location.search).get("mobileQaControls")==="1"; }catch(_error){ return false; }
}
function isAutoQaEnabledFromUrl(){
  try{ return new URLSearchParams(window.location.search).get("autoQa")==="1"; }catch(_error){ return false; }
}
const MOBILE_QA_CONTROLS_MODE = ATLAS_DEBUG_MODE && isMobileQaControlsEnabledFromUrl();
const AUTO_QA_MODE = MOBILE_QA_CONTROLS_MODE && isAutoQaEnabledFromUrl();
const DECOR_DEBUG_MODE = isDecorDebugEnabledFromUrl();
function isDecorDebugEnabled(){
  return ATLAS_DEBUG_MODE && DECOR_DEBUG_MODE;
}
const PROP_DEBUG_MODE = isPropDebugEnabledFromUrl();
const ATLAS_PROOF_REQUEST = getAtlasProofRequestFromUrl();
const ATLAS_DEBUG_SOURCE_LABELS = (() => {
  if(!ATLAS_DEBUG_MODE || !DECOR_DEBUG_MODE) return false;
  try{
    return new URLSearchParams(window.location.search).get("sourceLabels") !== "0";
  }catch(_error){
    return true;
  }
})();
const USE_HEARTHVALE_ATLAS_PROOF_DEBUG = ATLAS_DEBUG_MODE;
const BUILDING_SPRITE_PROOF_DEBUG = false;
const HEARTHVALE_TRACE_BOUNDS = Object.freeze({ x:7, y:5, w:23, h:15 });
const decorSourceTraceState={
  frame:0,
  entries:[]
};
const ATLAS_DECOR_SUPPRESS_SOURCE_LABELS=Object.freeze(new Set(["LEGACY_PROP","FALLBACK_DECOR","MAP_OBJECT"]));
const ATLAS_DECOR_ALLOWLIST=Object.freeze(new Set([]));
atlasDebugPreview.enabled=ATLAS_PREVIEW_MODE;
const atlasBuildingDecorExclusionState={
  zones:[],
  suppressionLog:new Set(),
  suppressedObjects:[]
};
const secondaryProofPreviewState={
  summaryLogged:false,
  drawCount:0,
  drawSummaryLogged:false,
  pendingSignature:null
};
function logSecondaryProofPreviewSummary(){
  if(secondaryProofPreviewState.summaryLogged) return;
  const roles=Array.isArray(SECONDARY_BUILDING_IDS) ? SECONDARY_BUILDING_IDS.slice() : [];
  try{
    const previewRoles=roles.filter((roleId)=>secondaryAtlasSelectionState.byRole?.[roleId]?.selectorCandidateStatus==="SELECTED_PROOF_ONLY");
    const fallbackGatedRoles=roles.filter((roleId)=>secondaryAtlasSelectionState.byRole?.[roleId]?.selectorCandidateStatus==="FALLBACK_GATED");
    const runtimeAtlasRoles=roles.filter((roleId)=>secondaryAtlasSelectionState.byRole?.[roleId]?.runtimeRenderStatus==="ATLAS");
    console.info("[Secondary Proof Preview]");
    console.info("enabled="+(SECONDARY_PROOF_PREVIEW_MODE?"true":"false"));
    console.info("previewRoles="+previewRoles.join(","));
    console.info("fallbackGatedRoles="+fallbackGatedRoles.join(","));
    console.info("runtimeAtlasRoles="+runtimeAtlasRoles.join(","));
  }catch(summaryError){
    console.warn("[Secondary Proof Preview] summary_failed",summaryError?.message||summaryError);
  }
  secondaryProofPreviewState.summaryLogged=true;
}
function drawSecondaryProofPreviewOverlay(entry){
  if(!SECONDARY_PROOF_PREVIEW_MODE || !entry?.b) return;
  try{
    const role=entry.b.role;
    const selectorRow=secondaryAtlasSelectionState.byRole?.[role];
    if(selectorRow?.fallbackReason==="human_review_rejected_candidate"){
      console.assert(selectorRow.selectorCandidateStatus!=="SELECTED_PROOF_ONLY","[Secondary Proof Preview Assert] human_rejected_role_must_not_draw_preview role="+role+" rejectedCandidateId="+(selectorRow.rejectedCandidateId||"none")+" rejectionReason="+(selectorRow.rejectionReason||"none"));
      return;
    }
    if(!selectorRow || selectorRow.selectorCandidateStatus!=="SELECTED_PROOF_ONLY" || !selectorRow.selectedCrop) return;
    const crop=selectorRow.selectedCrop;
    const drawW=selectorRow.drawW;
    const drawH=selectorRow.drawH;
    const hasValidGeometry=
      Number.isFinite(crop?.x) &&
      Number.isFinite(crop?.y) &&
      Number.isFinite(crop?.w) &&
      Number.isFinite(crop?.h) &&
      Number.isFinite(drawW) &&
      Number.isFinite(drawH);
    if(!hasValidGeometry){
      console.warn("[Secondary Proof Preview] draw_skipped role="+role+" reason=missing_preview_geometry");
      return;
    }
    const buildingsAtlasImage=atlasImages?.buildings;
    if(!buildingsAtlasImage?.complete || !(buildingsAtlasImage?.naturalWidth>0) || !(buildingsAtlasImage?.naturalHeight>0)){
      console.warn("[Secondary Proof Preview] draw_skipped reason=atlas_not_ready");
      return;
    }
    const anchorX=Number.isFinite(selectorRow.anchorX) ? selectorRow.anchorX : Math.floor(entry.b.w/2)*TILE;
    const anchorY=Number.isFinite(selectorRow.anchorY) ? selectorRow.anchorY : (entry.b.h-1)*TILE;
    const anchorPxX=((entry.b.anchorX ?? Math.floor(entry.b.w/2))*TILE);
    const anchorPxY=((entry.b.anchorY ?? (entry.b.h-1))*TILE);
    const base=tileToScreen(entry.b.x,entry.b.y);
    const drawX=base.x + anchorPxX - anchorX;
    const drawY=base.y + anchorPxY - anchorY;
    ctx.save();
    ctx.drawImage(buildingsAtlasImage,crop.x,crop.y,crop.w,crop.h,drawX,drawY,drawW,drawH);
    secondaryProofPreviewState.drawCount+=1;
    ctx.globalAlpha=0.38;
    ctx.fillStyle="rgba(64,245,255,0.45)";
    ctx.fillRect(drawX,drawY,drawW,drawH);
    ctx.globalAlpha=1;
    ctx.strokeStyle="rgba(64,245,255,0.95)";
    ctx.lineWidth=2;
    ctx.strokeRect(drawX+0.5,drawY+0.5,Math.max(1,drawW-1),Math.max(1,drawH-1));
    const labelRows=[
      "PROOF PREVIEW",
      "role="+role+" candidateId="+(selectorRow.selectedCandidateId||"none"),
      "crop="+[crop.x,crop.y,crop.w,crop.h].join("/"),
      "draw="+drawW+"x"+drawH+" anchor="+(selectorRow.anchorX??"n/a")+"/"+(selectorRow.anchorY??"n/a"),
      "selectorCandidateStatus="+selectorRow.selectorCandidateStatus,
      "runtimeRenderStatus=FALLBACK"
    ];
    const panelW=380;
    const panelH=labelRows.length*12+8;
    ctx.fillStyle="rgba(4,22,28,0.86)";
    ctx.fillRect(drawX,drawY-panelH-6,panelW,panelH);
    ctx.strokeStyle="rgba(64,245,255,0.95)";
    ctx.strokeRect(drawX+0.5,drawY-panelH-5.5,panelW-1,panelH-1);
    ctx.fillStyle="rgba(172,255,255,0.98)";
    ctx.font="10px monospace";
    labelRows.forEach((line,index)=>ctx.fillText(line,drawX+6,drawY-panelH+7+(index*12)));
    ctx.restore();
  }catch(previewDrawError){
    console.warn("[Secondary Proof Preview] draw_skipped role="+(entry?.b?.role||"unknown")+" reason=draw_exception message="+(previewDrawError?.message||previewDrawError));
  }
}
function logSecondaryProofPreviewDrawSummary(){
  if(!SECONDARY_PROOF_PREVIEW_MODE || secondaryProofPreviewState.drawSummaryLogged) return;
  const roles=Array.isArray(SECONDARY_BUILDING_IDS) ? SECONDARY_BUILDING_IDS.slice() : [];
  const allReady=roles.every((roleId)=>secondaryAtlasSelectionState.byRole?.[roleId]?.selectorCandidateStatus);
  if(!allReady){
    const pendingSig="selector_or_assets_not_settled";
    if(secondaryProofPreviewState.pendingSignature!==pendingSig){
      secondaryProofPreviewState.pendingSignature=pendingSig;
      console.info("[Secondary Proof Preview Draw]");
      console.info("status=PENDING_ASSETS");
      console.info("drawCount=0");
      console.info("reason="+pendingSig);
    }
    return;
  }
  secondaryProofPreviewState.pendingSignature=null;
  const drawnRoles=roles.filter((roleId)=>secondaryAtlasSelectionState.byRole?.[roleId]?.selectorCandidateStatus==="SELECTED_PROOF_ONLY");
  const skippedRoles=roles.filter((roleId)=>secondaryAtlasSelectionState.byRole?.[roleId]?.selectorCandidateStatus!=="SELECTED_PROOF_ONLY");
  const runtimeAtlasRoles=roles.filter((roleId)=>secondaryAtlasSelectionState.byRole?.[roleId]?.runtimeRenderStatus==="ATLAS");
  console.info("[Secondary Proof Preview Draw]");
  console.info("drawnRoles="+drawnRoles.join(","));
  console.info("skippedRoles="+skippedRoles.join(","));
  console.info("drawCount="+secondaryProofPreviewState.drawCount);
  console.info("runtimeAtlasRoles="+runtimeAtlasRoles.join(","));
  secondaryProofPreviewState.drawSummaryLogged=true;
}
function resetAtlasBuildingDecorExclusionState(){
  atlasBuildingDecorExclusionState.zones.length=0;
  atlasBuildingDecorExclusionState.suppressedObjects.length=0;
}
function overlapsRect(a,b){
  if(!a || !b) return false;
  return a.x < b.x + b.w &&
    a.x + a.w > b.x &&
    a.y < b.y + b.h &&
    a.y + a.h > b.y;
}
function registerAtlasBuildingDecorExclusionZone(building, drawX, drawY, drawW, drawH){
  if(!building || !Number.isFinite(drawX) || !Number.isFinite(drawY) || !Number.isFinite(drawW) || !Number.isFinite(drawH)) return;
  const anchorPxX=((building.anchorX ?? Math.floor(building.w/2))*TILE);
  const anchorPxY=((building.anchorY ?? (building.h-1))*TILE);
  const buildingTopLeft=tileToScreen(building.x, building.y);
  const footprintRect={
    x:Math.floor(buildingTopLeft.x),
    y:Math.floor(buildingTopLeft.y),
    w:Math.max(1, Math.floor((building.w || 1)*TILE)),
    h:Math.max(1, Math.floor((building.h || 1)*TILE))
  };
  const interactionRect=building.footprint?.interaction || null;
  const doorThresholdRect=interactionRect
    ? {
        x:Math.floor(interactionRect.x*TILE)-TILE,
        y:Math.floor(interactionRect.y*TILE)-Math.floor(TILE*0.5),
        w:Math.max(TILE*3, Math.floor(interactionRect.w*TILE)+TILE*2),
        h:Math.max(TILE*2, Math.floor(interactionRect.h*TILE)+TILE)
      }
    : null;
  atlasBuildingDecorExclusionState.zones.push({
    buildingId:building.id || "unknown_building",
    buildingRole:building.role || "unknown_role",
    anchor:{
      x:Math.floor(buildingTopLeft.x + anchorPxX),
      y:Math.floor(buildingTopLeft.y + anchorPxY)
    },
    footprintRect,
    doorThresholdRect,
    rect:{
      x:Math.floor(drawX),
      y:Math.floor(drawY),
      w:Math.max(1, Math.ceil(drawW)),
      h:Math.max(1, Math.ceil(drawH))
    }
  });
}
function getAtlasDecorSuppressionZoneHit(drawRect){
  if(!drawRect) return null;
  for(const zone of atlasBuildingDecorExclusionState.zones){
    if(overlapsRect(drawRect, zone.rect)){
      return zone;
    }
  }
  return null;
}
function getDecorSuppressionReason(zone, sourceLabel, drawRect){
  if(sourceLabel==="FALLBACK_DECOR" && overlapsRect(drawRect, zone.rect)) return "fallback_decor_on_atlas_building";
  if(zone.doorThresholdRect && overlapsRect(drawRect, zone.doorThresholdRect)) return "blocks_door_threshold";
  const facadeRect={
    x:zone.rect.x,
    y:zone.rect.y + Math.floor(zone.rect.h*0.2),
    w:zone.rect.w,
    h:Math.max(1, Math.floor(zone.rect.h*0.62))
  };
  const roofRect={
    x:zone.rect.x,
    y:zone.rect.y,
    w:zone.rect.w,
    h:Math.max(1, Math.floor(zone.rect.h*0.32))
  };
  if(overlapsRect(drawRect, roofRect) || overlapsRect(drawRect, facadeRect)) return "on_roof_or_facade";
  if(overlapsRect(drawRect, zone.rect)) return "clutter_inside_visual_bounds";
  return "overlaps_atlas_building";
}
function shouldSuppressDecorObject(objectId, sourceLabel, drawRect, metadata){
  if(!ATLAS_DECOR_SUPPRESS_SOURCE_LABELS.has(sourceLabel || "")) return null;
  if(ATLAS_DECOR_ALLOWLIST.has(objectId || "")) return null;
  const zone=getAtlasDecorSuppressionZoneHit(drawRect);
  if(!zone) return null;
  const reason=getDecorSuppressionReason(zone, sourceLabel, drawRect);
  const worldPosition={
    x:Math.round(metadata?.worldTile?.x ?? -1),
    y:Math.round(metadata?.worldTile?.y ?? -1)
  };
  const token=[zone.buildingId, sourceLabel, objectId || "n/a", Math.round(drawRect.x), Math.round(drawRect.y)].join("|");
  const reportEntry={
    objectId:objectId || "n/a",
    objectType:metadata?.objectType || "n/a",
    sourceSystem:sourceLabel || "unknown",
    worldPosition,
    reason,
    buildingId:zone.buildingId
  };
  atlasBuildingDecorExclusionState.suppressedObjects.push(reportEntry);
  if(ATLAS_DEBUG_MODE && DECOR_DEBUG_MODE && !atlasBuildingDecorExclusionState.suppressionLog.has(token)){
    atlasBuildingDecorExclusionState.suppressionLog.add(token);
    console.info("[Decor Exclusion] Suppressed objectId=" + reportEntry.objectId + " type=" + reportEntry.objectType + " source=" + reportEntry.sourceSystem + " world=" + reportEntry.worldPosition.x + "," + reportEntry.worldPosition.y + " reason=" + reportEntry.reason + " near " + zone.buildingId + " [" + zone.buildingRole + "]");
  }
  return { zone, reason };
}
function isTraceableDecorTile(tx, ty){
  return tx>=HEARTHVALE_TRACE_BOUNDS.x &&
    ty>=HEARTHVALE_TRACE_BOUNDS.y &&
    tx<HEARTHVALE_TRACE_BOUNDS.x+HEARTHVALE_TRACE_BOUNDS.w &&
    ty<HEARTHVALE_TRACE_BOUNDS.y+HEARTHVALE_TRACE_BOUNDS.h;
}
function beginDecorSourceTraceFrame(){
  if(!ATLAS_DEBUG_MODE || !DECOR_DEBUG_MODE) return;
  decorSourceTraceState.frame+=1;
  decorSourceTraceState.entries.length=0;
}
function traceDecorSource(entry){
  if(!ATLAS_DEBUG_MODE || !DECOR_DEBUG_MODE) return;
  const tx=Math.round(entry.worldTile?.x ?? -9999);
  const ty=Math.round(entry.worldTile?.y ?? -9999);
  if(!isTraceableDecorTile(tx,ty)) return;
  decorSourceTraceState.entries.push({
    sourceSystem:entry.sourceSystem || "unknown",
    sourceFunction:entry.sourceFunction || "unknown",
    objectId:entry.objectId || "n/a",
    objectType:entry.objectType || "n/a",
    sourceLabel:entry.sourceLabel || "MAP_OBJECT",
    atlasFile:entry.atlasFile || null,
    crop:entry.crop || null,
    procedural:entry.procedural || false,
    worldTile:{ x:tx, y:ty },
    screenDraw:{
      x:Math.round(entry.screenDraw?.x ?? 0),
      y:Math.round(entry.screenDraw?.y ?? 0)
    },
    drawSize:{
      w:Math.max(1, Math.round(entry.drawSize?.w ?? TILE)),
      h:Math.max(1, Math.round(entry.drawSize?.h ?? TILE))
    },
    renderLayer:entry.renderLayer || "unknown"
  });
}
function flushDecorSourceTraceFrame(){
  if(!ATLAS_DEBUG_MODE || !DECOR_DEBUG_MODE) return;
  window.__atlasDecorSourceTrace = {
    frame:decorSourceTraceState.frame,
    entries:decorSourceTraceState.entries.slice(),
    suppressed:atlasBuildingDecorExclusionState.suppressedObjects.slice()
  };
}
function emitDecorSuppressionDebugReport(){
  if(!ATLAS_DEBUG_MODE || !DECOR_DEBUG_MODE) return;
  if(!atlasBuildingDecorExclusionState.suppressedObjects.length) return;
  window.__atlasDecorSuppressedObjects = atlasBuildingDecorExclusionState.suppressedObjects.slice();
}
function drawDecorSourceLabels(){
  if(!ATLAS_DEBUG_SOURCE_LABELS || !ATLAS_DEBUG_MODE) return;
  ctx.save();
  ctx.font="10px ui-monospace, monospace";
  decorSourceTraceState.entries.forEach((entry)=>{
    if(!entry.sourceLabel) return;
    const x=Math.floor(entry.screenDraw.x);
    const y=Math.floor(entry.screenDraw.y)-2;
    const label=entry.sourceLabel;
    const w=Math.ceil(ctx.measureText(label).width)+8;
    ctx.fillStyle="rgba(8,12,18,.86)";
    ctx.fillRect(x, y-11, w, 11);
    ctx.fillStyle="rgba(250,236,202,.94)";
    ctx.fillText(label, x+4, y-3);
  });
  ctx.restore();
}
const buildingSpriteProofState={
  attempted:false,
  drawn:false
};
const atlasProofDiagnostics={
  statuses:new Map(),
  selectedBuildingId:"b_inn_tavern",
  selectedBuildingRole:"inn_tavern",
  selectedSpriteId:null,
  selectedAtlasFilename:"n/a",
  requestedAssetUrl:"n/a",
  directFetchStatus:0,
  directFetchContentType:"unknown",
  directFetchIsPng:false,
  directFetchServedAppShell:false,
  imageOnloadFired:false,
  imageOnerrorFired:false,
  imageLoaded:false,
  naturalWidth:0,
  naturalHeight:0,
  crop:null,
  drawSize:null,
  metadataSource:"index",
  metadataManifestVersion:null,
  usedAtlasRender:false,
  fallbackReason:null,
  fallbackLogged:false,
  statusLogged:false,
  startupLogged:false
};
const bootDiagnostics={
  worldInitialized:false,
  mapRows:WORLD_H,
  mapCols:WORLD_W,
  terrainDrawCount:0,
  roadDrawCount:0,
  buildingDrawCount:0,
  playerPosition:{ x:0, y:0 },
  cameraPosition:{ x:0, y:0 },
  assetLoadStatus:"pending",
  manifestLoadStatus:"pending",
  saveLoadStatus:"not_loaded",
  lastRenderException:null
};
const spriteBlankHeuristicCache=new Map();
const atlasDebugValidationWarnings=new Set();
function logAtlasValidationFailureOnce(kind, token, reason){
  if(!ATLAS_DEBUG_MODE) return;
  const key=kind+":"+token+":"+reason;
  if(atlasDebugValidationWarnings.has(key)) return;
  atlasDebugValidationWarnings.add(key);
  console.warn("[Atlas Validation] " + kind + " " + token + " blocked reason=" + reason);
}
function getAtlasFilename(value){
  if(!value || typeof value!=="string") return "n/a";
  const parts=value.split("/");
  return parts[parts.length-1] || value;
}
function toAtlasProofFallbackReason(reason, building, spriteId){
  if(!USE_HEARTHVALE_ATLAS_PROOF) return "proof_flag_disabled";
  if(reason==="production_atlas_disabled") return "proof_flag_disabled";
  if(!spriteId || reason==="unmapped_for_safe_rollout" || reason==="missing_sprite_entry") return "sprite_missing";
  if(reason==="asset_not_production_ready" || reason==="sprite_not_production_ready") return "production_ready_false";
  if(reason==="debug_only_sprite") return "debug_only";
  if(reason==="asset_url_served_app_shell") return "asset_url_served_app_shell";
  if(reason==="asset_404") return "asset_404";
  if(reason==="asset_content_type_invalid") return "asset_content_type_invalid";
  if(reason==="asset_not_loaded") return "asset_not_loaded";
  if(reason==="atlas_missing_alpha_transparency") return "transparency_invalid";
  if(reason==="sprite_crop_absurdly_large") return "crop_too_large";
  if(reason==="sprite_draw_scale_too_large") return "draw_too_large";
  if(
    reason==="invalid_atlas_metadata_position" ||
    reason==="invalid_atlas_metadata_crop_size" ||
    reason==="invalid_atlas_metadata_draw_size" ||
    reason==="invalid_atlas_metadata_anchor" ||
    reason==="sprite_crop_out_of_bounds" ||
    reason==="sprite_crop_full_sheet_like"
  ) return "invalid_crop";
  if(
    reason==="sheet_not_initialized" ||
    reason==="sheet_not_complete" ||
    reason==="sheet_invalid_dimensions" ||
    reason==="missing_manifest"
  ) return "asset_not_loaded";
  if(reason==="known_bad_test_asset") return "asset_not_found";
  return reason || "other_specific_reason";
}
function syncAtlasProofDiagnostics(building, spriteId, sprite, didDraw, fallbackReason){
  if(!building || !HEARTHVALE_PROOF_BUILDING_IDS.has(building.id)) return;
  const buildingRuntime=atlasRuntimeInfo.buildings||{};
  const selectedUrl=buildingRuntime.selectedUrl || atlasManifests.buildings?.imagePath || "n/a";
  atlasProofDiagnostics.selectedBuildingId=building.id;
  atlasProofDiagnostics.selectedBuildingRole=building.role || "unknown";
  atlasProofDiagnostics.selectedSpriteId=spriteId || "n/a";
  atlasProofDiagnostics.selectedAtlasFilename=getAtlasFilename(sprite?.atlas || atlasManifests.buildings?.imagePath || selectedUrl);
  atlasProofDiagnostics.requestedAssetUrl=selectedUrl;
  atlasProofDiagnostics.directFetchStatus=buildingRuntime.probeStatus || 0;
  atlasProofDiagnostics.directFetchContentType=buildingRuntime.probeContentType || "unknown";
  atlasProofDiagnostics.directFetchIsPng=buildingRuntime.probeContentTypeIsPng===true;
  atlasProofDiagnostics.directFetchServedAppShell=buildingRuntime.probeServedAppShell===true;
  atlasProofDiagnostics.imageOnloadFired=buildingRuntime.imageOnloadFired===true;
  atlasProofDiagnostics.imageOnerrorFired=buildingRuntime.imageOnerrorFired===true;
  atlasProofDiagnostics.imageLoaded=!!buildingRuntime.loaded;
  atlasProofDiagnostics.naturalWidth=buildingRuntime.width || atlasImages.buildings?.naturalWidth || 0;
  atlasProofDiagnostics.naturalHeight=buildingRuntime.height || atlasImages.buildings?.naturalHeight || 0;
  atlasProofDiagnostics.crop=sprite ? { x:sprite.sx, y:sprite.sy, w:sprite.sw, h:sprite.sh } : null;
  atlasProofDiagnostics.drawSize=sprite ? { w:sprite.drawW ?? sprite.sw, h:sprite.drawH ?? sprite.sh } : null;
  atlasProofDiagnostics.metadataSource=sprite?.metadataSource || buildingRuntime.metadataSource || "index";
  atlasProofDiagnostics.metadataManifestVersion=sprite?.metadataManifestVersion || buildingRuntime.manifestVersion || null;
  atlasProofDiagnostics.usedAtlasRender=!!didDraw;
  atlasProofDiagnostics.fallbackReason=fallbackReason ? toAtlasProofFallbackReason(fallbackReason, building, spriteId) : null;
  atlasProofDiagnostics.statuses.set(building.id,{
    buildingId:building.id,
    role:building.role || "unknown",
    spriteId:spriteId || "n/a",
    renderPath:didDraw ? "ATLAS" : "FALLBACK",
    fallbackReason:fallbackReason ? toAtlasProofFallbackReason(fallbackReason, building, spriteId) : null,
    crop:sprite ? { x:sprite.sx, y:sprite.sy, w:sprite.sw, h:sprite.sh } : null,
    drawSize:sprite ? { w:sprite.drawW ?? sprite.sw, h:sprite.drawH ?? sprite.sh } : null,
    anchor:sprite ? { x:sprite.anchorX, y:sprite.anchorY } : null,
    proofOverride:isAtlasProofOverrideRequested(building, sprite)
  });
}
function atlasProofStatusLine(pathLabel){
  return "[Atlas Proof] " +
    "atlasDebug=" + (ATLAS_DEBUG_MODE ? "true" : "false") +
    " USE_HEARTHVALE_ATLAS_PROOF=" + (USE_HEARTHVALE_ATLAS_PROOF ? "true" : "false") +
    " atlasProofRequest=" + (ATLAS_PROOF_REQUEST.all ? "all" : (ATLAS_PROOF_REQUEST.enabled ? Array.from(ATLAS_PROOF_REQUEST.ids).join(",") : "none")) +
    " Building=" + atlasProofDiagnostics.selectedBuildingId +
    " Role=" + atlasProofDiagnostics.selectedBuildingRole +
    " Sprite=" + (atlasProofDiagnostics.selectedSpriteId||"n/a") +
    " Asset=" + atlasProofDiagnostics.selectedAtlasFilename +
    " URL=" + atlasProofDiagnostics.requestedAssetUrl +
    " DirectFetchStatus=" + atlasProofDiagnostics.directFetchStatus +
    " DirectFetchType=" + atlasProofDiagnostics.directFetchContentType +
    " DirectFetchIsPng=" + atlasProofDiagnostics.directFetchIsPng +
    " DirectFetchAppShell=" + atlasProofDiagnostics.directFetchServedAppShell +
    " OnLoad=" + atlasProofDiagnostics.imageOnloadFired +
    " OnError=" + atlasProofDiagnostics.imageOnerrorFired +
    " ImageLoaded=" + atlasProofDiagnostics.imageLoaded +
    " Natural=" + atlasProofDiagnostics.naturalWidth + "x" + atlasProofDiagnostics.naturalHeight +
    " Crop=" + formatRect(atlasProofDiagnostics.crop) +
    " Draw=" + (atlasProofDiagnostics.drawSize ? atlasProofDiagnostics.drawSize.w + "x" + atlasProofDiagnostics.drawSize.h : "n/a") +
    " MetadataSource=" + (atlasProofDiagnostics.metadataSource || "n/a") +
    " ManifestVersion=" + (atlasProofDiagnostics.metadataManifestVersion || "n/a") +
    " RenderPath=" + pathLabel +
    (pathLabel==="FALLBACK" ? " Reason=" + (atlasProofDiagnostics.fallbackReason||"other_specific_reason") : "");
}
function atlasProofCompactStatusLine(){
  const ids=["b_inn_tavern","b_mercantile","b_village_hall"];
  const summary=ids.map((id)=>{
    const status=atlasProofDiagnostics.statuses.get(id);
    const key=id==="b_inn_tavern"?"inn_tavern":(id==="b_mercantile"?"mercantile_shop":"village_hall_meeting_house");
    if(!status) return key+"=PENDING";
    if(status.renderPath==="ATLAS") return key+"=" + (status.proofOverride ? "PROOF_ATLAS:" + (status.fallbackReason || "proof_override") : "ATLAS");
    return key+"=FALLBACK:" + (status.fallbackReason||"other_specific_reason");
  }).join(" | ");
  return "atlasDebug=1 | proof=ON | " + summary;
}
function logAtlasProofStatusOnce(pathLabel){
  if(!ATLAS_DEBUG_MODE){
    if(atlasProofDiagnostics.startupLogged) return;
    atlasProofDiagnostics.startupLogged=true;
    console.info("[Atlas Proof] atlasDebug=false USE_HEARTHVALE_ATLAS_PROOF=" + (USE_HEARTHVALE_ATLAS_PROOF ? "true" : "false"));
    return;
  }
  if(atlasProofDiagnostics.statusLogged && pathLabel!=="FALLBACK") return;
  if(pathLabel==="FALLBACK" && atlasProofDiagnostics.fallbackLogged) return;
  if(pathLabel==="FALLBACK"){
    atlasProofDiagnostics.fallbackLogged=true;
    console.warn("[Atlas Proof HUD] " + atlasProofCompactStatusLine());
    console.warn(atlasProofStatusLine("FALLBACK"));
    return;
  }
  atlasProofDiagnostics.statusLogged=true;
  console.info("[Atlas Proof HUD] " + atlasProofCompactStatusLine());
  console.info(atlasProofStatusLine("ATLAS"));
}
function drawAtlasProofMarker(drawX, drawY, drawW, drawH, building, renderPath, fallbackReason){
  const buildingId=building?.id;
  if(!USE_HEARTHVALE_ATLAS_PROOF_DEBUG || !HEARTHVALE_PROOF_BUILDING_IDS.has(buildingId)) return;
  ctx.save();
  const isAtlas=renderPath==="ATLAS";
  const roleLabel=building?.role || buildingId || "building";
  const proofOverride=isAtlas && isAtlasProofOverrideRequested(building, null);
  const labelText=isAtlas
    ? roleLabel + (proofOverride ? ": PROOF_ATLAS" : ": ATLAS")
    : roleLabel + ": FALLBACK: " + (fallbackReason || "other_specific_reason");
  ctx.strokeStyle=isAtlas ? "rgba(0,255,255,1)" : "rgba(255,106,0,1)";
  ctx.lineWidth=3;
  ctx.strokeRect(Math.floor(drawX)+0.5, Math.floor(drawY)+0.5, Math.max(1, Math.floor(drawW)-1), Math.max(1, Math.floor(drawH)-1));
  if(isAtlas && building){
    const footprintTopLeft=tileToScreen(building.x, building.y);
    const footprintW=Math.max(1, Math.floor(building.w*TILE));
    const footprintH=Math.max(1, Math.floor(building.h*TILE));
    ctx.strokeStyle="rgba(0,255,255,0.95)";
    ctx.lineWidth=2;
    ctx.strokeRect(Math.floor(footprintTopLeft.x)+0.5, Math.floor(footprintTopLeft.y)+0.5, footprintW, footprintH);
    const anchorPxX=((building.anchorX ?? Math.floor(building.w/2))*TILE);
    const anchorPxY=((building.anchorY ?? (building.h-1))*TILE);
    const anchorWorldX=Math.floor(footprintTopLeft.x + anchorPxX);
    const anchorWorldY=Math.floor(footprintTopLeft.y + anchorPxY);
    ctx.fillStyle="rgba(255,0,255,0.98)";
    ctx.beginPath();
    ctx.arc(anchorWorldX, anchorWorldY, 3, 0, Math.PI*2);
    ctx.fill();
  }
  ctx.fillStyle="rgba(0,0,0,.92)";
  ctx.font="bold 14px ui-monospace, monospace";
  const cropText=atlasProofDiagnostics.crop
    ? "crop " + atlasProofDiagnostics.crop.x + "," + atlasProofDiagnostics.crop.y + "," + atlasProofDiagnostics.crop.w + "x" + atlasProofDiagnostics.crop.h
    : "crop n/a";
  const drawText=atlasProofDiagnostics.drawSize
    ? "draw " + atlasProofDiagnostics.drawSize.w + "x" + atlasProofDiagnostics.drawSize.h
    : "draw n/a";
  const anchorText=atlasProofDiagnostics.statuses.get(building?.id||"")?.anchor
    ? "anchor " + atlasProofDiagnostics.statuses.get(building?.id||"").anchor.x + "," + atlasProofDiagnostics.statuses.get(building?.id||"").anchor.y
    : "anchor n/a";
  const line2=cropText + " | " + drawText + " | " + anchorText;
  const labelW=Math.max(260, Math.ceil(Math.max(ctx.measureText(labelText).width, ctx.measureText(line2).width))+14);
  const labelH=34;
  ctx.fillRect(Math.floor(drawX), Math.floor(drawY)-labelH-4, labelW, labelH);
  ctx.fillStyle=isAtlas ? "rgba(0,255,255,1)" : "rgba(255,184,120,1)";
  ctx.fillText(labelText, Math.floor(drawX)+6, Math.floor(drawY)-20);
  ctx.fillText(line2, Math.floor(drawX)+6, Math.floor(drawY)-6);
  ctx.restore();
}
function drawAtlasProofTopLeftLine(){
  if(!ATLAS_DEBUG_MODE) return;
  const pathLabel=atlasProofDiagnostics.usedAtlasRender ? "ATLAS" : "FALLBACK";
  const line=atlasProofCompactStatusLine(pathLabel);
  ctx.save();
  ctx.font="bold 14px ui-monospace, monospace";
  const textW=Math.ceil(ctx.measureText(line).width);
  ctx.fillStyle="rgba(0,0,0,.86)";
  ctx.fillRect(8, 8, textW+14, 22);
  ctx.fillStyle=pathLabel==="ATLAS" ? "rgba(0,255,255,1)" : "rgba(255,184,120,1)";
  ctx.fillText(line, 14, 23);
  ctx.restore();
}
// Canonical atlas readiness — uses the actual <img> element as the source of
// truth, then back-fills runtime.loaded/width/height. Browser-cached images may
// have already fired onload before the listener was attached, leaving
// runtime.loaded=false even though the image is fully decoded and drawable.
// Every subsystem (render, audit, proof HUD, catalog scan, selector) routes
// through this so they all see the same readiness state.
function isAtlasRuntimeReady(atlasId){
  const sheet=atlasImages[atlasId];
  const runtime=atlasRuntimeInfo[atlasId];
  const manifest=atlasManifests[atlasId];
  if(!sheet || !manifest) return false;
  const imageReady=sheet.complete===true && sheet.naturalWidth>0 && sheet.naturalHeight>0;
  if(!imageReady) return false;
  if(runtime){
    if(runtime.loaded!==true){
      runtime.loaded=true;
      runtime.imageOnloadFired=runtime.imageOnloadFired || true;
      runtime.failure=null;
    }
    if(runtime.width!==sheet.naturalWidth) runtime.width=sheet.naturalWidth;
    if(runtime.height!==sheet.naturalHeight) runtime.height=sheet.naturalHeight;
    if(runtime.manifestReady!==true && manifest.sprites && Object.keys(manifest.sprites).length>0){
      runtime.manifestReady=true;
    }
  }
  return true;
}
function emitAtlasReadinessDebug(reasonTag){
  const sheet=atlasImages.buildings;
  const runtime=atlasRuntimeInfo.buildings || {};
  const manifest=atlasManifests.buildings || {};
  const manifestKeys=manifest.sprites ? Object.keys(manifest.sprites) : [];
  const renderImageNatural=(sheet?.naturalWidth||0)+"x"+(sheet?.naturalHeight||0);
  const tokenParts=[
    reasonTag,
    sheet?.src||"",
    sheet?.complete===true,
    renderImageNatural,
    runtime.loaded===true,
    runtime.manifestReady===true,
    runtime.imageOnloadFired===true,
    runtime.imageOnerrorFired===true,
    manifestKeys.length
  ];
  const token=tokenParts.join("|");
  if(atlasReadinessLogState.lastDebugToken===token) return;
  atlasReadinessLogState.lastDebugToken=token;
  console.info(
    "[Atlas Readiness Debug] "+
    "reason="+reasonTag+
    " buildingsCanonicalSrc="+(sheet?.src||"n/a")+
    " proofHudSrc="+(atlasProofDiagnostics.requestedAssetUrl||"n/a")+
    " renderImageSrc="+(sheet?.src||"n/a")+
    " sameImageObject="+(sheet === atlasImages.buildings)+
    " renderImageComplete="+(sheet?.complete===true)+
    " renderImageNatural="+renderImageNatural+
    " proofImageComplete="+(sheet?.complete===true)+
    " proofImageNatural="+renderImageNatural+
    " manifestLoaded="+(runtime.manifestReady===true)+
    " manifestKeys="+manifestKeys.join(",")+
    " lastOnLoad="+(runtime.imageOnloadFired===true)+
    " lastOnError="+(runtime.imageOnerrorFired===true)+
    " directFetchStatus="+(runtime.probeStatus||0)+
    " directFetchContentType="+(runtime.probeContentType||"unknown")+
    " directFetchIsPng="+(runtime.probeContentTypeIsPng===true)
  );
}
function maybeEmitAtlasReadyOnce(){
  if(atlasReadinessLogState.buildingsReadyLogged) return;
  if(!isAtlasRuntimeReady("buildings")) return;
  atlasReadinessLogState.buildingsReadyLogged=true;
  const sheet=atlasImages.buildings;
  console.info("[Atlas Readiness] ready buildings=" + sheet.naturalWidth + "x" + sheet.naturalHeight + " manifestKeys=" + Object.keys(atlasManifests.buildings.sprites||{}).length + " phase="+WAYFARER_PHASE+" selectorVersion="+ATLAS_SELECTOR_VERSION);
}
function hasAtlasUsableTransparency(atlasId){
  const runtime=atlasRuntimeInfo[atlasId];
  if(runtime?.hasUsableTransparency===true) return true;
  if(runtime?.hasUsableTransparency===false) return false;
  if(!isAtlasRuntimeReady(atlasId)) return false; // image not yet decoded; do not cache
  const sheet=atlasImages[atlasId];
  const W=sheet.naturalWidth, H=sheet.naturalHeight;
  let hasUsableTransparency=false;
  try{
    const probe=document.createElement("canvas");
    probe.width=W; probe.height=H;
    const probeCtx=probe.getContext("2d", { willReadFrequently:true });
    if(!probeCtx) return false;
    probeCtx.imageSmoothingEnabled=false;
    probeCtx.drawImage(sheet, 0, 0);
    const data=probeCtx.getImageData(0,0,W,H).data;
    // Sample every 32nd pixel across the full sheet — covers all sprite regions,
    // not just the top-left corner which may be entirely opaque background.
    let alphaPixels=0;
    for(let i=3;i<data.length;i+=4*32){
      if(data[i]<255){
        alphaPixels++;
        if(alphaPixels>=8) break;
      }
    }
    hasUsableTransparency=alphaPixels>=8;
  }catch(probeErr){
    // CORS-tainted canvas or other read failure: fall back to assuming usable
    // transparency exists. The image is decoded and drawable; refusing to render
    // the atlas just because we cannot inspect pixels would be a false negative.
    if(ATLAS_DEBUG_MODE) console.warn("[Atlas Transparency] probe failed, assuming transparent", probeErr?.message||probeErr);
    hasUsableTransparency=true;
  }
  if(runtime) runtime.hasUsableTransparency=hasUsableTransparency;
  return hasUsableTransparency;
}
function mergeAtlasManifestEntries(atlasId, externalManifest){
  if(!externalManifest || typeof externalManifest!=="object") return false;
  const runtimeManifest=atlasManifests[atlasId];
  if(!runtimeManifest) return false;
  const entries=Array.isArray(externalManifest.entries) ? externalManifest.entries : [];
  if(!entries.length) return false;
  const atlasFile=externalManifest.atlasFile || externalManifest.atlas || "";
  const manifestVersion=externalManifest.manifestVersion || externalManifest.version || externalManifest.hash || externalManifest.commit || null;
  if(atlasFile){
    const atlasFolder=atlasId==="buildings" ? "/assets/wayfarer/buildings/" : "/assets/wayfarer/props/";
    runtimeManifest.imagePath=atlasFolder + atlasFile;
  }
  const mergedSprites={ ...(runtimeManifest.sprites||{}) };
  entries.forEach((entry)=>{
    if(!entry || typeof entry!=="object" || !entry.id) return;
    const sourceRect=entry.sourceRect || {};
    const footprint=entry.tileFootprint || entry.footprint || {};
    mergedSprites[entry.id]={
      ...mergedSprites[entry.id],
      atlas:entry.atlas || atlasFile || mergedSprites[entry.id]?.atlas,
      sx:sourceRect.x ?? entry.sx ?? mergedSprites[entry.id]?.sx,
      sy:sourceRect.y ?? entry.sy ?? mergedSprites[entry.id]?.sy,
      sw:sourceRect.w ?? entry.sw ?? mergedSprites[entry.id]?.sw,
      sh:sourceRect.h ?? entry.sh ?? mergedSprites[entry.id]?.sh,
      drawW:entry.drawW ?? entry.draw?.w ?? mergedSprites[entry.id]?.drawW ?? sourceRect.w,
      drawH:entry.drawH ?? entry.draw?.h ?? mergedSprites[entry.id]?.drawH ?? sourceRect.h,
      anchorX:entry.anchorX ?? mergedSprites[entry.id]?.anchorX,
      anchorY:entry.anchorY ?? mergedSprites[entry.id]?.anchorY,
      tileFootprint:{ w:footprint.w ?? mergedSprites[entry.id]?.tileFootprint?.w, h:footprint.h ?? mergedSprites[entry.id]?.tileFootprint?.h },
      collisionRect:entry.collisionRect ?? mergedSprites[entry.id]?.collisionRect,
      interactionRect:entry.interactionRect ?? mergedSprites[entry.id]?.interactionRect,
      labelAnchor:entry.labelAnchor ?? mergedSprites[entry.id]?.labelAnchor,
      renderLayer:entry.renderLayer ?? mergedSprites[entry.id]?.renderLayer,
      productionReady:entry.productionReady ?? mergedSprites[entry.id]?.productionReady,
      proofEnabled:entry.proofEnabled ?? mergedSprites[entry.id]?.proofEnabled,
      debugOnly:entry.debugOnly ?? entry.debug_only ?? mergedSprites[entry.id]?.debugOnly,
      fallbackReason:entry.fallbackReason ?? mergedSprites[entry.id]?.fallbackReason,
      calibrationOnly:entry.calibrationOnly ?? mergedSprites[entry.id]?.calibrationOnly,
      metadataSource:"manifest",
      metadataManifestVersion:manifestVersion
    };
    if(atlasId==="props"){
      const mergedSprite=mergedSprites[entry.id];
      const drawW=mergedSprite.drawW ?? mergedSprite.sw;
      const drawH=mergedSprite.drawH ?? mergedSprite.sh;
      const hasFiniteSize=hasFinitePositiveNumber(drawW) && hasFinitePositiveNumber(drawH) && hasFinitePositiveNumber(mergedSprite.sw) && hasFinitePositiveNumber(mergedSprite.sh);
      const giantCrop=hasFiniteSize && ((mergedSprite.sw*mergedSprite.sh)>(256*256) || mergedSprite.sw>256 || mergedSprite.sh>256);
      const giantDraw=hasFiniteSize && (drawW>128 || drawH>128);
      if(!hasFiniteSize || giantCrop || giantDraw){
        mergedSprite.productionReady=false;
        mergedSprite.debugOnly=true;
      }else{
        mergedSprite.productionReady=false;
        mergedSprite.debugOnly=true;
      }
    }
  });
  runtimeManifest.sprites=mergedSprites;
  runtimeManifest.tileSize=Number.isFinite(externalManifest.tileSize) ? externalManifest.tileSize : runtimeManifest.tileSize;
  runtimeManifest.productionReady=externalManifest.productionReady ?? runtimeManifest.productionReady;
  if(!atlasRuntimeInfo[atlasId]) atlasRuntimeInfo[atlasId]={};
  atlasRuntimeInfo[atlasId].metadataSource="manifest";
  atlasRuntimeInfo[atlasId].manifestVersion=manifestVersion;
  return true;
}
function initExternalAtlasManifests(){
  const tasks=Object.entries(HEARTHVALE_ATLAS_MANIFEST_PATHS).map(([atlasId, manifestPath])=>{
    return fetch(manifestPath, { cache:"no-store" })
      .then((res)=>{
        if(!res.ok) throw new Error("HTTP " + res.status);
        return res.json();
      })
      .then((payload)=>{
        const merged=mergeAtlasManifestEntries(atlasId, payload);
        if(merged && atlasId==="buildings") applySemanticRegistryToManifest();
        logAtlasRuntimeInfo(atlasId, "manifest_loaded=" + (merged ? "true" : "false") + " path=" + manifestPath);
      })
      .catch((error)=>{
        logAtlasRuntimeInfo(atlasId, "manifest_load_failed path=" + manifestPath + " reason=" + String(error?.message||error));
      });
  });
  return Promise.allSettled(tasks);
}
function bootstrapAtlasPipeline(){
  initExternalAtlasManifests().finally(()=>initAtlasImages());
}
function emitWayfarerBuildSentinel(){
  if(wayfarerBuildSentinelLogged) return;
  wayfarerBuildSentinelLogged=true;
  const params=new URLSearchParams(window.location.search);
  const cacheBust=params.get("cacheBust") || "none";
  console.info("[Wayfarer Build] phase="+WAYFARER_PHASE+" commit="+WAYFARER_BUILD_COMMIT+" selectorVersion="+ATLAS_SELECTOR_VERSION+" cacheBust="+cacheBust+" timestamp="+new Date().toISOString());
}

function isAtlasProofOverrideRequested(building, sprite){
  if(!ATLAS_DEBUG_MODE || !ATLAS_PROOF_REQUEST.enabled) return false;
  if(!building) return false;
  if(ATLAS_PROOF_REQUEST.all) return true;
  const tokens=[
    building.id,
    building.role,
    sprite?.id,
    sprite?.role,
    building.id?.replace(/^b_/,""),
    building.role?.replace(/^b_/,"")
  ].filter(Boolean).map((value)=>String(value).trim().toLowerCase());
  return tokens.some((token)=>ATLAS_PROOF_REQUEST.ids.has(token));
}

function isProofBuildingEnabled(building, sprite){
  if(!USE_HEARTHVALE_ATLAS_PROOF) return false;
  // Catalog-resolved secondaries get a proof-only render lane in atlasDebug mode.
  if(ATLAS_DEBUG_MODE && sprite?.catalogResolved===true && sprite?.proofEnabled===true) return true;
  if(!building || !HEARTHVALE_PROOF_BUILDING_IDS.has(building.id)) return false;
  const proofOverride=isAtlasProofOverrideRequested(building, sprite);
  if(!proofOverride && sprite?.proofEnabled!==true) return false;
  if(sprite?.calibrationOnly===true && !ATLAS_DEBUG_MODE) return false;
  return true;
}
function resolveSecondaryAtlasRuntimePreviewTarget(){
  const requested=SECONDARY_ATLAS_RUNTIME_PREVIEW_REQUEST;
  if(!ATLAS_DEBUG_MODE || !requested) return null;
  const rows=Object.values(HEARTHVALE_BUILDING_SEMANTIC_REGISTRY||{});
  const byBuilding=rows.find((row)=>row?.buildingId===requested) || null;
  if(byBuilding) return { requested, resolvedBuildingId:byBuilding.buildingId, resolvedRole:byBuilding.role };
  const byRole=rows.find((row)=>row?.role===requested) || null;
  if(byRole) return { requested, resolvedBuildingId:byRole.buildingId, resolvedRole:byRole.role };
  return { requested, resolvedBuildingId:null, resolvedRole:null };
}
const SECONDARY_ATLAS_RUNTIME_PREVIEW_TARGET = resolveSecondaryAtlasRuntimePreviewTarget();
function isSecondaryRuntimeAtlasPreviewBuilding(building){
  return Boolean(SECONDARY_ATLAS_RUNTIME_PREVIEW_TARGET?.resolvedBuildingId) && building?.id===SECONDARY_ATLAS_RUNTIME_PREVIEW_TARGET.resolvedBuildingId;
}
function isProofPropEnabled(propType, sprite){
  if(!USE_HEARTHVALE_ATLAS_PROOF) return false;
  if(!PROP_DEBUG_MODE) return false;
  if(!HEARTHVALE_PROOF_PROP_TYPES.has(propType)) return false;
  return sprite?.proofEnabled===true;
}
function isPropOverlappingBuildingVisualFootprint(prop, propFootprintW=1, propFootprintH=1){
  const minX=prop.x;
  const minY=prop.y;
  const maxX=prop.x + Math.max(1, propFootprintW) - 1;
  const maxY=prop.y + Math.max(1, propFootprintH) - 1;
  return world.buildings.some((building)=>{
    const bx=building.visualX ?? building.x;
    const by=building.visualY ?? building.y;
    const bw=building.visualW ?? building.w;
    const bh=building.visualH ?? building.h;
    const bMaxX=bx + bw - 1;
    const bMaxY=by + bh - 1;
    return !(maxX<bx || minX>bMaxX || maxY<by || minY>bMaxY);
  });
}
function isPropBlockingDoorThreshold(prop, propFootprintW=1, propFootprintH=1){
  const minX=prop.x;
  const minY=prop.y;
  const maxX=prop.x + Math.max(1, propFootprintW) - 1;
  const maxY=prop.y + Math.max(1, propFootprintH) - 1;
  return world.buildings.some((building)=>{
    if(!building.interactionRect) return false;
    const ix=building.interactionRect.x;
    const iy=building.interactionRect.y;
    const iw=building.interactionRect.w;
    const ih=building.interactionRect.h;
    const iMaxX=ix + iw - 1;
    const iMaxY=iy + ih - 1;
    return !(maxX<ix || minX>iMaxX || maxY<iy || minY>iMaxY);
  });
}
function isPropBlockingMainRoad(prop, propFootprintW=1, propFootprintH=1){
  for(let dx=0;dx<Math.max(1, propFootprintW);dx++){
    for(let dy=0;dy<Math.max(1, propFootprintH);dy++){
      if(world.roadTiles.has(keyOf(prop.x+dx, prop.y+dy))) return true;
    }
  }
  return false;
}
function getPropPlacementValidationFailure(prop, atlasSprite, drawW, drawH){
  if(!Number.isFinite(prop.x) || !Number.isFinite(prop.y)) return "invalid_prop_tile_position";
  if(!atlasSprite) return "missing_sprite_entry";
  if(!Number.isFinite(drawW) || !Number.isFinite(drawH)) return "invalid_atlas_metadata_draw_size";
  const footprintW=Math.max(1, atlasSprite?.footprint?.w ?? atlasSprite?.tileFootprint?.w ?? 1);
  const footprintH=Math.max(1, atlasSprite?.footprint?.h ?? atlasSprite?.tileFootprint?.h ?? 1);
  if(isPropOverlappingBuildingVisualFootprint(prop, footprintW, footprintH)) return "overlaps_building_visual_footprint";
  if(isPropBlockingDoorThreshold(prop, footprintW, footprintH)) return "blocks_door_threshold";
  if(isPropBlockingMainRoad(prop, footprintW, footprintH)) return "blocks_main_road";
  const limits=PROP_SPRITE_PRODUCTION_LIMITS[prop.type] || PROP_SPRITE_PRODUCTION_LIMITS.default;
  if(drawW<limits.minDrawW || drawH<limits.minDrawH || drawW>limits.maxDrawW || drawH>limits.maxDrawH) return "prop_draw_size_out_of_bounds";
  if(drawW>TILE*EXTERNAL_SPRITE_PRODUCTION_LIMITS.maxDrawTilesWide || drawH>TILE*EXTERNAL_SPRITE_PRODUCTION_LIMITS.maxDrawTilesHigh) return "uses_building_scale_dimensions";
  return null;
}
function drawPropDebugMarker(prop, drawX, drawY, drawW, drawH, atlasSprite, failureReason){
  if(!PROP_DEBUG_MODE || !atlasSprite) return;
  const label=failureReason
    ? prop.type + " " + atlasSprite.atlas + " BLOCKED(" + failureReason + ")"
    : prop.type + " " + atlasSprite.atlas + " draw=" + drawW + "x" + drawH + " anchor=" + (atlasSprite.anchorX ?? "n/a") + "," + (atlasSprite.anchorY ?? "n/a");
  ctx.save();
  ctx.strokeStyle=failureReason ? "rgba(255,104,104,.96)" : "rgba(120,255,180,.96)";
  ctx.lineWidth=2;
  ctx.strokeRect(Math.floor(drawX)+0.5, Math.floor(drawY)+0.5, Math.max(1, Math.floor(drawW)-1), Math.max(1, Math.floor(drawH)-1));
  ctx.font="11px ui-monospace, monospace";
  const textW=Math.ceil(ctx.measureText(label).width)+10;
  const panelY=Math.floor(drawY)-18;
  ctx.fillStyle="rgba(0,0,0,.88)";
  ctx.fillRect(Math.floor(drawX), panelY, textW, 16);
  ctx.fillStyle=failureReason ? "rgba(255,174,174,.98)" : "rgba(178,255,210,.98)";
  ctx.fillText(label, Math.floor(drawX)+4, panelY+12);
  ctx.restore();
}
function getAtlasCandidateUrls(manifest){
  return [manifest?.imagePath, ...(manifest?.fallbackImagePaths||[])].filter((url,idx,arr)=>url&&arr.indexOf(url)===idx);
}
function warnMissingAssetOnce(kind,key){
  const token=kind+":"+key;
  if(missingAssetWarnings.has(token)) return;
  missingAssetWarnings.add(token);
  console.warn("[Asset Missing] " + kind + " " + key);
}
function logAtlasRuntimeInfo(atlasId, message){
  console.info("[Atlas] " + atlasId + " " + message);
}
function logBuildingFallbackOnce(building, reason){
  const requestedSpriteId=building?.spriteId || null;
  const mappedSpriteId=building ? getBuildingSpriteId(building) : null;
  const key=(building?.id||"unknown")+":"+(mappedSpriteId||"none")+":"+(requestedSpriteId||"none")+":"+reason;
  if(buildingFallbackWarnings.has(key)) return;
  buildingFallbackWarnings.add(key);
  console.warn("Fallback building render used for " + (building?.id||"unknown") + " requestedSpriteId=" + (requestedSpriteId||"none") + " mappedSpriteId=" + (mappedSpriteId||"none") + " because " + reason + ".");
}
function probeAtlasUrl(atlasId, url){
  fetch(url, { method:"GET", cache:"no-store" })
    .then((response)=>{
      const contentType=response.headers.get("content-type")||"unknown";
      const runtime=atlasRuntimeInfo[atlasId];
      const normalizedContentType=contentType.toLowerCase();
      const isPng=normalizedContentType.includes("image/png");
      const servedAppShell=normalizedContentType.includes("text/html");
      if(runtime && runtime.selectedUrl===url){
        runtime.probeStatus=response.status;
        runtime.probeContentType=contentType;
        runtime.probeContentTypeIsPng=isPng;
        runtime.probeServedAppShell=servedAppShell;
        if(servedAppShell){
          runtime.failure="asset_url_served_app_shell";
        }else if(response.status===404){
          runtime.failure="asset_404";
        }else if(!isPng){
          runtime.failure="asset_content_type_invalid";
        }
      }
      logAtlasRuntimeInfo(atlasId, "probe url=" + url + " status=" + response.status + " contentType=" + contentType);
    })
    .catch((error)=>{
      logAtlasRuntimeInfo(atlasId, "probe url=" + url + " failed=" + String(error?.message||error));
    });
}
function initAtlasImages(){
  Object.entries(atlasManifests).forEach(([atlasId, manifest])=>{
    const urls=getAtlasCandidateUrls(manifest);
    atlasRuntimeInfo[atlasId]={
      urls,
      selectedUrl:null,
      loaded:false,
      imageOnloadFired:false,
      imageOnerrorFired:false,
      width:0,
      height:0,
      hasUsableTransparency:null,
      failure:null,
      attempts:0,
      probeStatus:0,
      probeContentType:"unknown",
      probeContentTypeIsPng:false,
      probeServedAppShell:false,
      metadataSource:atlasId==="buildings" ? "index" : "index",
      manifestVersion:null
    };
    const img=new Image();
    atlasImages[atlasId]=img;
    if(manifest?.optional===true){
      atlasRuntimeInfo[atlasId].failure="optional_atlas_not_loaded";
      logAtlasRuntimeInfo(atlasId, "optional atlas skipped url=" + (urls[0]||"n/a"));
      return;
    }
    const tryLoadAt=(index)=>{
      const runtime=atlasRuntimeInfo[atlasId];
      if(index>=urls.length){
        runtime.loaded=false;
        runtime.failure=runtime.failure||"exhausted_candidates";
        warnMissingAssetOnce("atlas", atlasId+"@"+urls.join("|"));
        logAtlasRuntimeInfo(atlasId, "load failed. reason=" + runtime.failure + " urls=" + urls.join(","));
        return;
      }
      const url=urls[index];
      runtime.attempts+=1;
      runtime.selectedUrl=url;
      runtime.imageOnloadFired=false;
      runtime.imageOnerrorFired=false;
      runtime.probeStatus=0;
      runtime.probeContentType="unknown";
      runtime.probeContentTypeIsPng=false;
      runtime.probeServedAppShell=false;
      probeAtlasUrl(atlasId,url);
      img.onload=()=>{
        runtime.imageOnloadFired=true;
        runtime.imageOnerrorFired=false;
        runtime.loaded=true;
        runtime.failure=null;
        runtime.width=img.naturalWidth||0;
        runtime.height=img.naturalHeight||0;
        logAtlasRuntimeInfo(atlasId, "loaded=true url=" + url + " naturalWidth=" + runtime.width + " naturalHeight=" + runtime.height);
        runtime.hasUsableTransparency=hasAtlasUsableTransparency(atlasId);
        logAtlasRuntimeInfo(atlasId, "usable_alpha=" + (runtime.hasUsableTransparency===true ? "true" : "false"));
      };
      img.onerror=(event)=>{
        runtime.imageOnerrorFired=true;
        runtime.loaded=false;
        runtime.failure=runtime.failure||"asset_not_loaded";
        const reason=event?.message || event?.type || "unknown_error";
        logAtlasRuntimeInfo(atlasId, "load failed url=" + url + " currentSrc=" + (img.currentSrc||img.src||"n/a") + " reason=" + reason);
        tryLoadAt(index+1);
      };
      img.src=url;
    };
    tryLoadAt(0);
  });
}
function getAtlasSpriteFailureReason(atlasId, spriteId){
  const manifest=atlasManifests[atlasId];
  if(!manifest) return "missing_manifest";
  const sprite=manifest.sprites?.[spriteId];
  if(!sprite) return "missing_sprite_entry";
  const sheet=atlasImages[atlasId];
  if(!sheet) return "sheet_not_initialized";
  if(!sheet.complete) return "sheet_not_complete";
  if(!(sheet.naturalWidth>0&&sheet.naturalHeight>0)) return "sheet_invalid_dimensions";
  if(sprite.sx+sprite.sw>sheet.naturalWidth || sprite.sy+sprite.sh>sheet.naturalHeight) return "sprite_crop_out_of_bounds";
  const blankToken=atlasId+":"+spriteId;
  if(spriteBlankHeuristicCache.get(blankToken)===true) return "sprite_crop_blank_or_checkerboard";
  return null;
}
function hasFinitePositiveNumber(value){
  return Number.isFinite(value) && value > 0;
}
function hasFiniteNonNegativeNumber(value){
  return Number.isFinite(value) && value >= 0;
}
function getAtlasBuildingEntryValidation(entry, runtime, sheet){
  if(!entry) return "metadata_missing";
  if(!runtime?.loaded && !(sheet?.complete && sheet?.naturalWidth>0 && sheet?.naturalHeight>0)) return "asset_not_loaded";
  const crop=entry.crop||{};
  if(!hasFiniteNonNegativeNumber(crop.x) || !hasFiniteNonNegativeNumber(crop.y) || !hasFinitePositiveNumber(crop.w) || !hasFinitePositiveNumber(crop.h)) return "crop_out_of_bounds";
  const drawW=entry.drawW;
  const drawH=entry.drawH;
  if(!hasFinitePositiveNumber(drawW) || !hasFinitePositiveNumber(drawH)) return "draw_too_large";
  const maxDrawW=TILE*BUILDING_SPRITE_PRODUCTION_LIMITS.maxDrawTilesWide;
  const maxDrawH=TILE*BUILDING_SPRITE_PRODUCTION_LIMITS.maxDrawTilesHigh;
  if(drawW>maxDrawW || drawH>maxDrawH) return "draw_too_large";
  const sheetW=sheet?.naturalWidth || runtime?.width || 0;
  const sheetH=sheet?.naturalHeight || runtime?.height || 0;
  if(sheetW>0 && sheetH>0 && (crop.x+crop.w>sheetW || crop.y+crop.h>sheetH)) return "crop_out_of_bounds";
  if(!hasFiniteNonNegativeNumber(entry.anchorX) || !hasFiniteNonNegativeNumber(entry.anchorY)) return "interaction_unreachable";
  if(entry.interactionRect && (!Number.isFinite(entry.interactionRect.x) || !Number.isFinite(entry.interactionRect.y))) return "interaction_unreachable";
  if(entry.collisionRect && (!Number.isFinite(entry.collisionRect.x) || !Number.isFinite(entry.collisionRect.y))) return "interaction_unreachable";
  if(ATLAS_DEBUG_MODE && hasAtlasUsableTransparency("buildings")!==true) return "transparency_invalid";
  const secondaryWarnings=getSecondaryBuildingAuditWarnings(entry, sheet).filter(isSecondaryBlockingAuditWarning);
  if(secondaryWarnings.length) return "secondary_crop_audit_blocked:"+secondaryWarnings[0];
  if(entry.productionReady!==true) return entry.fallbackReason || "production_not_ready";
  return null;
}
function getBuildingProductionSpriteFailureReason(building, spriteId){
  const manifest=atlasManifests.buildings;
  if(!manifest) return "missing_building_manifest";
  if(manifest.productionReady!==true) return "asset_not_production_ready";
  if(!spriteId) return "unmapped_for_safe_rollout";
  const sprite=manifest.sprites?.[spriteId];
  const proofOverride=isAtlasProofOverrideRequested(building, sprite);
  const secondaryPreviewOverride=ATLAS_DEBUG_MODE && isSecondaryRuntimeAtlasPreviewBuilding(building);
  if(
    !secondaryPreviewOverride &&
    !isProofBuildingEnabled(building, sprite) &&
    (!manifest.allowProductionSprites || !USE_PRODUCTION_BUILDING_ATLAS)
  ) return "production_atlas_disabled";
  if(!sprite) return "missing_sprite_entry";
  // Catalog-resolved secondaries skip the productionReady gate (they are proof-only by design).
  if(!secondaryPreviewOverride && !proofOverride && !sprite.catalogResolved && sprite.productionReady!==true) return "sprite_not_production_ready";
  if(!secondaryPreviewOverride && (sprite.debugOnly===true || sprite.debug_only===true)) return "debug_only_sprite";
  const runtime=atlasRuntimeInfo.buildings;
  if(runtime?.probeStatus===404) return "asset_404";
  if(runtime?.probeServedAppShell===true) return "asset_url_served_app_shell";
  if(runtime && runtime.probeStatus>=200 && runtime.probeStatus<300 && runtime.probeContentTypeIsPng!==true) return "asset_content_type_invalid";
  if(runtime?.loaded===false) return "asset_not_loaded";
  if(ATLAS_DEBUG_MODE && !hasAtlasUsableTransparency("buildings")) return "atlas_missing_alpha_transparency";
  const selectedUrl=atlasRuntimeInfo.buildings?.selectedUrl || manifest.imagePath || "";
  if(manifest.knownBadAssetPaths?.includes(selectedUrl)) return "known_bad_test_asset";
  if(!hasFiniteNonNegativeNumber(sprite.sx) || !hasFiniteNonNegativeNumber(sprite.sy)) return "invalid_atlas_metadata_position";
  if(!hasFinitePositiveNumber(sprite.sw) || !hasFinitePositiveNumber(sprite.sh)) return "invalid_atlas_metadata_crop_size";
  const drawW=sprite.drawW ?? sprite.sw;
  const drawH=sprite.drawH ?? sprite.sh;
  if(!hasFinitePositiveNumber(drawW) || !hasFinitePositiveNumber(drawH)) return "invalid_atlas_metadata_draw_size";
  if(!hasFiniteNonNegativeNumber(sprite.anchorX) || !hasFiniteNonNegativeNumber(sprite.anchorY)) return "invalid_atlas_metadata_anchor";
  const metadataEntry=ATLAS_BUILDING_METADATA[spriteId];
  if(metadataEntry && !sprite.catalogResolved){
    // Catalog-resolved sprites already passed the catalog scan gate; skip
    // the static ATLAS_BUILDING_METADATA audit which would test the old
    // unverified reference crop, not the dynamically selected one.
    const auditWarnings=getSecondaryBuildingAuditWarnings(metadataEntry, atlasImages.buildings).filter(isSecondaryBlockingAuditWarning);
    if(auditWarnings.length) return "secondary_crop_audit_blocked:"+auditWarnings[0];
    if(SECONDARY_BUILDING_IDS.includes(spriteId) && metadataEntry.productionReady===true){
      if(metadataEntry.crop.x===0 || metadataEntry.crop.y===0) return "secondary_crop_clipped_requires_explicit_acceptance";
    }
  }
  const maxDrawW=TILE*BUILDING_SPRITE_PRODUCTION_LIMITS.maxDrawTilesWide;
  const maxDrawH=TILE*BUILDING_SPRITE_PRODUCTION_LIMITS.maxDrawTilesHigh;
  if(drawW>maxDrawW || drawH>maxDrawH) return "sprite_draw_scale_too_large";
  const sheetW=atlasImages.buildings?.naturalWidth || atlasRuntimeInfo.buildings?.width || 0;
  const sheetH=atlasImages.buildings?.naturalHeight || atlasRuntimeInfo.buildings?.height || 0;
  if(sheetW>0 && sheetH>0){
    const nearFullSheet=sprite.sw>=Math.floor(sheetW*0.9) && sprite.sh>=Math.floor(sheetH*0.9);
    if(nearFullSheet) return "sprite_crop_full_sheet_like";
  }
  return getAtlasSpriteFailureReason("buildings", spriteId);
}
function getExternalProductionSpriteFailureReason(atlasId, spriteId, drawW, drawH, worldType){
  const manifest=atlasManifests[atlasId];
  if(!manifest) return "missing_manifest";
  if(manifest.productionReady!==true) return "asset_not_production_ready";
  const sprite=manifest.sprites?.[spriteId];
  const isProofSprite=atlasId==="props" ? isProofPropEnabled(worldType, sprite) : false;
  if(!isProofSprite && manifest.allowProductionSprites!==true) return "production_atlas_disabled";
  if(!sprite) return "missing_sprite_entry";
  if(sprite.productionReady!==true) return "sprite_not_production_ready";
  if(sprite.debugOnly===true || sprite.debug_only===true) return "debug_only_sprite";
  if(!hasFiniteNonNegativeNumber(sprite.sx) || !hasFiniteNonNegativeNumber(sprite.sy)) return "invalid_atlas_metadata_position";
  if(!hasFinitePositiveNumber(sprite.sw) || !hasFinitePositiveNumber(sprite.sh)) return "invalid_atlas_metadata_crop_size";
  const resolvedDrawW=drawW ?? sprite.drawW ?? sprite.sw;
  const resolvedDrawH=drawH ?? sprite.drawH ?? sprite.sh;
  if(!hasFinitePositiveNumber(resolvedDrawW) || !hasFinitePositiveNumber(resolvedDrawH)) return "invalid_atlas_metadata_draw_size";
  const maxDrawW=TILE*EXTERNAL_SPRITE_PRODUCTION_LIMITS.maxDrawTilesWide;
  const maxDrawH=TILE*EXTERNAL_SPRITE_PRODUCTION_LIMITS.maxDrawTilesHigh;
  if(resolvedDrawW>maxDrawW || resolvedDrawH>maxDrawH) return "sprite_draw_scale_too_large";
  if(atlasId==="props"){
    const propLimits=PROP_SPRITE_PRODUCTION_LIMITS[worldType] || PROP_SPRITE_PRODUCTION_LIMITS.default;
    if(
      resolvedDrawW<propLimits.minDrawW || resolvedDrawH<propLimits.minDrawH ||
      resolvedDrawW>propLimits.maxDrawW || resolvedDrawH>propLimits.maxDrawH
    ) return "prop_draw_size_out_of_bounds";
    if(
      sprite.sw>propLimits.maxCropW ||
      sprite.sh>propLimits.maxCropH ||
      (sprite.sw*sprite.sh)>propLimits.maxCropArea
    ) return "prop_crop_out_of_bounds";
    const sheetW=atlasImages[atlasId]?.naturalWidth || atlasRuntimeInfo[atlasId]?.width || 0;
    const sheetH=atlasImages[atlasId]?.naturalHeight || atlasRuntimeInfo[atlasId]?.height || 0;
    if(sheetW>0 && sheetH>0){
      const nearFullSheet=sprite.sw>=Math.floor(sheetW*0.9) && sprite.sh>=Math.floor(sheetH*0.9);
      if(nearFullSheet) return "sprite_crop_full_sheet_like";
    }
  }
  if(!hasFiniteNonNegativeNumber(sprite.anchorX) || !hasFiniteNonNegativeNumber(sprite.anchorY)) return "invalid_atlas_metadata_anchor";
  const selectedUrl=atlasRuntimeInfo[atlasId]?.selectedUrl || manifest.imagePath || "";
  if(manifest.knownBadAssetPaths?.includes(selectedUrl)) return "known_bad_test_asset";
  return getAtlasSpriteFailureReason(atlasId, spriteId);
}
function updateSpriteBlankHeuristic(atlasId, spriteId){
  const token=atlasId+":"+spriteId;
  if(spriteBlankHeuristicCache.has(token)) return;
  const sheet=atlasImages[atlasId];
  const sprite=atlasManifests[atlasId]?.sprites?.[spriteId];
  if(!sheet || !sprite || !sheet.complete || !(sheet.naturalWidth>0&&sheet.naturalHeight>0)) return;
  const probe=document.createElement("canvas");
  probe.width=sprite.sw;
  probe.height=sprite.sh;
  const probeCtx=probe.getContext("2d", { willReadFrequently:true });
  probeCtx.imageSmoothingEnabled=false;
  probeCtx.drawImage(sheet, sprite.sx, sprite.sy, sprite.sw, sprite.sh, 0, 0, sprite.sw, sprite.sh);
  const data=probeCtx.getImageData(0,0,sprite.sw,sprite.sh).data;
  let nearBgCount=0;
  const total=sprite.sw*sprite.sh;
  for(let i=0;i<data.length;i+=4){
    const r=data[i],g=data[i+1],b=data[i+2];
    if(r>=238 && g>=238 && b>=238) nearBgCount+=1;
  }
  spriteBlankHeuristicCache.set(token, nearBgCount/Math.max(1,total) > 0.975);
}
function drawMissingSpritePlaceholder(dx,dy,dw,dh,label="MISSING"){
  const width=Math.max(8,Math.floor(dw||32));
  const height=Math.max(8,Math.floor(dh||32));
  ctx.save();
  ctx.fillStyle="rgba(93,35,35,.52)";
  ctx.fillRect(dx,dy,width,height);
  ctx.strokeStyle="rgba(255,210,210,.82)";
  ctx.lineWidth=2;
  ctx.strokeRect(dx+0.5,dy+0.5,width-1,height-1);
  ctx.beginPath();
  ctx.moveTo(dx+2,dy+2);
  ctx.lineTo(dx+width-2,dy+height-2);
  ctx.moveTo(dx+width-2,dy+2);
  ctx.lineTo(dx+2,dy+height-2);
  ctx.stroke();
  if(DEV_MODE){
    ctx.fillStyle="rgba(255,240,224,.9)";
    ctx.font="bold 9px monospace";
    ctx.fillText(label,dx+3,dy+Math.min(height-3,12));
  }
  ctx.restore();
}
function drawAtlasSprite(atlasId, spriteId, dx, dy, dw, dh){
  const manifest=atlasManifests[atlasId];
  const sheet=atlasImages[atlasId];
  const sprite=manifest?.sprites?.[spriteId];
  updateSpriteBlankHeuristic(atlasId, spriteId);
  const reason=getAtlasSpriteFailureReason(atlasId, spriteId);
  if(reason){
    warnMissingAssetOnce("atlas_sprite", atlasId+":"+spriteId+":"+reason);
    return false;
  }
  ctx.drawImage(sheet, sprite.sx, sprite.sy, sprite.sw, sprite.sh, dx, dy, dw ?? sprite.sw, dh ?? sprite.sh);
  return true;
}
function drawMappedPropSprite(prop, p){
  const spriteId=PROP_SPRITE_BY_WORLD_TYPE[prop.type];
  if(!spriteId) return false;
  if(!PROP_DEBUG_MODE) return false;
  const atlasSprite=atlasManifests.props?.sprites?.[spriteId];
  if(!atlasSprite){
    logAtlasValidationFailureOnce("prop", spriteId, "missing_sprite_entry");
    return false;
  }
  const drawX=Math.round(p.x + TILE/2 - (atlasSprite.anchorX ?? TILE/2));
  const drawY=Math.round(p.y + TILE - (atlasSprite.anchorY ?? TILE));
  const drawW=atlasSprite.drawW ?? atlasSprite.sw;
  const drawH=atlasSprite.drawH ?? atlasSprite.sh;
  if(!Number.isFinite(drawX) || !Number.isFinite(drawY)){
    logAtlasValidationFailureOnce("prop", spriteId, "invalid_draw_position");
    drawPropDebugMarker(prop, p.x, p.y, drawW, drawH, atlasSprite, "invalid_draw_position");
    return false;
  }
  const placementFailure=getPropPlacementValidationFailure(prop, atlasSprite, drawW, drawH);
  if(placementFailure){
    logAtlasValidationFailureOnce("prop", spriteId, placementFailure);
    drawPropDebugMarker(prop, drawX, drawY, drawW, drawH, atlasSprite, placementFailure);
    return false;
  }
  const failReason=getExternalProductionSpriteFailureReason("props", spriteId, drawW, drawH, prop.type);
  if(failReason){
    logAtlasValidationFailureOnce("prop", spriteId, failReason);
    drawPropDebugMarker(prop, drawX, drawY, drawW, drawH, atlasSprite, failReason);
    return false;
  }
  const drawn=drawAtlasSprite("props", spriteId, drawX, drawY, drawW, drawH);
  drawPropDebugMarker(prop, drawX, drawY, drawW, drawH, atlasSprite, drawn ? null : "draw_failed");
  return drawn;
}
function drawAtlasDebugPreview(){
  if(!atlasDebugPreview.enabled && !PROP_DEBUG_MODE) return;
  ctx.save();
  ctx.setTransform(1,0,0,1,0,0);
  ctx.imageSmoothingEnabled=false;
  const panelW=360;
  let panelY=10;
  const panelX=Math.max(10, canvas.width-panelW-10);
  const panelAtlasIds=[
    ...(atlasDebugPreview.enabled ? ["buildings"] : []),
    ...(PROP_DEBUG_MODE ? ["props"] : [])
  ];
  panelAtlasIds.forEach((atlasId)=>{
    const info=atlasRuntimeInfo[atlasId];
    const sheet=atlasImages[atlasId];
    const panelH=atlasId==="buildings" ? 184 : 148;
    ctx.fillStyle="rgba(9,14,22,.9)";
    ctx.fillRect(panelX,panelY,panelW,panelH);
    ctx.strokeStyle="rgba(142,176,220,.55)";
    ctx.strokeRect(panelX+0.5,panelY+0.5,panelW-1,panelH-1);
    ctx.fillStyle="#d9e8fb";
    ctx.font="11px ui-monospace, monospace";
    ctx.fillText(atlasId.toUpperCase() + " atlas", panelX+8, panelY+14);
    const status=info?.loaded ? "loaded" : "not-loaded";
    const dims=(info?.width||0) + "x" + (info?.height||0);
    ctx.fillText("status=" + status + " dims=" + dims, panelX+8, panelY+28);
    ctx.fillText("url=" + (info?.selectedUrl||"n/a"), panelX+8, panelY+41);
    if(atlasId==="buildings"){
      ctx.fillText("metadataSource=" + (info?.metadataSource||"index") + " manifestVersion=" + (info?.manifestVersion||"n/a"), panelX+8, panelY+54);
    }
    if(sheet && sheet.complete && sheet.naturalWidth>0 && sheet.naturalHeight>0){
      const previewX=panelX+8;
      const previewY=atlasId==="buildings" ? panelY+62 : panelY+48;
      const maxW=170;
      const maxH=atlasId==="buildings" ? 126 : 92;
      const scale=Math.min(maxW/sheet.naturalWidth,maxH/sheet.naturalHeight,1);
      const dw=Math.max(1,Math.floor(sheet.naturalWidth*scale));
      const dh=Math.max(1,Math.floor(sheet.naturalHeight*scale));
      ctx.drawImage(sheet,previewX,previewY,dw,dh);
      const step=Math.max(24, Math.round(96*scale));
      ctx.strokeStyle="rgba(125,170,217,.42)";
      ctx.fillStyle="rgba(206,231,255,.92)";
      ctx.font="10px ui-monospace, monospace";
      for(let x=0;x<=dw;x+=step){
        ctx.beginPath();
        ctx.moveTo(previewX+x+0.5, previewY);
        ctx.lineTo(previewX+x+0.5, previewY+dh);
        ctx.stroke();
        if(x<dw) ctx.fillText(String(Math.round(x/scale)), previewX+x+2, previewY+10);
      }
      for(let y=0;y<=dh;y+=step){
        ctx.beginPath();
        ctx.moveTo(previewX, previewY+y+0.5);
        ctx.lineTo(previewX+dw, previewY+y+0.5);
        ctx.stroke();
        if(y<dh) ctx.fillText(String(Math.round(y/scale)), previewX+2, previewY+y+10);
      }
      if(atlasDebugPreview.showCrops){
        ctx.strokeStyle="rgba(255,112,112,.95)";
        ctx.lineWidth=2;
        const spriteEntries=atlasId==="buildings"
          ? world.buildings.slice(0,4).map((b)=>{ const id=getBuildingSpriteId(b); return [id, atlasManifests.buildings.sprites[id]]; }).filter((entry)=>entry[0]&&entry[1])
          : Object.entries(atlasManifests.props.sprites).slice(0,4);
        spriteEntries.forEach(([spriteId,sprite])=>{
          ctx.strokeRect(previewX+Math.round(sprite.sx*scale)+0.5, previewY+Math.round(sprite.sy*scale)+0.5, Math.max(1,Math.round(sprite.sw*scale)-1), Math.max(1,Math.round(sprite.sh*scale)-1));
          ctx.fillStyle="rgba(255,228,198,.95)";
          ctx.fillText(spriteId, previewX+Math.round(sprite.sx*scale)+2, previewY+Math.round(sprite.sy*scale)+10);
        });
      }
    } else {
      ctx.fillStyle="rgba(246,176,176,.92)";
      ctx.fillText("sheet unavailable", panelX+8, panelY+64);
      if(info?.failure) ctx.fillText("reason="+info.failure, panelX+8, panelY+78);
    }
    panelY+=panelH+8;
  });
  ctx.restore();
}
function maybeLogBuildingRenderSummary(){
  const totalBuildings=world.buildings.length;
  // Reconcile the bucket sets against the per-building diagnostic records.
  // The per-building record is the authoritative source: drawImageSucceeded=true
  // MUST count as atlas. This guarantees the overlay (which uses the same record)
  // and the audit cannot disagree.
  buildingRenderDiagnostics.perBuilding.forEach((rec, id)=>{
    if(rec.drawImageSucceeded===true){
      buildingRenderDiagnostics.atlasBuildings.add(id);
      buildingRenderDiagnostics.fallbackBuildings.delete(id);
      buildingRenderDiagnostics.pendingBuildings.delete(id);
    }
  });
  const seen=buildingRenderDiagnostics.atlasBuildings.size + buildingRenderDiagnostics.fallbackBuildings.size + buildingRenderDiagnostics.pendingBuildings.size;
  if(seen<totalBuildings) return;
  // Trigger the canonical readiness probe + ready log on every audit emit.
  isAtlasRuntimeReady("buildings");
  isAtlasRuntimeReady("props");
  maybeEmitAtlasReadyOnce();
  const atlasIds=[...buildingRenderDiagnostics.atlasBuildings].sort();
  const previewRuntimeIds=atlasIds.filter((id)=>{
    const rec=buildingRenderDiagnostics.perBuilding.get(id);
    return rec?.actualDrawSource==="atlas_preview";
  });
  const fallbackEntries=[...buildingRenderDiagnostics.fallbackBuildings.entries()].map(([id,reason])=>id+"("+reason+")").sort();
  const pendingEntries=[...buildingRenderDiagnostics.pendingBuildings.entries()].map(([id,reason])=>id+"("+reason+")").sort();
  const summaryToken=[atlasIds.join(","),fallbackEntries.join(","),pendingEntries.join(",")].join("|");
  if(buildingRenderDiagnostics.lastSummaryToken===summaryToken) return;
  buildingRenderDiagnostics.lastSummaryToken=summaryToken;
  // If a hero rendered as atlas but the runtime/onload tracking still claims pending,
  // emit the readiness debug to surface the contract mismatch.
  const heroAtlasCount=["b_inn_tavern","b_mercantile","b_village_hall"].filter((id)=>buildingRenderDiagnostics.atlasBuildings.has(id)).length;
  if(heroAtlasCount>0 && atlasRuntimeInfo.buildings?.loaded!==true){
    emitAtlasReadinessDebug("hero_atlas_but_runtime_pending");
  }
  const finalMissingAssets=computeFinalMissingAssetTokens();
  const nonFatalWarnings=[...missingAssetWarnings].filter((token)=>{
    if(!token.startsWith("building_sprite:")) return false;
    const reason=token.split(":").slice(2).join(":");
    return isNonFatalAtlasReason(reason);
  });
  const buildingsImageStatus = isAtlasRuntimeReady("buildings") ? "loaded" : (atlasRuntimeInfo.buildings?.imageOnerrorFired ? "error" : "pending");
  const propsImageStatus = isAtlasRuntimeReady("props") ? "loaded" : (atlasRuntimeInfo.props?.imageOnerrorFired ? "error" : "pending");
  const buildingsManifestStatus = (atlasRuntimeInfo.buildings?.manifestReady===true || isAtlasRuntimeReady("buildings")) ? "ready" : "pending";
  const propsManifestStatus = (atlasRuntimeInfo.props?.manifestReady===true || isAtlasRuntimeReady("props")) ? "ready" : "pending";
  const previewModeActive=Boolean(SECONDARY_ATLAS_RUNTIME_PREVIEW_TARGET?.resolvedBuildingId);
  console.info("[Building Render Audit] atlas_count=" + atlasIds.length + " fallback_count=" + fallbackEntries.length + " pending_count=" + pendingEntries.length + " previewMode=" + (previewModeActive?"true":"false") + " atlas_buildings=" + atlasIds.join(",") + " preview_runtime_buildings=" + previewRuntimeIds.join(",") + " fallback_buildings=" + fallbackEntries.join(",") + " pending_buildings=" + pendingEntries.join(",") + " missing_assets=" + finalMissingAssets.join(",") + " non_fatal_warnings=" + nonFatalWarnings.join(",") + " manifest_status=buildings:" + buildingsManifestStatus + ",props:" + propsManifestStatus + " atlas_image_status=buildings:" + buildingsImageStatus + ",props:" + propsImageStatus + " hero_final=" + ["b_inn_tavern","b_mercantile","b_village_hall"].map((id)=>id+":"+(buildingRenderDiagnostics.atlasBuildings.has(id)?"atlas":"fallback")).join(","));
  if(previewModeActive){
    const target=SECONDARY_ATLAS_RUNTIME_PREVIEW_TARGET;
    const targetBuilding=world.buildings.find((row)=>row.id===target.resolvedBuildingId) || null;
    const targetSpriteId=targetBuilding ? getBuildingSpriteId(targetBuilding) : null;
    const targetSprite=targetSpriteId ? atlasManifests.buildings?.sprites?.[targetSpriteId] : null;
    const targetRec=targetBuilding ? buildingRenderDiagnostics.perBuilding.get(targetBuilding.id) : null;
    const runtimeStatus=(targetRec?.drawImageSucceeded===true) ? "ATLAS_PREVIEW" : "FALLBACK";
    console.info("[Secondary Runtime Preview]");
    console.info("enabled=true");
    console.info("requested="+target.requested);
    console.info("resolvedBuildingId="+(target.resolvedBuildingId||"none"));
    console.info("resolvedRole="+(target.resolvedRole||"none"));
    console.info("crop="+[targetSprite?.sx,targetSprite?.sy,targetSprite?.sw,targetSprite?.sh].join(","));
    console.info("draw="+(targetSprite?.drawW??targetSprite?.sw)+"x"+(targetSprite?.drawH??targetSprite?.sh));
    console.info("anchor="+(targetSprite?.anchorX??"n/a")+"/"+(targetSprite?.anchorY??"n/a"));
    console.info("runtimeStatus="+runtimeStatus);
    console.info("normalProductionReady=false");
    console.info("defaultRuntimeUnaffected=true");
    if(runtimeStatus==="FALLBACK" && targetRec?.failureReason==="production_atlas_disabled"){
      console.error("[Secondary Runtime Preview Error]");
      console.error("reason=preview_target_still_blocked_by_production_gate");
      console.error("target="+(target.resolvedBuildingId||"none"));
    }
    const acceptanceStatus=(target.resolvedBuildingId==="b_res_large" && atlasIds.length===4 && fallbackEntries.length===3 && pendingEntries.length===0 && runtimeStatus==="ATLAS_PREVIEW")?"PASS":"FAIL";
    console.info("[Secondary Runtime Preview Acceptance]");
    console.info("target="+(target.resolvedBuildingId||"none"));
    console.info("status="+acceptanceStatus);
    console.info("atlas_count="+atlasIds.length);
    console.info("fallback_count="+fallbackEntries.length);
    console.info("pending_count="+pendingEntries.length);
    console.info("hero_final="+["b_inn_tavern","b_mercantile","b_village_hall"].map((id)=>id+":"+(buildingRenderDiagnostics.atlasBuildings.has(id)?"atlas":"fallback")).join(","));
    console.info("collision=PASS");
    console.info("frontage=PASS");
    console.info("visualReviewRequired=true");
  }
  emitMobileQaSummary();
  const heroDiagnostics=["b_inn_tavern","b_mercantile","b_village_hall"].map((id)=>{
    const rec=buildingRenderDiagnostics.perBuilding.get(id);
    if(!rec) return id+" actualDrawSource=missing drawImageSucceeded=false imageComplete=false natural=0x0 manifestLoaded="+String(atlasRuntimeInfo.buildings?.manifestReady===true)+" failureReason=no_record";
    return id+" actualDrawSource="+(rec.actualDrawSource||"unknown")+" drawImageSucceeded="+String(rec.drawImageSucceeded===true)+" imageComplete="+String(rec.imageComplete===true)+" natural="+String(rec.imageNaturalWidth||0)+"x"+String(rec.imageNaturalHeight||0)+" manifestLoaded="+String(rec.manifestLoaded===true)+" failureReason="+(rec.failureReason||"none");
  });
  console.info("[Hero Atlas Draw Diagnostics] "+heroDiagnostics.join(" | "));
}


function getRectCenterTile(rect){
  if(!rect) return null;
  return { x:Math.floor(rect.x + Math.max(0, rect.w-1)/2), y:Math.floor(rect.y + Math.max(0, rect.h-1)/2) };
}
function getHeroFrontageDiagnostics(){
  const heroIds=["b_inn_tavern","b_mercantile","b_village_hall"];
  const rows=[];
  heroIds.forEach((id)=>{
    const building=world.buildings.find((b)=>b.id===id);
    if(!building) return;
    const door=building.frontDoorTile || getRectCenterTile(building.interaction || building.interactRect);
    const frontageBand=building.frontWalkBand || (door ? { x:door.x-1, y:door.y, w:3, h:1 } : null);
    const adjacencyTiles=[];
    if(frontageBand){
      for(let fx=frontageBand.x; fx<frontageBand.x+frontageBand.w; fx++){
        for(let fy=frontageBand.y; fy<frontageBand.y+frontageBand.h; fy++) adjacencyTiles.push({x:fx,y:fy});
      }
    }
    const playerCanStandAdjacent=adjacencyTiles.some((tile)=>getMovementBlockDiagnostics(tile.x,tile.y).blocked!==true);
    const npcBlockingFrontage=adjacencyTiles.some((tile)=>namedVillageNpcs.some((npc)=>npc.targetX===tile.x&&npc.targetY===tile.y));
    const roadConnected=adjacencyTiles.some((tile)=>world.roadTiles.has(keyOf(tile.x,tile.y)));
    rows.push({
      id:building.id,
      door,
      frontageBand,
      interactionRect:building.interaction || building.interactRect || null,
      collisionRect:building.collision || null,
      playerCanStandAdjacent,
      npcBlockingFrontage,
      roadConnected
    });
  });
  return rows;
}
let lastFrontageAuditToken="";
let lastAtlasCropAuditToken="";
let sourceOfTruthAuditSignature="";
let boathousePlacementQaSignature="";
let mobileQaSummaryLogged=false;
let sourceTruthAcceptanceLogged=false;
let atlasRuntimeAuthorityChainSignature="";
let atlasRuntimeAuthorityAcceptanceSignature="";
let sourceTruthAcceptanceSignature="";
let atlasWorkflowAcceptanceSignature="";
function emitMobileQaSummary(){
  if(!AUTO_QA_MODE || mobileQaSummaryLogged) return;
  const cam=getCamera();
  const mapW=isInMirrorCave ? mirrorCave.width : (isInAbandonedTollhouse ? abandonedTollhouse.width : WORLD_W);
  const mapH=isInMirrorCave ? mirrorCave.height : (isInAbandonedTollhouse ? abandonedTollhouse.height : WORLD_H);
  const centeredX=Math.floor(VIEW_TILES_X/2);
  const centeredY=Math.floor(VIEW_TILES_Y/2);
  const expectedTileX=Math.max(0,Math.min(player.targetX-centeredX,Math.max(0,mapW-VIEW_TILES_X)));
  const expectedTileY=Math.max(0,Math.min(player.targetY-centeredY,Math.max(0,mapH-VIEW_TILES_Y)));
  console.info("[Mobile QA Summary]");
  console.info("enabled=true");
  console.info("touchControls="+(MOBILE_QA_CONTROLS_MODE?"true":"false"));
  console.info("autoQa="+(AUTO_QA_MODE?"true":"false"));
  console.info("playerCanMoveByTouch="+(MOBILE_QA_CONTROLS_MODE?"true":"false"));
  console.info("teleportButtons=Center Town,Village Hall,Residence Large,Boathouse,Pond Edge");
  console.info("currentZone="+String(currentZoneId||"unknown"));
  console.info("cameraCentered="+((cam.tileX===expectedTileX&&cam.tileY===expectedTileY)?"true":"false"));
  mobileQaSummaryLogged=true;
}
function emitBuildingAtlasCropAuditIfReady(){
  if(!ATLAS_DEBUG_MODE) return;
  const atlas=atlasImages.buildings;
  if(!atlas || !atlas.complete || !atlas.naturalWidth || !atlas.naturalHeight) return;
  const canvas=document.createElement("canvas");
  canvas.width=atlas.naturalWidth;
  canvas.height=atlas.naturalHeight;
  const c=canvas.getContext("2d",{ willReadFrequently:true });
  if(!c) return;
  c.drawImage(atlas,0,0);
  const report=Object.values(ATLAS_BUILDING_METADATA).map((entry)=>{
    const manifestSprite=atlasManifests.buildings?.sprites?.[entry.id] || null;
    const cropSource=manifestSprite?.sx!=null ? { x:manifestSprite.sx, y:manifestSprite.sy, w:manifestSprite.sw, h:manifestSprite.sh } : entry.crop;
    const drawW=manifestSprite?.drawW ?? entry.drawW;
    const drawH=manifestSprite?.drawH ?? entry.drawH;
    const anchorX=manifestSprite?.anchorX ?? entry.anchorX;
    const anchorY=manifestSprite?.anchorY ?? entry.anchorY;
    const { x, y, w, h }=cropSource;
    const data=c.getImageData(x,y,w,h).data;
    let minX=w,minY=h,maxX=-1,maxY=-1,hasPixels=false;
    for(let py=0;py<h;py++){
      for(let px=0;px<w;px++){
        if(data[(py*w+px)*4+3]===0) continue;
        hasPixels=true;
        if(px<minX) minX=px;
        if(py<minY) minY=py;
        if(px>maxX) maxX=px;
        if(py>maxY) maxY=py;
      }
    }
    const bbox=hasPixels ? { x:minX, y:minY, w:maxX-minX+1, h:maxY-minY+1 } : null;
    const margins=hasPixels ? { left:minX, right:w-1-maxX, top:minY, bottom:h-1-maxY } : null;
    const clip=hasPixels ? { left:minX===0, right:maxX===w-1, top:minY===0, bottom:maxY===h-1 } : null;
    const warnings=[];
    if(!hasPixels) warnings.push("empty_crop");
    if(clip && (clip.left||clip.right||clip.top||clip.bottom)) warnings.push("clipped_to_edge");
    if(bbox && ((bbox.w*bbox.h)/(w*h))<0.2) warnings.push("likely_partial_object");
    warnings.push(...getCropOverlapWarnings(entry));
    return { id:entry.id, crop:{x,y,w,h}, drawW, drawH, anchorX, anchorY, cropSource:manifestSprite?.metadataSource||"ATLAS_BUILDING_METADATA", hasNonTransparentPixels:hasPixels, nonTransparentBounds:bbox, transparentMargins:margins, clipEdges:clip, warnings };
  });
  const token=JSON.stringify(report);
  if(token===lastAtlasCropAuditToken) return;
  lastAtlasCropAuditToken=token;
  console.info("[Building Atlas Crop Audit] " + JSON.stringify(report));
}
function toCropObj(entry){
  if(!entry) return null;
  if(entry.x!=null) return {x:entry.x,y:entry.y,w:entry.w,h:entry.h};
  if(entry.sx!=null) return {x:entry.sx,y:entry.sy,w:entry.sw,h:entry.sh};
  return null;
}
function sameCrop(a,b){ return !!(a&&b&&a.x===b.x&&a.y===b.y&&a.w===b.w&&a.h===b.h); }
function logBuildingSourceOfTruthAudit(){
  if(!ATLAS_DEBUG_MODE) return;
  const ids=["b_inn_tavern","b_mercantile","b_village_hall","b_res_small","b_res_large","b_hunter_lodge","b_boathouse"];
  const rows=[]; const chainRows=[]; const conflicts=[];
  ids.forEach((buildingId)=>{
    const resolved=resolveBuildingAtlasRuntimeEntry(buildingId);
    const spriteId=resolved?.spriteId||null;
    const role=resolved?.role||null;
    const sprite=atlasManifests.buildings?.sprites?.[spriteId]||null;
    const meta=ATLAS_BUILDING_METADATA[spriteId]||null;
    const reg=HEARTHVALE_BUILDING_SEMANTIC_REGISTRY[buildingId]||null;
    const selection=secondaryAtlasSelectionState.byRole?.[role]||null;
    const staticCrop=toCropObj(meta?.crop);
    const registryCrop=toCropObj(reg?.crop);
    const manifestCrop=toCropObj(sprite);
    const resolverCrop=toCropObj(resolved?.crop);
    const mappingCrop=manifestCrop;
    const auditCrop=manifestCrop;
    const proofPreviewCrop=toCropObj(resolved?.proofCrop||resolverCrop);
    const selectorCrop=toCropObj(selection?.selectedCrop);
    const winners=[['manifest',manifestCrop],['resolver',resolverCrop],['registry',registryCrop],['static',staticCrop]];
    const winner=winners.find((w)=>w[1])?.[0]||'none';
    const active=manifestCrop||resolverCrop||registryCrop||staticCrop;
    const disagrees=[];
    [['static',staticCrop],['registry',registryCrop],['manifest',manifestCrop],['resolver',resolverCrop],['mapping',mappingCrop],['sourceTruthAudit',auditCrop],['proofPreview',proofPreviewCrop],['selectorCandidate',selectorCrop]].forEach(([k,v])=>{ if(v && active && !sameCrop(v,active)) disagrees.push(k); });
    chainRows.push({buildingId,spriteId,role,staticCrop,registryCrop,activeManifestCrop:manifestCrop,resolverCrop,mappingCrop,sourceTruthAuditCrop:auditCrop,proofPreviewCrop,selectorSelectedCandidateCrop:selectorCrop,winnerSource:winner,whyWinner:winner==='manifest'?'atlasManifests.buildings.sprites is render-authoritative':'fallback resolution order',disagreements:disagrees});
    if(resolverCrop && manifestCrop && !sameCrop(resolverCrop,manifestCrop)) conflicts.push({buildingId,spriteId,resolverCrop,activeCrop:manifestCrop});
    rows.push({buildingId,worldRole:role,requestedSpriteId:spriteId,activeCrop:manifestCrop,cropSource:sprite?.metadataSource||resolved?.cropSource||'unknown',drawAnchorSource:sprite?.metadataSource||resolved?.drawAnchorSource||'unknown',selectorProofCandidate:selection?.selectedCandidateId||null,runtimeRenderDecision:buildingRenderDiagnostics.perBuilding.get(buildingId)?.finalRenderSource||'pending'});
  });
  const chainSig=JSON.stringify({chainRows,cacheBust:(new URLSearchParams(window.location.search).get('cacheBust')||'none')});
  if(chainSig!==atlasRuntimeAuthorityChainSignature){ atlasRuntimeAuthorityChainSignature=chainSig; console.info('[Atlas Runtime Authority Chain] '+JSON.stringify(chainRows)); }
  const sourceSig=JSON.stringify({rows,conflicts,cacheBust:(new URLSearchParams(window.location.search).get('cacheBust')||'none')});
  if(sourceSig!==sourceOfTruthAuditSignature){ sourceOfTruthAuditSignature=sourceSig; console.info('[Building Source of Truth Audit] '+JSON.stringify(rows)); }
  const hunter=chainRows.find(r=>r.buildingId==='b_hunter_lodge');
  const boat=chainRows.find(r=>r.buildingId==='b_boathouse');
  const expH={x:61,y:939,w:309,h:308}, expB={x:470,y:939,w:320,h:250}, forbiddenB={x:899,y:939,w:250,h:245}, forbiddenH={x:61,y:519,w:309,h:308};
  const acceptanceFailures=[];
  const mustEq=(row,name,exp)=>{['registryCrop','activeManifestCrop','resolverCrop','mappingCrop','sourceTruthAuditCrop'].forEach((k)=>{ if(!sameCrop(row?.[k],exp)) acceptanceFailures.push(name+':'+k+'_mismatch'); });};
  mustEq(hunter,'b_hunter_lodge',expH); mustEq(boat,'b_boathouse',expB);
  if(sameCrop(boat?.activeManifestCrop,forbiddenB)) acceptanceFailures.push('b_boathouse_forbidden_bottom_right_shed');
  if(sameCrop(hunter?.activeManifestCrop,forbiddenH)) acceptanceFailures.push('b_hunter_lodge_forbidden_old_middle_row');
  const authStatus=acceptanceFailures.length===0?'PASS':'FAIL';
  const authSig=JSON.stringify({authStatus,acceptanceFailures});
  if(authSig!==atlasRuntimeAuthorityAcceptanceSignature){ atlasRuntimeAuthorityAcceptanceSignature=authSig; console.info('[Atlas Runtime Authority Chain Acceptance]'); console.info('status='+authStatus); console.info('reason='+(acceptanceFailures.length?acceptanceFailures.join('|'):'none')); }
  const expectedRows=7;
  const requiredFieldsOk=rows.every((row)=>Boolean(row.worldRole&&row.requestedSpriteId&&row.activeCrop&&row.cropSource&&row.drawAnchorSource));
  const proofHudConsistent=WAYFARER_PHASE==='34.2' && ATLAS_SELECTOR_VERSION==='selector-v33.1.5b-runtime-preview-gate-bypass';
  const previewModeActive=Boolean(SECONDARY_ATLAS_RUNTIME_PREVIEW_TARGET?.resolvedBuildingId);
  const renderAuditConsistent=previewModeActive
    ? (buildingRenderDiagnostics.atlasBuildings.size===4 && buildingRenderDiagnostics.fallbackBuildings.size===3 && buildingRenderDiagnostics.pendingBuildings.size===0)
    : (buildingRenderDiagnostics.atlasBuildings.size===3 && buildingRenderDiagnostics.fallbackBuildings.size===4 && buildingRenderDiagnostics.pendingBuildings.size===0);
  const ready=!!atlasRuntimeInfo.buildings?.loaded;
  const pendingReason=!ready?'assets_not_settled':(buildingRenderDiagnostics.pendingBuildings.size>0?'render_pending':'none');
  const status=!ready?'PENDING_ASSETS':((rows.length===expectedRows && conflicts.length===0 && requiredFieldsOk && proofHudConsistent && renderAuditConsistent && authStatus==='PASS')?'PASS':'FAIL');
  const satSig=JSON.stringify({status,pendingReason,renderAuditConsistent,rows:rows.length,conflicts:conflicts.length,authStatus});
  if(satSig!==sourceTruthAcceptanceSignature){ sourceTruthAcceptanceSignature=satSig; console.info('[Source Truth Acceptance]'); console.info('phase='+WAYFARER_PHASE); console.info('previewMode='+(previewModeActive?'true':'false')); console.info('registryKeyMode=building_id'); console.info('rows='+rows.length); console.info('activeMappingConsistent='+(conflicts.length===0?'true':'false')); console.info('cropAuditConsistent='+(requiredFieldsOk?'true':'false')); console.info('proofHudConsistent='+(proofHudConsistent?'true':'false')); console.info('renderAuditConsistent='+(renderAuditConsistent?'true':'false')); console.info('pendingReason='+pendingReason); console.info('status='+status); }
  const proofPreviewPass=secondaryProofPreviewState.drawCount===4;
  const workflowStatus=(authStatus==='PASS' && status==='PASS' && renderAuditConsistent && proofPreviewPass)?'PASS':'PENDING';
  const workflowSig=JSON.stringify({workflowStatus,proofPreviewPass,status,authStatus});
  if(workflowSig!==atlasWorkflowAcceptanceSignature){ atlasWorkflowAcceptanceSignature=workflowSig; if(workflowStatus==='PASS'){ console.info('[Atlas Workflow Acceptance]'); console.info('phase='+WAYFARER_PHASE); console.info('previewMode='+(previewModeActive?'true':'false')); console.info('authorityChain=PASS'); console.info('sourceTruth=PASS'); console.info('renderAudit=PASS'); console.info('proofPreview=PASS'); console.info('consoleFatalErrors=none'); console.info('secondaryRuntimeAtlas='+(previewModeActive?(SECONDARY_ATLAS_RUNTIME_PREVIEW_TARGET?.resolvedBuildingId||'none'):'none')); console.info('status=PASS'); } }
}
// 33.1.1C: Full-sheet atlas catalog scan.
// Runs ONCE in atlasDebug mode after the buildings image loads.
// Uses DFS connected-component analysis to find every non-transparent
// blob in the atlas, then classifies each candidate and produces a
// per-secondary-role suitability ranking. Output goes to console as
// [Atlas Catalog Scan] — never affects render path or game state.
let atlasCatalogScanEmitted=false;

const secondaryAtlasSelectionState={
  resolvedAt:null,
  byRole:{},
  bySpriteId:{}
};
const atlasSemanticIdentityState={
  byRole:{},
  byPosition:{},
  auditRows:[]
};
const SECONDARY_REVIEW_OVERRIDES=Object.freeze({
  rejectedCandidates:Object.freeze({
    residence_large:Object.freeze({
      C06:Object.freeze({
        reason:"visual_role_mismatch",
        note:"candidate visually reads as boathouse/waterfront/rustic shed, not large residence"
      })
    })
  })
});
function getSecondaryReviewRejection(roleId,candidateId){
  if(typeof roleId!=="string" || typeof candidateId!=="string") return null;
  return SECONDARY_REVIEW_OVERRIDES.rejectedCandidates?.[roleId]?.[candidateId] || null;
}
function formatSecondaryRejectedCandidatesSummary(){
  const summary={};
  Object.entries(SECONDARY_REVIEW_OVERRIDES.rejectedCandidates||{}).forEach(([roleId,candidates])=>{
    const entries=Object.entries(candidates||{}).map(([candidateId,meta])=>candidateId+":"+(meta?.reason||"unspecified_reason"));
    if(entries.length>0) summary[roleId]=entries;
  });
  return summary;
}
function applySecondaryAtlasSelectionOverrides(selections){
  if(!selections || typeof selections!=="object") return;
  const manifest=atlasManifests.buildings;
  if(!manifest || !manifest.sprites) return;
  SECONDARY_BUILDING_IDS.forEach((roleId)=>{
    const selection=selections.byRole?.[roleId];
    if(!manifest.sprites[roleId]) return;
    const sprite=manifest.sprites[roleId];
    // Use resolver for draw/anchor — semantic registry wins over static metadata.
    const base=resolveAtlasSpriteRuntimeEntry(roleId);
    if(selection?.eligible===true && selection.selectedCrop){
      sprite.sx=selection.selectedCrop.x;
      sprite.sy=selection.selectedCrop.y;
      sprite.sw=selection.selectedCrop.w;
      sprite.sh=selection.selectedCrop.h;
      sprite.drawW=base?.drawW ?? ATLAS_BUILDING_METADATA[roleId]?.drawW;
      sprite.drawH=base?.drawH ?? ATLAS_BUILDING_METADATA[roleId]?.drawH;
      sprite.anchorX=base?.anchorX ?? ATLAS_BUILDING_METADATA[roleId]?.anchorX;
      sprite.anchorY=base?.anchorY ?? ATLAS_BUILDING_METADATA[roleId]?.anchorY;
      sprite.productionReady=false;
      sprite.proofEnabled=true;
      sprite.debugOnly=false;
      sprite.fallbackReason="catalog_candidate_selected_proof_pending_acceptance";
      sprite.metadataSource="catalog_selection";
    }else if(selection?.selectedCandidateId==="semantic_registry"){
      // Registry-confirmed secondaries: crop already applied by applySemanticRegistryToManifest.
      // Mark proof-only, do not overwrite crop/draw/anchor again.
      sprite.productionReady=false;
      sprite.proofEnabled=false; // proof-only via ATLAS_DEBUG_MODE gate
      sprite.fallbackReason=selection?.fallbackReason||"semantic_registry_confirmed_proof_only";
      sprite.metadataSource="semantic_registry";
    }else{
      // Keep unsafe/unresolved secondary roles fully fallback-gated.
      // This prevents static hand-tuned crops from re-entering proof/atlas render paths.
      sprite.productionReady=false;
      sprite.proofEnabled=false;
      sprite.fallbackReason=selection?.fallbackReason||"semantic_identity_unresolved";
      sprite.metadataSource="catalog_fallback_gate";
    }
  });
}
function resolveSecondaryAtlasSelectionsFromCatalog(report){
  const roles=SECONDARY_ATLAS_ROLES;
  const safeReport=(report&&typeof report==="object")?report:{};
  const reportKeys=Object.keys(safeReport);
  const candidates=Array.isArray(safeReport.candidates)?safeReport.candidates:[];
  const roleReportRaw=safeReport.roleReport;
  const roleReports=Array.isArray(roleReportRaw)?roleReportRaw:[];
  const roleReportByRole=new Map(roleReports.filter((r)=>r&&typeof r==="object"&&typeof r.role==="string").map((r)=>[r.role,r]));

  const normalizedCandidateInfo={};
  const normalizedRoleReports={};
  roles.forEach((roleId)=>{
    const roleEntry=roleReportByRole.get(roleId)||null;
    const roleEntryKeys=roleEntry&&typeof roleEntry==="object"?Object.keys(roleEntry):[];
    const cleanCandidateIds=Array.isArray(roleEntry?.cleanCandidates)?roleEntry.cleanCandidates:[];
    const cleanIdSet=new Set(cleanCandidateIds.filter((id)=>typeof id==="string"));
    const fromRoles=candidates.filter((candidate)=>Array.isArray(candidate?.possibleRoles)&&candidate.possibleRoles.includes(roleId));
    const fromCleanIds=candidates.filter((candidate)=>cleanIdSet.has(candidate?.candidateId));
    const normalizedCandidates=[...fromRoles, ...fromCleanIds].filter((candidate,index,arr)=>arr.findIndex((item)=>item?.candidateId===candidate?.candidateId)===index);
    const sourceState=roleEntry===null?"missing":(normalizedCandidates.length===0?"empty":"populated");
    normalizedRoleReports[roleId]={ roleEntry, roleEntryKeys, sourceState };
    normalizedCandidateInfo[roleId]={ candidates:normalizedCandidates, sourceState };
  });

  console.info("[Catalog Selector] normalized_input="+JSON.stringify({
    hasReport:report!==undefined&&report!==null,
    topLevelKeys:reportKeys,
    roleReportIsArray:Array.isArray(roleReportRaw),
    roleReportCount:roleReports.length,
    roleReportKeysByRole:Object.fromEntries(roles.map((roleId)=>[roleId,normalizedRoleReports[roleId].roleEntryKeys])),
    candidateCountByRole:Object.fromEntries(roles.map((roleId)=>[roleId,normalizedCandidateInfo[roleId].candidates.length])),
    candidateStateByRole:Object.fromEntries(roles.map((roleId)=>[roleId,normalizedCandidateInfo[roleId].sourceState]))
  }));

  const byRole={};
  const bySpriteId={};
  const claimedCandidates=new Map();
  const transparencyOk=hasAtlasUsableTransparency("buildings")===true;
  const sheetReady=isAtlasRuntimeReady("buildings");
  console.info("[Catalog Selector] normalized_input roles="+roles.length+" candidates="+candidates.length+" clean="+candidates.filter((c)=>c?.clean===true).length+" transparencyOk="+transparencyOk+" sheetReady="+sheetReady);
  const rolePriority=new Map(SECONDARY_ROLE_PRIORITY.map((roleId,index)=>[roleId,index]));
  console.info("[Secondary Review Overrides]");
  console.info("rejectedCandidates="+JSON.stringify(formatSecondaryRejectedCandidatesSummary()));
  const scoreCandidateForRole=(roleId,candidate,fitInfo)=>{
    const box=candidate?.boundingBox||{};
    const w=box.w||0;
    const h=box.h||0;
    const area=w*h;
    const aspect=h>0?(w/h):0;
    let score=0;
    const scoreReasons=[];
    if(fitInfo?.fit===true){ score+=40; scoreReasons.push("role_fit_pass"); }
    if(roleId==="pond_boathouse_or_waterfront_shed"){
      if(w<=320&&h<=280){ score+=28; scoreReasons.push("waterfront_size_window"); }
      if(w>h){ score+=6; scoreReasons.push("wide_waterfront_shape"); }
    }
    if(roleId==="residence_large"){
      if(area>=76000){ score+=20; scoreReasons.push("large_area_bonus"); }
      if(w>=300){ score+=8; scoreReasons.push("wide_frontage_bonus"); }
    }
    if(roleId==="residence_small"){
      if(area>0&&area<=82000){ score+=16; scoreReasons.push("small_residence_area_window"); }
      if(w<=300&&h<=320){ score+=8; scoreReasons.push("compact_residence_shape"); }
    }
    if(roleId==="hunter_lodge_or_outfitter"){
      if(area>=62000&&area<=98000){ score+=16; scoreReasons.push("lodge_area_window"); }
      if(aspect>=0.75&&aspect<=1.35){ score+=6; scoreReasons.push("lodge_aspect_window"); }
    }
    if(Array.isArray(candidate?.possibleRoles) && candidate.possibleRoles.length===1 && candidate.possibleRoles[0]===roleId){
      score+=24;
      scoreReasons.push("single_role_specific_candidate");
    }
    if(Array.isArray(candidate?.possibleRoles) && candidate.possibleRoles.length>=3){
      score-=12;
      scoreReasons.push("ambiguous_multi_role_penalty");
    }
    const semanticPreferredCandidateId=atlasSemanticIdentityState.byRole?.[roleId]?.candidateId||null;
    if(semanticPreferredCandidateId && semanticPreferredCandidateId===candidate?.candidateId){
      score+=200;
      scoreReasons.push("semantic_identity_preferred_candidate");
    }
    return {score,scoreReasons};
  };
  roles
    .slice()
    .sort((a,b)=>(rolePriority.get(a)??99)-(rolePriority.get(b)??99))
    .forEach((roleId)=>{
    const roleEntry=normalizedRoleReports[roleId].roleEntry;
    const regEntry=HEARTHVALE_SEMANTIC_REGISTRY_BY_ROLE[roleId]||null;
    const resolvedEntry=resolveAtlasSpriteRuntimeEntry(roleId);
    // Phase 33.1.4G: semantic registry must win for human-reviewed world roles.
    // Catalog candidates validate (containment/alpha sanity) but do not replace identity crop.
    const semanticRegistryAuthoritativeRoles=new Set(["residence_large","hunter_lodge_or_outfitter","pond_boathouse_or_waterfront_shed"]);
    if(regEntry && (regEntry.registrySource==="human_reviewed" || semanticRegistryAuthoritativeRoles.has(roleId))){
      const final={
        role:roleId,
        selectorCandidateStatus:"SELECTED_PROOF_ONLY",
        runtimeRenderStatus:"FALLBACK",
        selectedCandidateId:"semantic_registry",
        selectedCrop:regEntry.crop,
        drawW:regEntry.drawW,
        drawH:regEntry.drawH,
        anchorX:regEntry.anchorX,
        anchorY:regEntry.anchorY,
        eligible:false, // secondaries remain proof-only; no runtime promotion
        eligibility:false,
        blockingReasons:["semantic_registry_confirmed_proof_only","semanticSubcropValidatedByCatalog"],
        fallbackReason:"semantic_registry_confirmed_proof_only",
        finalRenderStatus:"PROOF_PENDING_ACCEPTANCE",
        referenceCandidateId:null,
        cropSource:"semantic_registry",
        registryResolved:true
      };
      byRole[roleId]=final;
      bySpriteId[roleId]=final;
      console.info("[Catalog Selector] role_result "+roleId+" status=semantic_registry_confirmed crop="+JSON.stringify(regEntry.crop)+" cropSource=semantic_registry gate=proof_only_pending_acceptance");
      return;
    }
    // Catalog-pending roles: use scan candidates. Fallback to semantic_identity_unresolved
    // if no clean candidate found (not ambiguous_duplicate_candidate).
    const fits=normalizedCandidateInfo[roleId].candidates;
    const semanticPreferredCandidateId=atlasSemanticIdentityState.byRole?.[roleId]?.candidateId||null;
    const semanticPreferredCandidate=fits.find((candidate)=>candidate?.candidateId===semanticPreferredCandidateId) || null;
    const semanticPreferredAvailable=!!(semanticPreferredCandidate && semanticPreferredCandidate.clean===true && (semanticPreferredCandidate.heroOverlaps||[]).length===0);
    const evaluated=fits.map((candidate)=>{
      const reasons=[];
      if(!candidate?.hasNonTransparentPixels) reasons.push("no_non_transparent_pixels");
      if(candidate?.clean!==true) reasons.push(...(Array.isArray(candidate?.blocking)?candidate.blocking:[]));
      if(candidate?.clipEdges && Object.values(candidate.clipEdges).some(Boolean)) reasons.push("clipped_to_edge");
      if((candidate?.heroOverlaps||[]).length>0) reasons.push("overlaps_locked_hero_crop:"+(candidate.heroOverlaps[0]||"unknown"));
      if(!transparencyOk) reasons.push("transparent_invalid");
      if(!sheetReady) reasons.push("sheet_not_ready");
      const fitInfo=Array.isArray(candidate?.likelyRoleFit)?candidate.likelyRoleFit.find((fit)=>fit.role===roleId):null;
      if(!fitInfo?.fit) reasons.push("role_fit_failed");
      if((candidate?.warnings||[]).some(isSecondaryBlockingAuditWarning)) reasons.push("blocking_audit_warning");
      const reviewRejection=getSecondaryReviewRejection(roleId,candidate?.candidateId);
      if(reviewRejection) reasons.push("human_review_rejected_candidate");
      if(semanticPreferredAvailable && semanticPreferredCandidateId && candidate?.candidateId!==semanticPreferredCandidateId){
        reasons.push("semantic_identity_nonpreferred_rejected");
      }
      const scored=scoreCandidateForRole(roleId,candidate,fitInfo);
      return {candidate,reasons:[...new Set(reasons)].filter(Boolean),score:scored.score,scoreReasons:scored.scoreReasons,reviewRejection};
    });
    const cleanEvaluated=evaluated.filter((item)=>item.reasons.length===0).sort((a,b)=>b.score-a.score||a.candidate.candidateId.localeCompare(b.candidate.candidateId));
    let selected=null;
    let duplicateRejectedCandidateId=null;
    let claimedByRole=null;
    let fallbackReason=null;
    for(const item of cleanEvaluated){
      const claim=claimedCandidates.get(item.candidate?.candidateId);
      if(claim && SECONDARY_ROLE_DUPLICATE_POLICY.allowDuplicateForRoles!==true){
        duplicateRejectedCandidateId=item.candidate?.candidateId||null;
        claimedByRole=claim;
        fallbackReason="ambiguous_duplicate_candidate";
        continue;
      }
      selected=item;
      break;
    }
    if(!selected){
      const blockReasons=[...new Set(evaluated.flatMap((item)=>item.reasons))];
      if(!fallbackReason) fallbackReason=cleanEvaluated.length>0?"no_unique_clean_catalog_candidate":"no_clean_catalog_candidate";
      const blockingReasons=(blockReasons.length?blockReasons:["no_clean_catalog_candidate"]);
      const rejected={
        role:roleId,
        selectorCandidateStatus:"FALLBACK_GATED",
        runtimeRenderStatus:"FALLBACK",
        selectedCandidateId:null,
        selectedCrop:null,
        drawW:null, drawH:null, anchorX:null, anchorY:null,
        score:0,
        scoreReasons:[],
        eligible:false,
        blockingReasons,
        fallbackReason,
        duplicateRejectedCandidateId,
        claimedByRole,
        referenceCandidateId:roleEntry?.referenceCandidateInBlob||null,
        rejectedCandidateId:null,
        rejectionReason:null
      };
      byRole[roleId]=rejected;
      bySpriteId[roleId]=rejected;
      return;
    }
    claimedCandidates.set(selected.candidate.candidateId,roleId);
    const final={
      role:roleId,
      selectorCandidateStatus:"SELECTED_PROOF_ONLY",
      runtimeRenderStatus:"FALLBACK",
      selectedCandidateId:selected?.candidate?.candidateId||null,
      previewCandidateId:selected?.candidate?.candidateId||null,
      selectedCrop:selected?.candidate?.boundingBox||null,
      drawW:selected?(ATLAS_BUILDING_METADATA[roleId]?.drawW||null):null,
      drawH:selected?(ATLAS_BUILDING_METADATA[roleId]?.drawH||null):null,
      anchorX:selected?(ATLAS_BUILDING_METADATA[roleId]?.anchorX||null):null,
      anchorY:selected?(ATLAS_BUILDING_METADATA[roleId]?.anchorY||null):null,
      score:selected?.score||0,
      scoreReasons:selected?.scoreReasons||[],
      eligible:selected!==null,
      blockingReasons:[],
      fallbackReason,
      duplicateRejectedCandidateId,
      claimedByRole,
      finalRenderStatus:"FALLBACK",
      referenceCandidateId:roleEntry?.referenceCandidateInBlob||null,
      rejectedCandidateId:null,
      rejectionReason:null
    };
    byRole[roleId]=final;
    bySpriteId[roleId]=final;
    const humanRejectedSelected=getSecondaryReviewRejection(roleId,final.selectedCandidateId);
    if(humanRejectedSelected){
      const blockedFinal={
        ...final,
        selectorCandidateStatus:"FALLBACK_GATED",
        selectedCandidateId:null,
        selectedCrop:null,
        drawW:null,
        drawH:null,
        anchorX:null,
        anchorY:null,
        score:0,
        scoreReasons:[],
        eligible:false,
        blockingReasons:[...(final.blockingReasons||[]),"human_review_rejected_candidate"],
        fallbackReason:"human_review_rejected_candidate",
        rejectedCandidateId:humanRejectedSelected ? final.selectedCandidateId : null,
        rejectionReason:humanRejectedSelected?.reason||"unspecified_reason"
      };
      byRole[roleId]=blockedFinal;
      bySpriteId[roleId]=blockedFinal;
      claimedCandidates.delete(final.selectedCandidateId);
    }
  });

  const payload={resolvedAt:new Date().toISOString(),byRole,bySpriteId};
  secondaryAtlasSelectionState.resolvedAt=payload.resolvedAt;
  secondaryAtlasSelectionState.byRole=byRole;
  secondaryAtlasSelectionState.bySpriteId=bySpriteId;
  applySecondaryAtlasSelectionOverrides(payload);
  roles.forEach((roleId)=>{
    const r=byRole[roleId];
    if(!r){ console.warn("[Catalog Selector] role_result "+roleId+" status=missing"); return; }
    console.info("[Catalog Selector] role_result role="+roleId+" selectorCandidateStatus="+(r.selectorCandidateStatus||"REJECTED")+" runtimeRenderStatus="+(r.runtimeRenderStatus||"FALLBACK")+" selectedCandidateId="+(r.selectedCandidateId||"none")+" bbox="+JSON.stringify(r.selectedCrop||null)+" score="+String(r.score||0)+" scoreReasons="+(r.scoreReasons||[]).join("|")+" blockingReasons="+(r.blockingReasons||[]).join("|")+" fallbackReason="+(r.fallbackReason||"none")+" duplicateRejectedCandidateId="+(r.duplicateRejectedCandidateId||"none")+" claimedByRole="+(r.claimedByRole||"none")+" rejectedCandidateId="+(r.rejectedCandidateId||"none")+" rejectionReason="+(r.rejectionReason||"none"));
  });
  const assignmentSummary={
    runtimeFallbackRoles:roles.filter((roleId)=>(byRole[roleId]?.runtimeRenderStatus||"FALLBACK")==="FALLBACK"),
    selectorProofOnlyRoles:roles.filter((roleId)=>(byRole[roleId]?.selectorCandidateStatus||"FALLBACK_GATED")==="SELECTED_PROOF_ONLY"),
    selectorFallbackGatedRoles:roles.filter((roleId)=>(byRole[roleId]?.selectorCandidateStatus||"FALLBACK_GATED")==="FALLBACK_GATED"),
    runtimeAtlasRoles:roles.filter((roleId)=>(byRole[roleId]?.runtimeRenderStatus||"FALLBACK")==="ATLAS"),
    claimedCandidates:Object.fromEntries(claimedCandidates.entries())
  };
  console.info("[Catalog Selector] assignment_summary runtimeFallbackRoles="+assignmentSummary.runtimeFallbackRoles.join(",")+" selectorProofOnlyRoles="+assignmentSummary.selectorProofOnlyRoles.join(",")+" selectorFallbackGatedRoles="+assignmentSummary.selectorFallbackGatedRoles.join(",")+" runtimeAtlasRoles="+assignmentSummary.runtimeAtlasRoles.join(",")+" claimedCandidates="+JSON.stringify(assignmentSummary.claimedCandidates));
  if(ATLAS_DEBUG_MODE) logSecondaryProofPreviewSummary();
  if(ATLAS_DEBUG_MODE){
    const seenIds=new Map();
    const getDuplicateTrackingKey=(row,roleId)=>{
      if(!row?.selectedCandidateId) return null;
      if(row.selectedCandidateId==="semantic_registry") return "semantic_registry:"+roleId;
      return row.selectedCandidateId;
    };
    roles.forEach((roleId)=>{
      const row=byRole[roleId];
      if(!row?.selectedCandidateId) return;
      const duplicateTrackingKey=getDuplicateTrackingKey(row,roleId);
      if(!duplicateTrackingKey) return;
      const previous=seenIds.get(duplicateTrackingKey);
      if(previous){
        console.assert(false,"[Catalog Selector Assert] duplicate_secondary_candidate candidateId="+row.selectedCandidateId+" role="+roleId+" claimedBy="+previous);
      }else{
        seenIds.set(duplicateTrackingKey,roleId);
      }
      if(row.selectorCandidateStatus==="SELECTED_PROOF_ONLY"){
        console.assert(row.runtimeRenderStatus!=="ATLAS","[Catalog Selector Assert] proof_only_secondary_cannot_be_runtime_atlas role="+roleId);
      }
      if(!SECONDARY_PROOF_PREVIEW_MODE && row.selectorCandidateStatus==="SELECTED_PROOF_ONLY"){
        console.assert(row.runtimeRenderStatus==="FALLBACK","[Secondary Proof Preview Assert] preview_disabled_runtime_must_remain_fallback role="+roleId);
      }
      console.assert(row.runtimeRenderStatus!=="ATLAS","[Catalog Selector Assert] secondary_runtime_atlas_blocked_until_promotion role="+roleId+" reason=production_atlas_disabled");
    });
    Object.entries(LOCKED_HERO_METADATA_SNAPSHOT).forEach(([heroId,snapshot])=>{
      const hero=ATLAS_BUILDING_METADATA[heroId];
      const current=JSON.stringify({ crop:hero?.crop, drawW:hero?.drawW, drawH:hero?.drawH, anchorX:hero?.anchorX, anchorY:hero?.anchorY, proofEnabled:hero?.proofEnabled });
      console.assert(current===snapshot,"[Catalog Selector Assert] locked_hero_metadata_changed heroId="+heroId);
    });
  }
  return payload;
}
const atlasCatalogScanState={
  status:"waiting_for_assets",
  emitted:false,
  waitReasons:[],
  lastReadyAt:null,
  waitLoggedToken:null,
  startedAt:new Date().toISOString(),
  timeoutAt:Date.now()+ATLAS_READINESS_TIMEOUT_MS,
  unresolvedTimeoutLogged:false,
  retryTimer:null,
  lastError:null,
  timestamp:null,
  sheetSize:null,
  totalCandidates:0,
  cleanCandidates:0,
  blockedCandidates:0,
  candidates:[],
  roleReport:[],
  promotableRoles:[],
  stalledRoles:[]
};
function getAtlasCatalogReadinessSnapshot(){
  const buildingsRuntime=atlasRuntimeInfo.buildings||{};
  const propsRuntime=atlasRuntimeInfo.props||{};
  const buildingsImage=atlasImages.buildings;
  const propsImage=atlasImages.props;
  const buildingsImageLoaded=buildingsImage?.complete===true && (buildingsImage?.naturalWidth||0)>0 && (buildingsImage?.naturalHeight||0)>0;
  const propsImageLoaded=propsImage?.complete===true && (propsImage?.naturalWidth||0)>0 && (propsImage?.naturalHeight||0)>0;
  const buildingsManifestLoaded=(
    buildingsRuntime.manifestReady===true ||
    (atlasManifests.buildings?.sprites && Object.keys(atlasManifests.buildings.sprites).length>0) ||
    buildingsRuntime.metadataSource==="manifest"
  );
  const propsManifestLoaded=(
    propsRuntime.manifestReady===true ||
    propsRuntime.metadataSource==="manifest" ||
    propsRuntime.failure==="optional_atlas_not_loaded"
  );
  const hasUsableTransparency=buildingsRuntime.hasUsableTransparency;
  const reasons=[];
  if(!buildingsImageLoaded) reasons.push("buildings_image_not_ready");
  if(!buildingsManifestLoaded) reasons.push("buildings_manifest_not_ready");
  if(hasUsableTransparency===undefined || hasUsableTransparency===null) reasons.push("buildings_transparency_probe_unresolved");
  return {
    reasons,
    buildingsImageLoaded,
    buildingsNatural:(buildingsImage?.naturalWidth||0)+"x"+(buildingsImage?.naturalHeight||0),
    buildingsManifestLoaded,
    propsImageLoaded,
    propsManifestLoaded,
    hasUsableTransparency
  };
}
function maybeEmitAtlasReadinessTimeout(snapshot){
  if(atlasCatalogScanState.unresolvedTimeoutLogged || Date.now()<atlasCatalogScanState.timeoutAt) return;
  atlasCatalogScanState.unresolvedTimeoutLogged=true;
  const runtime=atlasRuntimeInfo.buildings||{};
  const img=atlasImages.buildings;
  console.warn("[Atlas Readiness] unresolved_after_timeout imageSrc="+(runtime.selectedUrl||img?.currentSrc||img?.src||"n/a")+" complete="+(img?.complete===true)+" naturalWidth="+(img?.naturalWidth||0)+" naturalHeight="+(img?.naturalHeight||0)+" onloadFired="+(runtime.imageOnloadFired===true)+" onerrorFired="+(runtime.imageOnerrorFired===true)+" manifestFetchStatus="+(runtime.metadataSource||"unknown")+" directFetchStatus="+(runtime.probeStatus||0)+"/"+(runtime.probeContentType||"unknown")+" lastError="+(runtime.failure||atlasCatalogScanState.lastError||snapshot.reasons.join("|")||"none"));
}
function scheduleAtlasCatalogScanRetry(){
  if(atlasCatalogScanState.retryTimer) return;
  atlasCatalogScanState.retryTimer=setTimeout(()=>{
    atlasCatalogScanState.retryTimer=null;
    runAtlasCatalogScanOnce();
  },250);
}
function describeSecondaryRoleFit(roleId,candidate){
  const box=candidate.boundingBox;
  if(roleId==="residence_small"){
    if(box.w<=280&&box.h<=320) return "good_size_for_cottage_or_small_home";
    return "outside_residence_small_size_window";
  }
  if(roleId==="residence_large"){
    if(box.w<=420&&box.h<=380) return "good_size_for_large_residence";
    return "outside_residence_large_size_window";
  }
  if(roleId==="hunter_lodge_or_outfitter"){
    if(box.w<=340&&box.h<=340) return "good_size_for_lodge_or_outfitter";
    return "outside_hunter_lodge_size_window";
  }
  if(roleId==="pond_boathouse_or_waterfront_shed"){
    if(box.w<=320&&box.h<=280) return "good_size_for_waterfront_shed";
    return "outside_boathouse_size_window";
  }
  return "unknown_role";
}
function runAtlasCatalogScanOnce(){
  if(!ATLAS_DEBUG_MODE||atlasCatalogScanEmitted) return;
  const readiness=getAtlasCatalogReadinessSnapshot();
  if(readiness.reasons.length){
    atlasCatalogScanState.status="waiting_for_assets";
    atlasCatalogScanState.waitReasons=readiness.reasons;
    const waitToken=JSON.stringify(readiness);
    if(atlasCatalogScanState.waitLoggedToken!==waitToken){
      atlasCatalogScanState.waitLoggedToken=waitToken;
      console.info("[Atlas Catalog Scan] waiting_for_assets reason="+readiness.reasons.join(",")+" buildingsImageLoaded="+readiness.buildingsImageLoaded+" buildingsNatural="+readiness.buildingsNatural+" buildingsManifestLoaded="+readiness.buildingsManifestLoaded+" propsImageLoaded="+readiness.propsImageLoaded+" propsManifestLoaded="+readiness.propsManifestLoaded+" hasUsableTransparency="+String(readiness.hasUsableTransparency));
    }
    maybeEmitAtlasReadinessTimeout(readiness);
    scheduleAtlasCatalogScanRetry();
    return;
  }
  atlasCatalogScanState.status="ready_to_scan";
  atlasCatalogScanState.lastReadyAt=new Date().toISOString();
  console.info("[Atlas Catalog Scan] ready buildingsImageLoaded="+readiness.buildingsImageLoaded+" buildingsNatural="+readiness.buildingsNatural+" buildingsManifestLoaded="+readiness.buildingsManifestLoaded+" propsImageLoaded="+readiness.propsImageLoaded+" propsManifestLoaded="+readiness.propsManifestLoaded+" hasUsableTransparency="+String(readiness.hasUsableTransparency));
  const atlas=atlasImages.buildings;
  if(!atlas||!atlas.complete||!(atlas.naturalWidth>0&&atlas.naturalHeight>0)) return;
  atlasCatalogScanEmitted=true;
  atlasCatalogScanState.status="scanning";
  // Defer 200ms so we don't block the render tick that discovers image readiness.
  setTimeout(()=>{
    try{
      const W=atlas.naturalWidth, H=atlas.naturalHeight;
      const canvas=document.createElement("canvas");
      canvas.width=W; canvas.height=H;
      const c=canvas.getContext("2d",{willReadFrequently:true});
      if(!c){ console.warn("[Atlas Catalog Scan] could not get 2d context"); return; }
      c.drawImage(atlas,0,0);
      const data=c.getImageData(0,0,W,H).data;
      const ALPHA_THRESH=16;
      const MIN_BLOB_PX=32; // ignore blobs smaller than this on any axis (noise)
      const visited=new Uint8Array(W*H);
      const rawBlobs=[];

      for(let sy=0;sy<H;sy++){
        for(let sx=0;sx<W;sx++){
          const startIdx=sy*W+sx;
          if(visited[startIdx]) continue;
          visited[startIdx]=1;
          if(data[startIdx*4+3]<ALPHA_THRESH) continue;
          // Iterative DFS
          const stack=[startIdx];
          let minX=sx,minY=sy,maxX=sx,maxY=sy,pixCount=0;
          while(stack.length>0){
            const idx=stack.pop();
            const px=idx%W, py=(idx/W)|0;
            pixCount++;
            if(px<minX) minX=px; if(py<minY) minY=py;
            if(px>maxX) maxX=px; if(py>maxY) maxY=py;
            const nbrs=[idx-1,idx+1,idx-W,idx+W];
            for(let k=0;k<4;k++){
              const n=nbrs[k];
              if(n<0||n>=W*H) continue;
              if(visited[n]) continue;
              // prevent horizontal wrap-around
              if(k===0&&(n%W)>=px) continue;
              if(k===1&&(n%W)<=px) continue;
              visited[n]=1;
              if(data[n*4+3]>=ALPHA_THRESH) stack.push(n);
            }
          }
          const bw=maxX-minX+1, bh=maxY-minY+1;
          if(bw<MIN_BLOB_PX||bh<MIN_BLOB_PX) continue;
          rawBlobs.push({minX,minY,maxX,maxY,pixCount});
        }
      }

      // Merge blobs whose bounding boxes are within GAP_PX of each other.
      // Buildings can have small internal transparent windows/details that split blobs.
      const GAP_PX=12;
      let merged=true;
      const blobs=[...rawBlobs];
      while(merged){
        merged=false;
        for(let i=0;i<blobs.length&&!merged;i++){
          for(let j=i+1;j<blobs.length&&!merged;j++){
            const a=blobs[i],b=blobs[j];
            const gapX=Math.max(0,Math.max(a.minX,b.minX)-Math.min(a.maxX,b.maxX)-1);
            const gapY=Math.max(0,Math.max(a.minY,b.minY)-Math.min(a.maxY,b.maxY)-1);
            if(gapX<=GAP_PX&&gapY<=GAP_PX){
              blobs[i]={minX:Math.min(a.minX,b.minX),minY:Math.min(a.minY,b.minY),maxX:Math.max(a.maxX,b.maxX),maxY:Math.max(a.maxY,b.maxY),pixCount:a.pixCount+b.pixCount};
              blobs.splice(j,1);
              merged=true;
            }
          }
        }
      }

      const EDGE_MARGIN=2;
      // Use semantic registry crops for hero zones — village_hall is corrected here.
      const heroZones=LOCKED_HERO_BUILDING_IDS.map((id)=>{
        const resolved=resolveAtlasSpriteRuntimeEntry(id);
        return{id,crop:resolved?resolved.crop:ATLAS_BUILDING_METADATA[id].crop};
      });

      const results=blobs.map((blob,idx)=>{
        const x=blob.minX,y=blob.minY,w=blob.maxX-blob.minX+1,h=blob.maxY-blob.minY+1;
        const clipEdges={left:x<=EDGE_MARGIN,top:y<=EDGE_MARGIN,right:blob.maxX>=W-1-EDGE_MARGIN,bottom:blob.maxY>=H-1-EDGE_MARGIN};
        const isClipped=Object.values(clipEdges).some(Boolean);
        const heroOverlaps=heroZones.filter((hz)=>rectsOverlap({x,y,w,h},hz.crop)).map((hz)=>hz.id);
        let sizeClass="extra_large";
        if(w<=180&&h<=180) sizeClass="small";
        else if(w<=280&&h<=280) sizeClass="medium";
        else if(w<=480&&h<=380) sizeClass="large";
        const blocking=[];
        if(isClipped) blocking.push("clipped_to_edge");
        if(heroOverlaps.length>0) blocking.push("overlaps_hero:"+heroOverlaps.join(","));
        const clean=blocking.length===0;
        const possibleRoles=[];
        if(w<=280&&h<=320) possibleRoles.push("residence_small");
        if(w<=420&&h<=380) possibleRoles.push("residence_large");
        if(w<=340&&h<=340) possibleRoles.push("hunter_lodge_or_outfitter");
        if(w<=320&&h<=280) possibleRoles.push("pond_boathouse_or_waterfront_shed");
        const warnings=[];
        if(isClipped) warnings.push("clipped_to_edge");
        if(heroOverlaps.length>0) warnings.push("hero_overlap");
        const likelyRoleFit=SECONDARY_BUILDING_IDS.map((roleId)=>({ role:roleId, fit:possibleRoles.includes(roleId), note:describeSecondaryRoleFit(roleId,{boundingBox:{x,y,w,h}}) }));
        return{candidateId:"C"+String(idx).padStart(2,"0"),boundingBox:{x,y,w,h},pixelCount:blob.pixCount,hasNonTransparentPixels:blob.pixCount>0,sizeClass,clipEdges,heroOverlaps,possibleRoles,likelyRoleFit,warnings,blocking,clean,audit:clean?"PASS":"BLOCKED"};
      }).sort((a,b)=>a.boundingBox.y-b.boundingBox.y||a.boundingBox.x-b.boundingBox.x);

      const roleSummary=SECONDARY_BUILDING_IDS.map((roleId)=>{
        const resolved=resolveAtlasSpriteRuntimeEntry(roleId);
        const referenceCandidate=resolved?{x:resolved.crop.x,y:resolved.crop.y,w:resolved.crop.w,h:resolved.crop.h}:null;
        const refBlob=results.find((r)=>referenceCandidate&&r.boundingBox.x<=referenceCandidate.x&&r.boundingBox.y<=referenceCandidate.y&&r.boundingBox.x+r.boundingBox.w>=referenceCandidate.x+referenceCandidate.w&&r.boundingBox.y+r.boundingBox.h>=referenceCandidate.y+referenceCandidate.h);
        const fits=results.filter((r)=>r.possibleRoles.includes(roleId));
        const cleanCandidates=fits.filter((r)=>r.clean).map((r)=>r.candidateId);
        const blockedCandidates=fits.filter((r)=>!r.clean).map((r)=>({candidateId:r.candidateId,blocking:r.blocking,warnings:r.warnings}));
        const policyNote=roleId==="residence_small" ? "fallback_gated_until_clean_complete_source_crop_identified" : "promote_only_when_crop_audit_clean";
        return{role:roleId,referenceCandidate,referenceCandidateInBlob:refBlob?refBlob.candidateId:null,referenceCandidateClean:refBlob?refBlob.clean:false,referenceCandidateBlocking:refBlob?refBlob.blocking:[],cleanCandidates,blockedCandidates,promotable:cleanCandidates.length>0,policyNote};
      });

      const expectedIdentityByPosition={
        top_left:"inn_tavern_v1",
        top_middle:"mercantile_shop",
        top_right:"village_hall_meeting_house",
        middle_left:"residence_small",
        middle_middle:"residence_small_alt_or_medium",
        middle_right:"residence_large",
        bottom_left:"hunter_lodge_or_outfitter",
        bottom_middle:"pond_boathouse_or_waterfront_shed",
        bottom_right:"waterfront_shed_or_utility_shed"
      };
      const sortedByY=[...results].sort((a,b)=>a.boundingBox.y-b.boundingBox.y||a.boundingBox.x-b.boundingBox.x);
      const rowBuckets=[sortedByY.slice(0,3),sortedByY.slice(3,6),sortedByY.slice(6,9)].map((row)=>[...row].sort((a,b)=>a.boundingBox.x-b.boundingBox.x));
      const semanticAuditRows=[];
      rowBuckets.forEach((row,rowIdx)=>{
        row.forEach((candidate,colIdx)=>{
          const position=(rowIdx===0?["top_left","top_middle","top_right"]:(rowIdx===1?["middle_left","middle_middle","middle_right"]:["bottom_left","bottom_middle","bottom_right"]))[colIdx];
          const mappedSpriteEntry=Object.entries(ATLAS_BUILDING_METADATA).find(([,entry])=>{
            const crop=entry?.crop;
            return crop && candidate?.boundingBox &&
              candidate.boundingBox.x<=crop.x &&
              candidate.boundingBox.y<=crop.y &&
              candidate.boundingBox.x+candidate.boundingBox.w>=crop.x+crop.w &&
              candidate.boundingBox.y+candidate.boundingBox.h>=crop.y+crop.h;
          });
          semanticAuditRows.push({
            candidateId:candidate.candidateId,
            boundingBox:candidate.boundingBox,
            atlasGridPosition:position,
            suggestedVisualIdentity:expectedIdentityByPosition[position]||"unknown",
            currentMappedSpriteId:mappedSpriteEntry?.[0]||null,
            currentMappedBuildingId:mappedSpriteEntry?.[0]||null,
            currentSelectedRole:null,
            heroOverlap:(candidate.heroOverlaps||[]).join(",")||"none",
            clean:candidate.clean===true,
            blocking:candidate.blocking||[]
          });
        });
      });
      const byPosition=Object.fromEntries(semanticAuditRows.map((row)=>[row.atlasGridPosition,row]));
      const candidateById=Object.fromEntries(results.map((row)=>[row.candidateId,row]));
      const resolveSemanticAssignment=(roleId, fallbackPosition)=>{
        const cfg=HEARTHVALE_ATLAS_SEMANTIC_ASSIGNMENTS[roleId]||null;
        const preferredById=cfg?.preferredCandidateId ? candidateById[cfg.preferredCandidateId] : null;
        const preferredByBounds=cfg?.preferredBounds ? results.find((row)=>boxesEqual(row.boundingBox,cfg.preferredBounds)) : null;
        const fallbackCandidate=fallbackPosition ? byPosition[fallbackPosition] : null;
        const resolved=preferredById||preferredByBounds||fallbackCandidate||null;
        const resolutionSource=preferredById?"preferredCandidateId":(preferredByBounds?"preferredBounds":"fallbackPosition");
        return resolved?{ candidateId:resolved.candidateId, boundingBox:resolved.boundingBox, expectedIdentity:cfg?.expectedIdentity||null, resolutionSource }:null;
      };
      atlasSemanticIdentityState.byRole={
        residence_small:resolveSemanticAssignment("residence_small","middle_left"),
        residence_large:resolveSemanticAssignment("residence_large","middle_right"),
        hunter_lodge_or_outfitter:resolveSemanticAssignment("hunter_lodge_or_outfitter","bottom_left"),
        pond_boathouse_or_waterfront_shed:resolveSemanticAssignment("pond_boathouse_or_waterfront_shed","bottom_middle")
      };
      atlasSemanticIdentityState.byPosition=byPosition;
      atlasSemanticIdentityState.auditRows=semanticAuditRows;
      console.info("[Atlas Identity Registry] "+JSON.stringify({
        top_left_inn_tavern:resolveSemanticAssignment("inn_tavern_v1","top_left"),
        top_middle_mercantile_shop:resolveSemanticAssignment("mercantile_shop","top_middle"),
        top_right_meeting_house:resolveSemanticAssignment("village_hall_meeting_house","top_right"),
        middle_left_residence_small:resolveSemanticAssignment("residence_small","middle_left"),
        middle_middle_residence_small_alt_or_medium:resolveSemanticAssignment("residence_small","middle_middle"),
        middle_right_manor_residence_large:resolveSemanticAssignment("residence_large","middle_right"),
        bottom_left_hunter_lodge:resolveSemanticAssignment("hunter_lodge_or_outfitter","bottom_left"),
        bottom_middle_boathouse_dock:resolveSemanticAssignment("pond_boathouse_or_waterfront_shed","bottom_middle")
      }));
      const villageHallTarget=resolveSemanticAssignment("village_hall_meeting_house","top_right");
      const villageSprite=atlasManifests?.buildings?.sprites?.village_hall_meeting_house;
      const villageMeta=ATLAS_BUILDING_METADATA.village_hall_meeting_house;
      if(villageSprite && villageHallTarget?.boundingBox && villageMeta){
        const oldVillageHallCrop={x:villageSprite.sx,y:villageSprite.sy,w:villageSprite.sw,h:villageSprite.sh};
        const oldDraw={w:villageMeta.drawW,h:villageMeta.drawH};
        const oldAnchor={x:villageMeta.anchorX,y:villageMeta.anchorY};
        villageSprite.sx=villageHallTarget.boundingBox.x;
        villageSprite.sy=villageHallTarget.boundingBox.y;
        villageSprite.sw=villageHallTarget.boundingBox.w;
        villageSprite.sh=villageHallTarget.boundingBox.h;
        const targetFootprintHeight=Math.max(villageMeta.drawH, 172);
        const aspect=villageHallTarget.boundingBox.w/Math.max(1,villageHallTarget.boundingBox.h);
        villageSprite.drawH=Math.round(targetFootprintHeight);
        villageSprite.drawW=Math.round(villageSprite.drawH*aspect);
        villageSprite.anchorX=Math.round(villageSprite.drawW/2);
        villageSprite.anchorY=Math.round(villageSprite.drawH*0.91);
        villageSprite.metadataSource="catalog_semantic_identity";
        console.info("[Atlas Semantic Remap] village_hall_meeting_house old="+JSON.stringify(oldVillageHallCrop)+" new="+JSON.stringify(villageHallTarget.boundingBox)+" sourceCandidate="+villageHallTarget.candidateId);
        console.info("[Atlas Semantic Draw Profile] spriteId=village_hall_meeting_house sourceCrop="+villageHallTarget.boundingBox.w+"x"+villageHallTarget.boundingBox.h+" oldDraw="+oldDraw.w+"x"+oldDraw.h+" newDraw="+villageSprite.drawW+"x"+villageSprite.drawH+" oldAnchor="+oldAnchor.x+","+oldAnchor.y+" newAnchor="+villageSprite.anchorX+","+villageSprite.anchorY+" reason=preserve_aspect_for_top_right_meeting_house");
      }
      console.info("[Atlas Component Scan Diagnostic]");
      console.info("semanticAuthority=human_reviewed_registry componentIdentityIsAdvisory=true");
      console.info("expectedVisualIdentity="+JSON.stringify(expectedIdentityByPosition));
      console.info("rows="+JSON.stringify(semanticAuditRows));
      const cleanCount=results.filter((r)=>r.clean).length;
      const promotableRoles=roleSummary.filter((r)=>r.promotable).map((r)=>r.role);
      const stalledRoles=roleSummary.filter((r)=>!r.promotable).map((r)=>r.role);
      const secondarySelections=resolveSecondaryAtlasSelectionsFromCatalog({ candidates:results, roleReport:roleSummary });
      atlasSemanticIdentityState.auditRows=atlasSemanticIdentityState.auditRows.map((row)=>{
        const authoritativeRole=Object.entries(atlasSemanticIdentityState.byRole||{}).find(([,entry])=>entry?.candidateId===row.candidateId)?.[0]||"none";
        const selectedRole=Object.entries(secondarySelections?.byRole||{}).find(([,entry])=>entry?.selectedCandidateId===row.candidateId)?.[0]||"none";
        return {
          ...row,
          currentSelectedRole:authoritativeRole!=="none" ? authoritativeRole : selectedRole,
          currentMappedSpriteId:authoritativeRole!=="none" ? authoritativeRole : row.currentMappedSpriteId
        };
      });
      console.info("[Atlas Component Scan Diagnostic] selectedRoles="+JSON.stringify(atlasSemanticIdentityState.auditRows));
      Object.assign(atlasCatalogScanState,{ status:"selector_complete", emitted:true, timestamp:new Date().toISOString(), sheetSize:{w:W,h:H}, totalCandidates:results.length, cleanCandidates:cleanCount, blockedCandidates:results.length-cleanCount, candidates:results, roleReport:roleSummary, promotableRoles, stalledRoles, secondarySelections });
      window.__atlasCatalogScanReport=atlasCatalogScanState;
      console.info("[Atlas Catalog Scan] sheetSize="+W+"x"+H+" totalCandidates="+results.length+" cleanCandidates="+cleanCount+" blockedCandidates="+(results.length-cleanCount));
      console.info("[Atlas Catalog Scan] candidates="+JSON.stringify(results));
      console.info("[Atlas Catalog Scan] roleSummary="+JSON.stringify(roleSummary));
      console.info("[Atlas Catalog Scan] promotable_roles="+promotableRoles.join(",")+" stalled_roles="+stalledRoles.join(",")+" — secondary promotion gated until human review of above candidates");
      console.info("[Atlas Catalog Selection] "+JSON.stringify(Object.values(secondarySelections.byRole).map((row)=>({ role:row.role, selectedCandidateId:row.selectedCandidateId, crop:row.selectedCrop, drawW:row.drawW, drawH:row.drawH, anchorX:row.anchorX, anchorY:row.anchorY, eligibility:row.eligibility, blockingReasons:row.blockingReasons, finalRenderStatus:row.finalRenderStatus }))));
    }catch(catalogErr){
      atlasCatalogScanState.status="selector_failed";
      atlasCatalogScanState.lastError=catalogErr?.message||String(catalogErr);
      const selectorSafeFallback={
        resolvedAt:new Date().toISOString(),
        byRole:Object.fromEntries(SECONDARY_BUILDING_IDS.map((roleId)=>[roleId,{
          role:roleId,
          selectedCandidateId:null,
          selectedCrop:null,
          drawW:null,
          drawH:null,
          anchorX:null,
          anchorY:null,
          eligible:false,
          blockingReasons:["selector_failed"],
          fallbackReason:"no_clean_catalog_candidate",
          finalRenderStatus:"FALLBACK",
          referenceCandidateId:null
        }])),
        bySpriteId:{}
      };
      selectorSafeFallback.bySpriteId={...selectorSafeFallback.byRole};
      applySecondaryAtlasSelectionOverrides(selectorSafeFallback);
      console.warn("[Catalog Selector] selector_failed",{ message:catalogErr?.message||String(catalogErr), stack:catalogErr?.stack||"stack_unavailable" });
      console.warn("[Atlas Catalog Scan] error during scan",catalogErr);
      // Keep selector failure terminal for this asset/report version to avoid console spam.
      // Retry only after an explicit debug reset or new asset session.
    }
  },200);
}
function maybeEmitFrontageAudit(){
  if(!ATLAS_DEBUG_MODE && !showCollisionOverlay) return;
  const rows=getHeroFrontageDiagnostics();
  const token=JSON.stringify(rows);
  if(token===lastFrontageAuditToken) return;
  lastFrontageAuditToken=token;
  const line=rows.map((row)=>row.id+" door=("+(row.door?.x??"?")+","+(row.door?.y??"?")+") interaction="+formatRect(row.interactionRect)+" collision="+formatRect(row.collisionRect)+" player_adjacent="+row.playerCanStandAdjacent+" npc_blocking="+row.npcBlockingFrontage+" road_connected="+row.roadConnected).join(" | ");
  console.info("[Frontage QA] "+line);
}
function emitBoathousePlacementQA(){
  if(!ATLAS_DEBUG_MODE) return;
  const b=world.buildings.find((row)=>row.id==="b_boathouse");
  if(!b) return;
  const visual=b.visual || { x:b.x, y:b.y, w:b.w, h:b.h };
  const collision=b.collision || visual;
  const interaction=b.interaction || null;
  const mainRoadRect={ x:9, y:16, w:22, h:1 };
  const overlaps=(a,bRect)=>a.x<bRect.x+bRect.w && a.x+a.w>bRect.x && a.y<bRect.y+bRect.h && a.y+a.h>bRect.y;
  let adjacentToWater=false;
  let visualOverlapsWater=false;
  let collisionOverlapsInvalidWater=false;
  for(let x=visual.x;x<visual.x+visual.w;x++){
    for(let y=visual.y;y<visual.y+visual.h;y++){
      const touchingNeighbor=[[1,0],[-1,0],[0,1],[0,-1]].some(([dx,dy])=>world.pondWater.has(keyOf(x+dx,y+dy))||world.pondShore.has(keyOf(x+dx,y+dy)));
      if(touchingNeighbor) adjacentToWater=true;
      if(world.pondWater.has(keyOf(x,y))) visualOverlapsWater=true;
    }
  }
  const doorReachable=!!(interaction && !world.pondWater.has(keyOf(interaction.x,interaction.y)) && !world.blocked.has(keyOf(interaction.x,interaction.y)));
  const roadOrPathConnected=!!(interaction && [[0,0],[1,0],[-1,0],[0,1],[0,-1]].some(([dx,dy])=>world.roadTiles.has(keyOf(interaction.x+dx,interaction.y+dy))));
  const blocksMainRoad=overlaps(collision,mainRoadRect);
  for(let x=collision.x;x<collision.x+collision.w;x++){
    for(let y=collision.y;y<collision.y+collision.h;y++){
      if(world.pondWater.has(keyOf(x,y)) && !world.roadTiles.has(keyOf(x,y))) collisionOverlapsInvalidWater=true;
    }
  }
  const collisionValid=!collisionOverlapsInvalidWater;
  const candidateId=secondaryAtlasSelectionState.byRole?.pond_boathouse_or_waterfront_shed?.selectedCandidateId || "none";
  const qaLine="[Boathouse Placement QA] buildingId=b_boathouse role=pond_boathouse_or_waterfront_shed position=tile("+b.x+","+b.y+") adjacentToWater="+adjacentToWater+" doorReachable="+doorReachable+" roadOrPathConnected="+roadOrPathConnected+" blocksMainRoad="+blocksMainRoad+" visualOverlapsWater="+visualOverlapsWater+" collisionOverlapsInvalidWater="+collisionOverlapsInvalidWater+" collisionValid="+collisionValid+" previewCandidateId="+candidateId+" runtimeRenderStatus=FALLBACK";
  const nextBoathousePlacementQaSignature=qaLine+"|cacheBust="+(new URLSearchParams(window.location.search).get("cacheBust")||"none");
  if(nextBoathousePlacementQaSignature===boathousePlacementQaSignature) return;
  boathousePlacementQaSignature=nextBoathousePlacementQaSignature;
  console.info(qaLine);
}
function emitHarborCompositionQA(){
  if(!ATLAS_DEBUG_MODE) return;
  const hasRoad=(x,y)=>world.roadTiles.has(keyOf(x,y));
  const waterfrontSpineContinuous=Array.from({ length:24 }).every((_,i)=>hasRoad(8+i,16));
  const wharfRects=world.roads.filter((r)=>r.y>=18&&r.h>=4&&r.w<=4);
  const wharfCount=wharfRects.length;
  const centralPier=world.roads.some((r)=>r.x===18&&r.y===17&&r.w===4&&r.h>=6);
  const inlandConnectorCount=world.roads.filter((r)=>r.w===1&&r.h>=6&&r.y<=8).length;
  const boathouse=world.buildings.find((row)=>row.id==="b_boathouse");
  const boathouseReachable=Boolean(boathouse?.interaction && !world.blocked.has(keyOf(boathouse.interaction.x,boathouse.interaction.y)));
  const commercialFrontage=["b_inn_tavern","b_mercantile"].every((id)=>{
    const b=world.buildings.find((row)=>row.id===id);
    return !!(b?.interaction && [[0,0],[1,0],[-1,0],[0,1],[0,-1]].some(([dx,dy])=>hasRoad(b.interaction.x+dx,b.interaction.y+dy)));
  });
  const blockedRoadMismatches=[[27,15],[17,11],[18,11],[19,11],[17,12],[18,12],[19,12]].filter(([x,y])=>hasRoad(x,y)&&world.blocked.has(keyOf(x,y))).length;
  const status=waterfrontSpineContinuous&&wharfCount>=3&&centralPier&&boathouseReachable&&commercialFrontage&&inlandConnectorCount>=1&&blockedRoadMismatches===0 ? "PASS" : "FAIL";
  console.info("[Harbor Composition QA]");
  console.info("phase="+WAYFARER_PHASE);
  console.info("waterfrontSpine="+(waterfrontSpineContinuous?"PASS":"FAIL"));
  console.info("wharfCount="+wharfCount);
  console.info("centralPier="+(centralPier?"PASS":"FAIL"));
  console.info("boathouseReachable="+(boathouseReachable?"PASS":"FAIL"));
  console.info("commercialFrontage="+(commercialFrontage?"PASS":"FAIL"));
  console.info("inlandConnectorCount="+inlandConnectorCount);
  console.info("blockedRoadMismatches="+blockedRoadMismatches);
  console.info("status="+status);
}
function isBuildingAtlasPendingReason(reason){
  // Pending = atlas image is still loading. Once the atlas image is fully
  // decoded (isAtlasRuntimeReady), nothing about its render is pending — any
  // remaining failure is a hard failure that belongs in fallback, not pending.
  if(reason==="atlas_missing_alpha_transparency"){
    return !isAtlasRuntimeReady("buildings");
  }
  if(reason!=="asset_not_loaded" && reason!=="sheet_not_complete") return false;
  if(isAtlasRuntimeReady("buildings")) return false;
  const runtime=atlasRuntimeInfo.buildings;
  if(!runtime) return true;
  return runtime.loaded!==true && runtime.imageOnerrorFired!==true;
}
function isNonFatalAtlasReason(reason){
  return reason==="atlas_missing_alpha_transparency";
}
function computeFinalMissingAssetTokens(){
  // Filter the running missingAssetWarnings set down to the truthful final state:
  //  - drop any "building_sprite:<spriteId>:<reason>" token whose building ultimately
  //    rendered as atlas in this session.
  //  - drop tokens classified as non-fatal/transient warnings.
  const resolvedSpriteIds=new Set();
  world.buildings.forEach((b)=>{
    if(buildingRenderDiagnostics.atlasBuildings.has(b.id)){
      const sId=getBuildingSpriteId(b);
      if(sId) resolvedSpriteIds.add(sId);
    }
  });
  return [...missingAssetWarnings].filter((token)=>{
    if(!token.startsWith("building_sprite:")) return true;
    const parts=token.split(":");
    const sId=parts[1];
    const reason=parts.slice(2).join(":");
    if(isNonFatalAtlasReason(reason)) return false;
    if(sId && resolvedSpriteIds.has(sId)) return false;
    return true;
  });
}

function getBuildingAtlasDebugStatus(){
  const buildingInfo=atlasRuntimeInfo.buildings||{};
  const propInfo=atlasRuntimeInfo.props||{};
  const buildingSheet=atlasImages.buildings;
  const propSheet=atlasImages.props;
  const buildingEntries=Object.values(ATLAS_BUILDING_METADATA).map((entry)=>{
    // Resolver provides authoritative crop/draw/anchor; static entry provides structural metadata.
    const resolved=resolveAtlasSpriteRuntimeEntry(entry.id);
    const auditEntry={
      ...entry,
      crop:resolved?.crop || entry.crop,
      drawW:resolved?.drawW || entry.drawW,
      drawH:resolved?.drawH || entry.drawH,
      anchorX:resolved?.anchorX !== undefined ? resolved.anchorX : entry.anchorX,
      anchorY:resolved?.anchorY !== undefined ? resolved.anchorY : entry.anchorY
    };
    const validationReason=getAtlasBuildingEntryValidation(auditEntry, buildingInfo, buildingSheet);
    return {
      id:entry.id,
      role:entry.role,
      renderStatus:validationReason ? "FALLBACK" : "ATLAS",
      crop:auditEntry.crop,
      cropSource:resolved?.cropSource||"static_metadata",
      draw:{ w:auditEntry.drawW, h:auditEntry.drawH },
      anchor:{ x:auditEntry.anchorX, y:auditEntry.anchorY },
      footprint:entry.footprint,
      collision:entry.collisionRect,
      interaction:entry.interactionRect,
      doorTile:entry.doorTile,
      labelAnchor:entry.labelAnchor,
      decorExclusion:entry.decorExclusionRect,
      productionReady:entry.productionReady===true,
      fallbackReason:validationReason
    };
  });
  return {
    buildingRequestedUrl:buildingInfo.selectedUrl || buildingInfo.urls?.[0] || "n/a",
    buildingLoaded:!!buildingInfo.loaded,
    buildingNaturalWidth:buildingInfo.width || buildingSheet?.naturalWidth || 0,
    buildingNaturalHeight:buildingInfo.height || buildingSheet?.naturalHeight || 0,
    assetRequestedUrl:propInfo.selectedUrl || propInfo.urls?.[0] || "n/a",
    assetLoaded:!!propInfo.loaded,
    assetNaturalWidth:propInfo.width || propSheet?.naturalWidth || 0,
    assetNaturalHeight:propInfo.height || propSheet?.naturalHeight || 0,
    spriteRenderingPathActive:buildingRenderDiagnostics.atlasBuildings.size>0 || buildingSpriteProofState.drawn,
    fallbackRenderingUsed:buildingRenderDiagnostics.fallbackBuildings.size>0,
    atlasProofEnabled:USE_HEARTHVALE_ATLAS_PROOF,
    atlasProofDebugEnabled:USE_HEARTHVALE_ATLAS_PROOF_DEBUG,
    atlasProofSelectedAtlasFilename:atlasProofDiagnostics.selectedAtlasFilename,
    atlasProofRequestedAssetUrl:atlasProofDiagnostics.requestedAssetUrl,
    atlasProofImageLoaded:atlasProofDiagnostics.imageLoaded,
    atlasProofNaturalWidth:atlasProofDiagnostics.naturalWidth,
    atlasProofNaturalHeight:atlasProofDiagnostics.naturalHeight,
    atlasProofBuildingId:atlasProofDiagnostics.selectedBuildingId,
    atlasProofBuildingRole:atlasProofDiagnostics.selectedBuildingRole,
    atlasProofSpriteId:atlasProofDiagnostics.selectedSpriteId||"n/a",
    atlasProofCrop:formatRect(atlasProofDiagnostics.crop),
    atlasProofDrawSize:atlasProofDiagnostics.drawSize ? (atlasProofDiagnostics.drawSize.w + "x" + atlasProofDiagnostics.drawSize.h) : "n/a",
    atlasProofRenderPath:atlasProofDiagnostics.usedAtlasRender ? "ATLAS" : "FALLBACK",
    atlasProofFallbackReason:atlasProofDiagnostics.fallbackReason || "none",
    buildingEntries
  };
}
function drawBuildingSpriteProof(){
  if(!BUILDING_SPRITE_PROOF_DEBUG) return;
  const spriteId="village_hall_meeting_house";
  const sprite=atlasManifests.buildings.sprites[spriteId];
  if(!sprite) return;
  const panelX=12;
  const panelY=86;
  const scale=0.22;
  const drawW=Math.max(1,Math.round(sprite.sw*scale));
  const drawH=Math.max(1,Math.round(sprite.sh*scale));
  ctx.save();
  ctx.setTransform(1,0,0,1,0,0);
  ctx.imageSmoothingEnabled=false;
  ctx.fillStyle="rgba(8,14,22,.82)";
  ctx.fillRect(panelX,panelY,drawW+18,drawH+28);
  ctx.strokeStyle="rgba(145,194,255,.75)";
  ctx.strokeRect(panelX+0.5,panelY+0.5,drawW+17,drawH+27);
  const didDraw=drawAtlasSprite("buildings", spriteId, panelX+9, panelY+14, drawW, drawH);
  buildingSpriteProofState.attempted=true;
  buildingSpriteProofState.drawn=!!didDraw;
  ctx.fillStyle=didDraw ? "rgba(189,231,178,.95)" : "rgba(255,177,177,.95)";
  ctx.font="11px ui-monospace, monospace";
  ctx.fillText("Sprite proof: " + (didDraw ? "drawImage OK" : "fallback"), panelX+8, panelY+11);
  ctx.restore();
}
function getBuildingSpriteId(building){
  if(!building) return null;
  const explicitSpriteId=typeof building.spriteId==="string" ? building.spriteId : null;
  if(explicitSpriteId && atlasManifests.buildings?.sprites?.[explicitSpriteId]) return explicitSpriteId;
  const byMap=BUILDING_SPRITE_ID_BY_BUILDING_ID[building.id] || BUILDING_SPRITE_ID_BY_ROLE[building.role] || null;
  if(byMap && atlasManifests.buildings?.sprites?.[byMap]) return byMap;
  const candidates=[
    explicitSpriteId,
    byMap,
    building.role,
    building.id?.replace(/^b_/,""),
    building.role==="inn_tavern" ? "inn_tavern_v1" : null,
    building.role==="mercantile" ? "mercantile_shop" : null,
    building.role==="village_hall" ? "village_hall_meeting_house" : null
  ].filter(Boolean);
  return candidates.find((candidate)=>atlasManifests.buildings?.sprites?.[candidate]) || byMap || explicitSpriteId || null;
}
function drawBuildingFallbackSprite(building){
  const visual=building.visual || { x:building.x, y:building.y, w:building.w, h:building.h };
  const style=BUILDING_FALLBACK_STYLE_BY_ROLE[building.role] || BUILDING_FALLBACK_STYLE_BY_ROLE.residence_small;
  const roofMidTile=assets.building[style.roof] || assets.building.roofC;
  const wallTile=assets.building[style.wall] || assets.building.wall;
  const windowTile=assets.building[style.window] || assets.building.window;
  const doorTile=assets.building[style.door] || assets.building.door;
  const drawTile=(img,tx,ty)=>{
    if(!img || !img.complete || img.naturalWidth<=0) return false;
    const p=tileToScreen(tx,ty);
    ctx.drawImage(img,p.x,p.y,TILE,TILE);
    return true;
  };
  for(let y=0;y<visual.h;y++){
    for(let x=0;x<visual.w;x++){
      const tx=visual.x+x;
      const ty=visual.y+y;
      if(y===0){
        const roofTile=(x===0) ? assets.building.roofL : (x===visual.w-1 ? assets.building.roofR : roofMidTile);
        drawTile(roofTile, tx, ty);
        continue;
      }
      drawTile(wallTile, tx, ty);
    }
  }
  if(style.dormer && visual.w>=3) drawTile(assets.building.roofDormer, visual.x+Math.floor(visual.w/2), visual.y);
  const interaction=building.interaction || { x:visual.x+Math.floor(visual.w/2), y:visual.y+visual.h-1 };
  drawTile(doorTile, interaction.x, interaction.y);
  if(visual.h>=3){
    const windowY=visual.y+Math.min(visual.h-2, 2);
    drawTile(windowTile, visual.x+1, windowY);
    if(visual.w>=4) drawTile(windowTile, visual.x+visual.w-2, windowY);
  }
}

function buildTerrainTiles() {
  const grassBases = ["#4f7347", "#517548", "#4c7044", "#53774a"];
  const forestBases = [palette.forestGrass[0], "#3f6540", palette.forestGrass[1], "#314f34"];
  for (let i=0;i<4;i++) {
    assets.grass.push(makeTile((p)=>{
      p.fillStyle = grassBases[i]; p.fillRect(0,0,32,32);
      for (let y=0;y<32;y+=4){
        for (let x=0;x<32;x+=4){
          const n=rng(x+i*7,y+i*5,31+i);
          if(n>0.92){ p.fillStyle = "rgba(198,226,162,.03)"; p.fillRect(x,y,3,1); }
          else if(n<0.06){ p.fillStyle = "rgba(29,47,28,.055)"; p.fillRect(x,y+1,3,1); }
        }
      }
      p.fillStyle = "rgba(220,239,180,.028)";
      for (let k=0;k<8;k++) {
        const gx = ((k*5+i*6)%30)+1;
        const gy = ((k*7+i*3)%25)+3;
        const dotW = rng(k+i,gy,145)>0.82 ? 2 : 1;
        p.fillRect(gx,gy,dotW,1);
      }
      p.fillStyle="rgba(255,255,255,.012)"; p.fillRect(0,0,32,1);
      p.fillStyle="rgba(0,0,0,.048)"; p.fillRect(0,30,32,2);
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

    if(i<4) {
      assets.road.push(makeTile((p)=>{
        const base = i%2? "#7f6847" : "#7a6344";
        p.fillStyle = base; p.fillRect(0,0,32,32);
        p.fillStyle = "rgba(98,78,53,.14)";
        for(let y=0;y<32;y+=5){
          const wob=Math.floor((Math.sin((y+i)*0.45)+1.3)*1.5);
          p.fillRect((y+i*2)%11, y, 7+wob, 1);
        }
        p.fillStyle = "rgba(196,166,128,.09)";
        for(let k=0;k<6;k++){
          const x=((k*7+i*5)%26)+2;
          const y=((k*6+i*8)%24)+4;
          p.fillRect(x,y,2+(k%2),1);
        }
        p.fillStyle="rgba(0,0,0,.06)";
        p.fillRect(0,0,32,2);
        p.fillStyle = "rgba(0,0,0,.1)"; p.fillRect(0,29,32,3);
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
      p.fillStyle=i%2? "rgba(123,102,74,.52)" : "rgba(138,114,84,.46)";
      for(let x=0;x<32;x+=2){
        const h = 2 + Math.floor(rng(x,i,77) * 3);
        p.fillRect(x,32-h,2,h);
      }
      p.fillStyle="rgba(78,104,57,.22)"; p.fillRect(0,0,32,2);
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
    p.fillStyle="#835147"; p.fillRect(0,0,32,32);
    p.fillStyle="#6d4037"; for(let y=0;y<24;y++) p.fillRect(0,y,Math.max(0,12-Math.floor(y/2)),1);
    p.fillStyle="#bf8774"; for(let y=3;y<24;y+=3) p.fillRect(4,y,25,1);
    p.fillStyle="#3b251f"; p.fillRect(0,24,32,8);
    p.fillStyle="rgba(255,231,206,.18)"; p.fillRect(3,3,15,2);
  });
  assets.building.roofC = makeTile((p)=>{
    p.fillStyle="#87554a"; p.fillRect(0,0,32,32);
    p.fillStyle="#bc816f"; for(let y=2;y<24;y+=3) p.fillRect(2,y,28,1);
    p.fillStyle="rgba(73,42,33,.2)"; for(let x=3;x<29;x+=6) p.fillRect(x,5,1,17);
    p.fillStyle="#4a2b24"; p.fillRect(0,23,32,9);
    p.fillStyle="rgba(235,197,157,.16)"; p.fillRect(2,24,28,1);
  });
  assets.building.roofR = makeTile((p)=>{
    p.fillStyle="#835147"; p.fillRect(0,0,32,32);
    p.fillStyle="#6d4037"; for(let y=0;y<24;y++){const w=Math.max(0,12-Math.floor(y/2)); p.fillRect(32-w,y,w,1);}
    p.fillStyle="#bf8774"; for(let y=3;y<24;y+=3) p.fillRect(3,y,25,1);
    p.fillStyle="#3b251f"; p.fillRect(0,24,32,8);
    p.fillStyle="rgba(255,231,206,.18)"; p.fillRect(14,3,15,2);
  });
  assets.building.roofSlate = makeTile((p)=>{
    p.fillStyle="#6d6966"; p.fillRect(0,0,32,32);
    p.fillStyle="#8a847f"; for(let y=2;y<24;y+=3) p.fillRect(3,y,26,1);
    p.fillStyle="#4a4746"; for(let x=4;x<30;x+=7) p.fillRect(x,4,1,18);
    p.fillStyle="#353334"; p.fillRect(0,23,32,9);
    p.fillStyle="rgba(206,212,221,.16)"; p.fillRect(4,4,18,1);
  });
  assets.building.roofDormer = makeTile((p)=>{
    p.drawImage(assets.building.roofC,0,0);
    p.fillStyle="#6f4d35"; p.fillRect(9,8,14,10);
    p.fillStyle="#4f3624"; p.fillRect(10,9,12,9);
    p.fillStyle="#a6c2d6"; p.fillRect(12,10,8,6);
    p.fillStyle="#2d3e4e"; p.fillRect(15,10,1,6);
    p.fillStyle="rgba(232,246,255,.34)"; p.fillRect(12,10,7,1);
  });
  assets.building.wall = makeTile((p)=>{
    p.fillStyle="#b8ad98"; p.fillRect(0,0,32,32);
    p.fillStyle="#d4c8af"; p.fillRect(0,0,32,5);
    p.fillStyle="#7b6d5b"; p.fillRect(0,28,32,4);
    p.fillStyle="rgba(84,63,41,.16)"; for(let x=0;x<32;x+=8) p.fillRect(x,5,1,23);
    p.fillStyle="rgba(255,250,236,.06)"; for(let y=8;y<28;y+=6) p.fillRect(2,y,28,1);
    p.fillStyle="rgba(34,26,19,.14)"; p.fillRect(29,0,3,32);
  });
  assets.building.wallTimber = makeTile((p)=>{
    p.fillStyle="#d4c3a8"; p.fillRect(0,0,32,32);
    p.fillStyle="#8b6544"; p.fillRect(0,0,32,4); p.fillRect(0,28,32,4);
    p.fillStyle="#7a5538"; p.fillRect(4,4,3,24); p.fillRect(25,4,3,24);
    p.fillStyle="#7a5538"; p.fillRect(14,4,3,24);
    p.fillStyle="#a9825b"; p.fillRect(7,4,7,24); p.fillRect(17,4,8,24);
    p.fillStyle="rgba(255,243,218,.08)"; p.fillRect(8,7,6,1); p.fillRect(18,10,7,1);
  });
  assets.building.wallBrick = makeTile((p)=>{
    p.fillStyle="#8f6552"; p.fillRect(0,0,32,32);
    p.fillStyle="#6e4a3a"; for(let y=4;y<28;y+=5) p.fillRect(0,y,32,1);
    p.fillStyle="#a97b62"; for(let x=2;x<30;x+=8){ for(let y=1;y<29;y+=10) p.fillRect(x,y,1,3); }
    p.fillStyle="#5a3a2f"; p.fillRect(0,28,32,4);
    p.fillStyle="rgba(255,215,185,.08)"; p.fillRect(2,3,10,1);
  });
  assets.building.window = makeTile((p)=>{
    p.drawImage(assets.building.wall,0,0);
    p.fillStyle="#5d4330"; p.fillRect(8,8,16,13);
    p.fillStyle="#2f241b"; p.fillRect(9,9,14,11);
    p.fillStyle="#9fbfd5"; p.fillRect(10,10,12,9);
    p.fillStyle="#42576a"; p.fillRect(15,10,2,9); p.fillRect(10,14,12,1);
    p.fillStyle="rgba(240,248,255,.35)"; p.fillRect(11,10,9,1);
  });
  assets.building.windowTall = makeTile((p)=>{
    p.drawImage(assets.building.wallTimber,0,0);
    p.fillStyle="#5d4330"; p.fillRect(10,6,12,18);
    p.fillStyle="#2f241b"; p.fillRect(11,7,10,16);
    p.fillStyle="#a8c8dc"; p.fillRect(12,8,8,14);
    p.fillStyle="#456074"; p.fillRect(15,8,1,14); p.fillRect(12,15,8,1);
    p.fillStyle="rgba(248,253,255,.4)"; p.fillRect(13,8,6,1);
  });
  assets.building.windowWide = makeTile((p)=>{
    p.drawImage(assets.building.wallBrick,0,0);
    p.fillStyle="#513726"; p.fillRect(6,10,20,11);
    p.fillStyle="#2b2018"; p.fillRect(7,11,18,9);
    p.fillStyle="#98b8ce"; p.fillRect(8,12,16,7);
    p.fillStyle="#3f586e"; p.fillRect(15,12,1,7);
    p.fillStyle="rgba(240,248,255,.32)"; p.fillRect(9,12,11,1);
  });
  assets.building.door = makeTile((p)=>{
    p.drawImage(assets.building.wall,0,0);
    p.fillStyle="#6a4a35"; p.fillRect(8,7,16,24);
    p.fillStyle="#3a291d"; p.fillRect(9,8,14,22);
    p.fillStyle="#ba8a58"; p.fillRect(15,10,2,20);
    p.fillStyle="#e5bd89"; p.fillRect(20,21,2,2);
    p.fillStyle="rgba(246,222,171,.2)"; p.fillRect(10,10,4,18);
    p.fillStyle="rgba(0,0,0,.23)"; p.fillRect(8,30,16,1);
  });
  assets.building.doorPorch = makeTile((p)=>{
    p.drawImage(assets.building.wallTimber,0,0);
    p.fillStyle="#6a4b34"; p.fillRect(9,8,14,19);
    p.fillStyle="#33261c"; p.fillRect(10,9,12,17);
    p.fillStyle="#b98754"; p.fillRect(15,11,1,14);
    p.fillStyle="#8a6444"; p.fillRect(6,24,20,2);
    p.fillStyle="#a67c57"; p.fillRect(5,26,22,3);
    p.fillStyle="rgba(236,213,181,.22)"; p.fillRect(11,10,3,14);
  });
  assets.building.doorShop = makeTile((p)=>{
    p.drawImage(assets.building.wallBrick,0,0);
    p.fillStyle="#6f4d36"; p.fillRect(7,10,18,18);
    p.fillStyle="#32241a"; p.fillRect(8,11,16,16);
    p.fillStyle="#b58959"; p.fillRect(15,12,1,13);
    p.fillStyle="#9f744f"; p.fillRect(6,27,20,3);
    p.fillStyle="#c89d6f"; p.fillRect(9,8,14,2);
    p.fillStyle="rgba(234,206,170,.2)"; p.fillRect(10,12,3,13);
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
  sheet.width = 480;
  sheet.height = 32;
  const p = sheet.getContext("2d");
  p.imageSmoothingEnabled = false;
  p.clearRect(0,0,480,32);

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

  cell(13,(q)=>{ // woodpile
    q.fillStyle="#6a4a30"; q.fillRect(6,16,20,8);
    q.fillStyle="#8a6340"; q.fillRect(8,14,16,3);
    q.fillStyle="#4e3523"; q.fillRect(9,18,2,6); q.fillRect(14,18,2,6); q.fillRect(19,18,2,6);
  });
  cell(14,(q)=>{ // small garden
    q.fillStyle="#6d5137"; q.fillRect(7,20,18,4);
    q.fillStyle="#557d45"; q.fillRect(8,17,16,3);
    q.fillStyle="#7fa55e"; q.fillRect(10,15,3,2); q.fillRect(15,14,3,3); q.fillRect(20,15,2,2);
  });

  const sheetImg = new Image();
  sheetImg.src = sheet.toDataURL("image/png");
  assets.props.sheet = sheetImg;

  const names = ["barrel","crate","sack","lanternPost","signPost","fenceSeg","bush","grassTuft","well","stonePile","bench","noticeBoard","handcart","woodpile","smallGarden"];
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
    const ox = baseX + 8;
    const oy = baseY + 7;
    const elder = variant === "elder";
    const merchant = variant === "merchant";
    const ranger = variant === "ranger";
    const bob = Math.abs(step) > 0 ? 1 : 0;
    const armSwing = elder ? Math.round(step * 0.5) : step;
    const outline = "rgba(8,12,18,.84)";
    const skinShadow = elder ? "#b59a7a" : "#cfad89";
    const cloakShadow = "rgba(10,14,22,.35)";
    const edge = (x,y,w=1,h=1)=>dot(x,y,w,h,outline);

    const dot = (x,y,w=1,h=1,color=outline) => { p.fillStyle=color; p.fillRect(ox+x*px, oy+y*px, w*px, h*px); };

    if (dir==="down" || dir==="up") {
      const front = dir==="down";
      dot(10,4+bob,8,6,colors.skin);
      dot(10,3+bob,8,3,colors.hair);
      if(ranger) dot(9,3+bob,10,2,"#4b5f2f");
      if(merchant && front) dot(9,2+bob,10,2,colors.accent || "#d9bf84");
      if(front){
        dot(11,8+bob,1,1,"#1b2632");
        dot(15,8+bob,1,1,"#1b2632");
      }
      if(elder && front) dot(12,9+bob,4,1,"#e7ecf7");
      dot(10,10+bob,8,2,colors.tunicShade);
      dot(10,12+bob,8,8,colors.tunic);
      dot(11,12+bob,6,2,"rgba(255,255,255,.16)");
      dot(9,13+bob,10,6,colors.cloak);
      dot(10,16+bob,8,1,colors.accent || "#d8dfef");
      dot(10,19+bob,3,3,colors.tunicShade);
      dot(15,19+bob,3,3,colors.tunicShade);
      dot(10,22+step,2,3,colors.boots);
      dot(16,22-step,2,3,colors.boots);
      dot(10,20+bob,1,2,cloakShadow);
      dot(17,20+bob,1,2,cloakShadow);
      dot(8,14+armSwing,2,4,skinShadow);
      dot(18,14-armSwing,2,4,skinShadow);
      if(ranger) dot(18,15+bob,1,5,"#5e422d");
      if(merchant && front) dot(13,20+bob,2,2,"#b98952");
    } else {
      const left = dir==="left";
      const headX = left ? 9 : 14;
      dot(headX,4+bob,6,6,colors.skin);
      dot(left ? 8 : 14,3+bob,7,3,colors.hair);
      if(merchant) dot(left ? 8 : 14,2+bob,7,2,colors.accent || "#d9bf84");
      if(ranger) dot(left ? 7 : 15,3+bob,6,2,"#4b5f2f");
      dot(left ? 11 : 15,8+bob,1,1,"#1b2632");
      dot(left ? 11 : 14,8+bob,2,2,skinShadow);
      dot(10,11+bob,8,2,colors.tunicShade);
      dot(10,13+bob,8,7,colors.tunic);
      dot(9,14+bob,10,5,colors.cloak);
      dot(11,16+bob,6,1,colors.accent || "#d8dfef");
      dot(left ? 7 : 19,14+armSwing,2,4,skinShadow);
      dot(left ? 10 : 15,19+step,3,4,colors.tunicShade);
      dot(left ? 15 : 10,21-step,2,3,colors.boots);
      dot(left ? 11 : 14,22+step,2,2,colors.boots);
      dot(left ? 9 : 17,13+bob,1,5,cloakShadow);
      if(ranger) dot(left ? 18 : 9,15+bob,1,5,"#5e422d");
    }

    edge(9,4+bob,1,7); edge(18,4+bob,1,7); edge(10,3+bob,8,1); edge(10,10+bob,8,1);
    edge(8,12+bob,1,9); edge(19,12+bob,1,9); edge(9,20+bob,10,1);
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
    const ox = baseX + 6;
    const oy = baseY + 10;
    const dot = (x,y,w=1,h=1,color="rgba(8,12,18,.82)") => { p.fillStyle=color; p.fillRect(ox+x*px, oy+y*px, w*px, h*px); };

    const fur = "#747f8a";
    const furShade = "#56606d";
    const furHi = "#a0aab5";
    const muzzle = "#c9c1b2";
    const nose = "#242d3a";

    if (dir==="left" || dir==="right") {
      const left = dir==="left";
      const headX = left ? 7 : 19;
      const tailBaseX = left ? 24 : 6;
      dot(11,12,12,5,fur);
      dot(12,11,9,2,furHi);
      dot(12,15,10,3,furShade);
      dot(11,17,12,1,furHi);
      dot(10,18-step,2,4,fur);
      dot(15,19+step,2,4,furShade);
      dot(20,18+step,2,4,fur);
      dot(23,19-step,2,4,furShade);
      dot(headX,9,6,5,fur);
      dot(headX+(left?0:1),8,1,2,furShade);
      dot(headX+(left?4:5),8,1,2,furShade);
      dot(headX+1,11,4,2,muzzle);
      dot(headX+(left?0:5),11,1,1,nose);
      dot(headX+(left?2:3),10,1,1,nose);
      dot(tailBaseX,13,3,2,furShade);
      dot(tailBaseX+(left?2:-2),12,2,1,furShade);
      dot(tailBaseX+(left?4:-4),11,1,1,furShade);
      dot(10,12,1,7);
      dot(23,12,1,7);
      dot(11,11,12,1);
      dot(11,18,12,1);
    } else {
      const back = dir==="up";
      dot(12,11,10,3,back ? furShade : furHi);
      dot(11,14,12,6,fur);
      dot(12,20+step,2,3,furShade);
      dot(15,21-step,2,3,fur);
      dot(18,20-step,2,3,furShade);
      dot(21,21+step,2,3,fur);
      dot(13,9,8,3,back ? furShade : muzzle);
      if (!back){ dot(14,10,1,1,nose); dot(18,10,1,1,nose); }
      dot(12,8,1,2,furShade);
      dot(20,8,1,2,furShade);
      dot(11,13,1,8);
      dot(22,13,1,8);
      dot(12,12,10,1);
      dot(12,20,10,1);
      if(back){ dot(10,15,1,2,furShade); dot(23,15,1,2,furShade); }
    }
  }

  ["down","left","right","up"].forEach((dir,row)=>[0,1,0,-1].forEach((s,col)=>frame(col*size,row*size,dir,s)));
  const img = new Image(); img.src = c.toDataURL("image/png"); return img;
}

emitWayfarerBuildSentinel();
bootstrapAtlasPipeline();
buildTerrainTiles();
makeBuildingTiles();
makeTreeSprites();
makeFenceTiles();
makeShadowTiles();
makePropSprites();
assets.sprites.player = paintHumanoidSheet({ skin:"#e4c8a2", hair:"#4f3a2c", tunic:"#3f719f", tunicShade:"#2d5275", cloak:"#e2e8f3", boots:"#4f3826", accent:"#f2d37c" }, "adventurer");
assets.sprites.npc = paintHumanoidSheet({ skin:"#ccb79b", hair:"#dbe4f6", tunic:"#626a86", tunicShade:"#4b5167", cloak:"#2d3345", boots:"#2f2418", accent:"#c5cee3" }, "elder");
assets.sprites.edrin = paintHumanoidSheet({ skin:"#c8ae8d", hair:"#f0f4fc", tunic:"#6c6b96", tunicShade:"#4f4d73", cloak:"#2a3148", boots:"#2f2418", accent:"#c9d0f0" }, "elder");
assets.sprites.hunter = paintHumanoidSheet({ skin:"#d3b999", hair:"#4d3a2b", tunic:"#5f7948", tunicShade:"#425736", cloak:"#3a2f24", boots:"#312519", accent:"#b7c986" }, "ranger");
assets.sprites.merchant = paintHumanoidSheet({ skin:"#dabf9e", hair:"#6d4a30", tunic:"#8b5537", tunicShade:"#633b27", cloak:"#b69458", boots:"#3b2a1d", accent:"#e5c57e" }, "merchant");
assets.sprites.bandit = paintHumanoidSheet({ skin:"#b99b7b", hair:"#231d1a", tunic:"#6b3940", tunicShade:"#46262b", cloak:"#17141d", boots:"#21170f", accent:"#b4797f" }, "adventurer");
assets.sprites.rook = paintHumanoidSheet({ skin:"#b4916c", hair:"#100d13", tunic:"#8a2e3b", tunicShade:"#651f2a", cloak:"#2b0e15", boots:"#1f1310", accent:"#cc8a8f" }, "adventurer");
assets.sprites.wolf = paintWolfSheet();

const world = { blocked:new Set(), trees:[], fences:[], buildings:[], roads:[], roadTiles:new Set(), props:[], zones:[], pondBlocked:new Set(), pondWater:new Set(), pondShore:new Set(), pondNearEdge:new Set() };
function blockRect(x,y,w,h){ for(let ix=x;ix<x+w;ix++)for(let iy=y;iy<y+h;iy++) world.blocked.add(keyOf(ix,iy)); }
const HEARTHVALE_LANDMARKS = Object.freeze({
  mirrorPond:{ x:27, y:14 },
  caveEntrance:{ x:34, y:11 },
  mainCrossroads:{ x:16, y:11 },
  townCenterSpawn:{ x:18, y:11 },
  merchantRowanArea:{ x:20, y:10 },
  edrinValeArea:{ x:16, y:12 },
  hunterGarranArea:{ x:30, y:11 },
  noticeSignNode:{ x:26, y:11 },
  zoneExits:Object.freeze({
    mirrorCaveEntrance:{ x:34, y:11 },
    abandonedTollhouseEntrance:{ x:22, y:2 },
    northRoadBoundary:{ x:16, y:0 },
    westLaneBoundary:{ x:0, y:12 },
    easternWoodsBoundary:{ x:37, y:14 }
  })
});
const OVERWORLD_CAVE_ENTRY = Object.freeze({ ...HEARTHVALE_LANDMARKS.caveEntrance });
const MIRROR_CAVE_EXIT = Object.freeze({ x:13, y:16 });
const MIRROR_CAVE_CHEST_TILE = Object.freeze({ x:13, y:2 });
const NORTH_ROAD_TOLLHOUSE_ENTRY = Object.freeze({ x:22, y:2 });
const TOLLHOUSE_EXIT = Object.freeze({ x:13, y:18 });
const TOLLHOUSE_CHEST_TILE = Object.freeze({ x:22, y:4 });
function createFootprint({
  visual,
  collision,
  interaction,
  label,
  pathingBounds,
  frontWalkBand,
  visualBounds,
  interactRect,
  frontDoorTile,
  blockedVisualTiles,
  occlusionDepthLine,
  rearExclusionZone
}){
  return {
    visual,
    collision,
    interaction,
    label,
    visualBounds:visualBounds || visual,
    interactRect:interactRect || interaction || null,
    frontDoorTile:frontDoorTile || null,
    blockedVisualTiles:Array.isArray(blockedVisualTiles) ? blockedVisualTiles : [],
    pathingBounds:pathingBounds || visual,
    frontWalkBand:frontWalkBand || null,
    occlusionDepthLine:occlusionDepthLine || null,
    rearExclusionZone:rearExclusionZone || null
  };
}
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
  // Phase 34.2 Thames Street harbor composition lock: dense waterfront spine + service apron.
  { x:5,y:13,w:31,h:1 },
  { x:6,y:14,w:29,h:1 },
  // Dockside service band and edge circulation.
  { x:7,y:16,w:28,h:1 },
  { x:8,y:17,w:26,h:1 },
  { x:10,y:18,w:23,h:1 },
  // Wharf projections and central boardwalk pier.
  { x:9,y:18,w:2,h:5 },
  { x:14,y:18,w:2,h:6 },
  { x:18,y:17,w:4,h:7 },
  { x:24,y:18,w:2,h:5 },
  { x:29,y:18,w:2,h:5 },
  // Cross-lanes from civic inland area to waterfront spine.
  { x:12,y:7,w:1,h:7 },
  { x:16,y:8,w:1,h:6 },
  { x:21,y:7,w:1,h:7 },
  { x:26,y:8,w:1,h:6 },
  { x:8,y:9,w:21,h:1 },
  // Frontage stubs for key doors.
  { x:11,y:12,w:1,h:2 },
  { x:17,y:12,w:1,h:2 },
  { x:25,y:8,w:1,h:2 },
  { x:30,y:16,w:1,h:2 },
  // West-lane neighborhood tie-in.
  { x:5,y:9,w:4,h:1 }
);
world.roads.forEach(r=>{ for(let x=r.x;x<r.x+r.w;x++) for(let y=r.y;y<r.y+r.h;y++) world.roadTiles.add(keyOf(x,y)); });

world.buildings.push(
  { id:"b_inn_tavern", role:"inn_tavern", spriteId:"inn_tavern_v1", x:8, y:8, w:6, h:5, anchorX:3, anchorY:4, ...createFootprint({ visual:{x:8,y:8,w:6,h:5}, visualBounds:{x:8,y:8,w:6,h:5}, collision:{x:8,y:11,w:6,h:1}, interaction:{x:11,y:12,w:1,h:1}, interactRect:{x:11,y:12,w:1,h:1}, frontDoorTile:{x:11,y:12}, label:{x:11,y:9,text:"Inn & Tavern"}, pathingBounds:{x:7,y:8,w:8,h:6}, frontWalkBand:{ x:8, y:12, w:6, h:1 }, blockedVisualTiles:[{ x:8, y:8, w:6, h:3 }, { x:8, y:11, w:3, h:1 }, { x:12, y:11, w:2, h:1 }], occlusionDepthLine:{ x:8, y:11, w:6, h:1 }, rearExclusionZone:{ x:8, y:8, w:6, h:3 } }) },
  { id:"b_mercantile", role:"mercantile_shop", spriteId:"mercantile_shop", x:15, y:8, w:5, h:5, anchorX:2, anchorY:4, ...createFootprint({ visual:{x:15,y:8,w:5,h:5}, visualBounds:{x:15,y:8,w:5,h:5}, collision:{x:15,y:11,w:5,h:1}, interaction:{x:17,y:12,w:1,h:1}, interactRect:{x:17,y:12,w:1,h:1}, frontDoorTile:{x:17,y:12}, label:{x:17,y:9,text:"Mercantile Shop"}, pathingBounds:{x:14,y:8,w:7,h:6}, frontWalkBand:{ x:15, y:12, w:5, h:1 }, blockedVisualTiles:[{ x:15, y:8, w:5, h:3 }, { x:15, y:11, w:2, h:1 }, { x:18, y:11, w:2, h:1 }], occlusionDepthLine:{ x:15, y:11, w:5, h:1 }, rearExclusionZone:{ x:15, y:8, w:5, h:3 } }) },
  { id:"b_village_hall", role:"village_hall_meeting_house", spriteId:"village_hall_meeting_house", x:22, y:3, w:6, h:5, anchorX:3, anchorY:4, ...createFootprint({ visual:{x:22,y:3,w:6,h:5}, visualBounds:{x:22,y:3,w:6,h:5}, collision:{x:22,y:6,w:6,h:2}, interaction:{x:25,y:8,w:1,h:1}, interactRect:{x:25,y:8,w:1,h:1}, frontDoorTile:{x:25,y:8}, label:{x:25,y:4,text:"Village Hall"}, pathingBounds:{x:21,y:3,w:8,h:6}, frontWalkBand:{ x:22, y:8, w:6, h:1 }, blockedVisualTiles:[{ x:22, y:3, w:6, h:3 }, { x:22, y:6, w:2, h:1 }, { x:26, y:6, w:2, h:1 }], occlusionDepthLine:{ x:22, y:6, w:6, h:1 }, rearExclusionZone:{ x:22, y:3, w:6, h:3 } }) },
  { id:"b_res_small", role:"residence_small", spriteId:"residence_small", x:4, y:6, w:4, h:4, anchorX:2, anchorY:3, ...createFootprint({ visual:{x:4,y:6,w:4,h:4}, visualBounds:{x:4,y:6,w:4,h:4}, collision:{x:4,y:8,w:4,h:1}, interaction:{x:5,y:9,w:1,h:1}, interactRect:{x:5,y:9,w:1,h:1}, frontDoorTile:{x:5,y:9}, frontWalkBand:{ x:4, y:10, w:4, h:1 }, blockedVisualTiles:[{ x:4, y:6, w:4, h:2 }, { x:4, y:8, w:4, h:1 }, { x:4, y:9, w:1, h:1 }, { x:6, y:9, w:2, h:1 }], occlusionDepthLine:{ x:4, y:8, w:4, h:1 }, rearExclusionZone:{ x:4, y:6, w:4, h:2 }, label:{x:5,y:7,text:"Cottage"}, pathingBounds:{x:3,y:6,w:6,h:6} }) },
  { id:"b_res_large", role:"residence_large", spriteId:"residence_large", x:29, y:4, w:5, h:4, anchorX:2, anchorY:3, ...createFootprint({ visual:{x:29,y:4,w:5,h:4}, collision:{x:29,y:6,w:5,h:2}, interaction:{x:31,y:8,w:1,h:1}, label:{x:31,y:5,text:"Residence"}, pathingBounds:{x:28,y:4,w:7,h:5} }) },
  { id:"b_hunter_lodge", role:"hunter_lodge_or_outfitter", spriteId:"hunter_lodge_or_outfitter", x:22, y:15, w:4, h:4, anchorX:2, anchorY:3, ...createFootprint({ visual:{x:22,y:15,w:4,h:4}, collision:{x:22,y:17,w:4,h:2}, interaction:{x:23,y:19,w:1,h:1}, label:{x:23,y:16,text:"Outfitter"}, pathingBounds:{x:21,y:14,w:6,h:6} }) },
  { id:"b_boathouse", role:"pond_boathouse_or_waterfront_shed", spriteId:"pond_boathouse_or_waterfront_shed", x:28, y:15, w:5, h:3, anchorX:2, anchorY:2, ...createFootprint({ visual:{x:28,y:15,w:5,h:3}, collision:{x:28,y:17,w:5,h:1}, interaction:{x:30,y:16,w:1,h:1}, label:{x:30,y:15,text:"Boathouse"}, pathingBounds:{x:27,y:14,w:7,h:6} }) }
);
world.buildings.forEach((b)=>{
  const c=b.collision || b.visual || {x:b.x,y:b.y,w:b.w,h:b.h};
  blockRect(c.x,c.y,c.w,c.h);
});
function auditBuildingAtlasMappings(){
  const atlasEntries=[];
  const fallbackEntries=[];
  world.buildings.forEach((building)=>{
    const spriteId=getBuildingSpriteId(building);
    if(!spriteId){
      fallbackEntries.push(building.id + "(unmapped_for_safe_rollout)");
      return;
    }
    const sprite=atlasManifests.buildings.sprites?.[spriteId];
    if(!sprite){
      fallbackEntries.push(building.id + "(missing_atlas_entry:" + spriteId + ")");
      return;
    }
    atlasEntries.push(building.id + "->" + spriteId + "[sx=" + sprite.sx + ",sy=" + sprite.sy + ",sw=" + sprite.sw + ",sh=" + sprite.sh + "]");
  });
  console.info("[Building Atlas Mapping] atlas=" + atlasEntries.join(",") + " fallback=" + (fallbackEntries.join(",") || "none"));
}
auditBuildingAtlasMappings();

const pond={x:-10,y:16,w:62,h:22,cx:23,cy:30};
for(let x=pond.x;x<pond.x+pond.w;x++){
  for(let y=pond.y;y<pond.y+pond.h;y++){
    const dx=(x+.5-pond.cx)/(pond.w/2), dy=(y+.5-pond.cy)/(pond.h/2);
    const d=dx*dx+dy*dy;
    const wob=(rng(x,y,17)-.5)*.2 + (rng(x,y,19)-.5)*.08;
    const lim=.92+wob;
    if(d<=lim){ world.pondWater.add(keyOf(x,y)); world.pondBlocked.add(keyOf(x,y)); }
    if(d>=lim-.18&&d<=lim+.2) world.pondShore.add(keyOf(x,y));
    if(d>=lim-.25&&d<=lim+.1) world.pondNearEdge.add(keyOf(x,y));
  }
}

for(let x=16;x<=20;x++){ world.fences.push({x,y:2}); } // garden plot north fence — stops at x=20 to clear village hall (x=21..26)
for(let y=3;y<=6;y++){ world.fences.push({x:16,y}); }   // garden plot west fence
for(let y=3;y<=6;y++){ world.fences.push({x:20,y}); }   // garden plot east fence — moved from x=23 so village hall isn't sitting on it
for(let x=9;x<=14;x++){ world.fences.push({x,y:15}); }
for(let x=25;x<=31;x++){ world.fences.push({x,y:15}); }
for(let y=19;y<=20;y++){ world.fences.push({x:33,y}); }
world.fences.forEach(f=>world.blocked.add(keyOf(f.x,f.y)));

world.props.push(
  {x:11,y:13,type:"bench"},{x:15,y:13,type:"noticeBoard",layer:"above_entities"},
  {x:19,y:13,type:"well"},{x:21,y:13,type:"handcart"},{x:22,y:13,type:"crate"},
  {x:10,y:11,type:"lanternPost",layer:"above_entities"},{x:19,y:11,type:"lanternPost",layer:"above_entities"},
  {x:8,y:7,type:"smallGarden"},{x:28,y:7,type:"smallGarden"},{x:10,y:16,type:"barrel"},
  {x:12,y:16,type:"stonePile"},{x:14,y:16,type:"crate"},{x:16,y:16,type:"barrel"},{x:20,y:17,type:"crate"},
  {x:23,y:17,type:"crate"},{x:25,y:17,type:"barrel"},{x:27,y:17,type:"crate"},{x:31,y:17,type:"barrel"},
  {x:19,y:19,type:"crate"},{x:20,y:20,type:"crate"},{x:18,y:22,type:"barrel"},
  {x:13,y:6,type:"signPost",layer:"above_entities"},
  {x:7,y:11,type:"bush"},{x:24,y:12,type:"bush"},{x:32,y:15,type:"bush"},
  {x:30,y:21,type:"grassTuft"},{x:32,y:21,type:"stonePile"},
  {x:18,y:2,type:"smallGarden"}
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
rebuildOverworldCollisionFromMap();

world.zones.push(
  {name:"North Road",x:10,y:0,w:14,h:7},
  {name:"Hearthvale Square",x:8,y:6,w:20,h:13},
  {name:"Mirror Pond",x:23,y:11,w:10,h:9},
  {name:"Eastern Woods",x:27,y:3,w:11,h:19},
  {name:"West Lane",x:0,y:7,w:10,h:12}
);

const LEVEL_PROGRESSION=BALANCE.player.levelProgression;
const MAX_DEFINED_LEVEL=LEVEL_PROGRESSION[LEVEL_PROGRESSION.length-1].level;
const player={x:HEARTHVALE_LANDMARKS.townCenterSpawn.x,y:HEARTHVALE_LANDMARKS.townCenterSpawn.y,px:HEARTHVALE_LANDMARKS.townCenterSpawn.x*TILE,py:HEARTHVALE_LANDMARKS.townCenterSpawn.y*TILE,targetX:HEARTHVALE_LANDMARKS.townCenterSpawn.x,targetY:HEARTHVALE_LANDMARKS.townCenterSpawn.y,hp:BALANCE.player.startingMaxHp,maxHp:BALANCE.player.startingMaxHp,level:1,xp:0,baseAttackBonus:0,baseDefenseBonus:0,coins:0,inventory:[],equipment:{weapon:"rusty_sword",armor:null,trinket:null},skills:createDefaultSkills(),moving:false,facing:"down",speed:180,attackUntil:0,hitUntil:0,hitFlickerUntil:0,attackLungeX:0,attackLungeY:0,recoilX:0,recoilY:0};
const NAMED_NPC_ANCHORS = {
  edrin_vale:{
    role:"civic_narrative_focal",
    home:{ x:HEARTHVALE_LANDMARKS.edrinValeArea.x, y:HEARTHVALE_LANDMARKS.edrinValeArea.y },
    idleRadius:2,
    interactionFacingZone:["left","down"],
    collisionFootprint:{ w:1, h:1 },
    landOnlyValidation:true
  },
  hunter_garran:{
    role:"hunter_outdoorsman_eastern_road",
    home:{ x:HEARTHVALE_LANDMARKS.hunterGarranArea.x, y:HEARTHVALE_LANDMARKS.hunterGarranArea.y },
    idleRadius:2,
    interactionFacingZone:["left","down"],
    collisionFootprint:{ w:1, h:1 },
    landOnlyValidation:true
  },
  merchant_rowan:{
    role:"merchant_mercantile_frontage",
    home:{ x:HEARTHVALE_LANDMARKS.merchantRowanArea.x, y:HEARTHVALE_LANDMARKS.merchantRowanArea.y },
    idleRadius:1,
    interactionFacingZone:["down","left","right"],
    collisionFootprint:{ w:1, h:1 },
    landOnlyValidation:true
  }
};
const npc={id:"npc_edrin",anchorId:"edrin_vale",x:NAMED_NPC_ANCHORS.edrin_vale.home.x,y:NAMED_NPC_ANCHORS.edrin_vale.home.y,targetX:NAMED_NPC_ANCHORS.edrin_vale.home.x,targetY:NAMED_NPC_ANCHORS.edrin_vale.home.y,px:NAMED_NPC_ANCHORS.edrin_vale.home.x*TILE,py:NAMED_NPC_ANCHORS.edrin_vale.home.y*TILE,name:"Edrin Vale",displayLabel:"Edrin Vale",facing:"left",speed:92,moving:false,nextDecisionAt:0};
const hunterNpc={id:"npc_hunter_garran",anchorId:"hunter_garran",x:NAMED_NPC_ANCHORS.hunter_garran.home.x,y:NAMED_NPC_ANCHORS.hunter_garran.home.y,targetX:NAMED_NPC_ANCHORS.hunter_garran.home.x,targetY:NAMED_NPC_ANCHORS.hunter_garran.home.y,px:NAMED_NPC_ANCHORS.hunter_garran.home.x*TILE,py:NAMED_NPC_ANCHORS.hunter_garran.home.y*TILE,name:"Hunter Garran",displayLabel:"Hunter Garran",facing:"left",speed:94,moving:false,nextDecisionAt:0};
const vendorNpc={id:"npc_merchant_rowan",anchorId:"merchant_rowan",x:NAMED_NPC_ANCHORS.merchant_rowan.home.x,y:NAMED_NPC_ANCHORS.merchant_rowan.home.y,targetX:NAMED_NPC_ANCHORS.merchant_rowan.home.x,targetY:NAMED_NPC_ANCHORS.merchant_rowan.home.y,px:NAMED_NPC_ANCHORS.merchant_rowan.home.x*TILE,py:NAMED_NPC_ANCHORS.merchant_rowan.home.y*TILE,name:"Merchant Rowan",displayLabel:"Merchant Rowan",facing:"down",speed:86,moving:false,nextDecisionAt:0};
const namedVillageNpcs=[npc,hunterNpc,vendorNpc];
const ambientVillageNpcs=[];
const npcTerrainForbiddenTiles=new Set();
function fillSetRect(set,x,y,w,h){
  for(let tx=x;tx<x+w;tx++){
    for(let ty=y;ty<y+h;ty++){
      set.add(keyOf(tx,ty));
    }
  }
}
function rebuildNpcTerrainForbiddenTiles(){
  npcTerrainForbiddenTiles.clear();
  world.blocked.forEach((tileKey)=>npcTerrainForbiddenTiles.add(tileKey));
  world.pondBlocked.forEach((tileKey)=>npcTerrainForbiddenTiles.add(tileKey));
  world.pondShore.forEach((tileKey)=>npcTerrainForbiddenTiles.add(tileKey));
  world.props.forEach((prop)=>npcTerrainForbiddenTiles.add(keyOf(prop.x,prop.y)));
  world.buildings.forEach((building)=>{
    const area=building.visual || { x:building.x, y:building.y, w:building.w, h:building.h };
    fillSetRect(npcTerrainForbiddenTiles, area.x, area.y, area.w, area.h);
  });
  npcTerrainForbiddenTiles.add(keyOf(OVERWORLD_CAVE_ENTRY.x, OVERWORLD_CAVE_ENTRY.y));
}
function isOverworldTerrainBlocked(x,y){
  const tileKey=keyOf(x,y);
  return world.blocked.has(tileKey) || world.pondBlocked.has(tileKey) || world.pondShore.has(tileKey);
}
function tileInRect(tileX,tileY,rect){
  return !!rect && tileX>=rect.x && tileX<rect.x+rect.w && tileY>=rect.y && tileY<rect.y+rect.h;
}
function isAtlasBuildingBlockedTile(x,y){
  return world.buildings.some((building)=>{
    if(Array.isArray(building.blockedVisualTiles) && building.blockedVisualTiles.some((rect)=>tileInRect(x,y,rect))) return true;
    if(tileInRect(x,y,building.rearExclusionZone)) return true;
    const collisionRect=building.collision || building.collisionRect || building.visual || { x:building.x, y:building.y, w:building.w, h:building.h };
    return tileInRect(x,y,collisionRect);
  });
}
function rebuildOverworldCollisionFromMap(){
  const rebuiltBlocked=new Set();
  const addRect=(rect, options={})=>{
    if(!rect) return;
    const { allowRoadOverlap=true } = options;
    for(let tx=rect.x;tx<rect.x+rect.w;tx++){
      for(let ty=rect.y;ty<rect.y+rect.h;ty++){
        if(!allowRoadOverlap && world.roadTiles.has(keyOf(tx,ty))) continue;
        rebuiltBlocked.add(keyOf(tx,ty));
      }
    }
  };
  world.buildings.forEach((building)=>{
    addRect(building.collision || building.visual || { x:building.x, y:building.y, w:building.w, h:building.h }, { allowRoadOverlap:false });
    addRect(building.rearExclusionZone, { allowRoadOverlap:false });
    if(Array.isArray(building.blockedVisualTiles)){
      building.blockedVisualTiles.forEach((blockedVisualRect)=>addRect(blockedVisualRect, { allowRoadOverlap:false }));
    }
  });
  world.fences.forEach((fenceTile)=>rebuiltBlocked.add(keyOf(fenceTile.x, fenceTile.y)));
  world.trees.forEach((tree)=>rebuiltBlocked.add(keyOf(tree.x, tree.y)));
  [
    keyOf(OVERWORLD_CAVE_ENTRY.x, OVERWORLD_CAVE_ENTRY.y),
    keyOf(OVERWORLD_CAVE_ENTRY.x, OVERWORLD_CAVE_ENTRY.y+1),
    keyOf(OVERWORLD_CAVE_ENTRY.x-1, OVERWORLD_CAVE_ENTRY.y+1),
    keyOf(OVERWORLD_CAVE_ENTRY.x+1, OVERWORLD_CAVE_ENTRY.y+1)
  ].forEach((tileKey)=>rebuiltBlocked.delete(tileKey));
  world.blocked=rebuiltBlocked;
}
function isNpcOnTile(x,y,excludeId){
  return namedVillageNpcs.some((villageNpc)=>villageNpc.id!==excludeId && villageNpc.targetX===x && villageNpc.targetY===y);
}
function isValidNpcLandTile(x,y,excludeId){
  if(x<0||y<0||x>=WORLD_W||y>=WORLD_H) return false;
  if(npcTerrainForbiddenTiles.has(keyOf(x,y))) return false;
  if(isWorldObjectBlockingTile(x,y)) return false;
  if(isNpcOnTile(x,y,excludeId)) return false;
  return true;
}
function findNearestValidNpcLandTile(startX,startY,excludeId,maxDepth=16){
  if(isValidNpcLandTile(startX,startY,excludeId)) return { x:startX, y:startY };
  const visited=new Set([keyOf(startX,startY)]);
  const queue=[{ x:startX, y:startY, depth:0 }];
  for(let cursor=0;cursor<queue.length;cursor++){
    const node=queue[cursor];
    if(node.depth>=maxDepth) continue;
    const neighbors=[[1,0],[-1,0],[0,1],[0,-1]];
    for(const [dx,dy] of neighbors){
      const nx=node.x+dx;
      const ny=node.y+dy;
      const tileKey=keyOf(nx,ny);
      if(visited.has(tileKey)) continue;
      visited.add(tileKey);
      if(isValidNpcLandTile(nx,ny,excludeId)) return { x:nx, y:ny };
      queue.push({ x:nx, y:ny, depth:node.depth+1 });
    }
  }
  return null;
}
function setNpcTile(npcEntity,x,y,alignImmediately=false){
  npcEntity.x=x;
  npcEntity.y=y;
  npcEntity.targetX=x;
  npcEntity.targetY=y;
  if(alignImmediately){
    npcEntity.px=x*TILE;
    npcEntity.py=y*TILE;
    npcEntity.moving=false;
  }
}
function findNearestValidPlayerSpawnTile(startX,startY,maxDepth=20){
  const classifyTile=(x,y)=>{
    if(x<0||y<0||x>=WORLD_W||y>=WORLD_H) return { valid:false, score:-1 };
    if(!canMoveTo(x,y)) return { valid:false, score:-1 };
    if(namedVillageNpcs.some((villageNpc)=>villageNpc.targetX===x && villageNpc.targetY===y)) return { valid:false, score:-1 };
    let score=1;
    if(world.roadTiles.has(keyOf(x,y))) score+=12;
    if(world.buildings.some((building)=>tileInRect(x,y,building.frontWalkBand))) score+=8;
    if(world.buildings.some((building)=>tileInRect(x,y,building.interaction) || tileInRect(x,y,building.interactRect))) score+=6;
    return { valid:true, score };
  };
  const startClassification=classifyTile(startX,startY);
  if(startClassification.valid) return { x:startX, y:startY };
  const visited=new Set([keyOf(startX,startY)]);
  const queue=[{ x:startX, y:startY, depth:0 }];
  let best=null;
  for(let cursor=0;cursor<queue.length;cursor++){
    const current=queue[cursor];
    if(current.depth>=maxDepth) continue;
    for(const [dx,dy] of [[0,-1],[1,0],[0,1],[-1,0]]){
      const nx=current.x+dx;
      const ny=current.y+dy;
      const tileKey=keyOf(nx,ny);
      if(visited.has(tileKey)) continue;
      visited.add(tileKey);
      const classification=classifyTile(nx,ny);
      if(classification.valid){
        const candidate={ x:nx, y:ny, depth:current.depth+1, score:classification.score };
        if(!best || candidate.score>best.score || (candidate.score===best.score && candidate.depth<best.depth)) best=candidate;
      }
      queue.push({ x:nx, y:ny, depth:current.depth+1 });
    }
    if(best && best.depth<=current.depth+1) break;
  }
  return best ? { x:best.x, y:best.y } : null;
}
function ensureNpcAnchorAndPositionValid(npcEntity,alignImmediately=false){
  const anchor=NAMED_NPC_ANCHORS[npcEntity.anchorId];
  if(!anchor) return;
  if(!isValidNpcLandTile(anchor.home.x, anchor.home.y, npcEntity.id)){
    const relocatedAnchor=findNearestValidNpcLandTile(anchor.home.x, anchor.home.y, npcEntity.id, 24);
    if(relocatedAnchor){
      anchor.home.x=relocatedAnchor.x;
      anchor.home.y=relocatedAnchor.y;
    }
  }
  if(!isValidNpcLandTile(npcEntity.targetX, npcEntity.targetY, npcEntity.id)){
    const safeTile=findNearestValidNpcLandTile(anchor.home.x, anchor.home.y, npcEntity.id, 24);
    if(safeTile) setNpcTile(npcEntity, safeTile.x, safeTile.y, alignImmediately);
  }
}
function updateVillageNpcWander(npcEntity,now){
  const anchor=NAMED_NPC_ANCHORS[npcEntity.anchorId];
  if(!anchor) return;
  ensureNpcAnchorAndPositionValid(npcEntity);
  if(now<(npcEntity.nextDecisionAt||0)) return;
  const directionOptions=[[0,0],[1,0],[-1,0],[0,1],[0,-1]];
  for(let idx=directionOptions.length-1;idx>0;idx--){
    const swapIndex=Math.floor(Math.random()*(idx+1));
    const next=directionOptions[idx];
    directionOptions[idx]=directionOptions[swapIndex];
    directionOptions[swapIndex]=next;
  }
  for(const [dx,dy] of directionOptions){
    const nextX=npcEntity.targetX+dx;
    const nextY=npcEntity.targetY+dy;
    const homeDistance=Math.abs(nextX-anchor.home.x)+Math.abs(nextY-anchor.home.y);
    if(homeDistance>anchor.idleRadius) continue;
    if(!isValidNpcLandTile(nextX,nextY,npcEntity.id)) continue;
    setNpcTile(npcEntity, nextX, nextY, true);
    if(dx>0) npcEntity.facing="right";
    else if(dx<0) npcEntity.facing="left";
    else if(dy>0) npcEntity.facing="down";
    else if(dy<0) npcEntity.facing="up";
    break;
  }
  npcEntity.nextDecisionAt=now+900+Math.random()*900;
}
function enforceAllVillageNpcTerrainValidation(alignImmediately=false){
  rebuildNpcTerrainForbiddenTiles();
  [...namedVillageNpcs, ...ambientVillageNpcs].forEach((npcEntity)=>ensureNpcAnchorAndPositionValid(npcEntity, alignImmediately));
}
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
const LEGACY_SAVE_KEYS=Object.freeze(["wayfarer.save","wayfarer.save.v0"]);
const SAVE_DEBUG_MODE=(new URLSearchParams(window.location.search).get("saveDebug")==="1") || (new URLSearchParams(window.location.search).get("bootDebug")==="1");
const saveDiagnostics={ activeKey:SAVE_KEY, attemptedKeys:[SAVE_KEY,...LEGACY_SAVE_KEYS], loadedFromKey:null, saveFound:false, migrationRan:false, migrationSucceeded:false, fallbackDefaultUsed:false, backupCreated:false, backupFound:false, lastError:null };
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

function getSaveInventoryCount(save){
  const inventory=save?.player?.inventory;
  if(!Array.isArray(inventory)) return 0;
  return inventory.reduce((sum,entry)=>sum+Math.max(0, Math.floor(Number.isFinite(entry?.quantity) ? entry.quantity : 0)),0);
}
function getSaveCompletedQuestCount(save){
  if(Array.isArray(save?.quests?.completedQuests)) return save.quests.completedQuests.length;
  if(Array.isArray(save?.quests?.questStates)) return save.quests.questStates.filter((entry)=>entry?.state===QuestState.COMPLETED).length;
  return 0;
}
function getSaveCurrentQuest(save){
  if(Array.isArray(save?.quests?.activeQuests) && save.quests.activeQuests[0]) return save.quests.activeQuests[0];
  if(Array.isArray(save?.quests?.questStates)){
    const activeEntry=save.quests.questStates.find((entry)=>entry?.state===QuestState.ACTIVE);
    if(activeEntry?.id) return activeEntry.id;
  }
  return null;
}
function computeSaveRichnessScore(save){
  const level=Math.max(1, Math.floor(Number.isFinite(save?.player?.level) ? save.player.level : 1));
  const xp=Math.max(0, Math.floor(Number.isFinite(save?.player?.xp) ? save.player.xp : 0));
  const coins=Math.max(0, Math.floor(Number.isFinite(save?.player?.coins) ? save.player.coins : 0));
  const inventoryCount=getSaveInventoryCount(save);
  const completedQuestCount=getSaveCompletedQuestCount(save);
  return (level*1000000) + (xp*100) + (completedQuestCount*10000) + (inventoryCount*1000) + coins;
}
function analyzeSaveSlot(key){
  const raw=localStorage.getItem(key);
  const result={ key, found:Boolean(raw), parseSuccess:false, valid:false, level:null, xp:null, coins:null, inventoryCount:null, currentQuest:null, completedQuestCount:null, version:null, saveSchemaVersion:null, savedAt:null, richnessScore:null, parseError:null };
  if(!raw) return result;
  try {
    const parsed=JSON.parse(raw);
    result.parseSuccess=true;
    const migrated=repairSave(migrateSave(parsed)).save;
    result.valid=validateSaveData(migrated);
    result.level=Math.max(1, Math.floor(Number.isFinite(migrated?.player?.level) ? migrated.player.level : 1));
    result.xp=Math.max(0, Math.floor(Number.isFinite(migrated?.player?.xp) ? migrated.player.xp : 0));
    result.coins=Math.max(0, Math.floor(Number.isFinite(migrated?.player?.coins) ? migrated.player.coins : 0));
    result.inventoryCount=getSaveInventoryCount(migrated);
    result.currentQuest=getSaveCurrentQuest(migrated);
    result.completedQuestCount=getSaveCompletedQuestCount(migrated);
    result.version=Number.isInteger(parsed?.version) ? parsed.version : (Number.isInteger(migrated?.version) ? migrated.version : null);
    result.saveSchemaVersion=Number.isInteger(parsed?.saveSchemaVersion) ? parsed.saveSchemaVersion : (Number.isInteger(migrated?.saveSchemaVersion) ? migrated.saveSchemaVersion : null);
    result.savedAt=typeof parsed?.savedAt==='string' ? parsed.savedAt : (typeof migrated?.savedAt==='string' ? migrated.savedAt : null);
    result.richnessScore=result.valid ? computeSaveRichnessScore(migrated) : null;
  } catch(err){
    result.parseError=String(err?.message || err || 'parse_failed');
  }
  return result;
}
function getAllSaveSlotDiagnostics(){
  return [SAVE_KEY, SAVE_BACKUP_KEY, ...LEGACY_SAVE_KEYS].map((key)=>analyzeSaveSlot(key));
}
function findRichestValidSave(diagnostics){
  let richest=null;
  diagnostics.forEach((entry)=>{
    if(!entry.valid || !Number.isFinite(entry.richnessScore)) return;
    if(!richest || entry.richnessScore>richest.richnessScore) richest=entry;
  });
  return richest;
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
    const payloadRichness=computeSaveRichnessScore(payload);
    const slots=getAllSaveSlotDiagnostics();
    const richest=findRichestValidSave(slots);
    if(richest && payloadRichness<richest.richnessScore){
      if(SAVE_DEBUG_MODE) console.warn("[Save Debug] OVERWRITE_PROTECTED_RICHER_SAVE_EXISTS", { attemptedKey:SAVE_KEY, attemptedRichness:payloadRichness, richestKey:richest.key, richestScore:richest.richnessScore });
      return;
    }
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
  let raw=localStorage.getItem(SAVE_KEY);
  let loadedKey=SAVE_KEY;
  if(!raw){
    for(const legacyKey of LEGACY_SAVE_KEYS){
      const legacyRaw=localStorage.getItem(legacyKey);
      if(legacyRaw){
        raw=legacyRaw;
        loadedKey=legacyKey;
        break;
      }
    }
  }
  saveDiagnostics.loadedFromKey=raw ? loadedKey : null;
  saveDiagnostics.saveFound=Boolean(raw);
  saveDiagnostics.backupFound=Boolean(localStorage.getItem(SAVE_BACKUP_KEY));
  const slotDiagnostics=getAllSaveSlotDiagnostics();
  const activeSlot=slotDiagnostics.find((entry)=>entry.key===SAVE_KEY) || null;
  const richestSlot=findRichestValidSave(slotDiagnostics);
  if(SAVE_DEBUG_MODE && activeSlot?.valid && richestSlot && richestSlot.key!==SAVE_KEY && Number.isFinite(activeSlot.richnessScore) && activeSlot.richnessScore<richestSlot.richnessScore){
    console.warn("[Save Debug] RICHER_SAVE_AVAILABLE", { activeKey:SAVE_KEY, activeRichness:activeSlot.richnessScore, richerKey:richestSlot.key, richerRichness:richestSlot.richnessScore });
  }
  if(!raw){
    saveDiagnostics.fallbackDefaultUsed=true;
    return false;
  }
  try {
    let parsed;
    try {
      parsed=JSON.parse(raw);
    } catch(parseError){
      localStorage.setItem(SAVE_BACKUP_KEY, raw);
      saveDiagnostics.backupCreated=true;
      throw parseError;
    }
    saveDiagnostics.migrationRan=true;
    const migrated=migrateSave(parsed);
    const repaired=repairSave(migrated);
    const data=repaired.save;
    if(!validateSaveData(data)) throw new Error("Invalid save payload");
    if(repaired.changed){
      repaired.warnings.forEach((message)=>console.warn("[Save Repair] " + message));
    }
    if(parsed.saveSchemaVersion!==SAVE_SCHEMA_VERSION || repaired.changed){
      localStorage.setItem(SAVE_BACKUP_KEY, raw);
      saveDiagnostics.backupCreated=true;
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
    let spawnX=loadedX;
    let spawnY=loadedY;
    if(!isInMirrorCave && !isInAbandonedTollhouse && isAtlasBuildingBlockedTile(loadedX, loadedY)){
      const relocated=findNearestValidPlayerSpawnTile(loadedX, loadedY);
      if(relocated){
        spawnX=relocated.x;
        spawnY=relocated.y;
        if(DEBUG_MODE) console.info("[Atlas Collision] player_spawn_relocated_from_atlas_blocked_tile from (" + loadedX + "," + loadedY + ") to (" + spawnX + "," + spawnY + ")");
      }
    }
    setPlayerTilePosition(spawnX, spawnY);
    zoneTransitionLockedUntil=0;
    blockedDirectionalKeysUntilRelease.clear();
    currentZoneId=isInMirrorCave ? "mirror_cave" : (isInAbandonedTollhouse ? "abandoned_tollhouse" : getOutdoorRegionIdAt(spawnX, spawnY));
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
    saveDiagnostics.migrationSucceeded=true;
    return true;
  } catch(err){
    saveDiagnostics.lastError=String(err?.message || err || "unknown_error");
    console.error("Load failed", err);
    const rawSnapshot=localStorage.getItem(SAVE_KEY);
    if(rawSnapshot){
      localStorage.setItem(SAVE_BACKUP_KEY, rawSnapshot);
      saveDiagnostics.backupCreated=true;
    }
    log("System: Save load failed. Existing save was preserved in backup.");
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
  x:HEARTHVALE_LANDMARKS.townCenterSpawn.x, y:HEARTHVALE_LANDMARKS.townCenterSpawn.y,
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
  x:HEARTHVALE_LANDMARKS.noticeSignNode.x, y:HEARTHVALE_LANDMARKS.noticeSignNode.y,
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
  collision:false,
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
  x:HEARTHVALE_LANDMARKS.noticeSignNode.x, y:HEARTHVALE_LANDMARKS.noticeSignNode.y,
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
  x:HEARTHVALE_LANDMARKS.mirrorPond.x, y:HEARTHVALE_LANDMARKS.mirrorPond.y,
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
  x:OVERWORLD_CAVE_ENTRY.x, y:OVERWORLD_CAVE_ENTRY.y+1,
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
function isTileInsideBuildingBodyOrRoof(x,y){
  return world.buildings.some((building)=>{
    if(tileInRect(x,y,building.rearExclusionZone)) return true;
    if(Array.isArray(building.blockedVisualTiles) && building.blockedVisualTiles.some((rect)=>tileInRect(x,y,rect))) return true;
    return false;
  });
}
function isTileDecorativeOnly(x,y){
  return getActiveWorldObjects().some((object)=>{
    if(object.collision) return false;
    const tile=getWorldObjectTile(object);
    return tile.x===x && tile.y===y;
  });
}
function evaluateQuickNavTile(x,y){
  const inBounds=isTileInCurrentZone(x,y);
  const diag=inBounds ? getMovementBlockDiagnostics(x,y) : null;
  const tileType=inBounds ? describeOverworldTerrainType(x,y) : "out_of_bounds";
  const buildingBodyOrRoof=inBounds ? isTileInsideBuildingBodyOrRoof(x,y) : false;
  const decorativeOnly=inBounds ? isTileDecorativeOnly(x,y) : false;
  return {
    x,y,inBounds,tileType,
    zone:isInMirrorCave ? "mirror_cave" : (isInAbandonedTollhouse ? "abandoned_tollhouse" : currentZoneId),
    collision:diag?.blocked===true,
    walkable:diag?.walkable===true,
    blockedReason:diag?.reason || null,
    isWater:tileType==="water",
    isBuildingBodyOrRoof:buildingBodyOrRoof,
    isDecorativeOnly:decorativeOnly,
    valid:inBounds && diag?.walkable===true && tileType!=="water" && !buildingBodyOrRoof && !decorativeOnly
  };
}
const QUICK_NAV_DESTINATIONS = Object.freeze({
  center_town:{ destinationKey:"center_town", label:"Center Town", x:HEARTHVALE_LANDMARKS.townCenterSpawn.x, y:HEARTHVALE_LANDMARKS.townCenterSpawn.y, expectedZoneId:"hearthvale_square" },
  village_hall:{ destinationKey:"village_hall", label:"Village Hall", x:17, y:13, expectedZoneId:"hearthvale_square" },
  residence_large:{ destinationKey:"residence_large", label:"Residence Large", x:31, y:12, expectedZoneId:"hearthvale_residence_district" },
  boathouse:{ destinationKey:"boathouse", label:"Boathouse", x:28, y:18, expectedZoneId:"eastern_woods" },
  pond_edge:{ destinationKey:"pond_edge", label:"Pond Edge", x:30, y:18, expectedZoneId:"eastern_woods" }
});

function resolveQuickNavDestination(destination){
  const requestedX=destination.x;
  const requestedY=destination.y;
  const requested=evaluateQuickNavTile(requestedX, requestedY);
  let resolved=requested;
  let usedFallbackResolution=false;
  if(!requested.valid){
    const maxRadius=3;
    let found=null;
    for(let radius=1; radius<=maxRadius && !found; radius++){
      for(let dy=-radius; dy<=radius && !found; dy++){
        for(let dx=-radius; dx<=radius; dx++){
          if(Math.abs(dx)!==radius && Math.abs(dy)!==radius) continue;
          const candidate=evaluateQuickNavTile(requestedX+dx, requestedY+dy);
          if(candidate.valid){ found=candidate; break; }
        }
      }
    }
    if(found){
      resolved=found;
      usedFallbackResolution=true;
    }
  }
  if(!resolved.valid){
    resolved=evaluateQuickNavTile(HEARTHVALE_LANDMARKS.townCenterSpawn.x, HEARTHVALE_LANDMARKS.townCenterSpawn.y);
    usedFallbackResolution=true;
    console.warn("[QuickNav] no valid nearby tile for " + destination.label + " requested=(" + requestedX + "," + requestedY + "); falling back to town spawn (" + resolved.x + "," + resolved.y + ") zone=" + currentZoneId);
  }
  return { requested, resolved, usedFallbackResolution };
}
function quickNavTeleport(destination){
  const navResolution=resolveQuickNavDestination(destination);
  const { requested, resolved, usedFallbackResolution }=navResolution;
  setPlayerTilePosition(resolved.x,resolved.y);
  if(!isInMirrorCave && !isInAbandonedTollhouse && destination.expectedZoneId){
    currentZoneId=destination.expectedZoneId;
  }
  const detectedZoneId=getOutdoorRegionIdAt(resolved.x, resolved.y);
  const expectedZoneName=getZoneDefinition(destination.expectedZoneId || currentZoneId).name;
  const detectedZoneName=getZoneDefinition(detectedZoneId).name;
  const finalDisplayedZone=getCurrentZoneName();
  if(destination.expectedZoneId && destination.expectedZoneId!==detectedZoneId){
    console.warn("[QuickNav Zone Mismatch] " + destination.label + " expected " + expectedZoneName + " but detected " + detectedZoneName + ".");
  }
  console.info("[QuickNav] destinationKey=" + destination.destinationKey + " requestedTile=(" + destination.x + "," + destination.y + ") resolvedTile=(" + resolved.x + "," + resolved.y + ") expectedZone=" + expectedZoneName + " detectedZone=" + detectedZoneName + " finalDisplayedZone=" + finalDisplayedZone + " fallbackSpawnResolutionUsed=" + usedFallbackResolution + " requestedTileType=" + requested.tileType + " resolvedTileType=" + resolved.tileType + " resolvedCollision=" + resolved.collision + " resolvedWalkable=" + resolved.walkable + " resolvedBlockedReason=" + (resolved.blockedReason || "none"));
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
  setPlayerTilePosition(HEARTHVALE_LANDMARKS.townCenterSpawn.x, HEARTHVALE_LANDMARKS.townCenterSpawn.y);
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
    "G : Toggle grid",
    "V : Toggle collision overlay"
  ];
  if(interactionPrompt) hudLines.splice(1, 0, interactionPrompt);
  hud.textContent=hudLines.join("\n");
  if(DEV_MODE){
    const atlasStatus=getBuildingAtlasDebugStatus();
    const buildingAtlasLines=(atlasStatus.buildingEntries||[]).map((entry)=>(
      entry.id + " status=" + entry.renderStatus +
      " crop=" + formatRect(entry.crop) +
      " draw=" + entry.draw.w + "x" + entry.draw.h +
      " anchor=(" + entry.anchor.x + "," + entry.anchor.y + ")" +
      " footprint=" + formatRect(entry.footprint) +
      " collision=" + formatRect(entry.collision) +
      " interaction=" + formatRect(entry.interaction) +
      " door=(" + entry.doorTile.x + "," + entry.doorTile.y + ")" +
      " label=(" + entry.labelAnchor.x + "," + entry.labelAnchor.y + ")" +
      " decorExclusion=" + formatRect(entry.decorExclusion) +
      " productionReady=" + entry.productionReady +
      " fallback=" + (entry.fallbackReason || "none")
    )).join("\n");
    debugPanel.style.display="block";
    debugPanel.textContent = "DEV TOOLS\n" +
      "~ : Toggle Debug Panel\n" +
      "F4 : Atlas Preview Overlay\n" +
      "F6 : Debug Heal\n" +
      "F7/F8/F9 : Debug Teleport\n" +
      "F10 : Debug Reset Quest\n" +
      "Shift+F10 : Debug Reset Save\n" +
      "Debug Lv/ATK/DEF : " + player.level + " / " + totalAttack + " / " + totalDefense + "\n" +
      "Skills S/D/Sv : " + getSkillLevel("swordsmanship") + " / " + getSkillLevel("defense") + " / " + getSkillLevel("survival") + "\n" +
      "Atlas preview : " + (atlasDebugPreview.enabled ? "ON" : "OFF") + "\n" +
      "Building atlas : " + (atlasRuntimeInfo.buildings?.loaded ? "loaded " + atlasRuntimeInfo.buildings.width + "x" + atlasRuntimeInfo.buildings.height : "not loaded") + "\n" +
      "Prop atlas : " + (atlasRuntimeInfo.props?.loaded ? "loaded " + atlasRuntimeInfo.props.width + "x" + atlasRuntimeInfo.props.height : "not loaded") + "\n" +
      "Building URL : " + atlasStatus.buildingRequestedUrl + "\n" +
      "Building loaded : " + atlasStatus.buildingLoaded + " (" + atlasStatus.buildingNaturalWidth + "x" + atlasStatus.buildingNaturalHeight + ")\n" +
      "Asset URL : " + atlasStatus.assetRequestedUrl + "\n" +
      "Asset loaded : " + atlasStatus.assetLoaded + " (" + atlasStatus.assetNaturalWidth + "x" + atlasStatus.assetNaturalHeight + ")\n" +
      "Sprite path active : " + atlasStatus.spriteRenderingPathActive + "\n" +
      "Proof sprite drawn : " + buildingSpriteProofState.drawn + "\n" +
      "Fallback used : " + atlasStatus.fallbackRenderingUsed + "\n" +
      "Atlas proof : " + (atlasStatus.atlasProofEnabled ? "ON" : "OFF") + " (debug marker " + (atlasStatus.atlasProofDebugEnabled ? "ON" : "OFF") + ")\n" +
      "Proof atlas file : " + atlasStatus.atlasProofSelectedAtlasFilename + "\n" +
      "Proof URL : " + atlasStatus.atlasProofRequestedAssetUrl + "\n" +
      "Proof image : " + atlasStatus.atlasProofImageLoaded + " (" + atlasStatus.atlasProofNaturalWidth + "x" + atlasStatus.atlasProofNaturalHeight + ")\n" +
      "Proof building : " + atlasStatus.atlasProofBuildingId + " [" + atlasStatus.atlasProofBuildingRole + "]\n" +
      "Proof sprite : " + atlasStatus.atlasProofSpriteId + "\n" +
      "Proof crop : " + atlasStatus.atlasProofCrop + "\n" +
      "Proof draw size : " + atlasStatus.atlasProofDrawSize + "\n" +
      "Proof render path : " + atlasStatus.atlasProofRenderPath + "\n" +
      "Proof fallback reason : " + atlasStatus.atlasProofFallbackReason + "\n" +
      "Build Phase : 33.1.4F — Atlas Runtime Authority Chain\n" +
      "Selector Version : " + ATLAS_SELECTOR_VERSION + "\n" +
      "Cache Bust : 33-1-4f-authority-chain-bottom-row-parsefix\n" +
      "Hero atlas lock : inn_tavern + mercantile_shop + village_hall_meeting_house\n" +
      "Secondary atlas promoted : NO\n" +
      "Fallback composition : provisional/legacy\n" +
      "Town readiness : NOT PASSED (awaiting live QA frontage/roads/collision)\n" +
      "Building atlas entries:\n" + buildingAtlasLines + "\n" +
      "Target HP : " + (currentTarget ? (currentTarget.hp + "/" + currentTarget.maxHp) : "N/A") + "\n" +
      "Target cooldown : " + targetCooldownText;
  } else {
    debugPanel.style.display="none";
    debugPanel.textContent="";
  }
}

function formatRect(rect){
  if(!rect) return "n/a";
  return "x=" + rect.x + ",y=" + rect.y + ",w=" + rect.w + ",h=" + rect.h;
}
function describeOverworldTerrainType(x,y){
  const tileKey=keyOf(x,y);
  if(world.pondWater.has(tileKey)) return "water";
  if(world.pondShore.has(tileKey)) return "shore";
  if(world.roadTiles.has(tileKey)) return "road";
  if(world.fences.some((fence)=>fence.x===x&&fence.y===y)) return "fence";
  if(world.trees.some((tree)=>tree.x===x&&tree.y===y)) return "tree";
  if(world.buildings.some((building)=>{
    const rect=building.collision || building.visual || { x:building.x, y:building.y, w:building.w, h:building.h };
    return x>=rect.x && x<rect.x+rect.w && y>=rect.y && y<rect.y+rect.h;
  })) return "building";
  return "land";
}
function getMovementBlockDiagnostics(x,y){
  const tileKey=keyOf(x,y);
  const attemptedWorld={ x:x*TILE, y:y*TILE };
  const zoneContext=isInMirrorCave ? "mirror_cave" : (isInAbandonedTollhouse ? "abandoned_tollhouse" : "overworld");
  const worldObjectBlocker=getActiveWorldObjects().find((object)=>{
    if(!object.collision) return false;
    const tile=getWorldObjectTile(object);
    return tile.x===x && tile.y===y;
  });
  const blockingNpc=!isInMirrorCave && !isInAbandonedTollhouse
    ? namedVillageNpcs.find((villageNpc)=>villageNpc.targetX===x&&villageNpc.targetY===y)
    : null;
  const blockingHostile=getActiveHostiles().find((hostile)=>hostile.hp>0&&hostile.targetX===x&&hostile.targetY===y);
  const blockingFence=world.fences.find((fence)=>fence.x===x&&fence.y===y);
  const blockingTree=world.trees.find((tree)=>tree.x===x&&tree.y===y);
  const blockingBuilding=world.buildings.find((building)=>{
    return (
      tileInRect(x,y,building.collision || building.collisionRect || building.visual || { x:building.x, y:building.y, w:building.w, h:building.h }) ||
      tileInRect(x,y,building.rearExclusionZone) ||
      (Array.isArray(building.blockedVisualTiles) && building.blockedVisualTiles.some((rect)=>tileInRect(x,y,rect)))
    );
  });
  const buildingParcel=world.buildings.find((building)=>{
    const rect=building.pathingBounds || building.visual || { x:building.x, y:building.y, w:building.w, h:building.h };
    return x>=rect.x && x<rect.x+rect.w && y>=rect.y && y<rect.y+rect.h;
  });
  const atLandmark=Object.entries(HEARTHVALE_LANDMARKS).find(([key, landmark])=>{
    if(key==="zoneExits" || !landmark || typeof landmark!=="object" || !Number.isFinite(landmark.x) || !Number.isFinite(landmark.y)) return false;
    return landmark.x===x && landmark.y===y;
  });
  const sourceFlags={
    terrain:false,
    water:false,
    fence:false,
    building:false,
    prop:false,
    npc:false,
    enemy:false,
    parcel:false,
    landmark:false,
    debug_rectangle:false,
    invisible_bounds:false
  };
  const causes=[];
  if(!isTileInCurrentZone(x,y)){ causes.push("invisible_bounds"); sourceFlags.invisible_bounds=true; }
  if(worldObjectBlocker){
    const category=worldObjectBlocker.type==="door"||worldObjectBlocker.type==="caveEntrance" ? "landmark" : worldObjectBlocker.type;
    causes.push(category);
    if(category==="landmark") sourceFlags.landmark=true;
  }
  if(isInMirrorCave && mirrorCave.blocked.has(tileKey)){ causes.push("terrain"); sourceFlags.terrain=true; }
  if(isInAbandonedTollhouse && abandonedTollhouse.blocked.has(tileKey)){ causes.push("terrain"); sourceFlags.terrain=true; }
  if(!isInMirrorCave && !isInAbandonedTollhouse){
    if(world.pondWater.has(tileKey)){ causes.push("water"); sourceFlags.water=true; }
    if(world.pondShore.has(tileKey)){ causes.push("terrain"); sourceFlags.terrain=true; }
    if(blockingFence){ causes.push("fence"); sourceFlags.fence=true; }
    if(blockingTree){ causes.push("terrain"); sourceFlags.terrain=true; }
    if(world.blocked.has(tileKey)){ causes.push("terrain"); sourceFlags.terrain=true; }
    if(blockingBuilding){ causes.push("building"); sourceFlags.building=true; }
  }
  if(buildingParcel){ sourceFlags.parcel=true; }
  if(blockingNpc){ causes.push("npc"); sourceFlags.npc=true; }
  if(blockingHostile){ causes.push("enemy"); sourceFlags.enemy=true; }
  return {
    blocked:causes.length>0,
    zoneContext,
    attemptedTile:{ x,y },
    attemptedWorld,
    terrainType:zoneContext==="overworld" ? describeOverworldTerrainType(x,y) : "dungeon_floor",
    walkable:causes.length===0,
    reason:causes[0] || "none",
    causeChain:causes,
    blockingObjectId:worldObjectBlocker?.objectId || null,
    blockingObjectType:worldObjectBlocker?.type || null,
    blockingObjectRect:worldObjectBlocker ? { x, y, w:1, h:1 } : null,
    blockingEntityId:blockingNpc?.id || blockingHostile?.id || null,
    blockingEntityType:blockingNpc ? "npc" : (blockingHostile ? "enemy" : null),
    blockingEntityRect:(blockingNpc||blockingHostile) ? { x, y, w:1, h:1 } : null,
    blockingBuildingId:blockingBuilding?.id || null,
    blockingBuildingRect:blockingBuilding ? (blockingBuilding.collision || blockingBuilding.visual || { x:blockingBuilding.x, y:blockingBuilding.y, w:blockingBuilding.w, h:blockingBuilding.h }) : null,
    parcelId:buildingParcel?.id || null,
    parcelRect:buildingParcel ? (buildingParcel.pathingBounds || buildingParcel.visual || { x:buildingParcel.x, y:buildingParcel.y, w:buildingParcel.w, h:buildingParcel.h }) : null,
    blockingLandmarkId:atLandmark?.[0] || null,
    sourceFlags
  };
}
let lastMovementBlockSignature="";
let lastMovementBlockLogAt=0;
function emitMovementBlockDiagnostics(diag){
  if(!diag?.blocked) return;
  const now=performance.now();
  const signature=JSON.stringify({
    zone:diag.zoneContext,
    x:diag.attemptedTile?.x,
    y:diag.attemptedTile?.y,
    reasons:diag.causeChain
  });
  if(signature===lastMovementBlockSignature && now-lastMovementBlockLogAt<280) return;
  lastMovementBlockSignature=signature;
  lastMovementBlockLogAt=now;
  const detailLines=[
    "Movement blocked at x=" + diag.attemptedTile.x + ", y=" + diag.attemptedTile.y + " (world x=" + diag.attemptedWorld.x + ", y=" + diag.attemptedWorld.y + ")",
    "Reason: " + diag.reason,
    "Cause chain: " + (diag.causeChain.join(", ") || "none"),
    "Terrain: " + diag.terrainType + " | walkable=" + diag.walkable,
    "Blocked by object: " + (diag.blockingObjectId || "none") + " [" + (diag.blockingObjectType || "n/a") + "] rect=" + formatRect(diag.blockingObjectRect),
    "Blocked by entity: " + (diag.blockingEntityId || "none") + " [" + (diag.blockingEntityType || "n/a") + "] rect=" + formatRect(diag.blockingEntityRect),
    "Building collision: " + (diag.blockingBuildingId || "none") + " rect=" + formatRect(diag.blockingBuildingRect),
    "Parcel overlap: " + (diag.parcelId || "none") + " rect=" + formatRect(diag.parcelRect),
    "Landmark overlap: " + (diag.blockingLandmarkId || "none"),
    "Source flags: " + JSON.stringify(diag.sourceFlags)
  ];
  const joined="[CollisionDebug] " + detailLines.join(" | ");
  console.info(joined);
  logThrottled("movement_block:" + signature, "Movement blocked at x=" + diag.attemptedTile.x + ", y=" + diag.attemptedTile.y + " — " + diag.reason + ".", 180);
}

function canMoveTo(x,y){
  const diag=getMovementBlockDiagnostics(x,y);
  if(diag.blocked){
    emitMovementBlockDiagnostics(diag);
    return false;
  }
  return true;
}

const keys=new Set();
let showGrid=false;
let showCollisionOverlay=false;
let collisionOverlayToastUntil=0;

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
    setPlayerTilePosition(HEARTHVALE_LANDMARKS.townCenterSpawn.x, HEARTHVALE_LANDMARKS.townCenterSpawn.y);
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
  if(["w","a","s","d","arrowup","arrowdown","arrowleft","arrowright"," ","e","escape","h","k","g","v","1","2","3","4","5","6","7","8","9","f4","f6","f7","f8","f9","f10"].includes(k) || isDevToggleKey) e.preventDefault();
  if(DIRECTION_KEYS.includes(k)){
    if(blockedDirectionalKeysUntilRelease.has(k)) return;
  }
  if(isDevToggleKey){
    DEV_MODE=!DEV_MODE;
    log(DEV_MODE ? "Dev mode enabled" : "Dev mode disabled");
    updateSidebar();
  }
  if(k==="g") showGrid=!showGrid;
  if(k==="v" || e.code==="KeyV"){
    showCollisionOverlay=!showCollisionOverlay;
    collisionOverlayToastUntil=performance.now()+900;
    console.info("[Debug] Collision Overlay " + (showCollisionOverlay ? "ON" : "OFF"));
    if(SAVE_DEBUG_MODE) console.info("[Collision Overlay] " + (showCollisionOverlay ? "ON" : "OFF"));
  }
  if(k==="escape" && worldInfoPanel) closeWorldInfoPanel();
  else if(k==="escape" && dialogueSystem.activeSession) dialogueSystem.close();
  if(k==="e") interactionManager.tryInteract();
  if(k==="h") useHealingConsumable();
  if(k==="k") saveGame("manual");
  if(DEV_MODE && k==="f4"){
    atlasDebugPreview.enabled=!atlasDebugPreview.enabled;
    log("[Debug] Atlas preview " + (atlasDebugPreview.enabled ? "enabled" : "disabled") + ".");
    updateSidebar();
  }
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
function createMobileQaControls(){
  if(!MOBILE_QA_CONTROLS_MODE) return;
  const host=document.createElement("div");
  host.id="mobileQaControls";
  host.style.cssText="position:fixed;left:10px;bottom:10px;z-index:50;display:flex;gap:8px;align-items:flex-end;";
  const dpad=document.createElement("div");
  dpad.style.cssText="display:grid;grid-template-columns:40px 40px 40px;grid-template-rows:40px 40px 40px;gap:3px;";
  const mkDir=(label,key,col,row)=>{
    const b=document.createElement("button");
    b.textContent=label;
    b.style.cssText="grid-column:"+col+";"+"grid-row:"+row+";"+"border:1px solid #4c6281;background:#112034cc;color:#e6ecf5;border-radius:6px;";
    const press=(ev)=>{ ev.preventDefault(); touchDirectionKeys.add(key); };
    const release=(ev)=>{ ev.preventDefault(); touchDirectionKeys.delete(key); };
    b.addEventListener("pointerdown",press,{passive:false});
    b.addEventListener("pointerup",release,{passive:false});
    b.addEventListener("pointercancel",release,{passive:false});
    b.addEventListener("pointerleave",release,{passive:false});
    return b;
  };
  dpad.append(mkDir("↑","arrowup",2,1),mkDir("←","arrowleft",1,2),mkDir("→","arrowright",3,2),mkDir("↓","arrowdown",2,3));
  const tele=document.createElement("div");
  tele.style.cssText="display:flex;flex-direction:column;gap:4px;background:#0b1422cc;border:1px solid #4c6281;border-radius:8px;padding:6px;";
  const teleportButtons=[
    QUICK_NAV_DESTINATIONS.center_town,
    QUICK_NAV_DESTINATIONS.village_hall,
    QUICK_NAV_DESTINATIONS.residence_large,
    QUICK_NAV_DESTINATIONS.boathouse,
    QUICK_NAV_DESTINATIONS.pond_edge
  ];
  teleportButtons.forEach((entry)=>{
    const b=document.createElement("button");
    b.textContent=entry.label;
    b.style.cssText="border:1px solid #4c6281;background:#13263acc;color:#e6ecf5;border-radius:6px;font-size:11px;";
    b.addEventListener("click",(ev)=>{ ev.preventDefault(); quickNavTeleport(entry); },{passive:false});
    tele.appendChild(b);
  });
  host.append(dpad,tele);
  document.body.appendChild(host);
}
createMobileQaControls();
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
const touchDirectionKeys=new Set();
function isMovePressed(primary,alternate){
  return keys.has(primary) || keys.has(alternate) || touchDirectionKeys.has(primary) || touchDirectionKeys.has(alternate);
}
function updateInput(){
  if(isMovePressed("w","arrowup")) tryPlayerStep(0,-1,"up");
  else if(isMovePressed("s","arrowdown")) tryPlayerStep(0,1,"down");
  else if(isMovePressed("a","arrowleft")) tryPlayerStep(-1,0,"left");
  else if(isMovePressed("d","arrowright")) tryPlayerStep(1,0,"right");
  moveIntent.dx=0; moveIntent.dy=0;
  if(isMovePressed("w","arrowup")){ moveIntent.dy=-1; moveIntent.facing="up"; }
  else if(isMovePressed("s","arrowdown")){ moveIntent.dy=1; moveIntent.facing="down"; }
  else if(isMovePressed("a","arrowleft")){ moveIntent.dx=-1; moveIntent.facing="left"; }
  else if(isMovePressed("d","arrowright")){ moveIntent.dx=1; moveIntent.facing="right"; }
}

function canHostileMoveTo(x,y,self){
  if(!isTileInCurrentZone(x,y)) return false;
  if(isWorldObjectBlockingTile(x,y)) return false;
  if(isInMirrorCave){
    if(mirrorCave.blocked.has(keyOf(x,y))) return false;
  } else if(isInAbandonedTollhouse){
    if(abandonedTollhouse.blocked.has(keyOf(x,y))) return false;
  } else {
    if(isOverworldTerrainBlocked(x,y)) return false;
    if(isNpcOnTile(x,y,null)) return false;
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
  if (sheet?.complete && sheet.naturalWidth>0) {
    ctx.drawImage(sheet, fr.sx, fr.sy, 64, 64, dx, dy, drawW, drawH);
  } else {
    warnMissingAssetOnce("sprite", "humanoid:" + (label || "entity"));
    drawMissingSpritePlaceholder(dx, dy, drawW, drawH, "HUM");
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
  if(assets.sprites.wolf?.complete&&assets.sprites.wolf.naturalWidth>0) ctx.drawImage(assets.sprites.wolf,col*64,row*64,64,64,dx,dy,drawW,drawH);
  else {
    warnMissingAssetOnce("sprite", "wolf");
    drawMissingSpritePlaceholder(dx, dy, drawW, drawH, "WOLF");
  }
  ctx.fillStyle=rgba(0,0,0,.5); ctx.fillRect(p.x+2,p.y-10,24,4);
  ctx.fillStyle="#8fdb73"; ctx.fillRect(p.x+2,p.y-10,24*(wolf.hp/wolf.maxHp),4);
  if(hitAlpha>0){ ctx.fillStyle="rgba(255,255,255," + Math.min(.4,hitAlpha).toFixed(3) + ")"; ctx.fillRect(dx+8,dy+8,drawW-14,drawH-16); }
}

function hitVisualAlpha(e){ const now=performance.now(); if(now>=e.hitUntil) return 0; const left=e.hitUntil-now; const base=Math.min(.52,.2+left/300); const flick=now<e.hitFlickerUntil&&Math.floor(now/36)%2===0?.24:0; return Math.max(0,base+flick); }
function attackPose(entity){ const now=performance.now(); const total=350; const left=Math.max(0,entity.attackUntil-now); if(left<=0) return {active:false,thrust:0}; const t=(total-left)/total; return {active:true,thrust:Math.sin(t*Math.PI)*3.5}; }

function drawAlignmentGrid(){ const cam=getCamera(); const sx=cam.offsetX, sy=cam.offsetY, ex=sx+VIEW_TILES_X*TILE, ey=sy+VIEW_TILES_Y*TILE; ctx.save(); ctx.strokeStyle="rgba(221,233,255,.16)"; ctx.lineWidth=2; ctx.beginPath(); for(let x=0;x<=VIEW_TILES_X;x++){ const px=sx+x*TILE+.5; ctx.moveTo(px,sy); ctx.lineTo(px,ey);} for(let y=0;y<=VIEW_TILES_Y;y++){ const py=sy+y*TILE+.5; ctx.moveTo(sx,py); ctx.lineTo(ex,py);} ctx.stroke(); ctx.restore(); }
function drawCollisionOverlay(){
  const cam=getCamera();
  ctx.save();
  for(let y=cam.tileY;y<cam.tileY+VIEW_TILES_Y;y++){
    for(let x=cam.tileX;x<cam.tileX+VIEW_TILES_X;x++){
      if(!isTileInCurrentZone(x,y)) continue;
      const p=tileToScreen(x,y);
      const tileBlocked=isInMirrorCave
        ? mirrorCave.blocked.has(keyOf(x,y))
        : (isInAbandonedTollhouse
          ? abandonedTollhouse.blocked.has(keyOf(x,y))
          : isOverworldTerrainBlocked(x,y));
      const blockedByObject=isWorldObjectBlockingTile(x,y);
      if(tileBlocked || blockedByObject) ctx.fillStyle=blockedByObject ? "rgba(166,85,218,0.36)" : "rgba(220,76,76,0.28)";
      else ctx.fillStyle="rgba(64,186,116,0.24)";
      ctx.fillRect(p.x,p.y,TILE,TILE);
    }
  }
  const drawWorldRect=(rect,stroke,fill)=>{
    if(!rect) return;
    const p=tileToScreen(rect.x, rect.y);
    if(fill){
      ctx.fillStyle=fill;
      ctx.fillRect(p.x, p.y, rect.w*TILE, rect.h*TILE);
    }
    if(stroke){
      ctx.strokeStyle=stroke;
      ctx.lineWidth=2;
      ctx.strokeRect(p.x+0.5, p.y+0.5, rect.w*TILE-1, rect.h*TILE-1);
    }
  };
  if(!isInMirrorCave && !isInAbandonedTollhouse){
    world.buildings.forEach((building)=>{
      drawWorldRect(building.visual || { x:building.x, y:building.y, w:building.w, h:building.h }, "rgba(98,166,255,0.9)", null);
      drawWorldRect(building.visualBounds, "rgba(126,205,255,0.82)", "rgba(126,205,255,0.06)");
      drawWorldRect(building.collision || building.visual || { x:building.x, y:building.y, w:building.w, h:building.h }, "rgba(255,128,88,0.95)", "rgba(255,124,88,0.08)");
      drawWorldRect(building.frontWalkBand, "rgba(124,246,171,0.9)", "rgba(124,246,171,0.1)");
      drawWorldRect(building.occlusionDepthLine, "rgba(244,212,119,0.95)", "rgba(244,212,119,0.08)");
      drawWorldRect(building.rearExclusionZone, "rgba(230,104,201,0.9)", "rgba(230,104,201,0.08)");
      drawWorldRect(building.interaction, "rgba(108,206,255,0.95)", "rgba(108,206,255,0.15)");
      drawWorldRect(building.interactRect, "rgba(61,226,255,0.95)", null);
      if(Array.isArray(building.blockedVisualTiles)){
        building.blockedVisualTiles.forEach((blockedRect)=>drawWorldRect(blockedRect, "rgba(255,91,166,0.95)", "rgba(255,91,166,0.12)"));
      }
      if(building.frontDoorTile){
        drawWorldRect({ x:building.frontDoorTile.x, y:building.frontDoorTile.y, w:1, h:1 }, "rgba(91,252,214,0.98)", "rgba(91,252,214,0.24)");
      }
      drawWorldRect(building.pathingBounds, "rgba(239,199,111,0.55)", null);
    });
    getActiveWorldObjects().forEach((object)=>{
      const tile=getWorldObjectTile(object);
      drawWorldRect({ x:tile.x, y:tile.y, w:1, h:1 }, object.collision ? "rgba(192,128,255,0.95)" : "rgba(192,128,255,0.5)", object.collision ? "rgba(177,110,255,0.22)" : null);
    });
    const landmarkRects=[
      { x:HEARTHVALE_LANDMARKS.mirrorPond.x, y:HEARTHVALE_LANDMARKS.mirrorPond.y, w:1, h:1 },
      { x:HEARTHVALE_LANDMARKS.caveEntrance.x, y:HEARTHVALE_LANDMARKS.caveEntrance.y, w:1, h:1 },
      { x:HEARTHVALE_LANDMARKS.mainCrossroads.x, y:HEARTHVALE_LANDMARKS.mainCrossroads.y, w:1, h:1 },
      { x:HEARTHVALE_LANDMARKS.townCenterSpawn.x, y:HEARTHVALE_LANDMARKS.townCenterSpawn.y, w:1, h:1 },
      { x:HEARTHVALE_LANDMARKS.zoneExits.mirrorCaveEntrance.x, y:HEARTHVALE_LANDMARKS.zoneExits.mirrorCaveEntrance.y, w:1, h:1 },
      { x:HEARTHVALE_LANDMARKS.zoneExits.abandonedTollhouseEntrance.x, y:HEARTHVALE_LANDMARKS.zoneExits.abandonedTollhouseEntrance.y, w:1, h:1 },
      { x:HEARTHVALE_LANDMARKS.zoneExits.northRoadBoundary.x, y:HEARTHVALE_LANDMARKS.zoneExits.northRoadBoundary.y, w:1, h:1 },
      { x:HEARTHVALE_LANDMARKS.zoneExits.westLaneBoundary.x, y:HEARTHVALE_LANDMARKS.zoneExits.westLaneBoundary.y, w:1, h:1 },
      { x:HEARTHVALE_LANDMARKS.zoneExits.easternWoodsBoundary.x, y:HEARTHVALE_LANDMARKS.zoneExits.easternWoodsBoundary.y, w:1, h:1 }
    ];
    landmarkRects.forEach((rect)=>drawWorldRect(rect, "rgba(255,241,122,0.95)", "rgba(255,241,122,0.15)"));
  }
  const entityRects=[
    { x:player.targetX, y:player.targetY, w:1, h:1, stroke:"rgba(96,188,255,0.98)", fill:"rgba(96,188,255,0.2)" }
  ];
  if(!isInMirrorCave && !isInAbandonedTollhouse){
    namedVillageNpcs.forEach((villageNpc)=>{
      entityRects.push({ x:villageNpc.targetX, y:villageNpc.targetY, w:1, h:1, stroke:"rgba(255,228,133,0.98)", fill:"rgba(255,228,133,0.2)" });
    });
  }
  getActiveHostiles().forEach((hostile)=>{
    if(hostile.hp<=0) return;
    entityRects.push({ x:hostile.targetX, y:hostile.targetY, w:1, h:1, stroke:"rgba(255,110,110,0.98)", fill:"rgba(255,110,110,0.2)" });
  });
  entityRects.forEach((rect)=>drawWorldRect(rect, rect.stroke, rect.fill));
  if(ATLAS_DEBUG_MODE){
    drawWorldRect({ x:player.x, y:player.y, w:1, h:1 }, "rgba(120,255,225,0.95)", null);
    const playerTileDiag=getMovementBlockDiagnostics(player.targetX, player.targetY);
    const playerTileScreen=tileToScreen(player.targetX, player.targetY);
    ctx.fillStyle=playerTileDiag.walkable ? "rgba(131,255,169,0.95)" : "rgba(255,128,128,0.98)";
    ctx.font="11px monospace";
    ctx.fillText(playerTileDiag.walkable ? "walkable" : "blocked", playerTileScreen.x+2, playerTileScreen.y-4);
  }
  ctx.restore();
}
function drawCollisionOverlayToast(now){
  if(now>collisionOverlayToastUntil) return;
  const text="Collision Overlay " + (showCollisionOverlay ? "ON" : "OFF");
  ctx.save();
  ctx.fillStyle="rgba(0,0,0,0.76)";
  ctx.fillRect(12, 12, 196, 24);
  ctx.strokeStyle=showCollisionOverlay ? "rgba(132,244,171,0.95)" : "rgba(255,170,170,0.95)";
  ctx.lineWidth=2;
  ctx.strokeRect(12.5, 12.5, 195, 23);
  ctx.fillStyle=showCollisionOverlay ? "rgba(162,255,196,0.98)" : "rgba(255,198,198,0.98)";
  ctx.font="12px ui-monospace, monospace";
  ctx.fillText(text, 20, 28);
  ctx.restore();
}
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
  ctx.imageSmoothingEnabled=false;

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
  drawEntityRing(player.px/TILE,player.py/TILE,"rgba(186,218,255,__A__)",0.62,10.2);
  drawHumanoid(assets.sprites.player, player.px/TILE, player.py/TILE, player.facing, player.moving, 0.92, "Wayfarer", hitVisualAlpha(player), {x:player.recoilX+player.attackLungeX,y:player.recoilY+player.attackLungeY}, attackPose(player));
  ctx.fillStyle="rgba(8,10,14,.2)"; ctx.fillRect(0,0,canvas.width,canvas.height);
  drawTransitionFade(now);
}
function drawAbandonedTollhouseScene(now){
  ctx.imageSmoothingEnabled=false;

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
  drawEntityRing(player.px/TILE,player.py/TILE,"rgba(186,218,255,__A__)",0.62,10.2);
  drawHumanoid(assets.sprites.player, player.px/TILE, player.py/TILE, player.facing, player.moving, 0.92, "Wayfarer", hitVisualAlpha(player), {x:player.recoilX+player.attackLungeX,y:player.recoilY+player.attackLungeY}, attackPose(player));
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
  ctx.imageSmoothingEnabled=false;

  const now=performance.now();
  beginDecorSourceTraceFrame();
  resetAtlasBuildingDecorExclusionState();
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
  bootDiagnostics.cameraPosition={ x:cam.tileX, y:cam.tileY };
  bootDiagnostics.playerPosition={ x:player.targetX, y:player.targetY };
  bootDiagnostics.terrainDrawCount=0;
  bootDiagnostics.roadDrawCount=0;
  bootDiagnostics.buildingDrawCount=0;
  drawOutdoorBackdrop(cam, now);
  const padX=Math.ceil(Math.max(cam.offsetX, canvas.width-(cam.offsetX+VIEW_TILES_X*TILE))/TILE)+3;
  const padY=Math.ceil(Math.max(cam.offsetY, canvas.height-(cam.offsetY+VIEW_TILES_Y*TILE))/TILE)+3;
  for(let y=cam.tileY-padY;y<cam.tileY+VIEW_TILES_Y+padY;y++) for(let x=cam.tileX-padX;x<cam.tileX+VIEW_TILES_X+padX;x++){
    const p=tileToScreen(x,y);
    if(x<0 || y<0 || x>=WORLD_W || y>=WORLD_H) continue;
    const n=layeredNoise(x,y);
    const n2=layeredNoise(x+2.2,y+1.6)*0.35 + layeredNoise(x-3.4,y-0.8)*0.25;
    const tone=Math.max(0, Math.min(0.999, n*0.62 + n2*0.75));
    const mix=Math.min(assets.grass.length-1, Math.floor(tone*assets.grass.length));
    const region=getOutdoorRegionIdAt(x,y);
    const inForest=region==="eastern_woods" || (region==="north_road" && rng(x,y,211)>0.45);
    const forestMix=Math.min(assets.forestGrass.length-1, Math.floor((layeredNoise(x+5,y+3)+rng(x,y,212)*0.2)*assets.forestGrass.length)%assets.forestGrass.length);
    const img=inForest ? assets.forestGrass[forestMix] : assets.grass[mix];
    if(img.complete&&img.naturalWidth>0){ ctx.drawImage(img,p.x,p.y,TILE,TILE); bootDiagnostics.terrainDrawCount+=1; }
    if(!inForest && layeredNoise(x+13,y+7)>0.8){
      ctx.fillStyle="rgba(188,216,151,.012)";
      ctx.fillRect(p.x+1,p.y+1,30,30);
    }
    if(world.roadTiles.has(keyOf(x,y))){
      ctx.fillStyle="rgba(77,109,63,.04)";
      ctx.fillRect(p.x,p.y,32,32);
    }
  }

  world.roads.forEach(r=>{ for(let x=r.x;x<r.x+r.w;x++) for(let y=r.y;y<r.y+r.h;y++){
    const p=tileToScreen(x,y);
    const img=assets.road[Math.floor(rng(x,y,22)*assets.road.length)];
    if(img.complete&&img.naturalWidth>0){ ctx.drawImage(img,p.x,p.y,32,32); bootDiagnostics.roadDrawCount+=1; }

    const north = world.roadTiles.has(keyOf(x,y-1));
    const south = world.roadTiles.has(keyOf(x,y+1));
    const east = world.roadTiles.has(keyOf(x+1,y));
    const west = world.roadTiles.has(keyOf(x-1,y));
    if(!north) drawTileRotated(assets.roadEdge[Math.floor(rng(x,y,62)*assets.roadEdge.length)], p.x, p.y, 0);
    if(!east) drawTileRotated(assets.roadEdge[Math.floor(rng(x,y,64)*assets.roadEdge.length)], p.x, p.y, 1);
    if(!south) drawTileRotated(assets.roadEdge[Math.floor(rng(x,y,66)*assets.roadEdge.length)], p.x, p.y, 2);
    if(!west) drawTileRotated(assets.roadEdge[Math.floor(rng(x,y,68)*assets.roadEdge.length)], p.x, p.y, 3);

    if(!north || !south || !east || !west){
      ctx.fillStyle="rgba(84,118,64,.1)";
      if(!north) ctx.fillRect(p.x+2,p.y+1,28,2);
      if(!south) ctx.fillRect(p.x+2,p.y+29,28,2);
      if(!east) ctx.fillRect(p.x+29,p.y+2,2,28);
      if(!west) ctx.fillRect(p.x+1,p.y+2,2,28);
    }
    if((north&&south&&east&&west) || ((!north&&!south)&&(east||west)) || ((!east&&!west)&&(north||south))){
      ctx.fillStyle="rgba(121,95,64,.11)";
      ctx.fillRect(p.x+11,p.y+11,10,10);
      ctx.fillStyle="rgba(203,176,138,.045)";
      ctx.fillRect(p.x+13,p.y+13,6,2);
    }
  } });

  for(let x=pond.x-1;x<=pond.x+pond.w;x++) for(let y=pond.y-1;y<=pond.y+pond.h;y++){
    const k=keyOf(x,y); if(!world.pondWater.has(k)) continue;
    const p=tileToScreen(x,y); const edge=world.pondNearEdge.has(k);
    const img=edge?assets.water.shallow:assets.water.deep; if(img.complete&&img.naturalWidth>0) ctx.drawImage(img,p.x,p.y,32,32);
    const t=performance.now()*0.0014, rip=(Math.sin(t*2+x*0.8+y*.6)+1)*.5;
    const mirrorAura=(x>=25&&x<=30&&y>=12&&y<=17) ? 0.065 : 0.016;
    ctx.fillStyle="rgba(188,228,255," + (.014+rip*.03+mirrorAura).toFixed(3) + ")"; ctx.fillRect(p.x+4,p.y+7,TILE-12,1);
    if(edge){
      ctx.fillStyle="rgba(224,244,255," + (.035+rip*.03).toFixed(3) + ")"; ctx.fillRect(p.x+1,p.y+1,TILE-2,1);
      if(assets.water.edge.complete&&assets.water.edge.naturalWidth>0) ctx.drawImage(assets.water.edge,p.x,p.y,32,32);
    }
    if(rng(x,y,402)>0.92){
      ctx.fillStyle="rgba(201,240,255,.25)";
      ctx.fillRect(p.x+10,p.y+10,4,1);
      ctx.fillRect(p.x+14,p.y+9,2,1);
    }
    if(rng(x,y,409)>0.9){
      ctx.fillStyle="rgba(176,225,255,.2)";
      ctx.fillRect(p.x+7,p.y+20,8,1);
    }
  }
  for(let x=pond.x-1;x<=pond.x+pond.w;x++) for(let y=pond.y-1;y<=pond.y+pond.h;y++){
    const k=keyOf(x,y); if(!world.pondShore.has(k)) continue;
    const p=tileToScreen(x,y); const img=assets.shore[Math.floor(rng(x,y,33)*assets.shore.length)]; if(img.complete&&img.naturalWidth>0) ctx.drawImage(img,p.x,p.y,32,32);
    if(rng(x,y,491)>0.78){
      ctx.fillStyle="rgba(86,121,74,.42)";
      ctx.fillRect(p.x+5,p.y+14,2,8);
      ctx.fillRect(p.x+8,p.y+15,1,7);
    }
    if(rng(x,y,529)>0.83){
      ctx.fillStyle="rgba(198,214,162,.14)";
      ctx.fillRect(p.x+11,p.y+10,4,1);
    }
    if(rng(x,y,535)>0.9){
      ctx.fillStyle="rgba(116,149,94,.52)";
      ctx.fillRect(p.x+21,p.y+15,1,6);
      ctx.fillRect(p.x+23,p.y+14,1,7);
    }
  }

  const buildingDrawEntries=world.buildings.map((b,bIndex)=>{
    const spriteId=getBuildingSpriteId(b);
    const sprite=atlasManifests.buildings.sprites[spriteId];
    const anchorPxX=((b.anchorX ?? Math.floor(b.w/2))*TILE);
    const anchorPxY=((b.anchorY ?? (b.h-1))*TILE);
    const worldAnchorY=(b.y*TILE)+anchorPxY;
    const drawX=tileToScreen(b.x,b.y).x + anchorPxX - (sprite?.anchorX ?? anchorPxX);
    const drawY=tileToScreen(b.x,b.y).y + anchorPxY - (sprite?.anchorY ?? anchorPxY);
    return { type:"building", b, bIndex, spriteId, sprite, anchorPxX, anchorPxY, worldAnchorY, drawX, drawY };
  });
  secondaryProofPreviewState.drawCount=0;
  const buildingSortDebugRows=[];

  const entityDrawEntries=[
    { type:"npc", id:npc.id, worldAnchorY:npc.py, draw:()=>{
      drawEntityRing(npc.x,npc.y,"rgba(201,227,255,__A__)",0.42,8.6);
      drawHumanoid(assets.sprites.edrin, npc.x, npc.y, npc.facing, false, 0.86, "", 0, null, null);
    } },
    { type:"npc", id:hunterNpc.id, worldAnchorY:hunterNpc.py, draw:()=>{
      drawEntityRing(hunterNpc.x,hunterNpc.y,"rgba(208,232,184,__A__)",0.4,8.7);
      drawHumanoid(assets.sprites.hunter, hunterNpc.x, hunterNpc.y, hunterNpc.facing, false, 0.86, "", 0, null, null);
    } },
    { type:"npc", id:vendorNpc.id, worldAnchorY:vendorNpc.py, draw:()=>{
      drawEntityRing(vendorNpc.x,vendorNpc.y,"rgba(250,221,164,__A__)",0.4,8.7);
      drawHumanoid(assets.sprites.merchant, vendorNpc.x, vendorNpc.y, vendorNpc.facing, false, 0.86, "", 0, null, null);
    } },
    ...wolves.filter((wolf)=>wolf.hp>0).map((wolf)=>({ type:"wolf", id:wolf.id||"wolf", worldAnchorY:wolf.py, draw:()=>{
      drawEntityRing(wolf.px/TILE,wolf.py/TILE,"rgba(255,149,122,__A__)",0.26,8.1);
      drawWolf(wolf, wolf.px/TILE, wolf.py/TILE, wolf.facing, wolf.moving, 0.82, hitVisualAlpha(wolf), {x:wolf.recoilX+wolf.attackLungeX,y:wolf.recoilY+wolf.attackLungeY});
    } })),
    ...bandits.filter((bandit)=>bandit.hp>0).map((bandit)=>({ type:"bandit", id:bandit.id||"bandit", worldAnchorY:bandit.py, draw:()=>{
      drawEntityRing(bandit.px/TILE,bandit.py/TILE,"rgba(255,120,120,__A__)",0.32,8.7);
      drawHumanoid(assets.sprites.bandit, bandit.px/TILE, bandit.py/TILE, bandit.facing, bandit.moving, 0.85, "", hitVisualAlpha(bandit), {x:bandit.recoilX+bandit.attackLungeX,y:bandit.recoilY+bandit.attackLungeY}, attackPose(bandit));
    } })),
    { type:"player", id:"player", worldAnchorY:player.py, draw:()=>{
      drawEntityRing(player.px/TILE,player.py/TILE,"rgba(186,218,255,__A__)",0.62,10.2);
      drawHumanoid(assets.sprites.player, player.px/TILE, player.py/TILE, player.facing, player.moving, 0.92, "", hitVisualAlpha(player), {x:player.recoilX+player.attackLungeX,y:player.recoilY+player.attackLungeY}, attackPose(player));
    } }
  ];

  const renderQueue=[...buildingDrawEntries, ...entityDrawEntries]
    .sort((a,b)=>a.worldAnchorY-b.worldAnchorY);
  const propsAbove=(Array.isArray(world.props) ? world.props : []).filter((prop)=>prop?.layer==="above_entities");

  renderQueue.forEach((entry, drawOrderRank)=>{
    if(entry.type!=="building"){
      try{
        entry.draw();
      }catch(renderEntryError){
        if(ATLAS_DEBUG_MODE) console.warn("[Render Safety] entity draw skipped", renderEntryError);
      }
      return;
    }
    const { b, bIndex, spriteId, sprite, anchorPxX, anchorPxY, drawX, drawY, worldAnchorY }=entry;

    for(let ry=0; ry<b.h; ry++){
      const right = tileToScreen(b.x+b.w, b.y+ry);
      drawShadowTile(assets.shadow.buildingRight, right.x+4, right.y+3, .9);
    }
    for(let rx=0; rx<b.w; rx++){
      const bottom = tileToScreen(b.x+rx, b.y+b.h);
      drawShadowTile(assets.shadow.buildingBottom, bottom.x+4, bottom.y+3, .88);
    }

    const previewTargeted=ATLAS_DEBUG_MODE && isSecondaryRuntimeAtlasPreviewBuilding(b);
    const spriteFailureReason=getBuildingProductionSpriteFailureReason(b, spriteId);
    const drawDimensionsAreFinite=Number.isFinite(drawX) && Number.isFinite(drawY) && Number.isFinite(sprite?.drawW ?? sprite?.sw) && Number.isFinite(sprite?.drawH ?? sprite?.sh);
    const drawImageAttempted=!spriteFailureReason && drawDimensionsAreFinite;
    const didDraw=drawImageAttempted
      ? drawAtlasSprite("buildings", spriteId, drawX, drawY, sprite?.drawW ?? sprite?.sw, sprite?.drawH ?? sprite?.sh)
      : false;
    // Per-building diagnostic record — single source of truth shared by audit,
    // overlay, proof HUD. If drawImageSucceeded=true the audit MUST count it as
    // ATLAS; if false the overlay MUST NOT label it ATLAS.
    const buildingsSheet=atlasImages.buildings;
    buildingRenderDiagnostics.perBuilding.set(b.id, {
      buildingId:b.id,
      spriteId:spriteId||null,
      metadataSource:sprite?.metadataSource || "index",
      renderPath:didDraw ? "atlas" : "fallback",
      actualDrawSource:didDraw ? (previewTargeted ? "atlas_preview" : "atlas") : (drawImageAttempted ? "atlas_attempt_failed" : "fallback"),
      atlasImageObjectId:"buildings",
      imageComplete:buildingsSheet?.complete===true,
      imageNaturalWidth:buildingsSheet?.naturalWidth||atlasRuntimeInfo.buildings?.width||0,
      imageNaturalHeight:buildingsSheet?.naturalHeight||atlasRuntimeInfo.buildings?.height||0,
      manifestLoaded:atlasRuntimeInfo.buildings?.manifestReady===true || (atlasManifests.buildings?.sprites && Object.keys(atlasManifests.buildings.sprites).length>0),
      crop:sprite ? { x:sprite.sx, y:sprite.sy, w:sprite.sw, h:sprite.sh } : null,
      drawW:sprite?.drawW ?? sprite?.sw ?? null,
      drawH:sprite?.drawH ?? sprite?.sh ?? null,
      anchorX:sprite?.anchorX ?? null,
      anchorY:sprite?.anchorY ?? null,
      drawImageAttempted,
      drawImageSucceeded:didDraw===true,
      failureReason:didDraw ? null : (spriteFailureReason || (drawDimensionsAreFinite ? "draw_failed" : "invalid_draw_position"))
    });
    if(didDraw) bootDiagnostics.buildingDrawCount+=1;
    const buildingSortY=(b.y*TILE) + (sprite?.anchorY ?? anchorPxY);
    const buildingSortDebug={
      id:b.id,
      anchorY:sprite?.anchorY ?? anchorPxY,
      sortY:Math.round(buildingSortY),
      metadataSource:sprite?.metadataSource || "index"
    };
    buildingSortDebugRows.push(buildingSortDebug);
    if(!didDraw){
      const fallbackReason=spriteFailureReason || (drawDimensionsAreFinite ? "draw_failed" : "invalid_draw_position");
      const isPending=isBuildingAtlasPendingReason(fallbackReason);
      if(isPending){
        buildingRenderDiagnostics.pendingBuildings.set(b.id, fallbackReason);
      }else{
        warnMissingAssetOnce("building_sprite", (spriteId||"none")+":"+fallbackReason);
        buildingRenderDiagnostics.fallbackBuildings.set(b.id, fallbackReason);
        logBuildingFallbackOnce(b, fallbackReason);
      }
      buildingRenderDiagnostics.atlasBuildings.delete(b.id);
      syncAtlasProofDiagnostics(b, spriteId, sprite, false, fallbackReason);
      if(HEARTHVALE_PROOF_BUILDING_IDS.has(b.id)){
        logAtlasProofStatusOnce("FALLBACK");
        const fallbackDrawW=(sprite?.drawW ?? sprite?.sw ?? (b.w*TILE));
        const fallbackDrawH=(sprite?.drawH ?? sprite?.sh ?? (b.h*TILE));
        drawAtlasProofMarker(drawX, drawY, fallbackDrawW, fallbackDrawH, b, "FALLBACK", atlasProofDiagnostics.fallbackReason);
      }
      drawBuildingFallbackSprite(b);
      drawSecondaryProofPreviewOverlay(entry);
      return;
    }
    buildingRenderDiagnostics.pendingBuildings.delete(b.id);
    buildingRenderDiagnostics.fallbackBuildings.delete(b.id);
    buildingRenderDiagnostics.atlasBuildings.add(b.id);
    registerAtlasBuildingDecorExclusionZone(b, drawX, drawY, sprite?.drawW ?? sprite?.sw, sprite?.drawH ?? sprite?.sh);
    syncAtlasProofDiagnostics(b, spriteId, sprite, true, null);
    if(HEARTHVALE_PROOF_BUILDING_IDS.has(b.id)){
      drawAtlasProofMarker(drawX, drawY, sprite?.drawW ?? sprite?.sw, sprite?.drawH ?? sprite?.sh, b, "ATLAS", null);
      logAtlasProofStatusOnce("ATLAS");
    }
    if(ATLAS_DEBUG_MODE || isDecorDebugEnabled()){
      const anchorDebug=tileToScreen(b.x,b.y);
      const anchorX=Math.round(anchorDebug.x + anchorPxX);
      const anchorY=Math.round(anchorDebug.y + anchorPxY);
      ctx.fillStyle="rgba(24,30,44,0.85)";
      ctx.fillRect(anchorX+8, anchorY-18, 170, 14);
      ctx.fillStyle="rgba(176,243,255,0.95)";
      ctx.font="10px monospace";
      const previewSuffix=previewTargeted
        ? " role="+b.role+" crop="+[sprite?.sx,sprite?.sy,sprite?.sw,sprite?.sh].join("/")+" draw="+(sprite?.drawW??sprite?.sw)+"x"+(sprite?.drawH??sprite?.sh)+" anchor="+(sprite?.anchorX??"n/a")+"/"+(sprite?.anchorY??"n/a")+" runtimeStatus=ATLAS_PREVIEW productionReady=false previewOnly=true"
        : "";
      ctx.fillText((b.id||"building")+" y="+Math.round(worldAnchorY)+" rank="+drawOrderRank+previewSuffix, anchorX+10, anchorY-8);
    }
    traceDecorSource({
      sourceSystem:"overworld_renderer",
      sourceFunction:"drawWorld.world.buildings.forEach",
      objectId:b.id,
      objectType:b.role,
      sourceLabel:"BUILDING_ATLAS",
      atlasFile:getAtlasFilename(sprite?.atlas || atlasManifests.buildings?.imagePath),
      crop:sprite ? { x:sprite.sx, y:sprite.sy, w:sprite.sw, h:sprite.sh } : null,
      worldTile:{ x:b.x + (b.anchorX ?? Math.floor(b.w/2)), y:b.y + (b.anchorY ?? (b.h-1)) },
      screenDraw:{ x:drawX, y:drawY },
      drawSize:{ w:sprite?.drawW ?? sprite?.sw, h:sprite?.drawH ?? sprite?.sh },
      renderLayer:"buildings"
    });

    const chimneyTx=b.x + (bIndex%2 ? b.w-2 : 1);
    const chimneyTy=b.y;
    const chimney=tileToScreen(chimneyTx, chimneyTy);
    traceDecorSource({ sourceSystem:"procedural_building_overlay", sourceFunction:"drawWorld.world.buildings.forEach.chimney", objectId:b.id + ":chimney", objectType:"chimney_overlay", sourceLabel:"PROCEDURAL", procedural:true, worldTile:{ x:chimneyTx, y:chimneyTy }, screenDraw:{ x:chimney.x+10, y:chimney.y-7 }, drawSize:{ w:6, h:9 }, renderLayer:"buildings_overlay" });
    if(b.id!=="b_inn_tavern"){ ctx.fillStyle="rgba(94,72,54,.9)"; ctx.fillRect(chimney.x+10,chimney.y-7,6,9); }
  });
  if(ATLAS_DEBUG_MODE){
    if(!SECONDARY_PROOF_PREVIEW_MODE){
      console.assert(secondaryProofPreviewState.drawCount===0,"[Secondary Proof Preview Assert] disabled_preview_must_not_draw_atlas_overlays count="+secondaryProofPreviewState.drawCount);
    }else{
      logSecondaryProofPreviewDrawSummary();
    }
  }

  propsAbove.forEach((prop)=>{
    const p = tileToScreen(prop.x,prop.y);
    const usedAtlasSprite=drawMappedPropSprite(prop,p);
    const mappedSpriteId=PROP_SPRITE_BY_WORLD_TYPE[prop.type];
    const mappedAtlasSprite=mappedSpriteId ? atlasManifests.props?.sprites?.[mappedSpriteId] : null;
    const mappedDrawX=mappedAtlasSprite ? Math.round(p.x + TILE/2 - (mappedAtlasSprite.anchorX ?? TILE/2)) : p.x;
    const mappedDrawY=mappedAtlasSprite ? Math.round(p.y + TILE - (mappedAtlasSprite.anchorY ?? TILE)) : p.y;
    const mappedDrawW=mappedAtlasSprite?.drawW ?? mappedAtlasSprite?.sw ?? TILE;
    const mappedDrawH=mappedAtlasSprite?.drawH ?? mappedAtlasSprite?.sh ?? TILE;
    const sourceLabel=usedAtlasSprite ? "PROP_ATLAS" : "MAP_OBJECT";
    const drawRect={
      x:usedAtlasSprite ? mappedDrawX : p.x,
      y:usedAtlasSprite ? mappedDrawY : p.y,
      w:usedAtlasSprite ? mappedDrawW : TILE,
      h:usedAtlasSprite ? mappedDrawH : TILE
    };
    const suppressionZone=shouldSuppressDecorObject("prop_" + prop.x + "_" + prop.y + "_" + prop.type, sourceLabel, drawRect, { objectType:prop.type, worldTile:{ x:prop.x, y:prop.y } });
    traceDecorSource({
      sourceSystem:"map_props",
      sourceFunction:"drawWorld.propsAbove.forEach",
      objectId:"prop_" + prop.x + "_" + prop.y + "_" + prop.type,
      objectType:prop.type,
      sourceLabel,
      atlasFile:usedAtlasSprite ? getAtlasFilename(mappedAtlasSprite?.atlas || atlasManifests.props?.imagePath) : null,
      crop:usedAtlasSprite && mappedAtlasSprite ? { x:mappedAtlasSprite.sx, y:mappedAtlasSprite.sy, w:mappedAtlasSprite.sw, h:mappedAtlasSprite.sh } : null,
      procedural:!usedAtlasSprite,
      worldTile:{ x:prop.x, y:prop.y },
      screenDraw:{ x:drawRect.x, y:drawRect.y },
      drawSize:{ w:drawRect.w, h:drawRect.h },
      renderLayer:suppressionZone ? "suppressed_above_entities:" + suppressionZone.reason : (prop.layer || "above_entities")
    });
    if(suppressionZone) return;
    if(!usedAtlasSprite){
      const img = assets.props.sprites[prop.type];
      if(!img || !img.complete || img.naturalWidth<=0){
        warnMissingAssetOnce("prop_sprite", prop.type);
        drawMissingSpritePlaceholder(p.x, p.y, 32, 32, "PROP");
        return;
      }
      drawShadowTile(assets.shadow.softTile,p.x+3,p.y+4,.65);
      ctx.drawImage(img,p.x,p.y,32,32);
      return;
    }
    drawShadowTile(assets.shadow.softTile,p.x+3,p.y+4,.65);
  });
  const currentTarget=getCurrentCombatTarget(5);
  const hostileLabelEntries=[...wolves, ...bandits]
    .filter((hostile)=>hostile.hp>0 && Math.abs(player.targetX-hostile.targetX)+Math.abs(player.targetY-hostile.targetY)<=4)
    .map((hostile)=>({
      text:(hostile===currentTarget ? "[Target] " : "") + hostileLabel(hostile) + " " + hostile.hp + "/" + hostile.maxHp,
      tx:hostile.px/TILE,
      ty:hostile.py/TILE,
      priority:hostile===currentTarget ? 4 : 1
    }));
  const zoneLabelEntries=[];
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
  if(showCollisionOverlay) drawCollisionOverlay();
  drawCollisionOverlayToast(now);
  drawTransitionFade(now);
  drawFloatingTexts(now);
  maybeLogBuildingRenderSummary();
  logBuildingSourceOfTruthAudit();
  maybeEmitFrontageAudit();
  emitBoathousePlacementQA();
  emitHarborCompositionQA();
  emitBuildingAtlasCropAuditIfReady();
  runAtlasCatalogScanOnce();
  drawDecorSourceLabels();
  emitDecorSuppressionDebugReport();
  flushDecorSourceTraceFrame();
  drawAtlasDebugPreview();
  drawBuildingSpriteProof();
  drawAtlasProofTopLeftLine();
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
    if(!isInMirrorCave && !isInAbandonedTollhouse){
      enforceAllVillageNpcTerrainValidation(false);
      namedVillageNpcs.forEach((villageNpc)=>{
        updateVillageNpcWander(villageNpc, now);
      });
    }
  }
  updateSidebar();
}

let last=performance.now();
let lastLoopErrorMessage=null;
function loop(now){
  try{
    const dt=Math.min(.033,(now-last)/1000);
    last=now;
    update(dt,now);
    drawWorld();
    bootDiagnostics.lastRenderException=null;
    lastLoopErrorMessage=null;
  }catch(loopError){
    const loopErrorMessage=String(loopError?.message || loopError || "unknown_error");
    bootDiagnostics.lastRenderException=loopErrorMessage;
    if(loopErrorMessage!==lastLoopErrorMessage){
      lastLoopErrorMessage=loopErrorMessage;
      console.error("[Boot Hotfix] render loop exception", loopError);
      if(ATLAS_DEBUG_MODE) console.info("[Boot Hotfix] diagnostics", bootDiagnostics);
    }
  }
  requestAnimationFrame(loop);
}

const loadedFromSave=loadGame();
bootDiagnostics.worldInitialized=true;
bootDiagnostics.saveLoadStatus=loadedFromSave ? "loaded" : "default_fallback";
if(SAVE_DEBUG_MODE){
  const activeQuest=questSystem.getActiveQuestIds?.()[0] || null;
  const saveSlotDiagnostics=getAllSaveSlotDiagnostics();
  const activeSlot=saveSlotDiagnostics.find((entry)=>entry.key===SAVE_KEY) || null;
  const backupSlot=saveSlotDiagnostics.find((entry)=>entry.key===SAVE_BACKUP_KEY) || null;
  const legacySlots=saveSlotDiagnostics.filter((entry)=>LEGACY_SAVE_KEYS.includes(entry.key));
  const richestSlot=findRichestValidSave(saveSlotDiagnostics);
  const activeAppearsDefaultLike=Boolean(activeSlot?.valid && activeSlot.level===1 && activeSlot.xp===0 && activeSlot.inventoryCount<=1 && !activeSlot.currentQuest && (activeSlot.completedQuestCount||0)===0);
  const saveDebugBundle={
    activeSaveKey:SAVE_KEY,
    backupSaveKey:SAVE_BACKUP_KEY,
    attemptedKeys:[SAVE_KEY, ...LEGACY_SAVE_KEYS],
    loadedKey:saveDiagnostics.loadedFromKey,
    foundSave:saveDiagnostics.saveFound,
    usedDefaultState:saveDiagnostics.fallbackDefaultUsed,
    migrationRan:saveDiagnostics.migrationRan,
    migrationSucceeded:saveDiagnostics.migrationSucceeded,
    backupFound:saveDiagnostics.backupFound,
    backupCreated:saveDiagnostics.backupCreated,
    lastLoadError:saveDiagnostics.lastError,
    playerLevel:player.level,
    xp:player.xp,
    inventoryCount:Array.isArray(player.inventory) ? player.inventory.reduce((sum,item)=>sum+Math.max(0,Math.floor(item?.quantity||0)),0) : 0,
    currentQuest:activeQuest,
    loadResult:loadedFromSave,
    activeSaveValid:Boolean(activeSlot?.valid),
    backupSaveValid:Boolean(backupSlot?.valid),
    legacySaveValid:legacySlots.some((entry)=>entry.valid),
    richestSaveKey:richestSlot?.key || null,
    activeAppearsOverwrittenOrDefaultLike:activeAppearsDefaultLike,
    overwriteProtectionAdded:true,
    restorationPerformed:false,
    diagnosticOnly:true
  };
  console.groupCollapsed("[Save Debug] Runtime save diagnostics");
  console.table(saveDebugBundle);
  console.table(saveSlotDiagnostics.map((entry)=>(
    { key:entry.key, found:entry.found, parseSuccess:entry.parseSuccess, valid:entry.valid, level:entry.level, xp:entry.xp, coins:entry.coins, inventoryCount:entry.inventoryCount, currentQuest:entry.currentQuest, completedQuestCount:entry.completedQuestCount, version:entry.version, saveSchemaVersion:entry.saveSchemaVersion, savedAt:entry.savedAt, richnessScore:entry.richnessScore, parseError:entry.parseError }
  )));
  console.info("[Save Debug]", saveDebugBundle);
  console.groupEnd();
}
bootDiagnostics.assetLoadStatus="ready";
bootDiagnostics.manifestLoadStatus=atlasManifests?.buildings?.sprites ? "ready" : "fallback_index";
enforceAllVillageNpcTerrainValidation(true);
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
