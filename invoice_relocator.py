from PyPDF4.pdf import PdfFileReader
from PyPDF4.pdf import PdfFileWriter
from pathlib import Path, WindowsPath
import re
import os
import datetime

username = os.getlogin()

base_loc = WindowsPath(f"C:\\Users\\{username}\\Desktop\\Invoices\\")
folder_write_loc = base_loc / str(datetime.date.today())

desktop = WindowsPath(f"C:\\Users\\{username}\\Desktop\\")
pdf_list = [file for file in desktop.glob("*.pdf")]


def check_folder_exists():

    """Check if the folder with today's date exists under the 'Invoices' parent folder. If the 'Invoices' folder, itself, does not exist, create the folder using 'parents=True' option."""

    if folder_write_loc.is_dir():
        print("This folder exists")

    else:
        folder_write_loc.mkdir(parents=True)


def read_pdfs(pdf_list):

    """Take PDF files from base location, examine each to find whether or not this PDF is an invoice file."""

    invoice_list = []

    for pdf in pdf_list:

        with open(pdf, "rb") as file:
            reader = PdfFileReader(file)
            pdf_page = reader.getPage(0)
            pdf_text = pdf_page.extractText()

            if "Invoice" in pdf_text:
                print(f"{pdf} is an invoice")
                invoice_list.append(pdf)

    return invoice_list


def write_pdfs(invoice_list, folder_write_loc):
    
    """Split text in all invoice_list PDF(s). Determine the typical way the pdf is split up, and asssign varaibles. Write invoice PDF(s) to given folder location"""

    for pdf in invoice_list:

        with open(pdf, "rb") as file:
            reader = PdfFileReader(file)
            writer = PdfFileWriter()
            pdf_page = reader.getPage(0)
            writer.addPage(pdf_page)
            pdf_text = pdf_page.extractText()

            res = re.split("\n", pdf_text)

            date = res[0]  # not used
            inv_num = res[1]  # not used
            purch_order_num = res[12]
            cust = res[23]
            cust = cust.split(" ")
            cust = cust[0]

            new_filename = folder_write_loc / f"Zaco_{cust}_{purch_order_num}.pdf"

            with open(new_filename, "wb") as new_file:

                writer.write(new_file)


if __name__ == "__main__":

    check_folder_exists()
    invoice_list = read_pdfs(pdf_list)
    write_pdfs(invoice_list, folder_write_loc)
