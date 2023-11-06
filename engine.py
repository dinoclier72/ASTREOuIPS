#utilisation du corpus de donnée pour définir si l'étudiant sera astre ou ips
import csv
import json

#hypothèse 1: C + arduino = AStre (3points)
#hypothèse 2: construction dans minecraft + uX/UI = IPS (3 points)
#hypothèse 3: étranger = IPS (1 point)
#hypothèse 4: pc portable only ou pas de sac à dos IPS (1 point)
#hypothèse 5: redstone dans minecraft + domotique/robotique = astre (4 points)
#hypothèse 6: creation de contenu + proche de l'utilisateur = IPS (4 points)
#hypothèse 7: ENSIMERSION + UX/UI = TPS (2 points)
#hypothèse 8: démonté quelque chose + domotique/robotique = astre (4 points)
#hypothèse 9:
#hypothèse 10:

class Profil:
    def __init__(self, identifiant):
        self.identifiant = identifiant
        self.score_ips = 0
        self.score_astre = 0
        self.resultat_final = ""
    def add_IPS(self,valeur):
        self.score_ips += valeur
    def add_Astre(self,valeur):
         self.score_astre += valeur
    def decision(self):
        if(self.score_ips == self.score_astre):
            self.resultat_final = "Undefined"
        elif(self.score_ips > self.score_astre):
            self.resultat_final = "IPS"
        else:
             self.resultat_final = "Astre"

class Hypothese:
    def __init__(self, tests,poids,option):
        self.poids = poids
        self.tests = tests
        self.option = option

allProfiles = []
allHypothese = []

allHypothese.append(Hypothese({1:"C",4:"Arduino"},3,"Astre"))#hypothèse 1: C + arduino = AStre (3points)
allHypothese.append(Hypothese({6:"Construire des choses",3:"UX/UI"},3,"Ips"))#hypothèse 2: construction dans minecraft + uX/UI = IPS (3 points)
allHypothese.append(Hypothese({15:"!France"},1,"IPS"))#hypothèse 3: étranger = IPS (1 point)
allHypothese.append(Hypothese({17:"Je ne prends pas de sac à dos,Mon pc portable only"},1,"IPS"))#hypothèse 4: pc portable only ou pas de sac à dos IPS (1 point)
allHypothese.append(Hypothese({6:"La redstone",3:"Domotique,Robotique"},4,"Astre"))#hypothèse 5: redstone dans minecraft + domotique/robotique = astre (4 points)
allHypothese.append(Hypothese({14:"Créer du contenu",11:">4"},4,"IPS"))#hypothèse 6: creation de contenu + proche de l'utilisateur = IPS (4 points)
allHypothese.append(Hypothese({8:"ENSIMERSION",3:"UX/UI"},2,"Ips"))#hypothèse 7: ENSIMERSION + UX/UI = TPS (2 points)
allHypothese.append(Hypothese({5:"!Non",3:"Domotique,Robotique"},4,"Astre"))#hypothèse 8: démonté quelque chose + domotique/robotique = astre (4 points)

with open('reponses_cleaned.csv', newline='', encoding='utf-8') as csvfile:

    spamreader = csv.reader(csvfile, delimiter=',')

    next(spamreader,None)

    for data in spamreader:
            profilActuel = Profil(data[0])
            for hypothese in allHypothese:
                hypotheseValide = True
                for key,value in hypothese.tests.items():
                    if("!" in value):
                        if(value[1:] == data[key]):
                            hypotheseValide = False
                    elif("," in value):
                        tempBool = False
                        temp = value.split(",")
                        for val in temp:
                            if(val == data[key]):
                                tempBool = True
                        if(not tempBool):
                            hypotheseValide = False
                    elif(">" in value):
                        if(int(data[key]) <= int(value[1:])):
                            hypotheseValide = False
                    elif(data[key] != value):
                        hypotheseValide = False
                if(hypotheseValide):
                    if(hypothese.option == "Astre"):
                        profilActuel.add_Astre(hypothese.poids)
                    else:
                        profilActuel.add_IPS(hypothese.poids)
            profilActuel.decision()
            allProfiles.append(profilActuel)

with open("result.json","w") as file:
    file.write("{\n")
    file.write("\t\"profiles\":[\n")
    for profil in allProfiles:
        file.write("\t\t")
        json.dump(profil.__dict__,file)
        if(profil != allProfiles[-1]):
            file.write(",")
        file.write("\n")
    file.write("\t]\n")
    file.write("}")