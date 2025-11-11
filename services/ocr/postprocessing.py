import re

def extract_listing_info(text):
    data = {}

    # İlan No
    ilan_no = re.search(r"İlan No\s*(\d+)", text)
    if ilan_no:
        data["ilan_no"] = ilan_no.group(1)

    # Marka
    marka = re.search(r"Marka\s*([A-Za-zÇÖÜĞİŞçöüğiş]+)", text)
    if marka:
        data["marka"] = marka.group(1)

    # Seri/Model
    seri = re.search(r"Model\s*([A-Za-z0-9 ÇÖÜĞİŞçöüğiş]+)", text)
    if seri:
        data["model"] = seri.group(1).strip()

    # KM
    km = re.search(r"KM\s*([\d\.]+)", text)
    if km:
        data["km"] = km.group(1).replace(".", "")

    # Yıl
    yil = re.search(r"Yıl\s*(\d{4})", text)
    if yil:
        data["yil"] = yil.group(1)

    # Renk
    renk = re.search(r"Renk\s*([A-Za-zÇÖÜĞİŞçöüğiş]+)", text)
    if renk:
        data["renk"] = renk.group(1)

    return data
