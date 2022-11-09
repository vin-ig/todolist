import pytest

from goals.serializers import GoalSerializer


@pytest.mark.django_db
def test_goal_list(client, get_credentials, goal, user, board_participant):
	response = client.get(
		path='/goals/goal/list',
		HTTP_AUTHORIZATION=get_credentials
	)

	assert response.status_code == 200
	assert response.data == GoalSerializer().data
