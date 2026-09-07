# Toy attention walkthrough (3 keys, 1 query)

A chalk-board pass through the same call `main.py` prints at the end.
No network. No packages. Pencil and a calculator are enough.

## The bench setup

From `attention_warrior/core.py`, one head with `dim = 3`:

```text
query  q  = [1, 0, 1]
keys   K  = [[1, 0, 0],
             [0, 1, 0],
             [1, 0, 1]]
values V  = [[1, 0],
             [0, 1],
             [1, 1]]
```

Scores are scaled dots: `score_i = (q · K_i) / sqrt(dim)`.

## Step 1 — dots and scale

```text
sqrt(3) ≈ 1.7320508

q · K0 = 1·1 + 0·0 + 1·0 = 1   →  score0 = 1 / √3 ≈ 0.577350
q · K1 = 1·0 + 0·1 + 1·0 = 0   →  score1 = 0 / √3 = 0
q · K2 = 1·1 + 0·0 + 1·1 = 2   →  score2 = 2 / √3 ≈ 1.154701
```

Key 2 is the closest shape to the query (both have energy on dims 0 and 2). Key 1 is orthogonal. That is the whole trick before softmax.

## Step 2 — softmax weights

```text
m = max(scores) = score2 ≈ 1.154701

exp(score0 − m) ≈ exp(−0.577350) ≈ 0.561459
exp(score1 − m) ≈ exp(−1.154701) ≈ 0.315225
exp(score2 − m) ≈ exp(0)         = 1

sum ≈ 1.876684

w0 ≈ 0.299160
w1 ≈ 0.167943
w2 ≈ 0.532897
```

Most of the mass lands on key 2 (~53%). Key 0 still gets a fair share (~30%). Key 1 is the quiet one (~17%).

## Step 3 — weighted values

```text
out = w0·V0 + w1·V1 + w2·V2
    = 0.299160·[1, 0] + 0.167943·[0, 1] + 0.532897·[1, 1]
    ≈ [0.832057, 0.700840]
```

That is exactly the last line of `python3 main.py`:

```text
([0.8320565498522556, 0.7008402876896522],
 [0.2991597123103478, 0.1679434501477444, 0.5328968375419079])
```

`(output_vector, softmax_weights)` — output first, then the three weights over the keys.

## What to break next

1. Flip `K1` to `[1, 0, 1]` in `main.py` and re-run — watch `w1` rise.
2. Change one value row and see the output vector move while weights stay put (values do not affect scores).
3. When you want a one-screen map of the same path, claim [#3](https://github.com/primeodin/attention-warrior/issues/3) (ASCII Q/K/V diagram).

The rune is small on purpose. If you can redo these three steps on paper, you own the head.
