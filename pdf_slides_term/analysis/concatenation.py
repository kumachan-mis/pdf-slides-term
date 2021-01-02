from dataclasses import dataclass
from typing import Dict

from pdf_slides_term.candidates import DomainCandidateTermList
from pdf_slides_term.mecab import MeCabMorphemeClassifier, BaseMeCabMorpheme
from pdf_slides_term.share.data import Term


@dataclass(frozen=True)
class TermConcatenation:
    left_freq: Dict[str, Dict[str, int]]
    # number of occurrences of (left, morpheme) in the domain
    # if morpheme or left is meaningless (a modifying particle or a symbol),
    # this is fixed at zero
    right_freq: Dict[str, Dict[str, int]]
    # number of occurrences of (morpheme, right) in the domain
    # if morpheme or right is meaningless (a modifying particle or a symbol),
    # this is fixed at zero


class TermConcatenationAnalyzer:
    # public
    def __init__(self, ignore_augmented: bool = True):
        self._classifier = MeCabMorphemeClassifier()
        self._ignore_augmented = ignore_augmented

    def analyze(self, domain_candidates: DomainCandidateTermList) -> TermConcatenation:
        term_concat = TermConcatenation(dict(), dict())

        for pdf_candidates in domain_candidates.pdfs:
            for page_candidates in pdf_candidates.pages:
                for candidate in page_candidates.candidates:
                    if self._ignore_augmented and candidate.augmented:
                        continue
                    self._update_concat(term_concat, candidate)

        return term_concat

    # private
    def _update_concat(self, term_concat: TermConcatenation, candidate: Term):
        num_morphemes = len(candidate.morphemes)
        for i in range(num_morphemes):
            morpheme = candidate.morphemes[i]
            morpheme_str = str(morpheme)
            if self._is_meaningless_morpheme(morpheme):
                term_concat.left_freq[morpheme_str] = dict()
                term_concat.right_freq[morpheme_str] = dict()
                continue

            if i > 0:
                left_morpheme = candidate.morphemes[i - 1]
                left_morpheme_str = str(left_morpheme)

                if not self._is_meaningless_morpheme(left_morpheme):
                    left = term_concat.left_freq.get(morpheme_str, dict())
                    left[left_morpheme_str] = left.get(left_morpheme_str, 0) + 1
                    term_concat.left_freq[morpheme_str] = left

                    right = term_concat.right_freq.get(left_morpheme_str, dict())
                    right[morpheme_str] = right.get(morpheme_str, 0) + 1
                    term_concat.right_freq[left_morpheme_str] = right
                else:
                    left = term_concat.left_freq.get(morpheme_str, dict())
                    term_concat.left_freq[morpheme_str] = left
            else:
                left = term_concat.left_freq.get(morpheme_str, dict())
                term_concat.left_freq[morpheme_str] = left

            if i < num_morphemes - 1:
                right_morpheme = candidate.morphemes[i + 1]
                right_morpheme_str = str(right_morpheme)

                if not self._is_meaningless_morpheme(right_morpheme):
                    right = term_concat.right_freq.get(morpheme_str, dict())
                    right[right_morpheme_str] = right.get(right_morpheme_str, 0) + 1
                    term_concat.right_freq[morpheme_str] = right

                    left = term_concat.left_freq.get(right_morpheme_str, dict())
                    left[morpheme_str] = right.get(morpheme_str, 0) + 1
                    term_concat.left_freq[right_morpheme_str] = left
                else:
                    right = term_concat.right_freq.get(morpheme_str, dict())
                    term_concat.right_freq[morpheme_str] = right
            else:
                right = term_concat.right_freq.get(morpheme_str, dict())
                term_concat.right_freq[morpheme_str] = right

    def _is_meaningless_morpheme(self, morpheme: BaseMeCabMorpheme) -> bool:
        is_modifying_particle = self._classifier.is_modifying_particle(morpheme)
        is_symbol = self._classifier.is_symbol(morpheme)
        return is_modifying_particle or is_symbol
