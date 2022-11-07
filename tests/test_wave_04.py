# There are no tests for wave 4.


######################      THIS IS MY TEST    ########################3
import unittest
from unittest.mock import Mock, patch
from datetime import datetime
from app.models.task import Task
import pytest


pytest.mark.skip(reason="No way to test this feature yet")
def test_mark_complete_on_incomplete_task(client, one_task):
    # Arrange
    """
    The future Wave 4 adds special functionality to this route,
    so for this test, we need to set-up "mocking."

    Mocking will help our tests work in isolation, which is a
    good thing!

    We need to mock any POST requests that may occur during this
    test (due to Wave 4).

    There is no action needed here, the tests should work as-is.
    """
    

    # Act
    response = client.patch("/tasks/1/mark_complete")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    