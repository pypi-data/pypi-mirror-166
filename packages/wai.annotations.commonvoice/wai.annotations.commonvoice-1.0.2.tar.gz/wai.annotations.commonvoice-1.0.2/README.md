# wai-annotations-commonvoice
wai.annotations module for managing common voice audio annotations.

The manual is available here:

https://ufdl.cms.waikato.ac.nz/wai-annotations-manual/

## Plugins
### FROM-COMMON-VOICE-SP
Reads speech transcriptions in the Mozilla Common-Voice TSV-format

#### Domain(s):
- **Speech Domain**

#### Options:
```
usage: from-common-voice-sp [-I FILENAME] [-i FILENAME] [-N FILENAME] [-n FILENAME] [--seed SEED] [--rel-path REL_PATH]

optional arguments:
  -I FILENAME, --inputs-file FILENAME
                        Files containing lists of input files (can use glob syntax)
  -i FILENAME, --input FILENAME
                        Input files (can use glob syntax)
  -N FILENAME, --negatives-file FILENAME
                        Files containing lists of negative files (can use glob syntax)
  -n FILENAME, --negative FILENAME
                        Files that have no annotations (can use glob syntax)
  --seed SEED           the seed to use for randomisation
  --rel-path REL_PATH   the relative path from the annotations file to the audio files
```

### TO-COMMON-VOICE-SP
Writes speech transcriptions in the Mozilla Common-Voice TSV-format

#### Domain(s):
- **Speech Domain**

#### Options:
```
usage: to-common-voice-sp [--annotations-only] -o PATH [--split-names SPLIT NAME [SPLIT NAME ...]] [--split-ratios RATIO [RATIO ...]]

optional arguments:
  --annotations-only    skip the writing of data files, outputting only the annotation files
  -o PATH, --output PATH
                        the filename of the TSV file to write the annotations into
  --split-names SPLIT NAME [SPLIT NAME ...]
                        the names to use for the splits
  --split-ratios RATIO [RATIO ...]
                        the ratios to use for the splits
```
