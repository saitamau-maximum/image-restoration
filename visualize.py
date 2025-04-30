import argparse
import copy
import imageio
from PIL import Image, ImageDraw


def slide_row(grid, i, k):
    grid[i] = grid[i][-k:] + grid[i][:-k]


def slide_col(grid, j, k):
    N = len(grid)
    col = [grid[i][j] for i in range(N)]
    col = col[-k:] + col[:-k]
    for i in range(N):
        grid[i][j] = col[i]


def create_grid_image(grid, colors, cell_size=20):
    N = len(grid)
    image_width = N * cell_size
    image_height = N * cell_size
    image = Image.new("RGB", (image_width, image_height), "white")
    draw = ImageDraw.Draw(image)

    for i in range(N):
        for j in range(N):
            color_index = grid[i][j]
            color = tuple(colors[color_index])
            x1 = j * cell_size
            y1 = i * cell_size
            x2 = x1 + cell_size
            y2 = y1 + cell_size
            draw.rectangle([x1, y1, x2, y2], fill=color)

    return image


def main():
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("solution_file_path", help="Path to solution file")
        parser.add_argument(
            "--input",
            default="problem.txt",
            help="Path to input file containing grid and colors",
        )
        parser.add_argument(
            "--output", default="out/animation.gif", help="Path to output GIF file"
        )

        args = parser.parse_args()
        input_path = args.input
        solution_path = args.solution_file_path
        output_path = args.output

        N = 0
        M = 0
        initial_grid = []
        answer_grid = []
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
                    initial_grid.append(list(map(int, line.strip().split())))
                for line in lines[N + 1 : 2 * N + 1]:
                    answer_grid.append(list(map(int, line.strip().split())))
                for line in lines[2 * N + 1 : 2 * N + 1 + M]:
                    colors.append(list(map(int, line.strip().split())))
        except FileNotFoundError:
            raise FileNotFoundError(f"Input file not found: {input_path}")
        except ValueError as e:
            raise ValueError(f"Error reading input file: {e}")

        try:
            with open(solution_path, "r") as f:
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
            raise FileNotFoundError(f"Solution file not found: {solution_path}")
        except ValueError as e:
            raise ValueError(f"Error reading solution file: {e}")

        grid = copy.deepcopy(initial_grid)
        images = []
        images.append(create_grid_image(grid, colors))

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
                images.append(create_grid_image(grid, colors))
        except ValueError as e:
            raise ValueError(f"Error during grid operations: {e}")

        imageio.mimsave(output_path, images, duration=0.5)
        print(f"Animation saved to {output_path}")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
