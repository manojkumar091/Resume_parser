from os import replace
from PyPDF2 import PdfFileReader
import PyPDF2
import sqlite3
import re


def extract_information(pdf_path):

    # reading the PDF file 
    pdfFileObj = open(pdf_path, 'rb')    
    pdf = PdfFileReader(pdfFileObj)

    #information variable stores the document object
    information = pdf.getDocumentInfo()
    number_of_pages = pdf.getNumPages()
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    pageObj = pdfReader.getPage(0)

    #extracting the data from the file to text 
    text=(pageObj.extractText())

    #email text data to be extracted using regex for validations
    emailvalue = text.replace('\n','').replace('\t','')

    #value is the variable which stores the data 
    value = text.split( ";")

    # the file name can be fetched from the path 
    filename = pdf_path

    #name of the user if it is not fetched from the extracted files try block is used
    try:
        name = information.author
    except:
        name = None

    # all document informations are recorded
    subject =  information.subject
    title = information.title
    number_of_pages =  number_of_pages

    #regex for extracting mobile number
    r = re.compile(r'(\b([0-9]{10}|[0-9\s]{12})\b)')

    results = r.search(text)

    #regex for extracting email
    email_result = re.findall("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", emailvalue)

    #techstack key words
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
        #DB connection db name  : sqlite3
        sqliteConnection = sqlite3.connect('pdf_parsing.db')
        cursor = sqliteConnection.cursor()
        print("Successfully Connected to SQLite")

        #insert query
        sqlite_select_Query = f"INSERT INTO Candidates (tech_statck,phone_details,email_details,name,filename,subject,title)\
              VALUES('{lst[0]}','{phone_details}','{email_result[0]}','{name}','{filename}','{subject}','{title}')"

        cursor.execute(sqlite_select_Query)
        sqliteConnection.commit()
        cursor.close()

        print('data added successfully')

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)

    finally:
        # closing the DB connection
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")

if __name__ == '__main__':
    path = 'Resume.pdf'
    extract_information(path)

