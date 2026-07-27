from typing import Generator

from .UTF16KWord import (
    UTF16KWord,
    idx_highest_zero, n_start_bits_ones,
    word_is_high_surrogate, word_is_low_surrogate,
    UNICODE_SURROGATE_HIGH_MIN,
    UNICODE_SURROGATE_HIGH_SUP,
    UNICODE_SURROGATE_LOW_MIN,
    UNICODE_SURROGATE_LOW_SUP,
    UNICODE_SURROGATE_HIGH_PLANE_9_MIN,
    UNICODE_SURROGATE_HIGH_PLANE_9_SUP,
    UNICODE_SURROGATE_HIGH_PLANE_A_MIN,
    UNICODE_SURROGATE_HIGH_PLANE_A_SUP,

    MULTIPAIR_PROGRAMMABLE_N_BITS_HIGH,
    MULTIPAIR_PROGRAMMABLE_N_BITS_LOW,

    high_surrogate_is_utf_16k,
    high_surrogate_utf_16k_is_continuation,
    MULTIPAIR_OVERLONG_MASKS_4,
    MULTIPAIR_OVERLONG_4_LOW_MIN,
    MULTIPAIR_OVERLONG_MASKS,
)
from .UTF16KInt import UTF16KInt

class UTF16KIncrementalDecoder:
    def __init__(self) -> None:
        self._results:      list[UTF16KInt] = []
        self._words_buffer: list[int]        = []

        self._generator = self._parse_forever()
        self._wakeup()

    def __iter__(self) -> Generator[UTF16KInt, None, None]:
        # queue
        while self._results:
            yield self._results.pop(0)

    def feed(self, utf_16k_words: tuple[int]) -> None:
        self._words_buffer += list(utf_16k_words)
        self._wakeup()

    def close(self) -> None:
        """
        Close the parser.

        Raises EOFError if we are part way through parsing a UTF-16K code unit.

        Otherwise returns `None`.
        """
        self._generator.close()

    def _wakeup(self) -> None:
        self._generator.send(None)

    def _await_should_parse_again(self) -> Generator[None, None, None]:
        while not self._words_buffer:
            yield

    def _await_words(self, n_words: int) -> Generator[None, None, tuple[int]]:
        while len(self._words_buffer) < n_words:
            yield

        ret                = tuple(self._words_buffer[:n_words])
        self._words_buffer = self._words_buffer[n_words:]

        return ret

    def _await_word(self) -> Generator[None, None, int]:
        return (yield from self._await_words(1))[0]

    def _await_continuation_high_surrogate(self) -> Generator[None, None, int]:
        ret = yield from self._await_word()
        if not word_is_high_surrogate(ret):
            if word_is_low_surrogate(ret):
                self._on_error_unexpected_low_surrogate_word()
            else:
                self._unpop_word(ret)
                self._on_error_unexpected_non_surrogate()
        if not high_surrogate_is_utf_16k(ret):
            self._unpop_word(ret)
            self._on_error_unexpected_high_surrogate_non_plane_13()
        if not high_surrogate_utf_16k_is_continuation(ret):
            self._unpop_word(ret)
            self._on_error_unexpected_high_surrogate_plane_13_non_continuation()
        return ret

    def _await_low_surrogate(self) -> Generator[None, None, int]:
        ret = yield from self._await_word()
        if not word_is_low_surrogate(ret):
            self._unpop_word(ret)
            self._on_error_unexpected_high_surrogate_word()
        return ret

    def _unpop_words(self, b: tuple[int]) -> None:
        self._words_buffer = list(b) + self._words_buffer

    def _unpop_word(self, c: int) -> None:
        self._unpop_words((c,))

    def _on_error(self, error_message: str) -> None:
        raise ValueError(error_message)

    def _on_error_unexpected_high_surrogate_plane_13_non_continuation(self) -> None:
        # XXX TODO 101: should we create / raise a ReplacementCharacterException?
        #               thus should we be calling return on the `_on_error`
        #               functions instead of just calling them?
        self._on_error("Unexpected non-continuation plane-13 high surrogate")

    def _on_error_unexpected_high_surrogate_non_plane_13(self) -> None:
        # XXX TODO 101: should we create / raise a ReplacementCharacterException?
        #               thus should we be calling return on the `_on_error`
        #               functions instead of just calling them?
        self._on_error("Unexpected non-plane-13 high surrogate")

    def _on_error_unexpected_non_surrogate(self) -> None:
        # XXX TODO 101: should we create / raise a ReplacementCharacterException?
        #               thus should we be calling return on the `_on_error`
        #               functions instead of just calling them?
        self._on_error("Unexpected non-surrogate")

    def _on_error_unexpected_low_surrogate_word(self) -> None:
        # XXX TODO 101: should we create / raise a ReplacementCharacterException?
        #               thus should we be calling return on the `_on_error`
        #               functions instead of just calling them?
        self._on_error("Unexpected low surrogate")

    def _on_error_unexpected_high_surrogate_word(self) -> None:
        # XXX TODO 101: should we create / raise a ReplacementCharacterException?
        #               thus should we be calling return on the `_on_error`
        #               functions instead of just calling them?
        self._on_error("Unexpected high surrogate")

    def _on_error_overlong(self) -> None:
        # XXX TODO 101: read all following continuation bytes to skip them
        self._on_error("Overlong encoding")

    def _parse_once_one_word(self, parsed_words: list[UTF16KWord], word: int) -> None:
        # `word` belongs to
        # U+0000 to U+D7FF ( pre-surrogates)
        # or
        # U+E000 to U+FFFF (post-surrogates)
        # Nothing further to do
        parsed_words.append(UTF16KWord.SingleWord(word))

    def _parse_once_one_pair(self, parsed_words: list[UTF16KWord], word: int) -> Generator[None, None, None]:
        # `word` belongs to
        # U+D800 to U+D9FF (planes  1 to 8)
        # or
        # U+DA80 to U+DBFF (planes 11 to 16)
        pair_high = word
        pair_low  = yield from self._await_low_surrogate()
        parsed_words.append(UTF16KWord.HighSurrogateNonUTF16K(pair_high))
        parsed_words.append(UTF16KWord.LowSurrogateNonUTF16K(pair_low))

    def _parse_once_multi_pair(self, parsed_words: list[UTF16KWord], word: int) -> Generator[None, None, None]:
        # `word` belongs to
        # U+DA00 to U+DA3F (plane 9)
        start_pair_high = word
        start_pair_low  = yield from self._await_low_surrogate()

        n_words_expected = 4 # XXX check this

        idx_0 = idx_highest_zero(start_pair_high, MULTIPAIR_PROGRAMMABLE_N_BITS_HIGH)
        n_words_expected += 2 * n_start_bits_ones(idx_0, MULTIPAIR_PROGRAMMABLE_N_BITS_HIGH)

        if idx_0 == 5:
            # special case wrt mandatory content bits
            mask_high, mask_low = MULTIPAIR_OVERLONG_MASKS_4

            # if not mask_high & start_pair_high and not mask_low & start_pair_low and start_pair_low < MULTIPAIR_OVERLONG_4_MIN:
            if not mask_high & start_pair_high and start_pair_low < MULTIPAIR_OVERLONG_4_LOW_MIN:
                self._on_error_overlong()

            parsed_words.append(UTF16KWord.UTF16KHighSurrogate(start_pair_high, is_continuation_pair_word = False, is_start_pair_word = True, n_bits_content_total = idx_0, n_bits_content_mandatory = idx_0))
            parsed_words.append(UTF16KWord.UTF16KLowSurrogate(start_pair_low, is_continuation_pair_word = False, is_start_pair_word = True, n_bits_content_total = 10, n_bits_content_mandatory = 5))

            while len(parsed_words) < n_words_expected:
                # Only 2 more
                # Add the rest of the purely-content continuation bytes,
                # which have no mandatory content.
                pair_high = yield from self._await_continuation_high_surrogate()
                parsed_words.append(UTF16KWord.UTF16KHighSurrogateContinuationNonStartNotFirst(pair_high))
                # XXX not really accurate, not a NotFirst, it is First, just like 2-byte UTF-16K decoder
                pair_low = yield from self._await_low_surrogate()
                parsed_words.append(UTF16KWord.UTF16KLowSurrogateContinuationNonStartNotFirst(pair_low))
                # XXX not really accurate, not a NotFirst, it is First, just like 2-byte UTF-16K decoder

            return

        elif idx_0 != -1:
            # Start bits end in first pair high surrogate
            is_final_start_pair_a_continuation_pair            = False
            final_start_pair_n_bits_content_high               = idx_0
            final_start_pair_n_bits_content_low                = MULTIPAIR_PROGRAMMABLE_N_BITS_LOW
            final_start_pair_n_bits_content_mandatory_high     = idx_0
            final_start_pair_n_bits_content_mandatory_low      = MULTIPAIR_PROGRAMMABLE_N_BITS_LOW
            first_non_start_pair_n_bits_content_mandatory_high = 5 - idx_0
            first_non_start_pair_n_bits_content_mandatory_low  = 0

            idx_overlong = MULTIPAIR_PROGRAMMABLE_N_BITS_LOW + idx_0
        else:
            idx_0 = idx_highest_zero(start_pair_low, MULTIPAIR_PROGRAMMABLE_N_BITS_LOW)
            n_words_expected += 2 * n_start_bits_ones(idx_0, MULTIPAIR_PROGRAMMABLE_N_BITS_LOW)

            if idx_0 != -1:
                # Start bits end in first pair low surrogate
                is_final_start_pair_a_continuation_pair            = False
                final_start_pair_n_bits_content_high               = 0
                final_start_pair_n_bits_content_low                = idx_0
                final_start_pair_n_bits_content_mandatory_high     = 0
                final_start_pair_n_bits_content_mandatory_low      = idx_0
                first_non_start_pair_n_bits_content_mandatory_high = MULTIPAIR_PROGRAMMABLE_N_BITS_HIGH
                first_non_start_pair_n_bits_content_mandatory_low  = 9 - idx_0

                idx_overlong = idx_0
            else:
                is_final_start_pair_a_continuation_pair = True

                parsed_words.append(UTF16KWord.UTF16KHighSurrogateFirstFilled())
                parsed_words.append(UTF16KWord.UTF16KLowSurrogateFirstFilled())

                while True:
                    start_pair_high = yield from self._await_continuation_high_surrogate()
                    start_pair_low  = yield from self._await_low_surrogate()

                    idx_0 = idx_highest_zero(start_pair_high, MULTIPAIR_PROGRAMMABLE_N_BITS_HIGH)
                    n_words_expected += 2 * n_start_bits_ones(idx_0, MULTIPAIR_PROGRAMMABLE_N_BITS_HIGH)

                    if idx_0 != -1:
                        # Start bits end in continuation pair high surrogate
                        final_start_pair_n_bits_content_high               = idx_0
                        final_start_pair_n_bits_content_low                = MULTIPAIR_PROGRAMMABLE_N_BITS_LOW
                        final_start_pair_n_bits_content_mandatory_high     = idx_0
                        final_start_pair_n_bits_content_mandatory_low      = MULTIPAIR_PROGRAMMABLE_N_BITS_LOW
                        first_non_start_pair_n_bits_content_mandatory_high = 5 - idx_0
                        first_non_start_pair_n_bits_content_mandatory_low  = 0

                        idx_overlong = MULTIPAIR_PROGRAMMABLE_N_BITS_LOW + idx_0
                        break
                    else:
                        idx_0 = idx_highest_zero(start_pair_low, MULTIPAIR_PROGRAMMABLE_N_BITS_LOW)
                        n_words_expected += 2 * n_start_bits_ones(idx_0, MULTIPAIR_PROGRAMMABLE_N_BITS_LOW)

                        if idx_0 != -1:
                            # Start bits end in continuation pair low surrogate
                            final_start_pair_n_bits_content_high               = 0
                            final_start_pair_n_bits_content_low                = idx_0
                            final_start_pair_n_bits_content_mandatory_high     = 0
                            final_start_pair_n_bits_content_mandatory_low      = idx_0
                            first_non_start_pair_n_bits_content_mandatory_high = MULTIPAIR_PROGRAMMABLE_N_BITS_HIGH
                            first_non_start_pair_n_bits_content_mandatory_low  = 9 - idx_0

                            idx_overlong = idx_0
                            break
                        else:
                            parsed_words.append(UTF16KWord.UTF16KHighSurrogateContinuationFilled())
                            parsed_words.append(UTF16KWord.UTF16KLowSurrogateContinuationFilled())

        masks = MULTIPAIR_OVERLONG_MASKS[idx_overlong]
        m1, m2, m3, m4 = masks

        if not idx_overlong < 15:
            # 1 2

            if not (m1 & start_pair_high | m2 & start_pair_low):
                self._on_error_overlong()

            first_non_start_pair_high = yield from self._await_continuation_high_surrogate()
            first_non_start_pair_low  = yield from self._await_low_surrogate()
        else:
            first_non_start_pair_high = yield from self._await_continuation_high_surrogate()

            if not idx_overlong < 9:
                if not idx_overlong < 11:
                    # 1 2 3
                    if not (m1 & start_pair_high | m2 & start_pair_low | m3 & first_non_start_pair_high):
                        self._on_error_overlong()
                else:
                    # 2 3
                    if not (m2 & start_pair_low | m3 & first_non_start_pair_high):
                        self._on_error_overlong()

                first_non_start_pair_low = yield from self._await_low_surrogate()
            else:
                first_non_start_pair_low = yield from self._await_low_surrogate()

                if not idx_overlong < 1:
                    # 2 3 4
                    if not (m2 & start_pair_low | m3 & first_non_start_pair_high | m4 & first_non_start_pair_low):
                        self._on_error_overlong()
                else:
                    # 3 4
                    if not (m3 & first_non_start_pair_high | m4 & first_non_start_pair_low):
                        self._on_error_overlong()

        parsed_words.append(UTF16KWord.UTF16KHighSurrogate(
            start_pair_high,
            is_continuation_pair_word = is_final_start_pair_a_continuation_pair,
            is_start_pair_word = True,
            n_bits_content_total     = final_start_pair_n_bits_content_high,
            n_bits_content_mandatory = final_start_pair_n_bits_content_mandatory_high,
        ))

        parsed_words.append(UTF16KWord.UTF16KLowSurrogate(
            start_pair_low,
            is_continuation_pair_word = is_final_start_pair_a_continuation_pair,
            is_start_pair_word = True,
            n_bits_content_total     = final_start_pair_n_bits_content_low,
            n_bits_content_mandatory = final_start_pair_n_bits_content_mandatory_low,
        ))

        parsed_words.append(UTF16KWord.UTF16KHighSurrogateContinuationNonStartFirst(
            first_non_start_pair_high,
            n_bits_content_mandatory = first_non_start_pair_n_bits_content_mandatory_high,
        ))

        parsed_words.append(UTF16KWord.UTF16KLowSurrogateContinuationNonStartFirst(
            first_non_start_pair_low,
            n_bits_content_mandatory = first_non_start_pair_n_bits_content_mandatory_low,
        ))

        while len(parsed_words) < n_words_expected:
            pair_high = yield from self._await_continuation_high_surrogate()
            pair_low  = yield from self._await_low_surrogate()
            parsed_words.append(UTF16KWord.UTF16KHighSurrogateContinuationNonStartNotFirst(pair_high))
            parsed_words.append(UTF16KWord.UTF16KLowSurrogateContinuationNonStartNotFirst(pair_low))

    def _parse_once(self) -> Generator[None, None, UTF16KInt]:
        parsed_words: list[UTF16KWord] = []

        start_word = yield from self._await_word()

        if start_word < UNICODE_SURROGATE_HIGH_MIN:
            # U+0000 to U+D7FF
            # One word
            self._parse_once_one_word(parsed_words, start_word)

        elif start_word < UNICODE_SURROGATE_LOW_SUP:
            # U+D800 to U+DFFF
            # The surrogate range

            if start_word < UNICODE_SURROGATE_HIGH_SUP:
                # U+D800 to U+DBFF
                # High surrogate

                if start_word < UNICODE_SURROGATE_HIGH_PLANE_9_MIN:
                    # U+D800 to U+D9FF
                    # Planes 1 to 8
                    yield from self._parse_once_one_pair(parsed_words, start_word)

                elif start_word < UNICODE_SURROGATE_HIGH_PLANE_A_SUP:
                    # U+DA00 to U+DA7F
                    # Planes 9 and 10

                    if start_word < UNICODE_SURROGATE_HIGH_PLANE_A_MIN:
                        # U+DA00 to U+DA3F
                        # High surrogate of first pair
                        yield from self._parse_once_multi_pair(parsed_words, start_word)

                    else:
                        # U+DA40 to U+DA7F
                        # High surrogate of continuation pair
                        self._on_error("Invalid high surrogate for first of multipair UTF-16K")

                else:
                    # U+DA80 to U+DBFF
                    # Planes 11 to 16
                    yield from self._parse_once_one_pair(parsed_words, start_word)

            else:
                # U+DC00 to U+DFFF
                # Low surrogate
                self._on_error_unexpected_low_surrogate_word()

        else:
            # U+E000 to U+FFFF
            # One word
            self._parse_once_one_word(parsed_words, start_word)

        return UTF16KInt(parsed_words)

    def _parse_forever(self) -> Generator[None, None, None]:
        while True:
            try:
                yield from self._await_should_parse_again()
                # Park the generator in this 'parking lot' so that
                # if `close()` is called on the generator at this point
                # it's not an error, whereas if we are in the middle of
                # parsing a UTF-16K code unit below that *should* be an
                # EOFError if `close()` is called early.
            except GeneratorExit:
                return
            try:
                x = yield from self._parse_once()
            except GeneratorExit as e:
                raise EOFError("Partially decoded UTF-16K code unit didn't finish") from e
            else:
                self._results.append(x)
