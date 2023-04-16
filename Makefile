

ext: venv
	. venv/bin/activate && \
	python src/main.py 'Elektron Digitakt'

int: venv
	. venv/bin/activate && \
	python src/main.py 'IAC Driver Bus 1'

lint:
	. venv/bin/activate && \
	flake8 src tests

unit: venv lint
	. venv/bin/activate && \
	python -m unittest discover -b

venv:
	python3 -m venv venv
	. venv/bin/activate && \
	pip install -r requirements.txt

.PHONY: docs
docs:
	cd docs; make

clean:
	rm -rf venv