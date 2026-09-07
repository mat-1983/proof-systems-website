/* Execute production scene functions with controlled layout geometry.
 * This checks behaviour and mode changes, not browser rendering or physical touch. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const source = fs.readFileSync(path.join(__dirname, '../assets/js/site.js'), 'utf8');
const names = ['clamp', 'phase', 'ease', 'progressThrough', 'setPath', 'renderOpening', 'clearTrackLayout', 'measureTracks', 'trackProgress', 'visibleStage', 'renderDepth', 'renderTracks', 'syncMotionMode'];
const functions = names.map(name => {
  const match = source.match(new RegExp('^  function ' + name + '\\([^]*?(?=^  function |^  if \\(|^  window\\.)', 'm'));
  assert(match, 'Production function missing: ' + name);
  return match[0];
}).join('\n');
function style() {
  return {
    setProperty(key,value) {this[key]=value;},
    removeProperty(key) {delete this[key];}
  };
}
function classList() {
  return { toggle(key,value) {this[key]=value;}, remove(key) {delete this[key];} };
}
function fixture(kind, viewport, heights, flow=false) {
  const variables = style();
  let offset = 0;
  const connection = kind === 'connection';
  const panelHeights = Array.isArray(heights) ? heights : [heights,heights,heights,heights];
  const flowHeight = panelHeights.reduce((sum,height)=>sum+height, 0)+60;
  const parent = {
    get offsetHeight() {return context.flowQuery.matches || context.reducedQuery.matches ? flowHeight : parseFloat(variables['--panels-height']) || Math.max(...panelHeights);},
    getBoundingClientRect() {return {top:72-offset};}
  };
  const panels = connection ? [] : panelHeights.map((height,index) => ({
    offsetHeight:height, parentElement:parent, style:style(), classList:classList(),
    getBoundingClientRect() {
      const top=72-offset+panelHeights.slice(0,index).reduce((sum,h)=>sum+h+20,0);
      return {top,bottom:top+height};
    }
  }));
  const inner = {get offsetHeight() {return parent.offsetHeight+90;}};
  const stage = {get offsetHeight() {return parseFloat(variables['--stage-height']) || viewport-72;},querySelector:()=>inner};
  const indicators = panels.map(()=>({classList:classList()}));
  const thread = {style:style()};
  const light = {style:style()};
  const board = {style:style(), offsetHeight:panelHeights[0], getBoundingClientRect() {return {top:72-offset};}};
  const layer = {style:style()};
  const outcome = {style:style()};
  const caption = {};
  const wires = ['left','right','out'].map(wire=>({style:style(),dataset:{wire}}));
  const nodes = {'.scroll-stage':stage,'.stage-panels':parent,'.story-thread i':thread,'.process-light':kind==='process'?light:null,
    '.connection-board':board,'.connection-layer':layer,'.connection-outcome':outcome,'.connection-caption':caption};
  const track = {
    dataset:{scrollTrack:kind},style:variables,attrs:{},
    setAttribute(key,value){this.attrs[key]=value;}, removeAttribute(key){delete this.attrs[key];},
    get offsetHeight(){return context.flowQuery.matches || context.reducedQuery.matches ? (connection?board.offsetHeight:flowHeight)+40 : stage.offsetHeight+parseFloat(variables['--scroll-travel']);},
    getBoundingClientRect(){return {top:72-offset};},
    querySelector(selector){return nodes[selector] || null;},
    querySelectorAll(selector){
      if(selector==='[data-stage-panel]') return panels;
      if(selector==='[data-stage-indicator]') return indicators;
      if(selector==='.connection-wire') return connection?wires:[];
      return [...panels,thread,light,...(connection?[board,layer,outcome]:[])];
    }
  };
  const context = {tracks:[track],reducedQuery:{matches:false},flowQuery:{matches:flow},story:{setAttribute(){}},nav:{offsetHeight:72},
    viewportProbe:{offsetHeight:viewport},window:{innerHeight:viewport},needsMeasure:true,
    document:{documentElement:{classList:classList()},querySelectorAll:()=>[]},
    getComputedStyle(){return {paddingTop:'16',paddingBottom:'64',top:'72'};},
    measureWires(){}, render(){context.measureTracks();context.renderTracks();}};
  vm.createContext(context);vm.runInContext(functions,context);context.syncMotionMode();
  return {context,panels,variables,track,parent,board,layer,outcome,wires,caption,
    setProgress(value){offset=value*(track.offsetHeight-stage.offsetHeight);context.renderTracks();},
    scrollTo(value){offset=value;context.renderTracks();},
    setMode(mobile,reduced=false){context.flowQuery.matches=mobile;context.reducedQuery.matches=reduced;context.syncMotionMode();}
  };
}
for(const kind of ['story','process']) {
  for(const [height,natural] of [[900,470],[1024,580],[1146,470],[1600,470],[844,420],[600,450],[500,440],[480,490],[390,270]]) {
    const f=fixture(kind,height,natural);
    assert.equal(parseFloat(f.variables['--stage-height']),height-72,'Desktop stage fits beneath navigation');
    assert.equal(parseFloat(f.variables['--panels-height']),Math.min(natural,Math.max(80,height-72-170)),'Cue/indicator space is included in overflow reading');
    const overflow=Math.max(0,natural-f.parent.offsetHeight);
    const perCardTravel=parseFloat(f.variables['--scroll-travel'])/4;
    if(!overflow) assert(perCardTravel<=420,'Normal desktop travel is capped independently of monitor height');
    else assert(perCardTravel*.42>=overflow,'Overflow reading retains at least one scroll pixel per panned pixel');
    const snapshots=[];
    for(let i=0;i<4;i++) {
      f.setProgress((i+.24)/4);
      assert.equal(f.panels[i].style.opacity,'1');
      assert.equal(f.panels[i].style.transform,'translateY(0px)','Incoming heading remains readable');
      f.setProgress((i+.71)/4);
      assert.equal(f.panels[i].style.transform,`translateY(${-Math.max(0,natural-f.parent.offsetHeight)}px)`,'Full panel bottom is exposed before exit');
      snapshots.push(f.panels.map(p=>({...p.style})));
    }
    for(let i=3;i>=0;i--) {
      f.setProgress((i+.71)/4);
      assert.deepEqual(f.panels.map(p=>({...p.style})),snapshots[i],'Reverse scroll restores desktop state');
    }
    const travel=f.variables['--scroll-travel'];
    f.context.window.innerHeight+=70;f.context.measureTracks();
    assert.equal(f.variables['--scroll-travel'],travel,'Toolbar changes do not alter desktop travel');
    for(const reduced of [false,true]) {
      f.setMode(true,reduced);
      for(const key of ['--stage-height','--stage-top','--scroll-travel','--panels-height']) assert.equal(f.variables[key],undefined,'Ordinary flow has no artificial geometry');
      for(const panel of f.panels) {
        assert.equal(panel.style.transform,undefined,'Old desktop transforms are cleared');
        assert.equal(panel.style.opacity,undefined,'All flow narrative is visible');
      }
      f.scrollTo(380);
      for(const panel of f.panels) assert.equal(panel.style.transform,undefined,'Native scrolling never counter-translates flow cards');
      if(reduced) {
        assert.equal(f.track.attrs['data-progress'],'1.0000');
        assert.equal(f.variables['--flow-depth'],undefined,'Reduced Motion clears moving decoration');
        for(const key of ['--depth-x','--depth-y','--route-progress']) assert.equal(f.variables[key],undefined,'Reduced Motion clears brand artwork motion and route state');
      }
    }
    f.setMode(false);
    assert(f.variables['--scroll-travel'],'Returning to desktop measures its stage again');
    assert.equal(f.variables['--flow-progress'],undefined,'Returning to desktop removes flow decoration state');
    f.setMode(false,true);
    for(const panel of f.panels) assert.equal(panel.style.opacity,undefined,'Desktop Reduced Motion restores complete flow after active staging');
  }
  // Measure the fully stationary interval in the actual production transition, in scroll pixels.
  for(const viewport of [900,1146,1600]) {
    const pacing=fixture(kind,viewport,470);
    const step=parseFloat(pacing.variables['--scroll-travel'])/4;
    let stationary=0;
    for(let pixel=0;pixel<=step;pixel++) {
      pacing.setProgress((1+pixel/step)/4);
      if(pacing.panels[1].style.opacity==='1' && pacing.panels[1].style.transform==='translateY(0px)') stationary++;
    }
    assert(stationary<=211,'Normal middle-card stationary interval is at most210px plus sampling tolerance');
    assert(stationary>=180,'Shorter pacing retains a usable reading interval');
    let faintHandover=0;
    for(let pixel=0;pixel<=step;pixel++) {
      pacing.setProgress((.5+pixel/step)/4);
      const visible=pacing.panels.filter(panel=>Number(panel.style.opacity)>.001);
      assert(visible.length<=1,'Desktop handover never superimposes outgoing and incoming copy');
      if(pacing.panels.every(panel=>Number(panel.style.opacity)<.2)) faintHandover++;
    }
    assert(faintHandover<=32,'Clean handover has no prolonged empty interval');
  }
  const depth=fixture(kind,844,[330,350,330,360],true);
  depth.scrollTo(0);
  const initial={x:parseFloat(depth.variables['--depth-x']),y:parseFloat(depth.variables['--depth-y']),route:Number(depth.variables['--route-progress'])};
  depth.scrollTo(380);
  assert(parseFloat(depth.variables['--depth-x'])-initial.x>40,'One ordinary swipe produces clearly visible diagonal artwork movement');
  assert(initial.y-parseFloat(depth.variables['--depth-y'])>50,'Backdrop movement is materially stronger than the previous32px total');
  assert(initial.y-parseFloat(depth.variables['--depth-y'])<380,'Pinned decoration travels more slowly than native foreground');
  assert(Number(depth.variables['--route-progress'])>initial.route,'Amber route progresses with real scrolling');
  depth.scrollTo(0);
  assert.equal(parseFloat(depth.variables['--depth-x']),initial.x,'Reverse scrolling restores artwork exactly');
  assert.equal(parseFloat(depth.variables['--depth-y']),initial.y);
  depth.setMode(false,true);
  for(const key of ['--depth-x','--depth-y','--route-progress']) assert.equal(depth.variables[key],undefined);
  // Unequal cards deliberately prevent synthetic quartiles from matching the real reading position.
  const f=fixture(kind,844,[220,800,250,350],true);
  const readingOffset=(844-72)*.38;
  for(const [index,start,height] of [[0,0,220],[1,240,800],[2,1060,250],[3,1330,350]]) {
    f.scrollTo(start+height*.5-readingOffset);
    assert.equal(f.track.attrs['data-active-stage'],String(index+1),'Active stage follows the real card at the reading line');
    assert(f.panels[index].classList['is-current']);
  }
}
for(const [viewport,boardHeight] of [[844,430],[480,470],[390,270],[1024,550]]) {
  const f=fixture('connection',viewport,boardHeight);
  f.setProgress(.65);
  assert(f.board.style.transform,'Desktop overflow state exists before switching');
  f.setMode(true);
  assert.equal(f.board.style.transform,undefined);
  assert.equal(f.layer.style.opacity,undefined);
  assert.equal(f.outcome.style.opacity,undefined);
  // Drawing finishes while the entire short board fits; for tall boards before its top exits.
  const arrivalTop=Math.max(72,viewport-boardHeight);
  f.scrollTo(72-arrivalTop);
  for(const wire of f.wires) assert.equal(wire.style.strokeDashoffset,'0','Complete connection is drawn on arrival');
  assert.equal(f.board.style.transform,undefined,'Mobile diagram travels without counter-translation');
  f.scrollTo(72-viewport+40);
  assert(Number(f.wires[2].style.strokeDashoffset)>0,'Reverse scroll unwinds connections');
  f.setMode(true,true);
  for(const wire of f.wires) assert.equal(wire.style.strokeDashoffset,'0');
  assert.equal(f.layer.style.opacity,undefined,'Reduced Motion retains all diagram copy');
}
// Drive the real opening with a 40svh journey, preserving its five-node logo geometry.
{
  let offset=0;
  const element=()=>({style:style(),attrs:{},setAttribute(key,value){this.attrs[key]=value;}});
  const main=element(); main.classList={contains:name=>name==='v2-mark-main'};
  const branches=[element(),element()];
  branches.forEach((branch,index)=>branch.classList={contains:name=>name==='v2-mark-branch-one' && index===0});
  const mark=element(),svg=element(),outline=element(),name=element();
  const nodes=Array.from({length:5},element),lines=Array.from({length:3},element);
  const selectors={'.v2-opening-sticky':{offsetHeight:844},'.v2-opening-mark-wrap':mark,'.v2-opening-mark':svg,
    '.v2-mark-outline':outline,'.v2-mark-main':main,'.v2-opening-name':name};
  const opening={...element(),offsetHeight:844*1.4,getBoundingClientRect:()=>({top:-offset}),
    querySelector:selector=>selectors[selector]||null,
    querySelectorAll:selector=>selector==='.v2-mark-branch'?branches:selector==='.v2-mark-node'?nodes:lines};
  const context={opening,reducedQuery:{matches:false},window:{innerHeight:844}};
  vm.createContext(context);vm.runInContext(functions,context);
  context.renderOpening();const before=main.style.strokeDashoffset;
  offset=20;context.renderOpening();
  assert(Number(main.style.strokeDashoffset)<Number(before),'The first 20px of scroll visibly draws connections');
  let previous=lines.map(()=>0);
  for(const progress of [.25,.5,.75,.97,1]) {
    offset=progress*(opening.offsetHeight-844);context.renderOpening();
    lines.forEach((line,index)=>{
      assert(Number(line.style.opacity)>=previous[index],'Words progressively appear without reversing during forward scroll');
      previous[index]=Number(line.style.opacity);
    });
  }
  for(const line of lines) assert.equal(line.style.opacity,'1','All opening words are fully visible before the scene ends');
  assert.equal(main.attrs.d,'M108.00 200.00 L168.00 268.00 L304.00 132.00','Approved five-node geometry is retained');
  assert.equal(branches[0].attrs.d,'M148.00 132.00 L168.00 268.00');
  assert.equal(branches[1].attrs.d,'M252.00 228.00 L168.00 268.00');
  context.reducedQuery.matches=true;offset=0;context.renderOpening();
  for(const line of lines) assert.equal(line.style.opacity,'1','Reduced Motion has the complete opening');
}
const css=fs.readFileSync(path.join(__dirname,'../assets/css/site.css'),'utf8');
const html=fs.readFileSync(path.join(__dirname,'../index.html'),'utf8');
assert(/\.v2-opening \{\s*min-height: 140svh;/.test(css),'Opening travel is shortened to 40svh');
const breakpoint=source.match(/var flowQuery = window.matchMedia\("([^"]+)"\)/)[1];
assert(css.includes('@media '+breakpoint+' {'),'Phone/short-landscape JS and CSS breakpoints are identical');
const desktopRule=css.match(/\.motion-ready:not\(\.flow-scenes\) \[data-stage-panel\]\s*\{([^}]+)\}/);
assert(desktopRule && !/visibility\s*:\s*hidden|display\s*:\s*none/.test(desktopRule[1]),'Staged content remains in the accessibility tree');
assert(/pointer-events\s*:\s*none/.test(desktopRule[1]));
assert(!/\.motion-ready\s+(?:\.scroll-track|\.scroll-stage|\.stage-panels|\[data-stage-panel\])/.test(css),'Artificial stage layout cannot apply to phone flow');
assert(/\.scroll-track \.stage-panels\s*\{[^}]*height: auto;[^}]*overflow: visible/.test(css),'Flow has natural height and no clipping');
assert(/\.scroll-track \[data-stage-panel\]\s*\{[^}]*position: relative;[^}]*height: auto;[^}]*opacity: 1/.test(css),'All phone cards participate in ordinary layout');
const narrativePanels=[...html.matchAll(/<article[^>]*data-stage-panel="[0-3]"[^]*?<\/article>/g)];
assert.equal(narrativePanels.length,8);
for(const panel of narrativePanels) {
  assert(!/aria-hidden="true"|\bhidden(?:[\s=>])|\binert(?:[\s=>])/.test(panel[0]));
  assert(!/<(?:a|button|input|select|textarea|summary)\b|\btabindex\s*=/.test(panel[0]),'Desktop invisible panels have no keyboard stops');
}
const cues=[...html.matchAll(/<span class="scene-scroll-cue" data-scene-scroll-cue aria-hidden="true">([^]*?)<\/span>/g)];
assert.equal(cues.length,4);
for(const cue of cues) assert(/<svg\b/.test(cue[1]) && !/<(?:a|button)\b/.test(cue[0]));
assert(/\.scroll-track \.stage-indicator, \.scroll-track \.scene-scroll-cue, \.scroll-track \.story-thread \{ display: none;/.test(css),'Former sticky cues are absent from phone flow');
assert(/@media \(prefers-reduced-motion: reduce\)[^]*?\.scene-scroll-cue\s*\{\s*display:\s*none !important/.test(css));
assert(/\.scene-scroll-cue\s*\{[^}]*display:\s*none/.test(css),'No-JS shows no stray scroll cue');
const backdrops=[...html.matchAll(/<div class="scene-depth scene-depth--(?:story|process)" aria-hidden="true">([^]*?)<\/svg>/g)];
assert.equal(backdrops.length,2,'Both targeted scenes have their own accessible-safe code-native backdrop');
for(const backdrop of backdrops) assert(/focusable="false"/.test(backdrop[1]) && !/<(?:a|button)\b/.test(backdrop[1]));
assert(/\.scene-depth \{[^}]*pointer-events: none/.test(css),'Decorative art cannot intercept gestures');
assert(/\.scene-depth-window \{[^}]*overflow: clip/.test(css),'Oversized art clips inside its own window');
assert(!/\.scene-depth[^}]*animation:/.test(css),'Brand depth has no autonomous animation');
assert(/\.story-panel \{ padding: 1.1rem .5rem .4rem; border: 0; background: transparent;/.test(css),'Phone story avoids nested outer boxes');
console.log('PASS production scene geometry: capped desktop travel and 210px maximum middle-card hold; visible reversible SVG depth; desktop heading/bottom holds and reverse progression; phone natural flow, unequal-height visible stages, no counter-translation, early connection completion, responsive/motion-mode cleanup, accessible complete narration and cue scope');
