# PythonLotteryAnalyzer

Questo script in Python analizza i file PDF contenenti i risultati delle estrazioni del Superenalotto, conta le occorrenze di ciascun numero, calcola le probabilità associate a ciascun numero e genera una combinazione di numeri da giocare basata su queste probabilità. Inoltre, può inviare i risultati via email.

## Funzionalità

1. **Estrazione dei dati dal PDF**: La funzione `extract_data_from_pdf` legge i file PDF contenenti i risultati delle estrazioni del Superenalotto e estrae i dati in un DataFrame di pandas.
2. **Conteggio delle occorrenze**: La funzione `count_number_occurrences` conta quante volte ciascun numero è apparso nelle estrazioni.
3. **Calcolo delle probabilità**: La funzione `calculate_probabilities` calcola la probabilità di apparizione di ciascun numero.
4. **Generazione della combinazione**: La funzione `generate_combination` genera una combinazione di numeri da giocare basata sulle probabilità calcolate.
5. **Calcolo della percentuale di vincita**: La funzione `calculate_win_percentage` calcola la percentuale di vincita della combinazione generata rispetto a una sequenza vincente fornita.
6. **Invio email**: La funzione `send_email` invia i risultati via email.

## Installazione

1. Clonare il repository:
    ```bash
    git clone https://github.com/tuo-username/PythonLotteryAnalyzer.git
    cd PythonLotteryAnalyzer
    ```

2. Creare un ambiente virtuale:
    ```bash
    python -m venv env
    ```

3. Attivare l'ambiente virtuale:

    - Su Windows:
        ```bash
        .\env\Scripts\activate
        ```

    - Su macOS/Linux:
        ```bash
        source env/bin/activate
        ```

4. Installare le dipendenze:
    ```bash
    pip install -r requirements.txt
    ```

## Configurazione

Modifica le seguenti linee in `Analizzatore.py`:

- **Linea 53**:
    ```python
    from_email = 'INSERISCI LA TUA EMAIL DI INVIO'
    password = 'INSERISCI LA TUA PASSWORD DI INVIO'
    ```
- **Linea 66**:
    ```python
    server = smtplib.SMTP_SSL('IL TUO SERVER SMTP EMAIL', PORTA SMTP)
    ```
- **Linea 77**:
    ```python
    pdf_folder_path = r'INSERISCI IL PERCORSO DELLA CARTELLA ARCHIVIO ESTRAZIONI QUI'
    ```
- **Linea 119**:
    ```python
    send_email(subject, body, 'INSERISCI EMAIL RICEVENTE')
    ```

## Utilizzo

1. Posiziona i file PDF nella cartella specificata.
2. Esegui lo script:
    ```bash
    python Analizzatore.py
    ```

## Dipendenze

- `pandas`
- `PyMuPDF`
- `collections`
- `re`
- `random`
- `smtplib`
- `email`

## Licenza

Questo progetto è sotto licenza MIT.
