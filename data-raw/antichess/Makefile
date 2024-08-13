
.PHONY : download all_csv unified pasted

.PRECIOUS : %.bz2, %.zst

PYTHON 				  ?= python3.8
VERSION 				 = v1
VARIANT 				 = antichess

ALLMO 			 		 = 01 02 03 04 05 06 07 08 09 10 11 12
ALLYR 			 		 = 2015 2016 2017 2018 2019 2020 2021 2022 2023
# goes back a little further
DATES 					 = 2014-12
DATES 			 		+= $(foreach yr,$(ALLYR),$(foreach mo,$(ALLMO),$(yr)-$(mo)))
DATES 					+= 2024-01 2024-02 2024-03 2024-04 2024-05 2024-06 2024-07

ALL_PGN_BZ2 		 = $(foreach dat,$(DATES),lichess_db_$(VARIANT)_rated_$(dat).pgn.bz2)
ALL_PGN_ZST 		 = $(foreach dat,$(DATES),lichess_db_$(VARIANT)_rated_$(dat).pgn.zst)
ALL_CSV 				 = $(patsubst %.pgn.zst,%.csv,$(ALL_PGN_ZST))

STACKED_CSV      = stacked_$(VARIANT).csv
UNIFIED_CSV 		 = unified_$(VARIANT)_$(VERSION).csv
UNIFIED_FST 		 = unified_$(VARIANT)_$(VERSION).fst
# deprecated
PASTED_CSV  		 = pasted_$(VARIANT).csv
PASTED_FST  		 = pasted_$(VARIANT).fst

DUCKDB 					?= duckdb
DUCKDB_ZIP			 = duckdb_cli-linux-amd64.zip

download : $(ALL_PGN_ZST) ## download all variant files
all_csv : $(ALL_CSV) ## process all csv files

DO_TIME 		?= time

help :  ## get this help
	@grep -h -P '^(([^\s]+\s+)*([^\s]+))\s*:.*?##\s*.*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

$(ALL_PGN_BZ2) : %.pgn.bz2 : 
	wget -O $@ https://database.lichess.org/$(VARIANT)/$*.pgn.bz2

$(ALL_PGN_ZST) : %.pgn.zst : 
	wget -O $@ https://database.lichess.org/$(VARIANT)/$*.pgn.zst

% : %.bz2
	bunzip2 -k $<

% : %.zst
	unzstd $<

# I do not need the intermediate pgn laying around
# and make is not deleting the intermediates, so do this nonsense
$(ALL_CSV) : %.csv : parser.py %.pgn.zst
	unzstd -k -f $*.pgn.zst
	$(DO_TIME) $(PYTHON) $< $*.pgn $@ 2>./.$*.log
	-rm -f $*.pgn

stacked_csv : $(STACKED_CSV) ## paste all dated csv together into 1

$(STACKED_CSV) : $(ALL_CSV) 
	head -n 1 $< > $@
	tail -n +2 $^ | grep -P ',(Normal|Time forfeit),' >> $@

# have to use linux command line to paste together a bunch of csvs
$(UNIFIED_CSV) : $(ALL_CSV)
	$(eval tempf = .gamenum.csv)
	head -n 1 $< > .$@
	tail -n +2 $^ | grep -P ',(Normal|Time forfeit),' >> .$@
	r get_gamenum.r .$@ $(tempf)
	paste -d ',' .$@ $(tempf) > $@
	-rm .$@ $(tempf)

unified_csv : $(UNIFIED_CSV)  ## make a single unified csv file

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

$(DUCKDB) : $(DUCKDB_ZIP)
	unzip $^

$(DUCKDB_ZIP) :
	wget -O $@ https://github.com/duckdb/duckdb/releases/download/v1.0.0/duckdb_cli-linux-amd64.zip

#for vim modeline: (do not edit)
# vim:ts=2:sw=2:tw=79:fdm=marker:fmr=FOLDUP,UNFOLD:cms=#%s:tags=tags;:syn=make:ft=make:ai:si:cin:nu:fo=croqt:cino=p0t0c5(0:
