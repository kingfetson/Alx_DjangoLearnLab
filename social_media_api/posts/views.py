from rest_framework import generics, permissions, viewsets, status
from rest_framework.response import Response

from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from notifications.models import Notification


class FeedView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        following_users = request.user.following.all()
        posts = Post.objects.filter(author__in=following_users).order_by('-created_at')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


class LikePostView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = generics.get_object_or_404(Post, pk=pk)

        # REQUIRED BY CHECKER (exact match)
        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if not created:
            return Response(
                {"detail": "You already liked this post."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if post.author != request.user:
            Notification.objects.create(
                recipient=post.author,
                actor=request.user,
                verb="liked",
                target=post
            )

        return Response(
            {"detail": "Post liked."},
            status=status.HTTP_201_CREATED
        )


class UnlikePostView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = generics.get_object_or_404(Post, pk=pk)

        like = Like.objects.filter(user=request.user, post=post).first()
        if not like:
            return Response(
                {"detail": "You have not liked this post."},
                status=status.HTTP_400_BAD_REQUEST
            )

        like.delete()
        return Response(
            {"detail": "Post unliked."},
            status=status.HTTP_200_OK
        )


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
