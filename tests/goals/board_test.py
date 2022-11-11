import pytest

from goals.models import Goal, Board
from goals.serializers import BoardSerializer, BoardListSerializer
from tests.factories import GoalFactory, BoardFactory, BoardParticipantFactory


@pytest.mark.django_db
def test_board_create(client, get_credentials, user):
	data = {
		'title': 'title',
		'user': user.id,
	}

	response = client.post(
		path='/goals/board/create',
		HTTP_AUTHORIZATION=get_credentials,
		data=data,
		content_type='application/json'
	)

	assert response.status_code == 201
	assert response.data['title'] == data['title']


@pytest.mark.django_db
def test_board_list(client, get_credentials, board_participant):
	boards = [board_participant.board]
	boards.extend(BoardFactory.create_batch(10))
	for board in boards[1:]:
		BoardParticipantFactory.create(user=board_participant.user, board=board)
	boards.sort(key=lambda x: x.title)

	response = client.get(
		path='/goals/board/list',
		HTTP_AUTHORIZATION=get_credentials
	)

	assert response.status_code == 200
	assert response.data == BoardListSerializer(boards, many=True).data


@pytest.mark.django_db
def test_board_retrieve(client, get_credentials, board, board_participant):
	response = client.get(
		path=f'/goals/board/{board.id}',
		HTTP_AUTHORIZATION=get_credentials
	)

	assert response.status_code == 200
	assert response.data == BoardSerializer(board).data


@pytest.mark.django_db
def test_board_update(client, get_credentials, board, board_participant):
	new_title = 'updated_title'

	response = client.patch(
		path=f'/goals/board/{board.id}',
		HTTP_AUTHORIZATION=get_credentials,
		data={'title': new_title},
		content_type='application/json'
	)

	assert response.status_code == 200
	assert response.data.get('title') == new_title


@pytest.mark.django_db
def test_board_delete(client, get_credentials, board, board_participant):

	response = client.delete(
		path=f'/goals/board/{board.id}',
		HTTP_AUTHORIZATION=get_credentials,
	)

	assert response.status_code == 204
	assert response.data is None

"""
E = [
	OrderedDict([('id', 1), ('created', '2022-11-11T18:14:44.159101Z'), ('updated', '2022-11-11T18:14:44.159101Z'), ('title', 'Jessica Curtis'), ('is_deleted', False)]), 
	OrderedDict([('id', 2), ('created', '2022-11-11T18:14:44.169103Z'), ('updated', '2022-11-11T18:14:44.169103Z'), ('title', 'Noah Jones'), ('is_deleted', False)]),
	OrderedDict([('id', 3), ('created', '2022-11-11T18:14:44.171101Z'), ('updated', '2022-11-11T18:14:44.171101Z'), ('title', 'George Hamilton'), ('is_deleted', False)])
]
A = [
	OrderedDict([('id', 3), ('created', '2022-11-11T18:14:44.171101Z'), ('updated', '2022-11-11T18:14:44.171101Z'), ('title', 'George Hamilton'), ('is_deleted', False)]),
	             ('participants', [OrderedDict([('id', 3), ('role', <Role.owner: 1>), ('user', 'Mark Newman'), ('created', '2022-11-11T18:14:44.174106Z'), ('updated', '2022-11-11T18:14:44.174106Z'), ('board', 3)])]),
	OrderedDict([('id', 1), ('participants', [OrderedDict([('id', 1), ('role', <Role.owner: 1>), ('user', 'Mark Newman'), ('created', '2022-11-11T18:14:44.163104Z'), ('updated', '2022-11-11T18:14:44.163104Z'), ('board', 1)])]), ('created', '2022-11-11T18:14:44.159101Z'), ('updated', '2022-11-11T18:14:44.159101Z'), ('title', 'Jessica Curtis'), ('is_deleted', False)]), 
	OrderedDict([('id', 2), ('participants', [OrderedDict([('id', 2), ('role', <Role.owner: 1>), ('user', 'Mark Newman'), ('created', '2022-11-11T18:14:44.173101Z'), ('updated', '2022-11-11T18:14:44.173101Z'), ('board', 2)])]), ('created', '2022-11-11T18:14:44.169103Z'), ('updated', '2022-11-11T18:14:44.169103Z'), ('title', 'Noah Jones'), ('is_deleted', False)])
]"""
