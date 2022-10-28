# pysdhstrip

Intelligent [SDH/HI](https://en.wikipedia.org/wiki/Subtitles_for_the_deaf_or_hard-of-hearing) removal tool
removal tool for [SRT](https://en.wikipedia.org/wiki/SubRip#SubRip_file_format) subtitles.

## Installation

* PyPI: `pip install pysdhstrip` (coming soon)
* From source: `pdm install`

## Usage

### Python
```python
import pysdhstrip

with open("input.srt", encoding="utf-8") as fd:
    subtitles = fd.read()

stripped = pysdhstrip.strip(subtitles)

with open("output.srt", "w", encoding="utf-8") as fd:
    fd.write(stripped)
```

### CLI
Needs to be installed via `pip install "pysdhstrip[cli]"` or `pdm install --group cli`.

```sh
$ pysdhstrip input.srt -o output.srt
$ pysdhstrip input.srt  # Output to stdout
$ pysdhstrip -w input.srt  # Overwrite input file
```
