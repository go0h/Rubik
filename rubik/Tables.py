import os
import sys
import numpy as np
import rubik.Symmetries as sym
import rubik.Moves as m
import rubik.Pruning as p
from datetime import datetime


def get_table(table_name, create_table_func, type_=np.int32):

    print(f"Load table {table_name}", end=" ")
    dir = os.getcwd() + "/resources/"
    if os.getcwd().endswith("test"):
        dir = dir.replace("/test", "")
    table_name = dir + table_name
    t1 = datetime.now()

    if os.path.exists(table_name):
        try:
            with open(table_name, "r") as file:
                table = np.loadtxt(file, dtype=type_)
        except IOError:
            print(f"File {table_name} not accessible")
            sys.exit(-1)
    else:
        table = np.array(create_table_func(), dtype=type_)
        try:
            with open(table_name, "w") as file:
                np.savetxt(file, table, fmt="%d")
        except IOError:
            print(f"File {table_name} not accessible")
            sys.exit(-1)
    print(datetime.now() - t1)
    return table


#######################################################################################################################


# http://kociemba.org/math/symcord.htm

# загружаем таблицу ориентаций углов для Фазы 1
# 3^7 = 2187 возможных ориентаций углов в Фазе 1
# 16 - количество симметрий подгруппы Dh4 - http://kociemba.org/math/d4h.htm
# conj_twist[2187][16]
conj_twist = get_table("conj_twist", sym.create_conj_twist)

# загружаем таблицу перестановок верхних и нижних ребер для Фазы 2 (UR - DB)
# 8! = 40320 возможных перестановок 8 ребер в фазе 1
# 16 - количество симметрий подгруппы Dh4 - http://kociemba.org/math/d4h.htm
# conj_ud_edges[40320][16]
conj_ud_edges = get_table("conj_ud_edges", sym.create_conj_ud_edges)


#######################################################################################################################


# http://kociemba.org/math/twophase.htm
# загружаем таблицу перестановок + ориентаций UD-среза для фазы 1, c их симметриями
# 2^11 = 2048 возможных ориентаций 12 ребер
# 11880 / 24 = 495 - количество перестановок 4 средних ребер, порядок при этом игнорируется
# где:
#   - 12*11*10*9 = 11800 количество позиций 4 средних ребер в фазе 1
#   - 4! = 24 - количество перестановок 4 средних ребер в фазе 2
# fs_classidx[idx][0] -> classidx - класс эквивалентных значений
# получение по индексу номер симметрии из 16 симметрий группы D4h
# fs_classidx[idx][1] -> номер симметрии для fs_classidx[idx][0]

# За счет симметрий это количество перестановок 1013760 «редуцируется» до 64430 классов эквивалентности.
# Каждому классу эквивалентности принадлежит до 16 координат - 16, а не 48, потому что мы используем только симметрии,
# которые сохраняют ось UD (тип группы симметрий - D4h).
# fs_classidx[idx][2] - первое вхождение класса эквивалентности fs_classidx[idx][0]

fs_classidx = get_table("fs_classidx", sym.create_fs_classidx)


#######################################################################################################################


# http://kociemba.org/math/twophase.htm
# загружаем таблицу перестановок 8 углов для фазы 2 c их симметриями
# 8! = 40320 возможных перестановок 8 углов
# co_classidx[idx][0] -> classidx - класс эквивалентных значений

# получение по индексу номера симметрии из 16 симметрий
# co_classidx[idx][1] -> номер симметрии для co_classidx[idx][0]

# За счет симметрий это количество перестановок 40320 «редуцируется» до 2768 классов эквивалентности.
# Каждому классу эквивалентности принадлежит до 16 координат - 16, а не 48, потому что мы используем только симметрии,
# которые сохраняют ось UD, соответственно не меняют ориентацию углов (тип группы симметрий - D4h).
# Для каждого класса эквивалентности мы сохраняем наименьшую координату в качестве
# представителя этого класса в массиве размером 2768
# co_classidx[idx][2] - первое вхождение класса эквивалентности co_classidx[idx][0]

co_classidx = get_table("co_classidx", sym.create_co_classidx)


#######################################################################################################################


# http://kociemba.org/math/movetables.htm
# загружаем таблицы перестановок для отдельных координат
# координаты после применения движения получаются:
# twist_new = move_twist[twist][move]

# ориентация 8 углов
# move_twist[2187][18]
move_twist = get_table("move_twist", m.get_move_twist)

# ориетация 12 ребер
# move_twist[2048][18]
move_flip = get_table("move_flip", m.get_move_flip)

# перестановки 4 ребер UD-среза
# move_slice[11880][18]
move_slice_sorted = get_table("move_ud_slice", m.get_move_slice_sorted)

# перестановки 8 углов
# move_corners[40320][18]
move_corners = get_table("move_corners", m.get_move_corners)

# перестановки 8 ребер верхних и нижних
# move_ud_edges[40320][18]
move_ud_edges = get_table("move_ud_edges", m.get_move_ud_edges)


#######################################################################################################################

# http://kociemba.org/math/pruning.htm
# http://kociemba.org/math/distribution.htm

# таблица обрезки для фазы 1
phase1_prun = get_table("phase1_prun", p.create_pruning1_table, np.int8)

phase2_prun = get_table("phase2_prun", p.create_pruning2_table, np.int8)

#######################################################################################################################
