/* Pixelverse — interactive hero: a WebGL2 particle field that assembles the wordmark.
   Every pixel is drawn as separate red, green and blue sub-pixels: they overlap into white at rest
   and split apart when disturbed. Built for phones too: adaptive quality, DPR cap, touch behaviour. */
(() => {
'use strict';

/* ───────── Edit these ───────── */
const CONFIG = {
  home: 'PIXELVERSE',
  stackOnPortrait: ['PIXEL', 'VERSE'],
  homeLine: 'Create what doesn’t exist.',
  homeSub: 'Visual storytelling meets creative technology.',
  homeTint: [1, 1, 1],
  modes: {
    vfx: { word: 'VFX', line: 'Simulation, compositing and the shots that can’t be filmed.', tint: [1.00, 0.52, 0.42], href: '/portfolio/#vfx', cta: 'Watch the VFX reel' },
    '3d':{ word: '3D',  line: 'Worlds modelled, lit and rendered from nothing.',                  tint: [0.46, 0.72, 1.00], href: '/portfolio/#3d',  cta: 'Watch the 3D reel' },
    ai:  { word: 'AI',  line: 'Generative imagery, directed like a shoot.',                        tint: [0.80, 0.52, 1.00], href: '/portfolio/#ai',  cta: 'Watch the AI reel' }
  }
};
/* ────────────────────────────── */

const hero   = document.getElementById('hero');
const canvas = document.getElementById('gl');
const tagEl  = document.getElementById('tag');
const subEl  = document.getElementById('sub');
const copyEl = document.getElementById('copy');
const modesEl= document.getElementById('modes');
const hintEl = document.getElementById('hint');
const RM     = matchMedia('(prefers-reduced-motion: reduce)').matches;
const COARSE = matchMedia('(hover: none)').matches;
const LOCKQ  = /[?&]lockq/.test(location.search);       // test switch: disable adaptive quality

const gl = canvas.getContext('webgl2', { alpha:false, antialias:false, powerPreference: COARSE ? 'default' : 'high-performance' });
if (!gl) { document.documentElement.classList.add('no-gl'); document.body.classList.add('ready'); return; }

/* ───────── shaders ───────── */
const VS = `#version 300 es
precision highp float;
layout(location=0) in vec4 a_p;   // x y z aux(seed + kind)
layout(location=1) in vec3 a_v;   // vx vy ramp
uniform vec2  u_res; uniform float u_dpr; uniform vec2 u_rot; uniform float u_F;
uniform float u_kick; uniform float u_sweep; uniform float u_size; uniform float u_time; uniform vec3 u_tint;
out vec3 v_col;
void main(){
  float ch   = float(gl_VertexID);            // 0 = red, 1 = green, 2 = blue sub-pixel
  float sgn  = ch - 1.0;
  float kind = floor(a_p.w);                  // 0 = word pixel, 1 = dust
  float seed = fract(a_p.w);
  vec3 p = a_p.xyz;
  float cy=cos(u_rot.y), sy=sin(u_rot.y), cx=cos(u_rot.x), sx=sin(u_rot.x);
  vec3 q = vec3(cy*p.x + sy*p.z, p.y, -sy*p.x + cy*p.z);
  q = vec3(q.x, cx*q.y - sx*q.z, sx*q.y + cx*q.z);
  float s = u_F / (u_F + q.z);
  vec2 scr = q.xy * s;
  float sp = length(a_v.xy);
  scr += (a_v.xy * 0.95 * sgn + normalize(q.xy + vec2(0.001)) * u_kick * 11.0 * sgn * (0.4 + seed)) * s;
  gl_Position = vec4(scr.x/(u_res.x*0.5), -scr.y/(u_res.y*0.5), 0.0, 1.0);
  gl_PointSize = u_size * s * (kind > 0.5 ? (0.75 + seed*1.1) : 1.0) * u_dpr;
  vec3 base = ch < 0.5 ? vec3(1.0,0.10,0.30) : (ch < 1.5 ? vec3(0.10,1.0,0.55) : vec3(0.25,0.45,1.0));
  float b;
  if (kind > 0.5) {
    b = (0.30 + 0.25*sin(u_time*(0.4+seed*1.6) + seed*40.0)) * (0.55 + 0.45*clamp(s,0.0,1.2));
  } else {
    float band = exp(-pow((p.x - u_sweep)/70.0, 2.0));
    b = (0.82 + band*1.1) * (0.28 + 0.72*a_v.z);
  }
  b *= 1.0 + min(sp*0.07, 1.5);
  v_col = base * u_tint * b;
}`;
const FS = `#version 300 es
precision mediump float;
in vec3 v_col; uniform float u_core; uniform float u_fade; out vec4 o;
void main(){
  vec2 q = gl_PointCoord*2.0-1.0; float d = max(abs(q.x),abs(q.y));
  float core = 1.0 - smoothstep(u_core*0.82, u_core, d);
  float halo = pow(max(0.0,1.0-d), 2.6) * 0.20;
  o = vec4(v_col*(core+halo)*u_fade, 1.0);
}`;
function sh(type, src){ const s=gl.createShader(type); gl.shaderSource(s,src); gl.compileShader(s);
  if(!gl.getShaderParameter(s,gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(s)); return s; }
let prog;
try {
  prog = gl.createProgram();
  gl.attachShader(prog, sh(gl.VERTEX_SHADER, VS)); gl.attachShader(prog, sh(gl.FRAGMENT_SHADER, FS));
  gl.linkProgram(prog);
  if(!gl.getProgramParameter(prog,gl.LINK_STATUS)) throw new Error(gl.getProgramInfoLog(prog));
} catch (e) { document.documentElement.classList.add('no-gl'); document.body.classList.add('ready'); return; }
gl.useProgram(prog);
const U = {}; ['u_res','u_dpr','u_rot','u_F','u_kick','u_sweep','u_size','u_time','u_tint','u_core','u_fade']
  .forEach(n => U[n] = gl.getUniformLocation(prog, n));

/* ───────── particle store ───────── */
const small = Math.min(innerWidth, innerHeight) < 620;
const NF = small ? 8500 : (COARSE ? 12000 : 18000);   // pixels that form the word
const ND = small ? 1000 : (COARSE ? 1600 : 2600);     // ambient dust
const N  = NF + ND;
const F  = 1800;
const P  = new Float32Array(N*3), V = new Float32Array(N*3), Tg = new Float32Array(N*3);
const delay = new Float32Array(N), stiff = new Float32Array(N), seedA = new Float32Array(N), switchAt = new Float32Array(N);
const dBase = new Float32Array(ND*3), dPh = new Float32Array(ND*3);
const STRIDE = 7, inst = new Float32Array(N*STRIDE);
let NFa = NF, NDa = ND;                                 // active counts (adaptive quality)

const vao = gl.createVertexArray(); gl.bindVertexArray(vao);
const buf = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, buf);
gl.bufferData(gl.ARRAY_BUFFER, inst.byteLength, gl.DYNAMIC_DRAW);
gl.enableVertexAttribArray(0); gl.vertexAttribPointer(0,4,gl.FLOAT,false,STRIDE*4,0);  gl.vertexAttribDivisor(0,1);
gl.enableVertexAttribArray(1); gl.vertexAttribPointer(1,3,gl.FLOAT,false,STRIDE*4,16); gl.vertexAttribDivisor(1,1);
gl.disable(gl.DEPTH_TEST); gl.enable(gl.BLEND); gl.blendFunc(gl.ONE, gl.ONE);
gl.clearColor(5/255, 6/255, 11/255, 1);

/* ───────── layout + word → point targets ───────── */
let W=0, H=0, DPR=1, DPRCAP = COARSE ? 1.5 : 2, cyOff=0;
let modeTargets = {};
const maskCv = document.createElement('canvas');
const mctx = maskCv.getContext('2d', { willReadFrequently:true });
const FONT = 'PVSyne, "Arial Black", Impact, sans-serif';

function buildTargets(lines, maxW, maxH){
  const BASE = 280;
  mctx.font = `800 ${BASE}px ${FONT}`;
  const capH = mctx.measureText('H').actualBoundingBoxAscent || BASE*0.7;
  let lw = 0; lines.forEach(t => lw = Math.max(lw, mctx.measureText(t).width));
  const gap = capH * 1.2, totalH = capH + (lines.length-1)*gap, pad = 24;
  const cw = Math.ceil(lw + pad*2), ch = Math.ceil(totalH + pad*2);
  maskCv.width = cw; maskCv.height = ch;
  mctx.font = `800 ${BASE}px ${FONT}`;
  mctx.fillStyle = '#fff'; mctx.textAlign = 'center'; mctx.textBaseline = 'alphabetic';
  lines.forEach((t,i) => mctx.fillText(t, cw/2, pad + capH + i*gap));
  const d = mctx.getImageData(0,0,cw,ch).data;
  let cnt = 0; for (let i=3;i<d.length;i+=4) if (d[i] > 150) cnt++;
  const idx = new Int32Array(cnt); let k = 0; for (let i=0,j=3;j<d.length;i++,j+=4) if (d[j] > 150) idx[k++] = i;
  const s = Math.min(maxW/lw, maxH/totalH);
  const out = new Float32Array(NF*3);
  for (let i=0;i<NF;i++){
    const id = idx[(Math.random()*cnt)|0];
    const mx = (id % cw) + Math.random(), my = ((id / cw)|0) + Math.random();
    const z  = (Math.random()+Math.random()+Math.random()-1.5) * 60;
    const k3 = (F + z) / F;
    out[i*3]   = (mx - cw/2) * s * k3;
    out[i*3+1] = (my - ch/2) * s * k3 + cyOff;
    out[i*3+2] = z;
  }
  return { pts: out, h: totalH * s };
}

function sizeCanvas(){
  DPR = Math.min(window.devicePixelRatio || 1, DPRCAP);
  canvas.width = Math.round(W*DPR); canvas.height = Math.round(H*DPR);
  gl.viewport(0,0,canvas.width,canvas.height);
}
function layout(){
  const r = hero.getBoundingClientRect();
  W = Math.max(300, r.width); H = Math.max(360, r.height);
  sizeCanvas();
  cyOff = -H * 0.07;
  const portrait = W / H < 0.85;
  const homeLines = portrait ? CONFIG.stackOnPortrait : [CONFIG.home];
  const home = buildTargets(homeLines, Math.min(W*(portrait ? 0.88 : 0.80), 1280), H*(portrait ? 0.36 : 0.30));
  modeTargets = { home: home.pts };
  let tallest = home.h;
  for (const key in CONFIG.modes){
    const m = buildTargets([CONFIG.modes[key].word], W*(portrait ? 0.80 : 0.56), Math.min(H*0.34, 300));
    modeTargets[key] = m.pts; tallest = Math.max(tallest, m.h);
  }
  copyEl.style.setProperty('--copy-top', (H/2 + cyOff + tallest/2 + Math.max(26, H*0.04)) + 'px');
}

/* ───────── interaction state ───────── */
const mouse = { x:0, y:0, tx:0, ty:0, speed:0, real:false, lastMove:-99 };
const tilt  = { x:0, y:0, gx:0, gy:0 };
const bursts = [];
let mode = 'home', kick = 0, tint = CONFIG.homeTint.slice(), tintGoal = CONFIG.homeTint.slice();
let sweepStart = 1e9, ready = false, tStart = performance.now()/1000, pending = null, revertTimer = 0, last = 0, visible = true;
const now = () => performance.now()/1000 - tStart;

function setSub(m){
  if (COARSE && m !== 'home') {
    const c = CONFIG.modes[m];
    subEl.innerHTML = '<a href="' + c.href + '">' + c.cta + '</a>';
  } else subEl.textContent = CONFIG.homeSub;
}
function setMode(m, t){
  if (m === mode) return;
  mode = m;
  pending = modeTargets[m] || modeTargets.home;
  for (let i=0;i<NF;i++) switchAt[i] = t + Math.random()*0.38;
  kick = 1;
  tintGoal = (m === 'home') ? CONFIG.homeTint : CONFIG.modes[m].tint;
  bursts.push({ x:0, y:cyOff, t0:t, power:0.8 });
  tagEl.classList.add('swap');
  setTimeout(() => { tagEl.textContent = (m === 'home') ? CONFIG.homeLine : CONFIG.modes[m].line; setSub(m); tagEl.classList.remove('swap'); }, 190);
  modesEl.querySelectorAll('.btn').forEach(a => a.classList.toggle('on', a.dataset.mode === m));
}

modesEl.querySelectorAll('.btn').forEach(a => {
  if (COARSE) {
    // touch: first tap morphs the cloud and offers the link; tap the chip again to go
    a.addEventListener('click', e => { if (mode !== a.dataset.mode) { e.preventDefault(); setMode(a.dataset.mode, now()); } });
  } else {
    const on  = () => { clearTimeout(revertTimer); setMode(a.dataset.mode, now()); };
    const off = () => { clearTimeout(revertTimer); revertTimer = setTimeout(() => setMode('home', now()), 180); };
    a.addEventListener('pointerenter', on); a.addEventListener('pointerleave', off);
    a.addEventListener('focus', on);        a.addEventListener('blur', off);
  }
});
if (COARSE && hintEl) hintEl.textContent = 'Touch the pixels. Tap to break them.';

function toLocal(e){ const r = canvas.getBoundingClientRect(); return [e.clientX - r.left - r.width/2, e.clientY - r.top - r.height/2]; }
addEventListener('pointermove', e => {
  const [x,y] = toLocal(e); mouse.tx = x; mouse.ty = y; mouse.real = true; mouse.lastMove = now();
  tilt.gx = x / (W/2); tilt.gy = y / (H/2);
}, { passive:true });
document.addEventListener('pointerleave', () => { mouse.real = false; });
canvas.addEventListener('pointerdown', e => {
  const [x,y] = toLocal(e); bursts.push({ x, y, t0: now(), power:1 }); kick = Math.max(kick, 0.7);
  if (COARSE && mode !== 'home') setMode('home', now());
});
document.addEventListener('visibilitychange', () => { if (!document.hidden) last = now(); });
new IntersectionObserver(es => { visible = es[0].isIntersecting; if (visible) last = now(); }).observe(hero);

let resizeT = 0, lastW = innerWidth;
addEventListener('resize', () => { clearTimeout(resizeT); resizeT = setTimeout(() => {
  // mobile browsers fire resize as the address bar collapses; only rebuild on a real width change
  if (Math.abs(innerWidth - lastW) < 40 && Math.abs(hero.getBoundingClientRect().height - H) < 120) { return; }
  lastW = innerWidth;
  layout(); pending = modeTargets[mode] || modeTargets.home;
  const t = now(); for (let i=0;i<NF;i++) switchAt[i] = t + Math.random()*0.2;
}, 200); });

/* ───────── adaptive quality ───────── */
const QL = [1, 0.75, 0.55, 0.4]; let ql = 0, accT = 0, accN = 0;
function adapt(dt){
  if (LOCKQ || !ready || ql >= QL.length-1) return;
  accT += dt; accN++;
  if (accN < 80) return;
  const avg = accT / accN; accT = 0; accN = 0;
  if (avg > 0.029) {                                    // under ~35 fps: shed particles
    ql++; NFa = Math.floor(NF*QL[ql]); NDa = Math.floor(ND*QL[ql]);
    if (ql >= 2 && DPRCAP > 1.25) { DPRCAP = 1.25; sizeCanvas(); }
  }
}

/* ───────── simulation ───────── */
function spawn(){
  const sp = (a) => (Math.random()-0.5)*a;
  for (let i=0;i<NF;i++){
    const i3 = i*3;
    if (RM){ P[i3]=modeTargets.home[i3]; P[i3+1]=modeTargets.home[i3+1]; P[i3+2]=modeTargets.home[i3+2]; }
    else { P[i3]=sp(W*1.9); P[i3+1]=sp(H*1.9); P[i3+2]=-700 + Math.random()*1100; }
    Tg[i3]=modeTargets.home[i3]; Tg[i3+1]=modeTargets.home[i3+1]; Tg[i3+2]=modeTargets.home[i3+2];
    delay[i] = RM ? -1 : 0.25 + Math.random()*1.25;
    stiff[i] = 0.030 + Math.random()*0.040;
    seedA[i] = Math.random();
  }
  for (let j=0;j<ND;j++){
    const i = NF+j, i3=i*3, j3=j*3;
    dBase[j3]=sp(W*1.7); dBase[j3+1]=sp(H*1.7); dBase[j3+2]=-650 + Math.random()*1100;
    dPh[j3]=Math.random()*6.28; dPh[j3+1]=Math.random()*6.28; dPh[j3+2]=Math.random()*6.28;
    P[i3]=dBase[j3]; P[i3+1]=dBase[j3+1]; P[i3+2]=dBase[j3+2];
    delay[i]=-1; stiff[i]=0.006; seedA[i]=Math.random();
  }
}

function step(t, dt){
  const f = Math.min(dt*60, 2.2);
  let ghost = false;
  if (!RM && (!mouse.real || t - mouse.lastMove > 3.5) && ready){
    ghost = true;
    mouse.tx = Math.cos(t*0.42) * W*0.27;
    mouse.ty = cyOff + Math.sin(t*0.71) * H*0.07;
  }
  const px = mouse.x, py = mouse.y;
  mouse.x += (mouse.tx - mouse.x) * Math.min(1, 0.32*f);
  mouse.y += (mouse.ty - mouse.y) * Math.min(1, 0.32*f);
  const rawSp = Math.hypot(mouse.x-px, mouse.y-py) / f;
  mouse.speed += (rawSp - mouse.speed) * 0.2;
  const mx = mouse.x, my = mouse.y;
  const R  = Math.max(70, Math.min(175, Math.min(W,H)*0.15)), R2 = R*R;
  const push  = (ghost ? 1.05 : 1.7) + Math.min(mouse.speed, 40)*0.11;
  const swirl = 0.9;

  const gx = ghost ? Math.cos(t*0.42)*0.5 : tilt.gx, gy = ghost ? Math.sin(t*0.71)*0.3 : tilt.gy;
  tilt.x += ((-gy*0.07) - tilt.x) * 0.04*f;
  tilt.y += (( gx*0.12) - tilt.y) * 0.04*f;

  for (let b = bursts.length-1; b >= 0; b--) if (t - bursts[b].t0 > 1.5) bursts.splice(b,1);

  const damp = 1 - 0.16*f;
  for (let i=0;i<NFa;i++){
    const i3 = i*3;
    if (switchAt[i] > 0 && t >= switchAt[i]){ Tg[i3]=pending[i3]; Tg[i3+1]=pending[i3+1]; Tg[i3+2]=pending[i3+2]; switchAt[i]=0; }
    let r = (t - delay[i]) / 0.9; r = r < 0 ? 0 : r > 1 ? 1 : r; r = r*r*(3-2*r);
    const k = stiff[i] * r;
    let vx = V[i3], vy = V[i3+1], vz = V[i3+2];
    let x = P[i3], y = P[i3+1], z = P[i3+2];
    vx += (Tg[i3]-x)*k*f; vy += (Tg[i3+1]-y)*k*f; vz += (Tg[i3+2]-z)*k*f;
    if (r > 0.35){
      const dx = x-mx, dy = y-my, d2 = dx*dx+dy*dy;
      if (d2 < R2){
        const d = Math.sqrt(d2)+0.001, q = 1-d/R, qq = q*q;
        vx += (dx/d*push - dy/d*swirl)*qq*f; vy += (dy/d*push + dx/d*swirl)*qq*f;
        vz += (seedA[i]-0.5)*push*qq*8*f;
      }
      for (let b=0;b<bursts.length;b++){
        const B = bursts[b], age = t-B.t0, ring = age*1250;
        const bx = x-B.x, by = y-B.y, bd = Math.sqrt(bx*bx+by*by)+0.001, e = Math.abs(bd-ring);
        if (e < 70){
          const a = (1 - e/70) * (1 - age/1.5) * 3.4 * B.power * (0.6+seedA[i]*0.8);
          vx += bx/bd*a*f; vy += by/bd*a*f; vz += (seedA[i]-0.5)*a*10*f;
        }
      }
    }
    vx *= damp; vy *= damp; vz *= damp;
    P[i3]=x+vx*f; P[i3+1]=y+vy*f; P[i3+2]=z+vz*f; V[i3]=vx; V[i3+1]=vy; V[i3+2]=vz;
    const o = i*STRIDE;
    inst[o]=P[i3]; inst[o+1]=P[i3+1]; inst[o+2]=P[i3+2]; inst[o+3]=seedA[i];
    inst[o+4]=vx; inst[o+5]=vy; inst[o+6]=r;
  }
  for (let j=0;j<NDa;j++){
    const i = NF+j, i3=i*3, j3=j*3;
    const tx = dBase[j3]   + Math.sin(t*0.13+dPh[j3])*70;
    const ty = dBase[j3+1] + Math.cos(t*0.11+dPh[j3+1])*55;
    const tz = dBase[j3+2] + Math.sin(t*0.09+dPh[j3+2])*90;
    let vx=V[i3], vy=V[i3+1], vz=V[i3+2], x=P[i3], y=P[i3+1], z=P[i3+2];
    vx += (tx-x)*0.006*f; vy += (ty-y)*0.006*f; vz += (tz-z)*0.006*f;
    const dx = x-mx, dy = y-my, d2 = dx*dx+dy*dy;
    if (d2 < R2*1.4){ const d=Math.sqrt(d2)+0.001, q=1-d/(R*1.18); if(q>0){ const qq=q*q; vx += (dx/d*push*0.7 - dy/d*swirl)*qq*f; vy += (dy/d*push*0.7 + dx/d*swirl)*qq*f; } }
    for (let b=0;b<bursts.length;b++){
      const B = bursts[b], age=t-B.t0, ring=age*1250, bx=x-B.x, by=y-B.y, bd=Math.sqrt(bx*bx+by*by)+0.001, e=Math.abs(bd-ring);
      if (e < 90){ const a=(1-e/90)*(1-age/1.5)*2.2*B.power; vx+=bx/bd*a*f; vy+=by/bd*a*f; }
    }
    const dd = 1 - 0.07*f; vx*=dd; vy*=dd; vz*=dd;
    P[i3]=x+vx*f; P[i3+1]=y+vy*f; P[i3+2]=z+vz*f; V[i3]=vx; V[i3+1]=vy; V[i3+2]=vz;
    const o = (NFa+j)*STRIDE;
    inst[o]=P[i3]; inst[o+1]=P[i3+1]; inst[o+2]=P[i3+2]; inst[o+3]=1+seedA[NF+j];
    inst[o+4]=vx; inst[o+5]=vy; inst[o+6]=1;
  }
}

function draw(t){
  for (let c=0;c<3;c++) tint[c] += (tintGoal[c]-tint[c])*0.07;
  kick *= 0.94;
  let sweep = -99999;
  if (!RM && ready){
    const age = t - sweepStart;
    if (age >= 0 && age < 1.8) sweep = (-0.62 + (age/1.8)*1.24) * Math.min(W*0.8,1280);
    else if (age >= 9.5) sweepStart = t;
  }
  gl.clear(gl.COLOR_BUFFER_BIT);
  gl.uniform2f(U.u_res, W, H); gl.uniform1f(U.u_dpr, DPR); gl.uniform2f(U.u_rot, tilt.x, tilt.y);
  gl.uniform1f(U.u_F, F); gl.uniform1f(U.u_kick, kick); gl.uniform1f(U.u_sweep, sweep);
  // phones: slightly larger pixels, and compensate when the quality governor has thinned the cloud
  const base = small ? Math.max(1.5, W/430) : W/760;
  const coreCss = Math.max(1.35, Math.min(2.1, base)) * Math.pow(NF/NFa, 0.35), pointCss = coreCss*3.4;
  gl.uniform1f(U.u_size, pointCss); gl.uniform1f(U.u_core, coreCss/pointCss);
  gl.uniform1f(U.u_time, t); gl.uniform3f(U.u_tint, tint[0], tint[1], tint[2]);
  gl.uniform1f(U.u_fade, RM ? 1 : Math.min(1, t/0.9));
  const used = (NFa+NDa)*STRIDE;
  gl.bufferSubData(gl.ARRAY_BUFFER, 0, inst, 0, used);
  gl.drawArraysInstanced(gl.POINTS, 0, 3, NFa+NDa);
}

function frame(){
  requestAnimationFrame(frame);
  if (!visible || document.hidden) return;
  const t = now(), dt = Math.min(0.05, Math.max(0.001, t - last)); last = t;
  step(t, dt); draw(t); adapt(dt);
  if (!ready && t > (RM ? 0.1 : 2.3)){ ready = true; document.body.classList.add('ready'); sweepStart = t + 0.4; }
}
canvas.addEventListener('webglcontextlost', e => { e.preventDefault(); document.documentElement.classList.add('no-gl'); document.body.classList.add('ready'); });

async function init(){
  try { await Promise.race([ document.fonts.load('800 100px PVSyne'), new Promise(r => setTimeout(r, 1500)) ]); } catch(e){}
  layout(); spawn(); pending = modeTargets.home;
  tStart = performance.now()/1000; last = 0;
  window.__pv = { setMode: (m) => setMode(m, now()), burst: (x,y) => bursts.push({x,y,t0:now(),power:1}), get ready(){ return ready; }, get quality(){ return ql; } };
  requestAnimationFrame(frame);
}
init();
})();
