# import pytest
#
#
# @pytest.fixture
# @pytest.mark.django_db
# def user_token(client, django_user_model):
# 	username = "User from fixture"
# 	password = "Password8956"
#
# 	django_user_model.objects.create_user(username=username, password=password)
#
# 	response = client.post(
# 		"/core/signup",
# 		data={"username": username, "password": password, "password_repeat": password},
# 		content_type="application/json"
# 	)
# 	print(response.data)
# 	return response.data["token"]
