import os
import sys
import fitz
import re

def pdf_rename(case_number, path, counter=None):
    def sanitize_filename(filename):
        return re.sub(r'[\\/*?:"<>|]', "_", filename)
    # Define the new filename
    new_casenum = f"{case_number}_{counter}" if counter is not None else case_number
    new_filename = sanitize_filename(f"{new_casenum}.pdf")
    new_path = os.path.join(os.path.dirname(path), new_filename)
    # Rename the file
    try:
        os.rename(path, new_path)
    except FileExistsError:
        if counter is None:
            counter = 1
        else:
            counter += 1
        pdf_rename(case_number, path, counter)
    except (PermissionError, FileNotFoundError) as e:
        print(f"--error--: {e}, while renaming {path} to {new_path}")


def hans(lines):
    case_number = lines[2].strip()
    return case_number

def shimadzu(lines):
    sample_name_index = lines.index("Sample Name")
    case_number = lines[sample_name_index + 1]
    case_number = case_number[2:].upper()
    return case_number


def main(path, method):
    for filename in os.listdir(path):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(path, filename)
            print(f"Processing file: {filename}")
            doc = fitz.open(pdf_path)
            # Extract text from the first page
            page = doc[0]
            text = page.get_text()
            lines = text.split('\n')

            try:
                case_num = method(lines)
                print(f"extracted string {case_num}")
                doc.close()
                pdf_rename(case_num, pdf_path)

            except Exception as e:
                print(f'unable to find case number / rename | {e}')
                doc.close()
                continue
    print('script complete')


if __name__ == "__main__":
    print(f"sys.argv: {sys.argv}")
    path = sys.argv[1]
    file_type = sys.argv[2]
    path = os.path.normpath(path)

    if file_type == "Hans":
        method = hans
    if file_type == "Shimadzu":
        method = shimadzu

    main(path, method)


