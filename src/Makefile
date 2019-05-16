#!/usr/bin/make -f
# -*- mode:makefile -*-

MODEL_FILE_ITSI_BUILDING='../../itsi-indoorgml/model/ITSI.gml'
MODEL_FILE_CASE_PAPER='../../indoorgml-olc-models/models/case_of_use/outdoor-itis-IJGI.gml'
MODEL_FILE_CASE_CITISIM='../../indoorgml-olc-models/models/case_ITSI-Citisim/outdoor-indoor-citisim.gml'

all:

clean:
	$(RM) *~ *.txt
	$(RM) -rf __pycache__
	$(RM) -rf ../lib/__pycache__

run-server-itsi-building:
	./Server.py $(MODEL_FILE_ITSI_BUILDING) --Ice.Config=Server.config

run-server-case-paper:
	./Server.py $(MODEL_FILE_CASE_PAPER) --Ice.Config=Server.config

run-server-case-citisim:
	./Server.py $(MODEL_FILE_CASE_CITISIM) --Ice.Config=Server.config

run-server-tfm-ana:
	./Server.py '../../tfm.ana.rubio/case-of-use/model.gml' --Ice.Config=Server.config


