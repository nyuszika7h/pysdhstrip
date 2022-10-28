import unittest

from pysdhstrip import strip


class TestStrip(unittest.TestCase):
    def test_speaker_name(self) -> None:
        self.assertEqual(
            strip("1\n00:00:00,000 --> 00:00:05,000\nALICE: Good morning.\n"),
            "1\n00:00:00,000 --> 00:00:05,000\nGood morning.\n",
        )

    def test_multi_speaker(self) -> None:
        self.assertEqual(
            strip("1\n00:00:00,000 --> 00:00:05,000\nALICE: Good morning.\nBOB:\nGood morning, Alice.\n"),
            "1\n00:00:00,000 --> 00:00:05,000\n-Good morning.\n-Good morning, Alice.\n",
        )

    def test_ambiguous_speaker(self) -> None:
        self.assertEqual(
            strip("1\n00:00:00,000 --> 00:00:05,000\nALICE: GOOD MORNING.\n"),
            "1\n00:00:00,000 --> 00:00:05,000\nALICE: GOOD MORNING.\n",
        )

    def test_sdh(self) -> None:
        self.assertEqual(
            strip("1\n00:00:00,000 --> 00:00:05,000\n[indistinct] Good morning.\n"),
            "1\n00:00:00,000 --> 00:00:05,000\nGood morning.\n",
        )
        self.assertEqual(
            strip("1\n00:00:00,000 --> 00:00:05,000\n(indistinct) Good morning.\n"),
            "1\n00:00:00,000 --> 00:00:05,000\nGood morning.\n",
        )
        self.assertEqual(
            strip("1\n00:00:00,000 --> 00:00:05,000\n(INDISTINCT) Good morning.\n"),
            "1\n00:00:00,000 --> 00:00:05,000\nGood morning.\n",
        )

    def test_lone_sdh(self) -> None:
        self.assertEqual(
            strip(
                "1\n00:00:00,000 --> 00:00:05,000\nGood morning.\n\n"
                "2\n00:00:05,000 --> 00:00:10,000\n[door opens]\n\n"
                "3\n00:00:10,000 --> 00:00:15,000\nGood morning, Alice.\n"
            ),
            "1\n00:00:00,000 --> 00:00:05,000\nGood morning.\n\n"
            "2\n00:00:10,000 --> 00:00:15,000\nGood morning, Alice.\n"
        )

    def test_music(self) -> None:
        self.assertEqual(
            strip("1\n00:00:00,000 --> 00:00:05,000\n♪ Never gonna give you up ♪\n"),
            "1\n00:00:00,000 --> 00:00:05,000\n♪ Never gonna give you up ♪\n",
        )

    def test_lone_music(self) -> None:
        self.assertEqual(
            strip("1\n00:00:00,000 --> 00:00:05,000\n♪♪\n"),
            "",
        )
        self.assertEqual(
            strip("1\n00:00:00,000 --> 00:00:05,000\n♪ [music] ♪\n"),
            "",
        )

    def test_hashtag(self) -> None:
        self.assertEqual(
            strip("1\n00:00:00,000 --> 00:00:05,000\nThat's #amazing! I #love it!\n"),
            "1\n00:00:00,000 --> 00:00:05,000\nThat's #amazing! I #love it!\n",
        )

    def test_speaker_sdh(self) -> None:
        self.assertEqual(
            strip("1\n00:00:00,000 --> 00:00:05,000\n[whispering]: Hello.\n"),
            strip("1\n00:00:00,000 --> 00:00:05,000\nHello.\n"),
        )
        self.assertEqual(
            strip("1\n00:00:00,000 --> 00:00:05,000\nALICE [whispering]: Hello.\n"),
            strip("1\n00:00:00,000 --> 00:00:05,000\nHello.\n"),
        )
        self.assertEqual(
            strip("1\n00:00:00,000 --> 00:00:05,000\n[whispering] ALICE: Hello.\n"),
            strip("1\n00:00:00,000 --> 00:00:05,000\nHello.\n"),
        )


if __name__ == "__main__":
    unittest.main()
