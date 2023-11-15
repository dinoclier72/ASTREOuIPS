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
            self.resultat_final = "Rien"
        elif(self.score_ips > self.score_astre):
            self.resultat_final = "IPS"
        else:
             self.resultat_final = "Astre"

class Hypothese:
    def __init__(self, tests,poids,option,details=""):
        self.poids = poids
        self.tests = tests
        self.option = option
        self.details = details

allProfiles = []
allHypothese = [
    Hypothese({1:"C",4:"Arduino"},3,"Astre","C + Arduino"),#hypothèse 1: C + arduino = AStre (3points)
    Hypothese({6:"Construire des choses",3:"UX/UI"},3,"Ips","UX/UI + construction dans mincraft"),#hypothèse 2: construction dans minecraft + uX/UI = IPS (3 points)
    Hypothese({15:"!France"},1,"IPS","Etranger"),#hypothèse 3: étranger = IPS (1 point)
    Hypothese({17:"Je ne prends pas de sac à dos,Mon pc portable only"},2,"IPS","Pas de sac ou que le pc portable"),#hypothèse 4: pc portable only ou pas de sac à dos IPS (1 point)
    Hypothese({6:"La redstone",3:"Domotique,Robotique"},4,"Astre","Redstone dans minecraft et Robtique/Domotique"),#hypothèse 5: redstone dans minecraft + domotique/robotique = astre (4 points)
    Hypothese({14:"Créer du contenu",11:">4"},4,"IPS","Intressé par la création et proche de l'utilisateur"),#hypothèse 6: creation de contenu + proche de l'utilisateur = IPS (4 points)
    Hypothese({8:"ENSIMERSION",3:"UX/UI"},4,"Ips","ENSIMERSION et UX/UI"),#hypothèse 7: ENSIMERSION + UX/UI = TPS (2 points)
    Hypothese({5:"!Non",3:"Domotique,Robotique"},4,"Astre","A démonté quelque chose et est intéressé par la robotique/domotique"),#hypothèse 8: démonté quelque chose + domotique/robotique = astre (4 points)
    Hypothese({3:"Robotique",16:"Le fonctionnel"},4,"Astre","robotique et le fonctionnel"),#hypothèse 9:Robotique + fonctionnel = Astre (3 points)
    Hypothese({3:"Frontend / Backend"},3,"IPS","backend/frontend et esthétique")#hypothèse 10: frotend/backend + esthétique = IPS (3 points)
]

import json

def save_hypotheses_to_json(hypotheses, output_json):
    with open(output_json, 'w', encoding='utf-8') as file:
        json_hypotheses = [hypothesis.__dict__ for hypothesis in hypotheses]
        json.dump(json_hypotheses, file, ensure_ascii=False, indent=4)

def load_hypotheses(input_json):
    with open(input_json, 'r', encoding='utf-8') as file:
        json_hypotheses = json.load(file)
        allHypothese = []
        for hypothesis in json_hypotheses:
            tests = {int(k): v for k, v in hypothesis['tests'].items()}
            allHypothese.append(Hypothese(tests, hypothesis['poids'], hypothesis['option'],hypothesis['details']))
    return allHypothese

def process_data_and_write_to_json(input_csv, output_json,allHypothese):
    allProfiles = []
    with open(input_csv, newline='', encoding='utf-8') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        next(spamreader,None)
        for data in spamreader:
            profilActuel = Profil(data[0])
            for hypothese in allHypothese:
                hypotheseValide = True
                for key,value in hypothese.tests.items():
                    answer = data[key].split(";")
                    if("!" in value):
                        if(value[1:] in answer):
                            hypotheseValide = False
                    elif("," in value):
                        tempBool = False
                        temp = value.split(",")
                        for val in temp:
                            if(val in answer):
                                tempBool = True
                        if(not tempBool):
                            hypotheseValide = False
                    elif(">" in value):
                        if(int(answer[0]) <= int(value[1:])):
                            hypotheseValide = False
                    elif(value not in answer):
                        hypotheseValide = False
                if(hypotheseValide):
                    if(hypothese.option == "Astre"):
                        profilActuel.add_Astre(hypothese.poids)
                    else:
                        profilActuel.add_IPS(hypothese.poids)
            profilActuel.decision()
            allProfiles.append(profilActuel)

    with open(output_json,"w") as file:
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

if(__name__ == "__main__"):
    save_hypotheses_to_json(allHypothese, 'hypotheses.json')
    #allHypothese = load_hypotheses('hypotheses.json')
    #process_data_and_write_to_json("data_cleaned.csv","result.json")