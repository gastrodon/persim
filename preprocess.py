import re, typing

VAR_PATTERN = r"\$[a-zA-Z0-9\.\_\-]+"


def interpolate(doc: typing.Dict) -> typing.Dict:
    return interpolate_part(doc, doc)


def interpolate_part(doc: typing.Dict,
                     value: typing.Any,
                     tree: typing.List = []) -> typing.Any:
    if isinstance(value, (list, tuple)):
        return [interpolate_part(doc, it, tree) for it in value]

    if isinstance(value, dict):
        return {
            key: interpolate_part(doc, it, tree)
            for key, it in value.items()
        }

    if isinstance(value, (int, float)):
        return str(value)

    for name in re.findall(VAR_PATTERN, value):
        if value == name:
            value = value_of(doc, name[1:].strip(), tree)
        else:
            try:
                value = value.replace(name,
                                      value_of(doc, name[1:].strip(), tree))
            except TypeError:
                raise Exception(
                    f"Referenced value must be of type string to replace {name} in \n{value}"
                )

    return value


def value_of(doc: typing.Dict,
             name: str,
             tree: typing.List = []) -> typing.Any:
    if name in tree:
        raise Exception(f"valuing {name} after [{', '.join(tree)}]")

    current: typing.Any = {**doc}
    path: typing.List = []

    for it in name.split("."):
        try:
            current = current[it]
        except KeyError:
            raise Exception(f"{it} does not exist in ${'.'.join(path)}")

        path.append(it)
        if isinstance(current, str) and current.startswith("$"):
            current = value_of(doc, current[1:], tree + [".".join(path)])

    if not isinstance(current, str):
        current = interpolate_part(doc, current, tree)

    return current
