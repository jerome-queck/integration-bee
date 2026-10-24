# Yang chapters 1 and 2 template rewrap

Units 01 through 18 input `templates/technique-note.tex`, `drill-sheet.tex`, and `solution-sheet.tex`. A leading comment is allowed. Units 19 through 36, `past/`, `templates/`, the CLI, and `verify/drills_unit*.json` stay.

Unit 10 solution U10-D07 writes the King step with \(\cos^2\) in math mode.

Unit 22 already escaped the ampersand in `teaching.tex` on main, so that pack file matches and does not change.

The pack's `meta.yaml` `latex_note` and a few `teaching.md` pointers still said the notes were article-class until `templates/` landed. Those lines stay on the templates sentence already on main. The `.tex` files are the pack.

Receipt: `integration-bee-ch1-ch2-rewrap-2026-10-25`. Pack sha256: `e02cde4fc2ed320bc760aabf49c8c6f453d9c71c0201556b951388554fb6d1eb`.
