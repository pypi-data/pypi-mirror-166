import csv
import os
from typing import IO, ContextManager, Iterable


from wai.annotations.core.component.util import (
    SeparateFileWriter,
    SplitSink,
    SplitState,
    RequiresNoSplitFinalisation,
    WithPersistentSplitFiles,
    ExpectsFile
)
from wai.annotations.domain.audio.speech import SpeechInstance
from ..util import CoquiTTSDialect


class CoquiTTSWriter(
    ExpectsFile,
    WithPersistentSplitFiles[IO[str]],
    RequiresNoSplitFinalisation,
    SeparateFileWriter[SpeechInstance],
    SplitSink[SpeechInstance]
):
    """
    Writer of Coqui's TTS speech annotation format.
    """
    _split_path: str = SplitState(lambda self: self.get_split_path(self.split_label, self.output_path))

    # The CSV writer writing to the file for the current split
    split_writer: csv.writer = SplitState(lambda self: self._init_csv_writer())

    def consume_element_for_split(
            self,
            element: SpeechInstance
    ):
        # Write the audio file to the split directory
        self.write_data_file(element.data, self._split_path)

        # We're done if this is a negative
        if element.annotations is None:
            return

        # Create the Coqui TTS row as a dictionary
        instance_row = [os.path.splitext(element.data.filename)[0], element.annotations.text]

        # Write the instance to the file
        self.split_writer.writerow(instance_row)

    @classmethod
    def get_help_text_for_output_option(cls) -> str:
        return "the filename of the TTS file to write the annotations into"

    def _init_split_files(self) -> IO[str]:
        return open(self.get_split_path(self.split_label, self.output, True), 'w')

    def _iterate_split_files(self, split_files: IO[str]) -> Iterable[ContextManager]:
        return split_files,

    def _init_csv_writer(self) -> csv.writer:
        # Create a CSV writer using the dialect
        csv_writer = csv.writer(self._split_files, dialect=CoquiTTSDialect)

        return csv_writer
