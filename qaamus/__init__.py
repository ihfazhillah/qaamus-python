#coding:utf-8
import urllib2
from bs4 import BeautifulSoup as Bs
import re


opener = urllib2.build_opener()
opener.addheader = [('User-agent','Mozilla/4.0')]

class Qaamus:
    def __init__(self, kata):
        self.asli = kata
        kata = re.split(" ", kata)
        if kata :
            self.kata = "+".join(kata)
        else:
            self.kata = kata[0]
    def openHtml(self, url="http://www.qaamus.com/indonesia-arab/"):
        self.url = url
        htmltext =opener.open(url+self.kata)
        return Bs(htmltext)
    def cariArti(self, soup):
        #pencarian hasil utama
        hasil = soup.select('div.lateef2')[0].text
        return hasil
    def cariSecondary(self, soup):
        #pencarian untuk arti yang berkaitan
        if not soup.find(text=" (0 hasil)"):
            hasil_berhub_indo = soup.select('td a')
            hasil_berhub_arab  = soup.select('td.lateef')
            hasil_indo = [x.text for x in hasil_berhub_indo]
            hasil_arab = [x.text for x in hasil_berhub_arab]
            hasil = []
            for x in range(len(hasil_arab)):
                data = hasil_indo[x] + " : " + hasil_arab[x]
                hasil.append(data)
            return "\n".join(hasil)
        else:
            return None
    def ifPaged(self, soup):
        #cek paged apa enggak
            if not soup.find("ul", attrs={"class":"pagination"}).findNext(
            "li"
            ):
                return False
            else:
                return True
    def getUrlsPages(self, soup):
        #mencari url dulu, kalau ada pagination
        if self.ifPaged(soup):
            index = soup.find("ul", attrs={"class":"pagination"}).text
            index = re.split(" ",index)
            index = [int(x) for x in index if re.match("\d+", x)]
            index = index[-1]
            urls = []
            for x in range(index):
                x = x+1
                urls.append(self.url+self.kata+"&p="+str(x))
            return urls
        else:
            return None
    def artiSecondaryPages(self, soup):
        #ini untuk mencari arti dari semua yang berkaitan di halaman halam berikutnya
        try:
            hasil = []
            for x in self.getUrlsPages(soup)[1:]:
                soup2 = self.openHtml(x)
                hasil.append(self.cariSecondary(soup2))
                return "\n".join(hasil)
        except TypeError:
            pass
    def cari(self, soup):
        #pencarian utama
        kata = self.asli

        utama = kata + " = " + self.cariArti(soup)
        secondAwal = self.cariSecondary(soup)
        secondPages = self.artiSecondaryPages(soup)
        if secondAwal != None and secondPages!=None:
            
            outp = [utama,"\nHasil yang berkaitan\n" ,secondAwal, secondPages]
        elif secondAwal != None and secondPages == None:
            outp = [utama,"\nHasil yang berkaitan\n" ,secondAwal]
        else:
            outp = [utama]
        return "\n".join(outp)
        # return  "\n".join([utama, self.cariSecondary(soup), self.cariArti(soup)])
        # return outp
#contoh
if __name__ == "__main__":
    cari = Qaamus("gigit")
    soup = cari.openHtml()
    print cari.cari(soup)
