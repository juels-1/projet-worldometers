from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Configuration de Selenium avec Chrome
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Mode sans interface graphique
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# Lancer le navigateur
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Charger la page Worldometer
url = "https://www.worldometers.info/world-population/"
driver.get(url)

# Attendre que JavaScript charge les données (ajuste si nécessaire)
time.sleep(5)

# Récupérer le HTML complet après exécution du JavaScript
html_content = driver.page_source

# Enregistrer le HTML dans un fichier
with open("world_population.html", "w", encoding="utf-8") as file:
    file.write(html_content)

# Fermer Selenium
driver.quit()

