start: venv
	. venv/bin/activate && \
	python src/main.py 'IAC Driver Bus 1' OP-Z

lint:
	. venv/bin/activate && \
	flake8 src tests

unit: venv lint
	. venv/bin/activate && \
	python -m unittest discover

venv:
	python3 -m venv venv
	. venv/bin/activate && \
	pip install -r requirements.txt

clean:
	rm -rf venv