import json
from copy import deepcopy

from src.utils_pdf import extract_pdf_text
from src.section_parser import SectionParser
from src.entity_extractors import extract_medications, extract_vitals, extract_labs


class ClinicalExtractor:
    def __init__(self, ontology_path, template_path):
        """
        ontology_path: path to ontology_schema.json
        template_path: path to output_template.json
        """
        self.ontology = json.load(open(ontology_path, "r"))
        self.template = json.load(open(template_path, "r"))

    def run(self, pdf_path):
        """
        Runs the extraction pipeline.
        Returns a dict following the output_template.json structure.
        """

        # 1. Extract text from PDF
        pages = extract_pdf_text(pdf_path)
        full_text = "\n".join([p["text"] for p in pages])

        # 2. Prepare blank output from template
        out = deepcopy(self.template)

        # Metadata update
        out["document_meta"]["source_file"] = pdf_path
        out["document_meta"]["pages"] = len(pages)

        # 3. Section segmentation
        parser = SectionParser(self.ontology)
        detected_sections = parser.segment_sections(full_text)

        for section_name, sec_data in detected_sections.items():
            if section_name in out["sections"]:
                out["sections"][section_name]["text"] = sec_data["text"]
                out["sections"][section_name]["page"] = sec_data.get("page")
                out["sections"][section_name]["char_range"] = sec_data.get("char_range")

        # 4. Medications extraction
        med_block = out["sections"].get("medications", {}).get("text", "")
        medications = extract_medications(med_block)
        out["sections"]["medications"]["items"] = medications
        out["medications"] = medications

        # 5. Vitals extraction
        vitals_block = out["sections"].get("vitals", {}).get("text", "")
        vitals = extract_vitals(vitals_block)
        out["sections"]["vitals"]["structured"] = vitals

        # 6. Lab extraction
        labs_block = out["sections"].get("labs", {}).get("text", "")
        labs = extract_labs(labs_block)
        out["sections"]["labs"]["items"] = labs
        out["labs"] = labs

        return out
