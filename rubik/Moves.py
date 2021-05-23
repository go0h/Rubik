# from rubik.CubieCube import CubieCube
# from rubik.Utils import MOVES, INV_MOVE
#
#
# def get_move_twist():
#     move_twist = [[0 for _ in range(18)] for _ in range(2187)]
#     cub = CubieCube()
#     for twist in range(2187):
#         cub.set_corners_twist(twist)
#
#         for move in MOVES:
#             cub.move(move)
#             move_twist[twist][move] = cub.get_corners_twist()
#             cub.move(INV_MOVE[move])
#     return move_twist
