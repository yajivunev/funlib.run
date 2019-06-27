PKG=funlib.run
TMP_FILE:=$(shell mktemp).img

~/.funlib.run:
	cp .funlib.run ~/.funlib.run

default: ~/.funlib.run
	python setup.py install
	-rm -rf dist build $(PKG).egg-info

install-pip: ~/.funlib.run
	pip install .
	-rm -rf dist build $(PKG).egg-info

.PHONY: install-full
install-full: ~/.funlib.run
	pip install -r requirements.txt
	pip install .
	-rm -rf dist build $(PKG).egg-info

.PHONY: install-dev
install-de: ~/.funlib.run
	pip install -r requirements
	pip install -e .[full]
	-rm -rf dist build $(PKG).egg-info

singularity/funlib.run_test.img:
	sudo singularity build $(TMP_FILE) singularity/Singularity
	cp $(TMP_FILE) singularity/$(PKG)_test.img
	sudo rm $(TMP_FILE)

.PHONY: tests
tests: singularity/funlib.run_test.img
	PY_MAJOR_VERSION=py`python -c 'import sys; print(sys.version_info[0])'` pytest --cov-report term-missing -v --cov=$(PKG) --cov-config=.coveragerc funlib/tests
	flake8 $(PKG)
