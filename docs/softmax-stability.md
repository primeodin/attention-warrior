# Why subtract max before exp? (softmax stability)

Softmax turns scores into weights that sum to 1. The formula newcomers copy is:

```text
w_i = exp(x_i) / sum_j exp(x_j)
```

The forge version in `attention_warrior/core.py` does one extra move first:

```python
def softmax(xs):
    m = max(xs)
    ex = [math.exp(x - m) for x in xs]
    s = sum(ex)
    return [x / s for x in ex]
```

That `x - m` is not decoration. It keeps the math the same and stops the tape from running off the end.

## Bench: three scores

Issue asked for something like `10, 8, 2` — large enough that raw `exp` already looks ugly, small enough to do by hand.

```text
scores x = [10, 8, 2]
m = max(x) = 10
```

## Path A — no subtract (unstable sketch)

```text
exp(10) ≈ 22026.4658
exp(8)  ≈  2980.9580
exp(2)  ≈     7.3891
------------------------
sum     ≈ 25014.8128

w ≈ [0.880537, 0.119168, 0.000295]
sum(w) ≈ 1.000000
```

On this tiny bench float still survives. The hazard shows up when scores get bigger: `exp(1000)` overflows in Python (`OverflowError: math range error`). One huge score and the whole denom dies.

Shop note: you can get the *right* weights here and still be one bad batch away from a crash. Surviving once is not the same as a safe path.

## Path B — subtract max (stable, matches `core.py`)

```text
exp(10 − 10) = exp(0)  = 1
exp(8 − 10)  = exp(−2) ≈ 0.135335
exp(2 − 10)  = exp(−8) ≈ 0.00033546
------------------------------------
sum          ≈ 1.135671

w ≈ [0.880537, 0.119168, 0.000295]
sum(w) ≈ 1.000000
```

Same weights as Path A. Numbers stay near 1 instead of twenty thousand. The max becomes `exp(0) = 1`, everything else is ≤ 1, and the sum stays calm.

## Prove they match (and still sum to 1)

| score | raw `exp(x)` | `exp(x − max)` | weight |
| ---: | ---: | ---: | ---: |
| 10 | 22026.4658 | 1.000000 | 0.880537 |
| 8 | 2980.9580 | 0.135335 | 0.119168 |
| 2 | 7.3891 | 0.000335 | 0.000295 |
| **sum** | 25014.8128 | 1.135671 | **1.000000** |

Algebra punchline: dividing numerator and denominator by `exp(m)` is the same as subtracting `m` inside every `exp`. Softmax is shift-invariant — adding or subtracting the same constant from every score does not change the weights. We pick the constant that makes the biggest term `1`.

## When raw blows up for real

```text
scores = [1000, 998, 990]

exp(1000)  → OverflowError
exp(998)   → OverflowError
…
```

Shifted:

```text
exp(0)     = 1
exp(−2)    ≈ 0.135335
exp(−10)   ≈ 4.54e-05
sum        ≈ 1.135381
w          ≈ [0.880762, 0.119198, 0.000040]
```

Same ranking, no crash. That is why `core.py` always does `m = max(xs)` before `math.exp`.

## Tie to the real head

`AttentionHead.attend` builds scores, then calls this softmax:

```python
scores = [dot(query, k) / math.sqrt(self.dim) for k in keys]
weights = softmax(scores)
```

Scale (`/ √d`) keeps scores from getting huge in high dim. Max-shift keeps `exp` from exploding even when one score still wins big. Two shop moves, one job: weights that blend instead of a smoking console.

## Check it yourself

```bash
python3 - <<'PY'
import math
from attention_warrior.core import softmax

xs = [10, 8, 2]
w = softmax(xs)
print(w, sum(w))
assert abs(sum(w) - 1.0) < 1e-9
PY
```

If your hand table and `softmax([10, 8, 2])` disagree past a few decimals, re-check the arithmetic before blaming the forge.
