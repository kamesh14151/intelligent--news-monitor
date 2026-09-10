import sys
sys.path.insert(0, "backend")

from app.schemas.news import ImpactResult, StorySummary, ValidationResult


def test_validation_contract():
    result = ValidationResult(
        relevant=True,
        relevance_score=0.9,
        reason="Direct evidence",
        topics=["AI"],
        geography="Global",
    )
    assert 0 <= result.relevance_score <= 1


def test_impact_contract():
    result = ImpactResult(
        business_impact=8,
        urgency=7,
        market_impact=6,
        novelty=9,
        confidence=0.9,
    )
    assert all(0 <= x <= 10 for x in [result.business_impact, result.urgency, result.market_impact, result.novelty])
    assert 0 <= result.confidence <= 1


def test_summary_contract():
    result = StorySummary(
        headline="Example story",
        summary="Example summary.",
        key_points=["Point 1"],
        impact="Example impact.",
        what_to_watch=["Follow-up"],
    )
    assert result.headline
    assert result.summary
