from unittest.case import TestCase
import os

from pdfminer.pdfpage import PDFPage

from pdfminer.converter import PDFPageAggregator

from pdfminer.pdfdevice import PDFDevice

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter

from pdfminer.pdfdocument import PDFDocument, PDFTextExtractionNotAllowed

from pdfminer.pdfparser import PDFParser

from pdfminer.layout import LTTextBoxHorizontal, LTChar, LTAnno, LAParams


def dump_pdf(a_pdf, indent=""):
    if not isinstance(a_pdf, LTTextBoxHorizontal):
        print(indent + str(a_pdf))
    else:
        print("LTTextBox")
    if hasattr(a_pdf, "_objs"):
        for a_leaf in a_pdf._objs:
            if not isinstance(a_leaf, (LTChar, LTAnno)):
                dump_pdf(a_leaf, indent=indent + 4 * " ")


def load_pdf(a_pdf_file):
    path = os.path.dirname(__file__)
    # Open a PDF file.
    fp = open(path + "/" + a_pdf_file, 'rb')
    # Create a PDF parser object associated with the file object.
    parser = PDFParser(fp)
    # Create a PDF document object that stores the document structure.
    # Supply the password for initialization.
    document = PDFDocument(parser)
    # Check if the document allows text extraction. If not, abort.
    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed
    # Create a PDF resource manager object that stores shared resources.
    rsrcmgr = PDFResourceManager()
    # Create a PDF device object.
    device = PDFDevice(rsrcmgr)
    # Create a PDF interpreter object.
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    # Process each page contained in the document.
    laparams = LAParams()
    # Create a PDF page aggregator object.
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    all_pages = []
    for page in PDFPage.create_pages(document):
        interpreter.process_page(page)
        # receive the LTPage object for the page.
        layout = device.get_result()
        all_pages.append(layout)
    return all_pages



class TablePDFTest(TestCase):

    def test_tabled_pdf(self):
        all_pages = load_pdf("fixtures/tabled_pdf.pdf")
        for a_page in all_pages:
            dump_pdf(a_page)
