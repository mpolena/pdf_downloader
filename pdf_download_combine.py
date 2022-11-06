import os
import requests
# import argparse
import logging

from bs4 import BeautifulSoup
from PyPDF2 import PdfMerger
from pathlib import Path
from typing import List, Tuple, Any
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)


def combine_pdfs(merger: PdfMerger, path: str):
    """
    Combines pdf files given a merger object and a path

    Args:
        merger (PdfMerger): object
        path (str): destination
    """

    course = "MIT_6.006_"
    file_name = path + course + path.split('/')[-2] + ".pdf"
    merger.write(file_name)
    merger.close()
    logging.info(f"Generated combined file: {file_name}.")


def _process_pdf(
        merger: PdfMerger,
        base_path: str,
        fname: str,
        base_url: str,
        href: dict,
    ) -> PdfMerger:
    """
    Creates PdfMerger object used for merging pdf files

    Args:
        merger (PdfMerger): Merger object
        base_path (str): path
        fname (str): name of file
        base_url (str): url where file contents can be obrained
        href (dict): dictionary of pdf files

    Returns:
        PdfMerger: Object with list of pdf that can be combined.
    """
    with open(f"{base_path}{fname}", 'wb') as pdf:
        pdf.write(requests.get(base_url + href.get('href')).content)
    with open(f"{base_path}{fname}", 'rb') as pdf: 
        merger.append(pdf)
    return merger


def download_pdfs(
        links: list, 
        base_url: str,
        base_path: str,
        lecture_merger: PdfMerger,
        recitations_merger: PdfMerger,
    ) -> List[Tuple[Any, str]]:
    """
    Downloads set of lecture and recitation pdfs from MIT_6.006 course

    Args:
        links (list): list of links.
        base_url (str): class website URL.
        base_path (str): base path where files will be written.
        lecture_merger (PdfMerger): merger object for lectures.
        recitations_merger (PdfMerger): merger object for recitations.

    Returns:
        list of Tuples(merger, str): merger and path for further processing.
    """

    rec_base_path = f"{base_path}recitations/"
    lec_base_path = f"{base_path}lectures/"

    file_name_dict = {
        lec_base_path: "lec",
        rec_base_path: "r"
    }
    
    for link in links:
        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'html.parser')
        a_tags = soup.find_all('a')
        href_dict = {}
        for href in a_tags:
            pdf_url = base_url + href.get('href')
            if '.pdf' in pdf_url and pdf_url not in href_dict:
                # Populate dict to prevent downloading more than once.
                href_dict[pdf_url] = 1
                fname = href.get('href').split('/')[-1].split('_')[-1]
                logging.info(f"Downloading file: {fname}")

                # Process lecture.
                if file_name_dict[lec_base_path] in fname:
                    lecture_merger = _process_pdf(
                        lecture_merger,
                        lec_base_path,
                        fname,
                        base_url,
                        href,
                    )
                # Process recitation.
                elif file_name_dict[rec_base_path] in fname:
                    recitations_merger = _process_pdf(
                        recitations_merger,
                        rec_base_path,
                        fname,
                        base_url,
                        href,
                    )
    logging.info("All PDF files downloaded")

    return [(lecture_merger, lec_base_path), (recitations_merger, rec_base_path)]


def main():
    """
    Main Function; program entry-point.

    """
    base_url = os.getenv('base_url')
    url_ext = os.getenv('url_path')
    base_path = os.getenv('base_path')

    url = f"{base_url}{url_ext}"
    response = requests.get(url)

    # Parse text obtained
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all hyperlinks present on webpage
    links = soup.find_all('a')
    url_lst = [
        base_url + link.get('href') for link in links if 'resources' in link.get('href')
    ]

    lecture_merger = PdfMerger()
    recitations_merger = PdfMerger()

    merger_and_path_list = download_pdfs(
        url_lst, 
        base_url, 
        base_path,
        lecture_merger=lecture_merger,
        recitations_merger=recitations_merger,
    )

    for merger, path in merger_and_path_list:
        combine_pdfs(merger, path)


if __name__ == "__main__":
    main()
