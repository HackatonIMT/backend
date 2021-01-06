# Backend

Backend project in Python and Flask for the Hackathon of January 2021. 

## Setup

### Setup environment variables
Create a file called .env with the OpenWeatherMap API Token. It should be defined as follows
```terminal
OWM_TOKEN=<Open weather API Token>
```

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
* Setup Virtual Environment
```terminal
python3 -m venv venv
source venv/bin/activate
```

* Install packages
```terminal
pip install flask
pip install python-dotenv
pip install Flask-Cors
pip install requests
pip install gunicorn
```

### Option 3: Setup with Docker
* Build the project
```terminal
sudo docker build -t project .
```

* Run container
```terminal
sudo docker run -p 5000:5000 project
```

### Execution and Testing

* Run the application with the command
```terminal
flask run
```

* Make a GET request to http://localhost:5000/ with the browser or with curl
```terminal
curl http://localhost:5000/

OUTPUT:
Hello, World!
```
