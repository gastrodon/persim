# Friendly api

headers = lambda h : dict_list(h)
query_strings = lambda qs : dict_list(qs)
body = lambda content, lang : code_block(content, lang)
json = lambda content : code_block(content, "JSON")

# Mean functions

def dict_list(sectoin):
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

    return table(cells)

def table(cells, filler = " "):
    """
    Takes a 2d array, makes a markdown table
    filler: content to fill empty cells with
    """

    size_horizontal = max([len(sub) for sub in cells])
    separator = " - ".join("|" * (1 + size_horizontal))
    rows = [table_row(row, size = size_horizontal, filler = filler) for row in cells]
    rows.insert(1, separator)

    return "\n".join(rows)

def table_row(cells, size = None, filler = " "):
    """
    Tales an array, makes a markdown table row
    size: row size, if greater than the number of cells
    filler: content to fill empty cells with
    """

    size = size if size else len(cells)
    return "|" + "".join(f"{cell}|" for cell in cells) + "".join(s for s in f"{filler}|" * (size - len(cells)))

def code_block(content, lang = ""):
    """
    Takes text and an optional lang to render a code block
    content: content inside of this code block
    lang: language for syntax highlighting
    """
    return f"```{lang}\n{content}\n```"

def foldable(summary, details):
    return f"""<details>
<summary>{summary}</summary>
{details}
</details>
"""

def response(code, section):
    if section.get("title"):
        summary = f"{code} - {section['title']}"
    else:
        summary = code

    full = section.get("description", "")

    _headers = section.get("headers", [])
    if len(_headers):
        full += f"{headers(_headers)}\n\n"

    _body = section.get("body", {})
    if _body.get("content"):
        full += f"{body(_body['content'], _body.get('lang', ''))}\n\n"

    return foldable(summary, full)

def request(path, method, section):
    if section.get("description"):
        full = f"{section['description']}\n\n"
    else:
        full = ""

    _headers = section.get("headers", [])
    if len(_headers):
        full += f"{headers(_headers)}\n\n"

    _qs = section.get("query_strings", [])
    if len(_qs):
        full += f"{query_strings(_qs)}\n\n"

    _body = section.get("body", {})
    if _body.get("content"):
        full += f"{body(_body['content'], _body.get('lang', ''))}\n\n"

    _responses = section.get("responses", {})
    if len(_responses):
        response_section = ""
        for code in _responses:
            response_section += response(code, _responses[code])

        full += f"__responses__\n\n{response_section}"

    return foldable(f"{method} `{path}`", full)
