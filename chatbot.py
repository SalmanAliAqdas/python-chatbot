"""A beginner-friendly, rule-based chatbot for RumiWare."""

import re
from typing import Callable


BOT_NAME = "RumiBot"
EXIT_WORDS = {"bye", "exit", "quit"}


def normalize_message(message: str) -> str:
    """Return lowercase text with punctuation removed and spaces normalized."""
    words = re.findall(r"[a-z0-9]+", message.lower())
    return " ".join(words)


def get_response(message: str) -> str:
    """Return a response selected from simple, readable rules."""
    normalized = normalize_message(message)

    if not normalized:
        return "Please type a message so I can help you."

    words = set(normalized.split())

    if normalized in EXIT_WORDS:
        return "Goodbye! Thank you for chatting with RumiWare."

    if "good morning" in normalized:
        return "Good morning! How can I help you today?"

    if words.intersection({"hello", "hi", "hey"}):
        return "Hello! How can I help you today?"

    if "your name" in normalized or "who are you" in normalized:
        return f"My name is {BOT_NAME}, RumiWare's friendly rule-based chatbot."

    if "what can you do" in normalized or "how can you help" in normalized:
        return (
            "I can tell you about RumiWare and its website development, "
            "mobile application, AI automation, and software development services."
        )

    if "rumiware" in normalized or "company" in words:
        return (
            "RumiWare is a software development company that creates websites, "
            "mobile applications, AI automations, and custom software solutions."
        )

    if words.intersection({"website", "websites"}) or "web development" in normalized:
        return (
            "RumiWare develops modern, responsive websites tailored to business needs."
        )

    if words.intersection({"mobile", "app", "apps", "application", "applications"}):
        return (
            "RumiWare builds user-friendly mobile applications for practical "
            "business and customer needs."
        )

    if "ai" in words or "automation" in words:
        return (
            "RumiWare provides AI automation solutions that help businesses "
            "streamline repetitive tasks and improve efficiency."
        )

    if "software" in words or "services" in words:
        return (
            "RumiWare offers custom software development services, from planning "
            "and design through implementation and support."
        )

    return (
        "I'm sorry, I don't understand that question yet. Please ask me about "
        "RumiWare or its software services."
    )


def run_chatbot(
    input_func: Callable[[str], str] = input,
    output_func: Callable[[str], None] = print,
) -> None:
    """Run the chatbot until the user exits or the input stream closes."""
    output_func(f"{BOT_NAME}: Hello! Welcome to RumiWare.")
    output_func(f"{BOT_NAME}: Ask me about our services, or type bye to exit.")

    while True:
        try:
            message = input_func("You: ")
        except (EOFError, KeyboardInterrupt):
            output_func(f"\n{BOT_NAME}: Goodbye! Thank you for chatting with RumiWare.")
            break

        response = get_response(message)
        output_func(f"{BOT_NAME}: {response}")

        if normalize_message(message) in EXIT_WORDS:
            break


def main() -> None:
    """Start the command-line application."""
    run_chatbot()


if __name__ == "__main__":
    main()
