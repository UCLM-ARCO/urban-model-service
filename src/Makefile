#!/usr/bin/make -f
# -*- mode:makefile -*-

MODEL_FILE='../../itsi.indoorgml/model/ITSI.gml'

all:

clean:
	$(RM) *~ proxy.out
	$(RM) -rf __pycache__

run-server:
	./Server.py $(MODEL_FILE) --Ice.Config=Server.config | tee proxy.out
