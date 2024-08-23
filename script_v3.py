import requests
from bs4 import BeautifulSoup
import schedule
import time
import smtplib
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def check_value():
    # Configuration du navigateur Selenium avec les options
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")


    driver = webdriver.Chrome(options=options)
    
    try:
        # Naviguer vers la page de connexion
        driver.get('https://www.stych.fr/connexion')

        print("Connexion en cours...")

        username_field = driver.find_element(By.NAME, "email")
        password_field = driver.find_element(By.NAME, "mdp")
        username_field.send_keys("adresse mail") # Identifiant du site stych.fr
        password_field.send_keys("password") # Mot de passe du site stych.fr
        password_field.send_keys(Keys.RETURN)

        print("Connecté !")
        
        time.sleep(5)  # Attendez quelques secondes pour que la page se charge

        # Naviguer vers la page cible après connexion
        driver.get('https://www.stych.fr/elearning/formation/conduite/reservation/planning')

        print("Récupération de la valeur...")

        time.sleep(5) # Attendez quelques secondes pour que la page se charge

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        info_div = soup.find('div', id='information-message')
        
        if info_div:
            info_message = info_div.find('span').text.strip()
            print("Message d'information :", info_message)
            
            if "Nous n’avons pas trouvé de disponibilités" in info_message:
                print("Aucune disponibilité trouvée.")
            else:
                notify_user(info_message)
        else:
            print("La div avec l'id 'information-message' n'a pas été trouvée.")
    
    finally:
        driver.quit()

def notify_user(message):
    # Configuration du serveur SMTP de Gmail
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    
    # Connexion au compte Gmail
    server.login("adresse mail @gmail.com", "password") # Changer l'adresse email et le mot de passe d'applications : créer un mot de passe d'applications sur https://myaccount.google.com/apppasswords

    # Contenu de l'email
    sujet = "Notification du script"
    corps = f"Valeur détectée sur le site : {message}"
    message = f'Subject: {sujet}\n\n{corps}'

    recipients = ["email address"] # Liste des destinataires

    # Envoi de l'email
    server.sendmail("adresse mail @gmail.com", recipients, message.encode('utf-8')) # Changer l'adresse email de l'expéditeur
    server.quit()

# Planification du script entre 8h et 20h
def job():
    current_hour = time.localtime().tm_hour
    if 8 <= current_hour < 20:
        check_value()

schedule.every(30).minutes.do(job) # Changer la fréquence de vérification (en minutes) | Actuellement, le script vérifie la valeur toutes les 30 minutes

while True:
    schedule.run_pending()
    time.sleep(1)
