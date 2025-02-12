import pytest
from unittest.mock import mock_open
import src.webhook_handler as handler
from src.ci_server import app

@pytest.fixture
def mock_client():
    # Testing client for our app
    return app.test_client()

@pytest.fixture
def mock_payload():
    return {"something" : "something"}

@pytest.fixture
def mock_token():
    return "token"

def test_handle_webhook_push_event(mock_client, mock_payload, mock_token, mocker):
    # Test that a push event correctly triggers `handle_push_event`    
    
    # Simulate reading from the .token file
    mocker.patch("builtins.open", mock_open(read_data="token"))
    
    # Prevent handle_push_event from executing
    mock_handle_push_event = mocker.patch("webhook_handler.handle_push_event")

    # Send a simulated POST
    response = mock_client.post("/webhook", 
                           json={"something": "something"}, 
                           headers={"X-GitHub-Event": "push"})
    
    # Assertions
    assert response.status_code == 200
    assert response.get_json() == {"message": "Received update, running tests"}

    # Verify that handle_push_event was called with the correct arguments
    mock_handle_push_event.assert_called_once_with(mock_payload, mock_token)

def test_process_webhook_incorrect(mock_client, mock_payload, mock_token, mocker):
    # Test that an invalid event does not trigger `handle_push_event`    
    
    # Simulate reading from the .token file
    mocker.patch("builtins.open", mock_open(read_data="token"))
    
    # Prevent handle_push_event from executing
    mock_handle_push_event = mocker.patch("webhook_handler.handle_push_event")

    # Send a simulated POST request
    response = mock_client.post("/webhook", 
                           json={"something": "something"}, 
                           headers={"X-GitHub-Event": "potato"}) # Invalid event
    
    # Assertions
    assert response.status_code == 200
    assert response.get_json() == {"message": "Received update, running tests"}

    # Verify that handle_push_event was not called
    mock_handle_push_event.assert_not_called()
    

def test_webhook_push_event():
    """Placeholder: Tests handling of a push event webhook by making a real request."""
    pass

def test_webhook_pull_request_event():
    """Placeholder: Tests handling of a pull request event webhook by making a real request."""
    pass

def test_handle_push_event():
    """Placeholder: Tests direct call to handle_push_event function."""
    pass

def test_handle_pull_request_event():
    """Placeholder: Tests direct call to handle_pull_request_event function."""
    pass
