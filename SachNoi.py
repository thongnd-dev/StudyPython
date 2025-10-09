import  pyttsx3
from PyPDF2 import  PdfReader

with open("Microsoft_Visual_CSharp.pdf", "rb") as file:
    pdfreader = PdfReader(file)
    pages = len(pdfreader.pages)
    print(pages)
    page = pdfreader.pages[3]
    text = page.extract_text()

bot = pyttsx3.init()
voices = bot.getProperty('voices')
bot.setProperty('voice', voices[0].id)
bot.say(text)
bot.runAndWait()

file.close()