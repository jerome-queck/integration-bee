---- MODULE SessionFlow ----
\* One companion session for one Round 1 node.
\*
\* The companion skill is the protocol. The CLI is the writer.
\* A solid tick follows two distinct correct drills (verify/turn_contract.py:398).
\* A photo miss goes through turn apply, which calls record_attempt (scripts/control-integration-bee:579).
\* A mock starts only when mock_block_reason allows it (verify/model.py:32,
\* scripts/control-integration-bee:400), unless the learner asked for --cold.
\* A score is stored by mock-finish (scripts/control-integration-bee:445).
\*
\* Assumptions:
\*   One node stands in for the Round 1 gate. mock_block_reason is all-or-nothing.
\*   SymPy is an input (pass or miss), not a model of algebra.
\*   learning and skipped ticks are out of this spec. Only the solid gate tick is here.
\*   One photo miss and one incorrect check are enough to see the queues.
\*   Break selects a planted hole. The pass config sets Break to "none".

EXTENDS Integers

CONSTANTS Break

ASSUME Break \in {
  "none",
  "tick_early",
  "mock_ungated",
  "forget_weak",
  "score_without_open"
}

VARIABLES
  screen,
  taught,
  correct,
  weak,
  due,
  tickSolid,
  mock,
  coldAsked,
  coldUsed,
  mistakeRows,
  checkMisses,
  refused,
  opened

vars == <<
  screen, taught, correct, weak, due, tickSolid, mock,
  coldAsked, coldUsed, mistakeRows, checkMisses, refused, opened
>>

Screens == {
  "idle", "teaching", "drilling", "checked", "ticked",
  "marking", "mistaken", "mock_open", "mock_scored"
}

TypeOK ==
  /\ screen \in Screens
  /\ taught \in BOOLEAN
  /\ correct \in 0..2
  /\ weak \in BOOLEAN
  /\ due \in BOOLEAN
  /\ tickSolid \in BOOLEAN
  /\ mock \in {"none", "open", "scored"}
  /\ coldAsked \in BOOLEAN
  /\ coldUsed \in BOOLEAN
  /\ mistakeRows \in 0..1
  /\ checkMisses \in 0..1
  /\ refused \in BOOLEAN
  /\ opened \in BOOLEAN
  /\ mock = "open" => screen = "mock_open"
  /\ mock = "scored" => screen = "mock_scored"
  /\ coldUsed => coldAsked

Init ==
  /\ screen = "idle"
  /\ taught = FALSE
  /\ correct = 0
  /\ weak = FALSE
  /\ due = FALSE
  /\ tickSolid = FALSE
  /\ mock = "none"
  /\ coldAsked = FALSE
  /\ coldUsed = FALSE
  /\ mistakeRows = 0
  /\ checkMisses = 0
  /\ refused = FALSE
  /\ opened = FALSE

Teach ==
  /\ screen = "idle" \* .cursor/skills/integration-bee-companion/SKILL.md:22
  /\ ~taught
  /\ screen' = "teaching"
  /\ taught' = TRUE
  /\ refused' = FALSE
  /\ UNCHANGED <<correct, weak, due, tickSolid, mock, coldAsked, coldUsed, mistakeRows, checkMisses, opened>>

OfferDrill ==
  /\ taught \* .cursor/skills/integration-bee-companion/SKILL.md:24
  /\ screen \in {"teaching", "checked", "mistaken"}
  /\ screen # "checked" \/ correct < 2
  /\ screen' = "drilling"
  /\ UNCHANGED <<taught, correct, weak, due, tickSolid, mock, coldAsked, coldUsed, mistakeRows, checkMisses, refused, opened>>

CheckPass ==
  /\ screen = "drilling" \* scripts/control-integration-bee:313
  /\ correct < 2
  /\ correct' = correct + 1
  /\ screen' = "checked"
  /\ UNCHANGED <<taught, weak, due, tickSolid, mock, coldAsked, coldUsed, mistakeRows, checkMisses, refused, opened>>

CheckMiss ==
  /\ screen = "drilling" \* scripts/control-integration-bee:313
  /\ checkMisses = 0
  /\ checkMisses' = 1
  /\ weak' = TRUE \* verify/model.py:166
  /\ due' = TRUE \* verify/model.py:127
  /\ screen' = "checked"
  /\ UNCHANGED <<taught, correct, tickSolid, mock, coldAsked, coldUsed, mistakeRows, refused, opened>>

TickAfterTwo ==
  /\ screen = "checked" \* verify/turn_contract.py:398
  /\ correct = 2
  /\ ~tickSolid
  /\ tickSolid' = TRUE
  /\ screen' = "ticked"
  /\ UNCHANGED <<taught, correct, weak, due, mock, coldAsked, coldUsed, mistakeRows, checkMisses, refused, opened>>

TickEarly ==
  /\ Break = "tick_early"
  /\ taught \* verify/turn_contract.py:398
  /\ ~tickSolid
  /\ screen \in {"teaching", "drilling", "checked"}
  /\ correct < 2
  /\ tickSolid' = TRUE
  /\ screen' = "ticked"
  /\ UNCHANGED <<taught, correct, weak, due, mock, coldAsked, coldUsed, mistakeRows, checkMisses, refused, opened>>

MarkPhoto ==
  /\ screen \in {"idle", "teaching"} \* .cursor/skills/integration-bee-companion/SKILL.md:28
  /\ mistakeRows = 0
  /\ screen' = "marking"
  /\ UNCHANGED <<taught, correct, weak, due, tickSolid, mock, coldAsked, coldUsed, mistakeRows, checkMisses, refused, opened>>

RecordMistake ==
  /\ screen = "marking" \* scripts/control-integration-bee:579
  /\ mistakeRows' = 1
  /\ weak' = IF Break = "forget_weak" THEN weak ELSE TRUE
  /\ due' = IF Break = "forget_weak" THEN due ELSE TRUE
  /\ screen' = "mistaken"
  /\ UNCHANGED <<taught, correct, tickSolid, mock, coldAsked, coldUsed, checkMisses, refused, opened>>

AskCold ==
  /\ ~coldAsked \* .cursor/skills/integration-bee-companion/SKILL.md:32
  /\ mock = "none"
  /\ screen \in {"idle", "teaching", "checked", "mistaken", "drilling"}
  /\ coldAsked' = TRUE
  /\ refused' = FALSE
  /\ UNCHANGED <<screen, taught, correct, weak, due, tickSolid, mock, coldUsed, mistakeRows, checkMisses, opened>>

MockStartReady ==
  /\ tickSolid \* verify/model.py:33
  /\ mock = "none"
  /\ screen \in {"ticked", "mistaken"}
  /\ mock' = "open"
  /\ opened' = TRUE
  /\ coldUsed' = FALSE
  /\ screen' = "mock_open"
  /\ refused' = FALSE
  /\ UNCHANGED <<taught, correct, weak, due, tickSolid, coldAsked, mistakeRows, checkMisses>>

MockStartCold ==
  /\ coldAsked \* scripts/control-integration-bee:403
  /\ ~tickSolid
  /\ mock = "none"
  /\ screen \in {"idle", "teaching", "checked", "mistaken"}
  /\ mock' = "open"
  /\ opened' = TRUE
  /\ coldUsed' = TRUE
  /\ screen' = "mock_open"
  /\ refused' = FALSE
  /\ UNCHANGED <<taught, correct, weak, due, tickSolid, coldAsked, mistakeRows, checkMisses>>

MockStartUngated ==
  /\ Break = "mock_ungated"
  /\ ~tickSolid \* verify/model.py:33
  /\ ~coldAsked
  /\ mock = "none"
  /\ screen \in {"idle", "teaching", "checked", "mistaken"}
  /\ mock' = "open"
  /\ opened' = TRUE
  /\ coldUsed' = FALSE
  /\ screen' = "mock_open"
  /\ refused' = FALSE
  /\ UNCHANGED <<taught, correct, weak, due, tickSolid, coldAsked, mistakeRows, checkMisses>>

MockRefuse ==
  /\ Break # "mock_ungated"
  /\ ~tickSolid \* scripts/control-integration-bee:406
  /\ ~coldAsked
  /\ mock = "none"
  /\ ~refused
  /\ screen \in {"idle", "teaching", "checked", "mistaken"}
  /\ refused' = TRUE
  /\ UNCHANGED <<screen, taught, correct, weak, due, tickSolid, mock, coldAsked, coldUsed, mistakeRows, checkMisses, opened>>

MockScore ==
  /\ mock = "open" \* scripts/control-integration-bee:445
  /\ opened
  /\ mock' = "scored"
  /\ screen' = "mock_scored"
  /\ UNCHANGED <<taught, correct, weak, due, tickSolid, coldAsked, coldUsed, mistakeRows, checkMisses, refused, opened>>

ScoreWithoutOpen ==
  /\ Break = "score_without_open"
  /\ tickSolid \* scripts/control-integration-bee:445
  /\ mock = "none"
  /\ ~opened
  /\ mock' = "scored"
  /\ screen' = "mock_scored"
  /\ UNCHANGED <<taught, correct, weak, due, tickSolid, coldAsked, coldUsed, mistakeRows, checkMisses, refused, opened>>

Next ==
  \/ Teach
  \/ OfferDrill
  \/ CheckPass
  \/ CheckMiss
  \/ TickAfterTwo
  \/ TickEarly
  \/ MarkPhoto
  \/ RecordMistake
  \/ AskCold
  \/ MockStartReady
  \/ MockStartCold
  \/ MockStartUngated
  \/ MockRefuse
  \/ MockScore
  \/ ScoreWithoutOpen

Spec == Init /\ [][Next]_vars

\* A solid tick follows two correct drills for that node.
\* verify/turn_contract.py:398
TwoCorrectBeforeSolid == tickSolid => correct = 2

\* A stored mock was started with every Round 1 node solid, or with --cold.
\* verify/model.py:32
MockGate == mock = "none" \/ tickSolid \/ coldUsed

\* A photo miss appends a mistake and marks that tag weak and due.
\* scripts/control-integration-bee:579
MistakeQueuesWeak == mistakeRows = 0 \/ (weak /\ due)

\* An incorrect SymPy check marks the tag weak and puts the drill on the spaced queue.
\* scripts/control-integration-bee:313
MissQueuesReview == checkMisses = 0 \/ (weak /\ due)

\* A stored score follows an opened mock.
\* scripts/control-integration-bee:436
ScoreAfterOpen == mock # "scored" \/ opened

====
