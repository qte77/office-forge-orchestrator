"""Tests for embedding wrapper."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import numpy as np

from doc_memory.embed.embedder import Embedder


class TestEmbedder:
    def test_encode_returns_ndarray(self) -> None:
        mock_model = MagicMock()
        mock_model.encode.return_value = np.array([[0.1, 0.2, 0.3]])

        with patch(
            "doc_memory.embed.embedder.SentenceTransformer", return_value=mock_model
        ):
            embedder = Embedder(model_name="test-model")
            result = embedder.encode(["hello"])

        assert isinstance(result, np.ndarray)
        assert result.shape == (1, 3)

    def test_encode_multiple_texts(self) -> None:
        mock_model = MagicMock()
        mock_model.encode.return_value = np.array(
            [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]
        )

        with patch(
            "doc_memory.embed.embedder.SentenceTransformer", return_value=mock_model
        ):
            embedder = Embedder(model_name="test-model")
            result = embedder.encode(["hello", "world"])

        assert result.shape == (2, 3)

    def test_default_model_name(self) -> None:
        with patch("doc_memory.embed.embedder.SentenceTransformer") as mock_st:
            Embedder()
            mock_st.assert_called_once_with("all-MiniLM-L6-v2")
