import sys
import argparse
import rubik.Utils as u
import rubik.CubieCube as cc
import solver.TwoPhaseSolver as tfs


def solve(scramble_str, debug_mode, print_move, max_move):
    try:
        cubie = cc.CubieCube()
        cubie.scramble(scramble_str)
        solver = tfs.TwoPhaseSolver(cubie, max_move)
        moves = solver.solve(debug_mode, print_move)
        if len(moves) == 0:
            print(f"The cubie is already solved")
        else:
            print(' '.join([i for i in moves]))
    except ValueError as err:
        print(err)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Rubik's Cube Solver, with Kociemba algorithm")
    parser.add_argument("-d", "--debug", nargs="?", type=bool,
                        const=True, default=False, help="Debug mode")
    parser.add_argument("-s", "--scramble", nargs="+", type=str, metavar="move",
                        help="Scramble of Rubik's Cube to be solved")
    parser.add_argument("-g", "--god", nargs="?", type=bool,
                        const=True, default=False, help="God's mode")
    parser.add_argument("-p", "--print", nargs="?", type=bool,
                        const=True, default=False, help="Print moves")
    args = parser.parse_args()
    scramble = args.scramble
    debug = args.debug
    print_moves = args.print
    if args.god:
        max_moves = 21
    else:
        max_moves = 40

    if args.scramble is None:
        while True:
            try:
                scramble = input("Enter a scramble: ")
                scramble = ' '.join(scramble.split())
            except EOFError:
                print()
                sys.exit(0)
            if scramble in ["Q", "QUIT"]:
                sys.exit(0)
            elif scramble in ["D", "DEBUG"]:
                debug = not debug
            elif scramble in ["M", "MOVES"]:
                print_moves = not print_moves
            elif scramble == "RANDOM":
                scramble = u.get_random_scramble()
                print(f"Random scramble = {scramble}")
                solve(scramble, debug, print_moves, max_moves)
            else:
                solve(scramble, debug, print_moves, max_moves)
    else:
        solve(' '.join(scramble), debug, print_moves, max_moves)
