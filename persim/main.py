#! /usr/bin/env python3

import argparse, json, typing, yaml
import persim.preprocess as preprocess
import persim.render as render


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate markdown docs for a REST API")
    parser.add_argument("-o", "--out", default="out.md", type=str)
    parser.add_argument("-a", "--append", action = "store_true")
    parser.add_argument("file", nargs=1, default="")
    return parser.parse_args()


def render_from(file: str) -> str:
    with open(file) as stream:
        data: str = yaml.safe_load(stream.read())

    vars: typing.Dict = preprocess.interpolate(data.get("vars", {}))
    routes: typing.Dict = preprocess.interpolate_part(vars, data["routes"])
    return render.document(routes)


def main():
    args: argparse.Namespace = get_args()
    mode: str = "a" if args.append else "w"
    with open(args.out, mode) as stream:
        stream.write(render_from(args.file[0]))

if __name__ == "__main__":
    main()
