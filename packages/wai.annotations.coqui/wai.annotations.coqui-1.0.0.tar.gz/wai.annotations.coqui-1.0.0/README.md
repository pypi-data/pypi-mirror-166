# wai-annotations-coqui
wai.annotations plugin for coqui.ai support (STT/TTS).

The manual is available here:

https://ufdl.cms.waikato.ac.nz/wai-annotations-manual/


## Coqui file formats

* [STT](https://stt.readthedocs.io/en/latest/TRAINING_INTRO.html#training-on-your-own-data)
* [TTS](https://tts.readthedocs.io/en/latest/formatting_your_dataset.html)


## Plugins

### FROM-COQUI-STT-SP
Reads speech transcriptions in the Coqui STT CSV-format

#### Domain(s):
- **Speech Domain**

#### Options:
```
usage: from-coqui-stt-sp [-I FILENAME] [-i FILENAME] [-N FILENAME] [-n FILENAME] [-o FILENAME]
                         [--seed SEED] [--rel-path REL_PATH]

optional arguments:
  -I FILENAME, --inputs-file FILENAME
                        Files containing lists of input files (can use glob syntax) (default: [])
  -i FILENAME, --input FILENAME
                        Input files (can use glob syntax) (default: [])
  -N FILENAME, --negatives-file FILENAME
                        Files containing lists of negative files (can use glob syntax) (default: [])
  -n FILENAME, --negative FILENAME
                        Files that have no annotations (can use glob syntax) (default: [])
  -o FILENAME, --output-file FILENAME
                        optional file to write read filenames into (default: None)
  --seed SEED           the seed to use for randomisation (default: None)
  --rel-path REL_PATH   the relative path from the annotations file to the audio files (default: .)
```

### FROM-COQUI-TTS-SP
Reads speech transcriptions in the Coqui TTS text-format

#### Domain(s):
- **Speech Domain**

#### Options:
```
usage: from-coqui-tts-sp [-I FILENAME] [-i FILENAME] [-N FILENAME] [-n FILENAME] [-o FILENAME]
                         [--seed SEED] [--rel-path REL_PATH]

optional arguments:
  -I FILENAME, --inputs-file FILENAME
                        Files containing lists of input files (can use glob syntax) (default: [])
  -i FILENAME, --input FILENAME
                        Input files (can use glob syntax) (default: [])
  -N FILENAME, --negatives-file FILENAME
                        Files containing lists of negative files (can use glob syntax) (default: [])
  -n FILENAME, --negative FILENAME
                        Files that have no annotations (can use glob syntax) (default: [])
  -o FILENAME, --output-file FILENAME
                        optional file to write read filenames into (default: None)
  --seed SEED           the seed to use for randomisation (default: None)
  --rel-path REL_PATH   the relative path from the annotations file to the audio files (default: .)
```


### TO-COQUI-STT-SP
Writes speech transcriptions in the Coqui STT CSV-format

#### Domain(s):
- **Speech Domain**

#### Options:
```
usage: to-coqui-stt-sp [--annotations-only] -o PATH [--split-names SPLIT NAME [SPLIT NAME ...]]
                       [--split-ratios RATIO [RATIO ...]]

optional arguments:
  --annotations-only    skip the writing of data files, outputting only the annotation files
                        (default: False)
  -o PATH, --output PATH
                        the filename of the CSV file to write the annotations into (default: None)
  --split-names SPLIT NAME [SPLIT NAME ...]
                        the names to use for the splits (default: [])
  --split-ratios RATIO [RATIO ...]
                        the ratios to use for the splits (default: [])
```

### TO-COQUI-TTS-SP
Writes speech transcriptions in the Coqui TTS text-format

#### Domain(s):
- **Speech Domain**

#### Options:
```
usage: to-coqui-tts-sp [--annotations-only] -o PATH [--split-names SPLIT NAME [SPLIT NAME ...]]
                       [--split-ratios RATIO [RATIO ...]]

optional arguments:
  --annotations-only    skip the writing of data files, outputting only the annotation files
                        (default: False)
  -o PATH, --output PATH
                        the filename of the TTS file to write the annotations into (default: None)
  --split-names SPLIT NAME [SPLIT NAME ...]
                        the names to use for the splits (default: [])
  --split-ratios RATIO [RATIO ...]
                        the ratios to use for the splits (default: [])
```
