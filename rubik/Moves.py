from rubik.CubieCube import CubieCube
from rubik.Utils import MOVES, INV_MOVE


def get_move_twist():
    move_twist = [[0 for _ in range(18)] for _ in range(2187)]
    cub = CubieCube()
    for twist in range(2187):
        cub.set_corners_twist(twist)
        for move in MOVES:
            cub.move(move)
            move_twist[twist][move] = cub.get_corners_twist()
            cub.move(INV_MOVE[move])
    return move_twist


def get_move_flip():
    move_flip = [[0 for _ in range(18)] for _ in range(2048)]
    cub = CubieCube()
    for flip in range(2048):
        cub.set_edges_flip(flip)
        for move in MOVES:
            cub.move(move)
            move_flip[flip][move] = cub.get_edges_flip()
            cub.move(INV_MOVE[move])
    return move_flip


def get_move_slice_sorted():
    move_slice = [[0 for _ in range(18)] for _ in range(11880)]
    cub = CubieCube()
    for slice in range(11880):
        cub.set_ud_slice_coord(slice)
        for move in MOVES:
            cub.move(move)
            move_slice[slice][move] = cub.get_ud_slice_sorted()
            cub.move(INV_MOVE[move])
    return move_slice


def get_move_ud_edges():
    move_ud_edges = [[0 for _ in range(18)] for _ in range(40320)]
    cub = CubieCube()
    for ud_edge in range(40320):
        cub.set_ud_edges(ud_edge)
        for move in MOVES:
            cub.move(move)
            move_ud_edges[ud_edge][move] = cub.get_ud_edges()
            cub.move(INV_MOVE[move])
    return move_ud_edges


def get_move_corners():
    move_corners = [[0 for _ in range(18)] for _ in range(40320)]
    cub = CubieCube()
    for corner in range(40320):
        cub.set_corners(corner)
        for move in MOVES:
            cub.move(move)
            move_corners[corner][move] = cub.get_corners()
            cub.move(INV_MOVE[move])
    return move_corners
