start:
	python3 src/main.py

test:
	pytest -s src

install:
	pip3 install -r requirements.txt

write_env:
	cp .env.example .env

init:
	make write_env
	make install
