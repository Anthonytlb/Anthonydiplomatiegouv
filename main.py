import pprint
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from fake_useragent import UserAgent
import time

options = Options()
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option(
    "prefs", {"profile.managed_default_content_settings.media_stream": 2}
)
options.add_argument("--start-maximized")
options.add_argument("--disable-infobars")
# options.add_argument('--disable-extensions')
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
options.add_argument("--window-size=1920,1200")
options.add_argument("--start-fullscreen")
options.add_argument("--mute-audio")
options.add_extension("./ublock.crx")
options.add_argument("--blink-settings=imagesEnabled=false")
options.add_argument("--disable-notifications")
options.add_argument(
    "--disable-features=PreloadMediaEngagementData,MediaEngagementBypassAutoplayPolicies"
)
options.add_argument("--autoplay-policy=user-required")
ua = UserAgent()
user_agent = ua.random
options.add_argument(f"user-agent={user_agent}")

monpilote = webdriver.Chrome(options=options)
print("Chrome démarré")

monpilote.get("https://www.diplomatie.gouv.fr/fr")
print("Navigation page")

monbouton = WebDriverWait(monpilote, timeout=3).until(
    expected_conditions.element_to_be_clickable(
        (By.XPATH, "/html/body/div[1]/div[4]/button[2]")
    )
)
time.sleep(0.5)
monbouton.click()
print("Cookie cliqué")

time.sleep(1)


bouton_voyageurs = WebDriverWait(monpilote, timeout=10).until(
    expected_conditions.element_to_be_clickable(
        (
            By.XPATH,
            "/html/body/div[2]/main/div[1]/div/div/div[2]/article/div[2]/div[2]/div/div[3]/div/div[1]/div/h2/a",
        )
    )
)
bouton_voyageurs.click()
print("Cliqué sur Conseils aux voyageurs")


from selenium.webdriver.support.ui import Select

menu_pays = WebDriverWait(monpilote, timeout=10).until(
    expected_conditions.presence_of_element_located(
        (
            By.XPATH,
            "/html/body/div[2]/main/div[1]/div[2]/div/div[2]/article/div[1]/div/div/div[2]/div/div[2]/div/div/form/div/select",
        )
    )
)
select = Select(menu_pays)
select.select_by_visible_text("Brésil")
print("Brésil sélectionné")
time.sleep(0.5)
bouton_valider = WebDriverWait(monpilote, timeout=10).until(
    expected_conditions.element_to_be_clickable(
        (
            By.XPATH,
            "/html/body/div[2]/main/div[1]/div[2]/div/div[2]/article/div[1]/div/div/div[2]/div/div[2]/div/div/form/input[1]",
        )
    )
)
bouton_valider.click()
print("Validé")


dans_cette_rubrique = WebDriverWait(monpilote, timeout=10).until(
    expected_conditions.element_to_be_clickable(
        (
            By.XPATH,
            '//*[@id="block-diplomatie-navigation-laterale-fiche-pays"]/div/button',
        )
    )
)
dans_cette_rubrique.click()
print("Cliqué sur Dans cette rubrique")


politique_economie = WebDriverWait(monpilote, timeout=10).until(
    expected_conditions.element_to_be_clickable(
        (By.XPATH, '//*[@id="fr-sidemenu-wrapper"]/ul/li[3]/a')
    )
)
politique_economie.click()
print("Cliqué sur Politique et économie")


liste_representations = WebDriverWait(monpilote, timeout=10).until(
    expected_conditions.presence_of_all_elements_located(
        (
            By.XPATH,
            '//*[@id="block-diplomatie-fichepaysrepresentations"]/div[position()>1]/article/div/p[1]',
        )
    )
)

a = []
a.append(["Adresse", "Ville", "Code Postal", "Pays"])
for representation in liste_representations:
    info = representation.text
    print(info)
    if info != "":
        lignes = info.split("\n")
        while len(lignes) < 4:
            lignes.append("")
        a.append(lignes[:4])
print(a)
pprint.pprint(a)


import csv

fichier = open("consulats_bresil.csv", "w", newline="", encoding="utf-8-sig")
ecrivain = csv.writer(fichier, delimiter=",")
ecrivain.writerows(a)
fichier.close()
print("Fichier enregistré : consulats_bresil.csv")


fichier = open("AnthonyBabilotte.csv", "w", newline="", encoding="utf-8-sig")
ecrivain = csv.writer(fichier, delimiter=",")
ecrivain.writerows(a)
fichier.close()
print("Fichier enregistré : AnthonyBabilotte.csv")
monpilote.quit()


input("pause")
