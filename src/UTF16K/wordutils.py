import codecs

from .UTF16KWord import (
    UNICODE_SURROGATE_HIGH_MIN,
    UNICODE_SURROGATE_LOW_SUP,
    UNICODE_SURROGATE_HIGH_SUP,
    UNICODE_SURROGATE_HIGH_PLANE_9_MIN,
    UNICODE_SURROGATE_HIGH_PLANE_A_SUP,
)

FULL_BYTE_MASK = 0b11111111

def remap_word(x: int) -> int:
    """
    Remap 16-bit integers, the quantum of UTF-16K,
    so that high surrogates corresponding to longer code units
    are pushed to the end.

    Used in `utf_16k_strcmp`.
    """

    if x < UNICODE_SURROGATE_HIGH_MIN:
        # U+0000 to U+D7FF
        # Pre surrogate
        return x

    elif x < UNICODE_SURROGATE_LOW_SUP:
        # U+D800 to U+DFFF
        # The surrogate range

        if x < UNICODE_SURROGATE_HIGH_SUP:
            # U+D800 to U+DBFF
            # High surrogate

            if x < UNICODE_SURROGATE_HIGH_PLANE_9_MIN:
                # U+D800 to U+D9FF
                # High surrogates: planes 1 to 8
                return x + 0x2000

            elif x < UNICODE_SURROGATE_HIGH_PLANE_A_SUP:
                # U+DA00 to U+DA7F
                # High surrogates: planes 9 and 10
                return x + 0x2180

            else:
                # U+DA80 to U+DBFF
                # High surrogates: planes 11 to 16
                return x + 0x1F80

        else:
            # U+DC00 to U+DFFF
            # Low surrogate
            return x + 0x2000

    else:
        # U+E000 to U+FFFF
        # Post surrogate
        return x - 0x0800

def utf_16k_strcmp(s1: tuple[int], s2: tuple[int]) -> int:
    """
    Compare `s1` and `s2`, which are tuples of UTF-16K words.

    If `s1` and `s2` are equal then return `0`.

    If `s1` is less than `s2` then return `-1`.

    If `s1` is greater than `s2` then return `+1`.

    The comparison uses `remap_word` to compare the integers encoded
    inside the UTF-16K code units.
    """

    is1 = iter(s1)
    is2 = iter(s2)

    while True:
        c1 = next(is1, None)
        c2 = next(is2, None)

        if c1 is None:
            if c2 is None:
                return 0
            else:
                return -1
        if c2 is None:
            return +1

        if c1 == c2:
            continue

        c1_remap = remap_word(c1)
        c2_remap = remap_word(c2)

        if c1_remap < c2_remap:
            return -1
        else:
            return +1

class BytesToWords(codecs.BufferedIncrementalDecoder):
    def _buffer_decode(self, input, errors, final):
        q, r = divmod(len(input), 2)

        if final and r:
            raise ValueError("Odd number of bytes supplied for word chunking")

        ret = tuple(
            (input[idx] << 8) + (input[idx + 1])
            for idx in (2 * i for i in range(q))
        )

        return ret, 2 * q

    def feed_eof(self) -> None:
        self.decode(b"", final = True)

class WordsToBytes(codecs.IncrementalEncoder):
    def encode(self, input: tuple[int], final = False):
        ret_array = bytearray(2 * len(input))

        for idx, word in (
            (2 * i, w)
            for (i, w) in enumerate(input)
        ):
            ret_array[idx + 0] = (word >> 8) & FULL_BYTE_MASK
            ret_array[idx + 1] = (word >> 0) & FULL_BYTE_MASK
            # Tiny bit wasteful, but demonstrates the pattern

        ret = bytes(ret_array)

        return ret

    def feed_eof(self) -> None:
        self.encode(tuple(), final = True)
