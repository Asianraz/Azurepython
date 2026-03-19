# Pokemon Explorer (Python + Azure App Service)

A small Flask app that fetches Pokemon data from PokeAPI and displays it in a simple UI.

## 1. Run locally

```bash
python -m venv .venv
# Windows PowerShell
. .venv/Scripts/Activate.ps1
pip install -r requirements.txt
python app.py
```

Open: `http://localhost:8000`

## 2. Deploy to Azure App Service (Linux)

Make sure Azure CLI is installed and you are logged in:

```bash
az login
```

Set your values:

```bash
RESOURCE_GROUP="rg-pokemon-demo"
LOCATION="eastus"
APP_NAME="pokemon-app-<unique-name>"
PLAN_NAME="plan-pokemon-demo"
RUNTIME="PYTHON|3.11"
```

Create resource group, app service plan, and web app:

```bash
az group create --name $RESOURCE_GROUP --location $LOCATION
az appservice plan create --name $PLAN_NAME --resource-group $RESOURCE_GROUP --sku B1 --is-linux
az webapp create --resource-group $RESOURCE_GROUP --plan $PLAN_NAME --name $APP_NAME --runtime $RUNTIME
```

Set startup command for gunicorn:

```bash
az webapp config set --resource-group $RESOURCE_GROUP --name $APP_NAME --startup-file "gunicorn --bind=0.0.0.0:$PORT app:app"
```

Deploy code from this folder:

```bash
az webapp up --name $APP_NAME --resource-group $RESOURCE_GROUP --runtime $RUNTIME --sku B1
```

Open your deployed app:

```bash
az webapp browse --resource-group $RESOURCE_GROUP --name $APP_NAME
```

## Project structure

- `app.py`: Flask app
- `templates/index.html`: UI page
- `static/styles.css`: styles
- `requirements.txt`: Python dependencies
- `startup.txt`: startup command reference
