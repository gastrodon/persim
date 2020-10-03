#! /usr/bin/env python3

import argparse, json, typing, yaml
import persim.preprocess as preprocess
import persim.render as render


LIMIT: int = 20

def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate markdown docs for a REST API")
    parser.add_argument("-o", "--out", default="out.md", type=str)
    parser.add_argument("-a", "--append", action = "store_true")
    parser.add_argument("file", nargs="+", default="")
    return parser.parse_args()


def render_from(files: typing.List) -> str:
    data: typing.Dict = {}

    for file in files:
        with open(file) as stream:
            data = merge_json(data, yaml.safe_load(stream.read()))


    vars: typing.Dict = data.get("vars", {})
    depth: int = 0
    while "$" in str(vars := preprocess.interpolate(vars)):
        if (depth := depth + 1) == LIMIT:
            raise Exception(f"Could not interpolate vars past a depth of {LIMIT}")

        continue

    routes: typing.Dict = preprocess.interpolate_part(vars, data["routes"])
    return render.document({ key: routes[key] for key in sorted(routes) })


def merge_json(target: typing.Dict, source: typing.Dict) -> typing.Dict:
    merged: typing.Dict = {**target}

    key: str
    value: typing.Any
    for key, value in source.items():
        if not key in merged:
            merged[key] = value
            continue

        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = merge_json(merged[key], value)

        else:
            merged[key] = value

    return merged


def main():
    args: argparse.Namespace = get_args()
    mode: str = "a" if args.append else "w"
    with open(args.out, mode) as stream:
        stream.write(render_from(args.file))

if __name__ == "__main__":
    main()
