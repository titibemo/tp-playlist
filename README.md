## Initialisation du projet

Pour copier le projet utiliser la commande :

```bash
git clone https://github.com/titibemo/tp-playlist
```

Ouvrez ensuite votre projet avec votre IDE, ouvrez un terminal et effectuez cette commande :

```bash
docker compose up --build
```

Un container exercice-playlist devrait être créé avec: un container postgres, un container pgadmin ainsi qu'un container python.
ouvrez le terminal de docker et effectuer cette commande pour pouvoir intéragir avec l'exercice:

```bash
docker exec -it python2 bash
```
puis
```bash
python index.py
```
Pour pouvoir lancer le script.

## Supprimer le projet

Pour supprimer le projet effectuer cette commande via le termnial de votre IDE :

```bash
docker compose down -v
```
pour supprimer les containers et les volumes associés à ce projet.
