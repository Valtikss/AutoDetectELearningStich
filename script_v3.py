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
        
        # Vérification des messages
        info_div = soup.find('div', id='information-message')
        max_prop_div = soup.find('div', id='max-proposition-filter')
        
        if info_div and max_prop_div:
            info_message = info_div.find('span').text.strip()
            max_prop_message = max_prop_div.find('span').text.strip()

            if info_message:
                print("Message d'information :", info_message)
                if "Nous n’avons pas trouvé de disponibilités" in info_message:
                    print("Aucune disponibilité trouvée.")
            elif max_prop_message:
                print("Message max proposition filter:", max_prop_message)

                # If courses are available, retrieve them
                courses = soup.find_all('div', class_='course')
                courses_details = []
                for course in courses:
                    date = course.find_previous('div', class_='course-day').text.strip()
                    time = course.find('div', class_='course-time').text.strip()
                    address = course.find('div', class_='course-address').text.strip()
                    courses_details.append(f"{date} - {time} - {address}")

                notify_user(None, courses_details)
        else:
            print("Les divs 'information-message' ou 'max-proposition-filter' n'ont pas été trouvées.")
    
    finally:
        driver.quit()

def notify_user(info_message, courses):
    # Configuration du serveur SMTP de Gmail
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    
    # Connexion au compte Gmail
    server.login("adresse mail @gmail.com", "password") # Changer l'adresse email et le mot de passe d'applications : créer un mot de passe d'applications sur https://myaccount.google.com/apppasswords

    # Contenu de l'email
    sujet = "Notification du script"
    
    if info_message:
        corps = f"Message d'information : {info_message}"
    elif courses:
        corps = "Cours disponibles :\n" + "\n".join(courses)
    else:
        corps = "Aucun message ou cours à notifier."
        
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
