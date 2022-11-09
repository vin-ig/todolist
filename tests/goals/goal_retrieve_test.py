import base64

import pytest
from django.contrib.auth import authenticate

from core.models import User


@pytest.mark.django_db
def test_goal_retrieve(client, goal):
	expected_response = {
		'id': goal.id,
		'title': goal.title,
		'description': goal.description,
		'user': goal.user,
		'category': goal.category,
		'is_deleted': goal.is_deleted,
		'status': goal.status,
		'priority': goal.priority,
		'due_date': goal.due_date,
	}

	# user = User.objects.create_user(
	# 	username='Test_user_2',
	# 	password='Password8956'
	# )
	# goal.user = user
	# goal.save()
	#
	# print(goal.id, goal.user)
	# print(user.username, user.password)

	# credentials = base64.b64encode(b'Test_user_2:Password8956').decode('utf-8')
	# goal.user.set_password(goal.user.password)
	# goal.user.save()
	# goal.save()
	#
	credentials = base64.b64encode(bytes(f'{goal.user.username}:{goal.user.password}', 'utf-8')).decode('utf-8')
	response = client.get(
		f'/goals/goal/list',
		HTTP_AUTHORIZATION='Basic ' + credentials
	)

	# print(User.objects.all())
	# print(goal.category)
	# print(goal.category.user)
	# print(goal.category.board.categories)
	print(response.data)

	assert response.status_code == 200
	assert response.data == expected_response
