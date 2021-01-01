import os
import json

from pdf_slides_term.candidates import PDFnXMLPath, CandidateTermExtractor
from scripts.utils import generate_pdf_path, pdf_to_xml_path, pdf_to_candidate_path

if __name__ == "__main__":
    extractor = CandidateTermExtractor(modifying_particle_augmentation=True)
    pdf_paths = generate_pdf_path()
    for pdf_path in pdf_paths:
        xml_path = pdf_to_xml_path(pdf_path)
        pdfnxml = PDFnXMLPath(pdf_path, xml_path)
        candidate_term_list = extractor.extract_from_xml_file(pdfnxml)

        candidate_path = pdf_to_candidate_path(pdf_path)
        candidate_dir_name = os.path.dirname(candidate_path)
        os.makedirs(candidate_dir_name, exist_ok=True)

        with open(candidate_path, "w") as candidate_file:
            json_obj = candidate_term_list.to_json()
            json.dump(json_obj, candidate_file, ensure_ascii=False, indent=2)
