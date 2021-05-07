
.PHONY : download all_csv unified

.PRECIOUS : %.bz2

VARIANT 				 = antichess

ALLMO 			 		 = 01 02 03 04 05 06 07 08 09 10 11 12
ALLYR 			 		 = 2015 2016 2017 2018 2019 2020
DATES 			 		 = $(foreach yr,$(ALLYR),$(foreach mo,$(ALLMO),$(yr)-$(mo)))
DATES 					+= 2021-01 2021-02 2021-03 2021-04
# goes back a little further
DATES 					+= 2014-12

ALL_PGN_BZ2 		 = $(foreach dat,$(DATES),lichess_db_$(VARIANT)_rated_$(dat).pgn.bz2)
ALL_CSV 				 = $(patsubst %.pgn.bz2,%.csv,$(ALL_PGN_BZ2))

UNIFIED_CSV 		 = all_$(VARIANT).csv
UNIFIED_FST 		 = all_$(VARIANT).fst

download : $(ALL_PGN_BZ2) ## download all variant files
all_csv : $(ALL_CSV) ## process all csv files

DO_TIME 		?= time

help :  ## get this help
	@grep -h -P '^(([^\s]+\s+)*([^\s]+))\s*:.*?##\s*.*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

$(ALL_PGN_BZ2) : %.pgn.bz2 : 
	wget -O $@ https://database.lichess.org/$(VARIANT)/$*.pgn.bz2

% : %.bz2
	bunzip2 -k $<

# I do not need the intermediate pgn laying around
# and make is not deleting the intermediates, so do this nonsense
$(ALL_CSV) : %.csv : parser.py %.pgn.bz2
	bunzip2 -k $*.pgn.bz2
	$(DO_TIME) python3.9 $< $*.pgn $@ 2>./.$*.log
	-rm -f $*.pgn

$(UNIFIED_CSV) : paste.r $(ALL_CSV)
	$(DO_TIME) r $< --outfile=$@ $(ALL_CSV)

$(UNIFIED_FST) : paste.r $(ALL_CSV)
	$(DO_TIME) r $< --outfile=$@ $(ALL_CSV)

unified : $(UNIFIED_FST)  ## make a single unified fst file

#for vim modeline: (do not edit)
# vim:ts=2:sw=2:tw=79:fdm=marker:fmr=FOLDUP,UNFOLD:cms=#%s:tags=tags;:syn=make:ft=make:ai:si:cin:nu:fo=croqt:cino=p0t0c5(0:
