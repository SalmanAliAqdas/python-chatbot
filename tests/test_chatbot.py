"""Tests for the chatbot's response rules and terminal loop."""

import unittest
from unittest.mock import Mock

from chatbot import get_response, normalize_message, run_chatbot


class ResponseTests(unittest.TestCase):
    def test_normalization_ignores_case_and_punctuation(self):
        self.assertEqual(normalize_message("  HELLO, World!  "), "hello world")

    def test_empty_input(self):
        self.assertIn("Please type", get_response("   "))

    def test_common_greetings_are_recognized(self):
        for greeting in ("hello", "HI", "Hey there", "Good Morning!"):
            with self.subTest(greeting=greeting):
                self.assertIn("help", get_response(greeting).lower())

    def test_name_question(self):
        self.assertIn("RumiBot", get_response("What is your name?"))

    def test_capabilities_question(self):
        response = get_response("WHAT CAN YOU DO?").lower()
        self.assertIn("website development", response)
        self.assertIn("ai automation", response)

    def test_rumiware_question(self):
        self.assertIn("software development company", get_response("What is RumiWare?"))

    def test_service_topics(self):
        topics = {
            "Do you create websites?": "responsive websites",
            "Tell me about mobile apps": "mobile applications",
            "Do you offer AI automation?": "streamline",
            "What software services are available?": "custom software",
        }
        for question, expected in topics.items():
            with self.subTest(question=question):
                self.assertIn(expected, get_response(question).lower())

    def test_unknown_question(self):
        self.assertIn("don't understand", get_response("What is the weather?"))

    def test_exit_words(self):
        for word in ("bye", "EXIT", "Quit!"):
            with self.subTest(word=word):
                self.assertIn("Goodbye", get_response(word))


class ChatLoopTests(unittest.TestCase):
    def test_loop_continues_until_exit(self):
        messages = iter(["", "hello", "quit"])
        output = Mock()

        run_chatbot(input_func=lambda _prompt: next(messages), output_func=output)

        rendered = "\n".join(call.args[0] for call in output.call_args_list)
        self.assertIn("Please type", rendered)
        self.assertIn("How can I help", rendered)
        self.assertIn("Goodbye", rendered)

    def test_eof_exits_cleanly(self):
        output = Mock()

        def closed_input(_prompt):
            raise EOFError

        run_chatbot(input_func=closed_input, output_func=output)
        self.assertIn("Goodbye", output.call_args_list[-1].args[0])


if __name__ == "__main__":
    unittest.main()
