import re
from dataclasses import dataclass
from typing import List, Tuple, Dict, Any, Type

from pdf_slides_term.mecab import BaseMeCabMorpheme, MeCabMorphemeIPADic
from pdf_slides_term.share.consts import HIRAGANA_REGEX, KATAKANA_REGEX, KANJI_REGEX


JAPANESE_REGEX = rf"({HIRAGANA_REGEX}|{KATAKANA_REGEX}|{KANJI_REGEX})"


LinguSeq = Tuple[Tuple[str, str, str], ...]


@dataclass(frozen=True)
class Term:
    morphemes: List[BaseMeCabMorpheme]
    fontsize: float = 0.0
    augmented: bool = False

    def __str__(self) -> str:
        num_morphemes = len(self.morphemes)
        if not num_morphemes:
            return ""

        japanese_regex = re.compile(rf"{JAPANESE_REGEX}*")
        symbol_regex = re.compile("-")

        term_str = str(self.morphemes[0])
        for i in range(1, num_morphemes):
            prev_morpheme_str = str(self.morphemes[i - 1])
            morpheme_str = str(self.morphemes[i])
            if (
                japanese_regex.fullmatch(prev_morpheme_str) is None
                or japanese_regex.fullmatch(morpheme_str) is None
            ) and (
                symbol_regex.fullmatch(prev_morpheme_str) is None
                and symbol_regex.fullmatch(morpheme_str) is None
            ):
                term_str += " "

            term_str += morpheme_str

        return term_str

    def linguistic_sequence(self) -> LinguSeq:
        return tuple(
            (morpheme.pos, morpheme.category, morpheme.subcategory)
            for morpheme in self.morphemes
        )

    def to_json(self) -> Dict[str, Any]:
        return {
            "morphemes": list(map(lambda morpheme: morpheme.to_json(), self.morphemes)),
            "fontsize": self.fontsize,
            "augmented": self.augmented,
        }

    @classmethod
    def from_json(
        cls,
        obj: Dict[str, Any],
        morpheme_cls: Type[BaseMeCabMorpheme] = MeCabMorphemeIPADic,
    ):
        return cls(
            list(map(lambda item: morpheme_cls.from_json(item), obj["morphemes"])),
            obj.get("fontsize", 0),
            obj.get("augmented", False),
        )
