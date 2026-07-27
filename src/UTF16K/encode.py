from .UTF16KWord import (
    UNICODE_SURROGATE_HIGH_MIN,
    UNICODE_SURROGATE_HIGH_SUP,
    UNICODE_SURROGATE_LOW_MIN,
    UNICODE_SURROGATE_LOW_SUP,
    UTF_16_1_WORD_SUP,
    UNICODE_PLANE_9_MIN,
    UNICODE_PLANE_9_SUP,
    UNICODE_PLANE_A_MIN,
    UNICODE_PLANE_A_SUP,
    UNICODE_SUP,
    SURROGATE_PAIR_CODEPOINT_OFFSET,

    MULTIPAIR_PROGRAMMABLE_MASK_HIGH,
    MULTIPAIR_PROGRAMMABLE_MASK_LOW,
    MULTIPAIR_PROGRAMMABLE_N_BITS_HIGH,
    MULTIPAIR_PROGRAMMABLE_N_BITS_LOW,

    SURROGATE_FRAME_BITS_HIGH,
    SURROGATE_FRAME_BITS_LOW,
    SURROGATE_PROGRAMMABLE_MASK,
    SURROGATE_PROGRAMMABLE_N_BITS,
    MULTIPAIR_HIGH_PLANE_BITS,
    MULTIPAIR_SELF_SYNC_BITS_FIRST,
    MULTIPAIR_SELF_SYNC_BITS_CONTINUATION,
    MULTIPAIR_PROGRAMMABLE_N_BITS_TOTAL,
    MULTIPAIR_PROGRAMMABLE_INT_MASK,
    MULTIPAIR_SELF_PUNCTUATION_ONES_FULL,
    MULTIPAIR_SELF_PUNCTUATION_ONES_SOME,
    ceil_div,
)

def _encode_one_word(ret_ints: list[int], x: int) -> None:
    """
    1-word UTF-16.
    """
    ret_ints.insert(0, x)

def _encode_surrogate_pair(ret_ints: list[int], x: int) -> None:
    """
    2-word (1 surrogate pair) UTF-16.
    """

    y = x - SURROGATE_PAIR_CODEPOINT_OFFSET

    ### Allocate two words:
    ret_ints.append(0)
    ret_ints.append(0)

    ### Add the content bits:
    ret_ints[0] = (y >> 10) & SURROGATE_PROGRAMMABLE_MASK
    ret_ints[1] = (y >>  0) & SURROGATE_PROGRAMMABLE_MASK

    ### Add the surrogate frame bits '110110' and '110111':
    ret_ints[0] |= SURROGATE_FRAME_BITS_HIGH
    ret_ints[1] |= SURROGATE_FRAME_BITS_LOW

def encode(x: int) -> tuple[int]:
    """
    Encode an integer `x` into UTF-16K words.
    """

    if x < 0:
        raise ValueError("Cannot encode negative number")

    ret_ints: list[int] = []

    if x < UTF_16_1_WORD_SUP:
        # U+0000 to U+FFFF
        # UCS-2 1-word

        if x < UNICODE_SURROGATE_HIGH_MIN:
            # U+0000 to U+D7FF
            # Pre surrogate
            _encode_one_word(ret_ints, x)

        elif x < UNICODE_SURROGATE_LOW_SUP:
            # U+D800 to U+DFFF
            # The surrogate range

            if x < UNICODE_SURROGATE_HIGH_SUP:
                # U+D800 to U+DBFF
                # High surrogate
                raise ValueError("High Surrogate not encodable")

            else:
                # U+DC00 to U+DFFF
                # Low surrogate
                raise ValueError("Low Surrogate not encodable")

        else:
            # U+E000 to U+FFFF
            # Post surrogate
            _encode_one_word(ret_ints, x)

    elif x < UNICODE_SUP:
        # U+10000 to U+10FFFF
        # UTF-16 2-word

        if x < UNICODE_PLANE_9_MIN:
            # U+10000 to U+8FFFF
            # Planes 1 to 8
            _encode_surrogate_pair(ret_ints, x)

        elif x < UNICODE_PLANE_A_SUP:
            # U+90000 to U+AFFFF
            # Planes 9 and 10
            # Unencodable because of UTF-16K

            if x < UNICODE_PLANE_9_SUP:
                # U+90000 to U+9FFFF
                # Plane 9
                raise ValueError("Plane 9 not encodable")

            else:
                # U+A0000 to U+AFFFF
                # Plane 10
                raise ValueError("Plane 10 not encodable")

        else:
            # U+B0000 to U+10FFFF
            # Planes 11 to 16
            _encode_surrogate_pair(ret_ints, x)

    else:
        # U+110000 and beyond
        # UTF-16K multi-pair

        n_bits_content_occupied: int = 0
        y: int = x

        ### Add the content bits:
        while y > MULTIPAIR_PROGRAMMABLE_INT_MASK:
            final_10_bits = y & MULTIPAIR_PROGRAMMABLE_MASK_LOW
            ret_ints.insert(0, final_10_bits)
            n_bits_content_occupied += MULTIPAIR_PROGRAMMABLE_N_BITS_LOW
            y >>= MULTIPAIR_PROGRAMMABLE_N_BITS_LOW

            final_6_bits = y & MULTIPAIR_PROGRAMMABLE_MASK_HIGH
            ret_ints.insert(0, final_6_bits)
            n_bits_content_occupied += MULTIPAIR_PROGRAMMABLE_N_BITS_HIGH
            y >>= MULTIPAIR_PROGRAMMABLE_N_BITS_HIGH

        final_16_bits = y

        final_10_bits = y & MULTIPAIR_PROGRAMMABLE_MASK_LOW
        ret_ints.insert(0, final_10_bits)
        y >>= MULTIPAIR_PROGRAMMABLE_N_BITS_LOW

        final_6_bits = y
        ret_ints.insert(0, final_6_bits)

        while final_16_bits > 0:
            n_bits_content_occupied += 1
            final_16_bits >>= 1

        n_pairs_needed = ceil_div(n_bits_content_occupied - 1, 15)
        n_words_needed = 2 * n_pairs_needed

        ret_ints = [0 for _ in range(n_words_needed - len(ret_ints))] + ret_ints

        ### Add the self-punctuation start bits:
        idx_self_punctuation = 0

        n_start_pairs_filled_with_ones, n_ones_in_final_start_pair = divmod(n_pairs_needed - 2, MULTIPAIR_PROGRAMMABLE_N_BITS_TOTAL)
        n_start_words_filled_with_ones = 2 * n_start_pairs_filled_with_ones

        while idx_self_punctuation < n_start_words_filled_with_ones:
            ret_ints[idx_self_punctuation] |= MULTIPAIR_SELF_PUNCTUATION_ONES_FULL[0]
            idx_self_punctuation += 1
            ret_ints[idx_self_punctuation] |= MULTIPAIR_SELF_PUNCTUATION_ONES_FULL[1]
            idx_self_punctuation += 1

        ret_ints[idx_self_punctuation] |= MULTIPAIR_SELF_PUNCTUATION_ONES_SOME[n_ones_in_final_start_pair][0]
        idx_self_punctuation += 1
        ret_ints[idx_self_punctuation] |= MULTIPAIR_SELF_PUNCTUATION_ONES_SOME[n_ones_in_final_start_pair][1]
        idx_self_punctuation += 1

        ### Add the self-synchronization prefixes:
        idx_self_sync = 0

        ret_ints[idx_self_sync] |= MULTIPAIR_SELF_SYNC_BITS_FIRST
        # First word is a noop really, self-sync bits are zero
        idx_self_sync += 1
        # Nothing in low surrogate
        idx_self_sync += 1

        while idx_self_sync < n_words_needed:
            ret_ints[idx_self_sync] |= MULTIPAIR_SELF_SYNC_BITS_CONTINUATION
            idx_self_sync += 1
            # Nothing in low surrogate
            idx_self_sync += 1

        ### Add the high surrogate plane 9 and 10 indicator bits '100':
        idx_plane_9A_indicator = 0

        while idx_plane_9A_indicator < n_words_needed:
            ret_ints[idx_plane_9A_indicator] |= MULTIPAIR_HIGH_PLANE_BITS
            idx_plane_9A_indicator += 1
            # Nothing in low surrogate
            idx_plane_9A_indicator += 1

        ### Add the surrogate frame bits '110110' and '110111':
        idx_surrogate_frame = 0

        while idx_surrogate_frame < n_words_needed:
            ret_ints[idx_surrogate_frame] |= SURROGATE_FRAME_BITS_HIGH
            idx_surrogate_frame += 1
            ret_ints[idx_surrogate_frame] |= SURROGATE_FRAME_BITS_LOW
            idx_surrogate_frame += 1

    return tuple(ret_ints)
