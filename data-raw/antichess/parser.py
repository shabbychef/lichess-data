#! /usr/bin/env python
# coding: utf-8
#
"""antichess pgn to csv conversion

we mostly care about move sequence, tbh
but perhaps some pieces are stronger than others in anti

Usage:
  parser.py INPGN OUTCSV

"""

from docopt import docopt
from parsing import pgn_gen
import csv

# module as script
if __name__ == "__main__":
    arguments = docopt(__doc__, version="parser.py 1.0")
    pgn = open(arguments["INPGN"])
    with open(arguments["OUTCSV"], "w") as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=",", lineterminator="\n")
        iter = 0
        for result in pgn_gen(
            pgn,
            include_movel=False,
            include_king=True,
            include_passed_pawn=False,
            include_pawn_rank=False,
        ):
            iter += 1
            if iter % 50_000 == 0:
                print(f"finished {iter=} rows")
            spamwriter.writerow(result)
        csvfile.close()

# for vim modeline: (do not edit)
# vim:ts=4:sw=4:sts=4:tw=79:sta:et:ai:nu:fdm=indent:syn=python:ft=python:tag=.py_tags;:cin:fo=croql
