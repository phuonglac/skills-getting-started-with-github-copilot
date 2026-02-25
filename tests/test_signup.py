"""
Tests for signup and unregister endpoints
Using AAA (Arrange-Act-Assert) pattern for test structure
"""

import pytest


class TestSignupForActivity:
    """Tests for POST /activities/{activity_name}/signup endpoint"""

    def test_signup_success(self, client):
        """
        Test successful signup for an activity
        AAA Pattern:
        - Arrange: Basketball Team has 0 participants
        - Act: Sign up student for Basketball Team
        - Assert: Verify 200 response and student added to participants
        """
        # Arrange
        activity_name = "Basketball Team"
        email = "john@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )

        # Assert
        assert response.status_code == 200
        assert "Signed up" in response.json()["message"]
        
        # Verify student was added
        activities_response = client.get("/activities")
        activity_data = activities_response.json()[activity_name]
        assert email in activity_data["participants"]

    def test_signup_nonexistent_activity(self, client):
        """
        Test signup for activity that doesn't exist
        AAA Pattern:
        - Arrange: Nonexistent activity
        - Act: Try to sign up for it
        - Assert: Verify 404 response
        """
        # Arrange
        activity_name = "Nonexistent Club"
        email = "student@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )

        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_signup_duplicate_student(self, client):
        """
        Test that student cannot sign up twice for same activity
        AAA Pattern:
        - Arrange: Michael is already in Chess Club
        - Act: Try to sign up Michael again for Chess Club
        - Assert: Verify 400 response and error message
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )

        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]

    def test_signup_new_student_existing_activity(self, client):
        """
        Test new student can sign up for activity that has other participants
        AAA Pattern:
        - Arrange: Chess Club has existing participants
        - Act: Sign up new student for Chess Club
        - Assert: Verify 200 response and student added without removing others
        """
        # Arrange
        activity_name = "Chess Club"
        email = "alice@mergington.edu"
        original_participants = client.get("/activities").json()[activity_name]["participants"].copy()

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )

        # Assert
        assert response.status_code == 200
        
        # Verify new student and original participants all present
        updated_participants = client.get("/activities").json()[activity_name]["participants"]
        assert email in updated_participants
        for original_email in original_participants:
            assert original_email in updated_participants


class TestUnregisterFromActivity:
    """Tests for DELETE /activities/{activity_name}/signup endpoint"""

    def test_unregister_success(self, client):
        """
        Test successful unregister (removal) from activity
        AAA Pattern:
        - Arrange: Michael is signed up for Chess Club
        - Act: Unregister Michael from Chess Club
        - Assert: Verify 200 response and student removed from participants
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup?email={email}"
        )

        # Assert
        assert response.status_code == 200
        assert "Unregistered" in response.json()["message"]
        
        # Verify student was removed
        activities_response = client.get("/activities")
        activity_data = activities_response.json()[activity_name]
        assert email not in activity_data["participants"]

    def test_unregister_nonexistent_activity(self, client):
        """
        Test unregister from activity that doesn't exist
        AAA Pattern:
        - Arrange: Nonexistent activity
        - Act: Try to unregister from it
        - Assert: Verify 404 response
        """
        # Arrange
        activity_name = "Nonexistent Club"
        email = "student@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup?email={email}"
        )

        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_unregister_non_participant(self, client):
        """
        Test that cannot unregister a student not signed up
        AAA Pattern:
        - Arrange: Alice is not signed up for Basketball Team
        - Act: Try to unregister Alice from Basketball Team
        - Assert: Verify 400 response and error message
        """
        # Arrange
        activity_name = "Basketball Team"
        email = "alice@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup?email={email}"
        )

        # Assert
        assert response.status_code == 400
        assert "not signed up" in response.json()["detail"]

    def test_unregister_preserves_other_participants(self, client):
        """
        Test that unregistering one student doesn't affect others
        AAA Pattern:
        - Arrange: Chess Club has Michael and Daniel
        - Act: Unregister Michael
        - Assert: Verify Daniel still in participants
        """
        # Arrange
        activity_name = "Chess Club"
        removed_email = "michael@mergington.edu"
        remaining_email = "daniel@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup?email={removed_email}"
        )

        # Assert
        assert response.status_code == 200
        
        # Verify other participant still there
        updated_participants = client.get("/activities").json()[activity_name]["participants"]
        assert removed_email not in updated_participants
        assert remaining_email in updated_participants
