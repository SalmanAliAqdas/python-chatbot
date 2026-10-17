"""Version 2 of the offline, rule-based RumiWare chatbot."""

import json
import re
from difflib import SequenceMatcher
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple

BOT_NAME = "RumiBot"
EXIT_WORDS = {"bye", "exit", "quit"}
KNOWLEDGE_BASE_PATH = Path(__file__).with_name("knowledge_base.json")
FALLBACK = ("I'm sorry, I don't understand that question confidently. I won't guess. "
            "Type 'help' to see the topics I can discuss.")


def normalize_message(message: str) -> str:
    """Return lowercase text with punctuation removed and spaces normalized."""
    return " ".join(re.findall(r"[a-z0-9]+", message.lower()))


def phrase_in_text(phrase: str, text: str) -> bool:
    """Match a complete word or phrase, never part of another word."""
    phrase = normalize_message(phrase)
    return bool(phrase and re.search(rf"\b{re.escape(phrase)}\b", text))


def load_knowledge_base(path: Path = KNOWLEDGE_BASE_PATH) -> Dict:
    """Load and perform basic validation on the JSON knowledge base."""
    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except (OSError, json.JSONDecodeError) as error:
        raise RuntimeError(f"Could not load knowledge base: {error}") from error
    if not isinstance(data.get("topics"), list) or not data["topics"]:
        raise RuntimeError("The knowledge base must contain a non-empty topics list.")
    return data


class Chatbot:
    """Match messages to FAQ topics and remember the last matched subject."""

    def __init__(self, knowledge_base: Optional[Dict] = None) -> None:
        self.knowledge_base = knowledge_base or load_knowledge_base()
        self.topics: List[Dict] = self.knowledge_base["topics"]
        self.previous_topic: Optional[Dict] = None

    def available_categories(self) -> List[str]:
        return list(dict.fromkeys(topic["category"] for topic in self.topics))

    def help_response(self) -> str:
        return "Available topics: " + ", ".join(self.available_categories()) + "."

    @staticmethod
    def _keyword_score(message: str, topic: Dict) -> float:
        groups = topic.get("keyword_groups", [])
        if groups and not all(any(phrase_in_text(term, message) for term in group)
                              for group in groups):
            return 0.0
        matches = [term for term in topic.get("keywords", [])
                   if phrase_in_text(term, message)]
        if not groups and len(matches) < topic.get("minimum_keywords", 1):
            return 0.0
        # Multi-word phrases carry more meaning than broad single words.
        specificity = sum(len(normalize_message(term).split()) for term in matches)
        return 40 + len(matches) * 8 + specificity * 8 + topic.get("priority", 0)

    @staticmethod
    def _phrase_score(message: str, topic: Dict) -> float:
        best = 0.0
        for phrase in [topic["question"], *topic.get("alternatives", [])]:
            phrase = normalize_message(phrase)
            if message == phrase:
                best = max(best, 120 + len(phrase.split()))
            elif len(phrase.split()) >= 2 and phrase_in_text(phrase, message):
                # A phrase embedded in a longer question is useful evidence, but
                # should not overpower a more specific keyword phrase.
                best = max(best, 55 + len(phrase.split()))
        return best + topic.get("priority", 0) if best else 0.0

    @staticmethod
    def _fuzzy_score(message: str, topic: Dict) -> float:
        if len(message) < 5:
            return 0.0
        ratio = max(SequenceMatcher(None, message, normalize_message(phrase)).ratio()
                    for phrase in [topic["question"], *topic.get("alternatives", [])])
        return 70 + ratio * 20 + topic.get("priority", 0) if ratio >= 0.78 else 0.0

    def _find_topic(self, message: str) -> Optional[Dict]:
        scored: List[Tuple[float, Dict]] = []
        for topic in self.topics:
            score = max(self._phrase_score(message, topic),
                        self._keyword_score(message, topic),
                        self._fuzzy_score(message, topic))
            if score:
                scored.append((score, topic))
        return max(scored, key=lambda item: item[0])[1] if scored else None

    def _context_response(self, message: str) -> Optional[str]:
        if self.previous_topic is None:
            return None
        if message in {"tell me more", "more information", "can you explain more"}:
            return self.previous_topic["answer"]
        follow_ups = {"how long does it take": "timelines",
                      "what is the timeline": "timelines",
                      "how much does it cost": "pricing",
                      "what does it cost": "pricing",
                      "what about support": "customer_support"}
        target_id = follow_ups.get(message)
        if target_id:
            target = next(topic for topic in self.topics if topic["id"] == target_id)
            return f"For {self.previous_topic['label'].lower()}: {target['answer']}"
        return None

    def respond(self, message: str) -> str:
        normalized = normalize_message(message)
        if not normalized:
            return "Please type a message so I can help you."
        if normalized in EXIT_WORDS:
            return "Goodbye! Thank you for chatting with RumiWare."
        if normalized in {"help", "topics", "menu"}:
            return self.help_response()
        if normalized == "good morning":
            return "Good morning! How can I help you today?"
        if normalized in {"hello", "hi", "hey"} or normalized.startswith("hello "):
            return "Hello! How can I help you today?"
        if "your name" in normalized or normalized == "who are you":
            return f"My name is {BOT_NAME}, RumiWare's friendly rule-based chatbot."
        if normalized in {"what can you do", "how can you help"}:
            return self.help_response()
        contextual = self._context_response(normalized)
        if contextual:
            return contextual
        topic = self._find_topic(normalized)
        if topic:
            self.previous_topic = topic
            return topic["answer"]
        return FALLBACK


def get_response(message: str) -> str:
    """Version 1-compatible response helper without persistent context."""
    return Chatbot().respond(message)


def run_chatbot(input_func: Callable[[str], str] = input,
                output_func: Callable[[str], None] = print) -> None:
    bot = Chatbot()
    output_func(f"{BOT_NAME}: Hello! Welcome to RumiWare.")
    output_func(f"{BOT_NAME}: Ask about our services, type help for topics, or bye to exit.")
    while True:
        try:
            message = input_func("You: ")
        except (EOFError, KeyboardInterrupt):
            output_func(f"\n{BOT_NAME}: Goodbye! Thank you for chatting with RumiWare.")
            break
        output_func(f"{BOT_NAME}: {bot.respond(message)}")
        if normalize_message(message) in EXIT_WORDS:
            break


def main() -> None:
    try:
        run_chatbot()
    except RuntimeError as error:
        print(f"{BOT_NAME}: {error}")


if __name__ == "__main__":
    main()
