from . import color

# size_t counting num of words; this is the only machine limitation
# little bittian ordered (1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768)

### Common

ZERO = 0b00000000_00000000

N_BYTES_IN_WORD = 2

N_BITS_IN_BYTE = 8
N_BITS_IN_WORD = 16

### UCS-2

UCS_2_SELF_SYNC_N_BITS = 0

UCS_2_PROGRAMMABLE_N_BITS = 16

### UTF-16

SURROGATE_FRAME_MASK        = 0b11111100_00000000
SURROGATE_FRAME_BITS_HIGH   = 0b11011000_00000000
SURROGATE_FRAME_BITS_LOW    = 0b11011100_00000000
SURROGATE_PROGRAMMABLE_MASK = 0b00000011_11111111
SURROGATE_HIGH_PLANE_MASK   = 0b00000011_11000000

SURROGATE_FRAME_N_BITS        = 6
SURROGATE_PROGRAMMABLE_N_BITS = 10
SURROGATE_WORDS_IN_PAIR       = 2

SURROGATE_PAIR_CODEPOINT_OFFSET = 0x1_0000

### UTF-16K

MULTIPAIR_HIGH_PLANE_MASK = 0b00000011_10000000
MULTIPAIR_HIGH_PLANE_BITS = 0b00000010_00000000

MULTIPAIR_SELF_SYNC_MASK              = 0b00000000_01000000
MULTIPAIR_SELF_SYNC_BITS_FIRST        = 0b00000000_00000000
MULTIPAIR_SELF_SYNC_BITS_CONTINUATION = 0b00000000_01000000

MULTIPAIR_PROGRAMMABLE_MASK_HIGH = 0b00000000_00111111
MULTIPAIR_PROGRAMMABLE_MASK_LOW  = 0b00000011_11111111
MULTIPAIR_PROGRAMMABLE_N_BITS_HIGH  =  6
MULTIPAIR_PROGRAMMABLE_N_BITS_LOW   = 10
MULTIPAIR_PROGRAMMABLE_N_BITS_TOTAL = 16
MULTIPAIR_PROGRAMMABLE_INT_MASK = 0b11111111_11111111

MULTIPAIR_SELF_PUNCTUATION_ONES_FULL = (0b00000000_00111111, 0b00000011_11111111)
MULTIPAIR_SELF_PUNCTUATION_ONES_SOME = (
    (0b00000000_00000000, 0b00000000_00000000),
    (0b00000000_00100000, 0b00000000_00000000),
    (0b00000000_00110000, 0b00000000_00000000),
    (0b00000000_00111000, 0b00000000_00000000),
    (0b00000000_00111100, 0b00000000_00000000),
    (0b00000000_00111110, 0b00000000_00000000),
    (0b00000000_00111111, 0b00000000_00000000),
    (0b00000000_00111111, 0b00000010_00000000),
    (0b00000000_00111111, 0b00000011_00000000),
    (0b00000000_00111111, 0b00000011_10000000),
    (0b00000000_00111111, 0b00000011_11000000),
    (0b00000000_00111111, 0b00000011_11100000),
    (0b00000000_00111111, 0b00000011_11110000),
    (0b00000000_00111111, 0b00000011_11111000),
    (0b00000000_00111111, 0b00000011_11111100),
    (0b00000000_00111111, 0b00000011_11111110),
)

MULTIPAIR_FILLED_FIRST_HIGH        = 0b11011010_00111111
MULTIPAIR_FILLED_FIRST_LOW         = 0b11011111_11111111
MULTIPAIR_FILLED_CONTINUATION_HIGH = 0b11011010_01111111
MULTIPAIR_FILLED_CONTINUATION_LOW  = 0b11011111_11111111

### Anti-Overlong Checking

MULTIPAIR_OVERLONG_MASKS_4   = (0b00000000_00011111, 0b00000011_11100000)
MULTIPAIR_OVERLONG_4_LOW_MIN =                       0b11011100_00010001

MULTIPAIR_OVERLONG_MASKS = (
    (0b00000000_00000000, 0b00000000_00000000, 0b00000000_00111111, 0b00000011_11111110),
    (0b00000000_00000000, 0b00000000_00000001, 0b00000000_00111111, 0b00000011_11111100),
    (0b00000000_00000000, 0b00000000_00000011, 0b00000000_00111111, 0b00000011_11111000),
    (0b00000000_00000000, 0b00000000_00000111, 0b00000000_00111111, 0b00000011_11110000),
    (0b00000000_00000000, 0b00000000_00001111, 0b00000000_00111111, 0b00000011_11100000),
    (0b00000000_00000000, 0b00000000_00011111, 0b00000000_00111111, 0b00000011_11000000),
    (0b00000000_00000000, 0b00000000_00111111, 0b00000000_00111111, 0b00000011_10000000),
    (0b00000000_00000000, 0b00000000_01111111, 0b00000000_00111111, 0b00000011_00000000),
    (0b00000000_00000000, 0b00000000_11111111, 0b00000000_00111111, 0b00000010_00000000),
    (0b00000000_00000000, 0b00000001_11111111, 0b00000000_00111111, 0b00000000_00000000),
    (0b00000000_00000000, 0b00000011_11111111, 0b00000000_00111110, 0b00000000_00000000),
    (0b00000000_00000001, 0b00000011_11111111, 0b00000000_00111100, 0b00000000_00000000),
    (0b00000000_00000011, 0b00000011_11111111, 0b00000000_00111000, 0b00000000_00000000),
    (0b00000000_00000111, 0b00000011_11111111, 0b00000000_00110000, 0b00000000_00000000),
    (0b00000000_00001111, 0b00000011_11111111, 0b00000000_00100000, 0b00000000_00000000),
    (0b00000000_00011111, 0b00000011_11111111, 0b00000000_00000000, 0b00000000_00000000),
)

###

### Unicode Ranges

# MIN = minimum
# SUP = supremum (ie not inclusive)
UNICODE_MIN = 0x0
UNICODE_SUP = 0x11_0000

UTF_16_1_WORD_SUP = 0x1_0000

UNICODE_PLANE_9_MIN = 0x9_0000
UNICODE_PLANE_9_SUP = 0xA_0000
UNICODE_PLANE_A_MIN = 0xA_0000
UNICODE_PLANE_A_SUP = 0xB_0000

UNICODE_SURROGATE_HIGH_MIN = 0xD800
UNICODE_SURROGATE_HIGH_SUP = 0xDC00
UNICODE_SURROGATE_LOW_MIN  = 0xDC00
UNICODE_SURROGATE_LOW_SUP  = 0xE000

UNICODE_SURROGATE_HIGH_PLANE_9_MIN = 0xDA00 # First        Plane
UNICODE_SURROGATE_HIGH_PLANE_9_SUP = 0xDA40 # First        Plane
UNICODE_SURROGATE_HIGH_PLANE_A_MIN = 0xDA40 # Continuation Plane
UNICODE_SURROGATE_HIGH_PLANE_A_SUP = 0xDA80 # Continuation Plane

def ceil_div(x: int, y: int) -> int:
    return -(x // -y)

def fill_n_bits_shifted_by_m(n: int, m: int) -> int:
    pass         # example with n == 3, m == 4
    ret = 1      # 0b00000001
    ret <<= n    # 0b00001000
    ret -= 1     # 0b00000111
    ret <<= m    # 0b01110000
    return ret

def extract_n_bits_at_m(x: int, n: int, m: int, downshift: bool = True):
    pass                                  # example with n == 3, m == 4, downshift == True
    ret = x                               # 0bABCDEFGH
    mask = fill_n_bits_shifted_by_m(n, m) # 0b01110000
    ret &= mask                           # 0b0BCD0000
    if downshift:                         #
        ret >>= m                         # 0b00000BCD
    return ret

def word_is_high_surrogate(word: int) -> bool:
    return word & SURROGATE_FRAME_MASK == SURROGATE_FRAME_BITS_HIGH

def word_is_low_surrogate(word: int) -> bool:
    return word & SURROGATE_FRAME_MASK == SURROGATE_FRAME_BITS_LOW

def high_surrogate_is_utf_16k(high_surrogate: int) -> bool:
    return high_surrogate & MULTIPAIR_HIGH_PLANE_MASK == MULTIPAIR_HIGH_PLANE_BITS

def high_surrogate_utf_16k_is_continuation(high_surrogate_plane_13: int) -> bool:
    return high_surrogate_plane_13 & MULTIPAIR_SELF_SYNC_MASK == MULTIPAIR_SELF_SYNC_BITS_CONTINUATION

def int_find_highest_zero(c: int, n_bits: int) -> int:
    """
    Return the index of the highest 0 bit in the lowest `n_bits` of `c`.

    Returns -1 if a 0 bit is not found.
    """
    ret = n_bits - 1
    mask = 1 << ret
    for _ in range(n_bits):
        if not mask & c:
            break
        mask >>= 1
        ret -= 1
    return ret

def int_find_highest_one(c: int, n_bits: int) -> int:
    """
    Find the highest 1 in the lowest `n_bits` of `c`.

    Returns -1 if a 1 bit is not found.
    """
    ret = n_bits - 1
    mask = 1 << ret
    for _ in range(n_bits):
        if mask & c:
            break
        mask >>= 1
        ret -= 1
    return ret

def idx_highest_zero(c: int, n_bits: int) -> int:
    """
    Return the index of the highest 0 bit in the lowest `n_bits` of `c`.

    Returns -1 if a 0 bit is not found.
    """

    return int_find_highest_zero(c, n_bits)

def n_start_bits_ones(idx_0: int, n_bits: int) -> int:
    """
    Pass in `idx_0`, the result of calling `idx_highest_zero` with `n_bits`.

    Returns the number of extra bytes we expect in a code unit
    having read a 0 bit at `idx_0`, ie how many 1 bits there are
    above `idx_0` in the window of `n_bits`.
    """

    return (n_bits - 1) - idx_0

class UTF16KWord:
    def __init__(self, c: int, *,
        is_surrogate:              bool,
        is_utf_16k:     bool,
        is_high_surrogate:         bool,
        is_continuation_pair_word: bool,
        is_start_pair_word:        bool,
        n_bits_content_total:      int,
        n_bits_content_mandatory:  int,
    ) -> None:
        self.c = c
        self.is_surrogate              = is_surrogate
        self.is_utf_16k                = is_utf_16k # XXX this is True even for the low surrogates,
                                                    # which don't have the Plane 9 or A bits
        self.is_high_surrogate         = is_high_surrogate
        self.is_continuation_pair_word = is_continuation_pair_word
        self.is_start_pair_word        = is_start_pair_word # not used, even in UTF-8000?
        self.is_continuation_byte      = is_continuation_pair_word
        self.n_bits_content_total      = n_bits_content_total
        self.n_bits_content_mandatory  = n_bits_content_mandatory

    def __int__(self) -> int:
        return self.c

    def __str__(self) -> str:
        return f"0b{self.c:016b}"

    def __format__(self, format_spec: str) -> str:
        """
        Format the byte to be human readable.

        Format specifiers are comma-separated.

        if 'x' or 'X' is passed then:
            Format in hex.

        elif 'b' or no presentation type is passed then:
            Format in binary.

            if 'color' is passed then:
                Format in color

        if '#' is passed then:
            Prefix the string with the presentation type's prefix
            ('0x', '0X', '0b', '0B')
        """

        format_spec_args = format_spec.split(",")
        # primitive but enough

        do_base_prefix = "#"     in format_spec_args
        do_color       = "color" in format_spec_args

        if 'x' in format_spec_args:
            # Return hex digits.
            str_base_prefix = "0x" if do_base_prefix else ""
            return f"{str_base_prefix}{self.c:02x}"
        elif 'X' in format_spec_args:
            # Return HEX digits.
            str_base_prefix = "0X" if do_base_prefix else ""
            return f"{str_base_prefix}{self.c:02X}"

        if 'B' in format_spec_args:
            str_base_prefix = "0B" if do_base_prefix else ""
        else:
            str_base_prefix = "0b" if do_base_prefix else ""

        n_bits_content_total     = self.n_bits_content_total
        n_bits_content_mandatory = self.n_bits_content_mandatory
        n_bits_content_optional  = n_bits_content_total - n_bits_content_mandatory

        if not self.is_surrogate:
            n_bits_surrogate_frame = 0
            n_bits_plane_marker    = 0
            n_bits_self_sync       = 0
            n_bits_start           = 0
        else:
            n_bits_surrogate_frame = SURROGATE_FRAME_N_BITS
            if not self.is_utf_16k:
                # single surrogate pair
                if self.is_high_surrogate:
                    n_bits_plane_marker      = 4
                    n_bits_content_total    -= n_bits_plane_marker
                    n_bits_content_optional -= n_bits_plane_marker
                else:
                    n_bits_plane_marker = 0
                n_bits_self_sync = 0
                n_bits_start     = 0
            else:
                # multi surrogate pair
                if self.is_high_surrogate:
                    n_bits_plane_marker = 3
                    n_bits_self_sync    = 1
                    n_bits_start        = SURROGATE_PROGRAMMABLE_N_BITS - (n_bits_plane_marker + n_bits_self_sync + n_bits_content_total)
                else:
                    n_bits_plane_marker = 0
                    n_bits_self_sync    = 0
                    n_bits_start        = SURROGATE_PROGRAMMABLE_N_BITS - n_bits_content_total

        str_surrogate_frame = self._format_bit_field(
            n_bits_surrogate_frame, SURROGATE_PROGRAMMABLE_N_BITS,
            color = color.CSI_BOLD + color.CSI_FG_YELLOW, do_color = do_color
        )
        if self.is_utf_16k:
            plane_marker_color = color.CSI_BOLD + color.CSI_FG_RED
        else:
            plane_marker_color = color.CSI_FG_RED
        str_plane_marker = self._format_bit_field(
            n_bits_plane_marker, SURROGATE_PROGRAMMABLE_N_BITS - n_bits_plane_marker,
            color = plane_marker_color, do_color = do_color
        )
        str_self_sync_bits = self._format_bit_field(
            n_bits_self_sync, MULTIPAIR_PROGRAMMABLE_N_BITS_HIGH,
            color = color.CSI_BOLD + color.CSI_FG_CYAN, do_color = do_color
        )
        str_start_bits = self._format_bit_field(
            n_bits_start, n_bits_content_total,
            color = color.CSI_BOLD + color.CSI_FG_MAGENTA, do_color = do_color
        )
        str_mandatory_content_bits = self._format_bit_field(
            n_bits_content_mandatory, n_bits_content_optional,
            color = color.CSI_BOLD + color.CSI_FG_GREEN, do_color = do_color
        )
        str_optional_content_bits = self._format_bit_field(
            n_bits_content_optional, 0,
            color = color.CSI_FG_GREEN, do_color = do_color
        )

        return f"{str_base_prefix}{str_surrogate_frame}{str_plane_marker}{str_self_sync_bits}{str_start_bits}{str_mandatory_content_bits}{str_optional_content_bits}"

    def _format_bit_field(
        self, width: int, offset: int,
        *,
        color: str = None, do_color: bool = False
    ) -> str:
        if width == 0:
            # Normal string formatting of zero returns "0" but we want "".
            return ""

        data = extract_n_bits_at_m(self.c, width, offset)

        ret = f"{data:0{width}b}"

        if do_color:
            CSI_RESET = "\x1b[0m"
            ret = f"{color}{ret}{CSI_RESET}"

        return ret

    @property
    def is_content_word(self) -> bool:
        return self.n_bits_content_total > 0

    @property
    def content(self) -> int:
        content_mask = fill_n_bits_shifted_by_m(self.n_bits_content_total, 0)

        return self.c & content_mask

    @classmethod
    def SingleWord(cls, c: int):
        """
        Return a single UCS-2 word '0bxxxxxxxx_xxxxxxxx'.
        """
        return cls(
            c,
            is_surrogate = False,
            is_utf_16k = False,
            is_high_surrogate = False,
            is_continuation_pair_word = False,
            is_start_pair_word = False,
            n_bits_content_total = 16,
            n_bits_content_mandatory = 0,
        )

    @classmethod
    def HighSurrogateNonUTF16K(cls, c: int):
        """
        Return a UTF-16 high surrogate '0b110110xx_xxxxxxxx'.
        """
        return cls(
            c,
            is_surrogate = True,
            is_utf_16k = False,
            is_high_surrogate = True,
            is_continuation_pair_word = False,
            is_start_pair_word = False,
            n_bits_content_total = 10,
            n_bits_content_mandatory = 0,
        )

    @classmethod
    def LowSurrogateNonUTF16K(cls, c: int):
        """
        Return a UTF-16 low surrogate '0b110111xx_xxxxxxxx'.
        """
        return cls(
            c,
            is_surrogate = True,
            is_utf_16k = False,
            is_high_surrogate = False,
            is_continuation_pair_word = False,
            is_start_pair_word = False,
            n_bits_content_total = 10,
            n_bits_content_mandatory = 0,
        )

    @classmethod
    def UTF16KHighSurrogate(cls, c: int, *,
        is_continuation_pair_word: bool,
        is_start_pair_word:        bool,
        n_bits_content_total:      int,
        n_bits_content_mandatory:  int,
    ):
        """
        Return a UTF-16K high surrogate '0b11011010_0xxxxxxx'.
        """
        return cls(
            c,
            is_surrogate = True,
            is_utf_16k = True,
            is_high_surrogate = True,
            is_continuation_pair_word = is_continuation_pair_word,
            is_start_pair_word = is_start_pair_word,
            n_bits_content_total = n_bits_content_total,
            n_bits_content_mandatory = n_bits_content_mandatory,
        )

    @classmethod
    def UTF16KLowSurrogate(cls, c: int, *,
        is_continuation_pair_word: bool,
        is_start_pair_word:        bool,
        n_bits_content_total:      int,
        n_bits_content_mandatory:  int,
    ):
        """
        Return a UTF-16K low surrogate '0b110111xx_xxxxxxxx'.
        """
        return cls(
            c,
            is_surrogate = True,
            is_utf_16k = True,
            is_high_surrogate = False,
            is_continuation_pair_word = is_continuation_pair_word,
            is_start_pair_word = is_start_pair_word,
            n_bits_content_total = n_bits_content_total,
            n_bits_content_mandatory = n_bits_content_mandatory,
        )

    @classmethod
    def UTF16KHighSurrogateFirstFilled(cls):
        """
        Return a filled UTF-16K first-pair high surrogate '0b11011010_00111111'.
        """
        return cls.UTF16KHighSurrogate(
            MULTIPAIR_FILLED_FIRST_HIGH,
            is_continuation_pair_word = False,
            is_start_pair_word = True,
            n_bits_content_total = 0,
            n_bits_content_mandatory = 0,
        )

    @classmethod
    def UTF16KLowSurrogateFirstFilled(cls):
        """
        Return a filled UTF-16K first-pair low surrogate '0b11011111_11111111'.
        """
        return cls.UTF16KLowSurrogate(
            MULTIPAIR_FILLED_FIRST_LOW,
            is_continuation_pair_word = False,
            is_start_pair_word = True,
            n_bits_content_total = 0,
            n_bits_content_mandatory = 0,
        )

    @classmethod
    def UTF16KHighSurrogateContinuationFilled(cls):
        """
        Return a filled UTF-16K continuation-pair high surrogate '0b11011010_01111111'.
        """
        return cls.UTF16KHighSurrogate(
            MULTIPAIR_FILLED_CONTINUATION_HIGH,
            is_continuation_pair_word = True,
            is_start_pair_word = True,
            n_bits_content_total = 0,
            n_bits_content_mandatory = 0,
        )

    @classmethod
    def UTF16KLowSurrogateContinuationFilled(cls):
        """
        Return a filled UTF-16K continuation-pair low surrogate '0b11011111_11111111'.
        """
        return cls.UTF16KLowSurrogate(
            MULTIPAIR_FILLED_CONTINUATION_LOW,
            is_continuation_pair_word = True,
            is_start_pair_word = True,
            n_bits_content_total = 0,
            n_bits_content_mandatory = 0,
        )

    @classmethod
    def UTF16KHighSurrogateContinuationNonStartFirst(cls, c: int, *, n_bits_content_mandatory: int):
        return cls.UTF16KHighSurrogate(
            c,
            is_continuation_pair_word = True,
            is_start_pair_word = False,
            n_bits_content_total = MULTIPAIR_PROGRAMMABLE_N_BITS_HIGH,
            n_bits_content_mandatory = n_bits_content_mandatory,
        )

    @classmethod
    def UTF16KLowSurrogateContinuationNonStartFirst(cls, c: int, *, n_bits_content_mandatory: int):
        return cls.UTF16KLowSurrogate(
            c,
            is_continuation_pair_word = True,
            is_start_pair_word = False,
            n_bits_content_total = MULTIPAIR_PROGRAMMABLE_N_BITS_LOW,
            n_bits_content_mandatory = n_bits_content_mandatory,
        )

    @classmethod
    def UTF16KHighSurrogateContinuationNonStartNotFirst(cls, c: int):
        """
        Return a UTF-16K continuation high surrogate '0b11011010_01xxxxxx'.
        """
        return cls.UTF16KHighSurrogate(
            c,
            is_continuation_pair_word = True,
            is_start_pair_word = False,
            n_bits_content_total = MULTIPAIR_PROGRAMMABLE_N_BITS_HIGH,
            n_bits_content_mandatory = 0,
        )

    @classmethod
    def UTF16KLowSurrogateContinuationNonStartNotFirst(cls, c: int):
        """
        Return a UTF-16K continuation low surrogate '0b110111xx_xxxxxxxx'.
        """
        return cls.UTF16KLowSurrogate(
            c,
            is_continuation_pair_word = True,
            is_start_pair_word = False,
            n_bits_content_total = MULTIPAIR_PROGRAMMABLE_N_BITS_LOW,
            n_bits_content_mandatory = 0,
        )
