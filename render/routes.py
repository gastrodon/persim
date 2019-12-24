import markdown

_response_template = """### {code} - {short_descripton}
    {description}

    __<u>headers</u>__

    {headers}

    __<u>body</u>__

    ```{lang}
    {body}
    ```
"""
def render_response(method, r_dict):
    content = f"### {r_dict['code']} - {r_dict['short_descripton']}\n"

    if r_dict.get("description"):
        content += f"\n{r_dict['description']}\n"

    if r_dict.get('headers'):
        content += f"\n{render_headers(r_dict['headers'])}\n"

    if r_dict.get('body'):
        body = r_dict["body"]
        content += f"\n```{body.get('lang', '')}\n{body['example']}\n```\n"

def render_headers(headers):
    header_cells = [
        ["Name", "Type", "Required", "Example"],
        *[[key, headers[key]["type"], headers[key]["required"], headers[key]["example"]]
        for key in headers.keys()]
    ]
    return markdown.render_table(header_cells)
