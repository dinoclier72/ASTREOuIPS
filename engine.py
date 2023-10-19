#utilisation du corpus de donnée pour définir si l'étudiant sera astre ou ips
import csv

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
        if(self.score_ips > self.score_astre):
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

allHypothese.append(Hypothese({1:"C",4:"Arduino"},3,"Astre"))
allHypothese.append(Hypothese({6:"Construire des choses",3:"UX/UI"},3,"Ips"))
allHypothese.append(Hypothese({15:"!France"},1,"IPS")

with open('reponses_cleaned.csv', newline='', encoding='utf-8') as csvfile:

    spamreader = csv.reader(csvfile, delimiter=',')

    next(spamreader,None)

    for data in spamreader:
            profilActuel = Profil(data[0])
            for hypothese in allHypothese:
                hypotheseValide = True
                for key,value in hypothese.tests.items():
                    if("!" in value):
                        if("")
                    if("," in value):
                        print("pouet")
                    elif(data[key] != value):
                        hypotheseValide = False
                if(hypotheseValide):
                    if(hypothese.option == "Astre"):
                        profilActuel.add_Astre(hypothese.poids)
                    else:
                        profilActuel.add_IPS(hypothese.poids)
            profilActuel.decision()
            print(profilActuel.__dict__)