#!/usr/bin/env bash
# test-real-repo.sh — end-to-end: create remote, local clone, simulate pull
set -o pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
SCRIPT="$SCRIPT_DIR/scripts/git-batch-sync.sh"

TMP=$(mktemp -d)
trap "rm -rf $TMP" EXIT

# Bare remote (force main as default to avoid git version differences)
git init --bare -q --initial-branch=main "$TMP/remote.git"

# Local clone with initial commit
git clone -q "$TMP/remote.git" "$TMP/local"
cd "$TMP/local"
git -c user.email=t@t -c user.name=t commit -q --allow-empty -m "local init"
git push -q -u origin HEAD
BR=$(git symbolic-ref --short HEAD)

# Add incoming commit to remote (different working copy)
git clone -q "$TMP/remote.git" "$TMP/writer"
cd "$TMP/writer"
git -c user.email=t@t -c user.name=t commit -q --allow-empty -m "remote update"
git push -q

# Now run the skill against TMP (parent of 'local')
cd "$TMP"
LOGF=$(mktemp)
bash "$SCRIPT" "$TMP" >"$LOGF" 2>&1
rc=$?
out=$(cat "$LOGF")
rm -f "$LOGF"

if [ $rc -ne 0 ]; then
  echo "✗ exit $rc (expected 0)"
  echo "$out" | tail -30
  exit 1
fi
echo "✓ exit 0"

if ! grep -q "Updated        : 1" <<< "$out"; then
  echo "✗ expected 'Updated : 1'"
  echo "$out" | tail -30
  exit 1
fi
echo "✓ 1 repo updated"

# Verify local has the new commit (HEAD == origin/<branch> after ff-only)
cd "$TMP/local"
git fetch -q origin
LOCAL_HEAD=$(git rev-parse HEAD)
BR=$(git symbolic-ref --short HEAD)
REMOTE_HEAD=$(git rev-parse "origin/$BR")

if [ "$LOCAL_HEAD" != "$REMOTE_HEAD" ]; then
  echo "✗ local HEAD ($LOCAL_HEAD) != origin/$BR ($REMOTE_HEAD)"
  echo "  local log:"
  git log --oneline | sed 's/^/    /'
  echo "  origin log:"
  git log --oneline "origin/$BR" | sed 's/^/    /'
  echo "  script output:"
  echo "$out" | tail -40 | sed 's/^/    /'
  exit 1
fi
echo "✓ local HEAD matches origin/$BR"

# grep -q + pipefail causes SIGPIPE in git log; disable pipefail briefly
set +o pipefail
if ! git log --oneline | grep -q "remote update"; then
  set -o pipefail
  echo "✗ local missing 'remote update' commit"
  echo "  log:"
  git log --oneline | sed 's/^/    /'
  exit 1
fi
set -o pipefail
echo "✓ local has remote commit"

echo "PASS"
