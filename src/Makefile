#!/usr/bin/make -f
# -*- mode:makefile -*-

MODEL_FILE='../../itsi.indoorgml/model/ITSI.gml'
OSM_FILE='../test/map.osm'

all:

clean:
	$(RM) *~ *.txt
	$(RM) -rf __pycache__
	$(RM) -rf ../lib/__pycache__

run-server:
	./Server.py $(MODEL_FILE) $(OSM_FILE) --Ice.Config=Server.config

run-server-tfm-ana:
	./Server.py '../../tfm.ana.rubio/case-of-use/model.gml' $(OSM_FILE)--Ice.Config=Server.config
