# Attention Warrior

> Retrospective chapter for 2021. This repository is part of the honest `primeodin-legacy` archive: a reconstruction, study, and mythic technical autobiography forged later, not a falsified historical record.

I call this one `attention-warrior` because an educational Transformer reimplementation teaching attention as disciplined rage focus. The old lesson still bites: if a thing is worth understanding, it is worth reducing until you can hold it in your hand, turn it over, and see where the light leaks through. Feynman had that cheerful cruelty toward confusion. Tryndamere had the less cheerful habit of refusing to fall over. Between those two poles I learned to work: chalk in one hand, blade in the other, patience somewhere under the frost.

The code is intentionally written in a 2021-shaped accent. That does not mean every compiler warning has been preserved like a holy relic, but the dependencies, file shapes, and engineering mood are chosen to fit the period. The goal is not cosplay. The goal is disciplined archaeology: to ask what I would have built if this chapter had been sitting on the bench in 2021, with the tools of that season and the questions that were burning then.

There is a pleasure in finding things out that no trophy can replace. You run the little program, it gives the wrong number, you curse, you sharpen the knife, and then one line moves from darkness into sense. That is the private thunder of computing. Most of the world only sees the finished artifact; the builder remembers the winter: the stale coffee, the bad stack trace, the tiny victory when the rune finally holds.

This chapter favors smallness. The main program is deliberately readable, with comments that explain the pressure behind the choices. If the project is in C, memory is treated like weather: always present, sometimes murderous. If it is Python, the script tries to be plain enough that a student can pull it apart. If it is Java or shell, it carries the blunt habits of its era. I have resisted modern polish where polish would make the fossil lie.

The mythic language is not there to hide weak engineering. It is there because humans remember stories better than configuration flags. A rage meter is just state under stress. A rune is just an invariant you promised not to break. A kingdom is just a system with users depending on it after you have gone to sleep. The words are theatrical; the obligations are plain.

How to read this repository: start with the source. Then read the notes. Then change one parameter and watch what breaks. I have always trusted examples more than sermons. A good example is a small animal: alive, limited, and surprisingly hard to fake. If you can make it fail and then explain the failure, it has taught you something better than success.

This is therefore an artifact of memory rather than evidence of 2021 activity. The commits created by the setup script are current commits with retrospective messages. The tag marks the chapter, not a claim that the public record existed in that year. Legends are strongest when they can stand in daylight. No false snow is needed.

If you fork this, keep the honesty file. If you improve the code, say what you changed and when. If you use the voice, use it to make hard ideas clearer, not to make the past blurrier. The frozen path is long enough without inventing footprints behind us.

## Try it

No extra packages. Python 3.8+ from the repo root:

```bash
python3 main.py
```

Expected stdout (deterministic; the last line is the tiny 3-d head in `attention_warrior/core.py`):

```
attention-warrior :: attention
attention-000 energy=13.16074 peak=5.06112
attention-001 energy=9.43604 peak=4.86551
attention-002 energy=8.13386 peak=4.58891
attention-003 energy=6.07834 peak=4.29216
attention-004 energy=5.32723 peak=4.09066
attention-005 energy=2.78238 peak=2.83186
attention-006 energy=2.58436 peak=2.82135
attention-007 energy=0.63431 peak=1.61772
([0.8320565498522556, 0.7008402876896522], [0.2991597123103478, 0.1679434501477444, 0.5328968375419079])
```

That last line is `(output_vector, softmax_weights)` over three keys and one query. Change a key in `main.py` and watch the weights move. That is the lesson.

Want the same numbers on paper first? Read [`examples/toy-attention-walkthrough.md`](examples/toy-attention-walkthrough.md) — hand-worked dots, softmax, and weighted values that match this stdout.

Why `/ √d` before softmax? [`examples/scale-factor-walkthrough.md`](examples/scale-factor-walkthrough.md) — raw vs scaled side-by-side on the same toy vectors.

Prefer a one-screen map before the arithmetic? See [`docs/attention-diagram.md`](docs/attention-diagram.md) (ASCII + mermaid of query → keys → softmax → values).

Full smoke (run + unit tests):

```bash
./scripts/smoke.sh
```

Success ends with `The rune holds.` If it does not, the console is telling you the truth.

## Help / good first issues

See [CONTRIBUTING.md](CONTRIBUTING.md) for the local loop. Scoped tickets live in [Issues](https://github.com/primeodin/attention-warrior/issues).

**Open (good first issue):**
- [#5](https://github.com/primeodin/attention-warrior/issues/5) — pytest fixture for `AttentionHead.attend` (weights sum ~1)
- [#6](https://github.com/primeodin/attention-warrior/issues/6) — `docs/softmax-stability.md` (why subtract max before exp)
- [#7](https://github.com/primeodin/attention-warrior/issues/7) — `--attend` CLI demo (readable Q/K/V weights table)

**Shipped:**
- [`examples/scale-factor-walkthrough.md`](examples/scale-factor-walkthrough.md) (was #4)
- [`docs/attention-diagram.md`](docs/attention-diagram.md) (was #3)
- [`examples/toy-attention-walkthrough.md`](examples/toy-attention-walkthrough.md) (was #2)

New to pull requests? Start at [first-commit-ai](https://github.com/primeodin/first-commit-ai), then come back.

## Daily builds series

Tiny, tested teaching repos — starter → mid. Ship one, read it, then climb:

| Lane | Repo | Why open it |
| --- | --- | --- |
| Starter | [first-commit-ai](https://github.com/primeodin/first-commit-ai) | Mock-first chat CLI + pytest |
| Starter RAG | [notes-rag](https://github.com/primeodin/notes-rag) | Retrieve, cite, answer over Markdown notes |
| Starter tokenizer | [tiny-bpe-tokenizer](https://github.com/primeodin/tiny-bpe-tokenizer) | Watch text become token IDs — train, encode, decode |
| Mid tool agent | [tiny-tool-agent](https://github.com/primeodin/tiny-tool-agent) | ReAct: Thought, Action, Observation, Final Answer |
| Mid prompt lab | [prompt-lab](https://github.com/primeodin/prompt-lab) | A/B eval: two prompts, fixed cases, score, winner |
| Attention mid (this) | [attention-warrior](https://github.com/primeodin/attention-warrior) | Transformer attention you can hold in one hand |
| Shop skills | [mister-jay](https://github.com/primeodin/mister-jay) | Interactive DIY drills (vehicle, electrical, plumbing) — [live](https://primeodin.github.io/mister-jay/) |
| Literacy (Sinhala) | [jay-ai-sinhala](https://github.com/primeodin/jay-ai-sinhala) | Friends 70+ learning GitHub + AI — [live](https://primeodin.github.io/jay-ai-sinhala/) |
| Systems DIY | [camera-selector](https://github.com/primeodin/camera-selector) | NVR/Frigate camera planning — [live](https://primeodin.github.io/camera-selector/) |

Weekday cadence, in order: chat CLI → RAG → tokenizer → tool agent (shipped) → prompt lab → embeddings → vision → memory → shop-skill explainer.

Profile forge: [github.com/primeodin](https://github.com/primeodin)

## Built-out archive contents

This public-ready build-out adds `docs/CHAPTER.md`, `examples/transcript.txt`, and `scripts/smoke.sh` so the chapter is not only literary but inspectable. The smoke script is intentionally plain: it compiles or runs the small artifact, prints a short trace, and refuses to hide failure. That is the old bargain. If the rune breaks, the console should say so without ceremony.

## GitHub publication note

If this repository appears under `primeodin/attention-warrior`, read it as a chapter of the retrospective archive. The history is honest current work, not an invented twenty-year activity record. The myth is in the voice and the learning arc; the truth is in the archive note.

## What this repository is

This is a runnable retrospective chapter for **attention-warrior**: educational Transformer implementation from first principles.
It is not padded to impress a counter. The implementation is deliberately compact, tested by `./scripts/smoke.sh`, and written so a reader can follow the idea without spelunking through generated fog.

## Public-readiness notes

- The year marker is narrative context, not a forged GitHub timestamp.
- The `.retrospective` tag marks this as part of the honest archive reconstruction.
- Contributions should improve behavior, tests, explanation, or safety — not bulk.
