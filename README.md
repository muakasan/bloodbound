# bloodbound

Web app for playing the Bloodbound card game.

[Rules reference](https://images-cdn.fantasyflightgames.com/ffg_content/Blood%20Bound/HB08_Blood_Bound_rules_eng_V3.pdf)

## Setup
#### Backend Setup
1. Install pip
2. cd server
3. python -m venv bb_venv
4. source bb_venv/bin/activate
5. pip install -r requirements.txt
6. python server.py

#### Frontend Setup
1. Install npm
2. cd client
3. npm install
4. npm start

## Development
In `/client/` run `npm run start`, in `/server/` run `python3 server.py`. The
client is available at `localhost:3000`, the server at `localhost:8080`. 
You may also build and run the included Dockerfile, which by default hosts at `localhost:8000`.
