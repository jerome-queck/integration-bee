PYTHON ?= python3
export PYTHONPATH := $(CURDIR)/scripts

.PHONY: check hooks ci agents structure templates invariants mutations verify doctor latex formal

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

verify:
	bash verify/run.sh

doctor:
	$(PYTHON) scripts/control-integration-bee doctor

latex:
	bash scripts/compile-tex.sh

formal:
	bash verify/formal/run.sh
