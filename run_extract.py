import sys
import json
import os
from src.extractor import ClinicalExtractor


def main(pdf_path):
    """
    Runs the clinical extraction pipeline on the given PDF file.
    Saves nothing — only prints the output (you can modify this later).
    """

    extractor = ClinicalExtractor(
        "configs/ontology_schema.json",
        "configs/output_template.json"
    )

    result = extractor.run(pdf_path)

    # ensure output folder exists
    os.makedirs("output", exist_ok=True)

    # build output filename
    base = os.path.basename(pdf_path).replace(".pdf", "")
    out_path = f"output/{base}_extracted.json"

    # save json
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Output saved to: {out_path}\n")

    # Pretty-print to console
    # print(json.dumps(result, indent=2))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run_extract.py <path_to_pdf>")
        sys.exit(1)

    main(sys.argv[1])
