from typing import Type, Tuple

from wai.annotations.core.component import Component
from wai.annotations.core.domain import DomainSpecifier
from wai.annotations.core.specifier import SourceStageSpecifier


class CoquiTTSInputFormatSpecifier(SourceStageSpecifier):
    """
    Specifier of the components for reading Coqui TTS text-format
    speech annotations.
    """
    @classmethod
    def description(cls) -> str:
        return "Reads speech transcriptions in the Coqui TTS text-format"

    @classmethod
    def components(cls) -> Tuple[Type[Component], ...]:
        from wai.annotations.core.component.util import LocalFilenameSource
        from ..component import CoquiTTSReader
        return LocalFilenameSource, CoquiTTSReader

    @classmethod
    def domain(cls) -> Type[DomainSpecifier]:
        from wai.annotations.domain.audio.speech import SpeechDomainSpecifier
        return SpeechDomainSpecifier
