# -*- coding: utf-8 -*-
# Simulation complète du processus d'analyse décrit dans le diagramme fourni

import matplotlib.pyplot as plt
import numpy as np
import random
from collections import Counter
import hashlib
import time

# -------------------- 1. Base de données : Collecte des informations utilisateur -------------------- #
def collecter_informations():
    messages = ["fake news", "real deal", "AI generated", "trust me", "fake profile", "scam alert"] * 50
    likes = [random.randint(10, 100) for _ in range(300)] + [500, 520, 550]  # valeurs critiques
    scores_video = [random.gauss(70, 10) for _ in range(150)] + [25, 20, 15, 10]
    return messages, likes, scores_video


def collecter_informations(fichier_excel, feuille=0):
    """
    Lit un fichier Excel et extrait les colonnes nécessaires.
    
    Paramètres :
    - fichier_excel : chemin vers le fichier .xlsx
    - feuille : nom ou index de la feuille Excel à lire (par défaut = 0)

    Retour :
    - messages : liste de textes
    - likes : liste d'entiers
    - scores_video : liste de floats
    """
    try:
        df = pd.read_excel(fichier_excel, sheet_name=feuille)

        # On suppose que les colonnes s'appellent exactement ainsi :
        messages = df['message'].astype(str).tolist()
        likes = df['likes'].astype(int).tolist()
        scores_video = df['score_video'].astype(float).tolist()

        return messages, likes, scores_video
    
    except FileNotFoundError:
        print("Fichier Excel non trouvé.")
    except KeyError as e:
        print(f"Colonne manquante dans le fichier Excel : {e}")
    except Exception as e:
        print(f"Erreur inattendue : {e}")


# -------------------- 2. IA : Réception et prétraitement -------------------- #
def pretraiter_donnees(messages, likes, scores):
    messages = [mot.lower() for mot in messages]
    scores = np.clip(scores, 0, 100)
    return messages, likes, scores

# -------------------- 3. Analyse IA -------------------- #
def analyse_texte(messages):
    mots = ' '.join(messages).split()
    compteur = Counter(mots)
    return dict(compteur.most_common(10))

def analyse_nombre(likes):
    clusters = {'Faible': 0, 'Moyen': 0, 'Élevé': 0}
    for val in likes:
        if val < 100:
            clusters['Faible'] += 1
        elif val < 300:
            clusters['Moyen'] += 1
        else:
            clusters['Élevé'] += 1
    return clusters

def analyse_video(scores):
    seuil = 40
    scores = sorted(scores)
    return scores, seuil

# -------------------- 4. Extraction des résultats -------------------- #
def extraire_resultats(res_texte, res_nombres, res_scores):
    return {
        'texte': res_texte,
        'nombres': res_nombres,
        'video': res_scores
    }

# -------------------- 5. Stockage et hashage -------------------- #
def creer_hash(donnees):
    hash_input = str(donnees).encode()
    return hashlib.sha256(hash_input).hexdigest()

# -------------------- 6. Blockchain : sauvegarder le hash -------------------- #
def sauvegarder_hash(hash_val):
    print("Hash sauvegardé dans la blockchain :", hash_val)

# -------------------- 7. Plateforme : affichage des résultats -------------------- #
def afficher_resultats_graphiques(resultats):
    fig, axs = plt.subplots(1, 3, figsize=(18, 5))
    fig.suptitle("Résultats de l'analyse IA (Texte, Nombre, Vidéo)", fontsize=16)

    # Texte
    mots, valeurs = zip(*resultats['texte'].items())
    axs[0].bar(mots, valeurs, color='orange')
    axs[0].set_title("Analyse de texte (mots fréquents)")
    axs[0].tick_params(axis='x', rotation=45)

    # Nombre
    cles, quantites = zip(*resultats['nombres'].items())
    axs[1].bar(cles, quantites, color='steelblue')
    axs[1].set_title("Analyse numérique (likes par cluster)")

    # Vidéo
    axs[2].plot(resultats['video'][0], marker='o', linestyle='-', color='green')
    axs[2].axhline(y=resultats['video'][1], color='red', linestyle='--', label='Seuil de doute')
    axs[2].set_title("Analyse vidéo (score de fiabilité)")
    axs[2].legend()

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()

# -------------------- Simulation complète (1 mois) -------------------- #
def executer_processus():
    print("--- Démarrage du processus mensuel ---")

    messages, likes, scores = collecter_informations()
    messages, likes, scores = pretraiter_donnees(messages, likes, scores)

    res_texte = analyse_texte(messages)
    res_nombres = analyse_nombre(likes)
    res_video = analyse_video(scores)

    resultats = extraire_resultats(res_texte, res_nombres, res_video)
    hash_resultat = creer_hash(resultats)

    sauvegarder_hash(hash_resultat)
    afficher_resultats_graphiques(resultats)

    print("--- Fin du processus ---")

# -------------------- Exécution -------------------- #
if __name__ == "__main__":
    executer_processus()