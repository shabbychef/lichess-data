
VARIANTS 			 = antichess atomic chess960 standard horde
ALL_MAKEFILES  = $(foreach var,$(VARIANTS),$(var)/Makefile)
ALL_PARSERS 	 = $(foreach var,$(VARIANTS),$(var)/parser.py)
ALL_GAMENUM 	 = $(foreach var,$(VARIANTS),$(var)/attach_gamenum.r)

ALL_FILES 		 = parsing.py common_Makefile dates_Makefile 
ALL_FILES 		+= $(ALL_MAKEFILES) $(ALL_PARSERS) $(ALL_GAMENUM)
ALL_FILES 		+= Dockerfile compose.yaml

help :  ## get this help
	@grep -h -P '^(([^\s]+\s+)*([^\s]+))\s*:.*?##\s*.*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

tarball : code_trans.tgz   ## make code to be moved

code_trans.tgz : $(ALL_FILES) 
		tar -czvf $@ $^

