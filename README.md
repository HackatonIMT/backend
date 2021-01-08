# Backend

Backend en Python et Flask pour le Hackathon de janvier 2021. 

## Configuration
### Option 1 : Configuration de l'environnement avec requirements.txt
* Mise en place d'un environnement virtuel
```terminal
python3 -m venv venv
source venv/bin/activate
```

* Exigences d'installation
```terminal
pip install -r requirements.txt
```
### Option 2 : Configuration manuelle 
* Mise en place d'un environnement virtuel
```terminal
python3 -m venv venv
source venv/bin/activate
```

* Installer les paquets
```terminal
pip install flask
pip install python-dotenv
pip install Flask-Cors
pip install gunicorn
```

### Option 3 : Installation avec Docker
* Construire le projet
```terminal
sudo docker build -t project .
```

* exécuter le conteneur
```terminal
projet sudo docker run -p 5000:5000
```

### Exécution et tests

* Lancer l'application avec la commande
```terminal
flask run
```

* Faire une requete GET à http://localhost:5000/ avec le navigateur ou avec curl
```terminal
curl http://localhost:5000/

SORTIE :
Hello, World!

```
