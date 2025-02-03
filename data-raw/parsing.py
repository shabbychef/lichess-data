#! /usr/bin/env python
# coding: utf-8
#
"""
Common tools for chess pgn to csv conversion.


"""

import chess
from chess import variant, pgn
from re import sub,compile

from docopt import docopt
from functools import reduce
from math import floor

def fibu_str(astring:str,A:float=0.61803399,m:int=2**31):
    """
    returns a Fibonacci hash of a string, which is a pseudorandom number
    derived from the inpt string.
    this is useful for consistently generating a random number associated with a 
    given game URL.
    """
    lowy = ord('0')
    fbits = [(ord(c)-lowy)*A for c in astring]
    return (reduce(lambda a, b: (a + m * b) % 1,fbits))

def dpieces(endb, include_king:bool=False):
    """
    Returns a tuple of differences in piece counts at a given snapshot in a game.
    """
    dPAWN = (endb.occupied_co[chess.WHITE] & endb.pawns).bit_count() - (endb.occupied_co[chess.BLACK] & endb.pawns).bit_count()
    dKNIGHT = (endb.occupied_co[chess.WHITE] & endb.knights).bit_count() - (endb.occupied_co[chess.BLACK] & endb.knights).bit_count()
    dBISHOP = (endb.occupied_co[chess.WHITE] & endb.bishops).bit_count() - (endb.occupied_co[chess.BLACK] & endb.bishops).bit_count()
    dROOK = (endb.occupied_co[chess.WHITE] & endb.rooks).bit_count() - (endb.occupied_co[chess.BLACK] & endb.rooks).bit_count()
    dQUEEN = (endb.occupied_co[chess.WHITE] & endb.queens).bit_count() - (endb.occupied_co[chess.BLACK] & endb.queens).bit_count()
    if include_king:
        dKING = (endb.occupied_co[chess.WHITE] & endb.kings).bit_count() - (endb.occupied_co[chess.BLACK] & endb.kings).bit_count()
        return (dPAWN,dKNIGHT,dBISHOP,dROOK,dQUEEN,dKING)
    else:
        return (dPAWN,dKNIGHT,dBISHOP,dROOK,dQUEEN)


def seekto(game,at_ply:int):
    """
    Take a Game object, then play to just after at_ply, returning the board at that point.
    """
    myb = game.end().board()
    ms = myb.move_stack
    # no easy way to do this.
    subs = ms[0:at_ply]
    # is this how to get a board at the beginning?
    newb = game.board().copy()
    for move in subs:
        newb.push(move)
    return newb


def pos_seek(game,rando,min_rat=0,max_rat=1,min_ply=2,max_ply=None):
    """
    Like seekto, seek to a (random) position.

    let n be the number of ply in the game. 
    let l = max(min_rat*n,min_ply,0)
    let u = min(max_rat*n,max_ply,n+1)
    
    computes floor(l + r * (u-l)) and seeks to that position, returning a board.

    if max_ply is given as None, it is ignored. 
    you can set max_rat > 1 to possibly get
    the ending position (which seems uninteresting to me.)
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
    return (seekto(game, at_ply), at_ply)

#for vim modeline: (do not edit)
# vim:ts=4:sw=4:sts=4:tw=79:sta:et:ai:nu:fdm=indent:syn=python:ft=python:tag=.py_tags;:cin:fo=croql
