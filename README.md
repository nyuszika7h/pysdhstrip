# pysdhstrip

Intelligent SDH (Subtitles for the Deaf and Hard of Hearing) / HI (Hearing Impaired)
removal tool for SubRip (SRT) subtitles.

## Installation

* PyPI: `pip install pysdhstrip` (coming soon)
* From source: `pdm install`

## Usage

### Python
```python
import pysdhstrip

with open("input.srt") as fd:
    subtitles = fd.read()

stripped = pysdhstrip.strip(subtitles)

with open("output.srt", "w") as fd:
    fd.write(stripped)
```

### CLI
Needs to be installed via `pip install "pysdhstrip[cli]"` or `pdm install --group cli`.

```sh
$ pysdhstrip input.srt -o output.srt
$ pysdhstrip input.srt  # Output to stdout
$ pysdhstrip -w input.srt  # Overwrite input file
```
