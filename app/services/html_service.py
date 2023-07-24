import re
import requests
from bs4 import BeautifulSoup


def get_product_from_url(url):
    # check if url matches these product categories
    prore = re.compile(r"pro\.hukumonline\.com")
    klinikre = re.compile(r"hukumonline\.com/klinik")
    psre = re.compile(r"hukumonline\.com/stories")
    product = "Hukumonline"

    if prore.search(url):
        product = "Hukumonline Pro"
    elif klinikre.search(url):
        product = "Klinik Hukumonline"
    elif psre.search(url):
        product = "Premium Stories"

    return product


class HTMLMeta:
    def __init__(self):
        self.Title = ""
        self.Description = ""
        self.Image = ""
        self.SiteName = ""


def get_metadata_from_source_url(source_url):
    try:
        resp = requests.get(source_url, timeout=90)
        resp.raise_for_status()

        hm = HTMLMeta()
        soup = BeautifulSoup(resp.text, 'html.parser')
        title_found = False

        for tag in soup.find_all(['title', 'meta']):
            if tag.name == 'title':
                title_found = True

            if tag.name == 'meta':
                prop = tag.get('property', '')
                content = tag.get('content', '')

                if prop == 'description':
                    hm.Description = content

                if prop == 'og:title':
                    hm.Title = content

                if prop == 'og:description':
                    hm.Description = content

                if prop == 'og:image':
                    hm.Image = content

                if prop == 'og:site_name':
                    hm.SiteName = content

        for tag in soup.find_all(string=True):
            new_tag = tag.strip()
            if title_found and tag != "\n" and new_tag != "html" and "function" not in new_tag:
                hm.Title = new_tag
                title_found = False

        return hm

    except requests.exceptions.RequestException as e:
        raise Exception(f"Error fetching URL: {e}")
