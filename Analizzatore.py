import os
import pandas as pd
from collections import Counter
import fitz  # PyMuPDF
import re
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Funzione per estrarre i dati dal PDF
def extract_data_from_pdf(pdf_path):
    pdf_document = fitz.open(pdf_path)
    data = []

    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text = page.get_text()
        matches = re.findall(r"(\d+)\s(\d{2}/\d{2}/\d{4})\s((?:\d+\s){6})\d+\s-\s", text)
        for match in matches:
            concorso, data_str, numbers = match
            numbers = numbers.strip().split()
            data.append([int(concorso), data_str] + [int(num) for num in numbers])
    
    pdf_document.close()
    columns = ["Conc", "Date", "Num1", "Num2", "Num3", "Num4", "Num5", "Num6"]
    df = pd.DataFrame(data, columns=columns)
    return df

# Funzione per contare le occorrenze di ciascun numero
def count_number_occurrences(df):
    number_counter = Counter()
    for number in df[['Num1', 'Num2', 'Num3', 'Num4', 'Num5', 'Num6']].values.flatten():
        number_counter[number] += 1
    return number_counter

# Funzione per calcolare le probabilità di ciascun numero
def calculate_probabilities(number_counter, total_numbers):
    probabilities = {num: count / total_numbers for num, count in number_counter.items()}
    return probabilities

# Funzione per generare una combinazione di 6 numeri basata sulle probabilità
def generate_combination(probabilities):
    sorted_numbers = sorted(probabilities, key=probabilities.get, reverse=True)
    return sorted_numbers[:6]

# Funzione per calcolare la percentuale di vincita
def calculate_win_percentage(combination_to_play, winning_sequence):
    intersection = set(combination_to_play) & set(winning_sequence)
    percentage = (len(intersection) / len(winning_sequence)) * 100
    return percentage

# Funzione per inviare un'email con i risultati
def send_email(subject, body, to_email):
    from_email = 'INSERISCI LA TUA EMAIL DI INVIO'
    password = 'INSERISCI LA TUA PASSWORD DI INVIO'
    
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP_SSL('IL TUO SERVER SMTP EMAIL', PORTA SMTP) # type: ignore
        server.login(from_email, password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        print("Email inviata con successo.")
    except Exception as e:
        print(f"Errore durante l'invio dell'email: {e}")

# Funzione principale per gestire l'interazione con l'utente
def main():
    # Definisci il percorso della cartella contenente i file PDF
    pdf_folder_path = r'INSERISCI IL PERCORSO DELLA CARTELLA ARCHIVIO ESTRAZIONI QUI'

    # Leggere tutti i file PDF nella cartella
    all_dfs = []
    for file_name in os.listdir(pdf_folder_path):
        if file_name.endswith('.pdf'):
            pdf_path = os.path.join(pdf_folder_path, file_name)
            pdf_df = extract_data_from_pdf(pdf_path)
            all_dfs.append(pdf_df)

    # Concatenare tutti i dataframe
    df = pd.concat(all_dfs, ignore_index=True)

    # Contare le occorrenze di ciascun numero nelle estrazioni
    number_counter = count_number_occurrences(df)

    # Calcolare le probabilità di ciascun numero
    total_numbers = df[['Num1', 'Num2', 'Num3', 'Num4', 'Num5', 'Num6']].size
    probabilities = calculate_probabilities(number_counter, total_numbers)

    # Chiedi all'utente se vuole creare una combinazione
    risposta = input("Creo Combinazione? (SI/NO): ")

    if risposta.upper() == "SI":
        # Generazione della combinazione da giocare basata sulle probabilità calcolate
        combination_to_play = generate_combination(probabilities)

        # Stampare la combinazione generata
        print("Combinazione Generata:", combination_to_play)

        # Calcolo della percentuale di vincita
        # Supponiamo che winning_sequence sia una lista dei numeri vincenti estratti in un concorso.
        # Inserisci qui la lista dei numeri vincenti
        winning_sequence = [1, 2, 3, 4, 5, 6]  # Sostituisci questa lista con la sequenza vincente effettiva

        win_percentage = calculate_win_percentage(combination_to_play, winning_sequence)
        print("Percentuale di vincita della combinazione generata:", win_percentage, "%")
        
        # Invia i risultati via email
        subject = "Risultati Superenalotto"
        body = f"Combinazione Generata: {combination_to_play}\nPercentuale di vincita: {win_percentage}%"
        send_email(subject, body, 'INSERISCI EMAIL RICEVENTE')  # Sostituisci con l'email del destinatario

    elif risposta.upper() == "NO":
        print("Processo terminato.")
    else:
        print("Risposta non valida. Si prega di rispondere con 'SI' o 'NO'.")

if __name__ == "__main__":
    main()
