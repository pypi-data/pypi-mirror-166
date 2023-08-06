from w6libs.PyPDF2 import PdfFileReader


def pdf2txt(path):
    # creating a pdf reader object
    pdf_reader = PdfFileReader(path, 'rb')

    # extracting text from page
    pdf_text = ""
    for page in range(pdf_reader.numPages):
        page_obj = pdf_reader.getPage(page)
        pdf_text += page_obj.extract_text()
    return pdf_text
