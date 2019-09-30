# -*- mode: makefile-gmake; coding: utf-8 -*-
DESTDIR   ?= ~
ITSI_MODEL = ../itsi-indoorgml/final_models/outdoor-indoor-citisim.gml

all:

run:
	src/urban-model-server --Ice.Config=examples/Server.config \
	examples/case_paper_example.gml

run-itsi:
	@if ! [ -f "$(ITSI_MODEL)" ]; then \
	  echo "Please, download model first ($(ITSI_MODEL))";\
	else \
	  src/urban-model-server --Ice.Config=examples/Server.config \
	  "$(ITSI_MODEL)";\
	fi

install:
	python3 setup.py install \
	    --prefix=$(DESTDIR)/usr/ \
	    --no-compile \
	    --install-layout=deb

.PHONY: clean
clean:
	$(RM) -fr build

