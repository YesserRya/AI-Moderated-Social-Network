"""Decision rules for routing posts after model inference."""

PUBLISH_THRESHOLD = 0.50
REJECT_THRESHOLD = 0.80


def moderation_action(hate_probability: float) -> str:
    """Return ``publish``, ``review``, or ``reject`` for a model score."""
    if not 0.0 <= hate_probability <= 1.0:
        raise ValueError("hate_probability must be between 0 and 1")
    if hate_probability < PUBLISH_THRESHOLD:
        return "publish"
    if hate_probability > REJECT_THRESHOLD:
        return "reject"
    return "review"
