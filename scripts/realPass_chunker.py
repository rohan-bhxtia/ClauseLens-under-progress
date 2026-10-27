# testing remaining 4 pdfs ..


from pathlib import Path

from clauselens.ingest.parser import parse_pdf
from clauselens.ingest.chunker import groupBlocks_toClauses


DATA_DIR = Path("data")
LEASES = [
    ("lease_02.pdf", 17),
    ("lease_03.pdf", 18),
    ("lease_04.pdf", 17),
    ("lease_05.pdf", 18),
]


def main():
    all_passed = True

    for filename, expected_count in LEASES:
        path = DATA_DIR / filename

        print(f"\n{'=' * 50}")
        print(f"Testing: {filename}")

        if not path.exists():
            print(f"FAIL: PDF not found at {path}")
            all_passed = False
            continue

        blocks = parse_pdf(str(path))
        clauses = groupBlocks_toClauses(blocks)

        print(f"Blocks extracted: {len(blocks)}")
        print(f"Clauses created: {len(clauses)}")
        print(f"Expected clauses: {expected_count}")

        if len(clauses) != expected_count:
            print("FAIL: Clause count does not match.")
            all_passed = False
        else:
            print("PASS: Clause count matches.")

        for clause in clauses:
            preview = " ".join(clause.text.split())[:60]
            print(
                f"  Number={clause.number}, "
                f"Title={clause.title!r}, "
                f"Page={clause.page}, "
                f"Text={preview!r}"
            )

            if not clause.text.strip():
                print("  FAIL: Empty clause text.")
                all_passed = False

            if clause.page < 1:
                print("  FAIL: Invalid page number.")
                all_passed = False

    print(f"\n{'=' * 50}")
    print("OVERALL RESULT:", "PASS" if all_passed else "FAIL")


if __name__ == "__main__":
    main()
