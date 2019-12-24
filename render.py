def render_map_list(sectoin):
    """
    Takes a list of maps (like those of headers or query strings)
    and returns a markdown table representing that map
    sectoin: map list to render
    """
    if not len(sectoin):
        return ""

    cells = [
        list(sectoin[0].keys()),
        *[list(it.values()) for it in sectoin]
    ]

    return md.render_table(cells)

def render_table(cells, filler = " "):
    """
    Takes a 2d array, makes a markdown table
    filler: content to fill empty cells with
    """

    size_horizontal = max([len(sub) for sub in cells])
    separator = " - ".join("|" * (1 + size_horizontal))
    rows = [render_table_row(row, size = size_horizontal, filler = filler) for row in cells]
    rows.insert(1, separator)

    return "\n".join(rows)

def render_table_row(cells, size = None, filler = " "):
    """
    Tales an array, makes a markdown table row
    size: row size, if greater than the number of cells
    filler: content to fill empty cells with
    """

    size = size if size else len(cells)
    return "|" + "".join(f"{cell}|" for cell in cells) + "".join(s for s in f"{filler}|" * (size - len(cells)))

def render_code_block(content, lang = ""):
    """
    Takes text and an optional lang to render a code block
    content: content inside of this code block
    lang: language for syntax highlighting
    """
    return f"```{lang}\n{content}\n```"
