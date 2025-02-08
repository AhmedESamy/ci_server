import logging
import json
from flask import request, jsonify
from notifier import send_notification
import os

def get_user_email(username):
    """Get user's email from environment variable mapping."""
    try:
        # Load email mappings from environment variable
        email_mappings = json.loads(os.environ.get('USER_EMAIL_MAPPING', '{}'))
        return email_mappings.get(username, os.environ.get('DEFAULT_RECIPIENT'))
    except json.JSONDecodeError:
        logging.error("Failed to parse USER_EMAIL_MAPPING environment variable")
        return os.environ.get('DEFAULT_RECIPIENT')

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

def handle_push_event(payload):
    """Handles push events from GitHub webhook by triggering compilation, testing, and notification."""
    try:
        repo_name = payload['repository']['full_name']
        commit_sha = payload['after']
        
        # Get username and email of person who pushed
        username = payload.get('pusher', {}).get('name')
        recipient_email = get_user_email(username)
        
        # Send initial pending notification
        send_notification(
            status="pending",
            repo=repo_name,
            commit_sha=commit_sha,
            token=os.environ.get('GITHUB_TOKEN')
        )
        
        # Run tests and get results
        success, test_message = run_tests()
        
        # Send final notification
        send_notification(
            status="success" if success else "failure",
            repo=repo_name,
            commit_sha=commit_sha,
            token=os.environ.get('GITHUB_TOKEN'),
            email_config={
                "recipient": recipient_email,
                "smtp_server": os.environ.get('SMTP_SERVER'),
                "smtp_port": int(os.environ.get('SMTP_PORT')),
                "sender_email": os.environ.get('SENDER_EMAIL'),
                "sender_password": os.environ.get('EMAIL_PASSWORD')
            },
            message=test_message
        )
        
        return jsonify({
            "message": "Push event processed.",
            "test_success": success,
            "test_message": test_message
        }), 200
        
    except Exception as e:
        logging.error(f"Error processing push event: {str(e)}")
        return jsonify({"error": str(e)}), 500

def handle_pull_request_event(payload):
    """Handles pull request events from GitHub webhook by running tests and notifying results."""
    try:
        repo_name = payload['repository']['full_name']
        commit_sha = payload['pull_request']['head']['sha']
        
        # Get username and email of person who created the PR
        username = payload.get('pull_request', {}).get('user', {}).get('login')
        recipient_email = get_user_email(username)
        
        # Send initial pending notification
        send_notification(
            status="pending",
            repo=repo_name,
            commit_sha=commit_sha,
            token=os.environ.get('GITHUB_TOKEN')
        )
        
        # Run tests and get results
        success, test_message = run_tests()
        
        # Send final notification
        send_notification(
            status="success" if success else "failure",
            repo=repo_name,
            commit_sha=commit_sha,
            token=os.environ.get('GITHUB_TOKEN'),
            email_config={
                "recipient": recipient_email,
                "smtp_server": os.environ.get('SMTP_SERVER'),
                "smtp_port": int(os.environ.get('SMTP_PORT', 587)),
                "sender_email": os.environ.get('SENDER_EMAIL'),
                "sender_password": os.environ.get('EMAIL_PASSWORD')
            },
            message=test_message
        )
        
        return jsonify({
            "message": "Pull request event processed.",
            "test_success": success,
            "test_message": test_message
        }), 200
        
    except Exception as e:
        logging.error(f"Error processing pull request event: {str(e)}")
        return jsonify({"error": str(e)}), 500

def compile_project():
    """Placeholder: Compiles the project when a commit is pushed."""
    logging.info("Compiling project...")
    pass

def run_tests():
    """Placeholder: Runs automated tests and returns the result."""
    logging.info("Running tests...")
    return True, "Tests completed successfully"  # Replace with actual test execution logic