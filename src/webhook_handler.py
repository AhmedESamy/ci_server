import logging
from flask import request, jsonify
from notifier import send_notification
import os
import subprocess

# Placeholder for webhook processing
def process_webhook(payload):
    """Processes the webhook event received from GitHub and triggers necessary actions."""
    event_type = request.headers.get("X-GitHub-Event", "Unknown")
    logging.info(f"Received webhook event: {event_type}")
    
    if event_type == "push":
        return handle_push_event(payload)
    elif event_type == "pull_request":
        return handle_pull_request_event(payload)
    else:
        logging.warning(f"Unhandled event type: {event_type}")
        return jsonify({"message": "Event not handled."}), 400

# Placeholder for handling push events
def handle_push_event(payload):
    """Handles push events from GitHub webhook by triggering compilation, testing, and notification."""
    compile_project()
    test_results = run_tests()
    send_notification(test_results)
    return jsonify({"message": "Push event processed."}), 200

# Placeholder for handling pull request events
def handle_pull_request_event(payload):
    """Handles pull request events from GitHub webhook by running tests and notifying results."""
    test_results = run_tests()
    send_notification(test_results)
    return jsonify({"message": "Pull request event processed."}), 200

# Placeholder for compilation feature
def compile_project():
    """Placeholder: Compiles the project when a commit is pushed."""
    logging.info("Compiling project...")
    successCode = os.system("pwd && cd src/testingdir && git clone https://github.com/AhmedESamy/Launch_Interceptor")
    if successCode != 0:
        logging.info("Could not compile project")
    else:
        logging.info("Compiled project succesfully")
    pass

# Placeholder for running tests
def run_tests():
    """Placeholder: Runs automated tests and returns the result."""
    logging.info("Running tests...")
    result = subprocess.run(
        'cd src/testingdir && cd $(ls -d */) && pytest src/tests/ && cd .. && rm -rf $(ls -d */)',
        capture_output=True,
        text=True,
        shell=True
    )
    
    return result.stdout