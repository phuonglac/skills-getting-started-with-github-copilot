"""
Tests for the /activities endpoint
Using AAA (Arrange-Act-Assert) pattern for test structure
"""

import pytest


class TestGetActivities:
    """Tests for GET /activities endpoint"""

    def test_get_all_activities_success(self, client):
        """
        Test that GET /activities returns all activities with correct data
        AAA Pattern:
        - Arrange: Client is ready (via fixture)
        - Act: Make GET request to /activities
        - Assert: Verify 200 response and all activities are returned
        """
        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        data = response.json()
        
        # Verify all activities are returned
        assert len(data) == 3
        assert "Chess Club" in data
        assert "Programming Class" in data
        assert "Basketball Team" in data

    def test_get_activities_contains_activity_details(self, client):
        """
        Test that each activity contains required fields
        AAA Pattern:
        - Arrange: Client is ready
        - Act: Make GET request to /activities
        - Assert: Verify each activity has description, schedule, etc.
        """
        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        chess_club = data["Chess Club"]
        assert "description" in chess_club
        assert "schedule" in chess_club
        assert "max_participants" in chess_club
        assert "participants" in chess_club
        assert isinstance(chess_club["participants"], list)

    def test_get_activities_shows_current_participants(self, client):
        """
        Test that activity data includes current participants
        AAA Pattern:
        - Arrange: Chess Club has known participants
        - Act: Make GET request to /activities
        - Assert: Verify participants list matches expected
        """
        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        chess_participants = data["Chess Club"]["participants"]
        assert len(chess_participants) == 2
        assert "michael@mergington.edu" in chess_participants
        assert "daniel@mergington.edu" in chess_participants

    def test_get_activities_empty_participation(self, client):
        """
        Test that activities with no participants show empty list
        AAA Pattern:
        - Arrange: Basketball Team has no participants
        - Act: Make GET request to /activities
        - Assert: Verify empty participants list
        """
        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        basketball_participants = data["Basketball Team"]["participants"]
        assert basketball_participants == []
        assert len(basketball_participants) == 0
