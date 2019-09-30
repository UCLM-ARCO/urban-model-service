# -*- mode: makefile-gmake; coding: utf-8 -*-
DESTDIR ?= ~

all:

install:
	python3 setup.py install \
	    --prefix=$(DESTDIR)/usr/ \
	    --no-compile \
	    --install-layout=deb

.PHONY: clean
clean:
	$(RM) -fr build

