# users-crud

## Clone and Environment Setup

First, clone the repository and navigate into it:

```bash
git clone <repository-url>
cd users-crud
```

Then, set the environment variables for both the client and the server by copying `env.sample` to `.env` and setting the appropriate variables:

```bash
# For the server
cp server/env.sample server/.env
# Edit the server/.env file to set the appropriate variables

# For the client
cp client/env.sample client/.env
# Edit the client/.env file to set the appropriate variables
```

## Running the Setup and Run Scripts

You can either run the setup and run scripts or follow the manual instructions below.

To run the parser, run the following script:

```bash
bash run_parser.sh
```

To setup and run the server, run the following script: (it will only setup if there is no venv folder at root)

```bash
bash run_server.sh
```

To setup and run the client, run the following script: (it will only setup if there is no node_modules folder in the client folder)

```bash
bash run_client.sh
```

## Manual Setup

First, clone the repository and navigate into it:

```bash
git clone <repository-url>
cd users-crud
```

Then, create a Python environment:

```bash
cd server
python3 -m venv <name-of-enviroment>
source <name-of-enviroment>/bin/activate
```

Next, install the necessary npm packages in the client directory:

```bash
cd client
npm install
```

## Running

### The Parser

To run the parser, navigate to the server directory and execute the following command:

```bash
cd server
python3 parser.py
```

### The Server

To run the server, navigate to the server directory and execute the following command:

```bash
cd server
python3 main.py
```

### The Client

To run the client, navigate to the client directory and execute the following command:

```bash
cd client
npm run dev
```
