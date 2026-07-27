import sys
import argparse

from UTF16K.wordutils import WordsToBytes
from UTF16K.encode import encode

from .common import parse_codepoint

def main_encode(args: argparse.Namespace) -> None:
    words_to_bytes = WordsToBytes()

    for line in sys.stdin:
        n = parse_codepoint(line)

        utf_16k_words = encode(n)
        utf_16k_bytes = words_to_bytes.encode(utf_16k_words)

        sys.stdout.buffer.write(utf_16k_bytes)
        sys.stdout.buffer.flush()

    words_to_bytes.feed_eof()
