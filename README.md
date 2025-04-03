# Application Web pour l'Exécution de Commandes SSH

## Description

Ce projet est une application web basée sur Flask qui permet aux utilisateurs d'exécuter des commandes SSH sur plusieurs appareils via un jump host. Elle fournit une interface web simple où les utilisateurs peuvent saisir les informations de connexion, les appareils cibles et les commandes à exécuter. L'application utilise un `SSHManager` pour gérer les connexions SSH et exécuter les commandes sur les appareils spécifiés.

## Fonctionnalités

- Champs de saisie pour le jump host, les identifiants, les appareils cibles et les commandes.
- Exécution de commandes sur plusieurs appareils via SSH.
- Affichage des résultats des commandes exécutées dans un format convivial.

## Prérequis

Avant de lancer l'application, assurez-vous d'avoir les éléments suivants installés :

- Python 3.7 ou une version supérieure.
- Flask (`pip install flask`).
- Toutes les dépendances supplémentaires nécessaires au module `ssh_manager`.

## Installation

1. Clonez le dépôt ou téléchargez les fichiers du projet.
2. Naviguez dans le répertoire du projet :
   ```bash
   cd "CHEMIN_DU_PROJET"
   ```
3. Installez les packages Python requis :
   ```bash
   pip install -r requirements.txt
   ```
   *Utilisation d'une connnexion externe "4G" afin de bypass le PROXY*

## Utilisation

1. Lancez l'application Flask :
   ```bash
   python app.py
   ```
2. Ouvrez un navigateur web et accédez à :
   ```
   http://localhost:5000
   ```
3. Remplissez le formulaire avec les informations suivantes :
   - **Jump Host** : Le nom d'hôte ou l'adresse IP du serveur intermédiaire.
   - **Jump User** : Le nom d'utilisateur pour le serveur intermédiaire.
   - **Jump Password** : Le mot de passe pour le serveur intermédiaire.
   - **Radius User** : Le nom d'utilisateur pour les appareils cibles.
   - **Radius Password** : Le mot de passe pour les appareils cibles.
   - **Devices** : Une liste d'adresses IP ou de noms d'hôte des appareils cibles (un par ligne).
   - **Commands** : Une liste de commandes à exécuter sur les appareils (une par ligne).

4. Soumettez le formulaire pour exécuter les commandes. Les résultats seront affichés sur la page `results.html`.

## Fonctionnement

1. L'utilisateur saisit les informations de connexion, les appareils et les commandes dans le formulaire web.
2. L'application crée une instance de `SSHManager` avec les identifiants fournis.
3. Le `SSHManager` établit des connexions SSH aux appareils spécifiés via le jump host.
4. Les commandes sont exécutées sur les appareils, et les résultats sont collectés.
5. Les résultats sont affichés sur la page `results.html`.