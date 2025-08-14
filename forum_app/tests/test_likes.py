from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from forum_app.models import Like, Question
from forum_app.api.serializers import LikeSerializer
from rest_framework.authtoken.models import Token


class LikeTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.question = Question.objects.create(
            title='Test Question', content='Test Content', author=self.user, category='frontend')
        self.like = Like.objects.create(
            user=self.user, question=self.question)

        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_get_like(self):
        url = reverse('like-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_post_like(self):
        url = reverse('like-list')
        data = {
            'user': self.user.id,
            'question': self.question.id
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_detail_like(self):
        url = reverse('like-detail', kwargs={'pk': self.like.id})
        response = self.client.get(url)
        expected_data = LikeSerializer(self.like).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)
