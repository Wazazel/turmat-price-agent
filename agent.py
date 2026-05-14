import json


# =========================
# SCRAPE PRICE
# =========================

def scrape_price(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")

    selectors = [
        ".price",
        ".product-price",
        ".woocommerce-Price-amount"
    ]

    for selector in selectors:
        element = soup.select_one(selector)

        if element:
            text = element.get_text(strip=True)

            text = (
                text.replace("Kč", "")
                .replace("CZK", "")
                .replace(" ", "")
                .replace(",", ".")
            )

            try:
                return float(text)
            except:
                pass

    return None


# =========================
# MAIN
# =========================

def main():
    products = load_products()

    for product in products:
        name = product["name"]
        url = product["url"]
        target_price = product["target_price"]

        try:
            current_price = scrape_price(url)

            if current_price is None:
                print(f"Cena nenalezena: {name}")
                continue

            print(f"{name}: {current_price} Kč")

            if current_price <= target_price:
                send_discord_message(
                    f"🔥 {name} zlevnil na {current_price} Kč\n{url}"
                )

        except Exception as e:
            print(f"Chyba u produktu {name}")
            print(e)


main()
