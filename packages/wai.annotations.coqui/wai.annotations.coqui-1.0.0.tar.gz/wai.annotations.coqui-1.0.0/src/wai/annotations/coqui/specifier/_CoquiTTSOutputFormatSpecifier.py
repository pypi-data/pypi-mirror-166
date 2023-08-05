from typing import Type, Tuple

from wai.annotations.core.component import Component
from wai.annotations.core.domain import DomainSpecifier
from wai.annotations.core.specifier import SinkStageSpecifier


class CoquiTTSOutputFormatSpecifier(SinkStageSpecifier):
    """
    Specifier of the components for writing Coqui TTS text-format
    speech annotations.
    """
    @classmethod
    def description(cls) -> str:
        return "Writes speech transcriptions in the Coqui TTS text-format"

    @classmethod
    def components(cls) -> Tuple[Type[Component], ...]:
        from ..component import CoquiTTSWriter
        return CoquiTTSWriter,

    @classmethod
    def domain(cls) -> Type[DomainSpecifier]:
        from wai.annotations.domain.audio.speech import SpeechDomainSpecifier
        return SpeechDomainSpecifier
