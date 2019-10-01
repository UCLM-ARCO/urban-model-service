#!/usr/bin/make -f
# -*- mode:makefile -*-


PROJECT_DIR := ..
MODEL_FILE_ITSI_BUILDING='../../itsi-indoorgml/final_models/ITSI.gml'
MODEL_FILE_CASE_CITISIM='../../itsi-indoorgml/final_models/outdoor-indoor-citisim.gml'
MODEL_FILE_CASE_PAPER='case_paper_example.gml'



clean:
	$(RM) *~ *.txt
	find $(shell get-project-dir) | grep -E "__pycache__" | xargs rm -rf

run-server-itsi-building:
	$(PROJECT_DIR)/src/urban-model-server $(MODEL_FILE_ITSI_BUILDING) --Ice.Config=Server.config

run-IgmlLayerClient:
	./IgmlLayerClient.py

run-server-case-citisim:
	$(PROJECT_DIR)/src/urban-model-server $(MODEL_FILE_CASE_CITISIM) --Ice.Config=Server.config

run-CaseCITISIM:
	./RoutingServiceClientCITISIM.py

run-server-case-paper:
	$(PROJECT_DIR)/src/urban-model-server $(MODEL_FILE_CASE_PAPER) --Ice.Config=Server.config

run-server-tfm-ana:
	$(PROJECT_DIR)/src/urban-model-server '../../tfm.ana.rubio/case-of-use/model.gml' --Ice.Config=Server.config


