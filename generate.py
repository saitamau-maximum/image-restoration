import numpy as np
from PIL import Image
import random
from sklearn.cluster import KMeans
import argparse


def quantize_image(img, M):
    data = np.array(img).reshape((-1, 3))
    kmeans = KMeans(n_clusters=M, random_state=42).fit(data)
    labels = kmeans.predict(data)
    label_img = labels.reshape(img.size[1], img.size[0])
    return label_img, kmeans.cluster_centers_


def slide_row(grid, i, k):
    grid[i] = grid[i][-k:] + grid[i][:-k]


def slide_col(grid, j, k):
    N = len(grid)
    col = [grid[i][j] for i in range(N)]
    col = col[-k:] + col[:-k]
    for i in range(N):
        grid[i][j] = col[i]


def shuffle_grid(grid, shuffle_ops=1000):
    N = len(grid)
    for _ in range(shuffle_ops):
        if random.choice([True, False]):
            i = random.randint(0, N - 1)
            k = random.randint(1, N - 1)
            slide_row(grid, i, k)
        else:
            j = random.randint(0, N - 1)
            k = random.randint(1, N - 1)
            slide_col(grid, j, k)


def generate_preview_image(grid, centers):
    N = len(grid)
    img = Image.new("RGB", (N, N))
    pixels = img.load()
    for i in range(N):
        for j in range(N):
            color = tuple(int(c) for c in centers[grid[i][j]])
            pixels[j, i] = color
    return img


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("image_path", help="Path to input image file (e.g. PNG)")
    parser.add_argument("--N", type=int, default=100, help="Grid size")
    parser.add_argument("--M", type=int, default=5, help="Number of colors")
    parser.add_argument("--shuffle", type=int, default=1000, help="Shuffle operations")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument("--preview", action="store_true", help="Show preview images")
    args = parser.parse_args()

    random.seed(args.seed)
    np.random.seed(args.seed)
    if args.N <= 0 or args.M <= 0:
        raise ValueError("N and M must be positive integers.")

    img = (
        Image.open(args.image_path)
        .convert("RGB")
        .resize((args.N, args.N), Image.LANCZOS)
    )
    label_img, centers = quantize_image(img, args.M)

    original = label_img.tolist()
    shuffled = [row[:] for row in original]
    shuffle_grid(shuffled, args.shuffle)

    output_lines = []
    output_lines.append(f"{args.N} {args.M}")
    for row in original:
        output_lines.append(" ".join(map(str, row)))
    for row in shuffled:
        output_lines.append(" ".join(map(str, row)))
    for center in centers:
        output_lines.append(" ".join(map(str, map(int, center))))

    with open("./out/in.txt", "w") as f:
        f.write("\n".join(output_lines))

    if args.preview:
        preview_img = generate_preview_image(original, centers)
        preview_img.save("./out/original.png")
        preview_img = generate_preview_image(shuffled, centers)
        preview_img.save("./out/shuffled.png")


if __name__ == "__main__":
    main()
