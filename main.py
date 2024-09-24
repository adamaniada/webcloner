import requests
from urllib.parse import urlparse, urljoin, unquote
from bs4 import BeautifulSoup
import os
from tqdm import tqdm

visited_urls = set()  # Ensemble pour stocker les URLs déjà visitées
def download_page(url, folder_path):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Create folder structure only if needed
        os.makedirs(folder_path, exist_ok=True)

        # Extract and download linked resources
        for tag in soup.find_all(['img', 'link', 'script']):
            if tag.name == 'link' and not tag.get('href').endswith('.css'):
                continue  # Skip non-CSS links
            file_url = tag.get('src' if tag.name in ('img', 'script') else 'href')
            if file_url:
                download_file(urljoin(url, file_url), folder_path, tag.name)

        # Save the HTML page
        filename = os.path.join(folder_path, "index.html" if url == main_url else unquote(os.path.basename(urlparse(url).path)))
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(str(soup))


def download_file(url, folder_path, file_type):
    parsed_url = urlparse(url)
    relative_path = parsed_url.path.strip('/') or "root"
    local_filename = os.path.join(folder_path, relative_path, os.path.basename(parsed_url.path))

    # Download file with progress bar
    with tqdm(desc=f"Downloading {file_type}: {local_filename}", unit="B", unit_scale=True, unit_divisor=1024) as pbar:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            os.makedirs(os.path.dirname(local_filename), exist_ok=True)
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    pbar.update(len(chunk))
                    with open(local_filename, 'wb') as f:
                        f.write(chunk)


def clone_website(url, output_folder):
    global main_url
    main_url = url

    print("Téléchargement de la page principale...")
    download_page(url, output_folder)
    print("Page principale téléchargée avec succès.")

    base_url = urlparse(url).scheme + '://' + urlparse(url).netloc
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        links = [link.get('href') for link in soup.find_all('a') if link.get('href') and not link.get('href').startswith('#')]
        total_links = len(links)
        print(f"Nombre de liens trouvés sur la page principale : {total_links}")

        with tqdm(total=total_links, desc="Téléchargement des pages liées", unit="page") as pbar:
            for idx, link in enumerate(links):
                absolute_url = urljoin(base_url, link)
                download_page_recursive(absolute_url, output_folder)
                pbar.update(1)


def download_page_recursive(url, output_folder):
    if url.startswith(('tel:', 'mailto:')):
        return

    if url in visited_urls:
        print(f"L'URL {url} a déjà été téléchargée, évitant le téléchargement répété.")
        return

    visited_urls.add(url)

    try:
        print(f"Téléchargement de la page : {url}")
        download_page(url, os.path.join(output_folder, urlparse(url).path.strip('/')))

        base_url = urlparse(url).scheme + '://' + urlparse(url).netloc
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            links = [link.get('href') for link in soup.find_all('a') if link.get('href') and not link.get('href').startswith('#')]
            total_links = len(links)

            with tqdm(total=total_links, desc=f"Téléchargement des pages liées {url}", unit="page") as pbar:
                for link in links:
                    absolute_url = urljoin(base_url, link)
                    download_page_recursive(absolute_url, output_folder)
                    pbar.update(1)

    except requests.exceptions.Timeout:
        print(f"La connexion a expiré pour l'URL : {url}")

    except Exception as e:
        print(f"Une erreur s'est produite lors du téléchargement de la page {url}: {e}")


if __name__ == "__main__":
    # Example usage
    clone_website('https://www.aqilas.com/', 'aqilas_clone')
