from app.services.html_service import get_product_from_url

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
