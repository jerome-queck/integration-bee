# Pedagogy notes (portable)

## Sequence hard rule

**Concept teaching with easier drills → technique mastery → timed past papers.**  
Never past-papers-only. Enforced by `verify/unit_order_check.py`.

## Where a lesson lives

The canonical lesson for a unit is `units/<id>/teaching.tex`. The six contest gaps that the Yang Topics Guide files late or omits are indexed in `docs/techniques/beyond-yang.md`. Each heading names one file. That file is what a miss teaches.

Yang is one source among others. The other sources used in the notes are:

- the contest syllabus and the Techniques Guide under `sources/`
- the society site https://integration.soc.srcf.net/ for the round formats
- classical arguments written out in the unit notes: a reduction for \(I_n\), the half-angle substitution \(t=\tan(x/2)\), the Leibniz rule on a compact rectangle, the reflection \(x\mapsto a+b-x\), and the floor split at the integers

A PDF is a reference for checking a printed value. It is not the lesson. Do not copy a contest answer into a note. Do not invent a value that `drills.md` does not store and that SymPy has not checked.

## Contest gaps Yang does not cover alone

The six headings in `docs/techniques/beyond-yang.md` are the gap list. How to teach each one, including the Round 1 paper and the Round 2 and Round 3 games, is `pedagogy/contest-gaps.md`. The math stays in the note that heading names. Yang is one source. The Techniques Guide, the syllabus, and the participant guides are the others.

## Teach on a miss

`turn apply` names exactly one file in `say`. Teach that file. A wrong final answer with a gap id opens the technique note. A wrong final answer with no gap id opens `units/<unit>/teaching.tex`. A correct final answer that used the wrong method names the same kind of file and keeps the method note.

Read the worked example in that file, then the faded step, then set the integral again. Match `coach.detail` when it is present:

1. **worked** — full solution visible, then a faded step, then the integral.
2. **faded** — one blank step, then the integral.
3. **bare** — the integral only.

The study session does not edit a teaching note. `turn apply` stores the attempt and does not write the file. If the named note does not yet contain the move, a later commit adds an original example, or an existing drill id, to that same file.

## Teaching pattern used in Unit 1+

Drawn from cognitive-load / example-based instruction research (worked examples, fading, interleaving):

1. **Worked example** — full solution visible; learner studies, does not invent.
2. **Faded example** — some steps blank; learner completes the critical move (e.g. choose \(u\)).
3. **Interleaved easy drills** — mix slight variants so pattern-matching beats rote slot-filling.
4. **Spaced return** — later units revisit substitution inside harder techniques (a parameter derivative, half-angle cleanup).

Official contest materials are the source of *what* to learn (`syllabus-map.md`); this folder is *how* we teach it.

## Sources for contest content (not pedagogy theory)

- https://integration.soc.srcf.net/
- Local: `sources/UK_University_Integration_Bee_Techniques_Guide.pdf`, Syllabus PDF, sample problems.
- In-repo lessons: `units/` and `docs/techniques/`.
