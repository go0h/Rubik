import os
import sys
import array
from rubik.Symmetries import create_conj_twist, create_conj_ud_edges, create_fs_classidx, create_co_classidx
from datetime import datetime


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


# array:
#   H - unsigned short (2 байта) 0..65535
#   B - unsigned char (1 байт) 0..255
#   L - unsigned long (8 байта)
#   b - signed char (1 байт) -128..127

#######################################################################################################################

resource_dir = os.getcwd() + "/resources/"
if os.getcwd().endswith("test"):
    resource_dir = resource_dir.replace("/test", "")

# http://kociemba.org/math/symcord.htm

# загружаем таблицу ориентаций углов для Фазы 1
# 3^7 = 2187 возможных ориентаций углов в Фазе 1
# 16 - количество симметрий подгруппы Dh4 - http://kociemba.org/math/d4h.htm
# twist_conj[2187][16]
# conj_twist = load_table("conj_twist", 2187 * 16, "H")
table_name = "conj_twist"
elem_size = "H"
if os.path.exists(resource_dir + table_name):
    conj_twist = load_table(resource_dir + table_name, 2187 * 16, elem_size)
else:
    conj_twist = create_conj_twist()
    save_table(resource_dir + table_name, conj_twist, elem_size)

# загружаем таблицу перестановок верхних и нижних ребер для Фазы 2 (UR - DB)
# 8! = 40320 возможных перестановок 8 ребер в фазе 1
# 16 - количество симметрий подгруппы Dh4 - http://kociemba.org/math/d4h.htm
# twist_conj[40320][16]
# conj_ud_edges = load_table("conj_ud_edges", 40320 * 16, "H")
table_name = "conj_ud_edges"
elem_size = "H"
if os.path.exists(resource_dir + table_name):
    conj_ud_edges = load_table(resource_dir + table_name, 40320 * 16, elem_size)
else:
    conj_ud_edges = create_conj_ud_edges()
    save_table(resource_dir + table_name, conj_ud_edges, elem_size)

#######################################################################################################################

# http://kociemba.org/math/twophase.htm
# загружаем таблицу перестановок + ориентаций UD-среза для фазы 1
# 2^11 = 2048 возможных ориентаций 12 ребер
# 11880 / 24 = 495 - количество перестановок 4 средних ребер, порядок при этом игнорируется
# где:
#   - 12*11*10*9 = 11800 количество позиций 4 средних ребер в фазе 1
#   - 4! = 24 - количество перестановок 4 средних ребер в фазе 2
# fs_classidx[idx] -> classidx - класс эквивалентных значений
# fs_classidx[495][2048]

# получение по индексу индекс из 16 симметрий
# fs_sym[idx] -> symmetry num для fs_classidx[idx]
# fs_classidx[495][2048]

# За счет симметрий это количество перестановок 1013760 «редуцируется» до 64430 классов эквивалентности.
# Каждому классу эквивалентности принадлежит до 16 координат - 16, а не 48, потому что мы используем только симметрии,
# которые сохраняют ось UD (тип группы симметрий - D4h).
# fs_rep[classidx] - первое вхождение класса эквивалентности
# fs_rep[64430]

table_name1 = "fs_classidx"
table_name2 = "fs_sym"
table_name3 = "fs_rep"
if os.path.exists(resource_dir + table_name1) and \
        os.path.exists(resource_dir + table_name2) and \
        os.path.exists(resource_dir + table_name3):
    fs_classidx = load_table(resource_dir + table_name1, 495 * 2048, "H")
    fs_sym = load_table(resource_dir + table_name2, 2048 * 495, "B")
    fs_rep = load_table(resource_dir + table_name3, 64430, "L")
else:
    tables = create_fs_classidx()
    fs_classidx, fs_sym, fs_rep = tables
    save_table(resource_dir + table_name1, fs_classidx, "H")
    save_table(resource_dir + table_name2, fs_sym, "B")
    save_table(resource_dir + table_name3, fs_rep, "L")

#######################################################################################################################

# http://kociemba.org/math/twophase.htm
# загружаем таблицу перестановок 8 углов для фазы 2
# 8! = 40320 возможных перестановок 8 углов
# co_classidx[idx] -> classidx - класс эквивалентных значений
# co_classidx[40320]
# co_classidx = load_table(resource_dir + "co_classidx", 40320, "H")

# загружаем таблицу номеров симметрий для перестановок углов
# получение по индексу индекс из 16 симметрий
# co_sym[idx] -> symmetry num для co_classidx[idx]
# co_sym[40320]
# co_sym = load_table(resource_dir + "co_sym", 40320, "B")

# За счет симметрий это количество перестановок 40320 «редуцируется» до 2768 классов эквивалентности.
# Каждому классу эквивалентности принадлежит до 16 координат - 16, а не 48, потому что мы используем только симметрии,
# которые сохраняют ось UD, соответственно не меняют ориентацию углов (тип группы симметрий - D4h).
# Для каждого класса эквивалентности мы сохраняем наименьшую координату в качестве
# представителя этого класса в массиве размером 2768
# fs_rep[classidx] - первое вхождение класса эквивалентности
# fs_rep[2768]
# co_rep = load_table("co_rep", 2768, "H")

table_name1 = "co_classidx"
table_name2 = "co_sym"
table_name3 = "co_rep"
if os.path.exists(resource_dir + table_name1) and \
        os.path.exists(resource_dir + table_name2) and \
        os.path.exists(resource_dir + table_name3):
    co_classidx = load_table(resource_dir + table_name1, 40320, "H")
    co_sym = load_table(resource_dir + table_name2, 40320, "B")
    co_rep = load_table(resource_dir + table_name3, 2768, "H")
else:
    tables = create_co_classidx()
    co_classidx, co_sym, co_rep = tables
    save_table(resource_dir + table_name1, co_classidx, "H")
    save_table(resource_dir + table_name2, co_sym, "B")
    save_table(resource_dir + table_name3, co_rep, "H")

#######################################################################################################################
# http://kociemba.org/math/pruning.htm
# http://kociemba.org/math/distribution.htm

# таблица обрезка для фазы 1
table_name = "phase1_prun"
phase1_prun = load_table(resource_dir + table_name, (2187 * 64430) // 16 + 1, "L")

# t1 = datetime.now()
# table_name = "phase1_prun"
# elem_size = "L"
# if os.path.exists(resource_dir + table_name):
#     phase1_prun = load_table(resource_dir + table_name, (2187 * 64430) // 16 + 1, elem_size)
# else:
#     phase1_prun = create_pruning1_table(fs_classidx,fs_rep, fs_sym, conj_twist)
#     save_table(resource_dir + table_name, phase1_prun, elem_size)
#     print(f"Create {table_name} for {datetime.now() - t1}")


# phase1_prun = load_table(resource_dir + "phase1_prun", (2187 * 64430) // 16 + 1, "L")
table_name = "phase2_prun"
phase2_prun = load_table(resource_dir + table_name, (2768 * 40320) // 16, "L")

# distance[20][3] = -128..127
distance = array.array('b', [0 for _ in range(60)])
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
