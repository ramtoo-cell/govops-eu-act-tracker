
"""Tests for the EU AI Act obligation tracker."""
import unittest

from src.eu_act_tracker import EUActTracker, Obligation


def _tracker():
    t = EUActTracker()
    t.add(Obligation("O1", "Risk management system", "Art. 9",
                     ["high-risk"], "Establish a risk management system."))
    t.add(Obligation("O2", "Transparency notice", "Art. 50",
                     ["high-risk", "limited-risk"], "Inform users they face AI."))
    t.add(Obligation("O3", "Prohibition of social scoring", "Art. 5",
                     ["prohibited"], "Social scoring is banned."))
    return t


class TestEUActTracker(unittest.TestCase):
    def test_applicable(self):
        t = _tracker()
        self.assertEqual([o.ob_id for o in t.applicable("high-risk")], ["O1", "O2"])
        self.assertEqual([o.ob_id for o in t.applicable("limited-risk")], ["O2"])
        self.assertEqual(t.applicable("minimal-risk"), [])

    def test_verdict_prohibited(self):
        verdict = _tracker().verdict("prohibited")
        self.assertFalse(verdict["allowed"])
        self.assertIn("prohibited", verdict["reason"])

    def test_verdict_allowed(self):
        verdict = _tracker().verdict("high-risk")
        self.assertTrue(verdict["allowed"])
        self.assertEqual(verdict["obligations"], ["O1", "O2"])

    def test_assess_partial(self):
        result = _tracker().assess("high-risk", ["O1"])
        self.assertEqual(result["missing"], ["O2"])
        self.assertEqual(result["compliance_pct"], 0.5)
        self.assertFalse(result["compliant"])

    def test_assess_full(self):
        result = _tracker().assess("high-risk", ["O1", "O2"])
        self.assertTrue(result["compliant"])
        self.assertEqual(result["compliance_pct"], 1.0)

    def test_invalid_risk_class(self):
        with self.assertRaises(ValueError):
            _tracker().applicable("medium-risk")

    def test_bad_applies_to_rejected(self):
        t = EUActTracker()
        with self.assertRaises(ValueError):
            t.add(Obligation("OX", "bad", "Art. 1", ["medium-risk"]))

    def test_articles(self):
        self.assertEqual(_tracker().articles(), ["Art. 5", "Art. 50", "Art. 9"])
        self.assertEqual(len(_tracker().by_article("Art. 9")), 1)

    def test_duplicate_rejected(self):
        t = _tracker()
        with self.assertRaises(ValueError):
            t.add(Obligation("O1", "dup", "Art. 9", ["high-risk"]))


if __name__ == "__main__":
    unittest.main()
