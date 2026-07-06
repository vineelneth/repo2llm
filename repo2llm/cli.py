import argparse
import sys
from pathlib import Path
import tiktoken

from repo2llm.crawler import crawl_repository
from repo2llm.formatter import to_markdown, to_xml

def estimate_tokens(text: str, model: str = "gpt-4o") -> int:
    """
    Estimates token count using OpenAI's tiktoken.
    This gives the exact token cost for OpenAI models, and a very close 
    estimate for Anthropic's Claude.
    """
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        # Fallback to standard base encoding if model is unknown
        encoding = tiktoken.get_encoding("cl100k_base")
    
    # allowed_special="all" prevents errors if our code contains strings that look like tokens
    return len(encoding.encode(text, allowed_special="all"))

def main():
    # 1. Setup Command Line Arguments
    parser = argparse.ArgumentParser(
        description="repo2llm: Package your entire codebase into a single, LLM-friendly prompt."
    )
    
    parser.add_argument(
        "directory", 
        type=str, 
        nargs="?", 
        default=".", 
        help="The path to the repository you want to package (defaults to current directory)."
    )
    
    parser.add_argument(
        "--format", 
        choices=["markdown", "xml"], 
        default="markdown", 
        help="The output format (markdown or xml). XML is highly recommended for Claude."
    )
    
    parser.add_argument(
        "--out", 
        type=str, 
        default="repo_prompt.txt", 
        help="The name of the generated output file."
    )
    
    parser.add_argument(
        "--max-tokens", 
        type=int, 
        default=128000, 
        help="Warning threshold for token count (default: 128,000 for standard context windows)."
    )
    
    args = parser.parse_args()
    
    # 2. Resolve directory and validate
    root_dir = Path(args.directory).resolve()
    
    if not root_dir.is_dir():
        print(f"❌ Error: Directory '{root_dir}' does not exist.")
        sys.exit(1)
        
    print(f"🔍 Crawling repository at: {root_dir}")
    valid_files = crawl_repository(str(root_dir))
    
    print(f"📄 Found {len(valid_files)} valid text files to process.")
    
    # 3. Format the Output
    if args.format == "markdown":
        output_text = to_markdown(root_dir, valid_files)
    else:
        output_text = to_xml(root_dir, valid_files)
        
    # 4. Token Estimation
    print("⏳ Estimating token count...")
    token_count = estimate_tokens(output_text)
    
    print(f"\n📊 Total estimated tokens: {token_count:,}")
    
    # 5. Token Limit Warning
    if token_count > args.max_tokens:
        print(f"\n⚠️ WARNING: Token count ({token_count:,}) exceeds your max-tokens limit ({args.max_tokens:,}).")
        print("This might be too large for your LLM's context window. Consider pruning large files or adding them to your .gitignore.")
        
    # 6. Save the Output
    out_path = Path(args.out).resolve()
    try:
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(output_text)
        print(f"\n✅ Success! Prompt successfully written to {out_path}")
    except Exception as e:
        print(f"\n❌ Error writing output file: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()