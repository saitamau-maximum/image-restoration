import argparse
import copy


def slide_row(grid, i, k):
    grid[i] = grid[i][-k:] + grid[i][:-k]


def slide_col(grid, j, k):
    N = len(grid)
    col = [grid[i][j] for i in range(N)]
    col = col[-k:] + col[:-k]
    for i in range(N):
        grid[i][j] = col[i]


def main():
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "solution_file_path", help="Path to input image file (e.g. PNG)"
        )
        parser.add_argument("--input", default="problem.txt", help="Path to input file")

        args = parser.parse_args()
        input_path = args.input
        solution_file_path = args.solution_file_path

        N = 0
        M = 0
        answer_grid = []
        initial_grid = []
        colors = []

        try:
            with open(input_path, "r") as f:
                lines = f.readlines()
                if not lines:
                    raise ValueError("Input file is empty")
                N, M = map(int, lines[0].strip().split())
                if N <= 0 or M <= 0:
                    raise ValueError("Grid dimensions must be positive integers")
                for line in lines[1 : N + 1]:
                    answer_grid.append(list(map(int, line.strip().split())))
                for line in lines[N + 1 : 2 * N + 1]:
                    initial_grid.append(list(map(int, line.strip().split())))
                for line in lines[2 * N + 1 : 2 * N + 1 + M]:
                    colors.append(list(map(int, line.strip().split())))
        except FileNotFoundError:
            raise FileNotFoundError(f"Input file not found: {input_path}")
        except ValueError as e:
            raise ValueError(f"Error reading input file: {e}")

        try:
            with open(solution_file_path, "r") as f:
                lines = f.readlines()
                if not lines:
                    raise ValueError("Solution file is empty")
                ops = []
                for line in lines:
                    op = line.strip().split()
                    if len(op) != 3:
                        raise ValueError(f"Invalid operation format: {line}")
                    if op[0] not in ["R", "C"]:
                        raise ValueError(f"Invalid operation type: {op[0]}")
                    try:
                        op[1] = int(op[1])
                        op[2] = int(op[2])
                    except ValueError:
                        raise ValueError(f"Invalid operation parameters: {op}")

                    ops.append(op)
        except FileNotFoundError:
            raise FileNotFoundError(f"Solution file not found: {solution_file_path}")
        except ValueError as e:
            raise ValueError(f"Error reading solution file: {e}")

        grid = copy.deepcopy(initial_grid)
        try:
            for op in ops:
                if op[0] == "R":
                    i, k = op[1], op[2]
                    if i < 0 or i >= N or k < 1 or k >= N:
                        raise ValueError(f"Invalid row operation: {op}, out of range")
                    slide_row(grid, i, k)
                elif op[0] == "C":
                    j, k = op[1], op[2]
                    if j < 0 or j >= N or k < 1 or k >= N:
                        raise ValueError(
                            f"Invalid column operation: {op}, out of range"
                        )
                    slide_col(grid, j, k)
        except ValueError as e:
            raise ValueError(f"Error during grid operations: {e}")

        # Validate the grid
        for i in range(N):
            for j in range(N):
                if grid[i][j] != answer_grid[i][j]:
                    raise ValueError(f"Grid does not match at ({i}, {j})")
        print("Valid grid")

        print(f"Turn: {len(ops)}")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
