# LaTeX templates

Unit notes, drill sheets, and solution sheets share `ib-common.tex`. Compile from the repository root so `templates/latexmkrc` can find them.

```bash
latexmk -r templates/latexmkrc -pdf units/01-foundations-substitution/teaching.tex
```

The same recipe builds `drills.tex`, `solutions.tex`, and `templates/round1-sim.tex`.

`make latex` builds every unit file and the Round 1 sim, then removes the generated PDFs.
