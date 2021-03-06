import os
import json
from argparse import ArgumentParser

from py_slides_term.techterms import TechnicalTermExtractor
from scripts.utils import (
    relpath_from_basedir,
    get_domains,
    generate_domain_candidates,
    generate_domain_term_ranking,
    pdf_to_techterm_path,
)

script_name = os.path.basename(__file__)

if __name__ == "__main__":
    parser = ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--mcvalue", help="use MC-Value method", action="store_true")
    group.add_argument("--tfidf", help="use TF-IDF method", action="store_true")
    group.add_argument("--lfidf", help="use LF-IDF method", action="store_true")
    group.add_argument("--flr", help="use FLR method", action="store_true")
    group.add_argument("--hits", help="use HITS method", action="store_true")
    group.add_argument("--flrh", help="use FLRH method", action="store_true")
    group.add_argument("--mdp", help="use MDP method", action="store_true")
    args = parser.parse_args()

    if args.mcvalue:
        method_name = "mcvalue"
    elif args.tfidf:
        method_name = "tfidf"
    elif args.lfidf:
        method_name = "lfidf"
    elif args.flr:
        method_name = "flr"
    elif args.hits:
        method_name = "hits"
    elif args.flrh:
        method_name = "flrh"
    elif args.mdp:
        method_name = "mdp"
    else:
        raise RuntimeError("unreachable statement")

    extractor = TechnicalTermExtractor()

    domains = get_domains()
    domain_candidates_list = generate_domain_candidates(domains)
    domain_term_ranking_list = generate_domain_term_ranking(method_name, domains)
    ziped_list = zip(domain_candidates_list, domain_term_ranking_list)

    for domain_candidates, domain_term_ranking in ziped_list:
        domain_techterms = extractor.extract_from_domain(
            domain_candidates, domain_term_ranking
        )

        for pdf_techterms in domain_techterms.pdfs:
            techterm_path = pdf_to_techterm_path(pdf_techterms.pdf_path, method_name)
            print(f"{script_name}: creating {relpath_from_basedir(techterm_path)} ...")

            techterm_dir_name = os.path.dirname(techterm_path)
            os.makedirs(techterm_dir_name, exist_ok=True)

            with open(techterm_path, "w") as techterm_file:
                json_obj = pdf_techterms.to_json()
                json.dump(json_obj, techterm_file, ensure_ascii=False, indent=2)
