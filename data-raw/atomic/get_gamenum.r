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

doc <- "Usage: get_gamenum.r [-v] INFILE OUTFILE

reads a csv of game data and computes the game numbers for players.

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

resu <- readr::read_csv(opt$INFILE,
												col_types=cols_only(site = col_character(),
																						datetime = col_datetime(format = ""),
																						white = col_character(),
																						black = col_character()))

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

output <- resu %>%
	left_join(playnum %>% 
						rename(white=pid,
									 white_gamenum=gamenum),
						by=c('site','white')) %>%
	left_join(playnum %>% 
						rename(black=pid,
									 black_gamenum=gamenum),
						by=c('site','black')) %>%
	select(white_gamenum,black_gamenum)

output %>%
	readr::write_csv(opt$OUTFILE)

#for vim modeline: (do not edit)
# vim:fdm=marker:fmr=FOLDUP,UNFOLD:cms=#%s:syn=r:ft=r
