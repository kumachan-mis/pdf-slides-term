from typing import List, Iterator

from pdf_slides_term.methods.base import BaseMultipleDomainTermRankingMethod
from pdf_slides_term.methods.data import DomainTermRanking
from pdf_slides_term.methods.analyzers.occurrence import TermOccurrenceAnalyzer
from pdf_slides_term.methods.analyzers.charfont import TermCharFontAnalyzer
from pdf_slides_term.methods.rankers.tfidf import TFIDFRanker, TFIDFDomainRankingData
from pdf_slides_term.candidates.data import DomainCandidateTermList


class TFIDFMethod(BaseMultipleDomainTermRankingMethod):
    # public
    def __init__(self, consider_charfont: bool = True):
        super().__init__()

        self._consider_charfont = consider_charfont

        self._occurrence_analyzer = TermOccurrenceAnalyzer()
        self._char_font_analyzer = TermCharFontAnalyzer()
        self._ranker = TFIDFRanker()

    def rank_terms(
        self, domain_candidates_list: List[DomainCandidateTermList]
    ) -> Iterator[DomainTermRanking]:
        ranking_data_list = list(
            map(self._create_domain_ranking_data, domain_candidates_list)
        )

        for domain_candidates in domain_candidates_list:
            ranking_data = next(
                filter(
                    lambda item: item.domain == domain_candidates.domain,
                    ranking_data_list,
                ),
            )
            other_ranking_data_list = list(
                filter(
                    lambda item: item.domain != domain_candidates.domain,
                    ranking_data_list,
                )
            )
            domain_term_ranking = self._ranker.rank_terms(
                domain_candidates, ranking_data, other_ranking_data_list
            )
            yield domain_term_ranking

    def rank_domain_terms(
        self, domain: str, domain_candidates_list: List[DomainCandidateTermList]
    ) -> DomainTermRanking:
        domain_candidates = next(
            filter(lambda item: item.domain == domain, domain_candidates_list),
            None,
        )
        other_domain_candidates_list = list(
            filter(lambda item: item.domain != domain, domain_candidates_list)
        )

        if domain_candidates is None:
            raise ValueError(f"candidate term list in '{domain}' is not provided")

        ranking_data = self._create_domain_ranking_data(domain_candidates)
        other_ranking_data_list = list(
            map(self._create_domain_ranking_data, other_domain_candidates_list)
        )

        domain_term_ranking = self._ranker.rank_terms(
            domain_candidates, ranking_data, other_ranking_data_list
        )

        return domain_term_ranking

    # private
    def _create_domain_ranking_data(
        self,
        domain_candidates: DomainCandidateTermList,
    ) -> TFIDFDomainRankingData:
        term_freq = self._occurrence_analyzer.analyze_term_freq(domain_candidates)
        doc_freq = self._occurrence_analyzer.analyze_doc_freq(domain_candidates)
        num_docs = len(domain_candidates.xmls)
        term_maxsize = (
            self._char_font_analyzer.analyze_term_maxsize(domain_candidates)
            if self._consider_charfont
            else None
        )
        return TFIDFDomainRankingData(
            domain_candidates.domain, term_freq, doc_freq, num_docs, term_maxsize
        )
