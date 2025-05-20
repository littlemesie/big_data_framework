# -*- coding:utf-8 -*-

"""
@date: 2025/5/20 上午10:44
@summary: 重写onnx_mini_lm_l6_v2
"""
import importlib
import logging
import os
from functools import cached_property
from typing import List, Dict, Any, Optional, cast

import numpy as np
import numpy.typing as npt
from tenacity import retry, retry_if_exception, stop_after_attempt, wait_random

from chromadb.api.types import Documents, Embeddings, EmbeddingFunction, Space
from chromadb.utils.embedding_functions.schemas import validate_config_schema

logger = logging.getLogger(__name__)



# In order to remove dependencies on sentence-transformers, which in turn depends on
# pytorch and sentence-piece we have created a default ONNX embedding function that
# implements the same functionality as "all-MiniLM-L6-v2" from sentence-transformers.
# visit https://github.com/chroma-core/onnx-embedding for the source code to generate
# and verify the ONNX model.
class ONNXMiniLM_L6_V2(EmbeddingFunction[Documents]):

    def __init__(self, model_path: str, preferred_providers: Optional[List[str]] = None) -> None:
        """
        Initialize the ONNXMiniLM_L6_V2 embedding function.

        Args:
            preferred_providers (List[str], optional): The preferred ONNX runtime providers.
                Defaults to None.
        """
        self.model_path = model_path
        # convert the list to set for unique values
        if preferred_providers and not all(
            [isinstance(i, str) for i in preferred_providers]
        ):
            raise ValueError("Preferred providers must be a list of strings")
        # check for duplicate providers
        if preferred_providers and len(preferred_providers) != len(
            set(preferred_providers)
        ):
            raise ValueError("Preferred providers must be unique")

        self._preferred_providers = preferred_providers

        try:
            # Equivalent to import onnxruntime
            self.ort = importlib.import_module("onnxruntime")
        except ImportError:
            raise ValueError(
                "The onnxruntime python package is not installed. Please install it with `pip install onnxruntime`"
            )
        try:
            # Equivalent to from tokenizers import Tokenizer
            self.Tokenizer = importlib.import_module("tokenizers").Tokenizer
        except ImportError:
            raise ValueError(
                "The tokenizers python package is not installed. Please install it with `pip install tokenizers`"
            )
        try:
            # Equivalent to from tqdm import tqdm
            self.tqdm = importlib.import_module("tqdm").tqdm
        except ImportError:
            raise ValueError(
                "The tqdm python package is not installed. Please install it with `pip install tqdm`"
            )

    # Borrowed from https://gist.github.com/yanqd0/c13ed29e29432e3cf3e7c38467f42f51
    # Download with tqdm to preserve the sentence-transformers experience
    @retry(  # type: ignore
        reraise=True,
        stop=stop_after_attempt(3),
        wait=wait_random(min=1, max=3),
        retry=retry_if_exception(lambda e: "does not match expected SHA256" in str(e)),
    )

    # Use pytorches default epsilon for division by zero
    # https://pytorch.org/docs/stable/generated/torch.nn.functional.normalize.html
    def _normalize(self, v: npt.NDArray[np.float32]) -> npt.NDArray[np.float32]:
        """
        Normalize a vector.

        Args:
            v: The vector to normalize.

        Returns:
            The normalized vector.
        """
        norm = np.linalg.norm(v, axis=1)
        # Handle division by zero
        norm[norm == 0] = 1e-12
        return cast(npt.NDArray[np.float32], v / norm[:, np.newaxis])

    def _forward(
        self, documents: List[str], batch_size: int = 32
    ) -> npt.NDArray[np.float32]:
        """
        Generate embeddings for a list of documents.

        Args:
            documents: The documents to generate embeddings for.
            batch_size: The batch size to use when generating embeddings.

        Returns:
            The embeddings for the documents.
        """
        all_embeddings = []
        for i in range(0, len(documents), batch_size):
            batch = documents[i : i + batch_size]

            # Encode each document separately
            encoded = [self.tokenizer.encode(d) for d in batch]

            # Check if any document exceeds the max tokens
            for doc_tokens in encoded:
                if len(doc_tokens.ids) > self.max_tokens():
                    raise ValueError(
                        f"Document length {len(doc_tokens.ids)} is greater than the max tokens {self.max_tokens()}"
                    )

            input_ids = np.array([e.ids for e in encoded])
            attention_mask = np.array([e.attention_mask for e in encoded])

            onnx_input = {
                "input_ids": np.array(input_ids, dtype=np.int64),
                "attention_mask": np.array(attention_mask, dtype=np.int64),
                "token_type_ids": np.array(
                    [np.zeros(len(e), dtype=np.int64) for e in input_ids],
                    dtype=np.int64,
                ),
            }

            model_output = self.model.run(None, onnx_input)
            last_hidden_state = model_output[0]

            # Perform mean pooling with attention weighting
            input_mask_expanded = np.broadcast_to(
                np.expand_dims(attention_mask, -1), last_hidden_state.shape
            )
            embeddings = np.sum(last_hidden_state * input_mask_expanded, 1) / np.clip(
                input_mask_expanded.sum(1), a_min=1e-9, a_max=None
            )

            embeddings = self._normalize(embeddings).astype(np.float32)
            all_embeddings.append(embeddings)

        return np.concatenate(all_embeddings)

    @cached_property
    def tokenizer(self) -> Any:
        """
        Get the tokenizer for the model.

        Returns:
            The tokenizer for the model.
        """
        tokenizer = self.Tokenizer.from_file(
            os.path.join(
                self.model_path, "tokenizer.json"
            )
        )
        # max_seq_length = 256, for some reason sentence-transformers uses 256 even though the HF config has a max length of 128
        # https://github.com/UKPLab/sentence-transformers/blob/3e1929fddef16df94f8bc6e3b10598a98f46e62d/docs/_static/html/models_en_sentence_embeddings.html#LL480
        tokenizer.enable_truncation(max_length=256)
        tokenizer.enable_padding(pad_id=0, pad_token="[PAD]", length=256)
        return tokenizer

    @cached_property
    def model(self) -> Any:
        """
        Get the model.

        Returns:
            The model.
        """
        if self._preferred_providers is None or len(self._preferred_providers) == 0:
            if len(self.ort.get_available_providers()) > 0:
                logger.debug(
                    f"WARNING: No ONNX providers provided, defaulting to available providers: "
                    f"{self.ort.get_available_providers()}"
                )
            self._preferred_providers = self.ort.get_available_providers()
        elif not set(self._preferred_providers).issubset(
            set(self.ort.get_available_providers())
        ):
            raise ValueError(
                f"Preferred providers must be subset of available providers: {self.ort.get_available_providers()}"
            )

        # Suppress onnxruntime warnings
        so = self.ort.SessionOptions()
        so.log_severity_level = 3
        so.graph_optimization_level = self.ort.GraphOptimizationLevel.ORT_ENABLE_ALL

        return self.ort.InferenceSession(
            os.path.join(self.model_path, "model.onnx"),
            # Since 1.9 onnyx runtime requires providers to be specified when there are multiple available
            providers=self._preferred_providers,
            sess_options=so,
        )

    def __call__(self, input: Documents) -> Embeddings:
        """
        Generate embeddings for the given documents.

        Args:
            input: Documents to generate embeddings for.

        Returns:
            Embeddings for the documents.
        """

        # Generate embeddings
        embeddings = self._forward(input)

        # Convert to list of numpy arrays for the expected Embeddings type
        return cast(
            Embeddings,
            [np.array(embedding, dtype=np.float32) for embedding in embeddings],
        )

    @staticmethod
    def name() -> str:
        return "onnx_mini_lm_l6_v2"

    def default_space(self) -> Space:
        return "cosine"

    def supported_spaces(self) -> List[Space]:
        return ["cosine", "l2", "ip"]

    def max_tokens(self) -> int:
        # Default token limit for ONNX Mini LM L6 V2 model
        return 256

    @staticmethod
    def build_from_config(config: Dict[str, Any]) -> "EmbeddingFunction[Documents]":
        preferred_providers = config.get("preferred_providers")

        return ONNXMiniLM_L6_V2(preferred_providers=preferred_providers)

    def get_config(self) -> Dict[str, Any]:
        return {"preferred_providers": self._preferred_providers}

    def validate_config_update(
        self, old_config: Dict[str, Any], new_config: Dict[str, Any]
    ) -> None:
        # Preferred providers can be changed, so no validation needed
        pass

    @staticmethod
    def validate_config(config: Dict[str, Any]) -> None:
        """
        Validate the configuration using the JSON schema.

        Args:
            config: Configuration to validate

        Raises:
            ValidationError: If the configuration does not match the schema
        """
        validate_config_schema(config, "onnx_mini_lm_l6_v2")


# model_path = '/media/mesie/a1d6502f-8a4a-4017-a9b5-3777bd223927/model/vanna/chroma/onnx_models/all-MiniLM-L6-v2/onnx'
# text = "查询2021年1月份人员总数"
# embedding_function = ONNXMiniLM_L6_V2(model_path=model_path)
# print(embedding_function([text][0]))