

start: venv
	. venv/bin/activate && \
	python src/main.py 'Elektron Digitakt' OP-Z

m21: venv
	. venv/bin/activate && \
	python src/m21.py

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