from fastapi.testclient import TestClient

from src.app import activities, app

client = TestClient(app)


def test_signup_for_activity_adds_participant():
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    original_participants = activities[activity_name]["participants"].copy()

    try:
        # Arrange
        assert email not in activities[activity_name]["participants"]

        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={email}")

        # Assert
        assert response.status_code == 200
        assert response.json() == {"message": f"Signed up {email} for {activity_name}"}
        assert email in activities[activity_name]["participants"]
    finally:
        activities[activity_name]["participants"] = original_participants


def test_signup_for_activity_rejects_duplicate_email():
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    original_participants = activities[activity_name]["participants"].copy()

    try:
        # Arrange
        assert email in activities[activity_name]["participants"]

        # Act
        response = client.post(f"/activities/{activity_name}/signup?email={email}")

        # Assert
        assert response.status_code == 400
        assert response.json()["detail"] == "Student already signed up for this activity"
    finally:
        activities[activity_name]["participants"] = original_participants


def test_unregister_participant_removes_email():
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    original_participants = activities[activity_name]["participants"].copy()
    activities[activity_name]["participants"].append(email)

    try:
        # Arrange
        assert email in activities[activity_name]["participants"]

        # Act
        response = client.delete(f"/activities/{activity_name}/participants?email={email}")

        # Assert
        assert response.status_code == 200
        assert response.json() == {"message": f"Unregistered {email} from {activity_name}"}
        assert email not in activities[activity_name]["participants"]
    finally:
        activities[activity_name]["participants"] = original_participants
