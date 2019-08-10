default:
	@echo "Specify explicit target"

build:
	cd src/kernel; make test

fixme:
	cd ..; \
	echo "$(PWD)"; \
	current=$(shell ls -1 -d $(PWD)/meta/lib/versions/* | tail -1); \
	echo "HERE with $$current"; \
	tar czf meta/meta.tgz meta/bin/metac meta/lib/metastrap.py

