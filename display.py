import matplotlib.pyplot as plt
import json

# Read the data from the JSON file
with open('result.json') as f:
    data = json.load(f)

# Extracting required data
identifiers = [profile['identifiant'] for profile in data['profiles']]
ips_scores = [profile['score_ips'] for profile in data['profiles']]
astre_scores = [-profile['score_astre'] for profile in data['profiles']]  # Reversed the scores for astre
results = [profile['resultat_final'] for profile in data['profiles']]

# Creating the bar chart
x = range(len(identifiers))
width = 0.35

fig, ax = plt.subplots()
rects1 = ax.bar(x, ips_scores, width, label='IPS', color='b')
rects2 = ax.bar(x, astre_scores, width, label='Astre', color='r')  # Adjusted the position for astre

ax.set_xlabel('Identifiers')
ax.set_ylabel('Scores')
ax.set_title('Scores by Identifiers and Categories')
ax.set_xticks([i for i in x])
ax.set_xticklabels(identifiers, rotation=45)
ax.legend()

# Displaying the result on the bars
for i, result in enumerate(results):
    ax.text(i, ips_scores[i], result, ha='center', va='bottom')
plt.savefig('chart.png', bbox_inches='tight')

plt.show()
