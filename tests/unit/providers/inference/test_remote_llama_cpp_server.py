# Copyright (c) The OGX Contributors.
# All rights reserved.
#
# This source code is licensed under the terms described in the LICENSE file in
# the root directory of this source tree.

from ogx.providers.remote.inference.llama_cpp_server.config import LlamaCppServerConfig
from ogx.providers.remote.inference.llama_cpp_server.llama_cpp_server import (
    LlamaCppServerInferenceAdapter,
)
from ogx_api import ModelType


class TestConstructModelFromIdentifier:
    """LlamaCppServerInferenceAdapter.construct_model_from_identifier must classify via
    models.dev with a name-heuristic fallback, mirroring the vLLM adapter (#6610)."""

    def _make_adapter(self) -> LlamaCppServerInferenceAdapter:
        config = LlamaCppServerConfig(base_url="http://mocked.localhost:8080/v1")
        adapter = LlamaCppServerInferenceAdapter(config=config)
        adapter.__provider_id__ = "llama-cpp-server"
        return adapter

    def test_family_check_classifies_embedding_without_embed_in_identifier(self):
        # intfloat/multilingual-e5-large-instruct has no "embed" in its identifier
        # but its models.dev family is "text-embedding", so it must be classified
        # as an embedding model with metadata populated from models.dev.
        adapter = self._make_adapter()
        model = adapter.construct_model_from_identifier("intfloat/multilingual-e5-large-instruct")

        assert model.model_type == ModelType.embedding
        assert model.metadata.get("embedding_dimension") == 512

    def test_known_embedding_model_populates_metadata_from_models_dev(self):
        # text-embedding-3-large is in models_dev (openai provider) with
        # limit.output=3072 (embedding dimension) and limit.context=8191.
        adapter = self._make_adapter()
        model = adapter.construct_model_from_identifier("text-embedding-3-large")

        assert model.model_type == ModelType.embedding
        assert model.metadata.get("embedding_dimension") == 3072
        assert model.metadata.get("context_length") == 8191

    def test_unknown_embedding_model_falls_back_to_name_heuristic(self):
        adapter = self._make_adapter()
        model = adapter.construct_model_from_identifier("acme/custom-embed-v1")

        assert model.model_type == ModelType.embedding
        assert model.metadata == {}

    def test_rerank_model_classified_correctly(self):
        adapter = self._make_adapter()
        model = adapter.construct_model_from_identifier("Qwen/Qwen3-Reranker-0.6B")

        assert model.model_type == ModelType.rerank

    def test_non_embedding_non_rerank_model_falls_through_to_default(self):
        adapter = self._make_adapter()
        model = adapter.construct_model_from_identifier("qwen3-0.6b")

        assert model.model_type == ModelType.llm
