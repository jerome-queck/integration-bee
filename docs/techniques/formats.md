# Contest formats

Round 2 and Round 3 are games. A mark is still one final answer. The answer is often a digit, a short fill, or the chosen part of a pair. These notes cite the 2024 participant guides and do not copy a contest answer. The named formats are group, crossnumber, relay, chainlink, dichotomy, and tournament.

The Yang Topics Guide does not teach these formats. The sources are the participant guides and the contest site https://integration.soc.srcf.net/. Practice the answer-shape of the format with unit drills. The integral skill is still the unit note.

Sources:

- `sources/past/r2/2024/2024_Participant_Guide_R2_UK_University_Integration_Bee.pdf`
- `sources/past/r3/2024/Round_3_Integration_Bee_Participant_Guide.pdf`

The 2025 Round 2 participation guide keeps the same point values. Its crossnumber heading says 60 minutes and the paragraph under that heading still says 40 minutes. Train to the 40 minutes in the 2024 guide unless the briefing on the day names another clock.

## What the mark is

Write the object the blank asks for. A Round 1 blank and a group blank want the value. A crossnumber square wants one digit. A relay wants the current problem only, and a later correction is worth less than a first answer. If the written answer is a full antiderivative and the blank wanted a digit, the miss is the format, and this file is the note to teach. Do not paste a contest solution into the note.

Round 1, from the contest site, is a paper: 30 problems, a team of up to 3, 2 hours. Most of those integrals are definite. There is no grid, no banking, and no bracket. The group round is the short form of that paper. The other five formats add a rule on top of the integral.

## Group

Ten problems, 60 minutes, one team. A correct answer scores 6 points. A blank or a wrong answer scores nothing. There is no partial credit for a method. The maximum is 60. The problems rise in difficulty. Submit at the end of the hour.

Train by working a timed set of ten unit drills, hardest last. Skip a stuck integral instead of spending the hour on it. Six points on an easy drill is the same six points as a hard one, and a blank is zero either way.

## Crossnumber

Forty minutes in the 2024 guide. The maximum varies, typically between 45 and 50 points, one point per correct digit. A grid of digits, each square a digit from 0 to 9. The 2024 blank grid file is named Crossword. One half of the team has the across clues and the other half has the down clues. A team of two splits 1–1. A team of three splits 2–1. One set of clues is meant to be easier. Give that set to the person who is alone, unless the team chooses otherwise. Clues are not all integrals. Some need a digit already in the grid.

No communication is allowed except asking the other half to attempt a clue. You may say "please do 1 across". You may not say the digit. A grader checks the attempt and writes the correct digit into a master grid. Only the grader writes on that grid. Whether the attempt was right or wrong, that square is finished and cannot be attempted again.

You may submit one square, or a whole clue at once. A whole clue cannot be withdrawn once checking has started. One attempt per square. A correct digit scores 1. A wrong digit scores 0, and the correct digit still appears in the master grid. A blank square at the end scores 0.

Train by splitting a page: one person sees only the across clues, the other only the down clues. Agree a digit only by pointing at a clue, not by saying the value. Submit one square at a time. After a wrong digit, that square is gone, so check the units digit before you commit. If the stored value of the drill is an integer, the object you submit is that digit and nothing else.

## Relay

Forty-five minutes, 20 problems, maximum 70. The 2021 file is named Shuttle. Later years name the same format Relay. Problems arrive one at a time. The team solves or skips the current problem before seeing the next one, and it cannot return, even after problem 20.

A correct answer on the first attempt scores 3. A correct answer on a later attempt scores 1. A skip scores 0. The bonus is on the count of correct problems, not on a consecutive streak. Attempts still count as correct for the bonus. The 2024 guide scores that bonus as 0 points for 0–9 correct, 5 points for 10–14 correct, and 10 points for 15–20 correct. Twenty first-attempt answers are \(20\times 3+10=70\).

Train by covering the next drill until the current one is answered or skipped. A skip is allowed. Going back is not. Score a clean first answer as 3 and a corrected one as 1. Do not spend the round protecting a streak that the bonus does not measure.

## Chainlink

About 120 minutes, maximum 150. Five sets of eight problems, 40 problems in all. They arrive one at a time, in rising difficulty, as in the relay. The round has two halves.

In the first half each set is one game. After a correct answer the team banks the chain or continues. Three attempts are allowed. A skip is not allowed unless a lifeline says so. A failed problem ends that game. A banked chain of \(n\) solves scores

\[
\begin{array}{c|ccccccccc}
n & 0 & 1 & 2 & 3 & 4 & 5 & 6 & 7 & 8 \\
\hline
\text{points} & 0 & 2 & 4 & 7 & 11 & 15 & 20 & 25 & 30
\end{array}
\]

A failed chain scores the bank value of the highest safety net already reached, not the row for the number solved. The nets you start with are 1, 3, and 6 solves. Failing after 5 solves, with only those nets, pays the value of 3 solves, which is 7, not the banked value 15 of five solves. Failing after 6 pays 20. Banking five pays 15. The gap between a net and the next bank row is the cost of continuing.

Lifelines, first half, and they may be combined in one game:

- Stop-loss, twice in the half. Before the game ends, add one extra net from \(\{2, 4, 5, 7\}\). It applies to this game only. Nets count solved problems, not problem numbers.
- Take the money and run, once in the half. Before the third attempt, void the current problem and bank. The void is not a solve.
- This problem is dread, twice in the half. Before the third attempt, void the current problem and continue. On the last problem of the game the void banks instead.

The second half is the unused problems, in the same set order. A miss ends the chain and the next chain starts. There is no drop to a safety net. A skip counts as a miss. A chain of \(k\ge 1\) consecutive solves scores \(2k + \lfloor (k-1)/2 \rfloor\). The first few values are 2, 4, 7, 9 for \(k = 1, 2, 3, 4\). Dread may be used three times in this half: a void neither adds a solve nor breaks the chain. Four solves with a void between them are still a chain of length 4, worth 9.

Train the decision, not only the integral. After each correct drill, say out loud whether you would bank, and say which net you would fall to if the next drill failed. Banking keeps the safety net. Continuing risks it for a longer chain. In the second half, treat a skip as the end of the chain.

## Dichotomy

About 80 minutes, maximum 140. Three segments of 25 minutes. Each segment is seven pairs, and only the chosen problem in a pair is scored, so a team attempts up to 21 problems.

A team of three labels its members A, B, and C. In a segment two members select and one solves, and the solver rotates: C, then A, then B. A team of two uses A as selector then B as selector, and the third segment is their choice. Selectors and the solver do not talk.

The selectors see both problems in a pair and choose one. They cannot change the choice after it is passed. While the solver works on problem \(n\), the selectors choose problem \(n+1\). The solver receives problems one at a time and cannot return. Only the solver's answers score.

A correct first attempt scores 6. A later attempt scores 2. A skip scores 0. Unlimited attempts are allowed, with a 10-second wait between attempts on the same problem. Ten correct problems earn a bonus of 8. Fifteen correct problems replace that bonus with 14. They do not stack. The published maximum is \(21\times 6 + 14 = 140\).

Train with two drills face down. The selector looks at both integrands, picks the one the solver is more likely to finish, and passes only that one. The solver does not ask what the other one was. Score a clean first answer as 6 and a corrected one as 2.

## Tournament

About 140 minutes. Teams meet on the same problems in a bracket of four battles. The top team from chainlink plus dichotomy plays battle 1 and is already through to battle 3. Battles 1 and 2 give 2.5 minutes per problem, battle 3 gives 3, and battle 4 gives 4. Battles 1 to 3 are pairs of teams on the same problems at once. Battle 4 is the last three teams.

Each battle is three fights, and each fight is three problems, nine problems in all. Members are A, B, and C, and each fight belongs to one letter. A team of two chooses who fights as C. Two attempts per problem, unless a score gamble is in force. Circle or box the answer. An unboxed line is a wasted attempt. A correct answer still scores after the other team has solved it.

Speed awards 1 battle point to the first correct team in the pair, or in the triple in battle 4. Battle points decide the fight. They do not convert into score points, and they reset after the battle. The battle winner is the team with more fights won, then more battle points, then more solves, then a sudden-death problem. In battle 1 the top team's battle points are not used. That team takes the winner's points if it solves more problems than the average of the two battle-1 winners.

A contestant may declare a score gamble before a fight begins, once per battle, and only for that contestant's fight. It is double or nothing: one attempt on each problem, and those problem points are doubled. Battle points are not doubled. Declare it when the fight is offered, before the integrals are the reason you are declaring. A gamble called after the fight has started is too late.

Points per correct answer, and the extra from gambling one fight of three problems:

- Battles 1 and 2: 8 points, or 16 with a gamble. Winning the battle is 8. Nine solves plus the win are 80. The gamble adds \(3\times 8 = 24\).
- Battle 3: 3 points, or 6 with a gamble. Winning is 3. The gamble adds 9.
- Battle 4: 2 points, or 4 with a gamble. Winning is 2. The gamble adds 6.

An eliminated team can still submit a redemption answer on paper during battles 3 and 4, before any board is correct, and not while a board answer is being checked. One attempt per problem. Do not shout it. A gamble does not apply, and tiebreakers are not redeemed. A correct redemption in battle 3 scores 2, and in battle 4 scores 1. A team eliminated in battle 1 or 2 can still collect both, 27 points in all. A team eliminated in battle 3 has only the battle-4 paper, 9 points.

Train by racing a partner on three drills. Call the gamble before you see the integrals, and only when you want the swing. Box the final line. Keep that line clean even when the board has moved on, because redemption is a written answer after elimination.

## On a miss

Teach this file. Name the format, the object of the answer, and the rule the attempt broke: a second try at a square, a spoken digit, a return to an earlier relay problem, a bonus treated as a streak, a chain continued with no net under it, a selector telling the solver the other integrand, a gamble called after the fight started, an unboxed tournament answer. Then set an ordinary unit drill. Do not invent a contest answer. The integral skill for that drill is the coach card in `pedagogy/concept-map.md`.
