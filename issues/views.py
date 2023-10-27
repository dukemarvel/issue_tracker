from rest_framework import generics, status
from rest_framework.response import Response
from .models import Issue, Label, Comment
from .serializers import IssueSerializer, LabelSerializer, CommentSerializer, IssueAssignSerializer
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .filters import IssueFilter
from .permissions import IsCommentAuthorOrReadOnly
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User



class IssueListView(generics.ListCreateAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = IssueFilter
    ordering_fields = ['title', 'created_at', 'assigned_to__username']
    ordering = ['created_at']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class IssueDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer

    def update(self, request, *args, **kwargs):
        issue = self.get_object()
        serializer = self.serializer_class(issue, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LabelListCreateView(generics.ListCreateAPIView):
    queryset = Label.objects.all()
    serializer_class = LabelSerializer
    permission_classes = [IsAuthenticated]

class LabelRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Label.objects.all()
    serializer_class = LabelSerializer
    permission_classes = [IsAuthenticated]

class CommentListView(generics.ListCreateAPIView):
    def get_queryset(self):
        return Comment.objects.filter(issue=self.kwargs['issue_id'])
    
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsCommentAuthorOrReadOnly]
    lookup_field = 'issue_id'

    def perform_create(self, serializer):
        issue = Issue.objects.get(pk=self.kwargs['issue_id'])
        serializer.save(issue=issue, author=self.request.user)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsCommentAuthorOrReadOnly]



class IssueAssignView(generics.UpdateAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueAssignSerializer

    def update(self, request, *args, **kwargs):
        issue = self.get_object()
        user_id = request.data.get('assigned_to')
        
        # Fetch the user instance based on the provided ID
        user_to_assign = get_object_or_404(User, id=user_id)
        
        issue.assigned_to = user_to_assign
        issue.save()
        
        return Response({'message': 'Issue assigned successfully'}, status=status.HTTP_200_OK)
    
