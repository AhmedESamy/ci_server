import logging
import requests

def send_commit_status(repo, commit_sha, test_data, token):
    """Sends a commit status update to GitHub."""
    url = f"https://api.github.com/repos/{repo}/statuses/{commit_sha}"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    data = {
        "state": "success" if test_data.passed_pylint and test_data.passed_test else "failure",
        "description": "Pylint: " + ("Pass" if test_data.passed_pylint else "Fail") 
                    + ", Pytest: " + ("Pass" if test_data.passed_test else "Fail"),
        "context": "continuous-integration/custom-ci",
        "target_url": f"https://github.com/{repo}/actions"
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 201:
            logging.info(f"Successfully updated commit status for {commit_sha}")
        else:
            logging.error(f"Failed to update commit status. Status code: {response.status_code}")
            logging.error(f"Response: {response.text}")
    except Exception as e:
        logging.error(f"Error sending commit status: {str(e)}")
