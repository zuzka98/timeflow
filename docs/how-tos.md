
---
## First Time Installation and Configuration

1) Clone the <a href="https://github.com/dyvenia/timeflow" target="_blank">timeflow repository</a> into a directory chosen by you.
```git
git clone "https://github.com/dyvenia/timeflow"
```

2) Create `.env` file in the respository's `frontend` directory.

```bash
touch frontend/.env
```

Within the `.env` file, store the following environment variables:
```.env
GITHUB_CLIENT_ID = "##############"
GITHUB_CLIENT_SECRET = "##############"
SESSION_SECRET_KEY = "############"
```

**Note:** *You will need to request these details from whoever has access to the authenticating GitHub account. This will likely need to be personally requested from your organization's GitHub account.*

**Note 2:** *`GITHUB_CLIENT_ID` and `GITHUB_CLIENT_SECRET` will differ depending on whether or not you are planning to use the app in developer mode or in production mode. Make sure to enter in the appropriate details for whichever mode you plan on spinning up.*

**Note 3:** *If you are an organization owner, you will likely need to create two <a href="https://docs.github.com/en/developers/apps/building-oauth-apps/creating-an-oauth-app" target="_blank">GitHub OAuth apps</a> on your organization's GitHub in order to support both developer and production modes. If this is the case, proceed to step 2.1)*

2.1) Ignore this step if **Note 3** from step 2) does not apply to you.

Use the following guide to create the <a href="https://docs.github.com/en/developers/apps/building-oauth-apps/creating-an-oauth-app" target="_blank">GitHub OAuth apps</a>.

Set the first application's application name to "timeflow_dev". Set the homepage url to "https://127.0.0.1/". Set the callback url to "https://127.0.0.1:8001/callback".

Set the second application's application name to "timeflow". Set the homepage url to your deployed website's home url "https://my-domain.com/". Set the callback url to "https://my-domain.com/callback".

3) Create the certifications necessary for HTTPS.

Install <a href="https://github.com/FiloSottile/mkcert" target="_blank">mkcert</a> by following the installation instructions on their GitHub.
Using mkcert, create the certificates for 127.0.0.1, which is localhost. You will want to cd to the directory where mkcert is downloaded, and then the code to generate the certificates will look something like this:
```bash
mkcert 127.0.0.1
```

**Note:** *The name of your mkcert file will likely be longer/different from what was given in the example, in that case, use the entire name of the file on your system.*

This will generate two certificates. Move these certificates now into `timeflow/frontend/`. This can be done either by "dragging and dropping" or by using the terminal.

## Local Setup

1) Install <a href="https://nodejs.org/en/download/" target="_blank">npm</a>

```bash
npm install -g npm
```

2) Install npx

```bash
npm install -g npx
```

3) Install IDOM

```bash
pip install "idom[stable]"
```

4) Install Tailwind CSS
```bash
npm install -D tailwindcss postcss postcss-cli autoprefixer
npx tailwindcss init
```

5) Install FastAPI

```bash
pip install FastAPI
```

6) Spin up the backend Fastapi dev server

```bash
cd timeflow
uvicorn backend.main:app --reload
```

7) Spin up the frontend IDOM dev server
```bash
python3 -m frontend/run_reload.py
```
8) Compile the tailwind css file

```bash
cd idom_frontend/tailwind
npm run build
```


## Docker Setup - Developer mode

**Note:** ***Do not under any circumstances run this on your production server (the place where you are deploying the app). Developer mode triggers the deletion of the app's database and loads in a new one with sample data.***

1) Open a git bash terminal

2) Ensure you are in the root directory of the project

3) Navigate to `frontend/tailwind` and run `npm run build`

```bash
cd frontend/tailwind
npm run build
```

4) Run sh build.sh in home directory
```bash
cd ../..
sh build.sh
```

5) Run docker-compose -f docker-compose-dev.yaml up
```bash
docker-compose -f docker-compose-dev.yaml up
```
*If you don't wish to look at the docker logs, run the command `docker-compose up` with the flag `-d` instead of `docker-compose up`*
```bash
docker-compose up -d
```

## Docker Setup - Production mode

1) Open a git bash terminal

2) Ensure you are in the root directory of the project

3) Navigate to `frontend/tailwind` and run `npm run build`

```bash
cd frontend/tailwind
npm run build
```

4) Run sh build.sh in home directory
```bash
cd ../..
sh build.sh
```

5) Run docker-compose up
```bash
docker-compose up
```
*If you don't wish to look at the docker logs, run the command `docker-compose up` with the flag `-d` instead of `docker-compose up`*
```bash
docker-compose up -d
```

## Navigating to the application

By default, both the [Local Setup](/timeflow/how-tos/#local-setup) and the [Docker Setup](/timeflow/how-tos/#docker-setup) host the application at `127.0.0.1:8001/client/index.html`.

Thus in order to view the running application, open your favorite web browser, eg. Chrome, FireFox, etc., and enter `127.0.0.1:8001/client/index.html` into the search bar.

<a href="http://127.0.0.1:8001/client/index.html" target="_blank">http://127.0.0.1:8001/client/index.html</a>

## Working on the documentation

Timeflow's documentation has been built with <a href="https://www.mkdocs.org/" target="_blank">MkDocs</a>

The easiest way to update these docs is to host them locally, and write the updates necessary. MkDocs auto-reloads everytime you save changes to a file which allows for quick building and visualization.

```bash
mkdocs serve
```

*If you are having trouble with this step, it may be due to mkdocs auto-loading on port 8000. You may have an app already running on port 8000. If that is the case, enter the following code instead.*

```bash
mkdocs serve -a 127.0.0.1:8003
```

**Note:** *You can substitute port 8003 with any other port that is not currently in use on your system.*