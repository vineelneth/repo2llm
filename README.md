# repo2llm 🚀

A lightning-fast CLI utility that packages your entire local repository into a single, highly-compressed text file optimized for massive-context LLMs (like Claude 3.5 Sonnet and GPT-4o).

## Features
- **Smart Ignore:** Automatically respects your `.gitignore` and strips out bloat (`node_modules`, `.venv`, etc.).
- **Binary Filtering:** Safely ignores images and compiled binaries.
- **Visual File Tree:** Injects a macro-level directory map at the top of the prompt to help the LLM understand your architecture.
- **Format Toggles:** Outputs in Markdown (for GPT) or strict XML (for Claude).

## Installation
```bash
pip install repo2llm

# Package the current directory
repo2llm .

# Package for Claude (uses XML)
repo2llm . --format xml --out claude_prompt.xml