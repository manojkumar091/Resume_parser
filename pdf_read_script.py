from os import replace
from PyPDF2 import PdfFileReader
import PyPDF2
import sqlite3
import re


def extract_information(pdf_path):

    pdfFileObj = open(pdf_path, 'rb')
    pdf = PdfFileReader(pdfFileObj)
    information = pdf.getDocumentInfo()
    number_of_pages = pdf.getNumPages()
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    pageObj = pdfReader.getPage(0)

    text=(pageObj.extractText())
    emailvalue = text.replace('\n','').replace('\t','')
    value = text.split( ";")

    filename = pdf_path

    name = information.author
    subject =  information.subject
    title = information.title
    number_of_pages =  number_of_pages

    r = re.compile(r'(\b([0-9]{10}|[0-9\s]{12})\b)')

    results = r.search(text)

    email_result = re.findall("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", emailvalue)

    search_keywords=['Django','Vue','Javascript' , 'python' , 'java','ruby' , 'AWS' , 'C++' , 'C#' , 'PHP' , 'Perl']

    lst = []

    for sentence in value:
        for word in search_keywords:
            if word in sentence:
                lst.append(word)

    try:
        phone_details = results.group()
    
    except:

        phone_details = None

    try:
        sqliteConnection = sqlite3.connect('pdf_parsing.db')
        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")

        sqlite_select_Query = f"INSERT INTO Candidates (tech_statck,phone_details,email_details,name,filename,subject,title)\
              VALUES('{lst[0]}','{phone_details}','{email_result[0]}','{name}','{filename}','{subject}','{title}')"

        print('sqlite_select_Query' , sqlite_select_Query)

        cursor.execute(sqlite_select_Query)
        sqliteConnection.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)

    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")

if __name__ == '__main__':
    path = 'Resume.pdf'
    extract_information(path)

