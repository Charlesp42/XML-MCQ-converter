#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from lxml import etree # pip install lxml
import random
import re # pour les questions type "cloze"


tree = etree.parse("input2.xml")
root = tree.getroot()

melanger_reponses=False




######################## type question ########################
Type=[]
for question in tree.xpath("/quiz/question"):
    Type.append(question.get("type"))
del (Type[0]) # retrait du 1er car titre du QCM


######################## titre question ########################
Titre=[]
for question in tree.xpath("/quiz/question/name/text"):
    Titre.append(question.text)



######################## texte question ########################
Questions=[]
for question in tree.xpath("/quiz/question/questiontext/text"):
    Questions.append(question.text)



############# texte reponses et image question ####################
Liste_reponses=[]
Liste_reponses_sugg=[' ']*(len(Questions)+1)
numqst=0
Image_questions=[' ']*(len(Questions)+1)
for qst in root.findall("./question"):
#    print(qst.attrib)
    Liste_rep_tmp=[]                                # type multichoice
    for rep in qst.findall("./answer/text"):        # type multichoice
#        print(rep.text)
        Liste_rep_tmp.append(rep.text)
    Liste_reponses.append(Liste_rep_tmp)
    
    Liste_rep_tmp=[]                              # type matching
    for rep in qst.findall("./subquestion/text"):           # sous question
        Liste_rep_tmp.append(rep.text)
    if Liste_reponses[numqst] == []:
        Liste_reponses[numqst]=Liste_rep_tmp

    Liste_rep_tmp=[]
    for rep in qst.findall("./subquestion/answer/text"):    # suggestions
        Liste_rep_tmp.append(rep.text)
        random.shuffle(Liste_rep_tmp)   # on mélange les réponses
        Liste_reponses_sugg[numqst]=Liste_rep_tmp
    
    for img in qst.findall("./image_base64/text"):          # image question
        Image_questions[numqst]=img.text
    numqst=numqst+1
    
del (Liste_reponses[0]) # retrait du 1er car titre du QCM
del (Image_questions[0]) # retrait du 1er car titre du QCM
del (Liste_reponses_sugg[0]) # retrait du 1er car titre du QCM
    
######################## image questions ########################


# for img in tree.xpath("/quiz/question/image_base64/text"):
# #    print('---------- question '+str(i)+' ----------')
# #    print(question.text)
#     image_questions.append(img.text)
# #    for answer in tree.xpath("/quiz/question/answer/text"):
# #        print('reponse:')
# #        print(answer.text)






for qst in range(len(Questions)):
    if Type[qst] == 'cloze':
        string=Questions[qst]
        split_string = re.split(r'[{}]', string)
        nb_trous=string.count(':MULTICHOICE:')+string.count(':SHORTANSWER:')
        nb_txt=len(split_string)-nb_trous
        split_rep=['']*nb_trous
        
        i=0
        for partie_string in range(len(split_string)):
            if split_string[partie_string].startswith(":MULTICHOICE:"):
               # split_string[partie_string] = re.split(r'[%]', string[partie_string])
                split_repi = re.split(r'[%]', split_string[partie_string])
                del (split_repi[0]) # retire texte multichoice
                split_repi = split_repi[1::2] # retire indication du bareme (index pair)
                split_repi = {re.sub('[#~]', '', split_repi[i]) for i in range(len(split_repi))}
                repi='/'.join(split_repi)
                split_rep[i]='('+repi+')'
                split_string[partie_string]=split_rep[i]
                i=i+1
            if split_string[partie_string].startswith(":SHORTANSWER:"):
                split_string[partie_string]='..........................'
        
        string=' '.join(split_string)
        
        Questions[qst]=string



if melanger_reponses:
    for qst in range(len(Questions)):
        if Type[qst] == 'multichoice':
            random.shuffle(Liste_reponses[qst])   # on mélange les réponses





"""  écriture du fichier de sortie  """
outputfile=open('output.html','w+')

outputfile.write('<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8"><title>QCM</title></head><body>')


for qst in range(len(Questions)):
    # print(qst)
    outputfile.write('<h2>Question '+str(qst+1)+'</h2>')
    
    outputfile.write('<h2>'+Questions[qst]+'</h2>')

    if Image_questions[qst] != ' ':
        outputfile.write('<img src="data:image/png;base64,'+ Image_questions[qst]+'" alt="erreur de chargement de l\'image"/></br>')

    if Type[qst] == 'multichoice':
        for rep in Liste_reponses[qst]:
            outputfile.write('☐ '+rep+'<br/>')

    if Type[qst] == 'numerical':
        outputfile.write('</br> réponse (nombre): ....................')
    
    if Type[qst] == 'matching':
        for repnum in range(len(Liste_reponses[qst])):
            outputfile.write(Liste_reponses[qst][repnum]+'• &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; •' + Liste_reponses_sugg[qst][repnum]+' <br/><br/>')
    
    
    outputfile.write('<br/>')


outputfile.write('</body></html>')

outputfile.close()




























