#! /usr/bin/env python
# coding: utf-8
#
"""standard chess pgn to csv conversion

we mostly care about move sequence, tbh
but perhaps some pieces are stronger than others in anti

Usage:
  parser.py INPGN OUTCSV

"""

from ..parsing import fib_str, pos_seek, dpieces

import chess
from chess import variant, pgn
from re import sub,compile

from docopt import docopt
from math import floor

def pgn_gen(pgn):
    rpat = compile("https?://lichess.org/")
    nmove = 10
    suffixes = ['dpawn','dknight','dbishop','drook','dqueen',] # 'dking']
    prefixes = ['l1','rr','t1','t2','t3']
    # have to be careful about the ordering of that double zip...
    yield ('site','datetime','time_control','termination','outcome','nply',
            *[f"move{i}" for i in range(1,nmove+1)],
            # 'moves',
            'white','black',
            'white_elo','black_elo','white_elo_diff','black_elo_diff',
            *[ f"{bit}_ply" for bit in ['rr','t1','t2','t3'] ],
            *[ f"{pre}_{suf}" for pre in prefixes for suf in suffixes])
    # empty
    mt_dp = tuple(float('nan') for i in range(len(suffixes)))
    while (pgn):
        gam = chess.pgn.read_game(pgn)
        try:
            rhed = gam.headers
        except:
            # I believe you get here when you reach end of file. break and return then
            break
        term = rhed['Termination']
        tc = rhed['TimeControl']
        # an ID for the game
        site = sub(rpat,'',rhed['Site']) 
        # now use this to seek to random, first 1/3, middle 1/3, late 1/3 positions.
        # we have Normal, Time forfeit, Abandoned
        if term != 'Abandoned':
            try:
                ending = gam.end()
                endb = ending.board()
                moves = [str(x) for x in endb.move_stack]
            except:
                moves = []
            nply = len(moves)
            # movel = ":".join(moves)
            if (len(moves) > nmove):
                moves = moves[0:nmove]
            else:
                moves.extend([''] * (nmove - len(moves)))
            try:
                wdiff = int(rhed['WhiteRatingDiff'])
                bdiff = int(rhed['BlackRatingDiff'])
            except:
                wdiff = float('nan')
                bdiff = float('nan')
            try:
                lmov = endb.pop()
                d_l1 = dpieces(endb)
            except:
                d_l1 = mt_dp
            # pseudo random locations
            randbit = fibu_str(site)
            (rr_board,rr_ply) = pos_seek(gam,randbit,min_rat=0,max_rat=1,min_ply=2)
            d_rr = dpieces(rr_board)
            # squeeze more randomness out of randbit? seems dangerous..
            m = 2**31
            rbit_t1 = ((floor(m * randbit) << 4) / m) % 1
            (t1_board,t1_ply) = pos_seek(gam,rbit_t1,min_rat=0,max_rat=0.33333,min_ply=2)
            d_t1 = dpieces(t1_board)
            rbit_t2 = ((floor(m * randbit) << 8) / m) % 1
            (t2_board,t2_ply) = pos_seek(gam,rbit_t2,min_rat=0.33333,max_rat=0.66667,min_ply=2)
            d_t2 = dpieces(t2_board)
            rbit_t3 = ((floor(m * randbit) << 12) / m) % 1
            (t3_board,t3_ply) = pos_seek(gam,rbit_t3,min_rat=0.66667,max_rat=1.00000,min_ply=2)
            d_t3 = dpieces(t3_board)
        else:
            # movel = ''
            # could also be 'Time forfeit', 'Abandoned'
            moves = [''] * nmove
            wdiff = float('nan')
            bdiff = float('nan')
            nply = float('nan')
            rr_ply = 0
            t1_ply = 0
            t2_ply = 0
            t3_ply = 0
            d_l1 = mt_dp
            d_rr = mt_dp
            d_t1 = mt_dp
            d_t2 = mt_dp
            d_t3 = mt_dp
        # outcome from white's pov, as a number:
        if rhed['Result'] == '1-0':
            outcome = 1.0
        elif rhed['Result'] == '0-1':
            outcome = 0.0
        elif rhed['Result'] == '1/2-1/2':
            outcome = 0.5
        else:
            outcome = float('nan')
        # who is playing
        try:
            white = rhed['White']
            black = rhed['Black']
        except:
            white = ''
            black = ''
        # whie and black elo
        try:
            welo = int(rhed['WhiteElo'])
        except:
            welo = float('nan')
        try:
            belo = int(rhed['BlackElo'])
        except:
            belo = float('nan')

        try:
            dat = sub('\.','-',rhed['UTCDate'])
            datetime = f"{dat}T{rhed['UTCTime']}Z"
        except:
            datetime = ''
        yield (site,datetime,tc,term,outcome,nply,
                *moves,
                # movel,
                white,black,welo,belo,wdiff,bdiff,
                rr_ply,t1_ply,t2_ply,t3_ply,
                *d_l1,
                *d_rr,*d_t1,*d_t2,*d_t3)
    pgn.close()
    return

# module as script
if __name__ == "__main__":
    import csv
    arguments = docopt(__doc__, version='parser.py 1.0')
    pgn = open(arguments['INPGN'])
    with open(arguments['OUTCSV'], 'w') as csvfile:
        spamwriter = csv.writer(csvfile,delimiter=',', lineterminator='\n')
        iter = 0
        for result in pgn_gen(pgn):
            iter += 1
            if iter % 50_000 == 0:
                print(f"finished {iter=} rows")
            spamwriter.writerow(result)
        csvfile.close()

#for vim modeline: (do not edit)
# vim:ts=4:sw=4:sts=4:tw=79:sta:et:ai:nu:fdm=indent:syn=python:ft=python:tag=.py_tags;:cin:fo=croql
