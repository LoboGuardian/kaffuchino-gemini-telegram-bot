import re


def escape_html(text: str) -> str:
    """Escapes HTML special characters in a string.

    Replaces &, <, > with HTML entities to prevent them
    from being interpreted as HTML tags when output.

    Args:
        text (str): The text to escape.

    Returns:
        str: The text with HTML characters escaped.
    """
    text = text.replace("&", "&amp;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    return text


def apply_hand_points(text: str) -> str:
    """Replaces markdown bullet points (*) with right hand point emoji.

    Args:
    text (str): The text to modify.

    Returns:
    str: The text with markdown bullet points replaced with emoji.
    """
    pattern = r"(?<=\n)\*\s(?!\*)|^\*\s(?!\*)"

    replaced_text = re.sub(pattern, "👉 ", text)

    return replaced_text


def apply_bold(text: str) -> str:
    """Replaces markdown bold formatting with HTML bold tags.

    Args:
    text (str): The text to modify.

    Returns:
    str: The text with markdown bold replaced by HTML tags.
    """
    pattern = r"\*\*(.*?)\*\*"
    replaced_text = re.sub(pattern, r"<b>\1</b>", text)
    return replaced_text


def apply_italic(text: str) -> str:
    """Replaces markdown italic formatting with HTML italic tags.

    Args:
    text (str): The text to modify.

    Returns:
    str: The text with markdown italic replaced by HTML tags.
    """
    pattern = r"(?<!\*)\*(?!\*)(?!\*\*)(.*?)(?<!\*)\*(?!\*)"
    replaced_text = re.sub(pattern, r"<i>\1</i>", text)
    return replaced_text


def apply_code(text: str) -> str:
    """Replace markdown code blocks with HTML <pre> tags.

    Args:
    text (str): The text to modify.

    Returns:
    str: The text with markdown code blocks replaced by HTML tags.
    """
    pattern = r"```([\w]*?)\n([\s\S]*?)```"
    replaced_text = re.sub(pattern, r"<pre lang='\1'>\2</pre>", text,
                           flags=re.DOTALL)
    return replaced_text


def apply_monospace(text: str) -> str:
    """Replaces markdown monospace backticks with HTML <code> tags.

    Args:
    text (str): The input text containing markdown monospace formatting.

    Returns:
    str: The text with monospace sections replaced with HTML tags.
    """
    pattern = r"(?<!`)`(?!`)(.*?)(?<!`)`(?!`)"
    replaced_text = re.sub(pattern, r"<code>\1</code>", text)
    return replaced_text


def apply_link(text: str) -> str:
    """Replace markdown links with HTML anchor tags.

    Args:
    text (str): The input text containing markdown links.

    Returns:
    str: The text with markdown links replaced by HTML anchor tags.
    """
    pattern = r"\[(.*?)\]\((.*?)\)"
    replaced_text = re.sub(pattern, r'<a href="\2">\1</a>', text)
    return replaced_text


def apply_underline(text: str) -> str:
    """Replace markdown underline with HTML underline tags.

    Args:
    text (str): The input text to modify.

    Returns:
    str: The text with markdown underlines replaced with HTML tags."""
    pattern = r"__(.*?)__"
    replaced_text = re.sub(pattern, r"<u>\1</u>", text)
    return replaced_text


def apply_strikethrough(text: str) -> str:
    """Replace markdown strikethrough with HTML strikethrough tags.

    Args:
    text (str): The input text to modify.

    Returns:
    str: The text with markdown strikethroughs replaced with HTML tags.
    """
    pattern = r"~~(.*?)~~"
    replaced_text = re.sub(pattern, r"<s>\1</s>", text)
    return replaced_text


def apply_header(text: str) -> str:
    """Replace markdown header # with HTML header tags.

    Args:
    text (str): The input text to modify.

    Returns:
    str: The text with markdown headers replaced with HTML tags.
    """
    pattern = r"^(#{1,6})\s+(.*)"
    replaced_text = re.sub(pattern, r"<b><u>\2</u></b>", text, flags=re.DOTALL)
    return replaced_text


def apply_exclude_code(text: str) -> str:
    """Applies text formatting to non-code lines  within a given string.

    This function iterates through each line of the input text.
    It identifies code blocks delimited by ''' and skips formatting
    those lines. For lines outside of code blocks, it applies header,
    link, bold, italic, underline, strikethrough, monospace, and hand-point
    text formatting

   Args:
        text: The input string containing text and potentially code blocks.

    Returns:
        The modified string with formatting applied to non-code lines.

    """
    lines = text.splitlines()
    in_code_block = False
    formatted_lines = []

    for line in lines:
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            formatted_lines.append(line)  # Keep code block delimiters as is
            continue  # Skip further formatting on code block delimiters.

        if in_code_block:
            formatted_lines.append(line)  # Keep code block as is
            continue

        # Apply formatting to non-code lines here (placeholder)
        # calls the helper function for formatting
        formatted_line = _format_text(line)
        formatted_lines.append(formatted_line)

    return "\n".join(formatted_lines)


def _format_text(line: str) -> str:
    """Applies all text formatting to a single line.

    This is a helper function that applies various formatting
    functions like header, link, bold, italic, underline,
    strikethrough, monospace, and hand-point to a given line.

    Args:
        line: The input string for a single line.

    Returns:
        The formatted string.
    """
    formatted_line = line
    formatted_line = apply_header(formatted_line)
    formatted_line = apply_link(formatted_line)
    formatted_line = apply_bold(formatted_line)
    formatted_line = apply_italic(formatted_line)
    formatted_line = apply_underline(formatted_line)
    formatted_line = apply_strikethrough(formatted_line)
    formatted_line = apply_monospace(formatted_line)
    formatted_line = apply_hand_points(formatted_line)
    return formatted_line


def format_message(text: str) -> str:
    """Format the given message text from markdown to HTML.

    Escapes HTML characters, applies link, code, and other rich text
    formatting, and returns the formatted HTML string.

    Args:
      text: The plain text message to format.

    Returns:
      The formatted HTML string.
    """
    formatted_text = escape_html(text)
    formatted_text = apply_exclude_code(formatted_text)
    formatted_text = apply_code(formatted_text)
    return formatted_text
