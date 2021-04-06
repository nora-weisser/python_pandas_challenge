import isodate
import pandas as pd
import numpy as np

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

INPUT_URL = 'https://s3-eu-west-1.amazonaws.com/dwh-test-resources/recipes.json'
OUTPUT_PATH = 'result.csv'

CHILI_FORMS = [
    'chile',
    'chiles',
    'chili',
    'chilies',
    'chilled',
]


def check_contains_word(line, words):
    """
    :param line: whitespace separated line
    :param words: set of values for the filtering
    :return: if any of the words in the line is contained in the words
    """
    search_words = set(words)
    for line_word in line.split():
        if line_word.lower() in search_words:
            return True
    return False


def check_contains_word_2(line, prefix):
    """
    :param line: whitespace separated line
    :param prefix:
    :return: if any of the words in the line starts with the prefix
    """
    for line_word in line.split():
        if line_word.lower().startswith(prefix):
            return True
    return False


def convert_duration_to_minutes(pt_duration):
    """
    The function converts PT duration to minutes
    :param pt_duration
    :return: duration in minutes
    """
    if pt_duration == '':
        return None
    seconds = isodate.parse_duration(pt_duration).total_seconds()
    minutes = seconds / 60
    return minutes


def download_recipes(url):
    """
    The function downloads the recipes
    :param url: string, URL for downloading the recipes
    :return: dataframe with recipes
    """
    return pd.read_json(url, lines=True)


def calculate_difficulty(cook_time, prep_time):
    """
    The function calculates difficulty of the cooking process
    :param cook_time: int
    :param prep_time: int
    :return: string, difficulty
    """
    total_time = cook_time + prep_time

    if np.isnan(total_time):
        return 'Unknown'
    elif total_time > 60:
        return 'Hard'
    elif total_time >= 30:
        return 'Medium'
    else:
        return 'Easy'


def send_mail():
    mail_content = '''There is the result of Python script - .csv file
    '''

    # The mail addresses and password
    sender_address = 'eleonora.belova.16@gmail.com'
    sender_pass = 'XXXXXXXXXXX'
    receiver_address = 'eleo.belova@yandex.ru'

    # Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'The result of Python script'

    # The subject line
    # The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    attach_file_name = 'result.csv'
    attach_file = open(attach_file_name, 'rb')  # Open the file as binary mode
    payload = MIMEBase('application', 'octate-stream')
    payload.set_payload((attach_file).read())
    encoders.encode_base64(payload)  # encode the attachment

    # add payload header with filename
    payload.add_header('Content-Decomposition', 'attachment', filename=attach_file_name)
    message.attach(payload)

    # Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
    session.starttls()  # enable security
    session.login(sender_address, sender_pass)  # login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent')


if __name__ == '__main__':
    df = download_recipes(INPUT_URL)

    # Filter
    chili_mask = df['ingredients'].apply(lambda x: check_contains_word(x, CHILI_FORMS))
    # chili_mask = df['ingredients'].apply(lambda x: check_contains_word_2(x, 'chili'))
    df = df[chili_mask]

    # Parse duration
    df['cookTime_minutes'] = df['cookTime'].apply(convert_duration_to_minutes)
    df['prepTime_minutes'] = df['prepTime'].apply(convert_duration_to_minutes)

    # Calculate difficulty
    df['difficulty'] = df.apply(lambda row: calculate_difficulty(row['cookTime_minutes'], row['prepTime_minutes']),
                                axis=1)

    # Save dataframe
    df = df.drop(columns=['prepTime_minutes', 'cookTime_minutes'])
    df.to_csv(OUTPUT_PATH, index=False)

    #Send email to eleo.belova@yandex.ru with a file
    send_mail()
