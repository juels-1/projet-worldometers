from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Options Chrome supplémentaires pour les environnements serveurs
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")  # Nouvelle version headless, plus stable
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--disable-software-rasterizer")
options.add_argument("--remote-debugging-port=9222")

# Créer le driver avec timeout étendu
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.set_page_load_timeout(60)  # Timeout de 60 secondes

# Charger la page
url = "https://www.worldometers.info/world-population/"
driver.get(url)

# Attendre que JavaScript charge les données
time.sleep(5)

# Récupérer le contenu HTML
html_content = driver.page_source

# Sauvegarder le HTML dans un fichier
with open("world_population.html", "w", encoding="utf-8") as file:
    file.write(html_content)

# Fermer le driver
driver.quit()
