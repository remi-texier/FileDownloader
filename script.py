import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import argparse

def download_pdf(url, ext, folder):
    # Get the page
    response = requests.get(url)
    response.raise_for_status()

    # Parse the web page
    soup = BeautifulSoup(response.text, 'html.parser')
    links = [urljoin(url, link.get('href')) for link in soup.find_all('a') if link.get('href')]
    links_pdf = [link for link in links if link.lower().endswith(ext)]

    # If the arg folder doesn't exist yet, create it
    if not os.path.exists(folder):
        os.makedirs(folder)

    # loop for all pdf links
    for link in links_pdf:
        processed_file = link.split('/')[-1]

        # Check if the pdf already exist in the destination folder in order to avoid erasing data/useless use of bandwidth
        file_path = os.path.join(folder, processed_file)
        if os.path.exists(file_path):
            print(f'The file is already in {folder} : {processed_file}')
            continue
        
        # Download the file and write it to the folder
        try:
            response_pdf = requests.get(link)
            response_pdf.raise_for_status()

            with open(file_path, 'wb') as file:
                file.write(response_pdf.content)

            print(f'Downloaded : {processed_file}')

        except requests.RequestException as e:
            print(f'link {link}: {e} has failed')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download pdfs from an URL')
    parser.add_argument('url', help='URL')
    parser.add_argument('ext', help='Extensions e.g. <.pdf>')
    parser.add_argument('folder', help='Destination e.g. /path/to/folder')
    args = parser.parse_args()

    download_pdf(args.url, args.ext, args.folder)
