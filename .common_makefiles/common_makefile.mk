.PHONY: clean help all default _make_help_banner
.DEFAULT_GOAL: default

default: _make_help_banner all

_make_help_banner:
	@echo "Executing default all target (use 'make help' to show other targets/options)"

all::

clean:: ## Clean build and temporary files
	rm -Rf .help.txt

help::
	@# See https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
	@cat $(MAKEFILE_LIST) >.help.txt
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' .help.txt | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
	@rm -f .help.txt
