#! /usr/bin/env python
# coding: utf-8
#
"""antichess pgn to csv conversion

we only care about move sequence, tbh

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
    pp_count = passed_pawn_count(endb)
    return (dPAWN,dKNIGHT,dBISHOP,dROOK,dQUEEN,*pp_count)

def pgn_gen(pgn):
    import chess.pgn
    from re import sub,compile
    rpat = compile("https?://lichess.org/")
    nmove = 10
    yield ('site','datetime','termination','outcome','nply',
            *[f"move{i}" for i in range(1,nmove+1)],
            #'moves',
            'white','black',
            'white_elo','black_elo','white_elo_diff','black_elo_diff')
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
        else:
            movel = ''
            # could also be 'Time forfeit', 'Abandoned'
            moves = ['' for x in range(nmove)]
            wdiff = float('nan')
            bdiff = float('nan')
            nply = float('nan')
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
                #movel,
                white,black,welo,belo,wdiff,bdiff)
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
