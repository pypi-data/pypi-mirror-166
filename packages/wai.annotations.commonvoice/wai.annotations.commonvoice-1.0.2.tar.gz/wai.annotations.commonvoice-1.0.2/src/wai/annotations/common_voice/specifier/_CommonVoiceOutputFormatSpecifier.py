from typing import Type, Tuple

from wai.annotations.core.component import Component
from wai.annotations.core.domain import DomainSpecifier
from wai.annotations.core.specifier import SinkStageSpecifier


class CommonVoiceOutputFormatSpecifier(SinkStageSpecifier):
    """
    Specifier of the components for writing Mozilla Common-Voice TSV-format
    speech annotations.
    """
    @classmethod
    def description(cls) -> str:
        return "Writes speech transcriptions in the Mozilla Common-Voice TSV-format"

    @classmethod
    def components(cls) -> Tuple[Type[Component], ...]:
        from ..component import CommonVoiceWriter
        return CommonVoiceWriter,

    @classmethod
    def domain(cls) -> Type[DomainSpecifier]:
        from wai.annotations.domain.audio.speech import SpeechDomainSpecifier
        return SpeechDomainSpecifier
