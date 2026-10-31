const L = {
  cloned: "📥 Repo cloned", setup: "🤖 Agent runs setup", placement: "🎯 Placement drill",
  marking: "✍️ Coach marks your working", offer: "⏭️ You pick what to skip",
  lesson: "📖 Lesson from the notes", practice: "∫ Real contest integral",
  gap: "🧩 Gap captured", mock: "⏱️ Mock exam", ready: "🏆 Round 1 ready",
};
const G = {
  cloned: "Get set up", setup: "Get set up", placement: "Find your level", offer: "Find your level",
  marking: "Practise", practice: "Practise", lesson: "Learn", gap: "Learn", mock: "Prove it", ready: "Prove it",
};
export const title = "Your Integration Bee journey";
export const state = (v) => L[v.phase];
export const group = (v) => G[v.phase];
export const colors = { "Get set up": "blue", "Find your level": "purple", "Practise": "teal", "Learn": "yellow", "Prove it": "pink" };
const S = {
  PasteSetupPrompt: "you paste the setup prompt", SetupReady: "setup prints READY",
  SendPlacementWork: "you send your working", SendContestWork: "you send your working",
  AnotherProbe: "one more probe", OfferSkips: "coach offers skips",
  ConfirmSkips: "you confirm", TryContest: "you try one",
  NextIntegral: "correct: next integral", MissShowsGap: "a miss shows a gap",
  TeachGap: "coach reteaches it", StartMock: "every Round 1 node solid",
  PassMock: "you pass", MockGap: "the mock finds a gap", Done: null,
};
export const step = (a) => S[a];
