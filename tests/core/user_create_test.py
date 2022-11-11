import pytest


@pytest.mark.django_db
def test_user_create(client, django_user_model):
	data = {
		'username': 'Tester',
		'password': 'Password8956',
		'password_repeat': 'Password8956',
	}

	response = client.post(
		path='/core/signup',
		data=data,
		content_type='application/json'
	)

	user = django_user_model.objects.get(id=1)

	expected_response = {
		'id': user.id,
		'username': user.username,
		'password': user.password,
		'first_name': user.first_name,
		'last_name': user.last_name,
		'email': user.email
	}

	assert response.status_code == 201
	assert response.data == expected_response
