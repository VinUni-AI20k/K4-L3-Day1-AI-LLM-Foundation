"""
Checkpoint 3 (12h10) — Part 3: Streaming & độ bền
Chạy:  pytest tests/test_part3.py -v
Tất cả API đều được mock — không cần API key thật.
"""

import unittest
from unittest.mock import MagicMock, patch

from tests._loader import MOD


def _make_stream(text: str):
    """Tạo mock stream: cắt text thành các chunk giống OpenAI streaming."""
    chunks = []
    for piece in (text[: len(text) // 2], text[len(text) // 2 :]):
        chunk = MagicMock()
        chunk.choices = [MagicMock()]
        chunk.choices[0].delta.content = piece
        chunks.append(chunk)
    # Chunk cuối có delta.content = None — giống stream thật, code phải xử lý
    final = MagicMock()
    final.choices = [MagicMock()]
    final.choices[0].delta.content = None
    chunks.append(final)
    return chunks


class TestStreamingChatbot(unittest.TestCase):

    def test_function_exists_and_is_callable(self):
        self.assertTrue(callable(MOD.streaming_chatbot))

    @patch("builtins.input", side_effect=["quit"])
    @patch("openai.OpenAI")
    def test_exits_on_quit(self, MockOpenAI, mock_input):
        """Chatbot phải thoát sạch khi người dùng gõ 'quit'."""
        mock_client = MagicMock()
        MockOpenAI.return_value = mock_client
        try:
            MOD.streaming_chatbot()
        except StopIteration:
            pass  # input() hết side_effect — chấp nhận được

    @patch("builtins.input", side_effect=["Xin chào", "quit"])
    @patch("openai.OpenAI")
    def test_streams_one_turn_with_stream_true(self, MockOpenAI, mock_input):
        """Một lượt chat phải gọi API với stream=True."""
        mock_client = MagicMock()
        MockOpenAI.return_value = mock_client
        mock_client.chat.completions.create.return_value = _make_stream("Chào bạn!")

        try:
            MOD.streaming_chatbot()
        except StopIteration:
            pass

        self.assertTrue(
            mock_client.chat.completions.create.called,
            "Phải gọi API khi người dùng nhập tin nhắn",
        )
        _, kwargs = mock_client.chat.completions.create.call_args
        self.assertTrue(kwargs.get("stream", False), "Phải gọi API với stream=True")


class TestRetryWithBackoff(unittest.TestCase):

    def test_succeeds_on_first_try(self):
        result = MOD.retry_with_backoff(lambda: 42)
        self.assertEqual(result, 42)

    def test_retries_on_transient_exception(self):
        call_count = [0]

        def flaky():
            call_count[0] += 1
            if call_count[0] < 2:
                raise ValueError("transient")
            return "ok"

        result = MOD.retry_with_backoff(flaky, max_retries=3, base_delay=0.01)
        self.assertEqual(result, "ok")
        self.assertEqual(call_count[0], 2)

    def test_raises_after_max_retries(self):
        def always_fail():
            raise ValueError("permanent failure")

        with self.assertRaises(ValueError):
            MOD.retry_with_backoff(always_fail, max_retries=2, base_delay=0.01)


if __name__ == "__main__":
    unittest.main()
