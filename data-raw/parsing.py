#! /usr/bin/env python
# coding: utf-8
#
"""
Common tools for chess pgn to csv conversion.


"""

import chess
from chess import variant, pgn
from re import sub, compile
from math import floor
from functools import reduce


# these are all abandoned
def fibonacci_hash(x, A=0.6180339887, m=2 ** 31):
    """Fibonacci hash"""
    from math import floor

    return floor(m * ((x * A) % 1))


def fibonacci_strhash(astring, A=0.6180339887, m=2 ** 31):
    from math import floor

    lowy = ord("0")
    return floor(m * (sum([(ord(c) - lowy) * A for c in astring]) % 1))


def fibu_str(astring: str, A: float = 0.61803399, m: int = 2 ** 31):
    """
    returns a Fibonacci hash of a string, which is a pseudorandom number
    derived from the inpt string.
    this is useful for consistently generating a random number associated with a
    given game URL.
    """
    lowy = ord("0")
    fbits = [(ord(c) - lowy) * A for c in astring]
    return reduce(lambda a, b: (a + m * b) % 1, fbits)


def _dpieces_slow(endb):
    """
    This turns out to be quite slower than the other version...
    return tuple of differences in piece counts
    """
    dPAWN = len(endb.pieces(chess.PAWN, chess.WHITE)) - len(
        endb.pieces(chess.PAWN, chess.BLACK)
    )
    dKNIGHT = len(endb.pieces(chess.KNIGHT, chess.WHITE)) - len(
        endb.pieces(chess.KNIGHT, chess.BLACK)
    )
    dBISHOP = len(endb.pieces(chess.BISHOP, chess.WHITE)) - len(
        endb.pieces(chess.BISHOP, chess.BLACK)
    )
    dROOK = len(endb.pieces(chess.ROOK, chess.WHITE)) - len(
        endb.pieces(chess.ROOK, chess.BLACK)
    )
    dQUEEN = len(endb.pieces(chess.QUEEN, chess.WHITE)) - len(
        endb.pieces(chess.QUEEN, chess.BLACK)
    )
    dKING = len(endb.pieces(chess.KING, chess.WHITE)) - len(
        endb.pieces(chess.KING, chess.BLACK)
    )
    return (dPAWN, dKNIGHT, dBISHOP, dROOK, dQUEEN, dKING)


def dpieces(endb, include_king: bool = False):
    """
    Returns a tuple of differences in piece counts at a given snapshot in a game.
    """
    dPAWN = (endb.occupied_co[chess.WHITE] & endb.pawns).bit_count() - (
        endb.occupied_co[chess.BLACK] & endb.pawns
    ).bit_count()
    dKNIGHT = (endb.occupied_co[chess.WHITE] & endb.knights).bit_count() - (
        endb.occupied_co[chess.BLACK] & endb.knights
    ).bit_count()
    dBISHOP = (endb.occupied_co[chess.WHITE] & endb.bishops).bit_count() - (
        endb.occupied_co[chess.BLACK] & endb.bishops
    ).bit_count()
    dROOK = (endb.occupied_co[chess.WHITE] & endb.rooks).bit_count() - (
        endb.occupied_co[chess.BLACK] & endb.rooks
    ).bit_count()
    dQUEEN = (endb.occupied_co[chess.WHITE] & endb.queens).bit_count() - (
        endb.occupied_co[chess.BLACK] & endb.queens
    ).bit_count()
    if include_king:
        dKING = (endb.occupied_co[chess.WHITE] & endb.kings).bit_count() - (
            endb.occupied_co[chess.BLACK] & endb.kings
        ).bit_count()
        return (dPAWN, dKNIGHT, dBISHOP, dROOK, dQUEEN, dKING)
    else:
        return (dPAWN, dKNIGHT, dBISHOP, dROOK, dQUEEN)


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
    PASSER_WHITE_R2 = [
        (chess.BB_A2, FRONT_A2),
        (chess.BB_B2, FRONT_B2),
        (chess.BB_C2, FRONT_C2),
        (chess.BB_D2, FRONT_D2),
        (chess.BB_E2, FRONT_E2),
        (chess.BB_F2, FRONT_F2),
        (chess.BB_G2, FRONT_G2),
        (chess.BB_H2, FRONT_H2),
    ]
    PASSER_WHITE_R3 = [
        (chess.BB_A3, FRONT_A3),
        (chess.BB_B3, FRONT_B3),
        (chess.BB_C3, FRONT_C3),
        (chess.BB_D3, FRONT_D3),
        (chess.BB_E3, FRONT_E3),
        (chess.BB_F3, FRONT_F3),
        (chess.BB_G3, FRONT_G3),
        (chess.BB_H3, FRONT_H3),
    ]
    PASSER_WHITE_R4 = [
        (chess.BB_A4, FRONT_A4),
        (chess.BB_B4, FRONT_B4),
        (chess.BB_C4, FRONT_C4),
        (chess.BB_D4, FRONT_D4),
        (chess.BB_E4, FRONT_E4),
        (chess.BB_F4, FRONT_F4),
        (chess.BB_G4, FRONT_G4),
        (chess.BB_H4, FRONT_H4),
    ]
    PASSER_WHITE_R5 = [
        (chess.BB_A5, FRONT_A5),
        (chess.BB_B5, FRONT_B5),
        (chess.BB_C5, FRONT_C5),
        (chess.BB_D5, FRONT_D5),
        (chess.BB_E5, FRONT_E5),
        (chess.BB_F5, FRONT_F5),
        (chess.BB_G5, FRONT_G5),
        (chess.BB_H5, FRONT_H5),
    ]
    PASSER_WHITE_R6 = [
        (chess.BB_A6, FRONT_A6),
        (chess.BB_B6, FRONT_B6),
        (chess.BB_C6, FRONT_C6),
        (chess.BB_D6, FRONT_D6),
        (chess.BB_E6, FRONT_E6),
        (chess.BB_F6, FRONT_F6),
        (chess.BB_G6, FRONT_G6),
        (chess.BB_H6, FRONT_H6),
    ]
    PASSER_WHITE_R234 = [*PASSER_WHITE_R2, *PASSER_WHITE_R3, *PASSER_WHITE_R4]
    #
    PASSER_BLACK_R7 = [
        (chess.BB_A7, BACK_A7),
        (chess.BB_B7, BACK_B7),
        (chess.BB_C7, BACK_C7),
        (chess.BB_D7, BACK_D7),
        (chess.BB_E7, BACK_E7),
        (chess.BB_F7, BACK_F7),
        (chess.BB_G7, BACK_G7),
        (chess.BB_H7, BACK_H7),
    ]
    PASSER_BLACK_R6 = [
        (chess.BB_A6, BACK_A6),
        (chess.BB_B6, BACK_B6),
        (chess.BB_C6, BACK_C6),
        (chess.BB_D6, BACK_D6),
        (chess.BB_E6, BACK_E6),
        (chess.BB_F6, BACK_F6),
        (chess.BB_G6, BACK_G6),
        (chess.BB_H6, BACK_H6),
    ]
    PASSER_BLACK_R5 = [
        (chess.BB_A5, BACK_A5),
        (chess.BB_B5, BACK_B5),
        (chess.BB_C5, BACK_C5),
        (chess.BB_D5, BACK_D5),
        (chess.BB_E5, BACK_E5),
        (chess.BB_F5, BACK_F5),
        (chess.BB_G5, BACK_G5),
        (chess.BB_H5, BACK_H5),
    ]
    PASSER_BLACK_R4 = [
        (chess.BB_A4, BACK_A4),
        (chess.BB_B4, BACK_B4),
        (chess.BB_C4, BACK_C4),
        (chess.BB_D4, BACK_D4),
        (chess.BB_E4, BACK_E4),
        (chess.BB_F4, BACK_F4),
        (chess.BB_G4, BACK_G4),
        (chess.BB_H4, BACK_H4),
    ]
    PASSER_BLACK_R3 = [
        (chess.BB_A3, BACK_A3),
        (chess.BB_B3, BACK_B3),
        (chess.BB_C3, BACK_C3),
        (chess.BB_D3, BACK_D3),
        (chess.BB_E3, BACK_E3),
        (chess.BB_F3, BACK_F3),
        (chess.BB_G3, BACK_G3),
        (chess.BB_H3, BACK_H3),
    ]
    PASSER_BLACK_R765 = [*PASSER_BLACK_R7, *PASSER_BLACK_R6, *PASSER_BLACK_R5]
    #
    WP = board.pieces(chess.PAWN, chess.WHITE)
    BP = board.pieces(chess.PAWN, chess.BLACK)
    pp_234 = sum(
        [max(0, len(WP & x[0]) - len(BP & x[1])) for x in PASSER_WHITE_R234]
    ) - sum([max(0, len(BP & x[0]) - len(WP & x[1])) for x in PASSER_BLACK_R765])
    pp_5 = sum(
        [max(0, len(WP & x[0]) - len(BP & x[1])) for x in PASSER_WHITE_R5]
    ) - sum([max(0, len(BP & x[0]) - len(WP & x[1])) for x in PASSER_BLACK_R4])
    pp_6 = sum(
        [max(0, len(WP & x[0]) - len(BP & x[1])) for x in PASSER_WHITE_R6]
    ) - sum([max(0, len(BP & x[0]) - len(WP & x[1])) for x in PASSER_BLACK_R3])
    pp_7 = len(WP & chess.BB_RANK_7) - len(BP & chess.BB_RANK_2)
    return (pp_234, pp_5, pp_6, pp_7)


def dpawn_rank(board):
    """
    pawn rank count difference of pawn rank
    """
    import chess

    WP = board.pieces(chess.PAWN, chess.WHITE)
    BP = board.pieces(chess.PAWN, chess.BLACK)
    dPAWN2 = len(WP & chess.BB_RANK_2) - len(BP & chess.BB_RANK_7)
    dPAWN3 = len(WP & chess.BB_RANK_3) - len(BP & chess.BB_RANK_6)
    dPAWN4 = len(WP & chess.BB_RANK_4) - len(BP & chess.BB_RANK_5)
    return (dPAWN2, dPAWN3, dPAWN4)


def static_deltas(
    endb,
    include_king: bool = False,
    include_passed_pawn: bool = False,
    include_pawn_rank: bool = False,
):
    dp = dpieces(endb, include_king=include_king)
    if include_passed_pawn:
        pp_count = passed_pawn_count(endb)
        dp = (*dp, *pp_count)
    if include_pawn_rank:
        pawn_rank = dpawn_rank(endb)
        dp = (*dp, *pawn_rank)
    return dp


def seekto(game, at_ply: int, ncheck: int = 1):
    """
    Take a Game object, then play to just after at_ply, returning the board at that point.
    Also returns ncheck different checks forward for captures.
    If the game ends before that lookahead, we return false for whether that is a capture.
    """
    myb = game.end().board()
    ms = myb.move_stack
    # no easy way to do this.
    subs = ms[0:at_ply]
    # is this how to get a board at the beginning?
    newb = game.board().copy()
    for move in subs:
        newb.push(move)
    cap_stack = []
    if ncheck > 0:
        tail_moves = ms[at_ply:]
        copb = newb.copy()
        for idx in range(ncheck):
            if idx >= len(tail_moves):
                next_take = False
            else:
                next_take = copb.is_capture(tail_moves[idx])
                if idx < ncheck - 1:
                    copb.push(tail_moves[idx])
            cap_stack.append(next_take)
    return (newb, *cap_stack)


def pos_seek(game, rando, min_rat=0, max_rat=1, min_ply=2, max_ply=None, **kwargs):
    """
    Like seekto, seek to a (random) position.

    let n be the number of ply in the game.
    let l = max(min_rat*n,min_ply,0)
    let u = min(max_rat*n,max_ply,n+1)

    computes floor(l + r * (u-l)) and seeks to that position, returning a board.

    if max_ply is given as None, it is ignored.
    you can set max_rat > 1 to possibly get
    the ending position (which seems uninteresting to me.)

    returns:
        the ply number
        the board
        whether the next move would take a piece.
    """
    myb = game.end().board()
    ms = myb.move_stack
    nnn = len(ms)
    lll = max(max(nnn * min_rat, min_ply), 0)
    uuu = min(nnn * max_rat, nnn + 1)
    if max_ply is not None:
        uuu = min(uuu, max_ply)
    # just in case
    uuu = max(uuu, lll)
    at_ply = floor(lll + rando * (uuu - lll))
    return (at_ply, *seekto(game, at_ply, **kwargs))


def pgn_gen(
    pgn,
    include_movel: bool = False,
    include_king: bool = True,
    include_passed_pawn: bool = False,
    include_pawn_rank: bool = False,
):
    """
    Params
        include_movel (bool): whether to return a string of the moves joined
            by ':'.
        include_king (bool): whether to include metrics on the king.
            should probably only be True for antichess where the king
            does not have royal powers.
    """
    stat_kwargs = {
        "include_king": include_king,
        "include_passed_pawn": include_passed_pawn,
        "include_pawn_rank": include_pawn_rank,
    }
    import chess.pgn

    rpat = compile("https?://lichess.org/")
    nmove = 10
    d_piece_suffixes = [
        "dpawn",
        "dknight",
        "dbishop",
        "drook",
        "dqueen",
    ]
    if include_king:
        d_piece_suffixes.append("dking")
    if include_passed_pawn:
        d_piece_suffixes.extend(
            [
                "pp234",
                "pp5",
                "pp6",
                "pp7",
            ]
        )
    if include_pawn_rank:
        d_piece_suffixes.extend(
            [
                "dpawnr2",
                "dpawnr3",
                "dpawnr4",
            ]
        )
    suffixes = [*d_piece_suffixes, "next_take", "nextnext_take"]
    prefixes = ["l1", "rr", "t1", "t2", "t3"]
    # have to be careful about the ordering of that double zip...
    moves_colnames = ["moves"] if include_movel else []
    yield (
        "site",
        "datetime",
        "time_control",
        "termination",
        "outcome",
        "nply",
        *[f"move{i}" for i in range(1, nmove + 1)],
        *moves_colnames,
        "white",
        "black",
        "white_elo",
        "black_elo",
        "white_elo_diff",
        "black_elo_diff",
        *[f"{bit}_ply" for bit in ["rr", "t1", "t2", "t3"]],
        *[f"{pre}_{suf}" for pre in prefixes for suf in suffixes],
    )
    # empty
    mt_dp = tuple(float("nan") for i in range(len(d_piece_suffixes)))
    while pgn:
        try:
            gam = chess.pgn.read_game(pgn)
        except Exception as err:
            print(f"{err=}")
            continue
        try:
            rhed = gam.headers
        except:
            # I believe you get here when you reach end of file. break and return then
            break
        term = rhed["Termination"]
        tc = rhed["TimeControl"]
        # an ID for the game
        site = sub(rpat, "", rhed["Site"])
        # now use this to seek to random, first 1/3, middle 1/3, late 1/3 positions.
        # we have Normal, Time forfeit, Abandoned
        if term != "Abandoned":
            try:
                ending = gam.end()
                endb = ending.board()
                moves = [str(x) for x in endb.move_stack]
            except:
                moves = []
            nply = len(moves)
            if include_movel:
                movel = ":".join(moves)
            else:
                movel = ""
            if len(moves) > nmove:
                moves = moves[0:nmove]
            else:
                moves.extend([""] * (nmove - len(moves)))
            try:
                wdiff = int(rhed["WhiteRatingDiff"])
                bdiff = int(rhed["BlackRatingDiff"])
            except Exception as err:
                print(f"no ratings? {err=}")
                wdiff = float("nan")
                bdiff = float("nan")
            try:
                lmov = endb.pop()
                d_l1 = static_deltas(endb, **stat_kwargs)
                l1_take = endb.is_capture(lmov)
                l1_taketake = False
            except:
                d_l1 = mt_dp
                l1_take = False
                l1_taketake = False
            # in atomic I had originally pulled l2, l4 and l8,
            # but those are not as useful. If you want to add them
            # use code like this:
            """
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
            """
            # pseudo random locations
            try:
                randbit = fibu_str(site)
                (rr_ply, rr_board, rr_take, rr_taketake) = pos_seek(
                    gam, randbit, min_rat=0, max_rat=1, min_ply=2, ncheck=2
                )
                d_rr = static_deltas(rr_board, **stat_kwargs)
                # squeeze more randomness out of randbit? seems dangerous..
                m = 2 ** 31
                rbit_t1 = ((floor(m * randbit) << 4) / m) % 1
                (t1_ply, t1_board, t1_take, t1_taketake) = pos_seek(
                    gam, rbit_t1, min_rat=0, max_rat=0.33333, min_ply=2, ncheck=2
                )
                d_t1 = static_deltas(t1_board, **stat_kwargs)
                rbit_t2 = ((floor(m * randbit) << 8) / m) % 1
                (t2_ply, t2_board, t2_take, t2_taketake) = pos_seek(
                    gam, rbit_t2, min_rat=0.33333, max_rat=0.66667, min_ply=2, ncheck=2
                )
                d_t2 = static_deltas(t2_board, **stat_kwargs)
                rbit_t3 = ((floor(m * randbit) << 12) / m) % 1
                (t3_ply, t3_board, t3_take, t3_taketake) = pos_seek(
                    gam, rbit_t3, min_rat=0.66667, max_rat=1.00000, min_ply=2, ncheck=2
                )
                d_t3 = static_deltas(t3_board, **stat_kwargs)
            except Exception as err:
                print(f"{err=}")
                continue
        else:
            movel = ""
            # could also be 'Time forfeit', 'Abandoned'
            moves = [""] * nmove
            wdiff = bdiff = float("nan")
            nply = float("nan")
            rr_ply = t1_ply = t2_ply = t3_ply = 0
            d_l1 = d_rr = d_t1 = d_t2 = d_t3 = mt_dp
            rr_take = l1_take = t1_take = t2_take = t3_take = False
            rr_taketake = l1_taketake = t1_taketake = t2_taketake = t3_taketake = False
        # outcome from white's pov, as a number:
        if rhed["Result"] == "1-0":
            outcome = 1.0
        elif rhed["Result"] == "0-1":
            outcome = 0.0
        elif rhed["Result"] == "1/2-1/2":
            outcome = 0.5
        else:
            outcome = float("nan")
        # who is playing
        try:
            white = rhed["White"]
            black = rhed["Black"]
        except:
            white = ""
            black = ""
        # whie and black elo
        try:
            welo = int(rhed["WhiteElo"])
        except:
            welo = float("nan")
        try:
            belo = int(rhed["BlackElo"])
        except:
            belo = float("nan")

        try:
            dat = sub("\.", "-", rhed["UTCDate"])
            datetime = f"{dat}T{rhed['UTCTime']}Z"
        except:
            datetime = ""
        movestr_values = [movel] if include_movel else []
        yield (
            site,
            datetime,
            tc,
            term,
            outcome,
            nply,
            *moves,
            *movestr_values,
            white,
            black,
            welo,
            belo,
            wdiff,
            bdiff,
            rr_ply,
            t1_ply,
            t2_ply,
            t3_ply,
            *d_l1,
            l1_take,
            l1_taketake,
            *d_rr,
            rr_take,
            rr_taketake,
            *d_t1,
            t1_take,
            t1_taketake,
            *d_t2,
            t2_take,
            t2_taketake,
            *d_t3,
            t3_take,
            t3_taketake,
        )
    pgn.close()
    return


# for vim modeline: (do not edit)
# vim:ts=4:sw=4:sts=4:tw=79:sta:et:ai:nu:fdm=indent:syn=python:ft=python:tag=.py_tags;:cin:fo=croql
