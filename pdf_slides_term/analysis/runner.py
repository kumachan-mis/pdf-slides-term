from typing import Callable, TypeVar

from pdf_slides_term.candidates.data import DomainCandidateTermList
from pdf_slides_term.share.data import TechnicalTerm

AnalysisResult = TypeVar("AnalysisResult")


class AnalysisRunner:
    def __init__(self, ignore_augmented: bool = True):
        self._ignore_augmented = ignore_augmented

    def run_through_candidates(
        self,
        domain_candidates: DomainCandidateTermList,
        initial_result: AnalysisResult,
        update_result: Callable[[AnalysisResult, int, int, TechnicalTerm], None],
    ) -> AnalysisResult:
        result = initial_result

        for xml_id, xml_candidates in enumerate(domain_candidates.xmls):
            for page_candidates in xml_candidates.pages:
                page_num = page_candidates.page_num
                for candidate in page_candidates.candidates:
                    if self._ignore_augmented and candidate.augmented:
                        continue
                    update_result(result, xml_id, page_num, candidate)

        return result

    def run_through_subcandidates(
        self,
        domain_candidates: DomainCandidateTermList,
        initial_result: AnalysisResult,
        update_result: Callable[[AnalysisResult, int, int, TechnicalTerm], None],
    ) -> AnalysisResult:
        result = initial_result

        for xml_id, xml_candidates in enumerate(domain_candidates.xmls):
            for page_candidates in xml_candidates.pages:
                page_num = page_candidates.page_num
                for candidate in page_candidates.candidates:
                    if self._ignore_augmented and candidate.augmented:
                        continue

                    num_morphemes = len(candidate.morphemes)
                    for i in range(num_morphemes):
                        for j in range(i + 1, num_morphemes + 1):
                            sub_candidate = TechnicalTerm(
                                candidate.morphemes[i:j],
                                candidate.fontsize,
                                candidate.augmented,
                            )
                            update_result(result, xml_id, page_num, sub_candidate)

        return result