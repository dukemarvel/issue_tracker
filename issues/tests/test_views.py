from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from ..models import Issue, Label, Comment

class UserRegistrationTestCase(APITestCase):
    
    def test_valid_user_registration(self):
        data = {
            'username': 'testuser',
            'password': '@password1234',
            'email': 'testuser@example.com'
        }
        response = self.client.post("/auth/users/", data)
        print(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)


class IssueTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.force_authenticate(user=self.user)
        self.issue = Issue.objects.create(title="Test Issue", description="Description for test issue", created_by=self.user)

    def test_create_issue(self):
        data = {'title': 'Another Test Issue', 'description': 'Another description'}
        response = self.client.post("/api/issues/", data)
        print(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Issue.objects.count(), 2)

    def test_list_issues(self):
        response = self.client.get("/api/issues/")
        print(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class CommentTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.force_authenticate(user=self.user)
        self.issue = Issue.objects.create(title="Test Issue", description="Description for test issue", created_by=self.user)
        self.comment = Comment.objects.create(issue=self.issue, author=self.user, text="Test Comment")

    def test_create_comment(self):
        data = {'text': 'Another Test Comment'}
        response = self.client.post(f"/api/issues/{self.issue.id}/comments/", data)
        print(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 2)

    def test_list_comments(self):
        response = self.client.get(f"/api/issues/{self.issue.id}/comments/")
        print(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class IssueDetailTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.force_authenticate(user=self.user)
        self.issue = Issue.objects.create(title="Test Issue", description="Description for test issue", created_by=self.user)

    def test_retrieve_issue(self):
        response = self.client.get(f"/api/issues/{self.issue.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_issue(self):
        data = {'title': 'Updated Title', 'description': 'Updated description'}
        response = self.client.put(f"/api/issues/{self.issue.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.issue.refresh_from_db()
        self.assertEqual(self.issue.title, 'Updated Title')

    def test_partial_update_issue(self):
        data = {'title': 'Updated Title'}
        response = self.client.patch(f"/api/issues/{self.issue.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.issue.refresh_from_db()
        self.assertEqual(self.issue.title, 'Updated Title')

    def test_delete_issue(self):
        response = self.client.delete(f"/api/issues/{self.issue.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)



class LabelTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.force_authenticate(user=self.user)
        self.label = Label.objects.create(name='Bug')

    def test_list_labels(self):
        response = self.client.get("/api/labels/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_label(self):
        data = {'name': 'Bug'}
        response = self.client.post("/api/labels/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    

class CommentDetailTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.force_authenticate(user=self.user)
        self.issue = Issue.objects.create(title="Test Issue", description="Description for test issue", created_by=self.user)
        self.comment = Comment.objects.create(issue=self.issue, author=self.user, text="Test Comment")

    def test_retrieve_comment(self):
        response = self.client.get(f"/api/issues/{self.issue.id}/comments/{self.comment.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    


class IssueAssignTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.force_authenticate(user=self.user)
        self.issue = Issue.objects.create(title="Test Issue", description="Description for test issue", created_by=self.user)
        self.user2 = User.objects.create_user(username='testuser2', password='@password1234')

    def test_assign_user_to_issue(self):
        data = {'assigned_to': self.user2.id}
        response = self.client.patch(f"/api/issues/{self.issue.id}/assign/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.issue.refresh_from_db()  # Refresh the instance from the database to get updated data
        self.assertEqual(self.issue.assigned_to, self.user2)
