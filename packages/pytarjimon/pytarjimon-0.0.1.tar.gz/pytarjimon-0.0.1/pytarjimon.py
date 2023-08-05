from googletrans import Translator
t = Translator()
def tarjima(text, language):
    try:
        return t.translate(f"{text}", dest=f"{language}").text
    except Exception as ex:
        return ex