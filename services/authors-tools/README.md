# Authors-Tools

Cette instance propose des outils pour traiter les auteurs.

## Utilisation

### v1/orcid-disambiguation/orcidDisambiguation

Ce web service prend en entrée du JSON avec deux champs, `id` et `value`, et
renvoie un JSON avec un identifiant ORCID dans le champ `value`.  
Le champ `value` doit contenir un json contenant au minimum les deux champs
suivants:

- `firstName` : Le prénom de la personne que l'on souhaite trouver
- `lastName` : Le nom de la personne que l'on souhaite trouver

De plus, d'autres champs facultatifs (mais fortement recommandés d'utiliser pour
plus de précision) sont disponibles :

- `email` : Une liste `[]` d'emails de la personne que l'on souhaite trouver
- `titles` : Une liste `[]` de titres de publication scientifique de la personne
  que l'on souhaite trouver
- `coAuthors` : Une liste `[]` de co-auteurs de la personne que l'on souhaite
  trouver
- `affiliations` : Une liste `[]` d'affiliations (présentes ou passées) de la
  personne que l'on souhaite trouver

Le programme fonctionne de la façon suivante :

- Il fait une requète ORCID pour le `firstName` et `lastName` donnés récupérant
  un nombre `nameDepth` de personnes, `nameDepth` étant un paramètre fixé à 20,
  et pouvant être modifié via l'url.
- L'algorithme va ensuite prendre ces personnes une à une et effectuer dans cet
  ordre :
  - Si une liste d'emails a été fournie en entrée, il va effectuer une
    comparaison avec les emails disponibles pour la personne. Il s'arrète si il
    y en a un en commun, et renvoie l'orcid de la personne.
- L'algorithme va ensuite faire une requête afin de récupérer un nombre
  `worksDepth` maximum de publications de la personne, `worksDepth` étant un
  paramètre fixé à 20, et pouvant être modifié via l'url. De ces publications il
  va extraire les titres ainsi que tous les co-auteurs disponibles.
  - Si une liste de titres a été fournie en entrée, l'algorithme va ensuite
    comparer les titres de ces publications avec la liste d'entrée. Si un titre
    de la liste d'entrée correspond à plus de 70% avec un titre de la liste des
    publications de la personne, l'algorithme s'arrète et renvoie l'orcid de
    cette personne.
  - Si une liste de co-auteurs a été fournie en entrée, l'algorithme va ensuite
    comparer les co-auteurs de ces publications avec la liste d'entrée. Si un
    co-auteur de la liste d'entrée correspond avec un co-auteur de la liste des
    publications de la personne, l'algorithme s'arrête et renvoie l'orcid de
    cette personne.
  - Enfin si aucune des étapes précédentes n'est validée, et si une liste
    d'affiliations a été fournie, l'algorithme va comparer la liste
    d'affiliations d'entrée avec les affiliations présentes et passées de la
    personne. Plus il y a d'affiliations en commun, plus la personne obtiendra
    un score élévé et sera susceptible d'être retenue à la fin.
  - Pour finir, des points sont également ajoutés au score si la personne a le
    même nom, le même prénom ou la même initiale que le prénom de la personne
    que l'on souhaite retrouver. Si au cour de cette boucle l'algorithme ne
    s'est pas arrété suite à un email, titre ou co-auteur, il renverra la
    personne ayant obtenu le plus gros score.

Pour les combinaisons de prénom/nom très communes dans certains pays (par
exemple John Smith, Yue Chen), il est conseillé d'augmenter le paramètre
`nameDepth`. Cependant cela risque également d'augmenter le temps de calcul.  
De plus l'algorithme renverra dans la majorité des cas un résultat, mais il est
possible que celui-ci soit incorrect si aucun des arguments d'entrée n'a aidé à
identifier la personne recherchée.

Remarque : On ne pourra pas trouver une personne à l'aide de titres, co-auteurs,
emails et affiliations si cette personne n'a pas rentré ces données dans son
compte orcid, par conséquent une personne étant sur orcid mais n'ayant mis
aucune information à disposition peut ne pas être trouvée.

#### Exemple v1/orcid-disambiguation/orcidDisambiguation

```bash
$ cat <<EOF | curl -X POST --data-binary @- "https://authors-tools.services.inist.fr/v1/orcid-disambiguation/orcidDisambiguation"
[{"id":"1","value":[{"firstName" : "Pascal", "lastName" : "Cuxac", "email" : ["blabla@blabla.fr","pascal.cuxac@inist.fr"]}]},
 {"id":"2","value":[{"firstName" : "Rubén", "lastName" : "Vázquez-Cárdenas", "coAuthors" : ["Juan pablo Martínez-Pastor"]}]}]
EOF
```

Sortie

```json
[{"id":"1","value":"0000-0002-6809-5654"},
 {"id":"2","value":"0000-0002-8416-869X"}]
EOF
```

Exemple d'url en modifiant les paramètres `nameDepth` et `worksDepth` :

<https://authors-tools.services.inist.fr/v1/orcid-disambiguation/orcidDisambiguation?nameDepth=50&worksDepth=40>

### v1/first-name/gender

Ce web-service renvoie le genre d'un prénom.

Il prend en entrée du JSON avec deux champs, `id` et `value`, et renvoie un JSON
avec le genre du prénom dans le champ `value`.

#### Données de v1/first-name/gender

Le fichier `nam_dict_merged.txt` est la fusion de deux fichiers venant de
sources différentes :

- `nam_dict.txt` vient de données de la librairie
  [`gender_guesser`](<https://github.com/lead-ratings/gender-guesser/tree/master/gender_guesser/data>).
  Ces données sont sous licence GNU.
- `national_names.csv` vient de la base de données
  [`Kaggle`](https://www.kaggle.com/datasets/haezer/french-baby-names?select=national_names.csv)
  et contient tous les prénoms français données depuis 1900. Ce fichier a été
  pré-traité pour correspondre à la structure du `nam_dict.txt`. On le retrouve
  ainsi dans le fichier `nam_dict_merged.txt` à partir de la ligne 48822.

Le fichier `preprocessing.py` permet de créer le `name_gender.pickle` qui
contient des couples `{"prénom":"genre"}`.  
Enfin le fichier `gender.py` permet de renvoyer le genre d'un prénom en gérant
les différentes types de prénoms. Il renvoie le genre si le prénom est trouvé,
un "unknown" si le prénom n'est pas dans la base et une "erreur" si le prénom
n'a pas le format attendu par le web-service.  

> **NOTE**: pour le moment le fichier `affiliations-tools-corporate.json` est
> stocké sur un serveur interne à l'Inist, ce qui casse le test de cette route
> depuis GitHub.  Il faudra utiliser un remote DVC pour récupérer le fichier à
> la construction de l'image Docker.

#### Exemple de v1/first-name/gender

Entrée

```bash
$ cat <<EOF | curl -X POST --data-binary @- "https://authors-tools.services.inist.fr/v1/first-name/gender"
[{"id": "1", "value": "Jean Christophe"},{"id": "2", "value": "Amke"},{"id": "3", "value": "Seong-Eun"},{"id": "4", "value": "James A."}]
EOF
```

Sortie

```json
[
  {"id": "1", "value": "male"},
  {"id": "2", "value": "mostly_female"},
  {"id": "3", "value": "female"},
  {"id": "4", "value": "male"}
]
```

### v1/corporate/private-public

Ce web-service renvoie pour chaque affiliations d'auteurs si l'organisme d'appartenance est privé ou public.
Il prend en entrée du JSON avec deux champs, `id` et `value`, et renvoie un JSON avec le nom de l'entreprise et son statut dans le champ `value`.

Le programme filtre dans un premier temps les affiliations avec une liste de mots-clés issus du privé et du public. Ensuite, les affiliations restantes sont traitées (normalisation et découpage des abréviations). Les noms des entreprises et leur numéro de département (quand il est présent) sont envoyés par requête à l'API  [Recherche d’entreprises](<https://api.gouv.fr/documentation/api-recherche-entreprises>). Celle-ci renvoie toute une liste d'informations parmi lesquelles le champ `est_service_public`. Si ce champ est à False, alors il s'agit d'une entreprise privée.

NB : Ce WS peut être un peu lent car l'API limite le nombre de requêtes à 7 par seconde.

#### Exemple de v1/corporate/private-public

Entrée

```bash
$ cat <<EOF | curl -X POST --data-binary @- "https://authors-tools.services.inist.fr/v1/corporate/private-public"
[{"id": "1", "value": "Abeeway, F-06903 Sophia Antipolis, France"},{"id": "2", "value": "AiryLab SARL, 34 Rue Jean Baptiste Malon, F-04800 Greoux Les Bains, France"},{"id": "3", "value": "4G TECHNOL, F-06370 Mouans Sartoux, France"},{"id": "4", "value": "Univ Cote dAzur, INRIA, Ansys, Nice, France"}]
EOF
```

Sortie

```json
[
  {"id":"1","value":"organisme: abeeway, statut: private"},
  {"id":"2","value":"organisme: airylab sarl, statut: private"},
  {"id":"3","value":"organisme: 4g technique, statut: Informations manquantes"},
  {"id":"4","value":"organisme: univ cote dazur, statut: public"}]
```
