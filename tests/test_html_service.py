import responses
import requests
import pytest
from app.services.html_service import get_product_from_url, get_metadata_from_source_url

def test_get_product_from_url_pro():
    url = "https://pro.hukumonline.com/a/abcd"
    result = get_product_from_url(url)
    assert "Hukumonline Pro" in result

def test_get_product_from_url_klinik():
    url = "https://www.hukumonline.com/klinik/abcd"
    result = get_product_from_url(url)
    assert "Klinik Hukumonline" in result

def test_get_product_from_url_story():
    url = "https://www.hukumonline.com/stories/abcd"
    result = get_product_from_url(url)
    assert "Premium Stories" in result

def test_get_product_from_url_product():
    url = "https://www.hukumonline.com/xyz"
    result = get_product_from_url(url)
    assert "Hukumonline" in result

def test_get_metadata_from_source_url_helpcenter():
    url = "https://www.hukumonline.com/helpcenter"

    result = get_metadata_from_source_url(url)
    assert "Pertanyaan dan Jawaban Penggunaan Layanan | Hukumonline" == result.Title
    assert "Daftar pertanyaan yang sering diajukan pengguna baru. Periksa terlebih dahulu apakah pertanyaan yang akan Anda ajukan telah terjawab atau belum di sini." == result.Description

@responses.activate
def test_get_metadata_from_source_url_meta():
    body = """
    <title>Title Hukumonline.com</title>
    <meta property="og:site_name" content="hukumonline.com" />
    <meta property="og:type" content="website" />
    <meta property="og:title" content="Title Hukumonline.com"/>
    <meta property="og:description" content="This is Description"/>
    <meta property="og:image" content="https://static.hukumonline.com/frontend/default/images/kaze/default.jpg" />
    """
    url = "https://pro.hukumonline.com/a/abcd"
    responses.add(responses.GET, url, body=body, status=200)

    result = get_metadata_from_source_url(url)
    assert "Title Hukumonline.com" == result.Title
    assert "This is Description" == result.Description
    assert "https://static.hukumonline.com/frontend/default/images/kaze/default.jpg" == result.Image
    assert "hukumonline.com" in result.SiteName

@responses.activate
def test_get_metadata_from_source_url_description():
    body = """
    <title>Title Hukumonline.com</title>
    <meta property="description" content="This is Description"/>
    <meta property="og:site_name" content="hukumonline.com" />
    <meta property="og:type" content="website" />
    <meta property="og:title" content="Title Hukumonline.com"/>
    <meta property="og:image" content="https://static.hukumonline.com/frontend/default/images/kaze/default.jpg" />
    """
    url = "https://pro.hukumonline.com/a/abcd"
    responses.add(responses.GET, url, body=body, status=200)

    result = get_metadata_from_source_url(url)
    assert "Title Hukumonline.com" == result.Title
    assert "This is Description" == result.Description
    assert "https://static.hukumonline.com/frontend/default/images/kaze/default.jpg" == result.Image
    assert "hukumonline.com" in result.SiteName

@responses.activate
def test_get_metadata_from_source_url_title_not_found():
    body = """
    <meta property="description" content="This is Description"/>
    <meta property="og:site_name" content="hukumonline.com" />
    <meta property="og:type" content="website" />
    <meta property="og:title" content="Title Hukumonline.com"/>
    <meta property="og:image" content="https://static.hukumonline.com/frontend/default/images/kaze/default.jpg" />
    """
    url = "https://pro.hukumonline.com/a/abcd"
    responses.add(responses.GET, url, body=body, status=200)

    result = get_metadata_from_source_url(url)
    assert "Title Hukumonline.com" == result.Title
    assert "This is Description" == result.Description
    assert "https://static.hukumonline.com/frontend/default/images/kaze/default.jpg" == result.Image
    assert "hukumonline.com" in result.SiteName

@responses.activate
def test_get_metadata_from_source_url_text_true():
    body = """
    <title>Pertanyaan dan Jawaban Penggunaan Layanan | Hukumonline</title>
    <meta property="description" content="This is Description"/>
    <meta property="og:site_name" content="hukumonline.com" />
    <meta property="og:type" content="website" />
    <meta
      property="og:title"
      content="Pertanyaan dan Jawaban Penggunaan Layanan | Hukumonline"
    />
    <meta property="og:image" content="https://static.hukumonline.com/frontend/default/images/kaze/default.jpg" />
    <body>Hello World</body>
    """
    url = "https://pro.hukumonline.com/a/abcd"
    responses.add(responses.GET, url, body=body, status=200)

    result = get_metadata_from_source_url(url)
    assert "Pertanyaan dan Jawaban Penggunaan Layanan | Hukumonline" == result.Title
    assert "This is Description" == result.Description
    assert "https://static.hukumonline.com/frontend/default/images/kaze/default.jpg" == result.Image
    assert "hukumonline.com" in result.SiteName

@responses.activate
def test_get_metadata_from_source_url_error():
    body = """"""
    url = "https://pro.hukumonline.com/a/abcd"
    responses.add(responses.GET, url, body=requests.exceptions.RequestException("Error Function"), status=400)

    with pytest.raises(Exception) as exc_info:
        get_metadata_from_source_url(url)
    assert str(exc_info.value) == "Error fetching URL: Error Function"
