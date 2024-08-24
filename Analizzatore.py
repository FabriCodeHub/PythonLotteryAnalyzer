
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
def generate_combination(probabilities, previous_combinations):
    sorted_numbers = sorted(probabilities, key=probabilities.get, reverse=True)
    
    # Genera combinazioni finché non otteniamo una combinazione unica
    while True:
        combination = sorted(random.sample(sorted_numbers, 6))
        if combination not in previous_combinations:
            previous_combinations.add(tuple(combination))  # Aggiungiamo la combinazione all'insieme delle combinazioni già generate
            return combination

# Funzione per generare 4 combinazioni distinte
def generate_four_combinations(probabilities):
    previous_combinations = set()
    combinations = []
    
    for _ in range(4):
        combination = generate_combination(probabilities, previous_combinations)
        combinations.append(combination)
    
    return combinations

# Funzione per calcolare la percentuale di vincita
def calculate_win_percentage(combination_to_play, winning_sequence):
    intersection = set(combination_to_play) & set(winning_sequence)
    percentage = (len(intersection) / len(winning_sequence)) * 100
    return percentage

# Funzione per inviare un'email con i risultati
def send_email():
    pass  # Funzionalità da completare
