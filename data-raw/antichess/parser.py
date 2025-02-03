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
import chess
from math import floor
from chess import variant

def seekto(game,at_ply):
    """
    take a pgn of a game, then play to just after at_ply,
    returning the board
    """
    myb = game.end().board()
    ms = myb.move_stack
    # no easy way to do this.
    subs = ms[0:at_ply]
    #newb = chess.variant.AtomicBoard()
    newb = chess.variant.AntichessBoard()
    for move in subs:
        newb.push(move)
    return newb

def fibu_str(astring,A=0.61803399,m=2**31):
    from math import floor
    from functools import reduce
    lowy = ord('0')
    fbits = [(ord(c)-lowy)*A for c in astring]
    return (reduce(lambda a, b: (a + m * b) % 1,fbits))

def pos_seek(game,rando,min_rat=0,max_rat=1,min_ply=2,max_ply=None,new_board_func=lambda:variant.AntichessBoard()):
    """
    seek to a position

    let n be the number of ply in the game. 
    let l = max(min_rat*n,min_ply,0)
    let u = min(max_rat*n,max_ply,n+1)
    
    computes floor(l + r * (u-l)) and seeks to that position, returning a board.

    if max_ply is given as None, it is ignored. 
    you can set max_rat > 1 to possibly get
    the ending position (which seems uninteresting to me.)

    returns:
        the board
        the ply number
        whether the next move would take a piece.
    """
    myb = game.end().board()
    ms = myb.move_stack
    nnn = len(ms)
    lll = max(max(nnn*min_rat,min_ply),0)
    uuu = min(nnn*max_rat,nnn+1)
    if max_ply is not None:
        uuu = min(uuu,max_ply)
    # just in case
    uuu = max(uuu,lll)
    at_ply = floor(lll + rando * (uuu-lll))
    subs = ms[0:at_ply]
    newb = new_board_func()
    for move in subs:
        newb.push(move)
    try:
        if at_ply >= len(ms):
            next_take = False
        else:
            next_take = newb.is_capture(ms[at_ply])
    except Exception as err:
        print(f"CRAP {len(ms)} {at_ply} {ms}")
        raise
    return (newb,at_ply,next_take)


def dpieces_slow(endb):
    """
    This turns out to be quite slower than the other version...
    return tuple of differences in piece counts
    """
    dPAWN = len(endb.pieces(chess.PAWN,chess.WHITE)) - len(endb.pieces(chess.PAWN,chess.BLACK))
    dKNIGHT = len(endb.pieces(chess.KNIGHT,chess.WHITE)) - len(endb.pieces(chess.KNIGHT,chess.BLACK))
    dBISHOP = len(endb.pieces(chess.BISHOP,chess.WHITE)) - len(endb.pieces(chess.BISHOP,chess.BLACK))
    dROOK = len(endb.pieces(chess.ROOK,chess.WHITE)) - len(endb.pieces(chess.ROOK,chess.BLACK))
    dQUEEN = len(endb.pieces(chess.QUEEN,chess.WHITE)) - len(endb.pieces(chess.QUEEN,chess.BLACK))
    dKING = len(endb.pieces(chess.KING,chess.WHITE)) - len(endb.pieces(chess.KING,chess.BLACK))
    return (dPAWN,dKNIGHT,dBISHOP,dROOK,dQUEEN,dKING)

def dpieces(endb):
    """
    return tuple of differences in piece counts
    """
    dPAWN = (endb.occupied_co[chess.WHITE] & endb.pawns).bit_count() - (endb.occupied_co[chess.BLACK] & endb.pawns).bit_count()
    dKNIGHT = (endb.occupied_co[chess.WHITE] & endb.knights).bit_count() - (endb.occupied_co[chess.BLACK] & endb.knights).bit_count()
    dBISHOP = (endb.occupied_co[chess.WHITE] & endb.bishops).bit_count() - (endb.occupied_co[chess.BLACK] & endb.bishops).bit_count()
    dROOK = (endb.occupied_co[chess.WHITE] & endb.rooks).bit_count() - (endb.occupied_co[chess.BLACK] & endb.rooks).bit_count()
    dQUEEN = (endb.occupied_co[chess.WHITE] & endb.queens).bit_count() - (endb.occupied_co[chess.BLACK] & endb.queens).bit_count()
    dKING = (endb.occupied_co[chess.WHITE] & endb.kings).bit_count() - (endb.occupied_co[chess.BLACK] & endb.kings).bit_count()
    return (dPAWN,dKNIGHT,dBISHOP,dROOK,dQUEEN,dKING)

def pgn_gen(pgn):
    from math import floor
    import chess.pgn
    from re import sub,compile
    rpat = compile("https?://lichess.org/")
    nmove = 10
    d_piece_suffixes = ['dpawn','dknight','dbishop','drook','dqueen','dking',]
    suffixes = [*d_piece_suffixes,'next_take',]
    prefixes = ['l1','rr','t1','t2','t3']
    # have to be careful about the ordering of that double zip...
    yield ('site','datetime','time_control','termination','outcome','nply',
            *[f"move{i}" for i in range(1,nmove+1)],
            'moves',
            'white','black',
            'white_elo','black_elo','white_elo_diff','black_elo_diff',
            *[ f"{bit}_ply" for bit in ['rr','t1','t2','t3'] ],
            *[ f"{pre}_{suf}" for pre in prefixes for suf in suffixes])
    # empty
    mt_dp = tuple(float('nan') for i in range(len(d_piece_suffixes)))
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
            movel = ":".join(moves)
            if (len(moves) > nmove):
                moves = moves[0:nmove]
            else:
                for iii in range(len(moves),nmove):
                    moves.append('')
            try:
                wdiff = int(rhed['WhiteRatingDiff'])
                bdiff = int(rhed['BlackRatingDiff'])
            except:
                wdiff = float('nan')
                bdiff = float('nan')
            try:
                lmov = endb.pop()
                d_l1 = dpieces(endb)
                l1_take = endb.is_capture(lmov)
            except:
                d_l1 = mt_dp
                l1_take = False
            # pseudo random locations
            randbit = fibu_str(site)
            (rr_board,rr_ply,rr_take) = pos_seek(gam,randbit,min_rat=0,max_rat=1,min_ply=2)
            d_rr = dpieces(rr_board)
            # squeeze more randomness out of randbit? seems dangerous..
            m = 2**31
            rbit_t1 = ((floor(m * randbit) << 4) / m) % 1
            (t1_board,t1_ply,t1_take) = pos_seek(gam,rbit_t1,min_rat=0,max_rat=0.33333,min_ply=2)
            d_t1 = dpieces(t1_board)
            rbit_t2 = ((floor(m * randbit) << 8) / m) % 1
            (t2_board,t2_ply,t2_take) = pos_seek(gam,rbit_t2,min_rat=0.33333,max_rat=0.66667,min_ply=2)
            d_t2 = dpieces(t2_board)
            rbit_t3 = ((floor(m * randbit) << 12) / m) % 1
            (t3_board,t3_ply,t3_take) = pos_seek(gam,rbit_t3,min_rat=0.66667,max_rat=1.00000,min_ply=2)
            d_t3 = dpieces(t3_board)
        else:
            movel = ''
            # could also be 'Time forfeit', 'Abandoned'
            moves = ['' for x in range(nmove)]
            wdiff = bdiff = float('nan')
            nply = float('nan')
            rr_ply = t1_ply = t2_ply = t3_ply = 0
            d_l1 = d_rr = d_t1 = d_t2 = d_t3 = mt_dp
            rr_take = l1_take = t1_take = t2_take = t3_take = False
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
               movel,
               white,black,welo,belo,wdiff,bdiff,
               rr_ply,t1_ply,t2_ply,t3_ply,
               *d_l1,l1_take,
               *d_rr,rr_take,
               *d_t1,t1_take,
               *d_t2,t2_take,
               *d_t3,t3_take)
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
