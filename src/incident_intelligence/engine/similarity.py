import re
from .scoring import clamp

_STOP = {"the", "and", "for", "with", "from", "service", "error"}

def _tokens(text: str) -> set[str]:
    words = re.findall(r"[a-z0-9]+", text.casefold())
    return {w for w in words if len(w) > 2 and w not in _STOP}

def fingerprint(i):
    tokens = _tokens(i.service) | _tokens(i.title)
    tokens |= set().union(*(_tokens(s) for s in i.symptoms)) if i.symptoms else set()
    tokens |= set().union(*(_tokens(e.signal) for e in i.evidence)) if i.evidence else set()
    return tuple(sorted(tokens))

def similarity(a, b):
    A, B = set(fingerprint(a)), set(fingerprint(b))
    if not A or not B:
        return 0.0
    jaccard = len(A & B) / len(A | B)
    service = 1.0 if a.service.casefold() == b.service.casefold() else 0.0
    severity = 1 - abs(a.severity-b.severity)/9
    symptom_overlap = len(_tokens(" ".join(a.symptoms)) & _tokens(" ".join(b.symptoms))) / max(1, len(_tokens(" ".join(a.symptoms)) | _tokens(" ".join(b.symptoms))))
    return round(clamp((jaccard*.45 + service*.25 + severity*.10 + symptom_overlap*.20)*100), 2)
