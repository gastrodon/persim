import json

# Friendly api

headers = lambda h : dict_list(h)
query_strings = lambda qs : dict_list(qs)
body = lambda content, lang : code_block(content, lang)
json_body = lambda content : code_block(json.dumps(content, indent = 4), "JSON")

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
    full = f"- {code} - {section.get('title', '?')}\n"
    full += find_string("description", section)
    full += find_list("headers", section)
    full += find_body(section)

    return full

def request(path, method, section):
    full = find_string("description", section)
    full += find_list("headers", section)
    full += find_list("query_strings", section)
    full += find_body(section)
    full += find_responses(section)

    return foldable(f"{method} {path}", full)

def route(path, section):
    _rendered = ""
    for method in section:
        _rendered += request(path, method, section[method])

    return _rendered

def find_string(target, section):
    retrieved = section.get(target)

    if not retrieved:
        return ""

    return f"{retrieved}\n\n"

def find_list(target, section):
    retrieved = section.get(target, [])

    if len(retrieved):
        return f"{dict_list(retrieved)}\n\n"

    return ""

def find_body(section):
    retrieved = section.get("body", {})

    content = retrieved.get("content")
    if not content:
        return ""

    lang = retrieved.get("lang", "").lower()
    if lang == "json":
        return f"{json_body(content)}\n\n"

    return f"{body(content, lang)}\n\n"

def find_responses(section):
    retrieved = section.get("responses", {})

    if not len(retrieved):
        return ""

    return "__responses__\n\n" + "".join([response(code, retrieved[code]) for code in sorted(retrieved.keys())])
