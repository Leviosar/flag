SHELL := /bin/bash

# Colors
GREEN=\033[0;32m
RED=\033[0;31m
NC=\033[0m

setup:
	@echo Installing virtualenv using pip3
	@pip3 install virtualenv --user
	@echo -e "${RED} Removing previous existing virtualenv (if exists)... ${NC}"
	@rm -rf venv/
	@echo -e "${GREEN} Creating new virtualenv...${NC}\n"
	@python3 -m venv .venv/
	@source .venv/bin/activate && pip install -r requirements.txt
	@echo -e "${GREEN} Virtualenv created! ${NC}"

run:
	@echo -e "${GREEN} Executing $(source)... ${NC}"
	@./.venv/bin/python -m flagg ./samples/lcc/lcc.lexer.json $(source) --verbose

test:
	@echo -e "${GREEN} Running tests with Pytest ${NC}"
	@./.venv/bin/pytest -s ./tests