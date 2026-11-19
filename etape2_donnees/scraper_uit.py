import requests
from bs4 import BeautifulSoup
from loguru import logger


def scraper_actualites_uit() -> list:
    """
    Scrapes official announcements or guidelines from the official UIT website
    (with an offline fallback).
    """
    url = "https://univ-internationale.com/fr"
    scraped_data = []
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            for item in soup.find_all(["h2", "h3"], limit=5):
                text = item.get_text(" ", strip=True)
                if len(text) > 10:
                    scraped_data.append({
                        "source": "UIT Official Website",
                        "titre": "Annonce Officielle UIT",
                        "resume": f"Annonce officielle récupérée depuis le site de l'UIT : {text}",
                        "lien": url,
                        "date": "Thu, 19 Nov 2026 00:00:00 +0000",
                    })
            logger.info(f"Successfully scraped {len(scraped_data)} live items from {url}.")
    except Exception as e:
        logger.warning(f"Live web scraping skipped/failed (offline mode): {e}")

    if not scraped_data:
        scraped_data.append({
            "source": "UIT Official Website (Fallback)",
            "titre": "Portail Officiel UIT",
            "resume": (
                "Les étudiants de l'UIT doivent consulter régulièrement le site officiel "
                "https://univ-internationale.com/ pour les actualités, formations et informations académiques."
            ),
            "lien": "https://univ-internationale.com/fr",
            "date": "Thu, 19 Nov 2026 00:00:00 +0000",
        })

    return scraped_data