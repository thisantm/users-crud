# users-crud

## Running the Setup Scripts

To run the parser, run the following script:

```bash
bash run_parser.sh
```

To setup and run the server, run the following script: (it will only setup if there is no venv folder at root)

```bash
bash setup_server.sh
```

To setup and run the client, run the following script: (it will only setup if there is no node_modules folder in the client folder)

```bash
bash setup_client.sh
```


## Setup

First, clone the repository and navigate into it:

```bash
git clone <repository-url>
cd users-crud
```

Then, create a Python environment:

```bash
python3 -m venv <name-of-enviroment>
source env/bin/activate
```

Next, install the necessary npm packages in the client directory:

```bash
cd client
npm install
```

## Running the Server

To run the server, navigate to the server directory and execute the following command:

```bash
cd server
python3 main.py
```

## Running the Client

To run the client, navigate to the client directory and execute the following command:

```bash
cd client
npm run dev
```

## Running the Parser

To run the parser, navigate to the server directory and execute the following command:

```bash
python3 parser.py
```
