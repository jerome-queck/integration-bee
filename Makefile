PYTHON ?= python3
export PYTHONPATH := $(CURDIR)/scripts

.PHONY: check hooks ci agents structure templates invariants mutations verify doctor latex formal sanity

check: ci agents structure templates invariants mutations verify doctor latex formal

hooks:
	git config core.hooksPath .githooks

ci:
	$(PYTHON) scripts/check_ci.py

agents:
	$(PYTHON) scripts/check_agents_md.py

structure:
	$(PYTHON) scripts/check_structure.py

templates:
	$(PYTHON) scripts/check_templates.py

invariants:
	$(PYTHON) verify/invariants.py

mutations:
	$(PYTHON) verify/invariants.py --expect-fail past-before-concept
	$(PYTHON) verify/invariants.py --expect-fail unit01-is-past
	$(PYTHON) verify/invariants.py --expect-fail unit01-missing-yang
	$(PYTHON) verify/invariants.py --expect-fail unknown-tick
	$(PYTHON) verify/invariants.py --expect-fail negative-interval
	$(PYTHON) verify/invariants.py --expect-fail heatmap-fails-exceed
	$(PYTHON) verify/invariants.py --expect-fail mock-before-ready
	$(PYTHON) verify/invariants.py --expect-fail duplicate-streak-day
	$(PYTHON) verify/invariants.py --expect-fail bad-session-phase
	$(PYTHON) verify/invariants.py --expect-fail aptitude-needs-problem
	$(PYTHON) verify/invariants.py --expect-fail proposing-needs-offer
	$(PYTHON) verify/invariants.py --expect-fail proposing-still-open
	$(PYTHON) verify/invariants.py --expect-fail aptitude-bad-coverage
	$(PYTHON) verify/invariants.py --expect-fail mark-one-bool
	$(PYTHON) verify/invariants.py --expect-fail mark-has-correct
	$(PYTHON) verify/invariants.py --expect-fail sticky-stored-strength

verify:
	bash verify/run.sh

doctor:
	$(PYTHON) scripts/control-integration-bee doctor

latex:
	bash scripts/compile-tex.sh

formal:
	bash verify/formal/run.sh

# Fast numeric sanity check of solutions changed vs origin/main (IDS="A B" to name rows). Not part of check.
sanity:
	$(PYTHON) verify/solution_sanity.py $(IDS)
