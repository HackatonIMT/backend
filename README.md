# Backend

Backend project in Python and Flask for the Hackathon of January 2021. 

## Setup
### Option 1: Setup with requirements.txt
* Setup Virtual Environment
```terminal
python3 -m venv venv
source venv/bin/activate
```

* Install Requirements
```terminal
pip install -r requirements.txt
```
### Option 2: Setup from scratch
* Creer l'environement virtuel
```terminal
python3 -m venv venv
source venv/bin/activate
```

* Installer des packages
```terminal
pip install flask
pip install python-dotenv
pip install Flask-Cors
```

### Execution and Testing

* Exécutez l'application avec la commande
```terminal
flask run
```

* Faire un requete GET à l'adresse http://localhost:5000/ avec le navigateur ou curl
```terminal
curl http://localhost:5000/

OUTPUT:
Hello, World!
```
