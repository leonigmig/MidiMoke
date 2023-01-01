start: venv
	. venv/bin/activate && \
	python main.py OPZ

venv:
	python3 -m venv venv
	. venv/bin/activate && \
	pip install -r requirements.txt

clean:
	rm -rf venv