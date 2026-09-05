/* Execute production stage functions with controlled layout geometry.
 * This verifies scroll maths, not browser rendering or physical touch behaviour. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const source = fs.readFileSync(require('node:path').join(__dirname, '../assets/js/site.js'), 'utf8');
const names = ['clamp', 'phase', 'ease', 'measureTracks', 'trackProgress', 'renderTracks'];
const functions = names.map(name => {
  const match = source.match(new RegExp('^  function ' + name + '\\([^]*?(?=^  function |^  if \\()', 'm'));
  assert(match, 'Production function missing: ' + name);
  return match[0];
}).join('\n');
function fixture(kind, viewport, panelHeight) {
  const variables = {};
  const styles = () => ({setProperty: (key, value) => variables[key] = value});
  const classList = () => ({toggle() {}});
  const parent = {get offsetHeight() {return parseFloat(variables['--panels-height']) || panelHeight;}};
  const panels = Array.from({length:4}, () => ({offsetHeight:panelHeight, parentElement:parent, style:{},classList:classList()}));
  const inner = {get offsetHeight() {return parent.offsetHeight + 90;}};
  const stage = {get offsetHeight() {return parseFloat(variables['--stage-height']) || viewport-72;}, querySelector: () => inner};
  const indicators = panels.map(() => ({classList:classList()}));
  const thread = {style:{}};
  const light = {style:{}};
  let progress = 0;
  const track = {
    dataset:{scrollTrack:kind},style:styles(), attrs:{},
    setAttribute(key,value){this.attrs[key]=value;},
    get offsetHeight(){return stage.offsetHeight + parseFloat(variables['--scroll-travel']);},
    getBoundingClientRect(){return {top:72 - progress * (this.offsetHeight-stage.offsetHeight)};},
    querySelector(selector){return selector === '.scroll-stage' ? stage : selector === '.story-thread i' ? thread : selector === '.process-light' && kind === 'process' ? light : null;},
    querySelectorAll(selector){return selector === '[data-stage-panel]' ? panels : selector === '[data-stage-indicator]' ? indicators : [];}
  };
  const context = {tracks:[track], reducedQuery:{matches:false}, story:{setAttribute(){}},nav:{offsetHeight:72},viewportProbe:{offsetHeight:viewport},window:{innerHeight:viewport}, needsMeasure:true,
    // Bottom padding includes the rendered cue reserve (16px base + 48px cue).
    getComputedStyle(){return {paddingTop:'16',paddingBottom:'64',top:'72'};},measureWires(){throw new Error('Unexpected wire measure');}};
  vm.createContext(context); vm.runInContext(functions,context); context.measureTracks();
  assert.equal(parseFloat(variables['--panels-height']), Math.min(panelHeight,Math.max(80,viewport-72-170)), 'Cue space reduces the panel viewport and feeds the reading phase');
  return {context, panels, variables, track, parent, setProgress(value){progress=value;context.renderTracks();}};
}
for (const kind of ['story','process']) {
  for (const [height, natural] of [[900,470],[844,420],[600,450],[500,440],[480,490],[390,270]]) {
    const f = fixture(kind,height,natural);
    assert.equal(parseFloat(f.variables['--stage-height']), height-72, 'The stage fits below navigation');
    assert.equal(f.variables['--stage-top'], '72px', 'Oversized stages do not hide incoming headings above the viewport');
    const snapshots = [];
    for (let i=0;i<4;i++) {
      f.setProgress((i+0.18)/4);
      assert.equal(f.panels[i].style.opacity,'1');
      assert.equal(f.panels[i].style.transform,'translateY(0px)', 'Each incoming heading gets a readable hold');
      f.setProgress((i+0.76)/4);
      const overflow = Math.max(0,natural-f.parent.offsetHeight);
      assert.equal(f.panels[i].style.transform,`translateY(${-overflow}px)`, 'The bottom is exposed before leaving');
      snapshots.push(f.panels.map(p => ({...p.style})));
    }
    for (let i=3;i>=0;i--) {
      f.setProgress((i+0.76)/4);
      assert.deepEqual(f.panels.map(p => ({...p.style})),snapshots[i], 'Reverse scrolling restores the exact state');
    }
    const travel=f.variables['--scroll-travel'];
    f.context.window.innerHeight+=70; f.context.measureTracks();
    assert.equal(f.variables['--scroll-travel'],travel,'Toolbar changes do not alter scroll distance');
    f.context.reducedQuery.matches=true;f.setProgress(0);
    assert.equal(f.track.attrs['data-progress'],'1.0000','Reduced motion has a complete final geometry');
  }
}
assert(!source.includes('storyStaticQuery') && !source.includes('story-static'));
// Visual scroll stages must not remove the complete narrative from virtual-cursor reading.
const css = fs.readFileSync(require('node:path').join(__dirname, '../assets/css/site.css'), 'utf8');
const html = fs.readFileSync(require('node:path').join(__dirname, '../index.html'), 'utf8');
const panelRule = css.match(/\.motion-ready \[data-stage-panel\]\s*\{([^}]+)\}/);
assert(panelRule, 'Enhanced stage rule is present');
assert(!/visibility\s*:\s*hidden|display\s*:\s*none/.test(panelRule[1]), 'All narrative stages remain available to screen readers');
assert(/pointer-events\s*:\s*none/.test(panelRule[1]), 'Invisible panels do not intercept pointer input');
const narrativePanels = [...html.matchAll(/<article[^>]*data-stage-panel="[0-3]"[^]*?<\/article>/g)];
assert.equal(narrativePanels.length, 8);
for (const panel of narrativePanels) {
  assert(!/aria-hidden="true"|\bhidden(?:[\s=>])|\binert(?:[\s=>])/.test(panel[0]), 'Narration is not hidden from assistive technology');
  assert(!/<(?:a|button|input|select|textarea|summary)\b|\btabindex\s*=/.test(panel[0]), 'Invisible narrative panels cannot contain keyboard-focus stops');
}
const cues = [...html.matchAll(/<span class="scene-scroll-cue" data-scene-scroll-cue aria-hidden="true">([^]*?)<\/span>/g)];
assert.equal(cues.length, 4, 'Opening and all three sticky tracks have one decorative scroll cue');
for (const cue of cues) {
  assert(/<svg\b/.test(cue[1]) && !/<(?:a|button)\b/.test(cue[0]), 'Cues are code-native decoration, not controls');
}
const stageCuePadding = css.match(/\.motion-ready \.scroll-stage\s*\{([^}]+)\}/);
assert(stageCuePadding && /padding-bottom\s*:\s*calc\([^;]*--scene-cue-space/.test(stageCuePadding[1]), 'Sticky layout reserves measured space below content for its cue');
assert(/@media \(prefers-reduced-motion: reduce\)[^]*?\.scene-scroll-cue\s*\{\s*display:\s*none !important/.test(css), 'Reduced Motion hides the animated cue');
assert(/\.scene-scroll-cue\s*\{[^}]*display:\s*none/.test(css) && /\.motion-ready \.scene-scroll-cue\s*\{\s*display:\s*block/.test(css), 'No-JS flow has no stray cue');
console.log('PASS production scroll maths: six viewport/card geometries, all stages, heading/bottom holds, reverse motion, toolbar stability, reduced-motion geometry, complete accessible narration and four non-interactive reserved-space scroll cues');
