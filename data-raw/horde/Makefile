# note that the python processing step is I/O bound, not compute bound.
# running it in parallel with -j 4 will _not_ speed up total compute time.

VARIANT 				 = horde
VERSION 				 = v1

include ../dates_Makefile

ALLYR 			 		 = 2016 2017 2018 2019 2020 2021 2022 2023 2024

# seem to be some problems with 2015-06 file, there are four games with FEN "?", 
# and parser pukes on those.
#DATES 					 = 2015-04 2015-05 2015-06 2015-07 2015-08 2015-09 2015-10 2015-11 2015-12
DATES 					 = 2015-04 2015-05 2015-07 2015-08 2015-09 2015-10 2015-11 2015-12
DATES 			 		+= $(foreach yr,$(ALLYR),$(foreach mo,$(ALLMO),$(yr)-$(mo)))
DATES 					+= $(CURYR_DATES)

ALL_PGN_ZST 		 = $(foreach dat,$(DATES),lichess_db_$(VARIANT)_rated_$(dat).pgn.zst)
ALL_CSV 				 = $(patsubst %.pgn.zst,%.csv,$(ALL_PGN_ZST))
FIN_CSV 				 = $(patsubst lichess_db_$(VARIANT)_rated_%,processed_$(VARIANT)_%,$(ALL_CSV))

# needs to be after. sigh.
include ../common_Makefile

$(FIN_CSV) : processed_$(VARIANT)_% : attach_gamenum.r lichess_db_$(VARIANT)_rated_% 
	$(DO_TIME) $(LITTLER) $(LITTLER_FLAGS) $^ $@

fin_csv : $(FIN_CSV)  ## final csv files

$(UNIFIED_FST) : converter.r $(UNIFIED_CSV)
	$(DO_TIME) $(LITTLER) $(LITTLER_FLAGS) $^ $@

unified : $(UNIFIED_FST)  ## make a single unified fst file

# this is much more straightforward, but eats all memory on my laptop
$(PASTED_CSV) : paste.r $(ALL_CSV)
	$(DO_TIME) $(LITTLER) $(LITTLER_FLAGS) $< --outfile=$@ $(ALL_CSV)

$(PASTED_FST) : paste.r $(ALL_CSV)
	$(DO_TIME) $(LITTLER) $(LITTLER_FLAGS) $< --outfile=$@ $(ALL_CSV)

pasted: $(PASTED_FST)  ## paste together a unified fst file. deprecated

#for vim modeline: (do not edit)
# vim:ts=2:sw=2:tw=79:fdm=marker:fmr=FOLDUP,UNFOLD:cms=#%s:tags=tags;:syn=make:ft=make:ai:si:cin:nu:fo=croqt:cino=p0t0c5(0:
