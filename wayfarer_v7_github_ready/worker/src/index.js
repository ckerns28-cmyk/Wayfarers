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
    #brand,#stats,#objective,#logPanel{padding:14px;}
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
      position:absolute;left:20px;right:20px;bottom:20px;display:none;
      background:linear-gradient(#121a25,#0b1018);
      border:1px solid #51637d;
      border-radius:10px;
      box-shadow:0 12px 34px rgba(0,0,0,.5), inset 0 0 0 1px rgba(255,255,255,.06);
      padding:12px 14px;
    }
    #dialogueName{font-weight:700;color:var(--accent);margin-bottom:8px;letter-spacing:.4px}
    #dialogueText{white-space:pre-line;min-height:62px;line-height:1.5}
    #dialogueHint{margin-top:8px;color:var(--muted);font-size:12px}
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
        <div id="dialogueHint">Click dialogue panel to continue.</div>
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
function keyOf(x,y){ return x + "," + y; }
function rng(x,y,s=1){ return (((x*73856093)^(y*19349663)^(s*83492791))>>>0)%1000/1000; }

function makeTile(drawFn){
  const c = document.createElement("canvas"); c.width = TILE; c.height = TILE;
  const p = c.getContext("2d"); p.imageSmoothingEnabled = false; drawFn(p);
  const img = new Image(); img.src = c.toDataURL("image/png"); return img;
}

const assets = {
  grass: [], road: [], water: {}, shore: [],
  tree: {}, propWell: null, fence: [],
  building: {}, sprites: { player:null, npc:null, wolf:null }
};

function buildTerrainTiles() {
  for (let i=0;i<4;i++) {
    assets.grass.push(makeTile((p)=>{
      p.fillStyle = palette.grass[i%palette.grass.length]; p.fillRect(0,0,32,32);
      for (let y=0;y<32;y+=2){
        for (let x=0;x<32;x+=2){
          const n=rng(x+i*9,y+i*5,13+i);
          p.fillStyle = n>0.72?"rgba(171,205,131,.22)":n<0.14?"rgba(34,57,26,.28)":"rgba(0,0,0,0)";
          if (n>0.72||n<0.14) p.fillRect(x,y,2,2);
        }
      }
      p.fillStyle="rgba(255,255,255,.04)"; p.fillRect(0,0,32,2);
      p.fillStyle="rgba(0,0,0,.12)"; p.fillRect(0,30,32,2);
    }));

    assets.road.push(makeTile((p)=>{
      p.fillStyle = palette.road[0]; p.fillRect(0,0,32,32);
      p.fillStyle = palette.road[1];
      for(let y=0;y<32;y+=4){ for(let x=((y+i)%3);x<32;x+=6) p.fillRect(x,y,2,2); }
      p.fillStyle = palette.road[2];
      for(let k=0;k<7;k++){ const x=((k*11+i*7)%26)+2; const y=((k*13+i*5)%26)+2; p.fillRect(x,y,3,2); }
      p.fillStyle = "rgba(0,0,0,.14)"; p.fillRect(0,29,32,3);
      p.fillStyle = "rgba(255,255,255,.06)"; p.fillRect(0,0,32,2);
    }));

    assets.shore.push(makeTile((p)=>{
      p.fillStyle = i%2?"#5f7648":"#6f8452"; p.fillRect(0,0,32,32);
      p.fillStyle = "rgba(146,114,74,.4)"; p.fillRect(0,24,32,8);
      p.fillStyle = "rgba(102,130,85,.4)"; p.fillRect(0,0,32,10);
      p.fillStyle = "rgba(223,201,150,.2)"; p.fillRect(0,21,32,2);
      for(let x=4;x<30;x+=6){ p.fillStyle="#486d3f"; p.fillRect(x,16+(x%3),2,8); }
    }));
  }

  assets.water.deep = makeTile((p)=>{
    p.fillStyle = palette.water[1]; p.fillRect(0,0,32,32);
    p.fillStyle = palette.water[0]; p.fillRect(0,22,32,10);
    p.fillStyle = "rgba(98,164,214,.2)";
    for(let y=3;y<28;y+=5) p.fillRect(3+(y%4),y,24,1);
    p.fillStyle = "rgba(179,226,255,.13)"; p.fillRect(2,3,17,2);
  });
  assets.water.shallow = makeTile((p)=>{
    p.fillStyle = palette.water[2]; p.fillRect(0,0,32,32);
    p.fillStyle = "rgba(143,203,237,.24)"; p.fillRect(1,2,30,5);
    p.fillStyle = "rgba(63,115,165,.3)"; p.fillRect(0,24,32,8);
    p.fillStyle = "rgba(195,236,255,.23)"; p.fillRect(4,12,22,2);
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
  for(let i=0;i<2;i++) assets.fence.push(makeTile((p)=>{
    p.fillStyle = palette.fence[0]; p.fillRect(2,12,28,4);
    p.fillStyle = palette.fence[1]; p.fillRect(5,5,4,22); p.fillRect(23,5,4,22);
    p.fillStyle = palette.fence[2]; p.fillRect(2,11,28,1);
  }));
}

function paintHumanoidSheet(colors) {
  const size = 64;
  const c = document.createElement("canvas");
  c.width = size * 3;
  c.height = size * 4;
  const p = c.getContext("2d"); p.imageSmoothingEnabled=false;

  const dirs = ["down","left","right","up"];
  const stepOffset = [0,1,-1];

  function drawFrame(baseX, baseY, dir, step){
    const bx = baseX + 18;
    const by = baseY + 14;
    const legA = step*2;
    const legB = -step*2;
    p.fillStyle = colors.boots;
    p.fillRect(bx+6, by+28+legA, 6, 8);
    p.fillRect(bx+18, by+28+legB, 6, 8);

    p.fillStyle = colors.cloak;
    p.fillRect(bx+4, by+16, 22, 14);

    p.fillStyle = colors.tunic;
    p.fillRect(bx+7, by+15, 16, 14);
    p.fillStyle = colors.tunicShade; p.fillRect(bx+7, by+24, 16, 5);

    p.fillStyle = colors.skin;
    if (dir === "left") p.fillRect(bx+6, by+4, 12, 12);
    else if (dir === "right") p.fillRect(bx+12, by+4, 12, 12);
    else p.fillRect(bx+9, by+3, 12, 12);

    p.fillStyle = colors.hair;
    if (dir === "up") p.fillRect(bx+8, by+2, 14, 6);
    else if (dir === "left") p.fillRect(bx+6, by+3, 10, 6);
    else if (dir === "right") p.fillRect(bx+13, by+3, 10, 6);
    else p.fillRect(bx+8, by+2, 14, 5);

    p.strokeStyle = "rgba(10,16,24,.7)"; p.strokeRect(bx+6.5, by+3.5, 18, 33);
  }

  dirs.forEach((d,row)=> stepOffset.forEach((s,col)=> drawFrame(col*size,row*size,d,s)));
  const img = new Image(); img.src = c.toDataURL("image/png"); return img;
}

function paintWolfSheet() {
  const size = 64;
  const c = document.createElement("canvas"); c.width = size*3; c.height = size*2;
  const p = c.getContext("2d"); p.imageSmoothingEnabled=false;

  function frame(baseX,baseY,dir,step){
    const bx=baseX+12, by=baseY+20;
    const swing = step*2;
    p.fillStyle="#8f99a8"; p.fillRect(bx+10, by+8, 28, 12);
    p.fillStyle="#747f8e"; p.fillRect(bx+10, by+8, 28, 4);
    const hx = dir==="right"?30:4;
    p.fillStyle="#99a4b5"; p.fillRect(bx+hx, by+2, 14, 10);
    p.fillStyle="#6f7987"; p.fillRect(bx+hx+(dir==="right"?8:0), by+8, 6,3);
    p.fillStyle="#7c8796"; p.fillRect(bx+14, by+20+swing, 5,8); p.fillRect(bx+26, by+20-swing,5,8);
    p.fillStyle="#6f7987"; if(dir==="right") p.fillRect(bx+6,by+12,8,3); else p.fillRect(bx+34,by+12,8,3);
    p.strokeStyle="rgba(8,12,18,.7)"; p.strokeRect(bx+9.5,by+1.5,35,27);
  }
  ["left","right"].forEach((dir,row)=>[-1,0,1].forEach((s,col)=>frame(col*size,row*size,dir,s)));
  const img = new Image(); img.src = c.toDataURL("image/png"); return img;
}

buildTerrainTiles();
makeBuildingTiles();
makeTreeSprites();
makeFenceTiles();
assets.sprites.player = paintHumanoidSheet({ skin:"#e5c9a5", hair:"#4f3d30", tunic:"#3f77d2", tunicShade:"#2b549b", cloak:"#cad2db", boots:"#5d4029" });
assets.sprites.npc = paintHumanoidSheet({ skin:"#dbc39f", hair:"#d8e2ef", tunic:"#6c57b8", tunicShade:"#4f3f8d", cloak:"#46347a", boots:"#433124" });
assets.sprites.wolf = paintWolfSheet();

const world = { blocked:new Set(), trees:[], fences:[], buildings:[], roads:[], zones:[], pondBlocked:new Set(), pondWater:new Set(), pondShore:new Set(), pondNearEdge:new Set() };
function blockRect(x,y,w,h){ for(let ix=x;ix<x+w;ix++)for(let iy=y;iy<y+h;iy++) world.blocked.add(keyOf(ix,iy)); }

world.roads.push(
  { x:6,y:11,w:26,h:2 },{ x:17,y:5,w:2,h:15 },{ x:10,y:8,w:2,h:8 },
  { x:24,y:7,w:2,h:8 },{ x:19,y:12,w:5,h:2 },{ x:26,y:12,w:3,h:2 }
);

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

const treeData = [[1,2,"a"],[2,2,"b"],[3,3,"a"],[2,5,"c"],[1,6,"a"],[3,7,"b"],[2,9,"a"],[1,11,"c"],[3,12,"a"],[2,14,"b"],[1,17,"a"],[2,19,"b"],[3,21,"a"],[1,22,"c"],[4,23,"a"],[2,1,"a"],[4,2,"c"],[7,1,"b"],[10,2,"a"],[13,2,"c"],[27,2,"a"],[30,1,"b"],[33,2,"a"],[35,1,"c"],[37,2,"a"],[36,2,"a"],[35,4,"b"],[37,5,"a"],[36,7,"c"],[35,9,"a"],[36,11,"b"],[37,13,"a"],[35,15,"c"],[36,17,"a"],[37,19,"b"],[35,21,"a"],[36,23,"c"],[34,22,"a"],[4,22,"b"],[6,23,"a"],[9,22,"c"],[12,23,"a"],[15,22,"b"],[24,23,"a"],[27,22,"c"],[30,23,"a"],[33,22,"b"],[5,5,"a"],[6,8,"b"],[7,19,"a"],[9,4,"c"],[31,5,"a"],[32,8,"b"],[31,19,"a"],[29,21,"c"],[21,15,"a"],[22,18,"c"],[29,16,"b"],[28,19,"c"]];
treeData.forEach(([x,y,type])=>{ world.trees.push({x,y,type,seed:rng(x,y,91)}); world.blocked.add(keyOf(x,y)); });

world.zones.push(
  {name:"Hearthvale Square",x:9,y:7,w:18,h:11},
  {name:"Mirror Pond",x:21,y:12,w:10,h:8},
  {name:"Forest Edge",x:27,y:3,w:11,h:19},
  {name:"West Lane",x:0,y:7,w:10,h:12}
);

const player={x:18,y:11,px:18*TILE,py:11*TILE,targetX:18,targetY:11,hp:50,maxHp:50,xp:0,coins:0,moving:false,facing:"down",speed:180,attackUntil:0,hitUntil:0,hitFlickerUntil:0,attackLungeX:0,attackLungeY:0,recoilX:0,recoilY:0};
const npc={x:21,y:12,name:"Edrin Vale",facing:"down"};
const wolf={x:31,y:13,px:31*TILE,py:13*TILE,targetX:31,targetY:13,hp:22,maxHp:22,homeX:31,homeY:13,roam:3,speed:110,facing:"left",attackUntil:0,hitUntil:0,hitFlickerUntil:0,attackLungeX:0,attackLungeY:0,recoilX:0,recoilY:0,moving:false};

let lastWolfDecision=0,lastWolfAttack=0,lastPlayerAttack=0,wolfRespawnAt=0,hitStopUntil=0;
let activeDialogue=null,dialogueIndex=0;
const edrinLines=["You are not from here.","...good.","This town is older than it lets itself appear.","Mirror Pond listens longer than most people do.","Walk slowly. Some places reveal themselves only when you stop trying to rush them."];

function startDialogue(name,lines){ activeDialogue={name,lines}; dialogueIndex=0; renderDialogue(); }
function renderDialogue(){ if(!activeDialogue) return; dialogue.style.display="block"; dialogueName.textContent=activeDialogue.name; dialogueText.textContent=activeDialogue.lines[dialogueIndex]; }
dialogue.addEventListener("click",()=>{ if(!activeDialogue) return; dialogueIndex++; if(dialogueIndex>=activeDialogue.lines.length){ activeDialogue=null; dialogue.style.display="none"; return;} renderDialogue(); });

function currentZoneName(){
  for(const z of world.zones){ if(player.targetX>=z.x&&player.targetX<z.x+z.w&&player.targetY>=z.y&&player.targetY<z.y+z.h) return z.name; }
  return "Outer Road";
}

function updateSidebar(){
  hpVal.textContent = player.hp + "/" + player.maxHp;
  xpVal.textContent = String(player.xp);
  coinsVal.textContent = String(player.coins);
  zoneVal.textContent = currentZoneName();
  questVal.textContent = "Town Slice";
  objectiveText.textContent = "Walk Hearthvale, visit Mirror Pond, and speak to Edrin Vale.";
  hud.textContent = "WASD / Arrows : Move\nSpace : Attack\nClick Edrin Vale : Talk\nWolf nearby : Keep distance\nG : Toggle grid\nCurrent Zone : " + currentZoneName();
}

function canMoveTo(x,y){ if(x<0||y<0||x>=WORLD_W||y>=WORLD_H) return false; if(world.blocked.has(keyOf(x,y))||world.pondBlocked.has(keyOf(x,y))) return false; if(x===npc.x&&y===npc.y) return false; if(wolf.hp>0&&x===wolf.targetX&&y===wolf.targetY) return false; return true; }

const keys=new Set();
let showGrid=false;
addEventListener("keydown",(e)=>{ const k=e.key.toLowerCase(); if(["w","a","s","d","arrowup","arrowdown","arrowleft","arrowright"," "].includes(k)) e.preventDefault(); if(k==="g") showGrid=!showGrid; keys.add(k); });
addEventListener("keyup",(e)=> keys.delete(e.key.toLowerCase()));
canvas.addEventListener("click",(e)=>{ if(activeDialogue) return; const clicked=screenToWorld(e.clientX,e.clientY); if(clicked.x===npc.x&&clicked.y===npc.y) startDialogue(npc.name,edrinLines); });

function getCamera(){
  const tileX=Math.max(0,Math.min(player.targetX-Math.floor(VIEW_TILES_X/2),WORLD_W-VIEW_TILES_X));
  const tileY=Math.max(0,Math.min(player.targetY-Math.floor(VIEW_TILES_Y/2),WORLD_H-VIEW_TILES_Y));
  const viewPxW=VIEW_TILES_X*TILE, viewPxH=VIEW_TILES_Y*TILE;
  const offsetX=Math.floor((canvas.width-viewPxW)/2), offsetY=Math.floor((canvas.height-viewPxH)/2);
  return {tileX,tileY,offsetX,offsetY};
}
function tileToScreen(tx,ty){ const cam=getCamera(); return {x:(tx-cam.tileX)*TILE+cam.offsetX,y:(ty-cam.tileY)*TILE+cam.offsetY}; }
function screenToWorld(clientX,clientY){ const rect=canvas.getBoundingClientRect(); const mx=clientX-rect.left,my=clientY-rect.top; const cam=getCamera(); return {x:Math.floor((mx-cam.offsetX)/TILE)+cam.tileX,y:Math.floor((my-cam.offsetY)/TILE)+cam.tileY}; }

function smoothMove(entity,dt){ const tx=entity.targetX*TILE, ty=entity.targetY*TILE; const dx=tx-entity.px, dy=ty-entity.py; const dist=Math.hypot(dx,dy); if(dist<.35){ entity.px=tx; entity.py=ty; entity.moving=false; return; } entity.moving=true; const step=entity.speed*dt; entity.px += (dx/dist)*Math.min(step,dist); entity.py += (dy/dist)*Math.min(step,dist); }
function tryPlayerStep(dx,dy,facing){ if(player.moving||activeDialogue) return; const nx=player.targetX+dx, ny=player.targetY+dy; player.facing=facing; if(!canMoveTo(nx,ny)) return; player.targetX=nx; player.targetY=ny; }
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

function canWolfMoveTo(x,y){ if(x<0||y<0||x>=WORLD_W||y>=WORLD_H) return false; if(world.blocked.has(keyOf(x,y))) return false; if(x===npc.x&&y===npc.y) return false; return true; }
function updateWolf(now){
  if(wolf.hp<=0){ if(wolfRespawnAt!==0&&now>=wolfRespawnAt){ wolf.hp=wolf.maxHp; wolf.targetX=wolf.homeX; wolf.targetY=wolf.homeY; wolf.px=wolf.targetX*TILE; wolf.py=wolf.targetY*TILE; wolfRespawnAt=0; log("The wolf prowls back into the clearing."); } return; }
  if(now-lastWolfDecision<650) return; lastWolfDecision=now;
  const dx=player.targetX-wolf.targetX, dy=player.targetY-wolf.targetY, dist=Math.abs(dx)+Math.abs(dy);
  if(dist<=4){
    const sx=dx===0?0:dx>0?1:-1, sy=dy===0?0:dy>0?1:-1;
    const a={x:wolf.targetX+sx,y:wolf.targetY}, b={x:wolf.targetX,y:wolf.targetY+sy};
    if(Math.abs(dx)>=Math.abs(dy)&&canWolfMoveTo(a.x,a.y)){ wolf.targetX=a.x; wolf.targetY=a.y; if(sx!==0) wolf.facing=sx>0?"right":"left"; }
    else if(canWolfMoveTo(b.x,b.y)) wolf.targetY=b.y;
  } else {
    const backX=wolf.targetX<wolf.homeX?1:wolf.targetX>wolf.homeX?-1:0;
    const backY=wolf.targetY<wolf.homeY?1:wolf.targetY>wolf.homeY?-1:0;
    if(Math.abs(wolf.targetX-wolf.homeX)>wolf.roam&&canWolfMoveTo(wolf.targetX+backX,wolf.targetY)){ wolf.targetX+=backX; if(backX!==0) wolf.facing=backX>0?"right":"left"; }
    if(Math.abs(wolf.targetY-wolf.homeY)>wolf.roam&&canWolfMoveTo(wolf.targetX,wolf.targetY+backY)) wolf.targetY+=backY;
  }
}
function wolfAttack(now){
  if(wolf.hp<=0) return;
  const dist=Math.abs(player.targetX-wolf.targetX)+Math.abs(player.targetY-wolf.targetY);
  if(dist>1||now-lastWolfAttack<1100) return;
  lastWolfAttack=now; wolf.attackUntil=now+350;
  player.hp=Math.max(0,player.hp-5); player.hitUntil=now+300; player.hitFlickerUntil=now+220; hitStopUntil=now+55;
  const wx=player.targetX-wolf.targetX, wy=player.targetY-wolf.targetY, len=Math.max(1,Math.hypot(wx,wy));
  wolf.attackLungeX=(wx/len)*2; wolf.attackLungeY=(wy/len)*1.2; player.recoilX=(wx/len)*2.5; player.recoilY=(wy/len)*1.6;
  log("A wolf bites you for 5.");
  if(player.hp<=0){ player.hp=player.maxHp; player.targetX=18; player.targetY=11; player.px=player.targetX*TILE; player.py=player.targetY*TILE; log("System: You wake in Hearthvale Square."); }
}
function tryPlayerAttack(now){
  if(activeDialogue||wolf.hp<=0) return; if(!(keys.has(" ")||keys.has("space"))) return; if(now-lastPlayerAttack<420) return;
  lastPlayerAttack=now; player.attackUntil=now+350;
  const step={up:{x:0,y:-1},down:{x:0,y:1},left:{x:-1,y:0},right:{x:1,y:0}}[player.facing]||{x:0,y:1};
  const ax=player.targetX+step.x, ay=player.targetY+step.y;
  if(ax!==wolf.targetX||ay!==wolf.targetY){ log("You swing at empty air."); return; }
  wolf.hp=Math.max(0,wolf.hp-6); wolf.hitUntil=now+320; wolf.hitFlickerUntil=now+240; hitStopUntil=now+65;
  player.attackLungeX=step.x*2.4; player.attackLungeY=step.y*1.4; wolf.recoilX=step.x*2.3; wolf.recoilY=step.y*1.5;
  log("You strike the wolf for 6.");
  if(wolf.hp<=0){ player.xp+=12; player.coins+=4; wolfRespawnAt=now+10000; log("The wolf collapses. (+12 XP, +4 coins)"); }
}

function drawSoftShadow(cx,cy,rx,ry,a=.2){
  const g=ctx.createRadialGradient(cx+3,cy+3,Math.max(1,rx*.35),cx+3,cy+3,Math.max(rx,ry)*1.3);
  g.addColorStop(0,`rgba(0,0,0,${(a*.86).toFixed(3)})`); g.addColorStop(1,"rgba(0,0,0,0)");
  ctx.fillStyle=g; ctx.beginPath(); ctx.ellipse(cx+3,cy+3,rx,ry,0,0,Math.PI*2); ctx.fill();
}

function frameFromSprite(dir,moving){
  const row = dir==="down"?0:dir==="left"?1:dir==="right"?2:3;
  if(!moving) return {sx:64, sy:row*64};
  const col = Math.floor(performance.now()/120)%2===0 ? 0 : 2;
  return {sx:col*64, sy:row*64};
}

function drawHumanoid(sheet, tx, ty, facing, moving, scale, label, hitAlpha, recoil, attackData){
  const p = tileToScreen(tx,ty);
  const shiftX = Math.round((recoil?.x||0) + ((attackData&&attackData.active)?attackData.thrust:0));
  const shiftY = Math.round((recoil?.y||0) - ((attackData&&attackData.active)?Math.abs(attackData.thrust)*.2:0));
  const drawW = Math.round(64*scale), drawH = Math.round(64*scale);
  const dx = p.x + Math.round((32-drawW)/2) + shiftX;
  const dy = p.y - Math.round(drawH-32) + shiftY;
  drawSoftShadow(p.x+16,p.y+28,8*scale,4*scale,.24);

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
    ctx.fillStyle=`rgba(255,86,86,${Math.min(.45,hitAlpha).toFixed(3)})`; ctx.fillRect(dx+8,dy+7,drawW-16,drawH-12);
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

function drawWolf(tx,ty,facing,moving,scale,hitAlpha,recoil){
  const p=tileToScreen(tx,ty), row=facing==="right"?1:0;
  const col=!moving?1:(Math.floor(performance.now()/140)%2===0?0:2);
  const drawW=Math.round(64*scale),drawH=Math.round(64*scale);
  const dx=p.x+Math.round((32-drawW)/2)+Math.round(recoil?.x||0), dy=p.y-Math.round(drawH-32)+Math.round(recoil?.y||0);
  drawSoftShadow(p.x+16,p.y+28,9*scale,4*scale,.24);
  if(assets.sprites.wolf.complete&&assets.sprites.wolf.naturalWidth>0) ctx.drawImage(assets.sprites.wolf,col*64,row*64,64,64,dx,dy,drawW,drawH);
  ctx.fillStyle="rgba(0,0,0,.5)"; ctx.fillRect(p.x+2,p.y-10,24,4);
  ctx.fillStyle="#8fdb73"; ctx.fillRect(p.x+2,p.y-10,24*(wolf.hp/wolf.maxHp),4);
  if(hitAlpha>0){ ctx.fillStyle=`rgba(255,255,255,${Math.min(.4,hitAlpha).toFixed(3)})`; ctx.fillRect(dx+8,dy+8,drawW-14,drawH-16); }
}

function hitVisualAlpha(e){ const now=performance.now(); if(now>=e.hitUntil) return 0; const left=e.hitUntil-now; const base=Math.min(.52,.2+left/300); const flick=now<e.hitFlickerUntil&&Math.floor(now/36)%2===0?.24:0; return Math.max(0,base+flick); }
function attackPose(entity){ const now=performance.now(); const total=350; const left=Math.max(0,entity.attackUntil-now); if(left<=0) return {active:false,thrust:0}; const t=(total-left)/total; return {active:true,thrust:Math.sin(t*Math.PI)*3.5}; }

function drawAlignmentGrid(){ const cam=getCamera(); const sx=cam.offsetX, sy=cam.offsetY, ex=sx+VIEW_TILES_X*TILE, ey=sy+VIEW_TILES_Y*TILE; ctx.save(); ctx.strokeStyle="rgba(221,233,255,.16)"; ctx.lineWidth=1; ctx.beginPath(); for(let x=0;x<=VIEW_TILES_X;x++){ const px=sx+x*TILE+.5; ctx.moveTo(px,sy); ctx.lineTo(px,ey);} for(let y=0;y<=VIEW_TILES_Y;y++){ const py=sy+y*TILE+.5; ctx.moveTo(sx,py); ctx.lineTo(ex,py);} ctx.stroke(); ctx.restore(); }

function drawWorld(){
  ctx.clearRect(0,0,canvas.width,canvas.height);
  const cam=getCamera();
  for(let y=cam.tileY;y<cam.tileY+VIEW_TILES_Y;y++) for(let x=cam.tileX;x<cam.tileX+VIEW_TILES_X;x++){
    const mix=Math.floor(rng(x,y,4)*assets.grass.length);
    const p=tileToScreen(x,y);
    const img=assets.grass[mix];
    if(img.complete&&img.naturalWidth>0) ctx.drawImage(img,p.x,p.y,TILE,TILE);
  }

  world.roads.forEach(r=>{ for(let x=r.x;x<r.x+r.w;x++) for(let y=r.y;y<r.y+r.h;y++){ const p=tileToScreen(x,y); const img=assets.road[Math.floor(rng(x,y,22)*assets.road.length)]; if(img.complete&&img.naturalWidth>0) ctx.drawImage(img,p.x,p.y,32,32);} });

  for(let x=pond.x-1;x<=pond.x+pond.w;x++) for(let y=pond.y-1;y<=pond.y+pond.h;y++){
    const k=keyOf(x,y); if(!world.pondWater.has(k)) continue;
    const p=tileToScreen(x,y); const edge=world.pondNearEdge.has(k);
    const img=edge?assets.water.shallow:assets.water.deep; if(img.complete&&img.naturalWidth>0) ctx.drawImage(img,p.x,p.y,32,32);
    const t=performance.now()*0.002, rip=(Math.sin(t*3+x*1.1+y*.8)+1)*.5;
    ctx.fillStyle=`rgba(188,228,255,${(.02+rip*.05).toFixed(3)})`; ctx.fillRect(p.x+3,p.y+6,TILE-10,1);
    if(edge){ ctx.fillStyle=`rgba(224,244,255,${(.05+rip*.05).toFixed(3)})`; ctx.fillRect(p.x+1,p.y+1,TILE-2,1); }
  }
  for(let x=pond.x-1;x<=pond.x+pond.w;x++) for(let y=pond.y-1;y<=pond.y+pond.h;y++){
    const k=keyOf(x,y); if(!world.pondShore.has(k)) continue;
    const p=tileToScreen(x,y); const img=assets.shore[Math.floor(rng(x,y,33)*assets.shore.length)]; if(img.complete&&img.naturalWidth>0) ctx.drawImage(img,p.x,p.y,32,32);
  }

  world.buildings.forEach(b=>{
    const gp = tileToScreen(b.x,b.y+b.h); drawSoftShadow(gp.x+(b.w*16), gp.y+2, b.w*16, 7,.22);
    b.tileRows.forEach((row,ry)=> row.forEach((key,rx)=> { const p=tileToScreen(b.x+rx,b.y+ry); const img=assets.building[key]; if(img&&img.complete&&img.naturalWidth>0) ctx.drawImage(img,p.x,p.y,32,32); }));
  });

  const well = tileToScreen(18,11);
  ctx.fillStyle="#6d7580"; ctx.beginPath(); ctx.arc(well.x+16,well.y+16,11,0,Math.PI*2); ctx.fill();
  ctx.fillStyle="#315685"; ctx.beginPath(); ctx.arc(well.x+16,well.y+16,6,0,Math.PI*2); ctx.fill();
  ctx.fillStyle="#8e7450"; ctx.fillRect(well.x+6,well.y+4,3,10); ctx.fillRect(well.x+23,well.y+4,3,10); ctx.fillRect(well.x+8,well.y+4,16,3);

  world.fences.forEach((f,i)=>{ const p=tileToScreen(f.x,f.y); const img=assets.fence[i%assets.fence.length]; if(img.complete&&img.naturalWidth>0) ctx.drawImage(img,p.x,p.y,32,32); });
  world.trees.forEach(t=>{ const p=tileToScreen(t.x,t.y); const sway=Math.sin(performance.now()*0.0012+t.seed*8)*0.8; drawSoftShadow(p.x+16,p.y+25,10,5,.2); const img=assets.tree[t.type]||assets.tree.a; if(img.complete&&img.naturalWidth>0) ctx.drawImage(img,p.x+Math.round(sway),p.y-4,32,36); });

  if(showGrid) drawAlignmentGrid();

  function zoneLabel(text,tx,ty){ const p=tileToScreen(tx,ty); const w=text.length*7+12; ctx.fillStyle="rgba(7,11,18,.85)"; ctx.fillRect(p.x-3,p.y-31,w,16); ctx.strokeStyle="rgba(204,216,236,.62)"; ctx.strokeRect(p.x-3.5,p.y-31.5,w,16); ctx.fillStyle="#eff4ff"; ctx.font="bold 11px monospace"; ctx.fillText(text,p.x+2,p.y-19); }
  const zoneName=currentZoneName();
  if(zoneName==="Hearthvale Square") zoneLabel("Hearthvale Square",12,7);
  if(zoneName==="Mirror Pond") zoneLabel("Mirror Pond",23,12);
  if(zoneName==="Forest Edge") zoneLabel("Forest Edge",30,4);

  drawHumanoid(assets.sprites.npc, npc.x, npc.y, npc.facing, false, 0.78, Math.abs(player.targetX-npc.x)+Math.abs(player.targetY-npc.y)<=5?npc.name:"", 0, null, null);
  if(wolf.hp>0) drawWolf(wolf.px/TILE, wolf.py/TILE, wolf.facing, wolf.moving, 0.82, hitVisualAlpha(wolf), {x:wolf.recoilX+wolf.attackLungeX,y:wolf.recoilY+wolf.attackLungeY});
  drawHumanoid(assets.sprites.player, player.px/TILE, player.py/TILE, player.facing, player.moving, 0.84, "Wayfarer", hitVisualAlpha(player), {x:player.recoilX+player.attackLungeX,y:player.recoilY+player.attackLungeY}, attackPose(player));

  const tint=0.08+Math.max(0,Math.sin(performance.now()/9000))*.07;
  ctx.fillStyle=`rgba(9,16,26,${tint.toFixed(3)})`; ctx.fillRect(0,0,canvas.width,canvas.height);
  const edge=ctx.createRadialGradient(canvas.width*.5,canvas.height*.5,Math.min(canvas.width,canvas.height)*.35,canvas.width*.5,canvas.height*.5,Math.max(canvas.width,canvas.height)*.68);
  edge.addColorStop(0,"rgba(0,0,0,0)"); edge.addColorStop(.78,"rgba(1,6,10,.1)"); edge.addColorStop(1,"rgba(1,6,10,.46)");
  ctx.fillStyle=edge; ctx.fillRect(0,0,canvas.width,canvas.height);
}

function update(dt,now){
  player.recoilX*=.8; player.recoilY*=.8; player.attackLungeX*=.74; player.attackLungeY*=.74;
  wolf.recoilX*=.82; wolf.recoilY*=.82; wolf.attackLungeX*=.78; wolf.attackLungeY*=.78;
  if(now<hitStopUntil){ updateSidebar(); return; }
  updateInput(); tryPlayerAttack(now); smoothMove(player,dt);
  if(!player.moving&&(moveIntent.dx!==0||moveIntent.dy!==0)) tryPlayerStep(moveIntent.dx,moveIntent.dy,moveIntent.facing);
  updateWolf(now); smoothMove(wolf,dt); wolfAttack(now); updateSidebar();
}

let last=performance.now();
function loop(now){ const dt=Math.min(.033,(now-last)/1000); last=now; update(dt,now); drawWorld(); requestAnimationFrame(loop); }

log("System: Artistic rebuild slice loaded.");
log("System: Walk Hearthvale, visit Mirror Pond, and speak to Edrin Vale.");
updateSidebar();
requestAnimationFrame(loop);
</script>
</body>
</html>`;
