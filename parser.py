# -*- coding: utf-8 -*-
'''
Created on 18/10/2018, tested for Python 2.7
Update on 18/10/2018  (mixed sn-grams supported and Spacy dependency parser)
@authors: Juan-Pablo Posadas-Durán
Class for obtaining dependency trees using Spacy parser output.
Prerequisites: download and install Spacy NLP tool (https://spacy.io/), 
English model en_core_web_sm (https://spacy.io/models/en#en_core_web_sm) and
Spanish model es_core_news_md (https://spacy.io/models/es#es_core_news_md)
Ensure not to use input symbols that are not UTF-8.
Usage: 
1)For English texts
    $python parser.py input en
2)For Spanish texts
    $python parser.py input es

'''
import warnings
#Detected warnings caused by the update of numpy v1.15
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")
import sys
import codecs
import spacy
import textacy
import en_core_web_sm
import es_core_news_md

def normalization(text):
    prep_1=textacy.preprocess.fix_bad_unicode(text, normalization='NFC')
    prep_1=textacy.preprocess.normalize_whitespace(prep_1) 
    prep_1=textacy.preprocess.preprocess_text(prep_1, no_contractions=True, no_accents=True)                      
    return prep_1
def sentence_segmenter(text,language):
    aux=[]#variable that contains the sentences    
    if language=="en":
        nlp = en_core_web_sm.load()    
    else:
        nlp = es_core_news_md.load()    
    doc = nlp(text)    
    for sent in doc.sents:        
        aux.append(sent.text)       
        #print sent.text 
    return aux,nlp


def dependency_parser(aux,input_file,nlp):    
    output_file = input_file
    output_file = output_file.replace(".txt",".parse")
    #id=1
    try:
        #**Read the input file and identify the format (includes POS tags or not)
        outf=codecs.open(output_file,'w',encoding='utf-8',errors='ignore')                        
    except IOError as e:
        print input_file + "I/O error({0}): {1}".format(e.errno, e.strerror)
        exit(1)    
    for sent in aux:                        
            #print "Processing sentence "+str(id)
            #id+=1
        ln=""
        sent = textacy.preprocess.remove_punct(sent)
        sent = sent.replace("\n"," ")
        sent = sent.lower() 
        sent = textacy.preprocess.normalize_whitespace(sent)       
        if len(sent)>1:
            doc = nlp(sent)
            for token in doc:
                if token.lemma_=="-PRON-":
                    ln+=token.text+"/"+token.text+"/"+token.pos_+" "
                else:
                    ln+=token.text+"/"+token.lemma_+"/"+token.pos_+" "
            ln=ln.rstrip()
            ln+="\n\n"
            xx=""
            for token in doc:
                if(token.dep_.lower()=="root"):
                    xx+=token.dep_.lower()+"(ROOT-0, "+token.head.text+"-"+str(token.head.i+1)+")\n"
                else:
                    xx+=token.dep_.lower()+"("+token.head.text+"-"+str(token.head.i+1)+", "+token.text+"-"+str(token.i+1)+")\n"
            #xx = textacy.preprocess.normalize_whitespace(aux)          
            xx+="\n"
            outf.write(ln+xx)      
    outf.flush()
    outf.close()

        
############### MAIN ################################
if __name__ == '__main__':
    #How to use:
    #python parser.py input [en,es]    
    
    encod = 'utf-8'   #'utf-8' or other encoding like '1252'    
    #print sys.argv
    if len(sys.argv) != 3:
        print "Usage with ecxactly two parameters:"
        print "python parser.py input [en,es]"
        exit(1)
            
    input_file      = sys.argv[1]
    language        = sys.argv[2]    
    text=""                                                                                                       
    try:
        #**Read the input file and identify the format (includes POS tags or not)
        f1 = codecs.open (input_file,  "rU", encoding = encod, errors='ignore')
        text="".join(f1.readlines())                
        f1.close()
        
    except IOError as e:
        print input_file + "I/O error({0}): {1}".format(e.errno, e.strerror)
        exit(1)
    text = normalization(text) 
    aux,nlp = sentence_segmenter(text,language)    
    dependency_parser(aux,input_file,nlp)
    print "Done."
    
    