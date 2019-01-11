BIN := venv/bin
PYTHON := $(BIN)/python
DEPS := igmun_print.css bootstrap.min.css bootstrap-theme.min.css logo_icon.png

venv: requirements.txt
	python3 -m virtualenv -ppython3 venv
	$(PYTHON) -m pip install -r requirements.txt

clean:
	rm -rf venv
	rm -rf _generated

.PHONY: gen
gen: $(DEPS)
	cp $(DEPS) _generated/
	$(PYTHON) generate_profiles.py
