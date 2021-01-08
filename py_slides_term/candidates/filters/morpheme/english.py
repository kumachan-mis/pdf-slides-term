import re
from typing import List

from .base import BaseCandidateMorphemeFilter
from py_slides_term.morphemes import BaseMorpheme


class EnglishMorphemeFilter(BaseCandidateMorphemeFilter):
    def __init__(self):
        pass

    def inscope(self, morpheme: BaseMorpheme) -> bool:
        regex = re.compile(r"[A-Za-z]+|\-")
        return regex.fullmatch(str(morpheme)) is not None

    def is_partof_candidate(self, morphemes: List[BaseMorpheme], idx: int) -> bool:
        # TODO: use English dictionary
        return True
