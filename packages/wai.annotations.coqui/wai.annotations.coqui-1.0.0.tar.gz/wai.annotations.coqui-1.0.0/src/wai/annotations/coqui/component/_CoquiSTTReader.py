import csv
import os

from wai.common.cli.options import TypedOption

from wai.annotations.core.component.util import AnnotationFileProcessor
from wai.annotations.core.stream import ThenFunction
from wai.annotations.domain.audio import Audio
from wai.annotations.domain.audio.speech import SpeechInstance, Transcription
from ..util import CoquiSTTDialect, STT_EXPECTED_HEADER


class CoquiSTTReader(AnnotationFileProcessor[SpeechInstance]):
    """
    Reader of Coqui's STT speech annotation format.
    """
    # The audio clips may be in a separate folder to the annotations file
    rel_path = TypedOption(
        "--rel-path",
        type=str,
        default=".",
        required=False,
        help="the relative path from the annotations file to the audio files"
    )
    def read_annotation_file(self, filename: str, then: ThenFunction[SpeechInstance]):
        with open(filename, 'r', newline='') as file:
            # Consume the header
            header = file.readline()

            # Make sure the header is what we expect
            if header != STT_EXPECTED_HEADER + '\n':
                raise ValueError(f"Expected header: {STT_EXPECTED_HEADER}\n"
                                 f"Seen header: {header}")

            # Yield rows from the file
            for row in csv.DictReader(file,
                                      STT_EXPECTED_HEADER.split(','),
                                      dialect=CoquiSTTDialect):
                then(
                    SpeechInstance(
                        Audio.from_file(os.path.join(os.path.dirname(filename), self.rel_path, row["wav_filename"])),
                        Transcription(row['transcript'])
                    )
                )

    def read_negative_file(self, filename: str, then: ThenFunction[SpeechInstance]):
        then(SpeechInstance(Audio.from_file(filename), None))
