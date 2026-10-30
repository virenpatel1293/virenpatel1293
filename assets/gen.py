"""Generates the custom animated SVGs for the GitHub profile README."""
import os

OUT = os.path.join(os.path.dirname(__file__), "assets")
SANS = "'Segoe UI', -apple-system, BlinkMacSystemFont, Ubuntu, 'Helvetica Neue', Arial, sans-serif"
MONO = "SFMono-Regular, Consolas, 'Liberation Mono', Menlo, 'DejaVu Sans Mono', monospace"

C = dict(bg0="#060914", bg1="#0d1326", grid="#1b2440", sky="#38bdf8", vio="#a78bfa",
         grn="#34d399", amb="#fbbf24", pink="#f472b6", txt="#e2e8f0", mut="#64748b")


def write(name, body):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(body)


# ---------------------------------------------------------------- HERO
def hero():
    W, H = 1200, 400
    roles = [
        (C["sky"], "CODER", "I write the code that ships."),
        (C["vio"], "PROJECT MANAGER", "I scope it, plan it, unblock the team."),
        (C["grn"], "DEVOPS", "I build the pipeline &amp; keep prod green."),
    ]
    T = 9.0
    role_svg = []
    for i, (col, tag, line) in enumerate(roles):
        kt, vals = [("0;0.303;0.333;0.97;1", "1;1;0;0;1"),
                    ("0;0.333;0.363;0.636;0.666;1", "0;0;1;1;0;0"),
                    ("0;0.666;0.696;0.97;1", "0;0;1;1;0")][i]
        role_svg.append(f'''
    <g opacity="{1 if i == 0 else 0}">
      <animate attributeName="opacity" dur="{T}s" repeatCount="indefinite" keyTimes="{kt}" values="{vals}"/>
      <rect x="70" y="222" rx="6" width="{len(tag)*10.5+28}" height="30" fill="{col}" fill-opacity="0.14" stroke="{col}" stroke-opacity="0.6"/>
      <text x="84" y="243" font-family="{MONO}" font-size="15" font-weight="700" fill="{col}" letter-spacing="1.5">{tag}</text>
      <text x="{70+len(tag)*10.5+44}" y="244" font-family="{SANS}" font-size="22" fill="{C['txt']}">{line}</text>
    </g>''')

    pills = [("3.9k+", "contributions / yr", C["grn"]), ("295", "PRs opened in Oct", C["sky"]),
             ("16", "repos shipped to in a month", C["vio"])]
    px, pill_svg = 70, []
    for n, lab, col in pills:
        w = len(n) * 11 + len(lab) * 7.4 + 40
        pill_svg.append(f'''
    <g transform="translate({px},288)">
      <rect width="{w:.0f}" height="38" rx="19" fill="#0f172a" stroke="{col}" stroke-opacity="0.45"/>
      <circle cx="18" cy="19" r="4" fill="{col}"><animate attributeName="r" values="3;5;3" dur="2s" repeatCount="indefinite"/></circle>
      <text x="30" y="25" font-family="{SANS}" font-size="16" font-weight="700" fill="{col}">{n} <tspan font-weight="400" font-size="14" fill="{C['txt']}">{lab}</tspan></text>
    </g>''')
        px += w + 12

    cx, cy = 985, 185
    rings = [(62, C["sky"], "CODE", 7), (102, C["vio"], "PLAN", 11), (142, C["grn"], "SHIP", 16)]
    ring_svg = []
    for r, col, lab, sp in rings:
        ring_svg.append(f'''
    <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{col}" stroke-opacity="0.25" stroke-dasharray="3 6"/>
    <g><animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="{sp}s" repeatCount="indefinite"/>
      <circle cx="{cx+r}" cy="{cy}" r="7" fill="{col}" filter="url(#glow)"/>
      <circle cx="{cx-r}" cy="{cy}" r="3" fill="{col}" opacity="0.6"/>
    </g>
    <rect x="{cx-24}" y="{cy-r-9}" width="48" height="18" rx="9" fill="{C['bg0']}" stroke="{col}" stroke-opacity="0.5"/>
    <text x="{cx}" y="{cy-r+4}" text-anchor="middle" font-family="{MONO}" font-size="11" font-weight="700" fill="{col}" letter-spacing="1.5">{lab}</text>''')

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Viren Patel — Coder, Project Manager, DevOps">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{C['bg0']}"/><stop offset="1" stop-color="{C['bg1']}"/></linearGradient>
    <linearGradient id="name" x1="0" y1="0" x2="1" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="{C['sky']}"/><stop offset="0.5" stop-color="{C['vio']}"/><stop offset="1" stop-color="{C['grn']}"/>
      <animate attributeName="x1" values="0;600;0" dur="8s" repeatCount="indefinite"/>
      <animate attributeName="x2" values="620;1220;620" dur="8s" repeatCount="indefinite"/>
    </linearGradient>
    <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="{C['grid']}" stroke-width="1"/></pattern>
    <radialGradient id="orb1"><stop offset="0" stop-color="{C['vio']}" stop-opacity="0.35"/><stop offset="1" stop-color="{C['vio']}" stop-opacity="0"/></radialGradient>
    <radialGradient id="orb2"><stop offset="0" stop-color="{C['sky']}" stop-opacity="0.28"/><stop offset="1" stop-color="{C['sky']}" stop-opacity="0"/></radialGradient>
    <radialGradient id="core"><stop offset="0" stop-color="#1e293b"/><stop offset="1" stop-color="{C['bg0']}"/></radialGradient>
    <linearGradient id="sweep" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{C['sky']}" stop-opacity="0"/><stop offset="1" stop-color="{C['sky']}" stop-opacity="0.28"/></linearGradient>
    <linearGradient id="fadeR" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity="1"/></linearGradient>
    <filter id="glow" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
    <clipPath id="frame"><rect width="{W}" height="{H}" rx="18"/></clipPath>
  </defs>
  <g clip-path="url(#frame)">
    <rect width="{W}" height="{H}" fill="url(#bg)"/>
    <rect width="{W}" height="{H}" fill="url(#grid)" opacity="0.55"/>
    <circle cx="260" cy="80" r="260" fill="url(#orb1)"><animate attributeName="cx" values="200;420;200" dur="14s" repeatCount="indefinite"/></circle>
    <circle cx="980" cy="330" r="280" fill="url(#orb2)"><animate attributeName="cy" values="360;220;360" dur="12s" repeatCount="indefinite"/></circle>

    <!-- intro -->
    <text x="70" y="92" font-family="{MONO}" font-size="17" fill="{C['sky']}">&gt; hello, world — I'm<tspan fill="{C['sky']}">_<animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/></tspan></text>
    <text x="66" y="178" font-family="{SANS}" font-size="84" font-weight="800" fill="url(#name)" letter-spacing="-1">Viren Patel</text>
    {''.join(role_svg)}
    {''.join(pill_svg)}

    <!-- radar -->
    <g>
      <path d="M{cx} {cy} L{cx+150} {cy} A150 150 0 0 0 {cx+106} {cy-106} Z" fill="url(#sweep)">
        <animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="-360 {cx} {cy}" dur="5s" repeatCount="indefinite"/>
      </path>
      {''.join(ring_svg)}
      <circle cx="{cx}" cy="{cy}" r="34" fill="url(#core)" stroke="{C['sky']}" stroke-opacity="0.7"/>
      <circle cx="{cx}" cy="{cy}" r="34" fill="none" stroke="{C['sky']}" stroke-opacity="0.5">
        <animate attributeName="r" values="34;60" dur="2.4s" repeatCount="indefinite"/>
        <animate attributeName="stroke-opacity" values="0.6;0" dur="2.4s" repeatCount="indefinite"/>
      </circle>
      <text x="{cx}" y="{cy+8}" text-anchor="middle" font-family="{SANS}" font-size="22" font-weight="800" fill="{C['txt']}">VP</text>
    </g>

    <!-- status bar -->
    <rect y="{H-38}" width="{W}" height="38" fill="#000" fill-opacity="0.35"/>
    <line x1="0" y1="{H-38}" x2="{W}" y2="{H-38}" stroke="{C['grid']}"/>
    <circle cx="34" cy="{H-19}" r="5" fill="{C['grn']}"><animate attributeName="opacity" values="1;0.3;1" dur="1.6s" repeatCount="indefinite"/></circle>
    <text x="48" y="{H-14}" font-family="{MONO}" font-size="13" fill="{C['mut']}"><tspan fill="{C['grn']}">all systems operational</tspan>   │   build: <tspan fill="{C['grn']}">passing</tspan>   │   deploys: <tspan fill="{C['sky']}">zero-downtime</tspan>   │   timezone: <tspan fill="{C['txt']}">SAST (UTC+2)</tspan>   │   based in <tspan fill="{C['txt']}">Pretoria, ZA</tspan></text>
  </g>
  <rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="18" fill="none" stroke="{C['grid']}"/>
</svg>'''
    write("hero.svg", svg)


# ---------------------------------------------------------------- TERMINAL
def terminal():
    W = 1000
    lines = [
        ("cmd", "whoami"),
        ("out", [("viren_patel", C["txt"]), ("  // engineer · project manager · devops", C["mut"])]),
        ("cmd", "cat ~/stack.yml"),
        ("out", [("frontend: ", C["vio"]), ("[next.js, react, expo, tailwind]", C["txt"])]),
        ("out", [("backend:  ", C["vio"]), ("[node, .net c#, prisma, sql server, python]", C["txt"])]),
        ("out", [("infra:    ", C["vio"]), ("[cloudflare workers, aws, pm2, github actions]", C["txt"])]),
        ("out", [("ai:       ", C["vio"]), ("[mcp servers, agent tooling]", C["txt"])]),
        ("cmd", "git log --author=viren --since=30.days --oneline | wc -l"),
        ("out", [("459", C["amb"]), ("  // commits across 16 repos", C["mut"])]),
        ("cmd", "./ship.sh --env=production"),
        ("ok", "lint &amp; typecheck"),
        ("ok", "tests green"),
        ("ok", "build &amp; bundle"),
        ("ok", "deployed to the edge  ·  zero downtime  ·  team notified"),
    ]
    step, top = 25, 76
    H = top + len(lines) * step + 50
    T = 22.0
    t, rows, cmd_w = 0.8, [], 9.05
    for i, (kind, val) in enumerate(lines):
        y = top + i * step
        if kind == "cmd":
            dur_type = max(0.5, len(val) * 0.035)
            start, end = t, t + dur_type
            t = end + 0.45
            w = len(val) * cmd_w + 6
            k0, k1 = start / T, end / T
            rows.append(f'''
    <clipPath id="c{i}"><rect x="62" y="{y-18}" height="26" width="0">
      <animate attributeName="width" dur="{T}s" repeatCount="indefinite" keyTimes="0;{k0:.4f};{k1:.4f};0.96;1" values="0;0;{w:.0f};{w:.0f};0"/></rect></clipPath>
    <g opacity="0"><animate attributeName="opacity" dur="{T}s" repeatCount="indefinite" keyTimes="0;{k0:.4f};{k0+0.0005:.4f};0.96;0.98;1" values="0;0;1;1;0;0"/>
      <text x="28" y="{y}" font-family="{MONO}" font-size="15" fill="{C['grn']}">❯</text>
      <text x="44" y="{y}" font-family="{MONO}" font-size="15" fill="{C['sky']}">~</text>
      <text x="64" y="{y}" font-family="{MONO}" font-size="15" fill="{C['txt']}" clip-path="url(#c{i})">{val}</text>
    </g>''')
        else:
            start = t
            t += 0.28 if kind == "out" else 0.7
            k0 = start / T
            if kind == "out":
                inner = "".join(f'<tspan fill="{c}">{s}</tspan>' for s, c in val)
                content = f'<text x="44" y="{y}" font-family="{MONO}" font-size="15" xml:space="preserve">{inner}</text>'
            else:
                content = (f'<text x="44" y="{y}" font-family="{MONO}" font-size="15" fill="{C["grn"]}">✔</text>'
                           f'<text x="66" y="{y}" font-family="{MONO}" font-size="15" fill="{C["txt"]}">{val}</text>')
            rows.append(f'''
    <g opacity="0"><animate attributeName="opacity" dur="{T}s" repeatCount="indefinite" keyTimes="0;{k0:.4f};{k0+0.01:.4f};0.96;0.98;1" values="0;0;1;1;0;0"/>{content}</g>''')
    yc = top + len(lines) * step
    kc = t / T
    rows.append(f'''
    <g opacity="0"><animate attributeName="opacity" dur="{T}s" repeatCount="indefinite" keyTimes="0;{kc:.4f};{kc+0.001:.4f};0.96;0.98;1" values="0;0;1;1;0;0"/>
      <text x="28" y="{yc}" font-family="{MONO}" font-size="15" fill="{C['grn']}">❯</text>
      <text x="44" y="{yc}" font-family="{MONO}" font-size="15" fill="{C['sky']}">~</text>
      <rect x="64" y="{yc-14}" width="9" height="18" fill="{C['txt']}"><animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/></rect>
    </g>''')

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Terminal: whoami, stack, and a production deploy">
  <defs><clipPath id="frame"><rect width="{W}" height="{H}" rx="14"/></clipPath></defs>
  <g clip-path="url(#frame)">
    <rect width="{W}" height="{H}" fill="#0b0f19"/>
    <rect width="{W}" height="40" fill="#151b2b"/>
    <circle cx="24" cy="20" r="6.5" fill="#ff5f57"/><circle cx="46" cy="20" r="6.5" fill="#febc2e"/><circle cx="68" cy="20" r="6.5" fill="#28c840"/>
    <text x="{W/2}" y="25" text-anchor="middle" font-family="{MONO}" font-size="13" fill="{C['mut']}">viren@prod: ~ — zsh</text>
    {''.join(rows)}
  </g>
  <rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="14" fill="none" stroke="#243049"/>
</svg>'''
    write("terminal.svg", svg)


# ---------------------------------------------------------------- PIPELINE
def pipeline():
    W, H = 1200, 292
    stages = [("PLAN", "scope · tickets · sprint", C["vio"]),
              ("CODE", "Next.js · .NET · Node", C["sky"]),
              ("REVIEW", "PRs · QA · approvals", C["sky"]),
              ("BUILD", "CI · tests · bundle", C["grn"]),
              ("DEPLOY", "edge · zero-downtime", C["grn"]),
              ("MONITOR", "logs · PM2 · traces", C["grn"])]
    bw, bh, y0 = 158, 84, 104
    xs = [42 + i * 190 for i in range(6)]
    T = 6.0
    boxes = []
    for i, (name, sub, col) in enumerate(stages):
        x = xs[i]
        a = i / 6
        kt = f"0;{a:.3f};{a+0.08:.3f};{min(a+0.25,0.999):.3f};1"
        boxes.append(f'''
    <g>
      <rect x="{x}" y="{y0}" width="{bw}" height="{bh}" rx="14" fill="#0d1424" stroke="{col}" stroke-opacity="0.55"/>
      <rect x="{x}" y="{y0}" width="{bw}" height="{bh}" rx="14" fill="{col}" fill-opacity="0.16" stroke="{col}" stroke-width="2" opacity="0" filter="url(#glow)">
        <animate attributeName="opacity" dur="{T}s" repeatCount="indefinite" keyTimes="{kt}" values="0;0;1;0;0"/>
      </rect>
      <text x="{x+16}" y="{y0+24}" font-family="{MONO}" font-size="11" fill="{col}" opacity="0.8">0{i+1}</text>
      <text x="{x+bw/2}" y="{y0+48}" text-anchor="middle" font-family="{SANS}" font-size="20" font-weight="800" fill="{C['txt']}" letter-spacing="1.5">{name}</text>
      <text x="{x+bw/2}" y="{y0+70}" text-anchor="middle" font-family="{SANS}" font-size="12.5" fill="{C['mut']}">{sub}</text>
    </g>''')
    arrows = "".join(
        f'<line x1="{xs[i]+bw+4}" y1="{y0+bh/2}" x2="{xs[i+1]-8}" y2="{y0+bh/2}" stroke="#334155" stroke-width="2" marker-end="url(#ah)"/>'
        for i in range(5))

    bands = [(0, 0, "PROJECT MANAGER", C["vio"]), (1, 2, "CODER", C["sky"]), (3, 5, "DEVOPS", C["grn"])]
    band_svg = ""
    for a, b, lab, col in bands:
        x1, x2 = xs[a], xs[b] + bw
        band_svg += f'''
    <path d="M{x1} 88 V78 H{x2} V88" fill="none" stroke="{col}" stroke-width="2" stroke-opacity="0.8"/>
    <rect x="{(x1+x2)/2 - len(lab)*5.2 - 12}" y="66" width="{len(lab)*10.4+24}" height="24" rx="12" fill="{C['bg0']}" stroke="{col}"/>
    <text x="{(x1+x2)/2}" y="83" text-anchor="middle" font-family="{MONO}" font-size="13" font-weight="700" fill="{col}" letter-spacing="1.5">{lab}</text>'''

    lx1, lx2 = xs[0] + bw / 2, xs[5] + bw / 2
    loop = f"M{lx2} {y0+bh+4} V{y0+bh+52} Q{lx2} {y0+bh+62} {lx2-10} {y0+bh+62} H{lx1+10} Q{lx1} {y0+bh+62} {lx1} {y0+bh+52} V{y0+bh+10}"
    flow = f"M{xs[0]+bw} {y0+bh/2} H{xs[5]}"
    packets = "".join(
        f'<circle r="4.5" fill="{C["amb"]}" filter="url(#glow)"><animateMotion dur="{T}s" begin="{-k*T/3:.2f}s" repeatCount="indefinite" path="{flow}"/></circle>'
        for k in range(3))
    back = "".join(
        f'<circle r="3.5" fill="{C["vio"]}"><animateMotion dur="5s" begin="{-k*2.5:.2f}s" repeatCount="indefinite" path="{loop}"/></circle>'
        for k in range(2))

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Delivery loop: plan, code, review, build, deploy, monitor">
  <defs>
    <marker id="ah" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0 0 L8 4 L0 8 Z" fill="#475569"/></marker>
    <marker id="ahv" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0 0 L8 4 L0 8 Z" fill="{C['vio']}"/></marker>
    <filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
    <pattern id="grid" width="30" height="30" patternUnits="userSpaceOnUse"><path d="M30 0H0V30" fill="none" stroke="{C['grid']}" stroke-width="1"/></pattern>
    <clipPath id="frame"><rect width="{W}" height="{H}" rx="18"/></clipPath>
  </defs>
  <g clip-path="url(#frame)">
    <rect width="{W}" height="{H}" fill="{C['bg0']}"/>
    <rect width="{W}" height="{H}" fill="url(#grid)" opacity="0.4"/>
    <text x="42" y="40" font-family="{MONO}" font-size="14" fill="{C['mut']}">// one person, the whole loop — <tspan fill="{C['txt']}">idea → production → insight → next sprint</tspan></text>
    {band_svg}
    {arrows}
    <path d="{loop}" fill="none" stroke="{C['vio']}" stroke-opacity="0.55" stroke-width="2" stroke-dasharray="6 6" marker-end="url(#ahv)">
      <animate attributeName="stroke-dashoffset" values="0;-24" dur="1s" repeatCount="indefinite"/>
    </path>
    <rect x="{W/2-180}" y="{y0+bh+50}" width="360" height="24" rx="12" fill="{C['bg0']}"/>
    <text x="{W/2}" y="{y0+bh+67}" text-anchor="middle" font-family="{MONO}" font-size="13" fill="{C['vio']}">↺ metrics &amp; feedback feed the next sprint</text>
    {packets}
    {''.join(boxes)}
    {back}
  </g>
  <rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="18" fill="none" stroke="{C['grid']}"/>
</svg>'''
    write("pipeline.svg", svg)


# ---------------------------------------------------------------- ARCHITECTURE
def architecture():
    W, H = 1200, 470

    def node(x, y, w, h, title, sub, col):
        return f'''
    <g>
      <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="#0d1424" stroke="{col}" stroke-opacity="0.7"/>
      <rect x="{x}" y="{y}" width="5" height="{h}" rx="2" fill="{col}"/>
      <text x="{x+w/2+2}" y="{y+h/2-2}" text-anchor="middle" font-family="{SANS}" font-size="16" font-weight="700" fill="{C['txt']}">{title}</text>
      <text x="{x+w/2+2}" y="{y+h/2+18}" text-anchor="middle" font-family="{SANS}" font-size="12" fill="{C['mut']}">{sub}</text>
    </g>'''

    def wire(d, col, dur=1.2, w=2):
        return f'''<path d="{d}" fill="none" stroke="{col}" stroke-width="{w}" stroke-opacity="0.8" stroke-dasharray="5 7">
      <animate attributeName="stroke-dashoffset" values="24;0" dur="{dur}s" repeatCount="indefinite"/></path>'''

    n = []
    n.append(node(40, 175, 130, 76, "Shoppers", "web · mobile", C["pink"]))
    n.append(node(225, 155, 180, 116, "Cloudflare Edge", "Workers · cache · rules", C["amb"]))
    n.append(node(465, 115, 200, 76, "Next.js Storefront", "SSR · React · Tailwind", C["sky"]))
    n.append(node(465, 235, 200, 76, "Admin Portal", "Next.js · .NET", C["sky"]))
    n.append(node(725, 115, 190, 76, "Node + Prisma API", "REST · auth · cart", C["vio"]))
    n.append(node(725, 235, 190, 76, ".NET Services", "C# · back-office", C["vio"]))
    n.append(node(975, 155, 185, 116, "SQL Server", "orders · stock · users", C["grn"]))

    wires = [
        wire("M170 213 H225", C["pink"]),
        wire("M405 195 H435 V153 H465", C["amb"]), wire("M405 231 H435 V273 H465", C["amb"]),
        wire("M665 153 H725", C["sky"]), wire("M665 273 H725", C["sky"]),
        wire("M915 153 H945 V195 H975", C["vio"]), wire("M915 273 H945 V231 H975", C["vio"]),
    ]
    obs_y, ai_y = 370, 370
    taps = "".join(
        f'<line x1="{x}" y1="{y}" x2="{x}" y2="{obs_y}" stroke="{C["mut"]}" stroke-opacity="0.5" stroke-dasharray="2 5"/>'
        for x, y in [(315, 271), (565, 311)])
    taps += "".join(
        f'<line x1="{x}" y1="{y}" x2="{x}" y2="{ai_y}" stroke="{C["pink"]}" stroke-opacity="0.5" stroke-dasharray="2 5"/>'
        for x, y in [(820, 311), (1067, 271)])

    bottom = f'''
    <g>
      <rect x="225" y="{obs_y}" width="440" height="64" rx="12" fill="{C['grn']}" fill-opacity="0.06" stroke="{C['grn']}" stroke-opacity="0.5" stroke-dasharray="4 4"/>
      <text x="245" y="{obs_y+27}" font-family="{MONO}" font-size="12" font-weight="700" fill="{C['grn']}" letter-spacing="1.5">OBSERVABILITY</text>
      <text x="245" y="{obs_y+48}" font-family="{SANS}" font-size="13.5" fill="{C['txt']}">AWS ELB log analysis · PM2 monitor · devwatcher traces</text>
      <rect x="725" y="{ai_y}" width="435" height="64" rx="12" fill="{C['pink']}" fill-opacity="0.06" stroke="{C['pink']}" stroke-opacity="0.5" stroke-dasharray="4 4"/>
      <text x="745" y="{ai_y+27}" font-family="{MONO}" font-size="12" font-weight="700" fill="{C['pink']}" letter-spacing="1.5">AI AGENTS · MCP</text>
      <text x="745" y="{ai_y+48}" font-family="{SANS}" font-size="13.5" fill="{C['txt']}">repoflow · expo-dev · devwatcher · task trackers</text>
    </g>'''

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Architecture of the e-commerce platform I build and run">
  <defs>
    <pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1" fill="{C['grid']}"/></pattern>
    <clipPath id="frame"><rect width="{W}" height="{H}" rx="18"/></clipPath>
  </defs>
  <g clip-path="url(#frame)">
    <rect width="{W}" height="{H}" fill="{C['bg0']}"/>
    <rect width="{W}" height="{H}" fill="url(#dots)"/>
    <text x="40" y="46" font-family="{SANS}" font-size="20" font-weight="800" fill="{C['txt']}">What I build &amp; run</text>
    <text x="40" y="72" font-family="{MONO}" font-size="13" fill="{C['mut']}">// a production e-commerce stack — from the edge to the database, plus the tooling that watches it</text>
    <g font-family="{MONO}" font-size="11" fill="{C['mut']}">
      <text x="40" y="104">CLIENT</text><text x="225" y="104">EDGE</text><text x="465" y="104">APPS</text><text x="725" y="104">SERVICES</text><text x="975" y="104">DATA</text>
    </g>
    {taps}
    {''.join(wires)}
    {''.join(n)}
    {bottom}
  </g>
  <rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="18" fill="none" stroke="{C['grid']}"/>
</svg>'''
    write("architecture.svg", svg)




# ---------------------------------------------------------------- TELEMETRY
def telemetry():
    W, H = 1200, 250
    tiles = [("3,981", "contributions", "last 12 months", C["grn"], 0.92),
             ("464", "commits", "October 2026", C["sky"], 0.78),
             ("295", "pull requests", "opened in October", C["vio"], 0.70),
             ("17", "repositories", "shipped to in October", C["amb"], 0.60)]
    tw, gap, x0 = 264, 24, 42
    out = []
    for i, (num, lab, sub, col, frac) in enumerate(tiles):
        x = x0 + i * (tw + gap)
        cx, cy, r = x + 58, 140, 34
        circ = 2 * 3.14159 * r
        out.append(f'''
    <g>
      <rect x="{x}" y="70" width="{tw}" height="140" rx="14" fill="#0d1424" stroke="{col}" stroke-opacity="0.35"/>
      <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{col}" stroke-opacity="0.15" stroke-width="7"/>
      <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{col}" stroke-width="7" stroke-linecap="round"
        stroke-dasharray="{circ:.1f}" stroke-dashoffset="{circ:.1f}" transform="rotate(-90 {cx} {cy})">
        <animate attributeName="stroke-dashoffset" values="{circ:.1f};{circ*(1-frac):.1f};{circ*(1-frac):.1f};{circ:.1f}" keyTimes="0;0.25;0.9;1" dur="8s" begin="{i*0.2}s" repeatCount="indefinite"/>
      </circle>
      <circle cx="{cx}" cy="{cy}" r="5" fill="{col}"><animate attributeName="opacity" values="1;0.3;1" dur="1.8s" repeatCount="indefinite"/></circle>
      <text x="{x+108}" y="{cy-4}" font-family="{SANS}" font-size="34" font-weight="800" fill="{C['txt']}">{num}</text>
      <text x="{x+108}" y="{cy+18}" font-family="{SANS}" font-size="14" font-weight="600" fill="{col}">{lab}</text>
      <text x="{x+108}" y="{cy+36}" font-family="{MONO}" font-size="11" fill="{C['mut']}">{sub}</text>
    </g>''')
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="3,981 contributions in the last year; 464 commits, 295 pull requests and 17 repositories in October 2026">
  <defs>
    <pattern id="grid" width="30" height="30" patternUnits="userSpaceOnUse"><path d="M30 0H0V30" fill="none" stroke="{C['grid']}" stroke-width="1"/></pattern>
    <clipPath id="frame"><rect width="{W}" height="{H}" rx="18"/></clipPath>
  </defs>
  <g clip-path="url(#frame)">
    <rect width="{W}" height="{H}" fill="{C['bg0']}"/>
    <rect width="{W}" height="{H}" fill="url(#grid)" opacity="0.35"/>
    <circle cx="44" cy="40" r="5" fill="{C['grn']}"><animate attributeName="opacity" values="1;0.3;1" dur="1.4s" repeatCount="indefinite"/></circle>
    <text x="58" y="45" font-family="{MONO}" font-size="14" fill="{C['txt']}">TELEMETRY <tspan fill="{C['mut']}">// including private &amp; organisation work</tspan></text>
    {''.join(out)}
  </g>
  <rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="18" fill="none" stroke="{C['grid']}"/>
</svg>'''
    write("telemetry.svg", svg)


if __name__ == "__main__":
    hero(); terminal(); pipeline(); architecture(); telemetry()
    print("ok")
