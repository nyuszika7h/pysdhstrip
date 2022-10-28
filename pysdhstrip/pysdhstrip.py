import logging
from copy import copy

import pysrt
import regex

HTML_TAG_RE = r"</?[^>]+>"


log = logging.getLogger("pysdhstrip")


def strip(subtitles: str) -> str:
    """
    Strip SDH (Subtitles for the Deaf and Hard of Hearing) parts from subtitles.
    This is sometimes also known as HI (Hearing Impaired) subtitles.

    :param subtitles: SRT subtitles as an UTF-8 string
    :return: SDH-stripped SRT subtitles as an UTF-8 string
    """

    cues = pysrt.from_string(subtitles)

    # Step 1: Strip each cue individually
    for cue in cues:
        cue.text = _strip_cue(cue.text)

    # Step 2: Remove empty cues
    for cue in copy(cues):
        if not cue.text_without_tags.strip():
            cues.remove(cue)
            continue

    # Step 3: Renumber cues to get rid of any gaps
    cues.clean_indexes()

    return "\n".join(map(str, cues))


def _strip_cue(text: str) -> str:
    # Strip (parentheses) and [brackets] and the text inside them,
    # and leave one space if there was a leading and trailing space
    for a, b in {("(", ")"), ("[", "]")}:
        text = regex.sub(
            rf"(?P<sp1> *)\{a}.+?\{b}(?P<sp2> *)",
            lambda m: " " if m.group("sp1") and m.group("sp2") else "",
            text,
            flags=regex.DOTALL | regex.MULTILINE,
        )

    # Strip speaker names at the beginning of lines. This is automated when the
    # speaker name is all caps and the rest of the cue isn't, otherwise it's
    # skipped and a warning is emitted.
    pattern = regex.compile(
        rf"^({{\\an\d+}})?(?:{HTML_TAG_RE})?(?:-\s?)?(?:{HTML_TAG_RE})?(.+?):(?:\s+|$)(.*)",
        flags=regex.MULTILINE,
    )

    replaced = text

    if m := pattern.search(text):
        speaker = m.group(2) or ""
        rest = m.group(3) or ""

        replaced = regex.sub(pattern, r"\1-\3", text)
        replaced = "\n".join(x.strip() for x in replaced.splitlines() if x.strip("-")).strip()

        if not (not speaker or speaker.strip() in ("", "-") or (speaker.isupper() ^ rest.isupper())):
            log.warning(f"Skipping ambiguous replacement: {text!r} --> {replaced!r}")
            replaced = text

    # Strip lines containing only speaker/music symbols and optional whitespace
    replaced = regex.sub(r"^[-:#♪♫\s]+$", "", replaced, flags=regex.MULTILINE)

    # Remove stray tags
    # replaced = regex.sub(r"<([^>]+)>(?!</\1>)", "", replaced)
    # replaced = regex.sub(r"(?!<\1>)</([^>]+)>", "", replaced)

    # Strip leading and trailing whitespace
    replaced = "\n".join(x.strip() for x in replaced.splitlines()).strip()

    # Strip leading dash for single-line
    if len([x for x in replaced.splitlines() if x.replace("<i>", "").startswith("-")]) <= 1:
        replaced = regex.sub(r"^-", "", replaced, flags=regex.MULTILINE)

    # Strip leading colons
    replaced = regex.sub(r"^:\s*", "", replaced, flags=regex.MULTILINE)

    if text != replaced:
        log.info(f"Performing replacement: {text!r} --> {replaced!r}")

    return replaced
