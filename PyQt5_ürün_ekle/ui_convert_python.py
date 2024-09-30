from PyQt5 import uic

with open("Urun_Ekle.py","w",encoding="utf-8") as fout:
    uic.compileUi("urun_ekle.ui", fout)
    
    #bu sayfada yazılan kodlar urun_ekle.ui sayfasını kodlara cevırmek ıcın yazıldı
    