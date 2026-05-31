from collections import Counter
import re
import requests
from bs4 import BeautifulSoup
def analyze_website_seo(url):
    print(f"--- ГЛИБОКИЙ АНАЛІЗ САЙТУ: {url} ---\n")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            print(f"Помилка завантаження сторінки. Код: {response.status_code}")
            return
        soup = BeautifulSoup(response.text, "html.parser")
        page_text = soup.get_text().lower()
        words = re.findall(r"\b\w+\b", page_text)
        meaningful_words = [w for w in words if len(w) > 3]
        print(f"📊 МЕТРИКИ ТЕКСТУ:")
        print(f"   Загальна кількість слів: {len(words)}")
        print(f"   Унікальних слів: {len(set(words))}")
        word_counts = Counter(meaningful_words)
        top_words = word_counts.most_common(5)
        print("\n🔝 ТОП-5 ключових слів на сторінці:")
        for word, count in top_words:
            print(f"   - '{word}': зустрічається {count} разів")
        print("-" * 40)
        images = soup.find_all("img")
        images_without_alt = [img for img in images if not img.get("alt")]
        print(f"🖼️АНАЛІЗ МЕДІА:")
        print(f"Усього зображень на сторінці: {len(images)}")
        print(f"Зображень без опису (тегу alt): {len(images_without_alt)} ⚠️ (це мінус для SEO)")
        print("-" * 40)
        links = soup.find_all("a")
        internal_links = 0
        external_links = 0
        for link in links:
            href = link.get("href")
            if href:
                if href.startswith("http") and url not in href:
                    external_links += 1
                elif href.startswith("/") or url in href:
                    internal_links += 1
        print(f"🔗 АНАЛІЗ ПОСИЛАНЬ:")
        print(f"   Загалом посилань: {len(links)}")
        print(f"   Внутрішні (ведуть на цей же сайт): {internal_links}")
        print(f"   Зовнішні (ведуть на інші сайти): {external_links}")
    except Exception as e:
        print(f"Сталася помилка під час аналізу: {e}")
if __name__ == "__main__":
    analyze_website_seo("https://news.google.com")