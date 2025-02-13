# Continuous Integration (CI) Server

## Project Overview
This project is a minimal **Continuous Integration (CI) Server** that listens to GitHub webhooks, triggers automated builds and tests, and notifies results. It is implemented using **Python (Flask)** and follows standard software engineering best practices.

## Team Members
- **Ahmed** (Project Lead, Repository Setup)
- **Maxim** (Webhook Handling & Server Logic)
- **Annika** (Compilation)
- **Herdi** (Testing)
- **Kim** (CI Notification System)

## **Our Way Of Thinking** 

Our team currently occupies the stages of Formed and Collaborating in the Essence framework. Responsibilities and tasks have been assigned and adhered to with some efficiency, and rapport has been built within the team. Communication issues still arise, and misunderstandings regarding the scope of responsibilities have caused some conflicts in terms of productivity. For future improvement, communication about responsibilities and deadlines should be further clarified and made accessible to the whole team.


## Features
- **Webhook Handling:** Listens for `push` and `pull_request` events from GitHub.
- **Compilation & Testing:** Runs necessary build and test commands.
- **CI Notifications:** Sends status updates to GitHub and email notifications.
- **Automated Testing:** Uses `pytest` for test validation.

## Project Structure
```
📂 ci-server/
├── src/                 # Source code
│   ├── ci_server.py      # Main Flask app
│   ├── webhook_handler.py  # Webhook processing logic
│   ├── notifier.py       # Notification handling (commit status/email)
│
├── tests/               # Unit tests
│   ├── test_ci_server.py  # Pytest test cases
│
├── scripts/             # Helper scripts
│   ├── start_server.sh  # Script to start the CI server
│
├── config.yaml          # Configuration file
├── requirements.txt     # Python dependencies
├── README.md            # Documentation (this file)
└── .gitignore           # Ignored files (logs, virtual envs, etc.)
```

## Setup & Installation
### **1. Clone the Repository**
```sh
git clone https://github.com/AhmedESamy/ci_server/
cd ci-server
```

### **2. Create a Virtual Environment** (Optional but Recommended)
```sh
python3 -m venv venv
source venv/bin/activate  # On Mac/Linux
venv\Scripts\activate  # On Windows
```

### **3. Install Dependencies**
```sh
pip install -r requirements.txt
```

### **4. Create and set .token file**
The `.token` file will contain the access token needed to authorize updating the commit status on GitHub. 
It should be located in the base folder.
Instructions on creating a token file can be found [here](https://github.com/settings/tokens). 
If you're using a fine-grained token, it needs to be given "write" access to "Commit statuses".

NOTE: The token is secret to you. DO NOT PUSH IT. It has been added to the `.gitignore` for this reason.

## Running the CI Server
```sh
bash scripts/start_server.sh
```
This will start the Flask server and listen for webhook events.

Alternatively you accomplish this by first building the docker image by running `docker compose build`

Then you can start the server by running `docker compose up` 

## Running Tests
To run the unit tests, execute:
```sh
pytest tests/
```
This will validate the webhook handling, notification system, and CI logic.

## Webhook Configuration
To enable webhook support, configure your GitHub repository:
1. Go to **Repository Settings > Webhooks**.
2. Click **Add Webhook**.
3. Set **Payload URL** to: `http://<server-ip>:8024/webhook`
4. Choose **application/json** as the Content Type.
5. Select **push** and **pull_request** events.
6. Click **Add Webhook**.

## License
This project is licensed under the **MIT License**.

