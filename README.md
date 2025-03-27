### Introduction
#### Data Retrival Agent
An AI agent that retrieves and displays data as evidence to support your claims

It connects directly to your own databases and publicly available data via APIs to 
search for evidence supporting your claims or to answer questions with quantitative data.

### Tech Stack
1. PostgresSQL database (Running in Docker on local/cloud server)
2. Python backend codebase (FastAPI app, runs with Uvicorn, running in Docker on local/cloud server)
3. Redis (Caching/temp data for Python backend, running in Docker on local/cloud server)
4. React frontend (Vite + TypeScript, served as static files by Nginx on local/cloud server)
5. Nginx for SSL and routing (Runs directly on the local/cloud server)

### Functionalities
1. Run AI generated queries on a given database with provided credentials
2. Search the internet for data related to your question and as context to provide answer


### Developer Setup Instructions
#### Backend

1.	Create a local keys.list file with environment variables, and configure your Python run settings to use it.
2.	Install dependencies from requirements.txt.
3.	Clone the Git repository and create a development branch based on main.
4.	Push changes to the development branch and open a merge request to merge into main upon review.

#### Frontend

1. Save index.html to the local/cloud server