import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Provide a TestClient for making requests to the FastAPI app"""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """
    Reset activities to a known state before each test.
    This ensures tests don't interfere with each other due to shared in-memory state.
    """
    # Store original state
    original_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Competitive basketball practices and games",
            "schedule": "Mondays, Wednesdays, Fridays, 4:00 PM - 6:00 PM",
            "max_participants": 15,
            "participants": ["liam@mergington.edu", "sophia@mergington.edu"]
        },
        "Swimming Club": {
            "description": "Swim training and friendly competitions",
            "schedule": "Tuesdays and Thursdays, 5:00 PM - 6:30 PM",
            "max_participants": 20,
            "participants": ["noah@mergington.edu"]
        },
        "Robotics Club": {
            "description": "Design, build, and program robots for competitions and projects",
            "schedule": "Wednesdays, 3:30 PM - 5:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu"]
        },
        "Debate Club": {
            "description": "Develop public speaking and argumentation skills",
            "schedule": "Fridays, 3:30 PM - 4:30 PM",
            "max_participants": 25,
            "participants": ["olivia@mergington.edu"]
        },
        "Art Studio": {
            "description": "Explore drawing, painting, and mixed media",
            "schedule": "Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 20,
            "participants": ["ava@mergington.edu"]
        },
        "Music Ensemble": {
            "description": "Instrumental and vocal ensemble rehearsals",
            "schedule": "Tuesdays, 4:00 PM - 5:30 PM",
            "max_participants": 30,
            "participants": ["isabella@mergington.edu"]
        },
        "Badminton": {
            "description": "Casual and competitive badminton practice and matches",
            "schedule": "Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 16,
            "participants": ["noah@mergington.edu"]
        },
        "Soccer": {
            "description": "Competitive soccer practices and matches",
            "schedule": "Mondays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 18,
            "participants": ["lucas@mergington.edu", "aiden@mergington.edu"]
        }
    }
    
    # Clear and reset activities
    activities.clear()
    activities.update(original_activities)
    
    yield
    
    # Reset after test
    activities.clear()
    activities.update(original_activities)


# Test data fixtures
@pytest.fixture
def test_email_1():
    """First test email"""
    return "test1@mergington.edu"


@pytest.fixture
def test_email_2():
    """Second test email"""
    return "test2@mergington.edu"


@pytest.fixture
def test_email_3():
    """Third test email"""
    return "test3@mergington.edu"
