# repo2llm 🚀

A fast CLI and Desktop utility that converts an entire code repository into a single LLM-ready prompt file.

repo2llm scans your project, filters unnecessary files, creates a readable repository structure, and exports your codebase in formats optimized for large-context AI models like ChatGPT and Claude.

---

## ✨ Features

### 🧠 LLM Optimized Output

Packages your repository into a clean, structured prompt format that helps AI models understand your project architecture.

### 📁 Smart Ignore System

Automatically respects `.gitignore` rules and removes unnecessary files such as:

* `.git`
* `node_modules`
* virtual environments
* caches
* dependency lock files
* generated outputs

### 🛡️ Safe File Filtering

Prevents unwanted files from entering your prompt:

* Binary file detection
* Image filtering
* Archive filtering
* Executable filtering
* Large file protection

### 🌳 Repository Tree Generation

Creates a visual file map before the source code:

```text
project/
├── src/
│   ├── main.py
│   └── utils.py
├── README.md
```

This gives LLMs better understanding of your project structure.

### 🔄 Multiple Output Formats

Supports:

* **Markdown** — optimized for ChatGPT
* **XML** — optimized for Claude with CDATA protection

### 📊 Token Estimation

Uses OpenAI's `tiktoken` tokenizer to estimate prompt size before usage.

Helps prevent exceeding model context limits.

### 🖥️ Desktop GUI Included

Includes a simple Electron desktop application:

* Select repository visually
* Choose output format
* Generate prompts without terminal commands

---

# 🚀 Installation

## 1. Clone Repository

```bash
git clone https://github.com/vineelneth/repo2llm.git

cd repo2llm
```

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ⚡ CLI Usage

## Generate Markdown Prompt

Current folder:

```bash
python -m repo2llm.cli .
```

Output:

```text
repo_prompt.txt
```

---

## Convert Another Repository

Example:

```bash
python -m repo2llm.cli C:\Users\YourName\Project
```

---

## Generate Claude XML Format

```bash
python -m repo2llm.cli ./my-project --format xml --out claude_prompt.xml
```

---

## Token Limit Warning

Set a custom warning limit:

```bash
python -m repo2llm.cli . --max-tokens 50000
```

---

# 🖥️ Desktop Application

repo2llm also includes an Electron GUI.

## Setup

Move into the GUI folder:

```bash
cd repo2llm-gui
```

Install dependencies:

```bash
npm install
```

Start application:

```bash
npm start
```

---

# 📦 Output Example

Generated Markdown:

````markdown
# Repository Structure

```text
my-project/
├── app.py
├── requirements.txt
```

# File Contents

## File: app.py

```py
print("Hello World")
```
````

---

# 🏗️ Project Structure

```text
repo2llm/
├── repo2llm/
│   ├── cli.py
│   ├── crawler.py
│   ├── formatter.py
│   └── __init__.py
│
├── repo2llm-gui/
│   ├── index.html
│   ├── main.js
│   └── renderer.js
│
├── pyproject.toml
├── requirements.txt
└── README.md
```

---

# 🔧 Tech Stack

### Backend

* Python
* pathlib
* pathspec
* tiktoken

### Desktop

* Electron
* JavaScript
* HTML/CSS

---

# 📌 Use Cases

* Give full projects to AI assistants
* Code reviews with LLMs
* Architecture analysis
* Documentation generation
* Debugging large repositories
* Project onboarding

---

# 🤝 Contributing

Contributions are welcome.

Feel free to:

* report bugs
* suggest improvements
* add new features

---

# 📄 License

MIT License

---

Built to make AI-assisted development faster.
