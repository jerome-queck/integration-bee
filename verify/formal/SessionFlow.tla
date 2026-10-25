---- MODULE SessionFlow ----
\* One companion session for one Round 1 node.
\*
\* The companion skill is the protocol. The CLI is the writer.
\* A solid tick follows two distinct correct drills
\* (verify/turn_contract.py distinct_correct at 609, the solid tick at 815).
\* A photo miss goes through turn apply, which calls record_attempt
\* (scripts/control-integration-bee finish_plan at 919, record_attempt at 322).
\* A photo mark may copy image to submissions/ before that write
\* (store_mark_photo at 264, called from turn apply at 1239).
\* The copy is outside this spec. A missing file writes no attempt.
\* A mock starts only when mock_block_reason allows it (verify/model.py:30),
\* unless the learner asked for cold. turn apply mock-start refuses an open
\* integral or a skip offer before that gate
\* (scripts/control-integration-bee:1095).
\* A second mock-start keeps an unscored mock
\* (progress mock-start at 691, turn mock-start at 1099).
\* This spec starts only from mock = "none". The keep path does not open another.
\* A score is stored by mock-finish (progress at 713, turn at 1123).
\* progress mock-finish refuses while an integral or a skip offer is open (717).
\* Those phases are other screens here, so MockScore does not fire during them.
\*
\* Placement is one aptitude cycle from the opening idle screen.
\* plan_aptitude (verify/turn_contract.py:832) opens one drill.
\* A correct mark stays in aptitude and opens the contest probe
\* (_finish_placement at 785). A correct contest mark proposes a skip.
\* plan_confirm (901) writes skipped only for an id in that offer.
\* An empty confirm writes no skip. plan_cover (935) sets full_coverage
\* and does not write solid. This spec takes that flag from idle,
\* aptitude, and proposing. The code also accepts cover during a drill
\* or a mock. That write is the same flag and does not change the gate.
\* The mock still needs the node solid (verify/model.py:30, coach_queue_done at 161).
\*
\* Assumptions:
\*   One node stands in for the Round 1 gate. mock_block_reason is all-or-nothing.
\*   The placement probe is one drill id plus one manual contest row.
\*   That one id does not reach two distinct drills, so it does not tick solid.
\*   A later aptitude after this cycle is the same plan_aptitude. This spec runs it once.
\*   SymPy is an input (pass or miss), not a model of algebra.
\*   learning ticks are out of this spec. skipped is the confirm write.
\*   Policy rows are out of this spec.
\*   One photo miss and one incorrect check are enough to see the queues.
\*   Break selects a planted hole. The pass config sets Break to "none".

EXTENDS Integers

CONSTANTS Break

ASSUME Break \in {
  "none",
  "tick_early",
  "mock_ungated",
  "forget_weak",
  "score_without_open",
  "confirm_anytime",
  "skip_as_solid"
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
  opened,
  placement,
  skipped,
  proposed,
  fullCoverage

vars == <<
  screen, taught, correct, weak, due, tickSolid, mock,
  coldAsked, coldUsed, mistakeRows, checkMisses, refused, opened,
  placement, skipped, proposed, fullCoverage
>>

Screens == {
  "idle", "teaching", "drilling", "checked", "ticked",
  "marking", "mistaken", "mock_open", "mock_scored",
  "aptitude", "proposing"
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
  /\ placement \in {"none", "drill", "catalog"}
  /\ skipped \in BOOLEAN
  /\ proposed \in BOOLEAN
  /\ fullCoverage \in BOOLEAN
  /\ mock = "open" => screen = "mock_open"
  /\ mock = "scored" => screen = "mock_scored"
  /\ coldUsed => coldAsked
  /\ screen = "aptitude" => placement \in {"drill", "catalog"}
  /\ screen # "aptitude" => placement = "none"
  /\ screen = "proposing" => proposed

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
  /\ placement = "none"
  /\ skipped = FALSE
  /\ proposed = FALSE
  /\ fullCoverage = FALSE

Teach ==
  /\ screen = "idle" \* .agents/skills/integration-bee-companion/SKILL.md:165
  /\ ~taught
  /\ ~skipped \/ fullCoverage \* verify/model.py:161
  /\ screen' = "teaching"
  /\ taught' = TRUE
  /\ refused' = FALSE
  /\ UNCHANGED <<correct, weak, due, tickSolid, mock, coldAsked, coldUsed, mistakeRows, checkMisses, opened, placement, skipped, proposed, fullCoverage>>

OfferDrill ==
  /\ taught \* verify/turn_contract.py:685
  /\ screen \in {"teaching", "checked", "mistaken"}
  /\ screen # "checked" \/ correct < 2
  /\ screen' = "drilling"
  /\ UNCHANGED <<taught, correct, weak, due, tickSolid, mock, coldAsked, coldUsed, mistakeRows, checkMisses, refused, opened, placement, skipped, proposed, fullCoverage>>

CheckPass ==
  /\ screen = "drilling" \* scripts/control-integration-bee:518
  /\ correct < 2
  /\ correct' = correct + 1
  /\ screen' = "checked"
  /\ UNCHANGED <<taught, weak, due, tickSolid, mock, coldAsked, coldUsed, mistakeRows, checkMisses, refused, opened, placement, skipped, proposed, fullCoverage>>

CheckMiss ==
  /\ screen = "drilling" \* scripts/control-integration-bee:518
  /\ checkMisses = 0
  /\ checkMisses' = 1
  /\ weak' = TRUE \* scripts/control-integration-bee:360
  /\ due' = TRUE \* verify/model.py:229
  /\ screen' = "checked"
  /\ UNCHANGED <<taught, correct, tickSolid, mock, coldAsked, coldUsed, mistakeRows, refused, opened, placement, skipped, proposed, fullCoverage>>

TickAfterTwo ==
  /\ screen = "checked" \* verify/turn_contract.py:815
  /\ correct = 2
  /\ ~tickSolid
  /\ tickSolid' = TRUE
  /\ skipped' = FALSE
  /\ screen' = "ticked"
  /\ UNCHANGED <<taught, correct, weak, due, mock, coldAsked, coldUsed, mistakeRows, checkMisses, refused, opened, placement, proposed, fullCoverage>>

TickEarly ==
  /\ Break = "tick_early"
  /\ taught \* verify/turn_contract.py:609
  /\ ~tickSolid
  /\ screen \in {"teaching", "drilling", "checked"}
  /\ correct < 2
  /\ tickSolid' = TRUE
  /\ screen' = "ticked"
  /\ UNCHANGED <<taught, correct, weak, due, mock, coldAsked, coldUsed, mistakeRows, checkMisses, refused, opened, placement, skipped, proposed, fullCoverage>>

MarkPhoto ==
  /\ screen \in {"idle", "teaching"} \* .agents/skills/integration-bee-companion/SKILL.md:177
  /\ mistakeRows = 0
  /\ screen' = "marking"
  /\ UNCHANGED <<taught, correct, weak, due, tickSolid, mock, coldAsked, coldUsed, mistakeRows, checkMisses, refused, opened, placement, skipped, proposed, fullCoverage>>

RecordMistake ==
  /\ screen = "marking" \* scripts/control-integration-bee:322
  /\ mistakeRows' = 1
  /\ weak' = IF Break = "forget_weak" THEN weak ELSE TRUE
  /\ due' = IF Break = "forget_weak" THEN due ELSE TRUE
  /\ screen' = "mistaken"
  /\ UNCHANGED <<taught, correct, tickSolid, mock, coldAsked, coldUsed, checkMisses, refused, opened, placement, skipped, proposed, fullCoverage>>

AskCold ==
  /\ ~coldAsked \* .agents/skills/integration-bee-companion/SKILL.md:193
  /\ mock = "none"
  /\ screen \in {"idle", "teaching", "checked", "mistaken", "drilling"}
  /\ coldAsked' = TRUE
  /\ refused' = FALSE
  /\ UNCHANGED <<screen, taught, correct, weak, due, tickSolid, mock, coldUsed, mistakeRows, checkMisses, opened, placement, skipped, proposed, fullCoverage>>

MockStartReady ==
  /\ tickSolid \* verify/model.py:30
  /\ mock = "none"
  /\ screen \in {"ticked", "mistaken"}
  /\ mock' = "open"
  /\ opened' = TRUE
  /\ coldUsed' = FALSE
  /\ screen' = "mock_open"
  /\ refused' = FALSE
  /\ UNCHANGED <<taught, correct, weak, due, tickSolid, coldAsked, mistakeRows, checkMisses, placement, skipped, proposed, fullCoverage>>

MockStartCold ==
  /\ coldAsked \* scripts/control-integration-bee:685
  /\ ~tickSolid
  /\ mock = "none"
  /\ screen \in {"idle", "teaching", "checked", "mistaken"}
  /\ mock' = "open"
  /\ opened' = TRUE
  /\ coldUsed' = TRUE
  /\ screen' = "mock_open"
  /\ refused' = FALSE
  /\ UNCHANGED <<taught, correct, weak, due, tickSolid, coldAsked, mistakeRows, checkMisses, placement, skipped, proposed, fullCoverage>>

MockStartUngated ==
  /\ Break = "mock_ungated"
  /\ ~tickSolid \* verify/model.py:30
  /\ ~coldAsked
  /\ mock = "none"
  /\ screen \in {"idle", "teaching", "checked", "mistaken"}
  /\ mock' = "open"
  /\ opened' = TRUE
  /\ coldUsed' = FALSE
  /\ screen' = "mock_open"
  /\ refused' = FALSE
  /\ UNCHANGED <<taught, correct, weak, due, tickSolid, coldAsked, mistakeRows, checkMisses, placement, skipped, proposed, fullCoverage>>

MockRefuse ==
  /\ Break # "mock_ungated"
  /\ ~tickSolid \* scripts/control-integration-bee:688
  /\ ~coldAsked
  /\ mock = "none"
  /\ ~refused
  /\ screen \in {"idle", "teaching", "checked", "mistaken"}
  /\ refused' = TRUE
  /\ UNCHANGED <<screen, taught, correct, weak, due, tickSolid, mock, coldAsked, coldUsed, mistakeRows, checkMisses, opened, placement, skipped, proposed, fullCoverage>>

MockScore ==
  /\ mock = "open" \* scripts/control-integration-bee:713
  /\ opened
  /\ mock' = "scored"
  /\ screen' = "mock_scored"
  /\ UNCHANGED <<taught, correct, weak, due, tickSolid, coldAsked, coldUsed, mistakeRows, checkMisses, refused, opened, placement, skipped, proposed, fullCoverage>>

ScoreWithoutOpen ==
  /\ Break = "score_without_open"
  /\ tickSolid \* scripts/control-integration-bee:713
  /\ mock = "none"
  /\ ~opened
  /\ mock' = "scored"
  /\ screen' = "mock_scored"
  /\ UNCHANGED <<taught, correct, weak, due, tickSolid, coldAsked, coldUsed, mistakeRows, checkMisses, refused, opened, placement, skipped, proposed, fullCoverage>>

StartAptitude ==
  /\ screen = "idle" \* verify/turn_contract.py:858
  /\ placement = "none"
  /\ ~proposed
  /\ ~skipped
  /\ screen' = "aptitude"
  /\ placement' = "drill"
  /\ UNCHANGED <<taught, correct, weak, due, tickSolid, mock, coldAsked, coldUsed, mistakeRows, checkMisses, refused, opened, skipped, proposed, fullCoverage>>

MarkAptitudePass ==
  /\ screen = "aptitude" \* verify/turn_contract.py:791
  /\ placement = "drill"
  /\ placement' = "catalog"
  /\ UNCHANGED <<screen, taught, correct, weak, due, tickSolid, mock, coldAsked, coldUsed, mistakeRows, checkMisses, refused, opened, skipped, proposed, fullCoverage>>

MarkAptitudeMiss ==
  /\ screen = "aptitude" \* verify/turn_contract.py:787
  /\ placement = "drill"
  /\ screen' = "idle"
  /\ placement' = "none"
  /\ weak' = TRUE
  /\ due' = TRUE
  /\ UNCHANGED <<taught, correct, tickSolid, mock, coldAsked, coldUsed, mistakeRows, checkMisses, refused, opened, skipped, proposed, fullCoverage>>

MarkCatalogPass ==
  /\ screen = "aptitude" \* verify/turn_contract.py:797
  /\ placement = "catalog"
  /\ screen' = "proposing"
  /\ placement' = "none"
  /\ proposed' = TRUE
  /\ UNCHANGED <<taught, correct, weak, due, tickSolid, mock, coldAsked, coldUsed, mistakeRows, checkMisses, refused, opened, skipped, fullCoverage>>

MarkCatalogMiss ==
  /\ screen = "aptitude" \* verify/turn_contract.py:787
  /\ placement = "catalog"
  /\ screen' = "idle"
  /\ placement' = "none"
  /\ weak' = TRUE
  /\ due' = TRUE
  /\ UNCHANGED <<taught, correct, tickSolid, mock, coldAsked, coldUsed, mistakeRows, checkMisses, refused, opened, skipped, proposed, fullCoverage>>

ConfirmSkip ==
  /\ screen = "proposing" \* verify/turn_contract.py:925
  /\ proposed
  /\ ~skipped
  /\ ~tickSolid \/ Break = "skip_as_solid"
  /\ screen' = "idle"
  /\ skipped' = TRUE
  /\ placement' = "none"
  /\ tickSolid' = IF Break = "skip_as_solid" THEN TRUE ELSE tickSolid
  /\ UNCHANGED <<taught, correct, weak, due, mock, coldAsked, coldUsed, mistakeRows, checkMisses, refused, opened, proposed, fullCoverage>>

ConfirmDecline ==
  /\ screen = "proposing" \* verify/turn_contract.py:911
  /\ proposed
  /\ screen' = "idle"
  /\ placement' = "none"
  /\ UNCHANGED <<taught, correct, weak, due, tickSolid, mock, coldAsked, coldUsed, mistakeRows, checkMisses, refused, opened, skipped, proposed, fullCoverage>>

ConfirmWithoutOffer ==
  /\ Break = "confirm_anytime"
  /\ ~proposed \* verify/turn_contract.py:909
  /\ ~skipped
  /\ screen \in {"idle", "aptitude"}
  /\ skipped' = TRUE
  /\ UNCHANGED <<screen, taught, correct, weak, due, tickSolid, mock, coldAsked, coldUsed, mistakeRows, checkMisses, refused, opened, placement, proposed, fullCoverage>>

CoverOn ==
  /\ ~fullCoverage \* verify/turn_contract.py:950
  /\ screen \in {"idle", "aptitude", "proposing"}
  /\ fullCoverage' = TRUE
  /\ UNCHANGED <<screen, taught, correct, weak, due, tickSolid, mock, coldAsked, coldUsed, mistakeRows, checkMisses, refused, opened, placement, skipped, proposed>>

CoverOff ==
  /\ fullCoverage \* verify/turn_contract.py:938
  /\ screen \in {"idle", "aptitude", "proposing"}
  /\ fullCoverage' = FALSE
  /\ UNCHANGED <<screen, taught, correct, weak, due, tickSolid, mock, coldAsked, coldUsed, mistakeRows, checkMisses, refused, opened, placement, skipped, proposed>>

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
  \/ StartAptitude
  \/ MarkAptitudePass
  \/ MarkAptitudeMiss
  \/ MarkCatalogPass
  \/ MarkCatalogMiss
  \/ ConfirmSkip
  \/ ConfirmDecline
  \/ ConfirmWithoutOffer
  \/ CoverOn
  \/ CoverOff

Spec == Init /\ [][Next]_vars

\* A solid tick follows two correct drills for that node.
\* verify/turn_contract.py:815
TwoCorrectBeforeSolid == tickSolid => correct = 2

\* A stored mock was started with every Round 1 node solid, or with cold.
\* Cover and a skipped tick do not open that gate. verify/model.py:30
MockGate == mock = "none" \/ tickSolid \/ coldUsed

\* A photo miss appends a mistake and marks that tag weak and due.
\* scripts/control-integration-bee:322
MistakeQueuesWeak == mistakeRows = 0 \/ (weak /\ due)

\* An incorrect SymPy check marks the tag weak and puts the drill on the spaced queue.
\* scripts/control-integration-bee:518
MissQueuesReview == checkMisses = 0 \/ (weak /\ due)

\* A stored score follows an opened mock.
\* scripts/control-integration-bee:713
ScoreAfterOpen == mock # "scored" \/ opened

\* A skip is stored only after a proposing offer was shown.
\* verify/turn_contract.py:909
SkipFollowsProposal == skipped => proposed

\* Confirm writes skipped. It does not write the solid gate.
\* verify/turn_contract.py:925
SkipIsNotSolid == ~(skipped /\ tickSolid)

====
