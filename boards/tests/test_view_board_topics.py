from django.test import TestCase
from django.urls import resolve, reverse
from ..models import Board
from ..views import board_topics
from boards import views
from ..views import TopicListView


class BoardTopicsTests(TestCase):
    def setUp(self):
        Board.objects.create(id=1, name='Django', description='Django board.')

    def test_board_topics_view_success_status_code(self):
        url = reverse('board_topics', kwargs={'board_id': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_board_topics_view_not_found_status_code(self):
        url = reverse('board_topics', kwargs={'board_id': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_board_topics_url_resolves_board_topics_view(self):
        view = resolve('/boards/1/')
        self.assertEquals(view.func.view_class, TopicListView)