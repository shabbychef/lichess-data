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

doc <- "Usage: paste.r [-v] [-O <OUTFILE>] INFILES...

pastes together a bunch of atomic csv files, rejecting abnormal games, 
and sorting by datetime.

-O OUTFILE --outfile=OUTFILE     Give the outfile as csv or fst [default: all_atomic.fst]
                                 output type depends on file extension.
-v --verbose                     Be more verbose
-h --help                        show this help text"

opt <- docopt(doc)

suppressMessages({
	library(readr)
	library(dplyr)
	library(tidyr)
	library(fst)
	library(magrittr)
})

tot_rows <<- 0

readone <- function(apath) {
  resu <- readr::read_csv(apath,col_types=cols(site = col_character(),
																			 datetime = col_datetime(format = ""),
																			 time_control = col_character(),
																			 termination = col_character(),
																			 move1 = col_character(),
																			 move2 = col_character(),
																			 move3 = col_character(),
																			 move4 = col_character(),
																			 move5 = col_character(),
																			 move6 = col_character(),
																			 move7 = col_character(),
																			 move8 = col_character(),
																			 move9 = col_character(),
																			 move10 = col_character(),
																			 moves = col_character(),
																			 white = col_character(),
																			 black = col_character(),
																			 .default = col_double())) 
	tot_rows <<- tot_rows + nrow(resu)
	resu <- resu %>%
    filter(termination %in% c('Normal','Time forfeit'),
           nzchar(move1) > 0,
           move1 != 'NA',
           !is.na(white_elo),
           !is.na(black_elo)) %>%
	arrange(datetime) 
}

output <- lapply(opt$INFILES,readone) %>%
  bind_rows() %>%
	arrange(datetime)

playnum <- bind_rows(output %>% 
										 rename(pid=white) %>%
										 select(site,pid,datetime),
										 output %>% 
										 rename(pid=black) %>%
										 select(site,pid,datetime)) %>%
	arrange(datetime,pid) %>%
	group_by(pid) %>%
		mutate(gamenum=seq_len(n())) %>%
	ungroup() %>%
	select(-datetime)

output <- output %>%
	left_join(playnum %>% 
						rename(white=pid,
									 white_gamenum=gamenum),
						by=c('site','white')) %>%
	left_join(playnum %>% 
						rename(black=pid,
									 black_gamenum=gamenum),
						by=c('site','black')) 

cat(paste0("total rows: ",tot_rows,"\n"))

if (grepl('.fst$',opt$outfile)) {
	output %>%
		fst::write_fst(opt$outfile,compress=100)
} else {
	output %>%
		readr::write_csv(opt$outfile)
}

#for vim modeline: (do not edit)
# vim:fdm=marker:fmr=FOLDUP,UNFOLD:cms=#%s:syn=r:ft=r
