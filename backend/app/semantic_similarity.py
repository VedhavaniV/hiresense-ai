from __future__ import annotations

import math
import re
from collections import Counter


STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "in",
    "is",
    "of",
    "on",
    "or",
    "the",
    "to",
    "with",
    "we",
}


def tokenize(text: str) -> list[str]:
    tokens = re.findall(r"[a-zA-Z][a-zA-Z0-9+#.-]*", text.lower())
    return [token for token in tokens if token not in STOP_WORDS and len(token) > 1]


def cosine_similarity(first_text: str, second_text: str) -> float:
    first_counts = Counter(tokenize(first_text))
    second_counts = Counter(tokenize(second_text))

    if not first_counts or not second_counts:
        return 0.0

    vocabulary = set(first_counts).union(second_counts)
    dot_product = sum(first_counts[token] * second_counts[token] for token in vocabulary)
    first_norm = math.sqrt(sum(count * count for count in first_counts.values()))
    second_norm = math.sqrt(sum(count * count for count in second_counts.values()))

    if first_norm == 0 or second_norm == 0:
        return 0.0

    return dot_product / (first_norm * second_norm)


def semantic_similarity_score(first_text: str, second_text: str) -> int:
    return round(cosine_similarity(first_text, second_text) * 100)

