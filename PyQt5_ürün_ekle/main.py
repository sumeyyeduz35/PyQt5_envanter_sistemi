import sys
from PyQt5 import QtWidgets  #Qtwidgets kutuphanesı formumuzda bulunan tum widgetlerın classıdır
from PyQt5.QtWidgets import *
from Urun_Ekle import *

uygulama = QApplication(sys.argv)
pencere = QMainWindow()
ui = Ui_MainWindow() #bu kod satırı ıle Ui_MainWindow icerisindeki widgetlere ulasırız
ui.setupUi(pencere)
pencere.show()#bu satır ile pencereyi çalıstırırız


#uygulamanın veritabanı kodları asagıdakı gıbı olacak

import sqlite3

baglanti = sqlite3.connect("urunler.db") #parantez icine veritabanimizin adini yazdik
islem = baglanti.cursor() #veritabaninda yapılacak olan islemin imlecidir
baglanti.commit() #veritabaninda yapmis oldugumuz degisiklikleri kaydeder

table = islem.execute("create table if not exists urun(urunKodu int, urunAdi text, birimFiyat int, stokMiktari int, urunAciklamasi text, marka text, kategori text)") #yapmis oldugumuz islemi veritabanına isleriz
#"create table if not exists" ıle verıtabanında olmayan bır tabloyu olustururuz. eger bu ıslemler bır tabloda varsa o tablo uzerınden devam eder
baglanti.commit()#veritabanına kaydetmiş olduk


def kayit_ekle():
    UrunKodu = int(ui.lneurunKodu.text())
    UrunAdi = ui.lneurunAdi.text()
    BirimFiyat = int(ui.lnebirimFiyati.text())
    StokMiktari = int(ui.lnestokMiktari.text())
    UrunAciklamasi = ui.lneurunAciklamasi.text()
    Marka = ui.cmbMarka.currentText()  #currenttext() kullanmamızın nedenı o esmada sectıgımız sey ıle ıslem yapmak ıstememız
    
    
    #hata olup olmadıgını gorebilmek için try-except kullandık
    
    try:
        ekle = "insert into urun(urunKodu, urunAdi, birimFiyat, stokMiktari, urunAciklamasi, marka) values(?,?,?,?,?,?)"
        islem.execute(ekle, (UrunKodu, UrunAdi, BirimFiyat, StokMiktari, UrunAciklamasi, Marka))

        baglanti.commit() #yapilan islemi veritaanina kayıt ettik
        kayit_listele() #bu komuttan sonra ekleme yapıldıgında liste ekrana eklenecek
        ui.statusbar.showMessage("Kayıt işlemi başarıyla gerçekleştirilmiştir.", 20000)  #statusbar ıle ekrana yazdırmak ıstedıgımız mesajı yazdırırız.
        
    except Exception as error: #Exception as error ile hatayı ekrana yazdırırız
        ui.statusbar.showMessage("Kayıt Oluşturulamadı." + str(error))
        

def kayit_listele():
    ui.tblListele.clear() #bu komut sayesinde onceki listeyi sileriz
    ui.tblListele.setHorizontalHeaderLabels(("Ürün Kodu", "Ürün Adi", "Birim Fiyatı", "Stok Miktarı","Ürün Açıklama", "Markası", "Kategori"))
    
    sorgu = "select * from urun"
    islem.execute(sorgu)
    
    for indexSatir, kayitNumarasi in enumerate(islem):
        for indexSutun, kayitSutun in enumerate(kayitNumarasi):
            ui.tblListele.setItem(indexSatir, indexSutun, QTableWidgetItem(str(kayitSutun)))  #bu satırdakı komutlar ıle yazdırırız
    

def kategoriye_gore_listele():
    listelenecek_kategori = ui.cmbKategoriListele.currentText()
    
    sorgu = "select * from urun where kategori = ?"
    islem.execute(sorgu, (listelenecek_kategori,)) #listelenecek kategoriyi yazdırmak icin virgul koymak zorundayız
    ui.tblListele.clear()
    for indexSatir, kayitNumarasi in enumerate(islem):
        for indexSutun, kayitSutun in enumerate(kayitNumarasi):
            ui.tblListele.setItem(indexSatir, indexSutun, QTableWidgetItem(str(kayitSutun)))  #bu satırdakı komutlar ıle yazdırırız
    

def kayit_sil():
    sil_mesaj = QMessageBox.question(pencere, "Silme Onayı", "Silmek İstediğinizden Emin Misiniz?",QMessageBox.Yes | QMessageBox.No)
    
    if sil_mesaj == QMessageBox.Yes:
        secilen_kayit = ui.tblListele.selectedItems()
        silinecek_kayit = secilen_kayit[0].text()
        
        sorgu = "delete from urun where urunKodu = ?"
        try:
            islem.execute(sorgu,(silinecek_kayit,))
            baglanti.commit()
            ui.statusbar.showMessage("Kayıt Başarıyla Silindi")
        except Exception as error:
            ui.statusbar.showMessage("Kayıt Silinirken Hata Çıktı === " +str(error))
            kayit_listele() #bu komuttan sonra sıldıgımızde listeleme ekranda olmaya devam edecektir
    
    else:
        ui.statusbar.showMessage("Silme İşlemi İptal Edildi")
        
        
def kayit_guncelle():
    guncelle_mesaj = QMessageBox.question(pencere, "Güncelleme Onayı", "Değişiklikler Kaydedilsin Mi?", QMessageBox.Yes | QMessageBox.No)
    
    if guncelle_mesaj == QMessageBox.Yes:
        try:
            UrunKodu = ui.lneurunKodu.text()
            UrunAdi = ui.lneurunAdi.text()
            BirimFiyati = ui.lnebirimFiyati.text()
            StokMiktari = ui.lnestokMiktari.text()
            UrunAciklama = ui.lneurunAciklamasi.text()
            Marka = ui.cmbMarka.currentText()
            Kategori = ui.cmbKategori.currentText()
            
            if UrunAdi == "" and BirimFiyati == "" and StokMiktari == "" and UrunAciklama == "" and Marka == "":
                islem.execute("update urun set kategori = ? where urunKodu = ?", (Kategori, UrunKodu))  #=bu komut satırında urun koduna gore kategorıyı degıstırebılırız
            
            elif UrunAdi == "" and BirimFiyati == "" and StokMiktari == "" and UrunAciklama == "" and Kategori == "":
                islem.execute("update urun set marka = ? where urunKodu = ?", (Marka, UrunKodu))  #=bu komut satırında urun koduna gore Marka degıstırebılırız
            
            elif UrunAdi == "" and BirimFiyati == "" and StokMiktari == "" and Marka == "" and Kategori == "":
                islem.execute("update urun set urunAciklamasi = ? where urunKodu = ?", (UrunAciklama, UrunKodu))  #=bu komut satırında urun koduna gore urun acıklamasını degıstırebılırız
            
            elif UrunAdi == "" and BirimFiyati == "" and UrunAciklama == "" and Marka == "" and Kategori == "":
                islem.execute("update urun set StokMiktari = ? where urunKodu = ?", (StokMiktari, UrunKodu))  #=bu komut satırında urun koduna gore stok miktarını degıstırebılırız
            
            elif UrunAdi == "" and StokMiktari == "" and UrunAciklama == "" and Marka == "" and Kategori == "":
                islem.execute("update urun set birimFiyat = ? where urunKodu = ?", (BirimFiyati, UrunKodu))  #=bu komut satırında urun koduna gore birim fiyatını degıstırebılırız
            
            elif BirimFiyati == "" and StokMiktari == "" and UrunAciklama == "" and Marka == "" and Kategori == "":
                islem.execute("update urun set urunAdi = ? where urunKodu = ?", (UrunAdi, UrunKodu))  #=bu komut satırında urun koduna gore urun adını degıstırebılırız
            
            
            else:
                islem.execute("update urun set urunAdi = ?, birimFiyat = ?, stokMiktari = ?, urunAciklamasi = ?, marka = ?, kategori = ? where urunKodu = ?", (UrunAdi, BirimFiyati, StokMiktari, UrunAciklama, Marka, Kategori, UrunKodu))
                #yukarıdakı komut satırında tum bılgılerı guncelleyebılırız
            baglanti.commit() #bu komut satırı ıle verı tabanına kaydederız
            kayit_listele() #ekrandaki listeyi yeniler
            ui.statusbar.showMessage("Kayıt Başarı İle Güncellendi")
            
        except Exception as error:
            ui.statusbar.showMessage("Kayıt Güncellemede Hata Çıktı === "+str(error))

    else:
        ui.statusbar.showMessage("Güncelleme İptal Edildi")

#butonlar
ui.btnEkleme.clicked.connect(kayit_ekle) #kayıt ekle butonuna bastıgımızda yukarıdakı fonksıyonu aktıf eder
ui.btnListeleme.clicked.connect(kayit_listele) #kayıtları listeleme butonuna basınca yukarıdakı fonksıyonu aktıf eder
ui.btnKategoriyeGoreListele.clicked.connect(kategoriye_gore_listele) #kategoriye göre listelemek için bu buton fonksiyonu aktif eder
ui.btnSilme.clicked.connect(kayit_sil) #kayıtları silmek için bu buton fonksıyonu aktıf eder
ui.btnGuncelle.clicked.connect(kayit_guncelle) #kayıtları guncellemek ıcın bu buton ıle guncelleme fonksıyonlarını aktıf ederız

sys.exit(uygulama.exec_()) #bu kod satırı ıle uygulamayı kapatabılırız.