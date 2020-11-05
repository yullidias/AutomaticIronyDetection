# -*- coding: utf-8 -*-

from src.preprocess import Tag
from src.preprocess import tag_ellipsis
from src.preprocess import tag_emoticon_happy
from src.preprocess import tokenize_text
from src.preprocess import remove_especial_chars
from src.preprocess import tag_numbers
from src.preprocess import tag_hashtag
from src.preprocess import tag_emoticon_sad
from src.preprocess import tag_URL
from src.preprocess import tag_plus
from src.preprocess import tag_emoticon_rage
from src.preprocess import tag_at

import unittest


class TestPreprocess(unittest.TestCase):

    def test_tag_reticencias(self):
        self.assertEqual(tag_ellipsis("."), ".")
        self.assertEqual(tag_ellipsis(".."), Tag.ELLIPSIS.value)
        self.assertEqual(tag_ellipsis("..."), Tag.ELLIPSIS.value)
        self.assertEqual(tag_ellipsis("...."), Tag.ELLIPSIS.value)
        self.assertEqual(tag_ellipsis("a......b"),
                         "a"+Tag.ELLIPSIS.value+"b")
        self.assertEqual(tag_ellipsis("a...b"),
                         "a"+Tag.ELLIPSIS.value+"b")

    def test_tag_emoticon_happy(self):
        self.assertEqual(tag_emoticon_happy(":)"), Tag.HAPPY.value)
        self.assertEqual(tag_emoticon_happy(":))"), Tag.HAPPY.value)
        self.assertEqual(tag_emoticon_happy("A:)B"), "A"+Tag.HAPPY.value+"B")
        self.assertEqual(tag_emoticon_happy("A:))))))B"),
                         "A" + Tag.HAPPY.value + "B")
        self.assertEqual(tag_emoticon_happy("=)"), Tag.HAPPY.value)
        self.assertEqual(tag_emoticon_happy("=))"), Tag.HAPPY.value)
        self.assertEqual(tag_emoticon_happy(":3"), Tag.HAPPY.value)

    def test_tokenize_text(self):
        self.assertEqual(tokenize_text("anti-vírus"), ["anti-vírus"])
        self.assertEqual(tokenize_text("anti aéreo"), ["anti", "aéreo"])

    def test_remove_asterisk(self):
        self.assertEqual(remove_especial_chars('*'), ' ')
        self.assertEqual(remove_especial_chars('****'), ' ')
        self.assertEqual(remove_especial_chars('* *'), '   ')
        self.assertEqual(remove_especial_chars('a*1'), 'a 1')

    def test_tag_numbers(self):
        self.assertEqual(tag_numbers("+351910988936"), Tag.NUMBER.value)
        self.assertEqual(tag_numbers("55 19 3885-8000"), Tag.NUMBER.value)
        self.assertEqual(tag_numbers("08"), Tag.NUMBER.value)
        self.assertEqual(tag_numbers("11"), Tag.NUMBER.value)
        self.assertEqual(tag_numbers("10%"), Tag.NUMBER.value)
        self.assertEqual(tag_numbers("23,37%"), Tag.NUMBER.value)
        self.assertEqual(tag_numbers("100%"), Tag.NUMBER.value)
        self.assertEqual(tag_numbers("100 %"), Tag.NUMBER.value)
        self.assertEqual(tag_numbers("1000000000000%"), Tag.NUMBER.value)
        self.assertEqual(tag_numbers("11-08-2018"), Tag.DATE.value)
        self.assertEqual(tag_numbers("26.05.2019"), Tag.DATE.value)
        self.assertEqual(tag_numbers("2019.05.26"), Tag.DATE.value)
        self.assertEqual(tag_numbers("(02/06)"), f"({Tag.DATE.value})")
        self.assertEqual(tag_numbers("May 25, 2019"),
                         "May " + Tag.DATE.value)
        self.assertEqual(tag_numbers("May 26, 2019 at 04:30pm"),
                         "May " + Tag.DATE.value)
        self.assertEqual(tag_numbers("19:00"), Tag.DATE.value)
        self.assertEqual(tag_numbers("13:20"), Tag.DATE.value)
        self.assertEqual(tag_numbers("26/5 15:21"), Tag.DATE.value)

    def test_tag_hashtag(self):
        self.assertEqual(tag_hashtag("#M.D.T"), Tag.HASHTAG.value)
        self.assertEqual(tag_ellipsis(
                            tag_hashtag("#MatabichoEconomoPolitico…")
                         ),
                         Tag.HASHTAG.value + Tag.ELLIPSIS.value)
        self.assertEqual(tag_hashtag("#/PortugalYourHOMEBTS"), Tag.HASHTAG.value)

    def test_tag_emoticon_sad(self):
        self.assertEqual(tag_emoticon_sad("=/"), Tag.SAD.value)
        self.assertEqual(tag_emoticon_sad(":/"), Tag.SAD.value)
        self.assertEqual(tag_emoticon_sad("='/"), Tag.SAD.value)
        self.assertEqual(tag_emoticon_sad("=\\"), Tag.SAD.value)
        self.assertEqual(tag_emoticon_sad("://"), Tag.SAD.value)
        self.assertEqual(tag_emoticon_sad(":///"), Tag.SAD.value)

    def test_tag_emoticon_rage(self):
        self.assertEqual(tag_emoticon_rage("@:"), Tag.RAGE.value)
        self.assertEqual(tag_emoticon_rage(":@"), Tag.RAGE.value)

    def test_tag_URL(self):
        self.assertEqual(tag_URL("http://t.co/VkNuHVuTwe"), Tag.URL.value)
        self.assertEqual(tag_URL("https://t.co/VkNuHVuTwe"), Tag.URL.value)
        self.assertEqual(tag_URL("www.publico.pt/2019/05/26/"), Tag.URL.value)
        self.assertEqual(tag_URL("https://t.co/9AFihfU2jW"), Tag.URL.value)
        self.assertEqual(tag_URL("@ProfFerMuLLe"), "@ProfFerMuLLe")
        self.assertEqual(tag_URL("@tthiagoandre"), "@tthiagoandre")
        self.assertEqual(tag_URL("@Pit03Rd"), "@Pit03Rd")


    def test_tag_plus(self):
        self.assertEqual(tag_plus("meses+"), "meses" + Tag.PLUS.value)
        self.assertEqual(tag_plus("nada+"), "nada" + Tag.PLUS.value)
        self.assertEqual(tag_plus("+credibilidade"),
                         Tag.PLUS.value + "credibilidade")
        self.assertEqual(tag_plus("++"), Tag.PLUS.value + Tag.PLUS.value)
        self.assertEqual(tag_plus("+eu"), Tag.PLUS.value + "eu")
        self.assertEqual(tag_plus("a3+b3"), "a3" + Tag.PLUS.value + "b3")
        self.assertEqual(tag_plus("d+"), "d" + Tag.PLUS.value)
        self.assertEqual(tag_plus("d++"),
                         "d" + Tag.PLUS.value + Tag.PLUS.value)

    def test_tag_at(self):
        self.assertEqual(tag_at("@sugar_thae"), Tag.MARK.value)
        self.assertEqual(tag_at("@/prazertom"), Tag.MARK.value)
        self.assertEqual(tag_at("@/btsbrasil_official"), Tag.MARK.value)


if __name__ == '__main__':
    unittest.main()
