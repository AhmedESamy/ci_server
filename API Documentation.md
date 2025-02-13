# Continuous Integration (CI) Server API Documentation

## Overview
This document provides an API-level reference for the Continuous Integration (CI) Server, detailing the available endpoints and internal functions across different files.

## **1. Webhook Handling** (`webhook_handler.py`)
Handles incoming webhook events from GitHub and processes them accordingly.

### **1.1 `process_webhook(payload, event_type)`**
- **Description**: Processes GitHub webhook events.
- **Parameters**:
  - `payload` (*dict*): JSON data received from GitHub.
  - `event_type` (*str*): Type of GitHub event (e.g., `push`, `pull_request`).
- **Returns**:
  - JSON response with a status message.

### **1.2 `handle_push_event(payload)`**
- **Description**: Handles push events by identifying changes and triggering CI steps.
- **Parameters**:
  - `payload` (*dict*): JSON data for the push event.
- **Returns**:
  - JSON response confirming the processing of the push event.

### **1.3 `handle_pull_request_event(payload)`**
- **Description**: Handles pull request events and executes necessary checks.
- **Parameters**:
  - `payload` (*dict*): JSON data for the pull request event.
- **Returns**:
  - JSON response confirming the processing of the pull request event.

---

## **2. CI Server Main Application** (`ci_server.py`)
Main entry point of the CI server, which listens for webhook events.

### **2.1 `handle_webhook()`**
- **Description**: Flask route that listens for GitHub webhook events and forwards them for processing.
- **Request Type**: `POST`
- **Endpoint**: `/webhook`
- **Request Headers**:
  - `X-GitHub-Event`: Specifies the type of event received from GitHub.
- **Returns**:
  - JSON response confirming the receipt of the webhook.

---

## **3. Compilation Handling** (`ci_server.py` / `webhook_handler.py`)
Handles project compilation and syntax checking.

### **3.1 `compile_project()`**
- **Description**: Runs compilation steps for the repository.
- **Returns**:
  - `None` (logs compilation status internally).

---

## **4. Testing Execution** (`webhook_handler.py` / `test_ci_server.py`)
Manages test execution for automated validation.

### **4.1 `run_tests()`**
- **Description**: Executes automated tests and reports results.
- **Returns**:
  - *str*: `"success"` if tests pass, `"failure"` otherwise.

---

## **5. Notification System** (`notifier.py`)
Manages notifications for CI results.

### **5.1 `send_notification(status, repo, commit_sha, token, email_config)`**
- **Description**: Sends notifications (commit status updates or email) based on CI results.
- **Parameters**:
  - `status` (*str*): Build/test result (`success` or `failure`).
  - `repo` (*str*, optional): GitHub repository name.
  - `commit_sha` (*str*, optional): SHA of the commit.
  - `token` (*str*, optional): GitHub authentication token.
  - `email_config` (*dict*, optional): Email configuration (if email notifications are enabled).
- **Returns**:
  - `None` (logs notification status internally).

### **5.2 `send_commit_status(repo, commit_sha, status, token)`**
- **Description**: Updates the commit status on GitHub.
- **Parameters**:
  - `repo` (*str*): Repository name.
  - `commit_sha` (*str*): SHA of the commit.
  - `status` (*str*): Build/test result.
  - `token` (*str*): GitHub authentication token.
- **Returns**:
  - `None` (logs commit status update internally).

### **5.3 `send_email_notification(recipient, subject, message, smtp_server, smtp_port, sender_email, sender_password)`**
- **Description**: Sends an email notification with build/test results.
- **Parameters**:
  - `recipient` (*str*): Email address of the recipient.
  - `subject` (*str*): Email subject.
  - `message` (*str*): Email body.
  - `smtp_server` (*str*): SMTP server address.
  - `smtp_port` (*int*): SMTP server port.
  - `sender_email` (*str*): Sender's email address.
  - `sender_password` (*str*): Sender's email password.
- **Returns**:
  - `None` (logs email status internally).

---

## **6. Test Cases** (`test_ci_server.py`)
Unit tests for validating CI functionality.

### **6.1 `test_webhook_push_event(client)`**
- **Description**: Tests handling of a push event webhook.
- **Parameters**:
  - `client` (*Flask test client*): Simulated test client for the Flask app.
- **Returns**:
  - `None` (asserts expected behavior).

### **6.2 `test_webhook_pull_request_event(client)`**
- **Description**: Tests handling of a pull request event webhook.
- **Parameters**:
  - `client` (*Flask test client*): Simulated test client for the Flask app.
- **Returns**:
  - `None` (asserts expected behavior).

### **6.3 `test_handle_push_event()`**
- **Description**: Tests the `handle_push_event` function directly.
- **Returns**:
  - `None` (asserts expected behavior).

### **6.4 `test_handle_pull_request_event()`**
- **Description**: Tests the `handle_pull_request_event` function directly.
- **Returns**:
  - `None` (asserts expected behavior).

---

## **7. Server Startup** (`start_server.sh`)
Shell script for launching the CI server.

### **7.1 `start_server.sh` (Shell Script)**
- **Description**: Starts the CI server using Flask and exposes it using ngrok.
- **Usage**:
  ```sh
  bash scripts/start_server.sh
  ```
- **Behavior**:
  - Activates a virtual environment (if available).
  - Starts the Flask application.
  - Exposes the server via ngrok (if needed).

---

## **Conclusion**
This API documentation provides method-level details of the CI Server components, covering webhook handling, compilation, testing, notification, and deployment. Developers can use this as a reference for extending functionality or debugging existing features.

