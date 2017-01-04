#!/usr/bin/env python
# -*- coding: utf-8 -*-

#converting to .exe:
#first, comment out the lines starting with excludedimports in files \PyInstaller\hooks\hook-PIL.py and hook-PIL.SpiderImagePlugin.py
#cd C:\Users\cdrouadaine\Downloads\Install\PyInstaller-3.1\PyInstaller-3.1
#pyinstaller.py -F --hidden-import=Tkinter C:\Users\cdrouadaine\Desktop\PDFMerging\mergeEverything.py

print("Code starting")

import os
from os import listdir
from os.path import isfile, join 
from fpdf import FPDF
from PyPDF2 import PdfFileMerger, PdfFileReader, PdfFileWriter
import pymsgbox
#import Tkinter as tk
from PIL import Image
#import tkMessageBox

#21*29.7 minus margins
maxW = 190.0
maxH = 277.0

def resizePic(w, h):
    ratio = min(maxW/w, maxH/h)
    return (w*ratio, h*ratio)
	
def getExtension(fileName):
	return os.path.splitext(fileName)[1].lower()

'''#removes blank pages
def cleanPDF(sourcefile):
    infile = PdfFileReader(sourcefile, 'rb')
    output = PdfFileWriter()

    for i in xrange(infile.getNumPages()):
        p = infile.getPage(i)
        if i != 0: # getContents is None if  page is blank
            output.addPage(p)

    with open(sourcefile, 'wb') as f:
        output.write(f)

    return 1'''

finalDocumentName = "TOMEGERI.pdf"
tempo = "ZZZZFichierTemporaireAvecLesImages.pdf"
imageExtensions = [".png", ".jpg", ".jpeg"]
mypath = os.path.dirname(os.path.abspath(__file__)) # path to your image directory 

try:
    os.remove(finalDocumentName)
except OSError:
    pass

try:
    os.remove(tempo)
except OSError:
    pass

listOfFiles = set(listdir(mypath))
pdfFiles = [x for x in listOfFiles if getExtension(x) == ".pdf"]
imageFiles = [x for x in listOfFiles if getExtension(x) in imageExtensions]
ignoredFiles = [x for x in listOfFiles if x not in pdfFiles+imageFiles+["mergeEverything.exe","mergeEverything.py"]]
completion = 0

if imageFiles:
    pdf = FPDF()
    pdf.add_page()
    for each_file in imageFiles:
        turned = False
        im = Image.open(each_file)
        width, height = im.size
        if width > height:
            im = im.rotate(90, expand=True)
            im.save(each_file)
            width, height = im.size
            turned = True
        width, height = resizePic(width, height)
        pdf.image(each_file, w=width,h=height)
        if turned:
            im = Image.open(each_file)
            im = im.rotate(-90, expand=True)
            im.save(each_file)
        completion += 1
        print(str(completion*100/(len(pdfFiles)+len(imageFiles)+(0,1)[len(imageFiles) > 0])).split(".")[0]+" %")
    pdf.output(tempo, "F")
    #cleanPDF(tempo)
    tmp_pdfFiles = pdfFiles + [tempo]
else:
    tmp_pdfFiles = pdfFiles

merger = PdfFileMerger()
for each_file in tmp_pdfFiles:
    myPdf = PdfFileReader(each_file, 'rb')
    if myPdf.isEncrypted:
        myPdf.decrypt('')
    merger.append(myPdf)
    completion += 1
    print(str(completion*100/(len(pdfFiles)+len(imageFiles)+(0,1)[len(imageFiles) > 0])).split(".")[0]+" %")

merger.write(finalDocumentName)
if imageFiles:
    os.remove(tempo)

pymsgbox.alert(("","ATTENTION ! 2 fichiers PDF attendus, mais "+str(len(pdfFiles))+" reçu"+("s","")[len(pdfFiles) < 2]+" !\n\n")[len(pdfFiles) != 2]+"Fichiers ajoutés au PDF final :\n"+"\n".join(pdfFiles)+"\n"+"\n".join(imageFiles)+("","\n\nFichiers ignorés :\n"+"\n".join(ignoredFiles))[len(ignoredFiles) != 0], "Terminé !")
#top = tk.Tk()
#top.wm_withdraw()
#tkMessageBox.showinfo("Terminé !", ("","ATTENTION ! 2 fichiers PDF attendus, mais "+str(len(pdfFiles))+" reçu"+("s","")[len(pdfFiles) < 2]+" !\n\n")[len(pdfFiles) != 2]+"Fichiers ajoutés au PDF final :\n"+"\n".join(pdfFiles)+"\n"+"\n".join(imageFiles)+("","\n\nFichiers ignorés :\n"+"\n".join(ignoredFiles))[len(ignoredFiles) != 0])
