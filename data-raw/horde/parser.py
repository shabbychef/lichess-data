#! /usr/bin/env python
# coding: utf-8
#
"""atomic pgn to csv conversion

Usage:
  parser.py INPGN OUTCSV

"""

from docopt import docopt

# these are all abandoned
def fibonacci_hash(x,A=0.6180339887,m=2**31):
    """Fibonacci hash"""
    from math import floor
    return floor(m * ((x*A) % 1))

def fibonacci_strhash(astring,A=0.6180339887,m=2**31):
    from math import floor
    lowy = ord('0')
    return floor(m * (sum([(ord(c)-lowy)*A for c in astring]) % 1))

def seekto(game,at_ply):
    """
    take a pgn of a game, then play to just after at_ply,
    returning the board
    """
    myb = game.end().board()
    ms = myb.move_stack
    # no easy way to do this.
    subs = ms[0:at_ply]
    newb = chess.variant.HordeBoard()
    for move in subs:
        newb.push(move)
    return newb

def fibu_str(astring,A=0.61803399,m=2**31):
    from math import floor
    from functools import reduce
    lowy = ord('0')
    fbits = [(ord(c)-lowy)*A for c in astring]
    return (reduce(lambda a, b: (a + m * b) % 1,fbits))

def pos_seek(game,rando,min_rat=0,max_rat=1,min_ply=2,max_ply=None):
    """
    seek to a position

    let n be the number of ply in the game. 
    let l = max(min_rat*n,min_ply,0)
    let u = min(max_rat*n,max_ply,n+1)
    
    computes floor(l + r * (u-l)) and seeks to that position, returning a board.

    if max_ply is given as None, it is ignored. 
    you can set max_rat > 1 to possibly get
    the ending position (which seems uninteresting to me.)
    """
    from math import floor
    from chess import variant
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
    newb = variant.HordeBoard()
    for move in subs:
        newb.push(move)
    return (newb,at_ply)

def passed_pawn_count(board):
    """
    compute symmetric passed pawn count as a tuple.
    returns a count of passed pawns at 234 5 6 and pawn at 7
    again this is symmetric, so it is white's count minus black's count
    """
    import chess
    # passed pawn mask for white; 
    # which squares are in 'front of' the given square and can block passers
    FRONT_A6 = chess.SquareSet(chess.BB_A7 | chess.BB_B7)
    FRONT_A5 = FRONT_A6 | chess.BB_A6 | chess.BB_B6
    FRONT_A4 = FRONT_A5 | chess.BB_A5 | chess.BB_B5
    FRONT_A3 = FRONT_A4 | chess.BB_A4 | chess.BB_B4
    FRONT_A2 = FRONT_A3 | chess.BB_A3 | chess.BB_B3
    #
    FRONT_B6 = chess.SquareSet(chess.BB_A7 | chess.BB_B7 | chess.BB_C7)
    FRONT_B5 = FRONT_B6 | chess.BB_A6 | chess.BB_B6 | chess.BB_C6
    FRONT_B4 = FRONT_B5 | chess.BB_A5 | chess.BB_B5 | chess.BB_C5
    FRONT_B3 = FRONT_B4 | chess.BB_A4 | chess.BB_B4 | chess.BB_C4
    FRONT_B2 = FRONT_B3 | chess.BB_A3 | chess.BB_B3 | chess.BB_C3
    #
    FRONT_C6 = chess.SquareSet(chess.BB_B7 | chess.BB_C7 | chess.BB_D7)
    FRONT_C5 = FRONT_C6 | chess.BB_B6 | chess.BB_C6 | chess.BB_D6
    FRONT_C4 = FRONT_C5 | chess.BB_B5 | chess.BB_C5 | chess.BB_D5
    FRONT_C3 = FRONT_C4 | chess.BB_B4 | chess.BB_C4 | chess.BB_D4
    FRONT_C2 = FRONT_C3 | chess.BB_B3 | chess.BB_C3 | chess.BB_D3
    #
    FRONT_D6 = chess.SquareSet(chess.BB_C7 | chess.BB_D7 | chess.BB_E7)
    FRONT_D5 = FRONT_D6 | chess.BB_C6 | chess.BB_D6 | chess.BB_E6
    FRONT_D4 = FRONT_D5 | chess.BB_C5 | chess.BB_D5 | chess.BB_E5
    FRONT_D3 = FRONT_D4 | chess.BB_C4 | chess.BB_D4 | chess.BB_E4
    FRONT_D2 = FRONT_D3 | chess.BB_C3 | chess.BB_D3 | chess.BB_E3
    #
    FRONT_E6 = chess.SquareSet(chess.BB_D7 | chess.BB_E7 | chess.BB_F7)
    FRONT_E5 = FRONT_E6 | chess.BB_D6 | chess.BB_E6 | chess.BB_F6
    FRONT_E4 = FRONT_E5 | chess.BB_D5 | chess.BB_E5 | chess.BB_F5
    FRONT_E3 = FRONT_E4 | chess.BB_D4 | chess.BB_E4 | chess.BB_F4
    FRONT_E2 = FRONT_E3 | chess.BB_D3 | chess.BB_E3 | chess.BB_F3
    #
    FRONT_F6 = chess.SquareSet(chess.BB_E7 | chess.BB_F7 | chess.BB_G7)
    FRONT_F5 = FRONT_F6 | chess.BB_E6 | chess.BB_F6 | chess.BB_G6
    FRONT_F4 = FRONT_F5 | chess.BB_E5 | chess.BB_F5 | chess.BB_G5
    FRONT_F3 = FRONT_F4 | chess.BB_E4 | chess.BB_F4 | chess.BB_G4
    FRONT_F2 = FRONT_F3 | chess.BB_E3 | chess.BB_F3 | chess.BB_G3
    #
    FRONT_G6 = chess.SquareSet(chess.BB_F7 | chess.BB_G7 | chess.BB_H7)
    FRONT_G5 = FRONT_G6 | chess.BB_F6 | chess.BB_G6 | chess.BB_H6
    FRONT_G4 = FRONT_G5 | chess.BB_F5 | chess.BB_G5 | chess.BB_H5
    FRONT_G3 = FRONT_G4 | chess.BB_F4 | chess.BB_G4 | chess.BB_H4
    FRONT_G2 = FRONT_G3 | chess.BB_F3 | chess.BB_G3 | chess.BB_H3
    #
    FRONT_H6 = chess.SquareSet(chess.BB_G7 | chess.BB_H7)
    FRONT_H5 = FRONT_H6 | chess.BB_G6 | chess.BB_H6
    FRONT_H4 = FRONT_H5 | chess.BB_G5 | chess.BB_H5
    FRONT_H3 = FRONT_H4 | chess.BB_G4 | chess.BB_H4
    FRONT_H2 = FRONT_H3 | chess.BB_G3 | chess.BB_H3
    #
    BACK_H7 = FRONT_H2.mirror()
    BACK_H6 = FRONT_H3.mirror()
    BACK_H5 = FRONT_H4.mirror()
    BACK_H4 = FRONT_H5.mirror()
    BACK_H3 = FRONT_H6.mirror()
    #
    BACK_G7 = FRONT_G2.mirror()
    BACK_G6 = FRONT_G3.mirror()
    BACK_G5 = FRONT_G4.mirror()
    BACK_G4 = FRONT_G5.mirror()
    BACK_G3 = FRONT_G6.mirror()
    #
    BACK_F7 = FRONT_F2.mirror()
    BACK_F6 = FRONT_F3.mirror()
    BACK_F5 = FRONT_F4.mirror()
    BACK_F4 = FRONT_F5.mirror()
    BACK_F3 = FRONT_F6.mirror()
    #
    BACK_E7 = FRONT_E2.mirror()
    BACK_E6 = FRONT_E3.mirror()
    BACK_E5 = FRONT_E4.mirror()
    BACK_E4 = FRONT_E5.mirror()
    BACK_E3 = FRONT_E6.mirror()
    #
    BACK_D7 = FRONT_D2.mirror()
    BACK_D6 = FRONT_D3.mirror()
    BACK_D5 = FRONT_D4.mirror()
    BACK_D4 = FRONT_D5.mirror()
    BACK_D3 = FRONT_D6.mirror()
    #
    BACK_C7 = FRONT_C2.mirror()
    BACK_C6 = FRONT_C3.mirror()
    BACK_C5 = FRONT_C4.mirror()
    BACK_C4 = FRONT_C5.mirror()
    BACK_C3 = FRONT_C6.mirror()
    #
    BACK_B7 = FRONT_B2.mirror()
    BACK_B6 = FRONT_B3.mirror()
    BACK_B5 = FRONT_B4.mirror()
    BACK_B4 = FRONT_B5.mirror()
    BACK_B3 = FRONT_B6.mirror()
    #
    BACK_A7 = FRONT_A2.mirror()
    BACK_A6 = FRONT_A3.mirror()
    BACK_A5 = FRONT_A4.mirror()
    BACK_A4 = FRONT_A5.mirror()
    BACK_A3 = FRONT_A6.mirror()
    #
    PASSER_WHITE_R2 = [ (chess.BB_A2,FRONT_A2) , (chess.BB_B2,FRONT_B2) , (chess.BB_C2,FRONT_C2) , (chess.BB_D2,FRONT_D2) , 
            (chess.BB_E2,FRONT_E2) , (chess.BB_F2,FRONT_F2) , (chess.BB_G2,FRONT_G2) , (chess.BB_H2,FRONT_H2) , ]
    PASSER_WHITE_R3 = [ (chess.BB_A3,FRONT_A3) , (chess.BB_B3,FRONT_B3) , (chess.BB_C3,FRONT_C3) , (chess.BB_D3,FRONT_D3) , 
            (chess.BB_E3,FRONT_E3) , (chess.BB_F3,FRONT_F3) , (chess.BB_G3,FRONT_G3) , (chess.BB_H3,FRONT_H3) , ]
    PASSER_WHITE_R4 = [ (chess.BB_A4,FRONT_A4) , (chess.BB_B4,FRONT_B4) , (chess.BB_C4,FRONT_C4) , (chess.BB_D4,FRONT_D4) , 
            (chess.BB_E4,FRONT_E4) , (chess.BB_F4,FRONT_F4) , (chess.BB_G4,FRONT_G4) , (chess.BB_H4,FRONT_H4) , ]
    PASSER_WHITE_R5 = [ (chess.BB_A5,FRONT_A5) , (chess.BB_B5,FRONT_B5) , (chess.BB_C5,FRONT_C5) , (chess.BB_D5,FRONT_D5) , 
            (chess.BB_E5,FRONT_E5) , (chess.BB_F5,FRONT_F5) , (chess.BB_G5,FRONT_G5) , (chess.BB_H5,FRONT_H5) , ]
    PASSER_WHITE_R6 = [ (chess.BB_A6,FRONT_A6) , (chess.BB_B6,FRONT_B6) , (chess.BB_C6,FRONT_C6) , (chess.BB_D6,FRONT_D6) , 
            (chess.BB_E6,FRONT_E6) , (chess.BB_F6,FRONT_F6) , (chess.BB_G6,FRONT_G6) , (chess.BB_H6,FRONT_H6) , ]
    PASSER_WHITE_R234 = [ *PASSER_WHITE_R2, *PASSER_WHITE_R3, *PASSER_WHITE_R4 ]
    #
    PASSER_BLACK_R7 = [ (chess.BB_A7,BACK_A7) , (chess.BB_B7,BACK_B7) , (chess.BB_C7,BACK_C7) , (chess.BB_D7,BACK_D7) , 
            (chess.BB_E7,BACK_E7) , (chess.BB_F7,BACK_F7) , (chess.BB_G7,BACK_G7) , (chess.BB_H7,BACK_H7) , ]
    PASSER_BLACK_R6 = [ (chess.BB_A6,BACK_A6) , (chess.BB_B6,BACK_B6) , (chess.BB_C6,BACK_C6) , (chess.BB_D6,BACK_D6) , 
            (chess.BB_E6,BACK_E6) , (chess.BB_F6,BACK_F6) , (chess.BB_G6,BACK_G6) , (chess.BB_H6,BACK_H6) , ]
    PASSER_BLACK_R5 = [ (chess.BB_A5,BACK_A5) , (chess.BB_B5,BACK_B5) , (chess.BB_C5,BACK_C5) , (chess.BB_D5,BACK_D5) , 
            (chess.BB_E5,BACK_E5) , (chess.BB_F5,BACK_F5) , (chess.BB_G5,BACK_G5) , (chess.BB_H5,BACK_H5) , ]
    PASSER_BLACK_R4 = [ (chess.BB_A4,BACK_A4) , (chess.BB_B4,BACK_B4) , (chess.BB_C4,BACK_C4) , (chess.BB_D4,BACK_D4) , 
            (chess.BB_E4,BACK_E4) , (chess.BB_F4,BACK_F4) , (chess.BB_G4,BACK_G4) , (chess.BB_H4,BACK_H4) , ]
    PASSER_BLACK_R3 = [ (chess.BB_A3,BACK_A3) , (chess.BB_B3,BACK_B3) , (chess.BB_C3,BACK_C3) , (chess.BB_D3,BACK_D3) , 
            (chess.BB_E3,BACK_E3) , (chess.BB_F3,BACK_F3) , (chess.BB_G3,BACK_G3) , (chess.BB_H3,BACK_H3) , ]
    PASSER_BLACK_R765 = [ *PASSER_BLACK_R7, *PASSER_BLACK_R6, *PASSER_BLACK_R5 ]
    #
    WP = board.pieces(chess.PAWN,chess.WHITE)
    BP = board.pieces(chess.PAWN,chess.BLACK)
    pp_234 = (sum([max(0,len(WP & x[0]) - len(BP & x[1])) for x in PASSER_WHITE_R234]) -
            sum([max(0,len(BP & x[0]) - len(WP & x[1])) for x in PASSER_BLACK_R765]))
    pp_5 = (sum([max(0,len(WP & x[0]) - len(BP & x[1])) for x in PASSER_WHITE_R5]) -
            sum([max(0,len(BP & x[0]) - len(WP & x[1])) for x in PASSER_BLACK_R4]))
    pp_6 = (sum([max(0,len(WP & x[0]) - len(BP & x[1])) for x in PASSER_WHITE_R6]) -
            sum([max(0,len(BP & x[0]) - len(WP & x[1])) for x in PASSER_BLACK_R3]))
    pp_7 = (len(WP & chess.BB_RANK_7) - len(BP & chess.BB_RANK_2))
    return (pp_234,pp_5,pp_6,pp_7)

def dpawn_rank(board):
    """
    pawn rank count difference of pawn rank
    """
    import chess
    WP = board.pieces(chess.PAWN,chess.WHITE)
    BP = board.pieces(chess.PAWN,chess.BLACK)
    dPAWN2 = (len(WP & chess.BB_RANK_2) - len(BP & chess.BB_RANK_7))
    dPAWN3 = (len(WP & chess.BB_RANK_3) - len(BP & chess.BB_RANK_6))
    dPAWN4 = (len(WP & chess.BB_RANK_4) - len(BP & chess.BB_RANK_5))
    return (dPAWN2,dPAWN3,dPAWN4)

def dpieces(endb):
    """
    return tuple of differences in piece counts
    """
    import chess
    dPAWN = len(endb.pieces(chess.PAWN,chess.WHITE)) - len(endb.pieces(chess.PAWN,chess.BLACK))
    dKNIGHT = len(endb.pieces(chess.KNIGHT,chess.WHITE)) - len(endb.pieces(chess.KNIGHT,chess.BLACK))
    dBISHOP = len(endb.pieces(chess.BISHOP,chess.WHITE)) - len(endb.pieces(chess.BISHOP,chess.BLACK))
    dROOK = len(endb.pieces(chess.ROOK,chess.WHITE)) - len(endb.pieces(chess.ROOK,chess.BLACK))
    dQUEEN = len(endb.pieces(chess.QUEEN,chess.WHITE)) - len(endb.pieces(chess.QUEEN,chess.BLACK))
    pp_count = passed_pawn_count(endb)
    pawn_rank = dpawn_rank(endb)
    return (dPAWN,dKNIGHT,dBISHOP,dROOK,dQUEEN,*pp_count,*pawn_rank)

def pgn_gen(pgn):
    from math import floor
    import chess.pgn
    from re import sub,compile
    rpat = compile("https?://lichess.org/")
    nmove = 10
    suffixes = ['dpawn','dknight','dbishop','drook','dqueen',
            'pp234','pp5','pp6','pp7',
            'dpawnr2','dpawnr3','dpawnr4']
    prefixes = ['rr','t1','t2','t3']
    # have to be careful about the ordering of that double zip...
    yield ('site','datetime','time_control','termination','outcome','nply',
            *[f"move{i}" for i in range(1,nmove+1)],
            'moves',
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
            movel = ''
            # could also be 'Time forfeit', 'Abandoned'
            moves = ['' for x in range(nmove)]
            wdiff = float('nan')
            bdiff = float('nan')
            nply = float('nan')
            rr_ply = 0
            t1_ply = 0
            t2_ply = 0
            t3_ply = 0
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
                movel,
                white,black,welo,belo,wdiff,bdiff,
                rr_ply,t1_ply,t2_ply,t3_ply,
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
        for result in pgn_gen(pgn):
            spamwriter.writerow(result)
        csvfile.close()

#for vim modeline: (do not edit)
# vim:ts=4:sw=4:sts=4:tw=79:sta:et:ai:nu:fdm=indent:syn=python:ft=python:tag=.py_tags;:cin:fo=croql
