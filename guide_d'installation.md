# backend


### Creer l'environement virtuel
```terminal
python3 -m venv venv
source venv/bin/activate
```

### Installer des packages
```terminal
pip install flask
pip install python-dotenv
```

### Installer des packages

* Créer un dossier
```terminal 
mkdir app
```

* Créer un fichier __init__.py et un fichier routes.py dans le dossier créé précédemment
```terminal
touch app/__init__.py
touch app/routes.py
```

* Ajouter le contenu suivant au fichier __init__.py
```terminal
from flask import Flask

app = Flask(__name__)

from app import routes
```

* Ajouter le contenu suivant au fichier routes.py
```terminal
from app import app

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"
```

* Créer un fichier python avec le nom de votre choix dans la base du projet

```terminal
touch project.py
```

* Ajouter le contenu suivant au fichier routes.py
```terminal
from app import app
```

* Créer un fichier .flaskenv avec  le contenu suivant
```terminal
FLASK_APP=project.py
```
