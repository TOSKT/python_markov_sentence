"""
MIT License

Copyright (c) 2018 TOSKT

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""
from janome.tokenizer import Tokenizer
import re
import random
import tkinter as tk
import tkinter.filedialog as tf

sentence = ''
word_txt = None
markov_dic = None
menu = None
lb = None
def parse(new_text):
    t = Tokenizer()
    words = t.tokenize(new_text)
    result = []
    for word in words:
        result.append(word.surface)
    return(result)
def dic():
    global markov_dic,word_txt,menu
    with open(menu,"r",encoding = 'utf_8') as o:
        new_txt = o.read()
    new_txt = re.sub("\n","",new_txt)
    word_txt = parse(new_txt)
    markov_dic = {}
    p1 = ''
    p2 = ''
    p3 = ''
    for word in word_txt:
        if  p1 and p2 and p3:
            if (p1,p2,p3) not in markov_dic:
                markov_dic[(p1,p2,p3)] = []
            markov_dic[(p1,p2,p3)].append(word)
        p1,p2,p3 = p2,p3,word
def make():
    global sentence,markov_dic
    sentence = ''
    count = 0
    p1,p2,p3 = random.choice(list(markov_dic.keys()))
    while count < 50:
        if ((p1,p2,p3) in markov_dic) == True:
            puls = random.choice(markov_dic[(p1,p2,p3)])
            sentence += puls
        p1,p2,p3 = p2,p3,puls
        count += 1
    sentence = re.sub('^. + ?。','',sentence)
    sentence = re.sub('^. + ?？','',sentence)
    if re.search('.+。',sentence):
        sentence = re.search('.+。',sentence).group()
    sentence = re.sub('」','',sentence)
    sentence = re.sub('「','',sentence)
    sentence = re.sub(' ','',sentence)
    
def prepare():
    global sentence
    sentence = sentence.split('。')
    if '' in sentence:
        sentence.remove('')
    prepare = []
    for str in sentence:
        str = str +'。'
        if str =='。':
            break
        prepare.append(str)
    prepare = set(prepare)
    sentence = ''.join(prepare)

def push():
    global sentence,lb,word_txt,markov_dic
    sentence = None
    word_txt = None
    markov_dic = None
    lb.delete(0,1)
    dic()
    make()
    prepare()
    lb.insert(tk.END,sentence)

def save():
    global sentence
    new_sentence = ''
    new_sentence += sentence+'\n'
    with open('new_sentence.txt','a',encoding = 'utf_8') as a:
        a.writelines(new_sentence)

def menu_open():
    global menu,lb
    menu = tf.askopenfilename(
        title='開くファイルの指定')
    lb.delete(0,1)
    lb.insert(tk.END,'pushボタンで文章生成を行います')

root = tk.Tk()
root.geometry('1500x600')
root.title('make a sentence')
font = ('メイリオ',14)


lb = tk.Listbox(root,
width = 100,
height = 20,
font = font
)
lb.insert(tk.END,'ファイル→openからテキストを選んでください。')

sb2 = tk.Scrollbar(root,
orient = tk.HORIZONTAL,
command = lb.xview
)

lb.configure(xscrollcommand = sb2.set)

lb.grid(row = 0,column = 0)
sb2.grid(row = 1,column = 0,sticky = tk.EW)

menubar = tk.Menu(root)
root.config(menu = menubar)
filemenu = tk.Menu(menubar)
menubar.add_cascade(label='ファイル',menu=filemenu)
filemenu.add_command(label='open',command=menu_open)

button = tk.Button(
    width = 15,
    text = 'push',
    command = push)
button.place(x=1350,y=100)

button2 = tk.Button(
    width = 15,
    text = 'save',
    command = save)
button2.place(x=1350,y=200)

root.mainloop()