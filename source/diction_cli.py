# -*- coding: utf-8 -*-
"""
Created on Thu May 11 14:01:39 2017

@author: ASEEM_YADAV
"""

import requests
import re
import inspect, os, sys
from tkinter import messagebox, StringVar, IntVar
import json
import pygubu
import tkinter as tk
from pygame import mixer
from PIL import Image, ImageTk
from itertools import count
import threading

valid = False

#### USE YOUR API KEYS HERE
app_id = 'a1822637'
app_key = '869ade38021aaeade351323e50583c6a'
headers = {'app_id': app_id, 'app_key': app_key}
cur_file = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
delim = "\\" if os.name == 'nt' else '/'
ui_path = cur_file + delim
DELAY = 80
DELAY2 = 20


##### METHODS FOR EVERY FUNCTIONALITY #####
class UI(tk.Label):
    def __init__(self, master):
        super(UI, self).__init__()
        self.build = pygubu.Builder()
        self.build.add_from_file(ui_path + '../UI/tk_gui_gif.ui')
        self.build.get_object('main_label',master)
        self.keyword = ""
        self.dict = self.build.get_object('dictionary')
        self.synon = self.build.get_object('synonyms')
        self.anton = self.build.get_object('antonyms')
        self.etymo = self.build.get_object('ety')
        self.pro = self.build.get_object('pro')
        self.progress = self.build.get_object('progress')
        self.label1 = self.build.get_object('key_label')
        self.label1.config(font=('Georgia', 13, 'bold'))
        self.dict.config(variable=rval)
        self.synon.config(variable=checkval1)
        self.anton.config(variable=checkval2)
        self.etymo.config(variable=checkval3)
        self.pro.config(variable=checkval4)
        self.build.connect_callbacks(self)
        self.mainwindow = self.build.get_object('main_label', master)

############CODE FOR RUNNING ANIMATED PROGRESS BAR###############
    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)
        self.loc = 0
        self.frames = []

        try:
            for i in count(1):
                self.frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass

        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100

        if len(self.frames) == 1:
            self.config(image=self.frames[0])
        else:
            self.next_frame()

    def unload(self):
        #self.config(image=None)
        self.frames = None
        #self.info.config(image=None)
        #self.info.lower(self.mainwindow)
        self.info.grid_remove()

    def next_frame(self):
        #print("print this multiple times.")
        if self.frames:
            self.loc += 1
            self.loc %= len(self.frames)
            self.info = tk.Label(text = '', width=200, borderwidth=1, relief="solid")
            #self.info.lower(self.mainwindow)
            self.info.place(relx=1.0, rely=1.0, x=-100, y=-170, anchor="se")
            self.info.config(image = self.frames[self.loc])
            #self.config(image=self.frames[self.loc])
            #self.place(relx=1.0, rely=1.0, x=-2, y=-2, anchor="se")
            self.after(self.delay, self.next_frame)

    
####################################################

    def etymology(self):
        print(self.response['results'][0]['lexicalEntries'][0]['entries'][0]['etymologies'][0])
        return self.response['results'][0]['lexicalEntries'][0]['entries'][0]['etymologies'][0]

    def meaning(self):
        return self.response['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['definitions'][0]

    def usage(self):
        return self.response['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['examples'][0]['text']

    def pronounce(self):
        return self.response['results'][0]['lexicalEntries'][0]['pronunciations'][0]['phoneticSpelling']

    def call_api(self, path, media = False):
        self.page = requests.get(path,
                            headers=headers,
                            proxies={"http": "http://192.168.219.74:8080",},
                            stream = media
                            )

    def onGetValue(self):
        if self.p1.is_alive():
            self.after(DELAY, self.onGetValue)
            return
        else:
            self.progress.stop()
            #self.info.lower(self.mainwindow)
            #self.unload()
            self.print_listbox()

    def synonyms(self):
        visit_synon = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/en/'+self.keyword.lower()+'/synonyms'
        self.page_synon = self.page
        self.dump = json.dumps(self.page_synon.json())
        self.response_s = json.loads(self.dump)
        item = []
        itemlist = self.response_s['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['subsenses'][0]['synonyms']
        for i in range(len(itemlist)):
            print(itemlist[i]['text'])
            item.append(itemlist[i]['text'])
        return item

    def antonyms(self):
        visit_anton = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/en/'+self.keyword.lower()+'/antonyms'
        self.page_anton = self.call_api(visit_anton)
        self.page_anton = self.page
        self.dump = json.dumps(self.page_anton.json())
        self.response_a = json.loads(self.dump)
        item = []
        itemlist = self.response_a['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['antonyms']
        for i in range(len(itemlist)):
            print(itemlist[i]['text'])
            item.append(itemlist[i]['text'])
        return item

    def play_audio(self):
        ## SHOW ERROR IF WORD IS NOT SEARCHED
        if not self.keyword:
            messagebox.showinfo('Message', 'Please! Enter a keyword to search \nbefore listening to audio.')
        else:
            ## path to audio file
            path = self.response['results'][0]['lexicalEntries'][0]['pronunciations'][0]['audioFile']
            local_filename = path.split('/')[-1]
            if os.path.exists(local_filename):
                pass
            else:
                r = requests.get(path, stream=True)
                with open(local_filename, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=1024):
                        if chunk: # filter out keep-alive new chunks
                            f.write(chunk)
            ## PLAY THE DOWNLOADED AUDIO
            mixer.init()
            mixer.music.load(cur_file+delim+local_filename)
            mixer.music.play()

    def null_on_focus(self):
        self.search_field = self.build.get_object('search_field')
        self.search_field.focus_set()
        self.search_field.delete(0, tk.END)

    def validate(self, keyword):
        kw = re.search('\d', keyword)
        valid = True
        return kw

    def search_keyword(self):
        self.keyword = self.search_field.get()
        print(self.keyword)
        try:
            if self.validate(self.keyword).group(0):
                messagebox.showinfo('Message', 'You entered a digit!!\nPlease re-enter (only Alphabets)')
                self.parse_json(True)
                self.print_listbox(True)
        except:
            pass

        self.parse_json()

    def parse_json(self, not_word=False):
        visit = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/en/'+self.keyword.lower()
        print(visit)
        ## After user clicks OK, then load this GIF
        # self.load('../UI/hProgress.gif')

        self.p1 = threading.Thread(target=self.call_api, args=(visit,))
        self.p1.start()
        self.progress.start(DELAY2)
        self.after(DELAY, self.onGetValue)

    def print_listbox(self, not_word=False):

        print(self.p1.is_alive())
        print("Response Code: "+str(self.page.status_code))
        print(self.page.content)
        if not not_word and self.page.status_code != 404:
            self.dump = json.dumps(self.page.json())
            self.response = json.loads(self.dump)
        elif self.page.status_code == 404:
                self.print_listbox(True)

        #### PRINT DATA ONTO LISTBOX ####

        label_keyword = self.build.get_object('label_keyword')
        label_keyword.config(text = self.keyword.upper(), font=('courier', 15, 'bold'))
        content = self.build.get_object('content')
        ## GET SCROLLBAR
        scrollb = self.build.get_object('Scrollbar_1')
        scrollb.config(command=content.yview)
        content.configure(yscrollcommand=scrollb.set, font=('Georgia', 10))
        content.tag_configure("B_I", font = ('Helvetica', 11, 'italic'))
        content.config(state='normal')
        if not_word or "404" in self.page.text:
            content.delete(1.0, tk.END)
            content.insert("end", "No entry available for '{}'\n".format(self.keyword))
        else:
            try:
                content.delete(1.0, tk.END)
                content.insert("end", "MEANING: ", "B_I")
                meaning = self.meaning()
                content.insert("end", meaning)
            except IndexError as e:
                print("Exception occurred: "+str(sys.exc_info()[0]))
        content.insert("end", "\nUSAGE: ", "B_I")
        try:
            use = self.usage()
            content.insert("end", use)
        except:
            content.insert("end", 'N/A')
            pass

        if checkval3.get():
            content.insert("end", "\nETYMOLOGY: ", "B_I")
            try:
                ety = self.etymology()
                content.insert("end", ety)
            except:
                content.insert("end", 'N/A')
                pass
        if checkval4.get():
            content.insert("end", "\nPRONOUNCIATION: ", "B_I")
            try:
                pron = self.pronounce()
                content.insert("end", pron)
            except:
                content.insert("end", 'N/A')
                pass
        if checkval1.get():
            content.insert("end", "\nSYNONYMS: ", "B_I")
            try:
                syn = self.synonyms()
                if len(syn) == 1:
                    content.insert("end", val[0])
                else:
                    content.insert("end", "\n")
                    for i,val in enumerate(syn):
                        content.insert("end", str(i+1) + ": " + format(val) + "\n")
            except:
                content.insert("end", 'N/A')
                pass
        if checkval2.get():
            content.insert("end", "\nANTONYMS: ", "B_I")
            try:
                ant = self.antonyms()
                if len(ant) == 1:
                    content.insert("end", "1: "+ant[0])
                else:
                    content.insert("end", "\n")
                    for i,val in enumerate(ant):
                        content.insert("end", str(i+1) + ": " + format(val) + "\n")
            except:
                content.insert("end", 'N/A')
                pass
        content.config(state='disabled')
    def close_on_cancel(self):
        global root
        root.quit()
        root.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    root.resizable(False, False)
    rval = StringVar()
    rval.set('dc')
    checkval1 = IntVar()
    checkval2 = IntVar()
    checkval3 = IntVar()
    checkval4 = IntVar()
    app = UI(root)
    root.mainloop()

