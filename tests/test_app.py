"""
Tests for the Mergington High School Activities API

Tests cover all three endpoints:
- GET /activities
- POST /activities/{activity_name}/signup
- POST /activities/{activity_name}/drop
"""

import pytest


class TestGetActivities:
    """Tests for GET /activities endpoint"""

    def test_get_activities_returns_200(self, client):
        """Test that GET /activities returns 200 status code"""
        response = client.get("/activities")
        assert response.status_code == 200

    def test_get_activities_returns_all_activities(self, client):
        """Test that response includes all 11 activities"""
        response = client.get("/activities")
        activities = response.json()
        assert len(activities) == 11
        assert "Chess Club" in activities
        assert "Soccer" in activities

    def test_get_activities_has_correct_structure(self, client):
        """Test that each activity has required fields"""
        response = client.get("/activities")
        activities = response.json()
        
        for activity_name, activity in activities.items():
            assert "description" in activity
            assert "schedule" in activity
            assert "max_participants" in activity
            assert "participants" in activity
            assert isinstance(activity["participants"], list)

    def test_get_activities_shows_initial_participants(self, client):
        """Test that initial participant lists are correct"""
        response = client.get("/activities")
        activities = response.json()
        
        assert "michael@mergington.edu" in activities["Chess Club"]["participants"]
        assert "emma@mergington.edu" in activities["Programming Class"]["participants"]
        assert len(activities["Chess Club"]["participants"]) == 2

    def test_get_activities_reflects_signup(self, client, test_email_1):
        """Test that participant list updates after signup"""
        client.post(f"/activities/Chess%20Club/signup?email={test_email_1}")
        response = client.get("/activities")
        activities = response.json()
        
        assert test_email_1 in activities["Chess Club"]["participants"]
        assert len(activities["Chess Club"]["participants"]) == 3

    def test_get_activities_reflects_drop(self, client):
        """Test that participant list updates after drop"""
        response = client.get("/activities")
        initial_count = len(response.json()["Chess Club"]["participants"])
        
        client.post("/activities/Chess%20Club/drop?email=michael@mergington.edu")
        response = client.get("/activities")
        activities = response.json()
        
        assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]
        assert len(activities["Chess Club"]["participants"]) == initial_count - 1


class TestSignup:
    """Tests for POST /activities/{activity_name}/signup endpoint"""

    def test_signup_successful(self, client, test_email_1):
        """Test successful signup returns correct message and status code"""
        response = client.post(f"/activities/Chess%20Club/signup?email={test_email_1}")
        assert response.status_code == 200
        assert "Signed up" in response.json()["message"]
        assert test_email_1 in response.json()["message"]
        assert "Chess Club" in response.json()["message"]

    def test_signup_adds_participant(self, client, test_email_1):
        """Test that signup actually adds student to participants list"""
        client.post(f"/activities/Chess%20Club/signup?email={test_email_1}")
        response = client.get("/activities")
        assert test_email_1 in response.json()["Chess Club"]["participants"]

    def test_signup_duplicate_fails(self, client):
        """Test that duplicate signup fails with 400 error"""
        response = client.post("/activities/Chess%20Club/signup?email=michael@mergington.edu")
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]

    def test_signup_nonexistent_activity_fails(self, client, test_email_1):
        """Test that signup to non-existent activity fails with 404"""
        response = client.post(f"/activities/Nonexistent%20Club/signup?email={test_email_1}")
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_signup_multiple_students_same_activity(self, client, test_email_1, test_email_2):
        """Test that multiple students can sign up to same activity"""
        client.post(f"/activities/Chess%20Club/signup?email={test_email_1}")
        client.post(f"/activities/Chess%20Club/signup?email={test_email_2}")
        
        response = client.get("/activities")
        participants = response.json()["Chess Club"]["participants"]
        
        assert test_email_1 in participants
        assert test_email_2 in participants
        assert len(participants) == 4  # 2 original + 2 new

    def test_signup_persists_across_requests(self, client, test_email_1):
        """Test that signup persists in subsequent GET requests"""
        client.post(f"/activities/Chess%20Club/signup?email={test_email_1}")
        
        # Multiple subsequent requests should show the signup
        for _ in range(3):
            response = client.get("/activities")
            assert test_email_1 in response.json()["Chess Club"]["participants"]

    def test_signup_special_characters_in_activity_name(self, client, test_email_1):
        """Test signup with URL-encoded activity name containing spaces"""
        response = client.post(f"/activities/Programming%20Class/signup?email={test_email_1}")
        assert response.status_code == 200
        assert test_email_1 in response.json()["message"]

    def test_signup_different_activities(self, client, test_email_1):
        """Test signing up for multiple different activities"""
        client.post(f"/activities/Chess%20Club/signup?email={test_email_1}")
        client.post(f"/activities/Programming%20Class/signup?email={test_email_1}")
        
        response = client.get("/activities")
        assert test_email_1 in response.json()["Chess Club"]["participants"]
        assert test_email_1 in response.json()["Programming Class"]["participants"]


class TestDrop:
    """Tests for POST /activities/{activity_name}/drop endpoint"""

    def test_drop_successful(self, client, test_email_1):
        """Test successful drop returns correct message and status code"""
        client.post(f"/activities/Chess%20Club/signup?email={test_email_1}")
        response = client.post(f"/activities/Chess%20Club/drop?email={test_email_1}")
        
        assert response.status_code == 200
        assert "Dropped" in response.json()["message"]
        assert test_email_1 in response.json()["message"]
        assert "Chess Club" in response.json()["message"]

    def test_drop_removes_participant(self, client, test_email_1):
        """Test that drop actually removes student from participants list"""
        client.post(f"/activities/Chess%20Club/signup?email={test_email_1}")
        client.post(f"/activities/Chess%20Club/drop?email={test_email_1}")
        
        response = client.get("/activities")
        assert test_email_1 not in response.json()["Chess Club"]["participants"]

    def test_drop_nonregistered_fails(self, client, test_email_1):
        """Test that dropping when not registered fails with 400 error"""
        response = client.post(f"/activities/Chess%20Club/drop?email={test_email_1}")
        assert response.status_code == 400
        assert "not signed up" in response.json()["detail"]

    def test_drop_nonexistent_activity_fails(self, client, test_email_1):
        """Test that drop from non-existent activity fails with 404"""
        response = client.post(f"/activities/Nonexistent%20Club/drop?email={test_email_1}")
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_drop_persists_across_requests(self, client, test_email_1):
        """Test that drop persists in subsequent GET requests"""
        client.post(f"/activities/Chess%20Club/signup?email={test_email_1}")
        client.post(f"/activities/Chess%20Club/drop?email={test_email_1}")
        
        # Multiple subsequent requests should show the drop
        for _ in range(3):
            response = client.get("/activities")
            assert test_email_1 not in response.json()["Chess Club"]["participants"]

    def test_drop_multiple_students_independent(self, client, test_email_1, test_email_2):
        """Test that dropping one student doesn't affect others"""
        client.post(f"/activities/Chess%20Club/signup?email={test_email_1}")
        client.post(f"/activities/Chess%20Club/signup?email={test_email_2}")
        client.post(f"/activities/Chess%20Club/drop?email={test_email_1}")
        
        response = client.get("/activities")
        participants = response.json()["Chess Club"]["participants"]
        
        assert test_email_1 not in participants
        assert test_email_2 in participants

    def test_drop_from_original_participant(self, client):
        """Test dropping an original participant"""
        response = client.post("/activities/Chess%20Club/drop?email=michael@mergington.edu")
        assert response.status_code == 200
        
        activities_response = client.get("/activities")
        assert "michael@mergington.edu" not in activities_response.json()["Chess Club"]["participants"]


class TestIntegration:
    """Integration tests combining multiple operations"""

    def test_signup_drop_signup_cycle(self, client, test_email_1):
        """Test signup -> drop -> signup workflow succeeds"""
        # First signup
        response1 = client.post(f"/activities/Chess%20Club/signup?email={test_email_1}")
        assert response1.status_code == 200
        
        # Drop
        response2 = client.post(f"/activities/Chess%20Club/drop?email={test_email_1}")
        assert response2.status_code == 200
        
        # Second signup should succeed (not duplicate)
        response3 = client.post(f"/activities/Chess%20Club/signup?email={test_email_1}")
        assert response3.status_code == 200

    def test_signup_drop_verify_count_restored(self, client, test_email_1):
        """Test that participant count returns to original after signup then drop"""
        response = client.get("/activities")
        initial_count = len(response.json()["Chess Club"]["participants"])
        
        client.post(f"/activities/Chess%20Club/signup?email={test_email_1}")
        response = client.get("/activities")
        after_signup_count = len(response.json()["Chess Club"]["participants"])
        assert after_signup_count == initial_count + 1
        
        client.post(f"/activities/Chess%20Club/drop?email={test_email_1}")
        response = client.get("/activities")
        final_count = len(response.json()["Chess Club"]["participants"])
        assert final_count == initial_count

    def test_multiple_operations_data_consistency(self, client, test_email_1, test_email_2, test_email_3):
        """Test data consistency across multiple signup/drop operations"""
        # Multiple signups
        client.post(f"/activities/Soccer/signup?email={test_email_1}")
        client.post(f"/activities/Soccer/signup?email={test_email_2}")
        client.post(f"/activities/Soccer/signup?email={test_email_3}")
        
        response = client.get("/activities")
        assert len(response.json()["Soccer"]["participants"]) == 5  # 2 original + 3 new
        
        # Some drops
        client.post(f"/activities/Soccer/drop?email={test_email_1}")
        client.post(f"/activities/Soccer/drop?email={test_email_3}")
        
        response = client.get("/activities")
        participants = response.json()["Soccer"]["participants"]
        assert len(participants) == 3  # 2 original + 1 (test_email_2)
        assert test_email_1 not in participants
        assert test_email_2 in participants
        assert test_email_3 not in participants

    def test_cross_activity_operations(self, client, test_email_1):
        """Test that operations on different activities don't interfere"""
        client.post(f"/activities/Chess%20Club/signup?email={test_email_1}")
        client.post(f"/activities/Programming%20Class/signup?email={test_email_1}")
        client.post(f"/activities/Chess%20Club/drop?email={test_email_1}")
        
        response = client.get("/activities")
        activities = response.json()
        
        assert test_email_1 not in activities["Chess Club"]["participants"]
        assert test_email_1 in activities["Programming Class"]["participants"]
