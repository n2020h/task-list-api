# There are no tests for wave 4.


######################      OPTIONAL: WAVE 4 TEST   ########################3
import unittest
from unittest.mock import Mock, patch
from datetime import datetime
from app.models.task import Task
import pytest


pytest.mark.skip(reason="No way to test this feature yet")
def test_mark_complete_on_incomplete_task(client, one_task):
    # Arrange

    # Act
    response = client.patch("/tasks/1/mark_complete")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    #verify posted message in Slack app
    