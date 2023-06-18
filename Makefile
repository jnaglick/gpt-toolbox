start:
	python3 src/main.py

test:
	pytest -s src

install:
	pip3 install -r requirements.txt