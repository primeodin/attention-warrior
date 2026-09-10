# Why values aren't keys (lookup ≠ payload)

Attention has three roles:

- **Query** — what you are looking for
- **Keys** — the address book you match against
- **Values** — the boxes you actually pull off the shelf

Tutorials often draw one matrix and call it `K`/`V` as if they were the same tensor. In this forge head they are separate on purpose. Collapse them and you still get *weights*, but the *output* stops meaning "retrieved payload."

The demo in `main.py` already separates them. Same numbers as stdout:

```python
head.attend(
    [1, 0, 1],                         # query
    [[1, 0, 0], [0, 1, 0], [1, 0, 1]], # keys
    [[1, 0], [0, 1], [1, 1]],          # values (2-d payload)
)
# → ([0.832…, 0.701…], [0.299…, 0.168…, 0.533…])
```

## Same weights either way

Scores use only `Q` and `K` (`dot / √d`, then softmax). Values never touch the match step.

| key | `q·k` | `/ √3` | weight |
| --- | ---: | ---: | ---: |
| `[1,0,0]` | 1 | 0.57735 | **0.29916** |
| `[0,1,0]` | 0 | 0.00000 | **0.16794** |
| `[1,0,1]` | 2 | 1.15470 | **0.53290** |

`sum(w) = 1`. Those three weights are locked before `V` shows up.

## Path A — real payload (`V` as in `main.py`)

```text
out = 0.29916·[1,0] + 0.16794·[0,1] + 0.53290·[1,1]
    = [0.83206, 0.70084]
```

Matches the printed output vector. Keys found slot 2 strongest; values delivered a 2-d box.

## Path B — trap: set `V = K` (lookup doubles as payload)

```text
out = 0.29916·[1,0,0] + 0.16794·[0,1,0] + 0.53290·[1,0,1]
    = [0.83206, 0.16794, 0.53290]
```

Same weights. Different object: a soft blend of the *addresses*, not a retrieved payload. Dim even changes (3 vs 2) because you copied the key space.

| path | what you blend | output |
| --- | --- | --- |
| A — separate `V` | payload boxes | `[0.832, 0.701]` (2-d) |
| B — `V = K` | the keys themselves | `[0.832, 0.168, 0.533]` (3-d) |

## Shop judgment

- **Keep them separate** when the thing you match on is not the thing you want back (token id vs embedding, camera id vs layout note, question vs cited paragraph).
- **Sharing `K`/`V` in one matrix** is a training convenience in big models, not a license to forget the roles. If a student only ever sees one tensor, they will think attention "returns similar keys." It doesn't — it *weights values* by key match.
- **Debug tip:** if weights look right but the answer is nonsense, print `V` rows by themselves. Bad shelf, good address book.

Run `python3 main.py` and change only the values list. Weights stay put; the output vector moves. That is the lesson.
