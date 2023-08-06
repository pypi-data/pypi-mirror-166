import json
import sys

from . import clipboard


def prettify():
    """prettify json string from clipboard.

    1. get data from clipboard

    2. dump data to local data.json

    3. dumps to local terminal
    """
    json_file: str = 'data.json'

    args: list = sys.argv
    if len(args) > 1:
        content_list: list = args[1:]
        content: str = " ".join(content_list)
    else:
        content = clipboard.paste()

    try:
        content_eval = eval(content)
    except NameError:
        content_eval = json.loads(content)

    json.dump(content_eval, open(json_file, 'w', encoding='utf-8'), indent=True, ensure_ascii=False)

    text: str = json.dumps(content_eval, indent=True, ensure_ascii=False).encode('utf-8').decode()
    return text


if __name__ == "__main__":
    prettify()
