
VARIANTS = antichess atomic chess960 standard horde
ALL_MAKEFILES = $(foreach var,$(VARIANTS),$(var)/Makefile)
ALL_PARSERS = $(foreach var,$(VARIANTS),$(var)/parser.py)

ALL_FILES = parsing.py common_Makefile dates_Makefile $(ALL_MAKEFILES) $(ALL_PARSERS)

code_trans.tgz : $(ALL_FILES)  # make code to be moved
		tar -czvf $@ $^

help :  ## get this help
	@grep -h -P '^(([^\s]+\s+)*([^\s]+))\s*:.*?##\s*.*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
