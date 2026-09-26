# EU AI Act Obligation Tracker

Maps EU AI Act obligations by system risk class with applicability, prohibited-use verdicts, and compliance scoring.

**Stack:** Python 3.12 · stdlib only · unittest

## Problem

Maps the EU AI Act's obligations by system risk class (prohibited,
high-risk, limited-risk, minimal-risk): each obligation names its
article and the classes it applies to. applicable() lists a system's
duties; verdict() blocks prohibited uses outright; assess() scores
implementation and names the gaps.

## Design decisions

- Obligations carry an applies_to set of risk classes; prohibited
- assess() returns a compliance percent plus the missing obligation ids.
- Article numbers are display strings ("Art. 9"); risk classes are a

## Layout

- `README.md`
- `src/eu_act_tracker.py`
- `tests/test_eu_act_tracker.py`
- `LICENSE`
- `.gitignore`

## Setup

No third-party dependencies — Python 3.11+ standard library only.

```bash
cd govops-eu-act-tracker
python -m unittest discover -s tests -v
```

## Usage

```python
from src.eu_act_tracker import EUActTracker, Obligation

t = EUActTracker()
t.add(Obligation("O1", "Risk management system", "Art. 9", ["high-risk"]))
print(t.verdict("high-risk"))
print(t.assess("high-risk", ["O1"]))
```

## License

MIT — see [LICENSE](LICENSE).
