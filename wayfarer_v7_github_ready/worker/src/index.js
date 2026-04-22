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
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === "/favicon.ico") {
      return new Response(null, { status: 204 });
    }
    return new Response(html, {
      headers: { "content-type": "text/html; charset=UTF-8" },
    });
  },
};

const html = `<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Wayfarer v7</title>
<style>
  body { margin:0; overflow:hidden; background:#111; color:#fff; font-family:monospace; }
  #ui { position:fixed; top:10px; left:10px; z-index:5; background:rgba(0,0,0,.55); padding:10px; border:1px solid #666; }
  #dialogue { position:fixed; left:50%; transform:translateX(-50%); bottom:20px; width:min(760px,92vw); z-index:6; background:rgba(10,10,20,.92); border:2px solid #d7d7ff; padding:14px; display:none; }
  #dialogue button { margin-top:10px; font-family:inherit; }
  #inventory { position:fixed; top:10px; right:10px; width:260px; z-index:6; background:rgba(0,0,0,.6); border:1px solid #666; padding:10px; display:none; }
  #slots { display:grid; grid-template-columns:repeat(5, 1fr); gap:6px; }
  .slot { height:34px; border:1px solid #777; display:flex; align-items:center; justify-content:center; font-size:10px; text-align:center; padding:2px; background:rgba(255,255,255,.04); }
  canvas { display:block; image-rendering: pixelated; }
  .muted { color:#bbb; }
</style>
</head>
<body>
<div id="ui">
  <div><strong>Wayfarer v7</strong></div>
  <div class="muted">Move: WASD / Arrows</div>
  <div class="muted">Attack: Space</div>
  <div class="muted">Inventory: I</div>
  <div id="status">Connected. Mirror Pond awaits.</div>
  <div id="xp">XP: 0</div>
  <div id="zone">Zone: Hearthvale Crossroads</div>
</div>
<div id="inventory">
  <div><strong>Inventory</strong> (20)</div>
  <div id="slots"></div>
</div>
<div id="dialogue">
  <div id="dialogueName"></div>
  <div id="dialogueText" style="margin-top:8px; white-space:pre-line;"></div>
  <button id="dialogueNext">Continue</button>
</div>
<canvas id="game"></canvas>
<script>
const canvas = document.getElementById('game');
const ctx = canvas.getContext('2d');
const TILE = 32;
const VIEW_W = () => Math.floor(canvas.width / TILE);
const VIEW_H = () => Math.floor(canvas.height / TILE);
function resize(){ canvas.width = innerWidth; canvas.height = innerHeight; }
addEventListener('resize', resize); resize();

const world = { width: 72, height: 54 };
const player = { x: 10, y: 26, hp: 100, maxHp: 100, atk: 7, xp: 0, facing:'down', inventory:["Rusty Sword"], footprints:[] };
const state = { showInv:false, dialogue:null, dialogueIndex:0, ticks:0, combatCooldown:0 };

const zones = [
  { name:'Hearthvale Crossroads', x1:0,y1:20,x2:20,y2:34 },
  { name:'Western Fields', x1:0,y1:10,x2:22,y2:20 },
  { name:'Eastern Fields', x1:20,y1:10,x2:42,y2:22 },
  { name:'Mirror Pond', x1:29,y1:24,x2:49,y2:42 },
  { name:'Wolf Territory North', x1:45,y1:7,x2:68,y2:20 },
  { name:'Wolf Territory East', x1:50,y1:24,x2:70,y2:40 }
];

const pond = { x1:33, y1:27, x2:44, y2:36 };
const farms = [
  { x1:5,y1:12,x2:14,y2:18, label:'Field A' },
  { x1:22,y1:12,x2:31,y2:18, label:'Field B' },
  { x1:34,y1:12,x2:41,y2:18, label:'Field C' }
];
const trees = [];
for (let i=0;i<130;i++) {
  const x = 40 + (i*7)%30;
  const y = 4 + (i*11)%44;
  if ((x > pond.x1-2 && x < pond.x2+2 && y > pond.y1-2 && y < pond.y2+2)) continue;
  trees.push({x,y});
}
for (let i=0;i<50;i++) trees.push({x:2 + (i*3)%18, y:2 + (i*5)%12});

const npcs = [
  {
    id:'edrin', name:'Edrin Vale', x:31, y:25,
    dialogue:[
      'You are not from here.',
      '...good.',
      'Most travelers walk roads.',
      'Few question where they lead.',
      'There is a stone beyond the trees.',
      'It should not exist.',
      'Yet it does.'
    ]
  }
];

const loot = [];
const creatures = [];
function addCreature(type,x,y){
  creatures.push({
    type,x,y,hp:type==='wolf'?28:14,maxHp:type==='wolf'?28:14,
    atk:type==='wolf'?6:2, cooldown:0, dead:0,
    homeX:x, homeY:y,
    color:type==='wolf'?'#9aa3ad':'#9a6b2f',
    loot:type==='wolf'?[['Wolf Pelt',1],['Raw Meat',1],['Coins',6]]:[['Turkey Meat',1],['Feather',1],['Coins',3]]
  });
}
[[52,12],[57,14],[60,15],[55,18],[63,16],[58,30],[61,32],[64,35],[67,34]].forEach(p=>addCreature('wolf',...p));
[[9,15],[11,16],[24,14],[26,16],[36,15],[38,16]].forEach(p=>addCreature('turkey',...p));

function currentZone(){
  const z = zones.find(z => player.x>=z.x1 && player.x<=z.x2 && player.y>=z.y1 && player.y<=z.y2);
  return z ? z.name : 'Outskirts';
}
function passable(x,y){
  if (x<0||y<0||x>=world.width||y>=world.height) return false;
  if (trees.some(t=>t.x===x&&t.y===y)) return false;
  return true;
}
function addFootprint(){ player.footprints.push({x:player.x,y:player.y,life:40}); if(player.footprints.length>40) player.footprints.shift(); }
function move(dx,dy){
  const nx=player.x+dx, ny=player.y+dy;
  if (dx>0) player.facing='right'; if (dx<0) player.facing='left'; if (dy>0) player.facing='down'; if (dy<0) player.facing='up';
  if(passable(nx,ny)){ addFootprint(); player.x=nx; player.y=ny; pickupLoot(); }
}
addEventListener('keydown', e=>{
  if (state.dialogue) return;
  if (e.key==='ArrowUp'||e.key==='w'||e.key==='W') move(0,-1);
  if (e.key==='ArrowDown'||e.key==='s'||e.key==='S') move(0,1);
  if (e.key==='ArrowLeft'||e.key==='a'||e.key==='A') move(-1,0);
  if (e.key==='ArrowRight'||e.key==='d'||e.key==='D') move(1,0);
  if (e.key===' ') attackNearest();
  if (e.key==='i'||e.key==='I') toggleInventory();
});
canvas.addEventListener('click', e=>{
  const {wx, wy} = screenToWorld(e.clientX, e.clientY);
  const npc = npcs.find(n=>n.x===wx&&n.y===wy);
  if (npc){ openDialogue(npc); return; }
  const c = creatures.find(c=>!c.dead && Math.abs(c.x-wx)<=0 && Math.abs(c.y-wy)<=0);
  if (c) attackCreature(c);
});
function toggleInventory(){ state.showInv=!state.showInv; document.getElementById('inventory').style.display = state.showInv ? 'block':'none'; renderInventory(); }
function renderInventory(){
  const slots = document.getElementById('slots'); slots.innerHTML='';
  for(let i=0;i<20;i++){
    const div = document.createElement('div'); div.className='slot'; div.textContent = player.inventory[i] || ''; slots.appendChild(div);
  }
}
function openDialogue(npc){ state.dialogue=npc; state.dialogueIndex=0; document.getElementById('dialogue').style.display='block'; document.getElementById('dialogueName').textContent=npc.name; renderDialogue(); }
function renderDialogue(){ document.getElementById('dialogueText').textContent = state.dialogue.dialogue[state.dialogueIndex]; }
document.getElementById('dialogueNext').onclick=()=>{
  if(!state.dialogue) return;
  state.dialogueIndex++;
  if(state.dialogueIndex>=state.dialogue.dialogue.length){ document.getElementById('dialogue').style.display='none'; state.dialogue=null; return; }
  renderDialogue();
};
function pickupLoot(){
  for (let i=loot.length-1;i>=0;i--){
    const l=loot[i];
    if(l.x===player.x&&l.y===player.y){
      player.inventory.push(l.item);
      loot.splice(i,1);
      renderInventory();
      document.getElementById('status').textContent = 'Picked up ' + l.item + '.';
    }
  }
}
function attackNearest(){
  const target = creatures.filter(c=>!c.dead).find(c => Math.abs(c.x-player.x)+Math.abs(c.y-player.y) <= 1);
  if(target) attackCreature(target);
}
function attackCreature(c){
  if (c.dead) return;
  c.hp -= player.atk;
  document.getElementById('status').textContent = 'Hit ' + c.type + ' for ' + player.atk + '.';
  if (c.hp <= 0){
    c.dead = 200;
    player.xp += c.type==='wolf'?20:8;
    document.getElementById('xp').textContent = 'XP: ' + player.xp;
    c.loot.forEach(([item,count])=>{ loot.push({x:c.x,y:c.y,item}); });
    document.getElementById('status').textContent = 'Defeated ' + c.type + '.';
  }
}
function updateCreatures(){
  creatures.forEach(c=>{
    if(c.dead){ c.dead--; if(c.dead===0){ c.hp=c.maxHp; c.x=c.homeX; c.y=c.homeY; } return; }
    const dist = Math.abs(c.x-player.x)+Math.abs(c.y-player.y);
    if(c.type==='wolf' && dist<6){
      if(state.ticks%18===0){
        const dx = Math.sign(player.x-c.x), dy = Math.sign(player.y-c.y);
        const nx = c.x + (Math.abs(player.x-c.x) > Math.abs(player.y-c.y) ? dx : 0);
        const ny = c.y + (Math.abs(player.y-c.y) >= Math.abs(player.x-c.x) ? dy : 0);
        if(passable(nx,ny)){ c.x=nx; c.y=ny; }
      }
      if(dist<=1 && state.ticks%30===0){
        player.hp = Math.max(0, player.hp - c.atk);
        document.getElementById('status').textContent = 'A wolf bites you for ' + c.atk + '.';
      }
    } else if(state.ticks%50===0 && Math.random() < 0.4){
      const dirs = [[1,0],[-1,0],[0,1],[0,-1]];
      const [dx,dy] = dirs[Math.floor(Math.random()*dirs.length)];
      const nx=c.x+dx, ny=c.y+dy;
      const inTerritory = c.type==='wolf' ? ((c.homeX<60 && nx>=45&&nx<=68&&ny>=7&&ny<=20) || (c.homeX>=60 && nx>=50&&nx<=70&&ny>=24&&ny<=40)) : true;
      if(passable(nx,ny) && inTerritory){ c.x=nx; c.y=ny; }
    }
  });
  player.footprints.forEach(f=>f.life--);
  player.footprints = player.footprints.filter(f=>f.life>0);
}

function dayNightAlpha(){
  const t = (Math.sin(state.ticks/260)+1)/2; // 0..1
  return 0.08 + (1-t)*0.18;
}
function camera(){
  return { x: Math.max(0, Math.min(world.width - VIEW_W(), player.x - Math.floor(VIEW_W()/2))), y: Math.max(0, Math.min(world.height - VIEW_H(), player.y - Math.floor(VIEW_H()/2))) };
}
function worldToScreen(wx,wy){ const cam=camera(); return {sx:(wx-cam.x)*TILE, sy:(wy-cam.y)*TILE}; }
function screenToWorld(px,py){ const cam=camera(); return {wx:Math.floor(px/TILE)+cam.x, wy:Math.floor(py/TILE)+cam.y}; }
function drawTile(wx,wy){
  const {sx,sy}=worldToScreen(wx,wy);
  let color = '#355b2d';
  if (wy>=20 && wy<=32 && wx<22) color = '#496d30';
  if (wx>=pond.x1 && wx<=pond.x2 && wy>=pond.y1 && wy<=pond.y2) color = '#2a6fe8';
  if ((wx>=4&&wx<=42&&wy===26) || (wx===24&&wy>=18&&wy<=26) || (wx===36&&wy>=18&&wy<=26) || (wx===32&&wy>=26&&wy<=31) || (wx===46&&wy>=14&&wy<=26)) color = '#9a8458';
  ctx.fillStyle = color; ctx.fillRect(sx,sy,TILE,TILE);
}
function drawWorld(){
  const cam = camera();
  for(let y=cam.y;y<cam.y+VIEW_H()+1;y++){
    for(let x=cam.x;x<cam.x+VIEW_W()+1;x++) drawTile(x,y);
  }
  farms.forEach(f=>{
    for(let x=f.x1;x<=f.x2;x++) for(let y=f.y1;y<=f.y2;y++){
      const {sx,sy}=worldToScreen(x,y); ctx.fillStyle='#7c8f31'; ctx.fillRect(sx+4,sy+4,TILE-8,TILE-8);
    }
    for(let x=f.x1;x<=f.x2;x++){
      [[x,f.y1],[x,f.y2]].forEach(([xx,yy])=>{const {sx,sy}=worldToScreen(xx,yy); ctx.fillStyle='#c9b07d'; ctx.fillRect(sx,sy,TILE,4); ctx.fillRect(sx,sy+TILE-4,TILE,4);});
    }
    for(let y=f.y1;y<=f.y2;y++){
      [[f.x1,y],[f.x2,y]].forEach(([xx,yy])=>{const {sx,sy}=worldToScreen(xx,yy); ctx.fillStyle='#c9b07d'; ctx.fillRect(sx,sy,4,TILE); ctx.fillRect(sx+TILE-4,sy,4,TILE);});
    }
  });
  trees.forEach(t=>{ const {sx,sy}=worldToScreen(t.x,t.y); ctx.fillStyle='#174c21'; ctx.fillRect(sx+4,sy+2,24,20); ctx.fillStyle='#5b381b'; ctx.fillRect(sx+12,sy+18,8,12); });
  player.footprints.forEach(f=>{ const {sx,sy}=worldToScreen(f.x,f.y); ctx.fillStyle='rgba(180,180,180,'+(f.life/60)+')'; ctx.fillRect(sx+10,sy+22,4,4); ctx.fillRect(sx+18,sy+24,4,4); });
}
function drawPlayer(){
  const {sx,sy}=worldToScreen(player.x,player.y);
  // cloak/body
  ctx.fillStyle='#1f4aa8'; ctx.fillRect(sx+8,sy+6,16,22);
  ctx.fillStyle='#d6c6a3'; ctx.fillRect(sx+10,sy+2,12,8);
  ctx.fillStyle='#6d4a2b'; ctx.fillRect(sx+7,sy+28,6,4); ctx.fillRect(sx+19,sy+28,6,4);
  // sword
  ctx.fillStyle='#c7d2da';
  if(player.facing==='right') ctx.fillRect(sx+24,sy+12,8,3);
  else if(player.facing==='left') ctx.fillRect(sx,sy+12,8,3);
  else ctx.fillRect(sx+22,sy+14,6,2);
  // hp bar
  ctx.fillStyle='#111'; ctx.fillRect(sx, sy-8, TILE, 5); ctx.fillStyle='#30cc55'; ctx.fillRect(sx+1, sy-7, (TILE-2)*(player.hp/player.maxHp), 3);
}
function drawCreatures(){
  creatures.forEach(c=>{
    if(c.dead) return;
    const {sx,sy}=worldToScreen(c.x,c.y);
    if(c.type==='wolf'){
      ctx.fillStyle='#8b949e'; ctx.fillRect(sx+6,sy+10,20,12); ctx.fillStyle='#6f7780'; ctx.fillRect(sx+2,sy+12,8,8); ctx.fillRect(sx+22,sy+12,6,6);
    } else {
      ctx.fillStyle='#8b5a2b'; ctx.fillRect(sx+8,sy+10,16,14); ctx.fillStyle='#d2c08d'; ctx.fillRect(sx+18,sy+8,6,6);
    }
    ctx.fillStyle='#111'; ctx.fillRect(sx, sy-6, TILE, 4); ctx.fillStyle='#cc3333'; ctx.fillRect(sx+1, sy-5, (TILE-2)*(c.hp/c.maxHp), 2);
  });
}
function drawLoot(){
  loot.forEach(l=>{ const {sx,sy}=worldToScreen(l.x,l.y); ctx.fillStyle='#f4d35e'; ctx.fillRect(sx+12,sy+12,8,8); });
}
function drawNPCs(){
  npcs.forEach(n=>{ const {sx,sy}=worldToScreen(n.x,n.y); ctx.fillStyle='#7c5cff'; ctx.fillRect(sx+8,sy+6,16,20); ctx.fillStyle='#e5d4b4'; ctx.fillRect(sx+10,sy+2,12,8); ctx.fillStyle='white'; ctx.font='12px monospace'; ctx.fillText(n.name,sx-10,sy-4); });
}
function drawLabels(){
  const labels = [ ['Mirror Pond', 36, 26], ['Eastern Fields', 30, 10], ['Western Fields', 7, 10], ['Hearthvale Crossroads', 7, 22] ];
  labels.forEach(([name,x,y])=>{ const {sx,sy}=worldToScreen(x,y); ctx.fillStyle='rgba(0,0,0,.5)'; ctx.fillRect(sx-4,sy-16,ctx.measureText(name).width+10,18); ctx.fillStyle='white'; ctx.font='14px monospace'; ctx.fillText(name,sx,sy-4); });
}
function render(){
  ctx.clearRect(0,0,canvas.width,canvas.height);
  drawWorld(); drawLoot(); drawCreatures(); drawNPCs(); drawPlayer(); drawLabels();
  ctx.fillStyle = 'rgba(15,25,55,' + dayNightAlpha() + ')'; ctx.fillRect(0,0,canvas.width,canvas.height);
  document.getElementById('zone').textContent = 'Zone: ' + currentZone();
}
function loop(){ state.ticks++; updateCreatures(); render(); requestAnimationFrame(loop); }
renderInventory(); loop();
</script>
</body>
</html>`;
