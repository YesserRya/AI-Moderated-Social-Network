import unittest

from Mymedia.moderation import moderation_action


class ModerationActionTests(unittest.TestCase):
    def test_low_score_is_published(self):
        self.assertEqual(moderation_action(0.20), "publish")

    def test_intermediate_score_is_reviewed(self):
        self.assertEqual(moderation_action(0.65), "review")

    def test_high_score_is_rejected(self):
        self.assertEqual(moderation_action(0.95), "reject")

    def test_boundary_scores_are_reviewed(self):
        self.assertEqual(moderation_action(0.50), "review")
        self.assertEqual(moderation_action(0.80), "review")

    def test_invalid_probability_is_rejected(self):
        with self.assertRaises(ValueError):
            moderation_action(1.01)


if __name__ == "__main__":
    unittest.main()
