# Copyright (c) The OGX Contributors.
# All rights reserved.
#
# This source code is licensed under the terms described in the LICENSE file in
# the root directory of this source tree.

"""Containment scoring for short gold answers, plus the majority-answer baseline.

MultiHOP gold answers are short (median 1 word: Yes, No, an entity name), while the
file_search template makes replies several sentences long. SQuAD token-F1 then measures
reply length rather than correctness, so MultiHOP is scored by whether the normalized gold
answer appears, as whole tokens, in the normalized reply.

Containment accepts hedged replies (a reply of "Yes No" contains both), so every score is
reported next to the majority-answer baseline, which needs no retrieval and no generation.
"""

from __future__ import annotations

import re
import string
from collections import Counter

_CITATION_RE = re.compile(r"<\|[^|>]*\|>")
_ARTICLES_RE = re.compile(r"\b(a|an|the)\b")
_PUNCTUATION = frozenset(string.punctuation)


def normalize_answer(text: str) -> list[str]:
    """SQuAD-style normalization (lowercase, no punctuation or articles), as tokens.

    Unlike SQuAD, punctuation becomes a space rather than being deleted, so "Bankman-Fried"
    and "Bankman Fried" match. Citation markers such as ``<|file-abc|>`` are dropped first so
    file ids cannot match.
    """
    text = _CITATION_RE.sub(" ", text).lower()
    text = "".join(" " if ch in _PUNCTUATION else ch for ch in text)
    return _ARTICLES_RE.sub(" ", text).split()


def contains_answer(prediction: str, gold: str | list[str]) -> bool:
    """Whether any gold answer appears in the prediction as a contiguous run of whole tokens."""
    golds = gold if isinstance(gold, list) else [gold]
    pred_tokens = normalize_answer(prediction)
    for answer in golds:
        gold_tokens = normalize_answer(answer)
        if not gold_tokens:
            continue
        width = len(gold_tokens)
        if any(pred_tokens[i : i + width] == gold_tokens for i in range(len(pred_tokens) - width + 1)):
            return True
    return False


def containment_accuracy(predictions: dict[str, str], ground_truths: dict[str, str | list[str]]) -> float:
    """Fraction of queries, among those present in both dicts, whose reply contains the gold answer."""
    common_qids = set(predictions) & set(ground_truths)
    if not common_qids:
        return 0.0
    hits = sum(contains_answer(predictions[qid], ground_truths[qid]) for qid in common_qids)
    return hits / len(common_qids)


def majority_answer_baseline(ground_truths: dict[str, str | list[str]]) -> tuple[str, float]:
    """The most common gold answer and the containment score of replying with it to every query."""
    counts: Counter[str] = Counter()
    representative: dict[str, str] = {}
    for gold in ground_truths.values():
        answer = gold[0] if isinstance(gold, list) else gold
        key = " ".join(normalize_answer(answer))
        counts[key] += 1
        representative.setdefault(key, answer)
    if not counts:
        return "", 0.0
    key = counts.most_common(1)[0][0]
    answer = representative[key]
    return answer, containment_accuracy(dict.fromkeys(ground_truths, answer), ground_truths)


def baseline_warning(metrics: dict) -> str | None:
    """Warning for a MultiHOP run that does not clear the majority-answer baseline, else None."""
    if "containment" not in metrics:
        return (
            "scored with SQuAD token-F1 only, which is dominated by reply length on MultiHOP "
            "and cannot rank systems; re-run to get containment and the majority baseline"
        )
    baseline = metrics.get("majority_baseline")
    if baseline is None:
        return "no majority-answer baseline recorded; re-run to get one"
    if metrics["containment"] <= baseline:
        return (
            f"containment {metrics['containment']:.4f} does not beat the majority-answer baseline "
            f"{baseline:.4f} (always replying {metrics.get('majority_answer', '?')!r})"
        )
    return None
