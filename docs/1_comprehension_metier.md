# 1. Compréhension du Métier : Assistant du Règlement des Études

## 1. L'Utilisateur et le Problème
* **Utilisateur cible :** Un étudiant ou un enseignant de l'université qui a besoin de clarifications rapides, précises et officielles sur les règles de scolarité, les modalités d'examen, les conditions de passage en année supérieure ou le calcul des moyennes.
* **Questions types posées par l'utilisateur :**
  * Quelles sont les conditions pour valider mon semestre ?
  * Quel est le pourcentage d'absence autorisé avant d'être éliminé d'une matière ?
  * Comment est calculée la moyenne générale avec les rattrapages ?
  * Quelle est la procédure en cas de fraude constatée lors d'un examen ?

## 2. Pourquoi un LLM seul ne suffit pas
Un modèle de langage (LLM) standard entraîné sur Internet ne connaît pas les règles internes spécifiques de l'université.
* **Exemple de mauvaise réponse (sans RAG) :** Si on lui demande *"Quelles sont les règles de compensation des notes à l'université ?"*, un LLM générique va inventer des règles générales basées sur des systèmes éducatifs étrangers (ex: système américain ou français standard) au lieu d'appliquer le règlement exact du document officiel de l'université, ce qui induit l'étudiant en erreur.

## 3. La Solution : Schéma RAG + Agent + Outils
* **RAG (Retrieval-Augmented Generation) :** Recherche des articles pertinents dans le PDF du règlement des études pour alimenter le contexte du LLM.
* **Agent et Outils :** Un agent décisionnel capable d'utiliser au moins deux outils :
  1. *Recherche RAG* : pour extraire les textes réglementaires et citer les sources.
  2. *Calculateur de moyenne (`calculer_moyenne`)* : pour évaluer interactivement si un étudiant valide son semestre selon ses notes.

## 4. Critères de Succès Chiffrés
1. **Précision de la recherche (Hit@3) :** $\ge 85\%$ (le bon article du règlement apparaît dans les 3 premiers documents récupérés).
2. **Pertinence de la réponse (Fidélité) :** $\ge 90\%$ des réponses générées s'appuient strictement sur les sources extraites sans hallucination.
3. **Taux de citation des sources :** $100\%$ des réponses factuelles incluent la référence exacte de l'article ou de la page.
4. **Performance de l'agent :** Temps de réponse moyen de l'agent inférieur à 3 secondes pour une requête standard.

## 5. Contraintes et Risques
* **Droits et Confidentialité :** Utilisation exclusive d'un document officiel public ou autorisé de l'université (pas de données personnelles d'étudiants réels dans la base).
* **Biais et Hallucinations :** Risque critique pour un assistant réglementaire ; le prompt système doit interdire formellement toute invention.
* **Coût et Fraîcheur :** Le règlement évoluant peu au cours de l'année, une indexation statique du PDF actuel suffit, maintenant les coûts d'API à un niveau minime.