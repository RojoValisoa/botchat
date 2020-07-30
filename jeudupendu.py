import random

class JeuDuPendu :
    
    def __init__(self) :
        self.data = {}
        self.message = ''

    def setData(self, data) :
        self.data = data

    def setMessage(self, message) :
        self.message = message

    def inAvecAccent(self, lettre, mot) :
        if lettre.lower() == 'e' :
            for l in 'eéèêë' :
                if l in mot.lower() :
                    return True
        elif lettre.lower() == 'a' :
            for l in 'aàâä' :
                if l in mot.lower() :
                    return True
        elif lettre.lower() == 'u' :
            for l in 'uûü' :
                if l in mot.lower() :
                    return True
        elif lettre.lower() == 'o' :
            for l in 'oöô' :
                if l in mot.lower() :
                    return True
        elif lettre.lower() == 'i' :
            for l in 'iïî' :
                if l in mot.lower() :
                    return True
        elif lettre.lower() == 'c' :
            for l in 'cç' :
                if l in mot.lower() :
                    return True
        return False

    def thisIsNotABot(self) :
        if len(self.message) < 20 :
            return True
        return False

    def answer(self) :
        m = self.message
        d = self.data
        ans = 'Il faut écrire "Rojo pendu" simplement. Sans emoji, sans ponctuation,...'

        if not d["playing"] and m == "Rojo pendu" :
            with open("liste_francais.txt", "r", encoding = "ISO-8859-1") as f :
                lines = f.readlines()
            mot_random = random.choice(lines).strip().upper()
            while ' ' in mot_random or '-' in mot_random :
                mot_random = random.choice(lines).strip().upper()

            d["word_to_find"] = mot_random
            d["word_found"] = ''
            d["playing"] = True
            d["nb_try"] = 6
            d["letters_played"] = ''
            for lettre in mot_random :
                d["word_found"] += '_'

            ans = "Devine quel est ce mot de " + str(len(mot_random)) + " lettres" + chr(10) + chr(10)
            for lettre in mot_random :
                ans += '_ '
            ans = ans.strip() + chr(10) + chr(10)

            ans += "Vies restantes : " + str(d["nb_try"]) + chr(10)
            ans += "Lettres déjà énnoncées : " + d["letters_played"] + chr(10) + chr(10)
            ans += "Choisis une lettre (Tape Exit pour ne plus jouer)"
        
        elif d["playing"] :
            if m == "exit" :
                d["playing"] = False
                ans = "Le mot était : " + d["word_to_find"] + chr(10)
                ans += "Le jeu du pendu de Rojo te dit... Bye bye xD" + chr(10)
                ans += "Retape 'Rojo pendu' pour rejouer"
            
            elif len(m) > 1 or ( len(m) == 1 and m.lower() not in 'abcdefghijklmnopqrstuvwxyz' ) :
                ans = "Il faut choisir une seule lettre entre A et Z, sans accent. Au pire choisis une lettre au hasard (Tape Exit pour ne plus jouer)"
            elif m.upper() in d["letters_played"] :
                ans = "Cette lettre a déjà été énnoncée... Tu perds une vie" + chr(10) + chr(10)
                d["nb_try"] -= 1

                for letter in d["word_found"] :
                    ans += letter + ' '
                ans = ans.strip() + chr(10) + chr(10)

                ans += "Vies restantes : " + str(d["nb_try"]) + chr(10)
                ans += "Lettres déjà énnoncées : " + d["letters_played"] + chr(10) + chr(10)

                if d["nb_try"] <= 0 :
                    ans += "Tu as perdu et tu es...  pendu !" + chr(10) 
                    ans += "Le mot était : " + d["word_to_find"] + chr(10) + chr(10)
                    ans += "A la prochaine pour une autre partie ;) tu peux retaper 'Rojo pendu' pour rejouer"
                    d["playing"] = False
                else :
                    ans += "Choisis une lettre (Tape Exit pour ne plus jouer)"
            else :
                m = m.upper()
                d["letters_played"] += m

                if m in d["word_to_find"] or self.inAvecAccent(m, d["word_to_find"]) :
                    ans = "Oui il y a un " + m + " ! ^^" + chr(10) + chr(10)
                    mystere = ''
                    for i in range(len(d["word_to_find"])) :
                        if d["word_found"][i] == '_' and (d["word_to_find"][i] == m or self.inAvecAccent(m, d["word_to_find"][i])) :
                            mystere += d["word_to_find"][i]
                        else :
                            mystere += d["word_found"][i]
                    
                    d["word_found"] = mystere

                    for letter in d["word_found"] :
                        ans += letter + ' '
                    ans = ans.strip() + chr(10) + chr(10)

                    ans += "Vies restantes : " + str(d["nb_try"]) + chr(10)
                    ans += "Lettres déjà énnoncées : " + d["letters_played"] + chr(10) + chr(10)

                    if d["word_to_find"] == d["word_found"] :
                        ans += "Bravo tu as gagné ! ^u^" + chr(10)
                        ans += "Le mot était bel et bien : " + d["word_to_find"] + chr(10) + chr(10)
                        ans += "A la prochaine pour une autre partie ;) tu peux retaper 'Rojo pendu' pour rejouer"
                        d["playing"] = False
                    else :
                        ans += "Choisis une lettre (Tape Exit pour ne plus jouer)"

                else :
                    ans = "Dommage il n'y a pas de " + m + " :/" + chr(10) + chr(10)
                    d["nb_try"] -= 1

                    for letter in d["word_found"] :
                        ans += letter + ' '
                    ans = ans.strip() + chr(10) + chr(10)

                    ans += "Vies restantes : " + str(d["nb_try"]) + chr(10)
                    ans += "Lettres déjà énnoncées : " + d["letters_played"] + chr(10) + chr(10)

                    if d["nb_try"] <= 0 :
                        ans += "Tu as perdu et tu es... pendu !" + chr(10)
                        ans += "Le mot était : " + d["word_to_find"] + chr(10) + chr(10) 
                        ans += "A la prochaine pour une autre partie ;) tu peux retaper 'Rojo pendu' pour rejouer"
                        d["playing"] = False
                    else :
                        ans += "Choisis une lettre (Tape Exit pour ne plus jouer)"

            
        res = {"data": d, "answer": ans}
        return res