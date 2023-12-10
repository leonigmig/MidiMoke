export OPENAI_API_KEY=$(shell cat api_key.txt)

ext: venv
	. venv/bin/activate && \
	python src/main.py 'Elektron Digitakt'

int: venv
	. venv/bin/activate && \
	python src/main.py 'Midi Through:Midi Through Port-0 10'

lang: venv
	. venv/bin/activate && \
	python src/lchain.py

shell: venv
	. venv/bin/activate && \
	python

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
