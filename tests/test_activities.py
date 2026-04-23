"""
Tests for GET /activities endpoint.
"""
import pytest


class TestGetActivities:
    """Test cases for retrieving all activities."""

    def test_get_all_activities_returns_success(self, client):
        """
        Arrange: Create a test client
        Act: Make GET request to /activities
        Assert: Verify status code is 200 and response contains activities
        """
        # Arrange
        # (client fixture is already set up)
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        activities = response.json()
        assert len(activities) > 0

    def test_get_activities_returns_correct_structure(self, client):
        """
        Arrange: Create a test client
        Act: Make GET request to /activities
        Assert: Verify each activity has required fields
        """
        # Arrange
        # (client fixture is already set up)
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_name, str)
            assert "description" in activity_data
            assert "schedule" in activity_data
            assert "max_participants" in activity_data
            assert "participants" in activity_data
            assert isinstance(activity_data["participants"], list)

    def test_get_activities_includes_chess_club(self, client):
        """
        Arrange: Create a test client
        Act: Make GET request to /activities
        Assert: Verify Chess Club is in the response with correct data
        """
        # Arrange
        # (client fixture is already set up)
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        assert "Chess Club" in activities
        assert activities["Chess Club"]["description"] == "Learn strategies and compete in chess tournaments"
        assert activities["Chess Club"]["max_participants"] == 12
        assert "michael@mergington.edu" in activities["Chess Club"]["participants"]
        assert "daniel@mergington.edu" in activities["Chess Club"]["participants"]

    def test_get_activities_participant_count(self, client):
        """
        Arrange: Create a test client
        Act: Make GET request to /activities
        Assert: Verify participant counts are accurate
        """
        # Arrange
        # (client fixture is already set up)
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        # Chess Club has 2 participants and max 12, so 10 spots left
        chess_club = activities["Chess Club"]
        spots_left = chess_club["max_participants"] - len(chess_club["participants"])
        assert spots_left == 10
