all: run

install:
	pip install -r requirements.txt
run:
	python app.py
production:
	foreman start
