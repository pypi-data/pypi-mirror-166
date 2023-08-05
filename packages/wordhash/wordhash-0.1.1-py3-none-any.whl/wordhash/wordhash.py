#!/usr/bin/env python3
import argparse
import sys
import hashlib
import math
import os
import pathlib
import typing as t

import bitstring

_ROOT = os.path.abspath(os.path.dirname(__file__))
BUF_SIZE: int = 65536
DEFAULT_HASH_LENGTH: int = 8
DEFAULT_WORDLIST_PATH: pathlib.Path = pathlib.Path(
    os.path.join(_ROOT, "data", "wordlist.txt")
).expanduser()


def get_words(filepath: pathlib.Path) -> t.List[str]:
    with open(filepath) as f:
        lines = f.read().splitlines()
        f.close()
    return lines


def get_digest(
    filepath: t.Optional[pathlib.Path] = None,
    string: t.Optional[str] = None,
    input_bytes: t.Optional[bytes] = None,
    length: int = 8,
) -> bytes:
    if bool(filepath) + bool(string) + bool(input_bytes) != 1:
        raise ValueError(
            "Need exactly one of `filepath`,`string`, or `input_bytes` should be set"
        )
    hasher = hashlib.shake_256()
    if filepath:
        with open(filepath, "rb") as f:
            while True:
                data = f.read(BUF_SIZE)
                if not data:
                    break
                hasher.update(data)
    elif string:
        hasher.update(bytes(string, sys.stdin.encoding))
    elif input_bytes:
        hasher.update(input_bytes)
    else:
        raise ValueError(
            "Need exactly one of `filepath`,`string`, or `input_bytes` should be set"
        )
    return hasher.digest(8)


def get_wordencoding(data: bytes, wordlist: t.List[str], length: int) -> str:
    data_bitstring: str = bitstring.BitArray(data).bin
    id_bits: int = math.floor(math.log(len(wordlist)) / math.log(2))
    wordhashlist: t.List[str] = []
    for chunk_idx in range(0, len(data_bitstring) - 1, id_bits):
        chunk_bitstring = data_bitstring[chunk_idx : (chunk_idx + id_bits)]
        chunk_bytes = bitstring.BitArray(bin=chunk_bitstring)
        word_idx = chunk_bytes.uint
        word = wordlist[word_idx]
        wordhashlist.append(word)
    titlecased = map(lambda x: x.title(), wordhashlist)
    return "".join(titlecased)


def wordhash(data: bytes) -> str:
    wordlist = get_words(DEFAULT_WORDLIST_PATH.expanduser())
    digest = get_digest(input_bytes=data)
    return get_wordencoding(digest, wordlist, DEFAULT_HASH_LENGTH)


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "-w",
        "--wordlist",
        dest="wordlist_path",
        default=DEFAULT_WORDLIST_PATH.relative_to(os.getcwd()),
        help="Path to a newline-delimted file containing words to be used in the wordhash",
        type=pathlib.Path,
    )
    parser.add_argument(
        "-l",
        "--length",
        help="Length of hash digest for this program to use internally. Determines number of words in the resulting wordhash.",
        type=int,
        default=DEFAULT_HASH_LENGTH,
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-f", "--file", type=pathlib.Path, help="Path to file to use as input data"
    )
    group.add_argument("-s", "--string", type=str, help="String to use as input data")
    args = parser.parse_args()
    data_path: t.Optional[pathlib.Path] = args.file.expanduser() if args.file else None
    wordlist_path: pathlib.Path = args.wordlist_path.expanduser()

    wordlist = get_words(wordlist_path)
    digest = get_digest(data_path, args.string)
    res = get_wordencoding(digest, wordlist, args.length)
    print(res)


if __name__ == "__main__":
    main()
