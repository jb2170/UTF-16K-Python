from .UTF16KWord import UTF16KWord, N_BYTES_IN_WORD

class UTF16KInt:
    def __init__(self, utf_16k_words: list[UTF16KWord]) -> None:
        # No validation is done; we're assuming these come from `UTF16KIncrementalDecoder`
        self.utf_16k_words = utf_16k_words

    def __str__(self) -> str:
        return " ".join(str(w) for w in self.utf_16k_words)

    def __int__(self) -> int:
        ret = 0
        content_words = (w for w in self.utf_16k_words if w.is_content_word)
        for content_word in content_words:
            ret <<= content_word.n_bits_content_total
            ret += content_word.content
        return ret

    @property
    def n_words(self) -> int:
        return len(self.utf_16k_words)

    @property
    def n_bytes(self) -> int:
        return N_BYTES_IN_WORD * self.n_words

    @property
    def n_bits_content_total(self) -> int:
        """
        The number of content bits that the code unit contains.

        This is the 'capacity' of the code unit, not the count of 'occupied' bits.
        """
        return sum(w.n_bits_content_total for w in self.utf_16k_words)

    @property
    def n_bits_content_mandatory(self) -> int:
        """
        The number of mandatory content bits that the code unit contains.

        This is the 'capacity' of the code unit, not the count of 'occupied' bits.
        """
        return sum(w.n_bits_content_mandatory for w in self.utf_16k_words)
