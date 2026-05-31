from datetime import datetime, timedelta, timezone

from context_router.context.context_types import ContextItem
from context_router.scoring.importance import importance_score
from context_router.scoring.recency import recency_score
from context_router.scoring.relevance import HashingEmbeddingModel, relevance_scores


def test_importance_score_normalized():
    item = ContextItem("1", "important", datetime.now(timezone.utc), "personal", 0.8)
    assert importance_score(item) == 0.8


def test_recency_score_recent_higher_than_old():
    now = datetime.now(timezone.utc)
    recent = ContextItem("r", "recent", now - timedelta(hours=1), "personal")
    old = ContextItem("o", "old", now - timedelta(hours=100), "personal")
    assert recency_score(recent, now=now) > recency_score(old, now=now)


def test_recency_score_half_life():
    now = datetime.now(timezone.utc)
    item = ContextItem("h", "half", now - timedelta(hours=72), "personal")
    assert 0.49 < recency_score(item, now=now, half_life_hours=72) < 0.51


def test_relevance_scores_match_related_text():
    model = HashingEmbeddingModel()
    scores = relevance_scores("docker build", ["docker build failed", "greece hotel"], model)
    assert scores[0] > scores[1]
