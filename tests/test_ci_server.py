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
    
    mocker.patch("builtins.open", mock_open(read_data="token"))
    mock_handle_push_event = mocker.patch("webhook_handler.handle_push_event")
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
    
    mocker.patch("builtins.open", mock_open(read_data="token"))
    mock_handle_push_event = mocker.patch("webhook_handler.handle_push_event")
    response = mock_client.post("/webhook", 
                           json={"something": "something"}, 
                           headers={"X-GitHub-Event": "potato"}) # Invalid event
    
    # Assertions
    assert response.status_code == 200
    assert response.get_json() == {"message": "Received update, running tests"}

    # Verify that handle_push_event was not called
    mock_handle_push_event.assert_not_called()

def test_clone_project_upon_push_and_test_dir_exists(mocker):
    # Test that we remove `./testingdir` if it exists before cloning
    mock_rmtree = mocker.patch("shutil.rmtree")
    mocker.patch("pathlib.Path.is_dir", return_value=True)
    mocker.patch("src.webhook_handler.Repo.clone_from")
    payload = {"ref": "something",
               "before" : "something",
               "after" : "something",
               "repository" : {"html_url" : "something"},
               }
    handler.clone_project_upon_push_and_test(payload)
    mock_rmtree.assert_called_once_with("./testingdir")
    
def test_clone_project_upon_push_and_test_dir_not_exists(mocker):
    # Test that `rmtree` is not called if `./testingdir` does not exist
    mock_rmtree = mocker.patch("shutil.rmtree")
    mocker.patch("pathlib.Path.is_dir", return_value=False)
    mocker.patch("src.webhook_handler.Repo.clone_from")
    payload = {"ref": "something",
               "before" : "something",
               "after" : "something",
               "repository" : {"html_url" : "something"},
               }
    handler.clone_project_upon_push_and_test(payload)
    mock_rmtree.assert_not_called()
    

def test_a_new_test(mocker):
    assert True
    
def test_a_new_test_two(mocker):
    assert True