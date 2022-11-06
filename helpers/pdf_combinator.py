import os
import argparse

from PyPDF2 import PdfMerger
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
######## UNUSED - Combined in one script
def combine_pdfs(
        files_list: list, 
        path: Path, 
        course: str
    ):

    merger = PdfMerger()
    file_name = course + str(path.parts[-1])
    for file in files_list:
        if course not in file:
            with open(path / file, mode="rb") as pdf:
                merger.append(pdf)

    file = str(path) +"/"+ file_name + ".pdf"
    merger.write(file)
    merger.close()
    
    print(f"Successfully wrote {file}")


if __name__ == '__main__':
    
    recitations_path = Path(os.getenv('user_app_recitations'))
    lectures_path = Path(os.getenv('user_app_lectures'))
    course = "MIT_6.006_"

    parser = argparse.ArgumentParser(description='Process some strings.')

    lec_files = os.listdir(lectures_path)
    combine_pdfs(lec_files, lectures_path, course)

    rec_files = os.listdir(recitations_path)
    combine_pdfs(rec_files, recitations_path, course)
