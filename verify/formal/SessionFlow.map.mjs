// Chart labels for SessionFlow. The reader is the companion watching one learner.

export const readerActions = [];

function finish(label, v) {
  const extra = [];
  if (v.skipped) extra.push("node skipped");
  const placement =
    v.screen === "idle" || v.screen === "aptitude" || v.screen === "proposing";
  if (v.fullCoverage && placement) extra.push("full coverage");
  if (!extra.length) return label;
  return `${label}, ${extra.join(", ")}`;
}

export function state(v) {
  if (v.screen === "aptitude") {
    const kind = v.placement === "catalog" ? "Contest probe open" : "Aptitude drill open";
    return finish(kind, v);
  }
  if (v.screen === "proposing") return finish("Skip offer waiting", v);
  if (v.screen === "mock_scored") {
    return finish(v.coldUsed ? "Cold mock scored" : "Mock scored", v);
  }
  if (v.screen === "mock_open") {
    return finish(v.coldUsed ? "Cold mock running" : "Timed mock running", v);
  }
  if (v.screen === "marking") return finish("Photo on the table", v);
  if (v.screen === "mistaken") {
    const label = v.coldAsked ? "Miss recorded, review due, cold mock asked" : "Miss recorded, review due";
    return finish(label, v);
  }
  if (v.screen === "ticked") {
    return finish(v.weak ? "Skill solid, review still due" : "Skill solid", v);
  }
  const asked = v.coldAsked ? ", cold mock asked" : "";
  if (v.screen === "drilling") {
    if (v.weak && v.correct >= 1) return finish(`Second drill, review due${asked}`, v);
    if (v.weak) return finish(`Next drill, review due${asked}`, v);
    if (v.correct === 1) return finish(`Second drill on the table${asked}`, v);
    return finish(`Drill on the table${asked}`, v);
  }
  if (v.screen === "checked") {
    if (v.correct >= 2 && v.weak) return finish(`Two drills correct, review still due${asked}`, v);
    if (v.correct >= 2) return finish(`Two drills correct${asked}`, v);
    if (v.checkMisses > 0 && v.correct === 0) return finish(`Check missed, review due${asked}`, v);
    if (v.weak) return finish(`One drill correct, review due${asked}`, v);
    if (v.correct === 1) return finish(`One drill correct${asked}`, v);
    return finish(`Answer checked${asked}`, v);
  }
  if (v.screen === "teaching") {
    let label = "Teaching";
    if (v.refused) label = "Teaching, mock refused";
    else if (v.coldAsked) label = "Teaching, cold mock asked";
    if (v.weak || v.due) label = `${label}, review due`;
    return finish(label, v);
  }
  let label = "Ready";
  if (v.refused) label = "Mock refused";
  else if (v.coldAsked) label = "Cold mock asked";
  if (v.weak || v.due) label = `${label}, review due`;
  return finish(label, v);
}

export function group(v) {
  if (v.mock === "open" || v.mock === "scored") return "Mock";
  if (v.screen === "marking" || v.screen === "mistaken") return "Photo";
  if (v.screen === "aptitude" || v.screen === "proposing" || v.skipped) return "Placement";
  if (v.weak || v.due) return "Review due";
  if (v.tickSolid) return "Skill solid";
  return "Practice";
}

export const groupColors = {
  Practice: "#d6eaf8",
  "Review due": "#fdebd0",
  "Skill solid": "#d5f5e3",
  Photo: "#e8daef",
  Mock: "#f5b7b1",
  Placement: "#fcf3cf",
};

const STEPS = {
  Teach: "teach the concept",
  OfferDrill: "put a drill on the table",
  CheckPass: "the answer matches",
  CheckMiss: "the answer differs",
  TickAfterTwo: "mark the skill solid",
  TickEarly: "mark the skill solid too soon",
  MarkPhoto: "read the photo",
  RecordMistake: "record the miss",
  AskCold: "ask for a cold mock",
  MockStartReady: "start the timed mock",
  MockStartCold: "start a cold mock",
  MockStartUngated: "start a mock before the gate",
  MockRefuse: "refuse the mock",
  MockScore: "record the score",
  ScoreWithoutOpen: "record a score with no mock",
  StartAptitude: "open an aptitude drill",
  MarkAptitudePass: "the aptitude drill matches",
  MarkAptitudeMiss: "the aptitude drill differs",
  MarkCatalogPass: "the contest probe matches",
  MarkCatalogMiss: "the contest probe differs",
  ConfirmSkip: "confirm the skip",
  ConfirmDecline: "decline the skip",
  ConfirmWithoutOffer: "skip before the offer",
  CoverOn: "turn full coverage on",
  CoverOff: "turn full coverage off",
};

export function step(action) {
  return STEPS[action] ?? action;
}
