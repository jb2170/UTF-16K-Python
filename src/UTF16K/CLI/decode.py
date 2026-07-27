import sys
import argparse

from UTF16K.wordutils import BytesToWords
from UTF16K.decode import UTF16KIncrementalDecoder
from UTF16K.UTF16KWord import UNICODE_SUP
from UTF16K.UTF16KInt import UTF16KInt

from .common import (
    yes_no_is_stdout_tty,
    format_codepoint
)

_MAX_LEN_CODEPOINT = len(r"U+10FFFF")
_MAX_LEN_CHR_REPR  = len(r"'\U0010fffd'")
_MAX_LEN_HEX_WORDS = len(r"dbff dfff")

def format_code_unit(code_unit: UTF16KInt, *, do_color: bool) -> str:
    n = int(code_unit)

    ## Codepoint
    part_codepoint = f"{format_codepoint(n):{_MAX_LEN_CODEPOINT}}"

    ## Character repr
    if n < UNICODE_SUP:
        chr_repr = f"{chr(n)!r}"
    else:
        chr_repr = ""
    part_chr_repr = f"{chr_repr:{_MAX_LEN_CHR_REPR}}"

    ## Hex words
    hex_words = " ".join(f"{int(w):04x}" for w in code_unit.utf_16k_words)
    part_hex_words = f"{hex_words:{_MAX_LEN_HEX_WORDS}}"

    ## Bin words
    fmt_parts = []
    if do_color:
        fmt_parts.append("color")
    fmt = ",".join(fmt_parts)
    bin_words = " ".join(f"{w:{fmt}}" for w in code_unit.utf_16k_words)
    part_bin_words = f"{bin_words}"

    ret_parts = (part_codepoint, part_chr_repr, part_hex_words, part_bin_words)

    return " | ".join(ret_parts)

def main_decode(args: argparse.Namespace) -> None:
    do_color = yes_no_is_stdout_tty(args.color)

    bytes_to_words = BytesToWords()
    decoder        = UTF16KIncrementalDecoder()

    while chunk := sys.stdin.buffer.raw.read(4096):
        words = bytes_to_words.decode(chunk)
        decoder.feed(words)

        for code_unit in decoder:
            print(format_code_unit(code_unit, do_color = do_color))

    decoder.close()
    bytes_to_words.feed_eof()
