#!/usr/bin/env bash
# Usage: ./publish-article.sh <slug> [--no-push]
# Moves marketing/articles/ready/<slug>.md into polished/, adds it to article_order,
# stamps published/updated, builds, checks for leftovers, commits and pushes main.
set -euo pipefail
SLUG="${1:?usage: publish-article.sh <slug> [--no-push]}"; PUSH=1; [ "${2:-}" = "--no-push" ] && PUSH=0
HUB="$(cd "$(dirname "$0")" && pwd)"; ART="$HUB/../marketing/articles"
PY="${HUB_PY:-/workspace/course/.venv-hub/bin/python}"
SRC="$ART/ready/$SLUG.md"; DST="$ART/polished/$SLUG.md"
cd "$HUB"
[ -f "$SRC" ] || { echo "no $SRC"; exit 1; }
[ "$(git rev-parse --abbrev-ref HEAD)" = "main" ] || [ "$PUSH" = 0 ] || { echo "not on main"; exit 1; }
[ -z "$(git status --porcelain | grep -v "^?? publish-article.sh$")" ] || { echo "hub repo has uncommitted changes, stopping"; exit 1; }
NOW="$(date +%Y-%m-%dT%H:%M:%S%:z)"
"$PY" - "$SRC" "$DST" "$SLUG" "$NOW" <<'PYEOF'
import sys, json, re, pathlib
src, dst, slug, now = sys.argv[1:]
t = pathlib.Path(src).read_text()
head, body = t.split("\n---\n", 1)
head = re.sub(r'^(published|updated):.*\n?', '', head, flags=re.M).rstrip("\n")
head += f'\npublished: "{now}"\nupdated: "{now}"'
pathlib.Path(dst).write_text(head + "\n---\n" + body)
c = pathlib.Path("config.json"); cfg = json.loads(c.read_text())
if slug not in cfg["article_order"]: cfg["article_order"].append(slug)
c.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n")
PYEOF
"$PY" build.py | tee /tmp/publish-build.log
PAGE="docs/$SLUG/index.html"
[ -f "$PAGE" ] || { echo "FAIL: $PAGE not built"; exit 1; }
if grep -nE '\{\{|\[NEEDS FACT|\[[A-Z_]{4,}\]|TODO|TBD' "$PAGE"; then echo "FAIL: placeholders in $PAGE (nothing committed)"; exit 1; fi
grep -q "og:image" "$PAGE" || { echo "FAIL: no og:image"; exit 1; }
git add -A
git commit -qm "Publish article: $SLUG"
echo "Committed: $(git log --oneline -1)"
if [ "$PUSH" = 1 ]; then git push origin main && echo "Pushed. Live soon at https://guide.circularsurrealism.com/$SLUG/"; else echo "--no-push: not pushed"; fi
