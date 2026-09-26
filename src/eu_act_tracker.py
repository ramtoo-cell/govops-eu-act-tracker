
"""EU AI Act obligation tracker.

Maps the EU AI Act's obligations by system risk class (prohibited,
high-risk, limited-risk, minimal-risk): each obligation names its
article and the classes it applies to. applicable() lists a system's
duties; verdict() blocks prohibited uses outright; assess() scores
implementation and names the gaps.

Design:
- Obligations carry an applies_to set of risk classes; prohibited
  systems get a hard block verdict, not a compliance checklist.
- assess() returns a compliance percent plus the missing obligation ids.
- Article numbers are display strings ("Art. 9"); risk classes are a
  closed vocabulary validated at registration.
"""
from __future__ import annotations

from dataclasses import dataclass, field

RISK_CLASSES = ("prohibited", "high-risk", "limited-risk", "minimal-risk")


@dataclass
class Obligation:
    """One regulatory obligation."""
    ob_id: str
    title: str
    article: str
    applies_to: list = field(default_factory=list)
    description: str = ""


class EUActTracker:
    """Obligation store with applicability and compliance scoring."""

    def __init__(self):
        self._obligations = {}

    def add(self, obligation):
        if obligation.ob_id in self._obligations:
            raise ValueError("duplicate ob_id %r" % (obligation.ob_id,))
        bad = [c for c in obligation.applies_to if c not in RISK_CLASSES]
        if bad:
            raise ValueError("invalid risk classes: %s" % ", ".join(bad))
        if not obligation.applies_to:
            raise ValueError("obligation must apply to at least one risk class")
        obligation.applies_to = list(obligation.applies_to)
        self._obligations[obligation.ob_id] = obligation
        return obligation

    def get(self, ob_id):
        try:
            return self._obligations[ob_id]
        except KeyError:
            raise KeyError("unknown ob_id %r" % (ob_id,))

    def _require_class(self, risk_class):
        if risk_class not in RISK_CLASSES:
            raise ValueError("unknown risk class %r" % (risk_class,))

    def applicable(self, risk_class):
        """Obligations applying to a risk class, sorted by ob_id."""
        self._require_class(risk_class)
        return sorted((o for o in self._obligations.values()
                       if risk_class in o.applies_to),
                      key=lambda o: o.ob_id)

    def verdict(self, risk_class):
        """Allowed/blocked verdict for deploying a system of this class."""
        self._require_class(risk_class)
        if risk_class == "prohibited":
            return {"allowed": False,
                    "reason": "prohibited use case under the EU AI Act",
                    "obligations": []}
        return {"allowed": True, "reason": "",
                "obligations": [o.ob_id for o in self.applicable(risk_class)]}

    def assess(self, risk_class, implemented_ids):
        """Compliance score for a system: percent + missing obligations."""
        applicable = self.applicable(risk_class)
        required = [o.ob_id for o in applicable]
        implemented = [i for i in required if i in implemented_ids]
        missing = [i for i in required if i not in implemented_ids]
        pct = round(len(implemented) / len(required), 3) if required else 1.0
        return {
            "risk_class": risk_class,
            "required": required,
            "implemented": implemented,
            "missing": missing,
            "compliance_pct": pct,
            "compliant": not missing,
        }

    def articles(self):
        return sorted({o.article for o in self._obligations.values()})

    def by_article(self, article):
        return sorted((o for o in self._obligations.values() if o.article == article),
                      key=lambda o: o.ob_id)

    def __len__(self):
        return len(self._obligations)
