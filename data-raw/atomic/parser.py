#! /usr/bin/env python
# coding: utf-8
#
"""atomic pgn to csv conversion

Usage:
  parser.py INPGN OUTCSV

"""

from docopt import docopt


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
    return (dPAWN,dKNIGHT,dBISHOP,dROOK,dQUEEN)

def pgn_gen(pgn):
    import chess.pgn
    from re import sub,compile
    rpat = compile("https?://lichess.org/")
    yield ('site','datetime','termination','outcome','nply',
            'move1','move2','move3','move4','move5','move6','move7','move8','move9','move10',
            'moves',
            'white','black',
            'white_elo','black_elo','white_elo_diff','black_elo_diff',
            'l1_dpawn','l1_dknight','l1_dbishop','l1_drook','l1_dqueen',
            'l2_dpawn','l2_dknight','l2_dbishop','l2_drook','l2_dqueen',
            'l4_dpawn','l4_dknight','l4_dbishop','l4_drook','l4_dqueen',
            'l8_dpawn','l8_dknight','l8_dbishop','l8_drook','l8_dqueen')
    # empty
    mt_dp = (float('nan'), float('nan'), float('nan'), float('nan'), float('nan'))
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
            if (len(moves) > 10):
                moves = moves[0:10]
            else:
                for iii in range(len(moves),10):
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
            # could also be 'Time forfeit', 'Abandonded'
            moves = ['','','','','','','','','','']
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
