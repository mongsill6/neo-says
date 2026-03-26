"""Output formatting for quotes."""


def format_box(text, author="Neo"):
    """Format a quote in a Unicode box."""
    lines = []
    words = text.split()
    current = ""
    max_width = 46

    for word in words:
        if len(current) + len(word) + 1 <= max_width:
            current = f"{current} {word}" if current else word
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)

    width = max(len(line) for line in lines)
    width = max(width, len(author) + 4)

    box = []
    box.append(f"╭{'─' * (width + 2)}╮")
    for line in lines:
        box.append(f"│ {line:<{width}} │")
    box.append(f"│ {' ' * (width - len(author) - 2)}— {author} │")
    box.append(f"╰{'─' * (width + 2)}╯")

    return "\n".join(box)
