from django.shortcuts import render

from django.http import HttpResponse

from .forms import urlform

import bs4 as bs
import urllib.request
import re
import nltk
nltk.download('stopwords')
nltk.download('punkt')

def text_rank(per,text):
    stopwords = nltk.corpus.stopwords.words('english')
    sentence_list = nltk.sent_tokenize(text)


    nos=per*len(sentence_list)//100

    if nos<1:
        if len(sentence_list)!=0:
            summary='\n*'.join(sentence_list)
            return('*'+summary)
        else:
            return('')


    word_frequencies = {}
    for word in nltk.word_tokenize(text):
        if word not in stopwords:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1

        maximum_frequncy = max(word_frequencies.values())

        for word in word_frequencies.keys():
            word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)

        sentence_scores = {}

        for sent in sentence_list:
            for word in nltk.word_tokenize(sent.lower()):
                if word in word_frequencies.keys():

                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word]
                    else:
                        sentence_scores[sent]+= word_frequencies[word]
    import heapq
    summary=''
    summary_sentences = heapq.nlargest(nos, sentence_scores, key=sentence_scores.get)

    for i in sentence_list:
        if i in summary_sentences:
            summary+= '*'+i+'\n'
    return(summary)
# Create your models here.
def tsum(request):
    l=[]
    if request.method =="POST":
        form = urlform(request.POST)

        if form.is_valid():
            x=form.cleaned_data["url"]
            per=int(form.cleaned_data["percentage"])
            scraped_data = urllib.request.urlopen(x)
            article = scraped_data.read()
            soup = bs.BeautifulSoup(article,'html.parser')
            str=""
            str1=""
            l=soup.find('h1')
            a=l.text
            print(a)
            str1=str1+'\n'+a + '\n'
            l1=soup.find('p')
            
            str=''
            for i in l1.next_siblings:
                if i.name=='p':
                    str+=i.text
                elif i.name in ['h1','h2','h3']:
                    text = re.sub(r'\[[0-9]*\]', ' ', str)
                    ftext = re.sub(r'\s+', ' ', text)
                    ftext=ftext.strip()
                    str1=str1+text_rank(per,ftext)
                    
                    str=''
                    break

            for heading in soup.find_all(['h1', 'h2', 'h3']):
                h=heading.get_text()
                
                for elem in heading.next_siblings:
                    if elem.name and elem.name.startswith('h'):
                        
                        if str!='':
                            
                            str1=str1+'\n\n'+h + '\n\n'
                            text = re.sub(r'\[[0-9]*\]', ' ', str)
                            ftext = re.sub(r'\s+', ' ', text)
                            ftext=ftext.strip()
                            str1=str1+text_rank(per,ftext)
                            break
                    if elem.name == 'p':
                        
                        str+=elem.get_text()

                str=""
                l=str1.split("\n")
                
               
            

            

            

    form=urlform();
    return render (request, 'main.html',{'form': form,'summary':l})
