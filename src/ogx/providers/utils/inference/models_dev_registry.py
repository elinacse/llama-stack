# Copyright (c) The OGX Contributors.
# All rights reserved.
#
# This source code is licensed under the terms described in the LICENSE file in
# the root directory of this source tree.

"""Shared models.dev lookup for remote adapters whose /v1/models response has no
model task/type field, so embedding (and potentially other) models can't be told
apart from the identifier alone. Providers that serve arbitrary upstream model IDs
(vLLM, llama.cpp servers, etc.) can use this to classify by the models.dev registry
first, falling back to a name heuristic only for models it doesn't know about.
"""

from functools import cache

import models_dev as _models_dev


def is_embedding_model(model_id: str, model: _models_dev.Model) -> bool:
    """True if models.dev or the identifier itself marks this as an embedding model."""
    return (model.family is not None and "embed" in model.family) or "embed" in model_id.lower()


@cache
def models_dev_index() -> dict[str, _models_dev.Model]:
    """Index of models.dev embedding models by model ID, across all providers.

    Sorted so the huggingface provider entry is processed last: adapters that serve
    Hugging Face model IDs directly (vLLM, llama.cpp GGUF repos, etc.) find it the
    most authoritative source for those IDs, so it wins on conflicting entries.
    """
    index: dict[str, _models_dev.Model] = {}
    for provider in sorted(_models_dev.providers(), key=lambda p: p.id == "huggingface"):
        for model_id, model in provider.models.items():
            if is_embedding_model(model_id, model):
                index[model_id] = model
    return index


def lookup_models_dev(identifier: str) -> _models_dev.Model | None:
    """Look up ``identifier`` in the models.dev embedding-model index, if present."""
    return models_dev_index().get(identifier)
