default:
	@echo "Specify an explicit target"

ws: WORKSPACE

# target WORKSPACE
#   Create the WORKSPACE file from WORKSPACE.* files
WORKSPACE: .FORCE
	chmod 600 WORKSPACE
	cat WORKSPACE.pre WORKSPACE.{cc,js,py,go,rs} > WORKSPACE
	chmod 400 WORKSPACE

# target check:
#   Look for updates to rules
check: WORKSPACE
	web ws WORKSPACE

.FORCE:
