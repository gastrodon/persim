import json, argparse
from document import Document

def get_args():
    parser = argparse.ArgumentParser(description = "Generate markdown docs for REST")
    parser.add_argument("file", nargs = 1, default = "")
    return parser.parse_args()

def main():
    args = get_args()
    parsed_document = load_document(args.file[0]).parse_variables()
    print(json.dumps(parsed_document.routes))

def load_document(name):
    return Document(open(name).read())

def load_files(filenames):
    return [open(file).read() for file in filenames]

main()
