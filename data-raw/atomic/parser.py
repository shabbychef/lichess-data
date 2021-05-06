#! /usr/bin/env python
# coding: utf-8
#
"""atomic pgn to csv conversion

Usage:
  parser.py INPGN OUTCSV

"""

from docopt import docopt

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
    return (dPAWN,dKNIGHT,dBISHOP,dROOK,dQUEEN,*pp_count)

def pgn_gen(pgn):
    import chess.pgn
    from re import sub,compile
    rpat = compile("https?://lichess.org/")
    nmove = 10
    yield ('site','datetime','termination','outcome','nply',
            *[f"move{i}" for i in range(1,nmove+1)],
            'moves',
            'white','black',
            'white_elo','black_elo','white_elo_diff','black_elo_diff',
            'l1_dpawn','l1_dknight','l1_dbishop','l1_drook','l1_dqueen','l1_pp234','l1_pp5','l1_pp6','l1_pp7',
            'l2_dpawn','l2_dknight','l2_dbishop','l2_drook','l2_dqueen','l2_pp234','l2_pp5','l2_pp6','l2_pp7',
            'l4_dpawn','l4_dknight','l4_dbishop','l4_drook','l4_dqueen','l4_pp234','l4_pp5','l4_pp6','l4_pp7',
            'l8_dpawn','l8_dknight','l8_dbishop','l8_drook','l8_dqueen','l8_pp234','l8_pp5','l8_pp6','l8_pp7')
    # empty
    mt_dp = tuple(float('nan') for i in range(9))
    while (pgn):
        gam = chess.pgn.read_game(pgn)
        try:
            rhed = gam.headers
        except:
            # cannot do anything without the headers? fake them!
            #rhed = {'Termination':'ERROR','Result':'--','Site':"https://lichess.org/"}
            # I believe you get here when you reach end of file. return then
            break
        term = rhed['Termination']
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
            except:
                d_l1 = mt_dp
            try:
                lmov = endb.pop()
                d_l2 = dpieces(endb)
            except:
                d_l2 = mt_dp
            try:
                lmov = endb.pop()
                lmov = endb.pop()
                d_l4 = dpieces(endb)
            except:
                d_l4 = mt_dp
            try:
                lmov = endb.pop()
                lmov = endb.pop()
                lmov = endb.pop()
                lmov = endb.pop()
                d_l8 = dpieces(endb)
            except:
                d_l8 = mt_dp
        else:
            movel = ''
            # could also be 'Time forfeit', 'Abandoned'
            moves = ['' for x in range(nmove)]
            wdiff = float('nan')
            bdiff = float('nan')
            nply = float('nan')
            d_l1 = mt_dp
            d_l2 = mt_dp
            d_l4 = mt_dp
            d_l8 = mt_dp
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
        # an ID for the game
        site = sub(rpat,'',rhed['Site']) 
        yield (site,datetime,term,outcome,nply,
                *moves,
                movel,
                white,black,welo,belo,wdiff,bdiff,
                *d_l1,*d_l2,*d_l4,*d_l8)
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
