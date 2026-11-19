import requests
from bs4 import BeautifulSoup
from loguru import logger

def scraper_actualites_uit() -> list:
    """
    Scrapes official announcements or guidelines from academic pages (or fallback simulation).
    """
    url = "https://univ-internationale.com/"
    scraped_data = []
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Extract headings or announcements if available
            for item in soup.find_all(['h2', 'h3'], limit=5):
                text = item.get_text().strip()
                if len(text) > 10:
                    scraped_data.append({
                        "source": "UIT Web Scraper",
                        "titre": "Annonce Officielle en Ligne",
                        "resume": f"Annonce officielle récupérée du site de l'UIT : {text}",
                        "lien": url,
                        "date": "Wed, 18 Nov 2026 00:00:00 +0000"
                    })
            logger.info(f"Successfully scraped {len(scraped_data)} live items from UIT website.")
    except Exception as e:
        logger.warning(f"Live web scraping skipped/failed (offline mode): {e}")
        # Fallback structural items if offline
        scraped_data.append({
            "source": "UIT Web Scraper (Fallback)",
            "titre": "Portail Numérique UIT",
            "resume": "Les étudiants de l'UIT doivent consulter régulièrement le portail officiel pour les plannings d'examens et notes.",
            "lien": "https://univ-internationale.com/",
            "date": "Wed, 18 Nov 2026 00:00:00 +0000"
        })

    return scraped_data