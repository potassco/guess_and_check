from . import parse_args, solve_guess_and_check


def main():
    options, binary, toSat, guess_files, check_files = parse_args()
    solve_guess_and_check(options, binary, toSat, guess_files, check_files)


if __name__ == "__main__":
    main()
