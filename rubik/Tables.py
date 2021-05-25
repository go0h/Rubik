import os
import sys
import array
import rubik.Symmetries as sym
import rubik.Moves as m
import numpy as np


def load_table(file_name, table_size, size):
    try:
        with open(file_name, "rb") as file:
            table = array.array(size)
            table.fromfile(file, table_size)
    except IOError:
        print(f"File {file_name} not accessible")
        sys.exit(-1)
    return table


def save_table(file_name, arr, size):
    try:
        with open(file_name, "wb") as file:
            table = array.array(size, arr)
            table.tofile(file)
    except IOError:
        print(f"File {file_name} not accessible")
        sys.exit(-1)


def load_table_np(file_name):
    try:
        with open(file_name, "rb") as file:
            table = np.loadtxt(file, dtype="int").tolist()
    except IOError:
        print(f"File {file_name} not accessible")
        sys.exit(-1)
    return table


def save_table_np(file_name, arr):
    try:
        with open(file_name, "wb") as file:
            np.savetxt(file, np.array(arr), fmt="%d")
    except IOError:
        print(f"File {file_name} not accessible")
        sys.exit(-1)


def get_table(table_name, create_table_func):

    dir = os.getcwd() + "/resources/"
    if os.getcwd().endswith("test"):
        dir = dir.replace("/test", "")
    table_name = dir + table_name

    if os.path.exists(table_name):
        try:
            with open(table_name, "rb") as file:
                table = np.loadtxt(file, dtype="int").tolist()
        except IOError:
            print(f"File {table_name} not accessible")
            sys.exit(-1)
    else:
        table = create_table_func()
        try:
            with open(table_name, "wb") as file:
                np.savetxt(file, np.array(table), fmt="%d")
        except IOError:
            print(f"File {table_name} not accessible")
            sys.exit(-1)
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
move_slice = get_table("move_slice", m.get_move_slice_sorted)

# перестановки 8 углов
# move_corners[40320][18]
move_corners = get_table("move_corners", m.get_move_corners)

# перестановки 8 ребер верхних и нижних
# move_ud_edges[40320][18]
move_edges = get_table("move_ud_edges", m.get_move_ud_edges)


#######################################################################################################################


# http://kociemba.org/math/pruning.htm
# http://kociemba.org/math/distribution.htm

# array:
#   H - unsigned short (2 байта) 0..65535
#   B - unsigned char (1 байт) 0..255
#   L - unsigned long (8 байта)
#   b - signed char (1 байт) -128..127

resource_dir = os.getcwd() + "/resources/"
if os.getcwd().endswith("test"):
    resource_dir = resource_dir.replace("/test", "")

# таблица обрезки для фазы 1
table_name = "phase1_prun"
phase1_prun = load_table(resource_dir + table_name, (2187 * 64430) // 16 + 1, "L")

table_name = "phase2_prun"
phase2_prun = load_table(resource_dir + table_name, (2768 * 40320) // 16, "L")

# distance[20][3] = -1 .. 19
distance = [0 for _ in range(60)]
for i in range(20):
    for j in range(3):
        distance[3 * i + j] = (i // 3) * 3 + j
        if i % 3 == 2 and j == 0:
            distance[3 * i + j] += 3
        elif i % 3 == 0 and j == 2:
            distance[3 * i + j] -= 3

#######################################################################################################################


def get_fs_twist_depth3(index):
    """Возвращает количество ходов по модулю 3 для решения фазы 1 для куба с индексом index"""
    y = phase1_prun[index // 16]
    y >>= (index % 16) * 2
    return y & 3


def get_co_ud_edges_depth3(index):
    """Возвращает количество ходов по модулю 3 для решения фазы 2 для куба с индексом index"""
    y = phase2_prun[index // 16]
    y >>= (index % 16) * 2
    return y & 3
