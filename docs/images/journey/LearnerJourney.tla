---- MODULE LearnerJourney ----
VARIABLES phase, placed
vars == <<phase, placed>>

Init == phase = "cloned" /\ placed = FALSE

PasteSetupPrompt == phase = "cloned" /\ phase' = "setup" /\ UNCHANGED placed
SetupReady == phase = "setup" /\ phase' = "placement" /\ UNCHANGED placed
SendPlacementWork == phase = "placement" /\ phase' = "marking" /\ UNCHANGED placed
SendContestWork == phase = "practice" /\ phase' = "marking" /\ UNCHANGED placed
AnotherProbe == phase = "marking" /\ ~placed /\ phase' = "placement" /\ UNCHANGED placed
OfferSkips == phase = "marking" /\ ~placed /\ phase' = "offer" /\ placed' = TRUE
ConfirmSkips == phase = "offer" /\ phase' = "lesson" /\ UNCHANGED placed
TryContest == phase = "lesson" /\ phase' = "practice" /\ UNCHANGED placed
NextIntegral == phase = "marking" /\ placed /\ phase' = "practice" /\ UNCHANGED placed
MissShowsGap == phase = "marking" /\ placed /\ phase' = "gap" /\ UNCHANGED placed
TeachGap == phase = "gap" /\ phase' = "lesson" /\ UNCHANGED placed
StartMock == phase = "marking" /\ placed /\ phase' = "mock" /\ UNCHANGED placed
PassMock == phase = "mock" /\ phase' = "ready" /\ UNCHANGED placed
MockGap == phase = "mock" /\ phase' = "gap" /\ UNCHANGED placed
Done == phase = "ready" /\ UNCHANGED vars

Next == PasteSetupPrompt \/ SetupReady \/ SendPlacementWork \/ SendContestWork
     \/ AnotherProbe \/ OfferSkips \/ ConfirmSkips \/ TryContest \/ NextIntegral
     \/ MissShowsGap \/ TeachGap \/ StartMock \/ PassMock \/ MockGap \/ Done

\* Rules the learner agrees to
LessonsAfterPlacement == phase \in {"lesson", "practice", "gap", "mock", "ready"} => placed
SkipsOnlyOnce == phase = "offer" => placed
====
