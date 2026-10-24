---- MODULE TrackerWrites ----
\* Two writers share one data directory. The CLI does not lock that directory.
\* A second writer is supposed to use its own directory
\* (AGENTS.md, docs/decisions/0001-tracker-files.md).
\*
\* record_attempt reads, then write_json replaces each file from that read
\* (scripts/control-integration-bee:158, write_json at 82, attempts at 187,
\* heatmap at 188, project at 190).
\* The streak write at line 189 is omitted. No property here reads streaks.
\* project writes progress.local.json from the tick object captured at the read
\* (record_attempt:190, mock-start:404).
\* cmd_tick re-reads attempts at the project call (scripts/control-integration-bee:363).
\* cmd_mock_finish re-reads ticks and attempts (scripts/control-integration-bee:427).
\* mock-start returns the open session when its read already shows one (line 386).
\*
\* Assumptions:
\*   Each writer begins at most one command. Finishing a mock that writer opened
\*   is a later step of that command's aftermath, not a second begin.
\*   One drill and one tag. Counts stand in for the JSON arrays.
\*   SymPy's pass or miss is an input.
\*   A crash is the process stopping between write_json calls. There is no resume.
\*   Break "none" is the code. "drop_gate" deletes the mock gate.
\*   "force_second_open" deletes the early return that refuses a second open mock.

EXTENDS Integers

CONSTANTS Break

ASSUME Break \in {"none", "drop_gate", "force_second_open"}

VARIABLES
  attempts, incorrect, heatAttempts, heatFails,
  tickSolid, projTick, projMistakes,
  openCount, scoredCount, ungated, openedOnce, mockCold,
  attemptCommits, mockCommits,
  pc, snapA, snapI, snapHA, snapHF, snapTick, snapOpen, snapScored,
  wantMiss, wantCold, begun, holder, didFinish

Writers == {"companion", "second"}

Pc == {"idle", "holdA", "wroteA", "wroteH", "holdM", "wroteM", "wroteTick", "wroteFinish"}

vars == <<
  attempts, incorrect, heatAttempts, heatFails,
  tickSolid, projTick, projMistakes,
  openCount, scoredCount, ungated, openedOnce, mockCold,
  attemptCommits, mockCommits,
  pc, snapA, snapI, snapHA, snapHF, snapTick, snapOpen, snapScored,
  wantMiss, wantCold, begun, holder, didFinish
>>

Count == 0..2

TypeOK ==
  /\ attempts \in Count
  /\ incorrect \in Count
  /\ heatAttempts \in Count
  /\ heatFails \in Count
  /\ tickSolid \in BOOLEAN
  /\ projTick \in BOOLEAN
  /\ projMistakes \in Count
  /\ openCount \in Count
  /\ scoredCount \in Count
  /\ ungated \in BOOLEAN
  /\ openedOnce \in BOOLEAN
  /\ mockCold \in BOOLEAN
  /\ attemptCommits \in Count
  /\ mockCommits \in Count
  /\ pc \in [Writers -> Pc]
  /\ snapA \in [Writers -> Count]
  /\ snapI \in [Writers -> Count]
  /\ snapHA \in [Writers -> Count]
  /\ snapHF \in [Writers -> Count]
  /\ snapTick \in [Writers -> BOOLEAN]
  /\ snapOpen \in [Writers -> Count]
  /\ snapScored \in [Writers -> Count]
  /\ wantMiss \in [Writers -> BOOLEAN]
  /\ wantCold \in [Writers -> BOOLEAN]
  /\ begun \in [Writers -> BOOLEAN]
  /\ holder \in [Writers -> BOOLEAN]
  /\ didFinish \in [Writers -> BOOLEAN]

Init ==
  /\ attempts = 0
  /\ incorrect = 0
  /\ heatAttempts = 0
  /\ heatFails = 0
  /\ tickSolid = FALSE
  /\ projTick = FALSE
  /\ projMistakes = 0
  /\ openCount = 0
  /\ scoredCount = 0
  /\ ungated = FALSE
  /\ openedOnce = FALSE
  /\ mockCold = FALSE
  /\ attemptCommits = 0
  /\ mockCommits = 0
  /\ pc = [w \in Writers |-> "idle"]
  /\ snapA = [w \in Writers |-> 0]
  /\ snapI = [w \in Writers |-> 0]
  /\ snapHA = [w \in Writers |-> 0]
  /\ snapHF = [w \in Writers |-> 0]
  /\ snapTick = [w \in Writers |-> FALSE]
  /\ snapOpen = [w \in Writers |-> 0]
  /\ snapScored = [w \in Writers |-> 0]
  /\ wantMiss = [w \in Writers |-> FALSE]
  /\ wantCold = [w \in Writers |-> FALSE]
  /\ begun = [w \in Writers |-> FALSE]
  /\ holder = [w \in Writers |-> FALSE]
  /\ didFinish = [w \in Writers |-> FALSE]

Idle == \A w \in Writers : pc[w] = "idle"

\* The attempts file holds every append that passed write_json.
NoLostAttempt == Idle => attemptCommits = attempts

\* After every writer is idle, the heatmap counts the attempts file.
IdleFilesAgree == Idle => heatAttempts = attempts /\ heatFails = incorrect

\* After every writer is idle, progress.local.json matches the tick file and the misses.
ProjectionMatches == Idle => projMistakes = incorrect /\ projTick = tickSolid

\* A mock file is non-empty only after a gated start.
MockGate == ~ungated

\* The mock file holds at most one open session.
AtMostOneOpen == openCount <= 1

\* A score is written only after some start appended a session.
ScoreAfterOpen == scoredCount = 0 \/ openedOnce

\* Heatmap fails do not exceed heatmap attempts.
HeatSane == heatFails <= heatAttempts

\* Incorrect rows are a subset of attempt rows.
AttemptSane == incorrect <= attempts

\* A mock start that reached the mock file is still there once every writer is idle.
NoLostMock == Idle => mockCommits <= openCount + scoredCount

BeginRecord(w, miss) ==
  /\ pc[w] = "idle" \* scripts/control-integration-bee:159
  /\ ~begun[w]
  /\ attemptCommits < 2
  /\ begun' = [begun EXCEPT ![w] = TRUE]
  /\ pc' = [pc EXCEPT ![w] = "holdA"]
  /\ snapA' = [snapA EXCEPT ![w] = attempts]
  /\ snapI' = [snapI EXCEPT ![w] = incorrect]
  /\ snapHA' = [snapHA EXCEPT ![w] = heatAttempts]
  /\ snapHF' = [snapHF EXCEPT ![w] = heatFails]
  /\ snapTick' = [snapTick EXCEPT ![w] = tickSolid]
  /\ wantMiss' = [wantMiss EXCEPT ![w] = miss]
  /\ UNCHANGED <<
       attempts, incorrect, heatAttempts, heatFails,
       tickSolid, projTick, projMistakes,
       openCount, scoredCount, ungated, openedOnce, mockCold,
       attemptCommits, mockCommits,
       snapOpen, snapScored, wantCold, holder, didFinish
     >>

WriteAttempts(w) ==
  /\ pc[w] = "holdA" \* scripts/control-integration-bee:187
  /\ attempts' = snapA[w] + 1
  /\ incorrect' = snapI[w] + IF wantMiss[w] THEN 1 ELSE 0
  /\ attemptCommits' = attemptCommits + 1
  /\ pc' = [pc EXCEPT ![w] = "wroteA"]
  /\ UNCHANGED <<
       heatAttempts, heatFails, tickSolid, projTick, projMistakes,
       openCount, scoredCount, ungated, openedOnce, mockCold, mockCommits,
       snapA, snapI, snapHA, snapHF, snapTick, snapOpen, snapScored,
       wantMiss, wantCold, begun, holder, didFinish
     >>

WriteHeat(w) ==
  /\ pc[w] = "wroteA" \* scripts/control-integration-bee:188
  /\ heatAttempts' = snapHA[w] + 1
  /\ heatFails' = snapHF[w] + IF wantMiss[w] THEN 1 ELSE 0
  /\ pc' = [pc EXCEPT ![w] = "wroteH"]
  /\ UNCHANGED <<
       attempts, incorrect, tickSolid, projTick, projMistakes,
       openCount, scoredCount, ungated, openedOnce, mockCold,
       attemptCommits, mockCommits,
       snapA, snapI, snapHA, snapHF, snapTick, snapOpen, snapScored,
       wantMiss, wantCold, begun, holder, didFinish
     >>

ProjectRecord(w) ==
  /\ pc[w] = "wroteH" \* scripts/control-integration-bee:190
  /\ projMistakes' = snapI[w] + IF wantMiss[w] THEN 1 ELSE 0
  /\ projTick' = snapTick[w]
  /\ pc' = [pc EXCEPT ![w] = "idle"]
  /\ snapA' = [snapA EXCEPT ![w] = 0]
  /\ snapI' = [snapI EXCEPT ![w] = 0]
  /\ snapHA' = [snapHA EXCEPT ![w] = 0]
  /\ snapHF' = [snapHF EXCEPT ![w] = 0]
  /\ snapTick' = [snapTick EXCEPT ![w] = FALSE]
  /\ snapOpen' = [snapOpen EXCEPT ![w] = 0]
  /\ snapScored' = [snapScored EXCEPT ![w] = 0]
  /\ wantMiss' = [wantMiss EXCEPT ![w] = FALSE]
  /\ wantCold' = [wantCold EXCEPT ![w] = FALSE]
  /\ UNCHANGED <<
       attempts, incorrect, heatAttempts, heatFails, tickSolid,
       openCount, scoredCount, ungated, openedOnce, mockCold,
       attemptCommits, mockCommits, begun, holder, didFinish
     >>

Crash(w) ==
  /\ pc[w] # "idle"
  /\ pc' = [pc EXCEPT ![w] = "idle"]
  /\ snapA' = [snapA EXCEPT ![w] = 0]
  /\ snapI' = [snapI EXCEPT ![w] = 0]
  /\ snapHA' = [snapHA EXCEPT ![w] = 0]
  /\ snapHF' = [snapHF EXCEPT ![w] = 0]
  /\ snapTick' = [snapTick EXCEPT ![w] = FALSE]
  /\ snapOpen' = [snapOpen EXCEPT ![w] = 0]
  /\ snapScored' = [snapScored EXCEPT ![w] = 0]
  /\ wantMiss' = [wantMiss EXCEPT ![w] = FALSE]
  /\ wantCold' = [wantCold EXCEPT ![w] = FALSE]
  /\ UNCHANGED <<
       attempts, incorrect, heatAttempts, heatFails,
       tickSolid, projTick, projMistakes,
       openCount, scoredCount, ungated, openedOnce, mockCold,
       attemptCommits, mockCommits, begun, holder, didFinish
     >>

BeginTick(w) ==
  /\ pc[w] = "idle" \* scripts/control-integration-bee:357
  /\ ~begun[w]
  /\ ~tickSolid
  /\ begun' = [begun EXCEPT ![w] = TRUE]
  /\ tickSolid' = TRUE
  /\ pc' = [pc EXCEPT ![w] = "wroteTick"]
  /\ UNCHANGED <<
       attempts, incorrect, heatAttempts, heatFails,
       projTick, projMistakes,
       openCount, scoredCount, ungated, openedOnce, mockCold,
       attemptCommits, mockCommits,
       snapA, snapI, snapHA, snapHF, snapTick, snapOpen, snapScored,
       wantMiss, wantCold, holder, didFinish
     >>

ProjectTick(w) ==
  /\ pc[w] = "wroteTick" \* scripts/control-integration-bee:363
  /\ projTick' = TRUE
  /\ projMistakes' = incorrect
  /\ pc' = [pc EXCEPT ![w] = "idle"]
  /\ snapA' = [snapA EXCEPT ![w] = 0]
  /\ snapI' = [snapI EXCEPT ![w] = 0]
  /\ snapHA' = [snapHA EXCEPT ![w] = 0]
  /\ snapHF' = [snapHF EXCEPT ![w] = 0]
  /\ snapTick' = [snapTick EXCEPT ![w] = FALSE]
  /\ snapOpen' = [snapOpen EXCEPT ![w] = 0]
  /\ snapScored' = [snapScored EXCEPT ![w] = 0]
  /\ wantMiss' = [wantMiss EXCEPT ![w] = FALSE]
  /\ wantCold' = [wantCold EXCEPT ![w] = FALSE]
  /\ UNCHANGED <<
       attempts, incorrect, heatAttempts, heatFails, tickSolid,
       openCount, scoredCount, ungated, openedOnce, mockCold,
       attemptCommits, mockCommits, begun, holder, didFinish
     >>

BeginMockReady(w) ==
  /\ pc[w] = "idle" \* verify/model.py:33
  /\ ~begun[w]
  /\ tickSolid
  /\ mockCommits < 2
  /\ begun' = [begun EXCEPT ![w] = TRUE]
  /\ pc' = [pc EXCEPT ![w] = "holdM"]
  /\ snapOpen' = [snapOpen EXCEPT ![w] = openCount]
  /\ snapScored' = [snapScored EXCEPT ![w] = scoredCount]
  /\ snapTick' = [snapTick EXCEPT ![w] = tickSolid]
  /\ wantCold' = [wantCold EXCEPT ![w] = FALSE]
  /\ UNCHANGED <<
       attempts, incorrect, heatAttempts, heatFails,
       tickSolid, projTick, projMistakes,
       openCount, scoredCount, ungated, openedOnce, mockCold,
       attemptCommits, mockCommits,
       snapA, snapI, snapHA, snapHF, wantMiss, holder, didFinish
     >>

BeginMockCold(w) ==
  /\ pc[w] = "idle" \* scripts/control-integration-bee:381
  /\ ~begun[w]
  /\ ~tickSolid
  /\ mockCommits < 2
  /\ begun' = [begun EXCEPT ![w] = TRUE]
  /\ pc' = [pc EXCEPT ![w] = "holdM"]
  /\ snapOpen' = [snapOpen EXCEPT ![w] = openCount]
  /\ snapScored' = [snapScored EXCEPT ![w] = scoredCount]
  /\ snapTick' = [snapTick EXCEPT ![w] = tickSolid]
  /\ wantCold' = [wantCold EXCEPT ![w] = TRUE]
  /\ UNCHANGED <<
       attempts, incorrect, heatAttempts, heatFails,
       tickSolid, projTick, projMistakes,
       openCount, scoredCount, ungated, openedOnce, mockCold,
       attemptCommits, mockCommits,
       snapA, snapI, snapHA, snapHF, wantMiss, holder, didFinish
     >>

BeginMockUngated(w) ==
  /\ Break = "drop_gate"
  /\ pc[w] = "idle" \* verify/model.py:33
  /\ ~begun[w]
  /\ ~tickSolid
  /\ mockCommits < 2
  /\ begun' = [begun EXCEPT ![w] = TRUE]
  /\ pc' = [pc EXCEPT ![w] = "holdM"]
  /\ snapOpen' = [snapOpen EXCEPT ![w] = openCount]
  /\ snapScored' = [snapScored EXCEPT ![w] = scoredCount]
  /\ snapTick' = [snapTick EXCEPT ![w] = FALSE]
  /\ wantCold' = [wantCold EXCEPT ![w] = FALSE]
  /\ UNCHANGED <<
       attempts, incorrect, heatAttempts, heatFails,
       tickSolid, projTick, projMistakes,
       openCount, scoredCount, ungated, openedOnce, mockCold,
       attemptCommits, mockCommits,
       snapA, snapI, snapHA, snapHF, wantMiss, holder, didFinish
     >>

WriteMockKeep(w) ==
  /\ pc[w] = "holdM" \* scripts/control-integration-bee:386
  /\ snapOpen[w] >= 1
  /\ Break # "force_second_open"
  /\ pc' = [pc EXCEPT ![w] = "idle"]
  /\ snapA' = [snapA EXCEPT ![w] = 0]
  /\ snapI' = [snapI EXCEPT ![w] = 0]
  /\ snapHA' = [snapHA EXCEPT ![w] = 0]
  /\ snapHF' = [snapHF EXCEPT ![w] = 0]
  /\ snapTick' = [snapTick EXCEPT ![w] = FALSE]
  /\ snapOpen' = [snapOpen EXCEPT ![w] = 0]
  /\ snapScored' = [snapScored EXCEPT ![w] = 0]
  /\ wantMiss' = [wantMiss EXCEPT ![w] = FALSE]
  /\ wantCold' = [wantCold EXCEPT ![w] = FALSE]
  /\ UNCHANGED <<
       attempts, incorrect, heatAttempts, heatFails,
       tickSolid, projTick, projMistakes,
       openCount, scoredCount, ungated, openedOnce, mockCold,
       attemptCommits, mockCommits, begun, holder, didFinish
     >>

WriteMockAppend(w) ==
  /\ pc[w] = "holdM" \* scripts/control-integration-bee:402
  /\ snapOpen[w] = 0 \/ Break = "force_second_open"
  /\ openCount' = IF snapOpen[w] >= 1 THEN snapOpen[w] + 1 ELSE 1
  /\ scoredCount' = snapScored[w]
  /\ ungated' = IF snapOpen[w] + snapScored[w] = 0
                THEN ~snapTick[w] /\ ~wantCold[w]
                ELSE ungated \/ (~snapTick[w] /\ ~wantCold[w])
  /\ openedOnce' = TRUE
  /\ mockCold' = IF snapOpen[w] + snapScored[w] = 0 THEN wantCold[w]
                 ELSE mockCold \/ wantCold[w]
  /\ mockCommits' = mockCommits + 1
  /\ holder' = IF snapOpen[w] = 0 THEN [x \in Writers |-> x = w]
               ELSE [holder EXCEPT ![w] = TRUE]
  /\ pc' = [pc EXCEPT ![w] = "wroteM"]
  /\ UNCHANGED <<
       attempts, incorrect, heatAttempts, heatFails,
       tickSolid, projTick, projMistakes, attemptCommits,
       snapA, snapI, snapHA, snapHF, snapTick, snapOpen, snapScored,
       wantMiss, wantCold, begun, didFinish
     >>

ProjectMock(w) ==
  /\ pc[w] = "wroteM" \* scripts/control-integration-bee:404
  /\ projTick' = snapTick[w]
  /\ projMistakes' = incorrect
  /\ pc' = [pc EXCEPT ![w] = "idle"]
  /\ snapA' = [snapA EXCEPT ![w] = 0]
  /\ snapI' = [snapI EXCEPT ![w] = 0]
  /\ snapHA' = [snapHA EXCEPT ![w] = 0]
  /\ snapHF' = [snapHF EXCEPT ![w] = 0]
  /\ snapTick' = [snapTick EXCEPT ![w] = FALSE]
  /\ snapOpen' = [snapOpen EXCEPT ![w] = 0]
  /\ snapScored' = [snapScored EXCEPT ![w] = 0]
  /\ wantMiss' = [wantMiss EXCEPT ![w] = FALSE]
  /\ wantCold' = [wantCold EXCEPT ![w] = FALSE]
  /\ UNCHANGED <<
       attempts, incorrect, heatAttempts, heatFails, tickSolid,
       openCount, scoredCount, ungated, openedOnce, mockCold,
       attemptCommits, mockCommits, begun, holder, didFinish
     >>

WriteFinish(w) ==
  /\ pc[w] = "idle" \* scripts/control-integration-bee:419
  /\ holder[w]
  /\ openCount >= 1
  /\ ~didFinish[w]
  /\ openCount' = openCount - 1
  /\ scoredCount' = scoredCount + 1
  /\ holder' = [holder EXCEPT ![w] = FALSE]
  /\ didFinish' = [didFinish EXCEPT ![w] = TRUE]
  /\ pc' = [pc EXCEPT ![w] = "wroteFinish"]
  /\ UNCHANGED <<
       attempts, incorrect, heatAttempts, heatFails,
       tickSolid, projTick, projMistakes,
       ungated, openedOnce, mockCold,
       attemptCommits, mockCommits,
       snapA, snapI, snapHA, snapHF, snapTick, snapOpen, snapScored,
       wantMiss, wantCold, begun
     >>

ProjectFinish(w) ==
  /\ pc[w] = "wroteFinish" \* scripts/control-integration-bee:427
  /\ projTick' = tickSolid
  /\ projMistakes' = incorrect
  /\ pc' = [pc EXCEPT ![w] = "idle"]
  /\ snapA' = [snapA EXCEPT ![w] = 0]
  /\ snapI' = [snapI EXCEPT ![w] = 0]
  /\ snapHA' = [snapHA EXCEPT ![w] = 0]
  /\ snapHF' = [snapHF EXCEPT ![w] = 0]
  /\ snapTick' = [snapTick EXCEPT ![w] = FALSE]
  /\ snapOpen' = [snapOpen EXCEPT ![w] = 0]
  /\ snapScored' = [snapScored EXCEPT ![w] = 0]
  /\ wantMiss' = [wantMiss EXCEPT ![w] = FALSE]
  /\ wantCold' = [wantCold EXCEPT ![w] = FALSE]
  /\ UNCHANGED <<
       attempts, incorrect, heatAttempts, heatFails, tickSolid,
       openCount, scoredCount, ungated, openedOnce, mockCold,
       attemptCommits, mockCommits, begun, holder, didFinish
     >>

Next ==
  \/ \E w \in Writers : \E miss \in BOOLEAN : BeginRecord(w, miss)
  \/ \E w \in Writers : WriteAttempts(w)
  \/ \E w \in Writers : WriteHeat(w)
  \/ \E w \in Writers : ProjectRecord(w)
  \/ \E w \in Writers : Crash(w)
  \/ \E w \in Writers : BeginTick(w)
  \/ \E w \in Writers : ProjectTick(w)
  \/ \E w \in Writers : BeginMockReady(w)
  \/ \E w \in Writers : BeginMockCold(w)
  \/ \E w \in Writers : BeginMockUngated(w)
  \/ \E w \in Writers : WriteMockKeep(w)
  \/ \E w \in Writers : WriteMockAppend(w)
  \/ \E w \in Writers : ProjectMock(w)
  \/ \E w \in Writers : WriteFinish(w)
  \/ \E w \in Writers : ProjectFinish(w)

Spec == Init /\ [][Next]_vars

====
