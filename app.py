from __future__ import print_function, unicode_literals
import requests
import random
from time import sleep
from bs4 import BeautifulSoup
from loguru import logger
from pyfiglet import Figlet
from PyInquirer import prompt, print_json

class KaskusBot:
    def __init__(self,answer):
        self.session = requests.Session()
        self.rooturl = "https://m.kaskus.co.id/"
        self.message = self.get_txt('kata.txt')
        self.links = []

        self.login(answer['username'],answer['password'])
        self.get_thread(answer['kategori'],int(answer['berapahalaman?']))
        self.comment_bot()
    
    def login(self,username,password):
        try:
            baseurl = "https://m.kaskus.co.id/user/login"
            data = {
                "identifier":username,
                "password":password,
                "url":"/user/login"
            }
            self.session.post(baseurl, data=data)
            r = self.session.get('https://m.kaskus.co.id/user/editprofile')
            
            soup = BeautifulSoup(r.content,'lxml')
            usr = soup.findAll('input')
            logger.success('Login berhasil (%s)'%(usr[2]['value']))
        except:
            logger.warning('Login Gagal!')
            exit
        

    def get_txt(self,txtfiles):
        raw_lines = []
        lines = []

        f = open(txtfiles, "r")
        raw_lines = f.readlines()
        f.close()
        
        for line in raw_lines:
            lines.append(line.strip("\n"))

        return lines

    def get_thread(self, namecategory, howmanypages=1):
        """
        Get All Links from Category
        
        example namecategory:
        /21/the-lounge/
        """
        
        for page in range(howmanypages):
            page += 1
            baseurl = "https://m.kaskus.co.id/forum"+namecategory
            url = baseurl+str(page)
            r = self.session.get(url)

            soup = BeautifulSoup(r.content,'lxml')
            threads = soup.findAll('div',{'class':'Bdb(BdbThreadItem) nightmode_Bdbc(#000) Bgc(#fff) nightmode_Bgc(#171717) Pt(5px)'})
            for thread in threads:
                link = thread.findAll('a',class_="C(#484848) nightmode_C(#dcdcdc)")
                if '<i class="fas fa-thumbtack C(#ed1c24) nightmode_C(#faa517) Mend(5px)"></i>' in str(link[1]):
                    # Skip Pinned Post
                    continue
                rawlink = link[1]['href']
                linkprocessed = rawlink.split('/')[2]
                self.links.append(linkprocessed)
        logger.success('Sukses mengambil thread! Terdapat '+str(len(self.links))+' thread yang bisa di komen')
    
    def comment_bot(self,delay=30):
        """
        Commenting Automatically on each thread
        """
        terkomen = 0
        for link in self.links:
            baseurl = "https://m.kaskus.co.id/post_reply/"+link
            r = self.session.get(baseurl)
            soup = BeautifulSoup(r.content,'lxml')
            try:
                token = soup.find('input',{'name':'psecuritytoken'})
                token = token['value']

                data = {
                    "title": "",
                    "message": random.choice(self.message),
                    "forumimg": "",
                    "psecuritytoken": token,
                    "parent_post": "",
                    "order": 1,
                    "sbutton": "Post"
                }
            except Exception as e:
                logger.warning('Tidak bisa memposting')
                continue 
            
            try:
                self.session.post(baseurl, data=data)
                logger.success('[%s] [%s] Berhasil Mengkomen!'%(terkomen,link))
                terkomen += 1
                sleep(delay)
            except KeyboardInterrupt:
                exit
            

if __name__ == "__main__":
    f = Figlet(font='standard')
    print(f.renderText('Kaskus BOT'))

    print('Selamat datang di Kaskus Bot Auto Post versi beta! \n Purely written by Raihan Yudo Saputra \n')
    print('\t[HANYA UNTUK PEMBELAJARAN]\n')

    questions = [
        {
        'type': 'input',
        'name': 'username',
        'message': 'Username Kaskus Kamu:',
    },
        {
        'type': 'password',
        'name': 'password',
        'message': 'Password Kaskus Kamu:',
    },
        {
        'type': 'input',
        'name': 'kategori',
        'message': 'Kategori (contoh: /26/anime--manga-haven/ ) :',
    },
        {
        'type': 'input',
        'name': 'berapahalaman?',
        'message': 'Berapa banyak halaman?:',
    }]

    answers = prompt(questions)
    KaskusBot(answers)