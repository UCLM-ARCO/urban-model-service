#!/usr/bin/make -f
# -*- mode:makefile -*-


PROJECT_DIR := $(shell get-project-dir)
MODEL_FILE_ITSI_BUILDING='../../itsi-indoorgml/model/ITSI.gml'
MODEL_FILE_CASE_PAPER='../../indoorgml-olc-models/models/case_of_use/outdoor-itis-IJGI.gml'
MODEL_FILE_CASE_CITISIM='../../indoorgml-olc-models/models/case_ITSI-Citisim/outdoor-indoor-citisim.gml'


clean:
	$(RM) *~ *.txt
	find $(shell get-project-dir) | grep -E "__pycache__" | xargs rm -rf
	
run-server-itsi-building:
	$(PROJECT_DIR)/src/Server.py $(MODEL_FILE_ITSI_BUILDING) --Ice.Config=Server.config

run-IgmlLayerClient: 
	./IgmlLayerClient.py

run-server-case-citisim:
	$(PROJECT_DIR)/src/Server.py $(MODEL_FILE_CASE_CITISIM) --Ice.Config=Server.config

run-CaseCITISIM: 
	./RoutingServiceClientCITISIM.py

run-server-case-paper:
	$(PROJECT_DIR)/src/Server.py $(MODEL_FILE_CASE_PAPER) --Ice.Config=Server.config

run-server-tfm-ana:
	$(PROJECT_DIR)/src/Server.py '../../tfm.ana.rubio/case-of-use/model.gml' --Ice.Config=Server.config


