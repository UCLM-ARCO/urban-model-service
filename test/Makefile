#!/usr/bin/make -f
# -*- mode:makefile -*-

# FIXME: this repo should content all the needed models/code to make tests
# do NOT rely on a specific directory relative to this one

PROJECT_DIR := $(shell get-project-dir)
MODEL_FILE_ITSI_BUILDING='../../itsi-indoorgml/final_models/ITSI.gml'

clean:
	$(RM) *~ *.txt
	find $(shell get-project-dir) | grep -E "__pycache__" | xargs rm -rf

run-server-itsi-building:
	$(PROJECT_DIR)/src/Server.py $(MODEL_FILE_ITSI_BUILDING) --Ice.Config=Server.config

tests:
	nosetests3 unit_tests.py