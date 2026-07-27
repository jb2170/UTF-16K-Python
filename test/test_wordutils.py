import unittest

from UTF16K.wordutils import remap_word

class TestRemap(unittest.TestCase):
    def test_all(self):
        original = set(range(1 << 16))
        mapped   = set()

        for i in original:
            mapped.add(remap_word(i))

        self.assertEqual(original, mapped)
