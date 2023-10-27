from django.urls import path
from .views import IssueListView, IssueDetail, LabelListCreateView, LabelRetrieveUpdateDestroyView, CommentListView, CommentDetailView, IssueAssignView

urlpatterns = [
    path('issues/', IssueListView.as_view(), name='api_issue_list'),
    path('issues/<int:pk>/', IssueDetail.as_view(), name='api_issue_detail'),
    path('labels/', LabelListCreateView.as_view(), name='label-list-create'),
    path('labels/<int:pk>/', LabelRetrieveUpdateDestroyView.as_view(), name='label-retrieve-update-destroy'),
    path('issues/<int:issue_id>/comments/', CommentListView.as_view(), name='comment-list'),
    path('issues/<int:issue_id>/comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
    path('issues/<int:pk>/assign/', IssueAssignView.as_view(), name='issue-assign'),
]
