# LaTeX templates

Unit notes, drill sheets, and solution sheets share `ib-common.tex`. `templates/latexmkrc` adds its own directory to `TEXINPUTS`.

```bash
latexmk -r templates/latexmkrc -pdf units/01-foundations-substitution/teaching.tex
```

The same recipe builds `drills.tex`, `solutions.tex`, and `templates/round1-sim.tex`.

`make latex` builds every unit file and the Round 1 sim, then removes the generated PDFs. It also compiles the unit 01 teaching note from another directory, so a relative `templates:` path cannot pass.
