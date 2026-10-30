"""Fetch live GitHub contribution numbers and regenerate the profile SVGs.

Security notes
- Standard library only (no third-party packages to trust).
- The token is read from the STATS_TOKEN environment variable, sent only to
  api.github.com over HTTPS, and never printed or written to disk.
- Only aggregate counts are saved (assets/stats.json); no repo names are exposed.
"""
import datetime as dt
import json
import os
import subprocess
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATS = os.path.join(ROOT, "assets", "stats.json")

QUERY = """
query($yfrom: DateTime!, $mfrom: DateTime!, $to: DateTime!) {
  viewer {
    year: contributionsCollection(from: $yfrom, to: $to) {
      contributionCalendar { totalContributions }
    }
    month: contributionsCollection(from: $mfrom, to: $to) {
      totalCommitContributions
      totalPullRequestContributions
      totalRepositoriesWithContributedCommits
      totalRepositoriesWithContributedPullRequests
    }
  }
}
"""


def main():
    token = os.environ.get("STATS_TOKEN", "").strip()
    if not token:
        sys.exit("STATS_TOKEN secret is not set - add it under Settings > Secrets and variables > Actions.")

    now = dt.datetime.now(dt.timezone.utc).replace(microsecond=0)
    variables = {
        "yfrom": (now - dt.timedelta(days=365)).isoformat(),
        "mfrom": (now - dt.timedelta(days=30)).isoformat(),
        "to": now.isoformat(),
    }
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": variables}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json",
                 "User-Agent": "profile-stats-updater"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            payload = json.load(resp)
    except urllib.error.HTTPError as e:  # never echo headers (they hold the token)
        sys.exit(f"GitHub API request failed with HTTP {e.code}. Check the token is valid and not expired.")

    if payload.get("errors"):
        sys.exit("GitHub API returned an error: " + "; ".join(x.get("message", "?") for x in payload["errors"]))

    v = payload["data"]["viewer"]
    m = v["month"]
    stats = {
        "year_contributions": v["year"]["contributionCalendar"]["totalContributions"],
        "commits_30d": m["totalCommitContributions"],
        "prs_30d": m["totalPullRequestContributions"],
        "repos_30d": max(m["totalRepositoriesWithContributedCommits"],
                         m["totalRepositoriesWithContributedPullRequests"]),
        "updated": now.date().isoformat(),
    }
    with open(STATS, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)
        f.write("\n")
    print("Updated stats:", json.dumps(stats))

    subprocess.run([sys.executable, os.path.join(ROOT, "assets", "gen.py")], check=True)


if __name__ == "__main__":
    main()
