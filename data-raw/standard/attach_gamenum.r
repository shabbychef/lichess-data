# /usr/bin/r
#
# Copyright 2021-2021 Steven E. Pav. All Rights Reserved.
# Author: Steven E. Pav 
#
# This file is part of lichess.
#
# lichess is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# lichess is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with lichess.  If not, see <http://www.gnu.org/licenses/>.
#
# Created: 2021.05.01
# Copyright: Steven E. Pav, 2021
# Author: Steven E. Pav <steven@gilgamath.com>
# Comments: Steven E. Pav

suppressMessages(library(docopt))       # we need docopt (>= 0.3) as on CRAN

doc <- "Usage: get_gamenum.r [-v] [-m <MONTHS_BACK>] INFILE OUTFILE

reads a csv of game data and some previous months work of files,
computes the game numbers for players within that given window,
attaches the gamenumber, and produces a CSV or fst file.

-m MONTHS --months_back=MONTHS   Give the number of months back to pull for historical context [default: 6]
-v --verbose                     Be more verbose
-h --help                        show this help text"

opt <- docopt(doc)

suppressMessages({
	library(readr)
	library(dplyr)
	library(tidyr)
	library(fst)
	library(magrittr)
	library(lubridate)
})

# what bullshit is this?
setwd("/home/spav/github/lichess-data/data-raw/standard")
file_to_date <- function(filename) {
	as.Date(gsub('^.+_(20(1[34-9]|2[012345])-(0[1-9]|1[012])).*$','\\1-01',filename),format='%Y-%m-%d')
}
this_month <- file_to_date(opt$INFILE)
start_month <- this_month %m-% months(as.numeric(opt$months_back))
month_seq <- seq(start_month,this_month,by=1)
present_files <- dir(".",pattern="*.csv", full.names=TRUE)
present_files <- present_files[grepl('lichess.+csv$',present_files)]
in_range_file <- sapply(present_files,function(filename) {
	thisd <- file_to_date(filename)
	return(start_month <= thisd && thisd < this_month)
})
readus <- present_files[in_range_file]
	
allout <- readr::read_csv(opt$INFILE,
												col_types=cols(site = col_character(),
																			 datetime = col_datetime(format = ""),
																			 white = col_character(),
																			 black = col_character(),
																			 white_elo = col_double(),
																			 black_elo = col_double(),
																			 white_elo_diff = col_double(),
																			 black_elo_diff = col_double(),
																			 l1_dpawn = col_double(),
																			 l1_dknight = col_double(),
																			 l1_dbishop = col_double(),
																			 l1_drook = col_double(),
																			 l1_dqueen = col_double(),
																			 #l1_dking = col_double(),
																			 rr_dpawn = col_double(),
																			 rr_dknight = col_double(),
																			 rr_dbishop = col_double(),
																			 rr_drook = col_double(),
																			 rr_dqueen = col_double(),
																			 #rr_dking = col_double(),
																			 t1_dpawn = col_double(),
																			 t1_dknight = col_double(),
																			 t1_dbishop = col_double(),
																			 t1_drook = col_double(),
																			 t1_dqueen = col_double(),
																			 #t1_dking = col_double(),
																			 t2_dpawn = col_double(),
																			 t2_dknight = col_double(),
																			 t2_dbishop = col_double(),
																			 t2_drook = col_double(),
																			 t2_dqueen = col_double(),
																			 #t2_dking = col_double(),
																			 t3_dpawn = col_double(),
																			 t3_dknight = col_double(),
																			 t3_dbishop = col_double(),
																			 t3_drook = col_double(),
																			 t3_dqueen = col_double(),
																			 #t3_dking = col_double(),
																			 .default=col_guess()),
													guess_max=2000)

context <- lapply(readus,
									function(filename) {
										readr::read_csv(filename,
																		col_types=cols_only(site = col_character(),
																												datetime = col_datetime(format = ""),
																												white = col_character(),
																												black = col_character()))
									}) %>% 
	bind_rows()



resu <- bind_rows(allout %>% select(site,datetime,white,black),
									context)


playnum <- bind_rows(resu %>%
										 select(site,white,datetime) %>%
										 rename(pid=white),
										 resu %>% 
										 select(site,black,datetime) %>%
										 rename(pid=black)) %>%
	distinct(site,datetime,pid) %>%
	arrange(datetime,pid) %>%
	group_by(pid) %>%
		mutate(gamenum=seq_len(n())) %>%
	ungroup() %>%
	select(-datetime)

output <- allout %>%
	left_join(playnum %>% 
						rename(white=pid,
									 white_gamenum=gamenum),
						by=c('site','white')) %>%
	left_join(playnum %>% 
						rename(black=pid,
									 black_gamenum=gamenum),
						by=c('site','black')) 

if (grepl('\\.fst$',opt$OUTFILE)) {
	output %>%
		fst::write_fst(opt$OUTFILE)
} else {
	output %>%
		readr::write_csv(opt$OUTFILE)
}

#for vim modeline: (do not edit)
# vim:fdm=marker:fmr=FOLDUP,UNFOLD:cms=#%s:syn=r:ft=r
