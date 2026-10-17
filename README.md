# Simple Python Chatbot

Simple Python Chatbot is a beginner-friendly, rule-based terminal application. It demonstrates core Python concepts by matching user messages to predefined conversational responses about RumiWare and its software development services.

## Features

- Greets the user when the program starts
- Recognizes common greetings regardless of letter case
- Answers basic questions about its name and capabilities
- Describes RumiWare and its services
- Covers website development, mobile applications, AI automation, and custom software development
- Responds politely to empty or unknown input
- Continues chatting until the user enters `bye`, `exit`, or `quit`
- Exits cleanly when the terminal input closes or the user presses `Ctrl+C`
- Includes automated tests built with Python's standard `unittest` library

## Requirements

- Python 3.8 or newer
- A terminal, such as the integrated terminal in Visual Studio Code

The project uses only the Python standard library. No packages, API keys, databases, or external AI services are required.

## Installation

1. Download or clone the repository.
2. Open the project folder in Visual Studio Code.
3. Confirm that Python is installed:

   ```powershell
   python --version
   ```

No dependency installation is needed.

## Usage

From the project folder, run:

```powershell
python chatbot.py
```

Enter a message at the `You:` prompt. To end the conversation, enter `bye`, `exit`, or `quit`.

## Example

```text
RumiBot: Hello! Welcome to RumiWare.
RumiBot: Ask me about our services, or type bye to exit.
You: What can you do?
RumiBot: I can tell you about RumiWare and its website development, mobile application, AI automation, and software development services.
You: Tell me about websites
RumiBot: RumiWare develops modern, responsive websites tailored to business needs.
You: bye
RumiBot: Goodbye! Thank you for chatting with RumiWare.
```

## Testing

Run the complete automated test suite from the project folder:

```powershell
python -m unittest discover -s tests -v
```

The tests verify message normalization, greetings, service answers, unknown and empty input, exit commands, and clean terminal-loop behavior.

## Project Structure

```text
simple-python-chatbot/
|-- chatbot.py
|-- README.md
|-- .gitignore
`-- tests/
    |-- __init__.py
    `-- test_chatbot.py
```

## How It Works

The chatbot converts each message to lowercase, removes punctuation, and checks the resulting words and phrases against a small set of rules. The response logic is kept separate from the terminal loop so it is easy to read, extend, and test.
