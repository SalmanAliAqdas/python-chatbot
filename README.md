# Simple Python Chatbot — Version 2

Simple Python Chatbot is a beginner-friendly, offline, rule-based terminal application for answering questions about RumiWare and common software-service topics. It demonstrates JSON data loading, text normalization, ranked rule matching, fuzzy matching, conversation context, error handling, and automated testing with only the Python standard library.

The chatbot does not use artificial intelligence, machine learning, external APIs, databases, API keys, or paid services.

## Features

- Greets users and keeps chatting until `bye`, `exit`, or `quit`
- Loads questions, answers, keywords, and alternative phrasings from `knowledge_base.json`
- Includes more than 30 FAQ topics across 17 categories
- Matches input without regard to uppercase, lowercase, or punctuation
- Uses complete word and phrase boundaries to avoid partial-word matches
- Ranks specific phrases and keyword combinations above broad keywords
- Uses conservative fuzzy matching for minor typing mistakes
- Remembers the previous topic for simple follow-up questions
- Shows available categories with `help`, `topics`, or `menu`
- Avoids guessing when a question cannot be matched confidently
- Handles empty input, closed input streams, and `Ctrl+C` safely
- Keeps unconfirmed service descriptions clearly illustrative

## Knowledge Categories

- Company information
- Website development
- E-commerce websites
- WordPress
- Mobile applications
- SaaS development
- Custom software
- AI automation
- Chatbots
- Digital marketing
- SEO
- Hosting and domains
- Website maintenance
- Project timelines
- Pricing inquiries
- Customer support
- Contact inquiries

## Requirements

- Python 3.8 or newer
- A terminal such as the Visual Studio Code integrated terminal

No packages need to be installed, so this project does not require a `requirements.txt` file.

## Installation

1. Download or clone the repository.
2. Open the project folder in Visual Studio Code.
3. Check the installed Python version:

   ```powershell
   python --version
   ```

## Usage

Run the application from the project folder:

```powershell
python chatbot.py
```

Useful commands:

| Command | Action |
|---|---|
| `help`, `topics`, or `menu` | Display available categories |
| `bye`, `exit`, or `quit` | End the conversation |

## Example

```text
RumiBot: Hello! Welcome to RumiWare.
RumiBot: Ask about our services, type help for topics, or bye to exit.
You: Can you build an online shop?
RumiBot: An e-commerce website can present products, manage carts, and support ordering. This is general guidance; confirm e-commerce services with RumiWare.
You: How long does it take?
RumiBot: For e-commerce websites: Timelines depend on scope, complexity, content, feedback, and testing. RumiWare needs project details before providing an estimate.
You: quit
RumiBot: Goodbye! Thank you for chatting with RumiWare.
```

## Adding a Knowledge-Base Topic

Open `knowledge_base.json` and add an object to the `topics` array. Each topic uses this structure:

```json
{
  "id": "unique_topic_id",
  "label": "Readable topic name",
  "category": "Category name",
  "question": "Primary question?",
  "alternatives": [
    "Another way to ask",
    "A second alternative"
  ],
  "keywords": [
    "distinctive phrase",
    "another keyword"
  ],
  "priority": 0,
  "answer": "The response shown to the user."
}
```

The `id`, `label`, `category`, `question`, `alternatives`, `keywords`, and `answer` fields should be provided. `priority` is optional and should be used sparingly to resolve a known conflict in favor of a more specific topic. An optional `minimum_keywords` value can require multiple listed keywords before a keyword match is accepted.

Use distinctive multi-word keywords where possible. Keep answers factual, avoid unverified prices, guarantees, or contact information, and identify unconfirmed services as illustrative. Preserve valid JSON by placing a comma between adjacent topic objects.

After editing the knowledge base, run the tests and try the new primary question, each alternative, and an unrelated question.

## Testing

Run all automated tests from the project folder:

```powershell
python -m unittest discover -s tests -v
```

The suite covers original chatbot behavior, known questions, alternative phrasings, capitalization, punctuation, typing mistakes, word boundaries, conflicting keywords, follow-up context, help output, empty input, unknown questions, exit commands, and clean terminal shutdown.

## Project Structure

```text
simple-python-chatbot/
|-- chatbot.py
|-- knowledge_base.json
|-- README.md
|-- .gitignore
`-- tests/
    |-- __init__.py
    `-- test_chatbot.py
```

## How Matching Works

The chatbot normalizes each message and ranks possible FAQ matches. Exact questions and known alternative phrasings receive the strongest scores, followed by complete keyword or phrase matches. Conservative similarity matching handles small typos. When no candidate reaches a safe threshold, the chatbot displays a fallback instead of guessing.

Conversation context is held in memory only for the current run. Short follow-ups such as `tell me more`, `how long does it take`, and `how much does it cost` can refer to the previously matched topic.
