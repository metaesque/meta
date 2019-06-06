METAREP := $(shell metac config repository_path)

default:
	@echo "Specify explicit target"

test:
	@echo "METAREP: $(METAREP)"

# target update:
#   Update the meta repository with template data.
update: oopl.tgz
	@echo "Applying $$(pwd)/oopl.tgz onto $(METAREP)"
	@tar="$$(pwd)/oopl.tgz"; builtin cd $(METAREP); tar xzf $$tar

# target oopl.tgz:
#   This target creates a tar file that is to be dumped into
#   $METAREP$NEWSUFFIX/oopl to prepare it.
oopl.tgz: .FORCE
	@echo "Building oopl.tgz"
	@builtin cd oopl; rm -f $$(find . -name *~); builtin cd ..; tar czf oopl.tgz oopl

.FORCE:
