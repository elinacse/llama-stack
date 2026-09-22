# Copyright (c) The OGX Contributors.
# All rights reserved.
#
# This source code is licensed under the terms described in the LICENSE file in
# the root directory of this source tree.


from ogx.log import get_logger
from ogx.providers.remote.inference.llama_cpp_server.config import LlamaCppServerConfig
from ogx.providers.utils.inference.models_dev_registry import lookup_models_dev
from ogx.providers.utils.inference.openai_mixin import OpenAIMixin
from ogx_api import Model, ModelType

log = get_logger(name=__name__, category="inference::llama_cpp_server")


class LlamaCppServerInferenceAdapter(OpenAIMixin):
    """Inference adapter for llama.cpp servers with an OpenAI-compatible API."""

    config: LlamaCppServerConfig

    def get_api_key(self) -> str | None:
        if self.config.auth_credential is None:
            return "NO KEY REQUIRED"
        return self.config.auth_credential.get_secret_value()

    def get_base_url(self) -> str:
        return str(self.config.base_url)

    def construct_model_from_identifier(self, identifier: str) -> Model:
        # llama.cpp's /v1/models response does not expose a model task/type field
        # (a router can serve llm and embedding models on one endpoint), so we
        # classify with models.dev with a name fallback, mirroring the vLLM adapter.
        md = lookup_models_dev(identifier)
        is_embedding = md is not None or "embed" in identifier.lower()

        if is_embedding:
            metadata: dict[str, int] = {}
            if md is not None:
                if md.limit.output:
                    metadata["embedding_dimension"] = md.limit.output
                if md.limit.context:
                    metadata["context_length"] = md.limit.context
                log.debug(
                    "Classified embedding model via models.dev",
                    identifier=identifier,
                    family=md.family,
                    metadata=metadata,
                )
            else:
                log.debug(
                    "Classified embedding model via name heuristic (not in models.dev)",
                    identifier=identifier,
                )
            return Model(
                provider_id=self.__provider_id__,
                provider_resource_id=identifier,
                identifier=identifier,
                model_type=ModelType.embedding,
                metadata=metadata,
            )
        if "rerank" in identifier.lower():
            return Model(
                provider_id=self.__provider_id__,
                provider_resource_id=identifier,
                identifier=identifier,
                model_type=ModelType.rerank,
            )
        return super().construct_model_from_identifier(identifier)
