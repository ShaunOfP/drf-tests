from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status
from forum_app.models import Answer, Question
from forum_app.api.serializers import AnswerSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class AnswerTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.question = Question.objects.create(
            title='Test Question', content='Test Content', author=self.user, category='frontend')
        self.answer = Answer.objects.create(
            content='Test Content', author=self.user, question=self.question)

        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_list_post_answer(self):
        url = reverse('answer-list-create')
        data = {
            'content': 'Content1',
            'author': self.user.id,
            'question': self.question.id
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_detail_answer(self):
        url = reverse('answer-detail', kwargs={'pk': self.answer.id})
        response = self.client.get(url)
        expected_data = AnswerSerializer(self.answer).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)
