<!-- tla-blob: eb39ca7919c658137f0c57af267560cd2e026877 -->
## 1. Tracker idle, progress disagrees

Rule broken: After every writer is idle, progress.local.json matches the tick file and the misses.
Why: the process stopped after a tick or a check write and before progress caught up.
In the model, 3 different steps lead into this bug: "the process stops", "write progress from the check's old read", and "write progress from the mock's old read". The steps below are the shortest path that TLC found.

0. Start: Tracker idle
1. Write the solid tick. Now: Saving the tracker
2. The process stops. Now: Tracker idle, progress disagrees

## 2. Tracker idle, a correct attempt is saved, the heatmap disagrees

Rule broken: After every writer is idle, the heatmap counts the attempts file.
Why: the process stopped after the attempt write and before the heatmap write.
In the model, 5 different steps lead into this bug: "the process stops", "write progress from the check's old read", "refresh progress after the score", "refresh progress after the tick", and "write progress from the mock's old read". The steps below are the shortest path that TLC found.

0. Start: Tracker idle
1. Start saving a check. Now: Saving the tracker
2. Replace the attempts file. Now: Saving the tracker
3. The process stops. Now: Tracker idle, a correct attempt is saved, the heatmap disagrees

## 3. Tracker idle, an attempt was overwritten, the heatmap disagrees

Rule broken: The attempts file holds every append that passed write_json.
Why: both checks wrote the attempts file from the same read.
In the model, 2 different steps lead into this bug: "the process stops" and "write progress from the check's old read". The steps below are the shortest path that TLC found.

0. Start: Tracker idle
1. Start saving a check. Now: Saving the tracker
2. Start saving a check. Now: Saving the tracker
3. Replace the attempts file. Now: Saving the tracker
4. Replace the attempts file. Now: Saving the tracker
5. The process stops. Now: Saving the tracker
6. The process stops. Now: Tracker idle, an attempt was overwritten, the heatmap disagrees

## 4. Tracker idle, a cold mock is open, a mock start was overwritten

Rule broken: A mock start that reached the mock file is still there once every writer is idle.
Why: both mock starts wrote the mock file from the same read.
In the model, 3 different steps lead into this bug: "the process stops", "write progress from the mock's old read", and "refresh progress after the score". The steps below are the shortest path that TLC found.

0. Start: Tracker idle
1. Read the tracker to start a cold mock. Now: Saving the tracker
2. Read the tracker to start a cold mock. Now: Saving the tracker
3. Replace the mock file. Now: Saving the tracker
4. The process stops. Now: Saving the tracker
5. Replace the mock file. Now: Saving the tracker
6. The process stops. Now: Tracker idle, a cold mock is open, a mock start was overwritten

## 5. Tracker idle, an attempt was overwritten, the heatmap disagrees, progress disagrees

Rule broken: After every writer is idle, the heatmap counts the attempts file.
Why: the heatmap still counts a miss the attempts file lost.
In the model, 2 different steps lead into this bug: "the process stops" and "write progress from the check's old read". The steps below are the shortest path that TLC found.

0. Start: Tracker idle
1. Start saving a check. Now: Saving the tracker
2. Start saving a miss. Now: Saving the tracker
3. Replace the attempts file. Now: Saving the tracker
4. Replace the attempts file. Now: Saving the tracker
5. Replace the heatmap file. Now: Saving the tracker
6. Write progress from the check's old read. Now: Saving the tracker
7. The process stops. Now: Tracker idle, an attempt was overwritten, the heatmap disagrees, progress disagrees
