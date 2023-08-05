import csv
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
from ..util import CoquiSTTDialect, STT_EXPECTED_HEADER

EXPECTED_HEADER_LIST = STT_EXPECTED_HEADER.split(',')


class CoquiSTTWriter(
    ExpectsFile,
    WithPersistentSplitFiles[IO[str]],
    RequiresNoSplitFinalisation,
    SeparateFileWriter[SpeechInstance],
    SplitSink[SpeechInstance]
):
    """
    Writer of Coqui's STT speech annotation format.
    """
    _split_path: str = SplitState(lambda self: self.get_split_path(self.split_label, self.output_path))

    # The CSV writer writing to the file for the current split
    split_writer: csv.DictWriter = SplitState(lambda self: self._init_csv_writer())

    def consume_element_for_split(
            self,
            element: SpeechInstance
    ):
        # Write the audio file to the split directory
        self.write_data_file(element.data, self._split_path)

        # We're done if this is a negative
        if element.annotations is None:
            return

        # Create the Coqui STT CSV row as a dictionary
        instance_dict = {
            "wav_filename": element.data.filename,
            "wav_filesize": len(element.data.data),
            "transcript": element.annotations.text,
        }

        # Write the instance to the file
        self.split_writer.writerow(instance_dict)

    @classmethod
    def get_help_text_for_output_option(cls) -> str:
        return "the filename of the CSV file to write the annotations into"

    def _init_split_files(self) -> IO[str]:
        return open(self.get_split_path(self.split_label, self.output, True), 'w')

    def _iterate_split_files(self, split_files: IO[str]) -> Iterable[ContextManager]:
        return split_files,

    def _init_csv_writer(self) -> csv.DictWriter:
        # Create a CSV writer using the header
        csv_writer = csv.DictWriter(self._split_files, EXPECTED_HEADER_LIST, dialect=CoquiSTTDialect)

        # Write the header to file
        csv_writer.writeheader()

        return csv_writer
