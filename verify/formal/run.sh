#!/usr/bin/env bash
# TLC 1.7.4 on the learner-session specs, then the tracker repro.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
FORMAL="$ROOT/verify/formal"
CACHE="$FORMAL/.cache"
JAR="${TLA2TOOLS:-$CACHE/tla2tools.jar}"
META="$CACHE/tlc"
SHA=936a262061c914694dfd669a543be24573c45d5aa0ff20a8b96b23d01e050e88
mkdir -p "$META"

if ! command -v java >/dev/null 2>&1; then
  echo "FAIL formal: java is not on PATH. TLC 1.7.4 needs Java 11 or newer."
  exit 1
fi

if [[ ! -f "$JAR" ]]; then
  echo "download TLC 1.7.4"
  curl -fsSL -o "$JAR.partial" "https://github.com/tlaplus/tlaplus/releases/download/v1.7.4/tla2tools.jar"
  mv "$JAR.partial" "$JAR"
fi
echo "$SHA  $JAR" | sha256sum -c -

tlc() {
  java -XX:+UseParallelGC -Xmx512m -cp "$JAR" tlc2.TLC \
    -deadlock -nowarning -workers 1 -cleanup -metadir "$META" "$@"
}

cd "$FORMAL"

pass() {
  echo "== pass $1 =="
  tlc -config "$1" "$2"
}

fail() {
  local cfg="$1" spec="$2" name="$3"
  local out code
  echo "== expect $name =="
  set +e
  out="$(tlc -config "$cfg" "$spec" 2>&1)"
  code=$?
  set -e
  if [[ "$code" -eq 0 ]]; then
    echo "FAIL $name was not caught"
    printf '%s\n' "$out" | tail -20
    exit 1
  fi
  if ! grep -q "Invariant $name is violated" <<<"$out"; then
    echo "FAIL $name: TLC did not report that invariant"
    printf '%s\n' "$out" | tail -30
    exit 1
  fi
  echo "PASS caught $name"
}

pass SessionFlow.cfg SessionFlow.tla
fail SessionFlow.tick-early.cfg SessionFlow.tla TwoCorrectBeforeSolid
fail SessionFlow.mock-ungated.cfg SessionFlow.tla MockGate
fail SessionFlow.forget-weak.cfg SessionFlow.tla MistakeQueuesWeak
fail SessionFlow.score-without-open.cfg SessionFlow.tla ScoreAfterOpen

pass TrackerWrites.cfg TrackerWrites.tla
fail TrackerWrites.lost-attempt.cfg TrackerWrites.tla NoLostAttempt
fail TrackerWrites.torn-heat.cfg TrackerWrites.tla IdleFilesAgree
fail TrackerWrites.stale-progress.cfg TrackerWrites.tla ProjectionMatches
fail TrackerWrites.lost-mock.cfg TrackerWrites.tla NoLostMock
fail TrackerWrites.drop-gate.cfg TrackerWrites.tla MockGate
fail TrackerWrites.second-open.cfg TrackerWrites.tla AtMostOneOpen

SKILL="$ROOT/.cursor/skills/formal-verify-integration-bee/SKILL.md"
expect_blob() {
  local key="$1" file="$2" want got
  want="$(git -C "$ROOT" hash-object "$file")"
  got="$(awk -v k="$key" '$1 == k":" { print $2; exit }' "$SKILL")"
  if [[ "$got" != "$want" ]]; then
    echo "FAIL $key is '$got', blob of $file is $want"
    exit 1
  fi
  echo "PASS $key $want"
}
expect_blob session_flow_blob "$FORMAL/SessionFlow.tla"
expect_blob tracker_writes_blob "$FORMAL/TrackerWrites.tla"

expect_chart() {
  local mmd="$1" file="$2" want
  want="$(git -C "$ROOT" hash-object "$file")"
  if ! grep -q "tla-blob: $want" "$mmd"; then
    echo "FAIL $mmd is not stamped with tla-blob: $want"
    exit 1
  fi
  echo "PASS chart $mmd"
}
expect_chart "$FORMAL/charts/session-flow.mmd" "$FORMAL/SessionFlow.tla"
expect_chart "$FORMAL/charts/tracker-writes.mmd" "$FORMAL/TrackerWrites.tla"

python3 "$FORMAL/repro_tracker.py"
echo "PASS formal"
