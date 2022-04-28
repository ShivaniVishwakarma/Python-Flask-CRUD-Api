# Rollout Manager

Application to deploy applications across multiple environments. The application uses flask and svelte.

## Requirements
1. [nodejs](https://nodejs.org/en/)
2. [python](https://www.python.org/downloads/)
2. [postgres](https://www.postgresql.org/download/)

## Installation

## Svelte

Svelte application is inside the folder app/*

Use the package manager [npm](https://www.npmjs.com/) to install svelte dependencies.

```bash
cd app
npm install
```

To start the application use:
```bash
npm run dev
```

## Flask

Flask application runs inside the folder api/*

Use the package manager [pip](https://pypi.org/project/pip/) to install flask dependencies.

```bash
cd api
```

Create a virtual environment to download dependencies. To do that: 

```bash
python -m venv env
```
To activate the env
```bash
env\Scripts\activate.bat
```

To install dependencies
```bash
pip install -r requirements.txt
```

To start the application use:
```bash
flask run
```

Application runs on [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

## Initial Steps
## Postgresql

Create a new table in DB named rollout_manager.

## Migration

To initialize migration
```bash
flask db init
```
To make changes based on the model
```bash
flask db migrate
```
To update the changes to database
```bash
flask db upgrade 
```
