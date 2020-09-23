import json

REQUEST_TEMPLATE = """\
<details>
<summary>{method} {route}</summary>

{description}

{tables}

{body}

#### Responses
{responses}
</details>
"""

TABLES_TEMPLATE = """\
###### {title}
{table}
"""

BODY_TEMPLATE = """\
#### Body
```{lang}
{body}
```
"""

RESPONSE_TEMPLATE = """\
- `{code}`

  {description}

  {body}
"""


def document(data):
    return "\n".join([
        request(route_key, method_key, method_data)
        for route_key, route_data in data.items()
        for method_key, method_data in route_data.items()
    ])


def request(route, method, data):
    return REQUEST_TEMPLATE.format(
        method = method.upper(),
        route = route,
        description = data["description"],
        tables = tables(data.get("tables", {})),
        body = body(data.get("body", {})),
        responses = "\n".join([
            response(code, response_data)
            for code, response_data in data["responses"].items()
        ]),
    )


def tables(data):
    """
    Render a collection of tables. For any table that is not rendered,
    for example empty tables, it will be filtered out of the result

    For some route, this should recieve the data
    $<route>.<method>.tables
    """
    return "\n".join(
        [
            TABLES_TEMPLATE.format(
                title = key,
                table = table(value),
            )
            for key, value in data.items()
            if table(value)
        ]
    )


def response(code, data):
    """
    Given a status code and response, render it

    For some route method, this should recieve the data
    code, $<route>.<method>.<responses>[code]
    """
    return RESPONSE_TEMPLATE.format(
        code = f"{code}",
        description = data["description"],
        body = body(data.get("body"))
    )


def body(data):
    """
    Render a request or response body. If the body is empty,
    an empty string is returned

    For some route, this should recieve the data
    $<route>.<method>.body
    $<route>.<method>.<responses>[n].body
    """
    if not data:
        return ""

    if (lang := data.get("lang", "").lower()) == "json":
        data["content"] = json.dumps(
            json.loads(data["content"]),
            indent = 4,
        )

    return BODY_TEMPLATE.format(
        lang = lang,
        body = data["content"],
    )


def table(data):
    """
    Given a list of dicts, render it into a table.
    The top row of the table will be the dict keys as a title
    The following rows will be those values
    If data is empty, an empty string is returned

    If the dicts are not consistent, the table will not render correctly
    """
    if not data:
        return ""

    return "\n".join([
        table_row(list(data[0].keys())),
        table_row([" - "] * len(data[0])),
        *[table_row(list(it.values())) for it in data],
    ])


def table_row(cells, size=None):
    """
    Given an array, render it into a single table row
        Size: optional row length, if different than
    """
    size = size if size else len(cells)
    return "|" + "".join([
        f"{cell}|"
        for cell
        in cells + [" "] * (size - len(cells))
    ])
