import os
import sys
import array


def load_table(file_name, table_size, elem_size, resource_dir=f"{os.getcwd()}/resources/"):
    # для тестов
    if os.getcwd().endswith("test"):
        resource_dir = resource_dir.replace("/test", "")
    try:
        with open(resource_dir + file_name, "rb") as file:
            table = array.array(elem_size)
            table.fromfile(file, table_size)
            return table
    except IOError:
        print(f"File {resource_dir}{file_name} not accessible")
        sys.exit(-1)


# array:
#   H - unsigned short (2 байта) 0..65535
#   B - unsigned char (1 байт) 0..255
#   L - unsigned long (8 байта)
#   b - signed char (1 байт) -128..127

#######################################################################################################################

# http://kociemba.org/math/symcord.htm

# загружаем таблицу ориентаций углов для Фазы 1
# 3^7 = 2187 возможных ориентаций углов в Фазе 1
# 16 - количество симметрий подгруппы Dh4 - http://kociemba.org/math/d4h.htm
# twist_conj[2187][16]
twist_conj = load_table("conj_twist", 2187 * 16, "H")

# загружаем таблицу перестановок верхних и нижних ребер для Фазы 2 (UR - DB)
# 8! = 40320 возможных перестановок 8 ребер в фазе 1
# 16 - количество симметрий подгруппы Dh4 - http://kociemba.org/math/d4h.htm
# twist_conj[40320][16]
conj_ud_edges = load_table("conj_ud_edges", 40320 * 16, "H")

#######################################################################################################################

# http://kociemba.org/math/twophase.htm
# загружаем таблицу перестановок + ориентаций UD-среза для фазы 1
# 2^11 = 2048 возможных ориентаций 12 ребер
# 11880 / 24 = 495 - количество перестановок 4 средних ребер, порядок при этом игнорируется
# где:
#   - 12*11*10*9 = 11800 количество позиций 4 средних ребер в фазе 1
#   - 4! = 24 - количество перестановок 4 средних ребер в фазе 2
# fs_classidx[idx] -> classidx - класс эквивалентных значений
# fs_classidx[2048][495]
fs_classidx = load_table("fs_classidx", 495 * 2048, "H")

# загружаем таблицу номеров симметрий для перестановок UD-среза
# получение по индексу индекс из 16 симметрий
# fs_sym[idx] -> symmetry num для fs_classidx[idx]
# fs_classidx[2048][495]
fs_sym = load_table("fs_sym", 2048 * 495, "B")

# За счет симметрий это количество перестановок 1013760 «редуцируется» до 64430 классов эквивалентности.
# Каждому классу эквивалентности принадлежит до 16 координат - 16, а не 48, потому что мы используем только симметрии,
# которые сохраняют ось UD (тип группы симметрий - D4h).
# Для каждого класса эквивалентности мы сохраняем наименьшую координату в качестве
# представителя этого класса в массиве размером 64430
# fs_rep[classidx] - первое вхождение класса эквивалентности
# fs_rep[64430]
# fs_rep = load_table("fs_rep", 64430, "L")

#######################################################################################################################

# http://kociemba.org/math/twophase.htm
# загружаем таблицу перестановок 8 углов для фазы 2
# 8! = 40320 возможных перестановок 8 углов
# co_classidx[idx] -> classidx - класс эквивалентных значений
# co_classidx[40320]
co_classidx = load_table("co_classidx", 40320, "H")

# загружаем таблицу номеров симметрий для перестановок углов
# получение по индексу индекс из 16 симметрий
# co_sym[idx] -> symmetry num для co_classidx[idx]
# co_sym[40320]
co_sym = load_table("co_sym", 40320, "B")

# За счет симметрий это количество перестановок 40320 «редуцируется» до 2768 классов эквивалентности.
# Каждому классу эквивалентности принадлежит до 16 координат - 16, а не 48, потому что мы используем только симметрии,
# которые сохраняют ось UD, соответственно не меняют ориентацию углов (тип группы симметрий - D4h).
# Для каждого класса эквивалентности мы сохраняем наименьшую координату в качестве
# представителя этого класса в массиве размером 2768
# fs_rep[classidx] - первое вхождение класса эквивалентности
# fs_rep[2768]
# co_rep = load_table("co_rep", 2768, "H")

#######################################################################################################################

# Таблицы перемещения представляют собой двумерные массивы, описывающие,
# как изменяется та или иная координата при вращении.

# Пример:
# Для тог чтобы привеменить перемещение R2,
# move_twist[old_twist * 18 + 3 * R + 1] = new_twist даст новую координату
#   где - 18 количество возможных перемещений для каждого состояния
#       - 3 - количество возможных вращений вокруг каждой стороны
#       - R - порядковый номер стороны (U, R, F, D, L, B)
#       - R - порядковый номер вращения (R - 0, R2 - 1, R' - 2)
# Это делается быстрее по сравнению с перестановкой на уровне CubieCube или на уровне FaceletCube.


# Таблица ориентаций 8 углов для 18 возможных ходов (см. rubik.Utils.MOVES)
# 3^7 = 2187 количество возжножных ориентаций 8 углов для Фазы 1. Фаза 2 - 0.
# 18 - возможные ходы
# move_twist[2187][18]
move_twist = load_table("move_twist", 2187 * 18, "H")


# Таблица ориентаций 12 ребер для 18 возможных ходов (см. rubik.Utils.MOVES)
# 2^11 = 2048 количество возжножных ориентаций 12 углов для Фазы 1. Фаза 2 - 0.
# 18 - возможные ходы
# move_flip[2048][18]
move_flip = load_table("move_flip", 2048 * 18, "H")

# Таблица перестановок 4 UD-разреза ребер для 18 возможных ходов (см. rubik.Utils.MOVES)
# 12!/8! = 11880 количество возжножных перестановок 4 UD-разреза ребер для Фазы 1.
# Фаза 2 - 4! - 24.
# 18 - возможные ходы
# move_flip[11880][18]
move_slice_sorted = load_table("move_slice_sorted", 11880 * 18, "H")

# Таблица перестановок 8 Up-Down-ребер для 18 возможных ходов (см. rubik.Utils.MOVES) для Фазы 2.
# Фаза 1 - не используется
# 8! = 40320 количество возжножных перестановок 8 Up-Down-ребер для Фазы 2.
# Собранный куб - 0.
# 18 - возможные ходы
# move_u_edges[40320][18]
move_ud_edges = load_table("move_ud_edges", 40320 * 18, "H")


# Таблица перестановок 8 углов для 18 возможных ходов (см. rubik.Utils.MOVES).
# 8! = 40320 количество возжножных перестановок 8 углов.
# Собранный куб - 0.
# 18 - возможные ходы
# move_u_edges[40320][18]
move_corners = load_table("move_corners", 40320 * 18, "H")

#######################################################################################################################
# http://kociemba.org/math/pruning.htm
# http://kociemba.org/math/distribution.htm

# таблица обрезка для фазы 1
# по
phase1_prun = load_table("phase1_prun", (2187 * 64430) // 16 + 1, "L")

phase2_prun = load_table("phase2_prun", (2768 * 40320) // 16, "L")

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
