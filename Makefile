.PHONY: all ruuter resql 

all: ruuter resql 

ruuter:
	@echo "Building ruuter..."
	cd Ruuter && docker build -t ruuter .


resql:
	@echo "Building resql..."
	cd Resql && docker build -t resql .