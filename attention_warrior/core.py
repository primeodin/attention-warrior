import math, random, statistics
from .utils import clamp, moving_average, ascii_bar

PROJECT="attention-warrior"
DOMAIN="attention"
YEAR=2021

class Trace:
    def __init__(self):
        self.rows=[]
    def add(self, step, value, note=""):
        self.rows.append({"step":step,"value":float(value),"note":note})
    def mean(self):
        return statistics.mean([r["value"] for r in self.rows]) if self.rows else 0.0
    def render(self, limit=12):
        lines=[]
        for r in self.rows[:limit]:
            lines.append(f"{r['step']:03d} {r['value']:.5f} {ascii_bar(abs(r['value'])%1.0, 24)} {r['note']}")
        return "\n".join(lines)

def dot(a,b): return sum(x*y for x,y in zip(a,b))
def softmax(xs):
    m=max(xs); ex=[math.exp(x-m) for x in xs]; s=sum(ex); return [x/s for x in ex]

class AttentionHead:
    def __init__(self, dim): self.dim=dim
    def attend(self, query, keys, values):
        scores=[dot(query,k)/math.sqrt(self.dim) for k in keys]; weights=softmax(scores)
        out=[0.0]*len(values[0])
        for w,v in zip(weights,values):
            for i,x in enumerate(v): out[i]+=w*x
        return out,weights

def scenario(index=0, seed=None):
    """Return one deterministic teaching scenario without generated boilerplate.

    Earlier drafts carried hundreds of numbered functions. That made the forge
    look loud but not stronger. The real rune is the parameterization: same idea,
    one readable path, many repeatable cases.
    """
    if index < 0:
        raise ValueError("scenario index must be non-negative")
    if seed is None:
        seed = index
    rng = random.Random(seed + YEAR + index * 17)
    period = 11.0 + (index % 7)
    damping = 0.82 + (index % 5) * 0.025
    values = []
    carry = 0.0
    for j in range(32):
        signal = math.sin((j + 1) * (index + 1) / period)
        noise = (rng.random() - 0.5) * 0.08
        carry = damping * carry + signal + noise
        values.append(carry)
    smooth = moving_average(values, 5)
    energy = sum(v * v for v in smooth) / len(smooth)
    return {"name": f"attention-{index:03d}", "energy": energy, "peak": max(smooth), "trough": min(smooth)}


def run_scenarios(limit=8, seed=0):
    if limit < 0:
        raise ValueError("limit must be non-negative")
    return [scenario(i, seed + i) for i in range(limit)]
