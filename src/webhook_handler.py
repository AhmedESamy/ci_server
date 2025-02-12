import logging
import json
from flask import request, jsonify
from notifier import send_notification
import os

import subprocess
from git import Repo 
import pytest
import io
from contextlib import redirect_stdout, redirect_stderr

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
      
def clone_project_upon_push_and_test(payload):
    branch_name = '/'.join((payload["ref"]).split('/')[2:])
    logging.info(branch_name)
    repo_url = payload["repository"]["html_url"]
    
    logging.info("Before commit: "+payload["before"])
    logging.info("Most recent commit: "+payload["after"])

    logging.info("Repository url: "+repo_url)
    repo = Repo.clone_from(repo_url, "./src/testingdir", branch=branch_name, single_branch=True)
    return repo
  
def handle_push_event(payload):
    """Handles push events from GitHub webhook by triggering compilation, testing, and notification."""

    #compile_project()
    therepo = clone_project_upon_push_and_test(payload)
    test_results = run_tests_on_push(payload, therepo)
    
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

def clone_project_upon_pull(payload):
    branch_name = payload["pull_request"]["head"]["ref"]
    logging.info(branch_name)
    repo_url = payload["pull_request"]["head"]["repo"]["html_url"]
    logging.info(repo_url)
    repo = Repo.clone_from(repo_url, "./src/testingdir", branch=branch_name, single_branch=True)
    return repo
  
def handle_pull_request_event(payload):
    """Handles pull request events from GitHub webhook by running tests and notifying results."""

    theRepo = clone_project_upon_pull(payload)

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
    successCode = os.system("pwd && cd src/testingdir && git clone https://github.com/AhmedESamy/Launch_Interceptor")
    if successCode != 0:
        logging.info("Could not compile project")
    else:
        logging.info("Compiled project succesfully")
    pass


# Placeholder for running tests
def run_tests_on_push(payload, repo):
    """Placeholder: Runs automated tests and returns the result."""
    logging.info("Running tests... ")
    
    commits_list = [commit["id"] for commit in payload["commits"]]
    
    results = {}

    for commit_id in commits_list:
        logging.info(f"\nTesting Commit: {commit_id}")

        repo.git.checkout(commit_id)
        stdout_output = io.StringIO()
        stderr_output = io.StringIO()
        
        with redirect_stdout(stdout_output), redirect_stderr(stderr_output):
            pytest.main(["src/testingdir/src/tests"])
        
        results[commit_id] = "Standard output: "+stdout_output.getvalue()+"Standard error: "+stderr_output.getvalue()
        
    os.system("rm -rf src/testingdir")
        
    return results
