"""
Tests for DELETE /activities/{activity_name}/unregister endpoint.
"""
import pytest


class TestUnregisterFromActivity:
    """Test cases for unregistering from an activity."""

    def test_unregister_existing_participant_succeeds(self, client):
        """
        Arrange: Create a test client with existing participant
        Act: Make DELETE request to unregister
        Assert: Verify status code is 200 and success message returned
        """
        # Arrange
        activity_name = "Chess Club"
        # michael@mergington.edu is already in Chess Club
        email = "michael@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]

    def test_unregister_removes_participant_from_activity(self, client):
        """
        Arrange: Create a test client and identify existing participant
        Act: Make DELETE request, then GET activities
        Assert: Verify participant removed from participants list
        """
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"
        
        # Get initial participant count
        response = client.get("/activities")
        initial_participants = len(response.json()[activity_name]["participants"])
        
        # Act
        client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        assert email not in activities[activity_name]["participants"]
        assert len(activities[activity_name]["participants"]) == initial_participants - 1

    def test_unregister_nonexistent_activity_returns_404(self, client):
        """
        Arrange: Create a test client with invalid activity name
        Act: Make DELETE request for non-existent activity
        Assert: Verify status code is 404 and error message returned
        """
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "student@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()

    def test_unregister_nonexistent_participant_returns_404(self, client):
        """
        Arrange: Create a test client with non-registered student
        Act: Make DELETE request for student not in activity
        Assert: Verify status code is 404 and error message returned
        """
        # Arrange
        activity_name = "Chess Club"
        # This student is not registered for Chess Club
        email = "notregistered@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()

    def test_unregister_multiple_participants_sequentially(self, client):
        """
        Arrange: Create a test client with activity containing participants
        Act: Unregister multiple participants one by one
        Assert: Verify each removal succeeds and final state is correct
        """
        # Arrange
        activity_name = "Chess Club"
        # Chess Club has michael@mergington.edu and daniel@mergington.edu
        emails_to_remove = ["michael@mergington.edu", "daniel@mergington.edu"]
        
        # Act & Assert
        for email in emails_to_remove:
            response = client.delete(
                f"/activities/{activity_name}/unregister",
                params={"email": email}
            )
            assert response.status_code == 200
        
        # Verify all removed
        response = client.get("/activities")
        activities = response.json()
        assert len(activities[activity_name]["participants"]) == 0

    def test_unregister_after_signup(self, client):
        """
        Arrange: Create a test client and sign up new student
        Act: Sign up new student, then unregister the same student
        Assert: Verify student added then removed successfully
        """
        # Arrange
        activity_name = "Programming Class"
        new_email = "newstudent@mergington.edu"
        
        # Act - Sign up
        signup_response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": new_email}
        )
        assert signup_response.status_code == 200
        
        # Verify added
        response = client.get("/activities")
        assert new_email in response.json()[activity_name]["participants"]
        initial_count = len(response.json()[activity_name]["participants"])
        
        # Act - Unregister
        unregister_response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": new_email}
        )
        
        # Assert
        assert unregister_response.status_code == 200
        response = client.get("/activities")
        assert new_email not in response.json()[activity_name]["participants"]
        assert len(response.json()[activity_name]["participants"]) == initial_count - 1
