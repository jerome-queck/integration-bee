// Chart labels for SessionFlow. The reader is the companion watching one learner.

export const readerActions = [];

export function state(v) {
  if (v.screen === "mock_scored") {
    return v.coldUsed ? "Cold mock scored" : "Mock scored";
  }
  if (v.screen === "mock_open") {
    return v.coldUsed ? "Cold mock running" : "Timed mock running";
  }
  if (v.screen === "marking") return "Photo on the table";
  if (v.screen === "mistaken") {
    return v.coldAsked ? "Miss recorded, review due, cold mock asked" : "Miss recorded, review due";
  }
  if (v.screen === "ticked") {
    return v.weak ? "Skill solid, review still due" : "Skill solid";
  }
  const asked = v.coldAsked ? ", cold mock asked" : "";
  if (v.screen === "drilling") {
    if (v.weak && v.correct >= 1) return `Second drill, review due${asked}`;
    if (v.weak) return `Next drill, review due${asked}`;
    if (v.correct === 1) return `Second drill on the table${asked}`;
    return `Drill on the table${asked}`;
  }
  if (v.screen === "checked") {
    if (v.correct >= 2 && v.weak) return `Two drills correct, review still due${asked}`;
    if (v.correct >= 2) return `Two drills correct${asked}`;
    if (v.checkMisses > 0 && v.correct === 0) return `Check missed, review due${asked}`;
    if (v.weak) return `One drill correct, review due${asked}`;
    if (v.correct === 1) return `One drill correct${asked}`;
    return `Answer checked${asked}`;
  }
  if (v.screen === "teaching") {
    if (v.refused) return "Teaching, mock refused";
    if (v.coldAsked) return "Teaching, cold mock asked";
    return "Teaching";
  }
  if (v.refused) return "Mock refused";
  if (v.coldAsked) return "Cold mock asked";
  return "Ready";
}

export function group(v) {
  if (v.mock === "open" || v.mock === "scored") return "Mock";
  if (v.screen === "marking" || v.screen === "mistaken") return "Photo";
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
};

export function step(action) {
  return STEPS[action] ?? action;
}
