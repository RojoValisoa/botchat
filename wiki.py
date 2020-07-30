import wikipedia

class Wiki :

    def __init__(self, key=None) :
        wikipedia.set_lang('fr')
        self.key = key
        self.page = None

    def getSummary(self, key=None) :
        find = None
        if key == None and self.key != None :
            self.key = key
            find = self.key
        elif key != None :
            find = key
        
        if find != None :
            return wikipedia.summary(find)
        else :
            return None

    def getContent(self, key=None) :
        find = None
        if key == None and self.key != None :
            self.key = key
            find = self.key
        elif key != None :
            find = key

        if find != None :
            page = wikipedia.page(find)
            return page.content
        else :
            return None

    def getPage(self, search_string, lang='fr'):
        '''Returns results from searching for search_string with wikipedia wrapper library. 
        Note: Makes a web request'''

        res = {}
        res["search_string"] = search_string
        res["ambiguous"] = False
        res["page"] = None
        res["ambiguous_list"] = []
        res["suggestion"] = None
        res["error"] = False

        if lang :
            wikipedia.set_lang(lang)

        try:
            page = wikipedia.page(search_string)
            page_data = {"url":page.url,
                        "title":page.title,
                        "content":page.content,
                        "summary":page.summary}
            res["page"] = page_data
            self.page = page
        
        except wikipedia.DisambiguationError as e:
            s = wikipedia.search(search_string, suggestion=True, results=40)
            res["ambiguous"] = True
            res["ambiguous_list"] = s[0]
            res["suggestion"] = s[1]
        except :
            res["error"] = True
        
        return res
        
    def getTextFull(self, search, lang='fr') :
        if lang == None or lang == 'fr' :
            arg = ''
        else :
            arg = '-' + lang + ' '
        txt = "Pour plus de détails sur ta recherche, tape :" + chr(10)
        txt += "Rojo wikifull " + arg + search + chr(10)*2
        txt += "(Avertissement : tu risques de recevoir une avalanche de messages)"
        return txt

    def getListeContent(self) :
        content = self.page.content
        liste = content.split('\n\n\n')
        return liste

    def getTextListeAmbiguous(self, liste, search, module, lang='fr') :
        if lang == None or lang == 'fr' :
            arg = ''
        else :
            arg = '-' + lang + ' '
        txt = "La recherche a plusieurs résultats. Choisis parmis ces suggestions :" + chr(10)*2
        for l in liste :
            if l.lower() == search.lower() :
                continue
            txt += '- ' + l + chr(10)
        txt += chr(10) + "Ex : Rojo " + module.lower() + " " + arg + liste[1]
        return txt

    def getTextInfo(self) :
        txt = "Ce bot permet de te donner la définition d'une expression selon Wikipédia." + chr(10)
        txt += "Tu n'as qu'à taper :" + chr(10)
        txt += "Rojo wiki (suivi de l'expression à rechercher)" + chr(10)
        txt += "Ou pour plus de détails :" + chr(10)
        txt += "Rojo wikifull (suivi de l'expression à rechercher)" + chr(10)*2
        txt += "Ex : Rojo wiki banane" + chr(10)
        txt += "Ex : Rojo wiki effet papillon" + chr(10)
        txt += "Ex : Rojo wiki Ariana Grande" + chr(10)
        txt += "Ex : Rojo wikifull Barack Obama" + chr(10)*2
        txt += "~ Suggestion ~" + chr(10)
        txt += "Tu peux voir les suggestions de recherche en tapant :" + chr(10)
        txt += "Rojo wiki -s (suivi de l'expression à rechercher)" + chr(10)*2
        txt += "Ex : Rojo wiki -s banane" + chr(10)*2
        txt += "~ Langue ~" + chr(10)
        txt += "Tu peux spécifier la langue du résultat en tapant :" +chr(10)
        txt += "Rojo wiki -(code langue) (suivie de l'expression à rechercher)" + chr(10)*2
        txt += "Ex : Rojo wiki -en banane" + chr(10)
        txt += "Ex : Rojo wikifull -it banane" + chr(10)*2
        txt += "~ Suggestion + Langue ~" + chr(10)
        txt += "Tu peux aussi voir les suggestions de recherche selon la langue :" + chr(10)*2
        txt += "Ex : Rojo wiki -s-en dauphin" + chr(10)
        txt += "Ex : Rojo wiki -s-it dauphin" + chr(10)*2
        txt += "Pour voir la liste des langues disponibles, tape :" + chr(10)
        txt += "Rojo wikilang"

        return txt

    def getListeSearch(self, search_string, lang='fr', limit=10) :
        if lang :
            wikipedia.set_lang(lang)
        s = wikipedia.search(search_string, suggestion=True, results=limit)
        return s

    def getTextSearch(self, liste, limit=10, lang='fr') :
        if lang == None or lang == 'fr' :
            arg = ''
        else :
            arg = '-' + lang + ' '
        if len(liste) > 0 :
            exemple = liste[0] if len(liste) == 1 else liste[1]
            txt = "Voici les " + str(limit) + " premières suggestions :" + chr(10)*2
            for l in liste :
                txt += '- ' + l + chr(10)
            txt += chr(10) + "Par exemple, tape :" + chr(10) + "Rojo wiki " + arg + exemple
        else :
            txt = "Désolé mais ta recherche n'a eu aucun résultat :("
        return txt

    def getTextSearchInfo(self, search_string, lang='fr') :
        if lang == None or lang == 'fr' :
            arg = ''
        else :
            arg = '-' + lang
        txt = "Pour plus de suggestions de recherche, tape :" + chr(10)
        txt += "Rojo wiki -s" + arg + " " + search_string + chr(10)*2
        txt += "Pour plus d'infos sur la fonctionnalité Wikipédia de ce bot, tape :" + chr(10)
        txt += "Rojo wiki"
        return txt

    def getLangs(self) :
        return wikipedia.languages()

    def getTextLangs(self) :
        dict_lang = self.getLangs()
        i = 1
        txt = "Liste des langues disponibles avec leurs codes :" + chr(10)*2
        for k,e in dict_lang.items() :
            txt += str(i) + '. ' + k + ' : ' + e + chr(10)
            i += 1
        return txt