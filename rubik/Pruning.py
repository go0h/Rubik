# from rubik.Symmetries import SYM_CUBIES, INV_IDX
# import rubik.CubieCube as cc
# from rubik.Utils import MOVES
#
#
# def get_fs_twist_depth3(table, index):
#     """Возвращает количество ходов по модулю 3 для решения фазы 1 для куба с индексом index"""
#     y = table[index // 16]
#     y >>= (index % 16) * 2
#     return y & 3
#
#
# def set_fs_twist_depth3(table, ix, value):
#     shift = (ix % 16) * 2
#     base = ix >> 4
#     table[base] &= ~(3 << shift) & 0xffffffff
#     table[base] |= value << shift
#
#
# def create_pruning1_table(fs_classidx, fs_rep, fs_sym, conj_twist):
#
#     total = 64430 * 2187  # 140.689.710
#     fs_twist_depth = [0xffffffff for _ in range(total // 16 + 1)]
#
#     # #################### создаем таблицу ссиметрий fs_class  ###############################
#     cub = cc.CubieCube()
#     fs_sym_t = [0 for _ in range(64430)]
#     for i in range(64430):
#
#         rep = fs_rep[i]
#         cub.set_ud_slice_coord(rep // 2048)
#         cub.set_edges_flip(rep % 2048)
#
#         for s in range(16):
#             ss = cc.CubieCube(SYM_CUBIES[s].corners, SYM_CUBIES[s].edges)
#             ss.edge_multiply(cub)  # s*cc
#             ss.edge_multiply(SYM_CUBIES[INV_IDX[s]])  # s*cc*s^-1
#             if ss.get_ud_slice_coord() == rep // 2048 and ss.get_edges_flip() == rep % 2048:
#                 fs_sym_t[i] |= 1 << s
#     # ##################################################################################################################
#
#     set_fs_twist_depth3(fs_twist_depth, 0, 0)
#     done = 1
#     depth = 0
#     back_search = False
#     while done != total:
#         depth3 = depth % 3
#         if depth == 9:
#             back_search = True
#
#         idx = 0
#         for fs_classidx_ in range(64430):
#             twist = 0
#             while twist < 2187:
#
#                 # ########## если таблице не заполнены записи, ускряем ################################
#                 if not back_search and idx % 16 == 0 and fs_twist_depth[idx // 16] == 0xffffffff \
#                         and twist < 2187 - 16:
#                     twist += 16
#                     idx += 16
#                     continue
#                 ####################################################################################################
#
#                 if back_search:
#                     match = (get_fs_twist_depth3(fs_twist_depth, idx) == 3)
#                 else:
#                     match = (get_fs_twist_depth3(fs_twist_depth, idx) == depth3)
#
#                 if match:
#                     fs = fs_rep[fs_classidx_]
#                     flip = fs % 2048     # defs.N_FLIP = 2048
#                     slice_ = fs >> 11    # defs.N_FLIP
#
#                     cub = cc.CubieCube()
#                     cub.set_corners_twist(twist)
#                     cub.set_edges_flip(flip)
#                     cub.set_ud_slice_coord(slice_)
#
#                     for move in MOVES:
#                         cub.move(move)
#                         twist1 = cub.get_corners_twist()
#                         flip1 = cub.get_edges_flip()
#                         slice1 = cub.get_ud_slice_coord() // 24  # defs.N_PERM_4 = 24, 18*24 = 432
#
#                         # twist1 = mv.twist_move[18 * twist + move]
#                         # flip1 = mv.flip_move[18 * flip + move]
#                         # slice1 = mv.slice_sorted_move[432 * slice_ + move] // 24  # defs.N_PERM_4 = 24, 18*24 = 432
#
#                         fs1 = (slice1 << 11) + flip1
#                         fs1_classidx = fs_classidx[fs1]
#                         fs1_sym = fs_sym[fs1]
#                         twist1 = conj_twist[(twist1 << 4) + fs1_sym]
#                         idx1 = 2187 * fs1_classidx + twist1  # defs.N_TWIST = 2187
#                         if not back_search:
#                             if get_fs_twist_depth3(fs_twist_depth, idx1) == 3:  # entry not yet filled
#                                 set_fs_twist_depth3(fs_twist_depth, idx1, (depth + 1) % 3)
#                                 done += 1
#                                 # ####symmetric position has eventually more than one representation ###############
#                                 sym = fs_sym_t[fs1_classidx]
#                                 if sym != 1:
#                                     for j in range(1, 16):
#                                         sym >>= 1
#                                         if sym % 2 == 1:
#                                             twist2 = conj_twist[(twist1 << 4) + j]
#                                             # fs2_classidx = fs1_classidx due to symmetry
#                                             idx2 = 2187 * fs1_classidx + twist2
#                                             if get_fs_twist_depth3(fs_twist_depth, idx2) == 3:
#                                                 set_fs_twist_depth3(fs_twist_depth, idx2, (depth + 1) % 3)
#                                                 done += 1
#                                 ####################################################################################
#
#                         else:  # backwards search
#                             if get_fs_twist_depth3(fs_twist_depth, idx1) == depth3:
#                                 set_fs_twist_depth3(fs_twist_depth, idx, (depth + 1) % 3)
#                                 done += 1
#                                 break
#                 twist += 1
#                 idx += 1  # idx = defs.N_TWIST * fs_class + twist
#
#         depth += 1
#
#
