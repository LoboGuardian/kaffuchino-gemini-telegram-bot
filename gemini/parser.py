# gemini/parser.py

import re

# Precompile regex patterns for performance
PATTERNS = {
    "bold": re.compile(r"\*\*(.*?)\*\*"),
    "italic": re.compile(r"(?<!\*)\*(?!\*)(?!\*\*)(.*?)(?<!\*)\*(?!\*)"),
    "underline": re.compile(r"__(.*?)__"),
    "strikethrough": re.compile(r"~~(.*?)~~"),
    "monospace": re.compile(r"(?<!`)`(?!`)(.*?)(?<!`)`(?!`)"),
    "link": re.compile(r"\[(.*?)\]\((.*?)\)"),
    "header": re.compile(r"^(#{1,6})\s+(.*)", re.MULTILINE),
    "hand_points": re.compile(r"(?<=\n)\*\s(?!\*)|^\*\s(?!\*)"),
    "code_block": re.compile(r"```([\w]*?)\n([\s\S]*?)```", re.DOTALL),
}

"""
Escapes HTML special characters in a string.
Replaces &, <, > with HTML entities to prevent them
from being interpreted as HTML tags when output.
"""

def escape_html(text: str) -> str:
    """Escapes HTML special characters in a string."""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def apply_regex(text: str, pattern, replacement: str) -> str:
    """Apply a regex pattern replacement."""
    return pattern.sub(replacement, text)

def apply_formatting_pipeline(text: str) -> str:
    """Applies all text formatting in a single pass."""
    replacements = [
        (PATTERNS["bold"], r"<b>\1</b>"),
        (PATTERNS["italic"], r"<i>\1</i>"),
        (PATTERNS["underline"], r"<u>\1</u>"),
        (PATTERNS["strikethrough"], r"<s>\1</s>"),
        (PATTERNS["monospace"], r"<code>\1</code>"),
        (PATTERNS["link"], r'<a href="\2">\1</a>'),
        (PATTERNS["header"], r"<b><u>\2</u></b>"),
        (PATTERNS["hand_points"], "👉 "),
    ]
    for pattern, replacement in replacements:
        text = apply_regex(text, pattern, replacement)
    return text

def apply_code_blocks(text: str) -> str:
    """Replace markdown code blocks with HTML <pre> tags."""
    return apply_regex(text, PATTERNS["code_block"], r"<pre lang='\1'>\2</pre>")

def format_message(text: str) -> str:
    """Format the given message text from markdown to HTML."""
    text = escape_html(text)

    lines = text.split("\n")
    formatted_lines = []
    in_code_block = False

    for line in lines:
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            formatted_lines.append(line)
            continue

        formatted_lines.append(apply_formatting_pipeline(line) if not in_code_block else line)

    formatted_text = "\n".join(formatted_lines)
    return apply_code_blocks(formatted_text)