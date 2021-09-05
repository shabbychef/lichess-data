
.PHONY : download all_csv unified pasted

.PRECIOUS : %.bz2

VERSION 				 = v1
VARIANT 				 = horde

ALLMO 			 		 = 01 02 03 04 05 06 07 08 09 10 11 12
ALLYR 			 		 = 2016 2017 2018 2019 2020
# seem to be some problems with 2015-06 file, there are four games with FEN "?", 
# and parser pukes on those.
#DATES 					 = 2015-04 2015-05 2015-06 2015-07 2015-08 2015-09 2015-10 2015-11 2015-12
DATES 					 = 2015-04 2015-05 2015-07 2015-08 2015-09 2015-10 2015-11 2015-12
DATES 			 		+= $(foreach yr,$(ALLYR),$(foreach mo,$(ALLMO),$(yr)-$(mo)))
DATES 					+= 2021-01 2021-02 2021-03 2021-04 2021-05 2021-06

ALL_PGN_BZ2 		 = $(foreach dat,$(DATES),lichess_db_$(VARIANT)_rated_$(dat).pgn.bz2)
ALL_CSV 				 = $(patsubst %.pgn.bz2,%.csv,$(ALL_PGN_BZ2))

UNIFIED_CSV 		 = unified_$(VARIANT)_$(VERSION).csv
UNIFIED_FST 		 = unified_$(VARIANT)_$(VERSION).fst
# deprecated
PASTED_CSV  		 = pasted_$(VARIANT).csv
PASTED_FST  		 = pasted_$(VARIANT).fst

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
	bunzip2 -k -f $*.pgn.bz2
	$(DO_TIME) python3.9 $< $*.pgn $@ 2>./.$*.log
	-rm -f $*.pgn

# have to use linux command line to paste together a bunch of csvs
$(UNIFIED_CSV) : $(ALL_CSV)
	$(eval tempf = .gamenum.csv)
	head -n 1 $< > .$@
	tail -n +2 $^ | grep -P ',(Normal|Time forfeit),' >> .$@
	r get_gamenum.r .$@ $(tempf)
	paste -d ',' .$@ $(tempf) > $@
	-rm .$@ $(tempf)

%.csv.gz : %.csv
	gzip -k $<

$(UNIFIED_FST) : converter.r $(UNIFIED_CSV)
	$(DO_TIME) r $^ $@

unified : $(UNIFIED_FST)  ## make a single unified fst file

unigz : $(UNIFIED_CSV).gz  ## gzip a unified csv file

# this is much more straightforward, but eats all memory on my laptop
$(PASTED_CSV) : paste.r $(ALL_CSV)
	$(DO_TIME) r $< --outfile=$@ $(ALL_CSV)

$(PASTED_FST) : paste.r $(ALL_CSV)
	$(DO_TIME) r $< --outfile=$@ $(ALL_CSV)

pasted: $(PASTED_FST)  ## paste together a unified fst file. deprecated

#for vim modeline: (do not edit)
# vim:ts=2:sw=2:tw=79:fdm=marker:fmr=FOLDUP,UNFOLD:cms=#%s:tags=tags;:syn=make:ft=make:ai:si:cin:nu:fo=croqt:cino=p0t0c5(0:
