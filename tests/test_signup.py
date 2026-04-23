"""
Tests for POST /activities/{activity_name}/signup endpoint.
"""
import pytest


class TestSignupForActivity:
    """Test cases for signing up for an activity."""

    def test_signup_new_student_succeeds(self, client):
        """
        Arrange: Create a test client and prepare new student email
        Act: Make POST request to signup endpoint
        Assert: Verify status code is 200 and success message returned
        """
        # Arrange
        activity_name = "Chess Club"
        new_email = "newstudent@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": new_email}
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert new_email in data["message"]
        assert activity_name in data["message"]

    def test_signup_adds_participant_to_activity(self, client):
        """
        Arrange: Create a test client and prepare new student email
        Act: Make POST request to signup, then GET activities
        Assert: Verify new student added to participants list
        """
        # Arrange
        activity_name = "Chess Club"
        new_email = "newstudent@mergington.edu"
        
        # Act
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": new_email}
        )
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        assert new_email in activities[activity_name]["participants"]

    def test_signup_nonexistent_activity_returns_404(self, client):
        """
        Arrange: Create a test client with invalid activity name
        Act: Make POST request to signup for non-existent activity
        Assert: Verify status code is 404 and error message returned
        """
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "student@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()

    def test_signup_duplicate_student_returns_400(self, client):
        """
        Arrange: Create a test client with already-registered student
        Act: Make POST request to signup with duplicate email
        Assert: Verify status code is 400 and duplicate error returned
        """
        # Arrange
        activity_name = "Chess Club"
        # michael@mergington.edu is already in Chess Club
        duplicate_email = "michael@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": duplicate_email}
        )
        
        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "already signed up" in data["detail"].lower()

    def test_signup_multiple_students_different_activities(self, client):
        """
        Arrange: Create a test client and prepare multiple signups
        Act: Sign up new students for different activities
        Assert: Verify all signups succeed and participants are added
        """
        # Arrange
        signups = [
            ("Chess Club", "alice@mergington.edu"),
            ("Programming Class", "bob@mergington.edu"),
            ("Gym Class", "charlie@mergington.edu"),
        ]
        
        # Act
        for activity_name, email in signups:
            response = client.post(
                f"/activities/{activity_name}/signup",
                params={"email": email}
            )
            assert response.status_code == 200
        
        # Assert
        response = client.get("/activities")
        activities = response.json()
        for activity_name, email in signups:
            assert email in activities[activity_name]["participants"]
