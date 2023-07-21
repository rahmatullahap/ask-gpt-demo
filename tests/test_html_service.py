from app.services.html_service import get_product_from_url

def test_get_product_from_url():
    url = "https://pro.hukumonline.com/a/lt603de18a503ca/peraturan-pemerintah-tentang-pelaksanaan-perizinan-berusaha-berbasis-risiko---bagian-ii--bidang-usaha-energi-dan-sumber-daya-alam"
    result = get_product_from_url(url)
    assert "Hukumonline Pro" in result
