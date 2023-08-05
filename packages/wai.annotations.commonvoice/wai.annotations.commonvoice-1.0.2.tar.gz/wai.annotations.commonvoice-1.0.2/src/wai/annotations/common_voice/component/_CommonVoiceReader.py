import csv
import os

from wai.common.cli.options import TypedOption

from wai.annotations.core.component.util import AnnotationFileProcessor
from wai.annotations.core.stream import ThenFunction
from wai.annotations.domain.audio import Audio
from wai.annotations.domain.audio.speech import SpeechInstance, Transcription
from ..util import CommonVoiceDialect, EXPECTED_HEADER, EXPECTED_HEADER_OLD


class CommonVoiceReader(AnnotationFileProcessor[SpeechInstance]):
    """
    Reader of Mozilla's CommonVoice speech annotation format.
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

            # is the header as expected?
            if header == EXPECTED_HEADER + '\n':
                reader = csv.DictReader(file,
                                        EXPECTED_HEADER.split('\t'),
                                        dialect=CommonVoiceDialect)
            elif header == EXPECTED_HEADER_OLD + '\n':
                reader = csv.DictReader(file,
                                        EXPECTED_HEADER_OLD.split('\t'),
                                        dialect=CommonVoiceDialect)
            else:
                raise ValueError(f"Expected header: {EXPECTED_HEADER} or {EXPECTED_HEADER_OLD}\n"
                                 f"Seen header: {header}")

            # Yield rows from the file
            for row in reader:
                then(
                    SpeechInstance(
                        Audio.from_file(os.path.join(os.path.dirname(filename), self.rel_path, row["path"])),
                        Transcription(row['sentence'])
                    )
                )

    def read_negative_file(self, filename: str, then: ThenFunction[SpeechInstance]):
        then(SpeechInstance(Audio.from_file(filename), None))
