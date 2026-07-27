import argparse

from UTF16K.encode import encode
from UTF16K.decode import UTF16KIncrementalDecoder
from UTF16K.UTF16KWord import (
    UNICODE_SUP,
    UNICODE_SURROGATE_HIGH_MIN, UNICODE_SURROGATE_HIGH_SUP,
    UNICODE_SURROGATE_LOW_MIN, UNICODE_SURROGATE_LOW_SUP
)

from .common import (
    yes_no_is_stdout_tty,
    parse_codepoint, format_codepoint
)

def main_info(args: argparse.Namespace) -> None:
    # Initialise from args
    do_color: bool = yes_no_is_stdout_tty(args.color)
    n_str:    str  = args.n_str

    n = parse_codepoint(n_str)

    # Encode integer `n` in UTF-16K
    encoded = encode(n)
    decoder = UTF16KIncrementalDecoder()
    decoder.feed(encoded)
    code_unit = next(iter(decoder))

    # Print some info about the words / codepoint
    info_lines = []

    ## Unicode info
    line_parts = []
    if n < UNICODE_SUP:
        line_parts.append("In the Unicode range")
        if n in range(UNICODE_SURROGATE_HIGH_MIN, UNICODE_SURROGATE_HIGH_SUP):
            line_parts.append("(high surrogate)")
        elif n in range(UNICODE_SURROGATE_LOW_MIN, UNICODE_SURROGATE_LOW_SUP):
            line_parts.append("(low surrogate)")
        else:
            # This always happens with UTF-16K.
            # The encoder forbids encoding the surrogate range.
            pass
        line_parts.append(format_codepoint(n))
        line_parts.append(f"{chr(n)!r}")
    else:
        line_parts.append("Beyond the Unicode range")
        line_parts.append("(adventurous)")
        line_parts.append(format_codepoint(n))
    info_lines.append(" ".join(line_parts))

    ## UCS-2 / UTF-16 / UTF-16K length
    line_parts = []
    if n < UNICODE_SUP:
        codepoint_family = "UTF-16"
    else:
        codepoint_family = "UTF-16K"
    line_parts.append(f"{code_unit.n_words} word ({code_unit.n_bytes} byte) {codepoint_family}")
    line_parts.append(f"{code_unit.n_bits_content_total} bits")
    line_parts.append(f"{code_unit.n_bits_content_mandatory} mandatory bits")
    info_lines.append(" | ".join(line_parts))

    ## Hex words
    hex_words = " ".join(f"{int(w):04x}" for w in code_unit.utf_16k_words)
    info_lines.append(f"Hex: {hex_words}")

    ## Bin words
    fmt_parts = []
    if do_color:
        fmt_parts.append("color")
    fmt = ",".join(fmt_parts)
    # If there's a "," in a fmt_part then there's problems,
    # but our script won't do that.
    # Remember GitHub not sanitizing their input:
    # https://www.youtube.com/watch?v=m5t08CREHcE

    bin_words = " ".join(f"{w:{fmt}}" for w in code_unit.utf_16k_words)
    info_lines.append(f"Bin: {bin_words}")

    print("\n\n".join(info_lines))
