from typing import Iterator
import json
import sys
from tqdm import tqdm
import pathlib
from logging import Logger


def jsonlreader(filename: str, logger: Logger = None) -> Iterator[dict]:
    msg = "You can only use jsonl reader w/ json file"
    assert pathlib.Path(filename).suffix == ".jsonl", msg
    with open(filename, "r") as inf:
        for linenumber, line in tqdm(enumerate(inf), desc="reading {}".format(filename)):
            try:
                yield linenumber, json.loads(line)
            except json.decoder.JSONDecodeError:
                sys.stderr.write("[*]")


if __name__ == "__main__":

    for linenumber, line in jsonlreader("test/fixtures/data/oren.jsonl"):
        print(line)
