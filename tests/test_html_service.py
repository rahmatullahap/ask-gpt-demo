import responses
import requests
import pytest
from app.services.html_service import get_product_from_url, get_metadata_from_source_url

class TestGetProductFromUrl:
    # Tests that a valid url for Hukumonline Pro returns the correct product
    def test_valid_url_pro(self):
        url = 'https://pro.hukumonline.com/berita/2021/06/28/bpjs-ketenagakerjaan-akan-berikan-bantuan-jht-untuk-peserta-yang-terdampak-covid-19'
        assert get_product_from_url(url) == 'Hukumonline Pro'

    # Tests that a valid url for Klinik Hukumonline returns the correct product
    def test_valid_url_klinik(self):
        url = 'https://www.hukumonline.com/klinik/detail/lt5f1d7a6c8b0d9/putusan-pengadilan-terkait-penyelesaian-sengketa-tanah/'
        assert get_product_from_url(url) == 'Klinik Hukumonline'

    # Tests that a valid url for Premium Stories returns the correct product
    def test_valid_url_premium_stories(self):
        url = 'https://www.hukumonline.com/stories/2021/06/28/pemerintah-diminta-tidak-membiarkan-kasus-korupsi-di-bumn-terulang/'
        assert get_product_from_url(url) == 'Premium Stories'

    # Tests that an empty url returns the default product
    def test_empty_url(self):
        url = ''
        assert get_product_from_url(url) == 'Hukumonline'

    # Tests that a non-string url raises an exception
    def test_non_string_url(self):
        url = 123
        with pytest.raises(TypeError):
            get_product_from_url(url)

    # Tests that an invalid url returns the default product
    def test_invalid_url(self):
        url = 'https://www.google.com/'
        assert get_product_from_url(url) == 'Hukumonline'

class TestGetMetadataFromSourceURL:
    def test_get_metadata_from_source_url_helpcenter(self):
        url = "https://www.hukumonline.com/helpcenter"

        result = get_metadata_from_source_url(url)
        assert "Pertanyaan dan Jawaban Penggunaan Layanan | Hukumonline" == result.Title
        assert "Daftar pertanyaan yang sering diajukan pengguna baru. Periksa terlebih dahulu apakah pertanyaan yang akan Anda ajukan telah terjawab atau belum di sini." == result.Description

    @responses.activate
    def test_get_metadata_from_source_url_meta(self):
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
    def test_get_metadata_from_source_url_description(self):
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
    def test_get_metadata_from_source_url_title_not_found(self):
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
    def test_get_metadata_from_source_url_text_true(self):
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
    def test_get_metadata_from_source_url_error(self):
        body = """"""
        url = "https://pro.hukumonline.com/a/abcd"
        responses.add(responses.GET, url, body=requests.exceptions.RequestException("Error Function"), status=400)

        with pytest.raises(Exception) as exc_info:
            get_metadata_from_source_url(url)
        assert str(exc_info.value) == "Error fetching URL: Error Function"
