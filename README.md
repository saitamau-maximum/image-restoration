# Image Restoration

トーラス状の NxN グリッドにおいて、任意の行か列を任意の方向にスライドできる操作を 1 ターンとして、ピクセルランダマイズされた M 色で構成される画像をグリットにおいた時、スライドパズルの要領で復元する最短手数を求めるソルバーを作成せよ

デフォルトパラメータ

```txt
N = 100
M = 5
shuffle = 1000
seed = 42
```

## 入力

- N: グリッドのサイズ
- M: 色の数
- Pc_ij: i 行 j 列のピクセルの色 (正解)
- Pr_ij: i 行 j 列のピクセルの色 (初期状態)
- C_ir, C_ig, C_ib: i 番目の色 (rgb)

C は Visualizer で表示するための色を指定するためのもので、回答に利用する必要はありません。

```txt
N M
Pc_00 Pc_01 ... Pc_0N
Pc_10 Pc_11 ... Pc_1N
...
Pc_N0 Pc_N1 ... Pc_NN
Pr_00 Pr_01 ... Pr_0N
Pr_10 Pr_11 ... Pr_1N
...
Pr_N0 Pr_N1 ... Pr_NN
C_0r C_0g C_0b
C_1r C_1g C_1b
...
C_Mr C_Mg C_Mb
```

### 例

```txt
5 3
1 2 0 0 0
0 1 2 0 0
0 0 1 2 0
0 0 0 1 2
2 0 0 0 1
1 2 0 0 0
1 2 0 0 0
1 2 0 0 0
1 2 0 0 0
1 2 0 0 0
```

## 出力

- O_i: i 行目のスライド操作
  - `R` 行
  - `C` 列
- N: 何行/何列目か
- D: 何回スライドするか

```txt
O_0 N D
O_1 N D
...
O_N N D
```

## スコア

スコアは単純にテストが通った時の出力の行数で評価し、低いほど良い。

### 例

```txt
R 0 1
C 4 1
R 2 3
```

## 出力のテスト

```bash
uv run test.py [solution_file_path]
```

## ビジュアライザー

```bash
uv run visualize.py [solution_file_path]
```

## 問題生成

```bash
uv run generate.py [png_image_path]
```
