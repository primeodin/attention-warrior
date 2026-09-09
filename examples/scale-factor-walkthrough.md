# Why divide by √d? (scale-factor walkthrough)

Same toy bench as [`toy-attention-walkthrough.md`](toy-attention-walkthrough.md) and the last line of `python3 main.py`.
Here we only ask: **what does `/ math.sqrt(self.dim)` buy you?**

From `attention_warrior/core.py`:

```python
scores = [dot(query, k) / math.sqrt(self.dim) for k in keys]
weights = softmax(scores)
```

## The bench (dim = 3)

```text
query  q  = [1, 0, 1]
keys   K  = [[1, 0, 0],
             [0, 1, 0],
             [1, 0, 1]]
√3 ≈ 1.7320508
```

Raw dots (no scale):

```text
q · K0 = 1
q · K1 = 0
q · K2 = 2
```

## Side-by-side: raw dots → softmax vs scaled → softmax

Softmax uses a max-shift for stability (`m = max(scores)`), same as `core.py`.

### Raw (no `/ √dim`)

```text
scores = [1, 0, 2]
m = 2

exp(1 − 2) = exp(−1) ≈ 0.367879
exp(0 − 2) = exp(−2) ≈ 0.135335
exp(2 − 2) = 1

sum ≈ 1.503214

w_raw ≈ [0.244728, 0.090031, 0.665241]
```

### Scaled (matches `AttentionHead(3).attend`)

```text
scores = [1/√3, 0/√3, 2/√3] ≈ [0.577350, 0, 1.154701]
m ≈ 1.154701

exp(0.577350 − 1.154701) ≈ exp(−0.577350) ≈ 0.561459
exp(0 − 1.154701)         ≈ exp(−1.154701) ≈ 0.315225
exp(0)                    = 1

sum ≈ 1.876684

w_scaled ≈ [0.299160, 0.167943, 0.532897]
```

Same ranking (K2 wins, K1 loses). Different **sharpness**: raw already piles ~66% on K2; scaled keeps ~53% / 30% / 17% — still peaked, still readable.

Check against the real call:

```bash
python3 main.py
# last line weights: [0.2991597…, 0.1679434…, 0.5328968…]
```

## Punchline (plain English)

Dot products grow with dimension. Softmax is exponential. Without the `/ √d` scale, larger dims push the scores so far apart that softmax collapses toward a **one-hot** — one key eats nearly all the mass, everyone else goes to zero. You stop blending values and start hard-picking.

A tiny taste of that saturation (same *shape* of dots, bigger magnitudes as if dim grew):

```text
scores = [8, 0, 16]     # rough “big-dim” raw dots
softmax ≈ [0.000335, 0.000000, 0.999665]   # basically one-hot on key 2

scores / √64 = [1, 0, 2]   # same ratios, scaled
softmax ≈ [0.244728, 0.090031, 0.665241]   # peaked but not dead
```

So the `/ √dim` line is not fashion. It keeps the educational head (and real Transformer heads) in a regime where **several keys can still share the weight**.

## What to break next

1. Comment out `/ math.sqrt(self.dim)` in `core.py`, re-run `main.py`, and watch the weights harden toward the raw column above.
2. Keep the scale, bump `AttentionHead(3)` to a larger dim while leaving these tiny vectors unchanged — scores shrink, weights flatten (the opposite extreme).
3. Still open: [#5](https://github.com/primeodin/attention-warrior/issues/5) — a pytest fixture that asserts `attend` weights sum ≈ 1.

Paper first, then the code. That is the forge habit.
