import regex as re


class SectionParser:
    def __init__(self, ontology):
        """
        Load all section definitions from the ontology.
        """
        self.sections_cfg = ontology["sections"]

    def segment_sections(self, text):
        """
        Splits the entire document text into clinical sections based on
        anchors and stop anchors defined in ontology_schema.json.

        Returns:
            {
                "section_name": {
                    "text": "...",
                    "page": None,
                    "char_range": [start, end]
                },
                ...
            }
        """
        blocks = {}

        for sec_name, sec_cfg in self.sections_cfg.items():

            # Section anchors (mandatory)
            anchors = sec_cfg.get("anchors", [])
            stop_anchors = sec_cfg.get("stop_anchors", [])

            if not anchors:
                continue

            # Build regex for section anchor
            anchor_pattern = r"(?im)^(" + "|".join(map(re.escape, anchors)) + r")\b"

            start_match = re.search(anchor_pattern, text)
            if not start_match:
                continue

            start_idx = start_match.start()
            end_idx = len(text)

            # Determine stopping point
            if stop_anchors:
                stop_pattern = r"(?im)^(" + "|".join(map(re.escape, stop_anchors)) + r")\b"
                stop_match = re.search(stop_pattern, text[start_idx + 1:])

                if stop_match:
                    end_idx = start_idx + stop_match.start()

            # Extract section text
            section_text = text[start_idx:end_idx].strip()

            blocks[sec_name] = {
                "text": section_text,
                "page": None,                  # Add page detection later
                "char_range": [start_idx, end_idx]
            }

        return blocks
