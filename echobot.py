# -*- coding: UTF-8 -*-

from fbchat import log, Client
import json
from fbchat.models import *
from jeudupendu import JeuDuPendu
from wiki import Wiki

data = {}

# Subclass fbchat.Client and override required methods
class EchoBot(Client):
    global data

    def getInstruction(self, message) :
        """ Récupération des infos nécessaires si le message est une commande"""
        res = {"bot": False, "module": None, "value": None, "message": str(message), "argument": None}
        liste_module = ["pendu", "wiki", "wikifull", "wikilang"]
        split = message.split(' ')
        if len(split) >= 2 :
            if split[0].lower() == "rojo" and split[1].lower() in liste_module :
                res["bot"] = True
                res["module"] = split[1].lower()
                if len(split) > 2 :
                    res["value"] = ' '.join(split[2:])
                    if len(split) > 3 :
                        ar = split[2]
                        if len(ar) > 1 and ar[0] == '-' :
                            res["argument"] = ar[1:]
                            res["value"] = ' '.join(split[3:])
        return res

    def duringBot(self, d, thread_id, author_id, message) :
        """ Vérifie si on est en cours d'une application du bot """
        penduModule = "pendu"
        if penduModule in d.keys() :
            if thread_id in d[penduModule].keys() :
                if author_id in d[penduModule][thread_id].keys() :
                    if "playing" in d[penduModule][thread_id][author_id].keys() and d[penduModule][thread_id][author_id]["playing"] :
                        return (True, {"module":penduModule, "bot":True, "value":message})
        return (False, None)

    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        """ Déclenché à chaque message envoyé ou reçu """
        if thread_type == ThreadType.USER :
            
            print(message_object.text)

            instruction = self.getInstruction(message_object.text)
            print(instruction)

            duringBot = self.duringBot(data, thread_id, author_id, message_object.text)
            if duringBot[0] :
                instruction = duringBot[1]

            if instruction["bot"] :
                if instruction["module"] not in data.keys() :
                    data[instruction["module"]] = {}
                
                if thread_id not in data[instruction["module"]].keys() :
                    data[instruction["module"]][thread_id] = {}
                
                if author_id not in data[instruction["module"]][thread_id].keys() :
                    data[instruction["module"]][thread_id][author_id] = {}
                
                # Wiki et wikifull
                if instruction["module"] == "wiki" or instruction["module"] == "wikifull" :
                    searchLang = None
                    if instruction["value"] and instruction["argument"] :
                        wiki = Wiki()
                        dict_langs = wiki.getLangs()
                        liste_ar = ["s"] + list(dict_langs.keys())
                        ar = instruction["argument"]
                        splitar = ar.split('-')
                        notinliste = 0
                        isSearch = False
                        nblang = 0
                        argmument_used = []
                        theLang = None
                        for el in splitar :
                            if not el in liste_ar or el in argmument_used :
                                notinliste += 1
                            if el in dict_langs.keys() :
                                if nblang > 0 :
                                    notinliste += 1
                                else :
                                    nblang += 1
                                    argmument_used.append(el)
                                    theLang = el
                            if el == 's' :
                                argmument_used.append(el)
                                isSearch = True
                        if notinliste > 0 :
                            txt = "Mauvaise commande. Vérifie au niveau du : -" + '-'.join(splitar) + chr(10)
                            txt += "Pour plus d'infos sur la fonctionnalité de ce bot, tape :" + chr(10)
                            txt += "Rojo wiki" 
                            self.send(Message(text=txt), thread_id=thread_id, thread_type=thread_type)
                        else :
                            if isSearch :
                                liste_search = wiki.getListeSearch(instruction["value"], theLang, 40)
                                txt = wiki.getTextSearch(liste_search[0], 40, lang=theLang)
                                self.send(Message(text=txt), thread_id=thread_id, thread_type=thread_type)
                            elif theLang and not isSearch :
                                searchLang = theLang

                    if (instruction["value"] and not instruction["argument"]) or searchLang :
                        self.send(Message(text="Recherche en cours..."), thread_id=thread_id, thread_type=thread_type)
                        dataAuthor = {"search": instruction["value"], "page": None}
                        load = False
                        if instruction["module"] == "wikifull" :
                            if "search" in data[instruction["module"]][thread_id][author_id].keys() :
                                dataS = data[instruction["module"]][thread_id][author_id]["search"]
                                if dataS != None and dataS.lower() == instruction["value"].lower() :
                                    page = data[instruction["module"]][thread_id][author_id]["page"]
                                    load = True
                        if instruction["module"] == "wiki" or not load :
                            wiki = Wiki()
                            page = wiki.getPage(instruction["value"], searchLang)
                        dataAuthor["page"] = page
                        data[instruction["module"]][thread_id][author_id] = dataAuthor

                        if page["page"] :
                            if instruction["module"] == "wiki" :
                                summary = page["page"]["summary"]
                                self.send(Message(text=summary), thread_id=thread_id, thread_type=thread_type)
                                textFull = wiki.getTextFull(instruction["value"], searchLang)
                                self.send(Message(text=textFull), thread_id=thread_id, thread_type=thread_type)
                                textSearchInfo = wiki.getTextSearchInfo(instruction["value"], searchLang)
                                self.send(Message(text=textSearchInfo), thread_id=thread_id, thread_type=thread_type)
                            else :
                                liste = wiki.getListeContent()
                                for c in liste :
                                    self.send(Message(text=c), thread_id=thread_id, thread_type=thread_type)
                                self.send(Message(text="Fin recherche"), thread_id=thread_id, thread_type=thread_type)
                        else :
                            print(page)
                            if page["ambiguous"] :
                                listeAmb = wiki.getTextListeAmbiguous(page["ambiguous_list"], instruction["value"], instruction["module"].lower(), lang=searchLang)
                                self.send(Message(text=listeAmb), thread_id=thread_id, thread_type=thread_type)
                            elif page["error"] :
                                txtErr = "Désolé mais ta recherche n'a eu aucun résultat :("
                                self.send(Message(text=txtErr), thread_id=thread_id, thread_type=thread_type)
                                liste_search = wiki.getListeSearch(instruction["value"], searchLang, 40)
                                txt = wiki.getTextSearch(liste_search[0], 40, lang=searchLang)
                                self.send(Message(text=txt), thread_id=thread_id, thread_type=thread_type)

                    
                    elif not instruction["value"] :
                        wiki = Wiki()
                        txt = wiki.getTextInfo()
                        self.send(Message(text=txt), thread_id=thread_id, thread_type=thread_type)

                # Wikilang
                elif instruction["module"] == "wikilang" and instruction["value"] == None and instruction["argument"] == None :
                    wiki = Wiki()
                    txt = wiki.getTextLangs()
                    self.send(Message(text=txt), thread_id=thread_id, thread_type=thread_type)

                # Jeu du pendu
                elif instruction["module"] == "pendu" :
                    if data[instruction["module"]][thread_id][author_id] == {} :
                        data[instruction["module"]][thread_id][author_id]["myself"] = author_id == self.uid
                        data[instruction["module"]][thread_id][author_id]["playing"] = False
                        data[instruction["module"]][thread_id][author_id]["word_to_find"] = ''
                        data[instruction["module"]][thread_id][author_id]["work_found"] = ''
                        data[instruction["module"]][thread_id][author_id]["letters_played"] = ''
                        data[instruction["module"]][thread_id][author_id]["nb_try"] = 6
                        
                    # self.markAsDelivered(thread_id, message_object.uid)
                    # self.markAsRead(thread_id)
                    pendu = JeuDuPendu()
                    pendu.setData(data[instruction["module"]][thread_id][author_id])
                    pendu.setMessage(message_object.text.lower())
                    if pendu.thisIsNotABot() or not data[instruction["module"]][thread_id][author_id]["myself"] :
                        res = pendu.answer()
                        data[instruction["module"]][thread_id][author_id] = res['data']
                        message_answer = res['answer']

                        self.send(Message(text=message_answer), thread_id=thread_id, thread_type=thread_type)


cookies = {}
try:
    # Load the session cookies
    with open('session.json', 'r') as f:
        cookies = json.load(f)
except:
    # If it fails, never mind, we'll just login again
    pass

username = '0342873991'
password = 'rjvls01234!'
try :
    client = EchoBot(username, password, session_cookies=cookies, max_tries=20)

    # Save the session again
    with open('session.json', 'w') as f:
        json.dump(client.getSession(), f)
except AttributeError :
    pass


client.listen()
client.logout()