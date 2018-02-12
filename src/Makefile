#!/usr/bin/make -f
# -*- mode:makefile -*-

all:

clean:
	$(RM) *~ proxy.out
	$(RM) -rf tilescache

run-server:
	./Server.py --Ice.Config=Server.config | tee proxy.out
