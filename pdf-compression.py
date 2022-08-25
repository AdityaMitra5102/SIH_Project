pip install PyMuPDF


import glob, sys, fitz
import img2pdf
from PIL import Image
import os

zoom_x = 2.0 
zoom_y = 2.0  
mat = fitz.Matrix(zoom_x, zoom_y) 
path = '/home/anorak/Desktop/MIND-PALACE/SIH_Project-main/pdfdata/'
all_files = glob.glob(path + "*.pdf")
for filename in all_files:
    doc = fitz.open(filename) 
    for page in doc: 
        pix = page.get_pixmap(matrix=mat)  
        pix.save("/home/anorak/Desktop/MIND-PALACE/SIH_Project-main/pdfdata/page-%i.png" % page.number)

img_path = "/home/anorak/Desktop/MIND-PALACE/SIH_Project-main/pdfdata/compressed.png"
pdf_path = "/home/anorak/Desktop/MIND-PALACE/SIH_Project-main/pdfdata/compressed.pdf"
image = Image.open(img_path)
pdf_bytes = img2pdf.convert(image.filename)
file = open(pdf_path, "wb")
file.write(pdf_bytes)
image.close()
file.close()
print("Successfully made pdf file")
