// Chart labels for TrackerWrites. The reader is watching the tracker files.

function idle(v) {
  const pc = v.pc || {};
  return pc.companion === "idle" && pc.second === "idle";
}

export const readerActions = [
  "BeginRecord",
  "BeginTick",
  "BeginMockReady",
  "BeginMockCold",
  "WriteFinish",
];

export function state(v) {
  if (!idle(v)) return "Saving the tracker";
  const parts = ["Tracker idle"];
  if (v.attemptCommits > v.attempts) parts.push("an attempt was overwritten");
  else if (v.incorrect > 0) parts.push("a miss is saved");
  else if (v.attempts > 0) parts.push("a correct attempt is saved");
  if (v.heatAttempts !== v.attempts || v.heatFails !== v.incorrect) {
    parts.push("the heatmap disagrees");
  } else if (v.heatFails > 0) {
    parts.push("the weak tag is set");
  }
  if (v.projTick !== v.tickSolid || v.projMistakes !== v.incorrect) {
    parts.push("progress disagrees");
  } else if (v.tickSolid) {
    parts.push("the skill tick is in progress");
  }
  if (v.ungated) parts.push("the mock skipped the gate");
  if (v.openCount > 1) parts.push("two mocks are open");
  else if (v.openCount === 1) parts.push(v.mockCold ? "a cold mock is open" : "a mock is open");
  if (v.scoredCount > 0) parts.push("a mock is scored");
  if (v.mockCommits > v.openCount + v.scoredCount) parts.push("a mock start was overwritten");
  return parts.join(", ");
}

export function group(v) {
  if (!idle(v)) return "Write in progress";
  const torn =
    v.attemptCommits > v.attempts ||
    v.mockCommits > v.openCount + v.scoredCount ||
    v.heatAttempts !== v.attempts ||
    v.heatFails !== v.incorrect ||
    v.projTick !== v.tickSolid ||
    v.projMistakes !== v.incorrect ||
    v.ungated ||
    v.openCount > 1;
  return torn ? "Tracker disagrees" : "Tracker agrees";
}

export const groupColors = {
  "Tracker agrees": "#d5f5e3",
  "Tracker disagrees": "#f5b7b1",
  "Write in progress": "#d6eaf8",
};

export function cause(v, _facts, invariant) {
  if (invariant === "NoLostAttempt") {
    return "both checks wrote the attempts file from the same read";
  }
  if (invariant === "IdleFilesAgree") {
    if (v.heatFails > v.incorrect) {
      return "the heatmap still counts a miss the attempts file lost";
    }
    return "the process stopped after the attempt write and before the heatmap write";
  }
  if (invariant === "ProjectionMatches") {
    return "the process stopped after a tick or a check write and before progress caught up";
  }
  if (invariant === "NoLostMock") {
    return "both mock starts wrote the mock file from the same read";
  }
  return null;
}

const STEPS = {
  BeginRecord: "start saving a check",
  WriteAttempts: "replace the attempts file",
  WriteHeat: "replace the heatmap file",
  ProjectRecord: "write progress from the check's old read",
  Crash: "the process stops",
  BeginTick: "write the solid tick",
  ProjectTick: "refresh progress after the tick",
  BeginMockReady: "read the tracker to start a mock",
  BeginMockCold: "read the tracker to start a cold mock",
  BeginMockUngated: "read the tracker with the gate removed",
  WriteMockKeep: "keep the open mock",
  WriteMockAppend: "replace the mock file",
  ProjectMock: "write progress from the mock's old read",
  WriteFinish: "store the score",
  ProjectFinish: "refresh progress after the score",
};

export function step(action, before, after) {
  if (action === "BeginRecord") {
    const left = before.wantMiss || {};
    const right = after.wantMiss || {};
    if (right.companion !== left.companion) {
      return right.companion ? "start saving a miss" : "start saving a correct check";
    }
    if (right.second !== left.second) {
      return right.second ? "start saving a miss" : "start saving a correct check";
    }
  }
  return STEPS[action] ?? action;
}
