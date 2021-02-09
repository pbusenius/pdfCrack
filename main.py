import sys

import pikepdf
from tqdm import tqdm


def check_without_password(file, file_out):
    success = False
    try:
        with pikepdf.open(file) as file_in:
            file_in.save(file_out)
            success = True
    except pikepdf.PasswordError:
        pass

    return success


def check_with_password(file_in, file_out, min_range=0, max_range=100000):
    password = ""
    success = False

    for i in tqdm(range(min_range, max_range)):
        try:
            with pikepdf.open(file_in, str(i)) as file:
                file.save(file_out)
                success = True
                password = str(i)
                break
        except pikepdf.PasswordError:
            pass

    return success, password


pdf_file = sys.argv[1]
pdf_file_out = pdf_file.split(".")[0] + "_cracked.pdf"
cracked_password = ""

successful = check_without_password(pdf_file, pdf_file_out)

if not successful:
    successful, cracked_password = check_with_password(pdf_file, pdf_file_out)

if successful:
    print("PDF File was successfully cracked")
    print("Password: ", cracked_password)
