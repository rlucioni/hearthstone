.PHONY: load requirements

explore:
	jupyter notebook explore.ipynb

load:
	./load.py

requirements:
	pip install -r requirements.txt
