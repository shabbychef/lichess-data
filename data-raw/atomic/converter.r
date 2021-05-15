# /usr/bin/r
#
# Copyright 2021-2021 Steven E. Pav. All Rights Reserved.
# Author: Steven E. Pav 
#
# This file is part of data-raw.
#
# data-raw is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# data-raw is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with data-raw.  If not, see <http://www.gnu.org/licenses/>.
#
# Created: 2021.05.14
# Copyright: Steven E. Pav, 2021
# Author: Steven E. Pav <steven@gilgamath.com>
# Comments: Steven E. Pav

suppressMessages(library(docopt))       # we need docopt (>= 0.3) as on CRAN

doc <- "Usage: converter.r [-v] INFILE OUTFILE

convert a csv to fst.

-v --verbose                     Be more verbose
-h --help                        show this help text"

opt <- docopt(doc)

suppressMessages({
	library(readr)
	library(fst)
	library(magrittr)
})

readr::read_csv(opt$INFILE,
								col_types=cols(site = col_character(),
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
															 .default = col_double())) %>%
	fst::write_fst(opt$OUTFILE,compress=100)

#for vim modeline: (do not edit)
# vim:fdm=marker:fmr=FOLDUP,UNFOLD:cms=#%s:syn=r:ft=r
