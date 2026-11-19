#!/usr/bin/env python3
"""Builds /verdict/index.html (the All Verdicts catalogue) from verdict/verdicts.json.
Run from the repo root:  python3 tools/build_verdict_index.py
status: live = listed with link; review = listed as "In review", no link; hidden = not listed."""
import json, re, html
E = html.escape
home = open('index.html', encoding='utf-8').read()
style = re.search(r'<style>.*?</style>', home, re.S).group(0)
footer = re.search(r'<footer class="site dial">.*?</footer>', home, re.S).group(0)
footer = footer.replace('href="#home"', 'href="/"').replace('href="#verdict"', 'href="/verdict/"')
footer = re.sub(r'href="#(how-i-check|about|work)"', r'href="/#\1"', footer)
data = [v for v in json.load(open('verdict/verdicts.json', encoding='utf-8')) if v['status'] != 'hidden']
VN = {'p': 'Proven', 'np': 'Not proven', 'nj': 'Not justified'}
goals = []
for v in data:
    if v['status'] == 'live' and v['goal'] not in goals: goals.append(v['goal'])
ORDER = ['Know your risk', 'Slow aging', 'Hormones & sexual health', 'Recover & perform', 'Metabolic health', 'Detox & cleansing', 'Skin & appearance']
goals.sort(key=lambda g: ORDER.index(g) if g in ORDER else 99)
tools = sorted({v['tool'] for v in data if v['status'] == 'live'}, key=str.lower)
rows, soon = [], []
for v in data:
    live = v['status'] == 'live'
    hay = ' '.join([v['id'], v['tool'], v['method'], v['claim'], v['question'], v['who'], v['goal'], v['type'], v.get('also', ''), VN[v['verdict']] if live else '']).lower()
    if live:
        word = VN[v['verdict']] + (' · ' + v['qual'] if v.get('qual') else '')
        pill = f'<span class="pill s-{v["verdict"]}">{E(word)}</span>'
        meta = 'Issued ' + v['issued'] + (' · Evidence reviewed ' + v['evidence'] if v.get('evidence') else '')
        tag, href, cls = 'a', f' href="{v["url"]}"', 'row vx'
    else:
        pill = '<span class="pill s-ir">Coming ' + E(v['issued'].rsplit(' ', 1)[0]) + '</span>'
        meta = 'Review complete'
        tag, href, cls = 'div', '', 'row vx soon'
    (rows if live else soon).append(f'''        <{tag} class="{cls}"{href} data-g="{E(v['goal'])}" data-t="{E(v['tool'])}" data-s="{E(hay)}">
          <span class="date">{v['id']}</span>
          <span class="vb"><span class="vn">VERDICT.{v['id']}</span><span class="vt">{E(v['tool'])}</span><span class="rt">{E(v['question'])}</span><span class="vw">{E(v['who'])}</span></span>
          {pill}
          <span class="rd">{E(v['goal'])} · {E(meta)}</span>
        </{tag}>''')
tchips = '\n'.join(f'          <button type="button" class="chip" data-t="{E(t)}">{E(t)}</button>' for t in tools)
chips = '\n'.join(f'          <button type="button" class="chip" data-g="{E(g)}">{E(g)}</button>' for g in goals)
soon.reverse()
nlive = sum(1 for v in data if v['status'] == 'live')
page = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>All Verdicts: evidence reviews of medical tests, treatments and longevity claims | Yevgen Shagov, MD, PhD</title>
<meta name="description" content="SHAGOV | VERDICT. Independent, dated evidence reviews of medical tests, treatments and longevity claims. Search by treatment, test or health goal.">
<link rel="canonical" href="https://shagov.pro/verdict/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Yevgen Shagov">
<meta property="og:title" content="SHAGOV | VERDICT. Before you buy the promise, check the evidence.">
<meta property="og:description" content="Independent, dated evidence reviews of medical tests, treatments and longevity claims.">
<meta property="og:url" content="https://shagov.pro/verdict/">
<meta property="og:image" content="https://shagov.pro/img/og.jpg">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=PT+Serif:ital@0;1&display=swap">
{style}
<style>
/* ---------- Verdict index ---------- */
.vsearch {{ display: flex; align-items: center; gap: 12px; max-width: 640px; border: 1px solid rgba(220,225,232,.55); background: rgba(6,12,31,.45); padding: 0 16px; }}
.vsearch svg {{ flex: none; color: var(--gold); }}
.vsearch input {{ flex: 1; min-width: 0; background: transparent; border: 0; outline: 0; color: var(--on-dial); font: inherit; font-size: 17px; padding: 16px 0; }}
.vsearch input::placeholder {{ color: var(--on-dial-3); }}
.vsearch:focus-within {{ border-color: var(--gold); }}
.vbar {{ display: flex; flex-direction: column; gap: 14px; }}
.vgrp {{ display: flex; flex-wrap: wrap; align-items: center; gap: 8px; }}
.vgrp .gl {{ font-size: 10.5px; letter-spacing: 2.5px; text-transform: uppercase; font-weight: 700; color: var(--tantalum); margin-right: 8px; min-width: 96px; }}
.chip {{ font: inherit; font-size: 13px; font-weight: 600; color: var(--ink-2); background: var(--paper); border: 1px solid var(--hair-light); border-radius: 999px; padding: 7px 14px; cursor: pointer; }}
.chip:hover {{ border-color: var(--tantalum); }}
.chip.on {{ background: var(--ink); border-color: var(--ink); color: #fff; }}
.row.vx {{ grid-template-columns: 72px minmax(0,1fr) auto; row-gap: 6px; }}
.row.vx .date {{ grid-column: 1; grid-row: 1 / span 2; align-self: center; }}
.row.vx .vb {{ grid-column: 2; grid-row: 1; }}
.row.vx .pill {{ grid-column: 3; grid-row: 1 / span 2; align-self: center; }}
.row.vx > .rd {{ grid-column: 2; grid-row: 2; }}
.row.vx .vn {{ display: none; font-size: 11px; letter-spacing: 2.5px; font-weight: 700; color: var(--tantalum); margin-bottom: 6px; }}
.row.vx .vt {{ display: block; font-size: 21px; font-weight: 800; letter-spacing: -.2px; }}
.row.vx .rt {{ display: block; font-size: 16.5px; font-weight: 600; margin-top: 2px; }}
.row.vx .vw {{ display: block; font-size: 14px; color: var(--ink-2); margin-top: 4px; }}
.row.vx > .rd {{ display: block; font-size: 12.5px; color: var(--tantalum); }}
.row.vx:hover .vt {{ color: var(--chrome); }}
.row.vx.soon .vt {{ color: var(--ink-2); }}
.vsoon-h {{ font-size: 10.5px; letter-spacing: 2.5px; text-transform: uppercase; font-weight: 700; color: var(--tantalum); margin: 36px 0 10px; }}
.vhero {{ padding-top: 44px; padding-bottom: 40px; }}
.vhero h1 {{ font-size: clamp(30px, 4.4vw, 50px); }}
.vclear {{ font: inherit; font-size: 13px; font-weight: 700; color: var(--chrome); background: none; border: 0; border-bottom: 1.5px solid currentColor; padding: 0 0 1px; cursor: pointer; margin: 0 14px 0 6px; }}
.row.vx[hidden] {{ display: none; }}
.vcount {{ font-size: 13px; color: var(--tantalum); }}
.vempty {{ padding: 28px 0; border-bottom: 1px solid var(--hair-light); color: var(--ink-2); }}
@media (max-width: 720px) {{ .row.vx {{ grid-template-columns: minmax(0,1fr); row-gap: 10px; }} .row.vx .date {{ display: none; }} .row.vx .vn {{ display: block; }} .row.vx .vb, .row.vx .pill, .row.vx > .rd {{ grid-column: 1; grid-row: auto; }} .row.vx .pill {{ justify-self: start; }} .vgrp .gl {{ min-width: 100%; }} }}
</style>
</head>
<body>

<header class="site">
  <div class="wrap">
    <a class="logo" href="/"><span class="nm">Yevgen <b>SHAGOV</b></span><span class="cred">MD, PhD · Associate Professor</span></a>
    <nav class="main" aria-label="Main">
      <a class="v on" href="/verdict/">Verdicts</a>
      <a href="/#how-i-check">Method</a>
      <a href="/#about">About</a>
    </nav>
  </div>
</header>

<main>
  <section class="sec dial vhero" style="--cx: 85%; --cy: 0%;">
    <div class="wrap stack">
      <div class="narrow stack">
        <div class="eyebrow">SHAGOV | VERDICT.</div>
        <h1>Before you buy the promise. <span class="iv">Check the evidence.</span></h1>
        <p class="lead muted">Independent evidence reviews of medical tests, treatments and longevity claims. One promise, one group of people, one dated verdict.</p>
      </div>
      <label class="vsearch">
        <svg viewBox="0 0 20 20" width="20" height="20" aria-hidden="true"><circle cx="8.5" cy="8.5" r="5.5" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M13 13 L18 18" stroke="currentColor" stroke-width="1.8"/></svg>
        <input id="vq" type="search" placeholder="Search methods or claims…" aria-label="Search verdicts" autocomplete="off">
      </label>
    </div>
  </section>

  <section class="sec">
    <div class="wrap stack-lg">
      <div class="vbar">
        <div class="vgrp" id="vg-goal"><span class="gl">By goal</span>
          <button type="button" class="chip on" data-g="">All</button>
{chips}
        </div>
        <div class="vgrp" id="vg-tool"><span class="gl">By method</span>
          <button type="button" class="chip on" data-t="">All</button>
{tchips}
        </div>
      </div>
      <div>
        <p class="vcount" id="vcount" aria-live="polite">{nlive} published verdicts</p>
        <div class="rowlist" id="vlist">
{chr(10).join(rows)}
          <div class="vempty" id="vempty" hidden>No verdicts match your search and filters. <button type="button" class="vclear" id="vclear">Clear filters</button> <a class="link" href="mailto:yevgen@shagov.pro?subject=Suggest%20a%20VERDICT%20topic">Suggest a topic →</a></div>
        </div>
        <div id="vsoon"{'' if soon else ' hidden'}>
          <div class="vsoon-h">Coming next</div>
          <div class="rowlist" id="vlist2">
{chr(10).join(soon)}
          </div>
        </div>
      </div>
      <div class="defs">
        <div class="def s-p"><span class="pill">Proven</span><p>Enough evidence that the promised benefit is real for this goal and this group of people, with an acceptable balance of benefit and risk.</p></div>
        <div class="def s-np"><span class="pill">Not proven</span><p>There is a plausible rationale, but the evidence is insufficient to confirm the claimed benefit.</p></div>
        <div class="def s-nj"><span class="pill">Not justified</span><p>On current evidence, using this method for this purpose is not justified, considering the expected benefit, risks and costs.</p></div>
      </div>
      <p class="muted small">Each verdict concerns one specific promise for one group of people. It is not a rating of the method as a whole, and verdicts are not ranked against each other.</p>
      <p><a class="link" href="/#how-i-check">How I check →</a></p>
    </div>
  </section>
</main>

{footer}

<script>
(function () {{
  var q = document.getElementById('vq'), rows = [].slice.call(document.querySelectorAll('.row.vx')), soonBox = document.getElementById('vsoon'),
      empty = document.getElementById('vempty'), count = document.getElementById('vcount'), st = {{ q: '', t: '', g: '' }};
  try {{ var p = new URLSearchParams(location.search); st.q = p.get('q') || ''; st.t = p.get('t') || ''; st.g = p.get('g') || ''; }} catch (e) {{}}
  function apply(push) {{
    var words = st.q.toLowerCase().split(/\\s+/).filter(Boolean), n = 0, ns = 0;
    rows.forEach(function (r) {{
      var ok = (!st.t || r.getAttribute('data-t') === st.t) && (!st.g || r.getAttribute('data-g') === st.g);
      var s = r.getAttribute('data-s');
      for (var i = 0; ok && i < words.length; i++) if (s.indexOf(words[i]) === -1) ok = false;
      r.hidden = !ok; if (ok) {{ if (r.classList.contains('soon')) ns++; else n++; }}
    }});
    empty.hidden = (n + ns) !== 0; soonBox.hidden = ns === 0;
    count.textContent = (st.q || st.t || st.g) ? (n === 0 && ns > 0 ? 'Not published yet · coming next' : (n + (n === 1 ? ' published verdict' : ' published verdicts'))) : '{nlive} published verdicts';
    document.querySelectorAll('#vg-goal .chip').forEach(function (c) {{ c.classList.toggle('on', c.getAttribute('data-g') === st.g); }});
    document.querySelectorAll('#vg-tool .chip').forEach(function (c) {{ c.classList.toggle('on', c.getAttribute('data-t') === st.t); }});
    if (push) try {{
      var u = new URLSearchParams(); if (st.q) u.set('q', st.q); if (st.t) u.set('t', st.t); if (st.g) u.set('g', st.g);
      var qs = u.toString(); history.replaceState(null, '', qs ? '?' + qs : location.pathname);
    }} catch (e) {{}}
  }}
  q.value = st.q;
  q.addEventListener('input', function () {{ st.q = q.value.trim(); apply(true); }});
  function pair(g, t) {{ return rows.some(function (r) {{ return r.getAttribute('data-g') === g && r.getAttribute('data-t') === t; }}); }}
  document.getElementById('vg-goal').addEventListener('click', function (e) {{ var c = e.target.closest('.chip'); if (c) {{ st.g = c.getAttribute('data-g'); st.t = ''; apply(true); }} }});
  document.getElementById('vg-tool').addEventListener('click', function (e) {{ var c = e.target.closest('.chip'); if (c) {{ st.t = c.getAttribute('data-t'); st.g = ''; apply(true); }} }});
  document.getElementById('vclear').addEventListener('click', function () {{ st.q = ''; st.t = ''; st.g = ''; q.value = ''; apply(true); }});
  apply(false);
}})();
(function(){{var h=document.querySelector('header.site'),y=0;window.addEventListener('scroll',function(){{var n=window.scrollY;if(n>y&&n>80)h.classList.add('hide');else h.classList.remove('hide');y=n;}},{{passive:true}});}})();
</script>
</body>
</html>
'''
open('verdict/index.html', 'w', encoding='utf-8').write(page)
print('built', len(rows), 'live rows,', len(soon), 'coming;', nlive, 'live; goals:', goals)
