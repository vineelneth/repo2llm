import html
from pathlib import Path

def generate_file_tree(root_dir: Path, valid_files: list[Path]) -> str:
    """
    Generates a text-based folder structure tree to help the LLM visualize the repository.
    Only includes the files that passed through our crawler filters.
    """
    tree_lines = []
    # Sort paths so the tree looks neat and orderly
    sorted_files = sorted(valid_files)
    
    # Track paths we've seen to build the visual hierarchy
    seen_prefixes = set()
    
    tree_lines.append(f"{root_dir.name}/")
    
    for file_path in sorted_files:
        # Get path relative to the root
        rel_path = file_path.relative_to(root_dir)
        parts = rel_path.parts
        
        for i in range(len(parts)):
            sub_path = Path(*parts[:i+1])
            if sub_path in seen_prefixes:
                continue
                
            seen_prefixes.add(sub_path)
            indent = "    " * i
            
            if i == len(parts) - 1:
                # It's a file
                tree_lines.append(f"{indent}├── {parts[i]}")
            else:
                # It's a directory
                tree_lines.append(f"{indent}├── {parts[i]}/")
                
    return "\n".join(tree_lines)

def to_markdown(root_dir: Path, valid_files: list[Path]) -> str:
    """
    Formats the files using classic Markdown code blocks.
    """
    root_path = Path(root_dir).resolve()
    output = []
    
    # 1. Add the file tree at the very top
    output.append("# Repository Structure\n")
    output.append("```text")
    output.append(generate_file_tree(root_path, valid_files))
    output.append("```\n")
    
    # 2. Append the contents of each file
    output.append("# File Contents\n")
    for file_path in valid_files:
        rel_path = file_path.relative_to(root_path)
        # Convert windows backslashes to forward slashes for the LLM's readability
        display_path = str(rel_path).replace("\\", "/")

        safe_path = html.escape(display_path, quote=True)

        output.append(f'    <file path="{safe_path}">')
        
        # Use the extension to give Markdown a syntax highlighting hint
        extension = file_path.suffix.lstrip('.')
        output.append(f"```{extension}")
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                output.append(f.read())
        except Exception as e:
            output.append(f"[Error reading file: {str(e)}]")
            
        output.append("```\n")
        
    return "\n".join(output)

def to_xml(root_dir: Path, valid_files: list[Path]) -> str:
    """
    Formats the files using strict XML tags (highly optimized for Claude models).
    """
    root_path = Path(root_dir).resolve()
    output = []
    
    output.append("<repository>")
    output.append("  <structure>")
    output.append(generate_file_tree(root_path, valid_files))
    output.append("  </structure>\n")
    
    output.append("  <files>")
    for file_path in valid_files:
        rel_path = file_path.relative_to(root_path)
        display_path = str(rel_path).replace("\\", "/")
        
        output.append(f'    <file path="{display_path}">')
        output.append("<![CDATA[")  # CDATA prevents code characters like < or > from breaking the XML
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

                # Prevent accidental CDATA closing
                content = content.replace(
                    "]]>",
                    "]]]]><![CDATA[>"
                )

                output.append(content)

        except Exception as e:
            output.append(f"[Error reading file: {str(e)}]")
            
        output.append("]]>")
        output.append("    </file>\n")
        
    output.append("  </files>")
    output.append("</repository>")
    
    return "\n".join(output)