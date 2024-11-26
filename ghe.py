import streamlit as st
import pandas as pd


# Titre principal
st.markdown(
    "<h1 style='color: #e74c3c; text-align: center;'>Coloration des graphes planaires</h1>",
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader("Entrez votre matrice sous format CSV", type=["csv"])

# Vérification si un fichier est chargé
if uploaded_file is not None:
    try:
        # Lecture du fichier CSV
        matrice_adjacence = pd.read_csv(uploaded_file)
        st.success("Fichier importé avec succès ! Voici un aperçu des données :")
        st.dataframe(matrice_adjacence)
        st.subheader("La représentation planaire du graphe")
        st.image("GRAPHEPLANAIREAQUA.PNG", use_column_width=True)
        M=matrice_adjacence.values.tolist()
    except Exception as e:
        st.error(f"Erreur lors du traitement du fichier : {e}")


# Sélection de l'heuristique
st.subheader("Heuristiques de coloration")
heuristic = st.radio(
    "Sélectionnez une heuristique :",
    ("Algorithme de coloration du graphe planaire", "Algorithme de Welsh-Powell")
)
def calcul_degre(matrice_adj):
    n = len(matrice_adj)
    degre = [0] * n  # degre doit etre innitialise a 0 cad si on a 9 sommets c'est [0,0,...,0]
    for i in range(n):
        for j in range(n):
            degre[i] += matrice_adj[i][j]
    return degre
def ordre_sommet(matrice_adj):
    degre = calcul_degre(matrice_adj)  # Degré de chaque sommet
    ordre = sorted(range(len(matrice_adj)), key=lambda x: degre[x], reverse=True)
    return ordre
def non_adjacent(sommet, v, matrice_adj):
    if not v:  # pb de syntaxe python berk
        return True

    for i in v: #ihawwess direct dans v, makallah nchofo len(v)
        if matrice_adj[i][sommet] == 1:
            return False

    return True
def Welsh_Powell(matrice_adj):
    n = len(matrice_adj)
    degre = calcul_degre(matrice_adj)      #calcul des deg
    ordre = ordre_sommet(matrice_adj)      #ordoner les sommets
    couleur = [-1] * n                     # -1 cad pas encore colore
    degre_max = max(degre) + 1             # brooks
    C = [[] for _ in range(degre_max)]     # construction de la liste des couleurs

    for i in range(n):
        sommetP = ordre[i]                 # defiler dans l'ordre
        for j in range(degre_max):
            v = C[j]                       # verifier la couleur en cours
            if couleur[sommetP] == -1 and non_adjacent(sommetP, v, matrice_adj):
                v.append(sommetP)          # lui assigner une couleur
                couleur[sommetP] = j
                break                      # aller au sommet suivant???
    DEG=calcul_degre(matrice_adj)
    st.write('Les degres de chaque sommets sont:')
    sommets = [f"F{i+1}" for i in range(len(DEG))]
    df = pd.DataFrame([DEG], columns=sommets)
    st.table(df)
    ORD=ordre_sommet(matrice_adj)
    ordre_str = " > ".join([f"F{sommet + 1}" for sommet in ORD])
    st.write(f"L'ordre des sommets est : {ordre_str}")
    st.header('Resultat:')
    for j in range(degre_max):
        if C[j]:
        # Convert the vertex index to the desired format (F1, F2, ..., F9)
            st.write(f"Couleur {j + 1} pour les sommets: {', '.join([f'F{v + 1}' for v in C[j]])}")

    return C
def ordre_elimination(A):
    n = len(A)  # Nombre de sommets
    ordre = []  # Liste pour stocker l'ordre d'élimination
    degre = [sum(A[i]) for i in range(n)]  # Calcul des degrés initiaux des sommets

    while len(ordre) < n:
        # Trouver tous les sommets avec un degré <= 5 et non encore éliminés
        candidats = [v for v in range(n) if degre[v] <= 5 and v not in ordre]

        if not candidats:
            break  # Si aucun sommet n'est éligible, sortir de la boucle

        # Trouver le sommet avec le degré minimum parmi les candidats
        sommet_min = min(candidats, key=lambda v: degre[v])

        # Ajouter ce sommet à l'ordre d'élimination
        ordre.append(sommet_min)

        # Mettre à jour les degrés des voisins
        for u in range(n):
            if A[sommet_min][u] == 1:  # Si une arête existe
                degre[u] -= 1  # Réduire le degré du voisin
        degre[sommet_min] = -1  # Marquer le sommet comme supprimé

    return ordre
def heuristique2(A, ordre):
    n = len(A)  # Nombre de sommets
    couleurs = [-1] * n  # -1 signifie que le sommet n'est pas encore colorié
    
    # Parcourir les sommets dans l'ordre inverse
    for v in reversed(ordre):
        # Trouver les couleurs utilisées par les voisins
        couleurs_voisins = set()
        for u in range(n):
            if A[v][u] == 1 and couleurs[u] != -1:  # Si u est un voisin de v et colorié
                couleurs_voisins.add(couleurs[u])
        
        # Trouver la plus petite couleur non utilisée
        couleur = 0
        while couleur in couleurs_voisins:
            couleur += 1
        
        # Attribuer la couleur au sommet
        couleurs[v] = couleur
    
    # Dictionnaire pour regrouper les sommets par couleur
    couleurs_groupes = {}
    for sommet, couleur in enumerate(couleurs):
        if couleur not in couleurs_groupes:
            couleurs_groupes[couleur] = []
        couleurs_groupes[couleur].append(f"F{sommet + 1}")
    
    # Afficher les couleurs et les sommets associés
    st.header("Résultat:")
    for couleur, sommets in sorted(couleurs_groupes.items()):
        st.write(f"Couleur {couleur + 1} pour les sommets: {', '.join(map(str, sommets))}")
# Bouton pour appliquer la coloration
if st.button("Appliquer la coloration"):
    if uploaded_file is None:
        st.warning("Veuillez d'abord importer un fichier CSV.")
    else:
        if heuristic == "Algorithme de coloration du graphe planaire":
            ordre = ordre_elimination(M)
            ordre_str = " > ".join([f"F{sommet + 1}" for sommet in ordre])
            st.write("L'ordre d'élimination des sommets vérifiant $d(G) \\leq 5$ est :",ordre_str )
            heuristique2(M, ordre)
            st.image("minheur.PNG", use_column_width=True)
            
        elif heuristic == "Algorithme de Welsh-Powell":
            Welsh_Powell(M)
            st.image("welsheur.PNG", use_column_width=True)
