import csv
import os

from wai.common.cli.options import TypedOption

from wai.annotations.core.component.util import AnnotationFileProcessor
from wai.annotations.core.stream import ThenFunction
from wai.annotations.domain.audio import Audio
from wai.annotations.domain.audio.speech import SpeechInstance, Transcription
from ..util import CoquiTTSDialect


class CoquiTTSReader(AnnotationFileProcessor[SpeechInstance]):
    """
    Reader of Coqui's TTS speech annotation format.
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
            header = ["file", "transcript"]

            # Yield rows from the file
            for row in csv.DictReader(file, header, dialect=CoquiTTSDialect):
                wavname = row["file"]
                if not wavname.lower().endswith(".wav"):
                    wavname += ".wav"
                then(
                    SpeechInstance(
                        Audio.from_file(os.path.join(os.path.dirname(filename), self.rel_path, wavname)),
                        Transcription(row['transcript'])
                    )
                )

    def read_negative_file(self, filename: str, then: ThenFunction[SpeechInstance]):
        then(SpeechInstance(Audio.from_file(filename), None))
