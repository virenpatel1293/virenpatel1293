"""Rebuild the "Mission log" section of README.md from showcase.json + live repo data.

- Projects listed in the SHOWCASE_CONFIG secret (JSON, same shape as
  showcase.example.json) keep their hand-written blurbs and get a live
  activity dot from the repo's last push.
- Any of your repos with the topic `showcase` plus a category topic
  (devops / ai / product / game) is added automatically, using its description.
- Nothing is published unless it is in the config or tagged `showcase`.
- The config lives in a secret so private / organisation repo names are never
  stored in this public repo or shown in the (public) Actions logs.

Security: standard library only; the token (STATS_TOKEN) is sent only to
api.github.com and never printed. Logs show counts only, no repo names.
"""
import datetime as dt
import html
import json
import os
import re
import sys
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
README = os.path.join(ROOT, "README.md")
START, END = "<!-- MISSION-LOG:START -->", "<!-- MISSION-LOG:END -->"

QUERY = """
query($after: String) {
  viewer {
    login
    repositories(first: 100, after: $after,
                 ownerAffiliations: [OWNER, COLLABORATOR, ORGANIZATION_MEMBER]) {
      pageInfo { hasNextPage endCursor }
      nodes {
        name nameWithOwner description url isPrivate isFork isArchived
        pushedAt createdAt
        repositoryTopics(first: 20) { nodes { topic { name } } }
      }
    }
  }
}
"""


def gql(token, variables):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": variables}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json",
                 "User-Agent": "profile-showcase-updater"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            payload = json.load(resp)
    except urllib.error.HTTPError as e:
        sys.exit(f"GitHub API request failed with HTTP {e.code}.")
    if payload.get("errors") and not payload.get("data"):
        sys.exit("GitHub API returned an error.")
    return payload["data"]["viewer"]


def fetch_repos(token):
    repos, after, login = {}, None, None
    for _ in range(10):  # up to 1,000 repos
        v = gql(token, {"after": after})
        login = v["login"]
        page = v["repositories"]
        for r in page["nodes"]:
            if r:
                repos[r["nameWithOwner"].lower()] = r
        if not page["pageInfo"]["hasNextPage"]:
            break
        after = page["pageInfo"]["endCursor"]
    return login, repos


def parse_time(s):
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00")) if s else None


def ago(now, t):
    d = (now - t).days
    if d <= 0:
        return "today"
    if d == 1:
        return "yesterday"
    if d < 30:
        return f"{d}d ago"
    if d < 365:
        return f"{d // 30}mo ago"
    return f"{d // 365}y ago"


def badge(now, pushed, created):
    if not pushed:
        return ""
    days = (now - pushed).days
    dot = "🟢" if days <= 7 else "🟡" if days <= 30 else "⚪"
    new = " 🆕" if created and (now - created).days <= 30 else ""
    return f" <sub>{dot} {ago(now, pushed)}{new}</sub>"


def build(cfg, login, repos, now):
    def find(ref):
        key = (ref if "/" in ref else f"{login}/{ref}").lower()
        return repos.get(key)

    items, listed = [], set()
    for it in cfg["items"]:
        found = [r for r in (find(x) for x in it.get("repos", [])) if r]
        listed.update(r["nameWithOwner"].lower() for r in found)
        pushed = max((parse_time(r["pushedAt"]) for r in found if r["pushedAt"]), default=None)
        created = max((parse_time(r["createdAt"]) for r in found), default=None) if len(found) == 1 else None
        items.append(dict(category=it["category"], title=it["title"], blurb=it["blurb"],
                          pushed=pushed, created=created, url=None))

    # Opt-in auto-discovery via topics.
    cats = set(cfg["categories"])
    for key, r in repos.items():
        if key in listed or r["isFork"] or r["isArchived"]:
            continue
        topics = {n["topic"]["name"] for n in r["repositoryTopics"]["nodes"]}
        if "showcase" not in topics:
            continue
        cat = next((c for c in cfg["categories"] if c in topics), "product")
        if cat not in cats:
            continue
        items.append(dict(category=cat, title=html.escape(r["name"]),
                          blurb=html.escape(r["description"] or "new project — details soon"),
                          pushed=parse_time(r["pushedAt"]), created=parse_time(r["createdAt"]),
                          url=None if r["isPrivate"] else r["url"]))

    epoch = dt.datetime(1970, 1, 1, tzinfo=dt.timezone.utc)

    def cell(cat):
        rows = sorted((i for i in items if i["category"] == cat),
                      key=lambda i: i["pushed"] or epoch, reverse=True)
        active = sum(1 for i in rows if i["pushed"] and (now - i["pushed"]).days <= 7)
        head = f'<h4>{cfg["categories"][cat]}'
        head += f' <sub>· {active} active this week</sub></h4>' if active else "</h4>"
        lines = []
        for i in rows:
            name = f'<a href="{i["url"]}"><b>{i["title"]}</b></a>' if i["url"] else f'<b>{i["title"]}</b>'
            lines.append(f'      {name} — {i["blurb"]}{badge(now, i["pushed"], i["created"])}')
        return "    <td width=\"50%\">\n      " + head + "\n" + "<br/>\n".join(lines) + "\n    </td>"

    out = ["<table>"]
    for row in cfg["layout"]:
        out.append('  <tr valign="top">')
        out.extend(cell(c) for c in row)
        out.append("  </tr>")
    out.append("</table>")
    out.append("")
    out.append("<sub>🔒 Most of this lives in private &amp; organisation repos — happy to demo any of it on a call."
               f" &nbsp;·&nbsp; 🟢 pushed this week &nbsp;🟡 this month &nbsp;⚪ earlier &nbsp;🆕 new"
               f" &nbsp;·&nbsp; auto-updated {now.date().isoformat()}</sub>")
    return "\n".join(out), len(items)


def main():
    token = os.environ.get("STATS_TOKEN", "").strip()
    if not token:
        sys.exit("STATS_TOKEN secret is not set.")
    raw = os.environ.get("SHOWCASE_CONFIG", "").strip()
    if not raw:
        sys.exit("SHOWCASE_CONFIG secret is not set.")
    try:
        cfg = json.loads(raw)
    except json.JSONDecodeError as e:  # report position only, never the content
        sys.exit(f"SHOWCASE_CONFIG is not valid JSON (line {e.lineno}, column {e.colno}).")
    now = dt.datetime.now(dt.timezone.utc)
    login, repos = fetch_repos(token)
    section, count = build(cfg, login, repos, now)

    with open(README, encoding="utf-8") as f:
        readme = f.read()
    pattern = re.compile(re.escape(START) + r".*?" + re.escape(END), re.S)
    if not pattern.search(readme):
        sys.exit("Mission log markers not found in README.md.")
    readme = pattern.sub(lambda _: f"{START}\n{section}\n{END}", readme)
    with open(README, "w", encoding="utf-8") as f:
        f.write(readme)
    print(f"Mission log rebuilt: {count} projects.")


if __name__ == "__main__":
    main()
