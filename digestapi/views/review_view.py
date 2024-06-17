from rest_framework import viewsets, status, serializers, permissions
from rest_framework.response import Response
from digestapi.models import BookReview, Book
from django.contrib.auth.models import User

class ReviewSerializer(serializers.ModelSerializer):
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = BookReview
        fields = ['id', 'book', 'user', 'rating', 'comment', 'date', 'is_owner']
        read_only_fields = ['user']

    def get_is_owner(self, obj):
        # Check if the user is the owner of the review
        return self.context['request'].user == obj.user


class ReviewViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    # Get all reviews
    def list(self, request):
        reviews = BookReview.objects.all()

        # Serialize the objects, and pass request to determine owner
        serializer = ReviewSerializer(
            reviews, 
            many=True, 
            context={'request': request}
        )

        # Return the serialized data with 200 status code
        return Response(serializer.data, status=status.HTTP_200_OK)


    def create(self, request):
        book_id = request.data['bookId']
        book_instance = Book.objects.get(pk=book_id)
        # Create a new instance of a review and assign property
        # values from the request payload using `request.data`
        review = BookReview()
        review.user = request.user
        review.book = book_instance
        review.rating = request.data.get('rating')
        review.comment = request.data.get('comment')
        review.date = request.data.get('date') or None

        # Save the review
        review.save()

        try:
            # Serialize the objects, and pass request as context
            serializer = ReviewSerializer(review, context={'request': request})
            # Return the serialized data with 201 status code
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as ex:
            return Response(None, status=status.HTTP_400_BAD_REQUEST)



    # def retrieve(self, request, pk=None):
    #     try:
    #         # Get the requested review

    #         # Serialize the object (make sure to pass the request as context)

    #         # Return the review with 200 status code

    #     except Review.DoesNotExist:
    #         return Response(status=status.HTTP_404_NOT_FOUND)



    def destroy(self, request, pk=None):
        try:
            # Get the requested review
            review = BookReview.objects.get(pk=pk)

            # Check if the user has permission to delete
            # Will return 403 if authenticated user is not author
            if review.user.id != request.user.id:
                return Response(status=status.HTTP_403_FORBIDDEN)

            # Delete the review
            review.delete()

            # Return success but no body
            return Response(status=status.HTTP_204_NO_CONTENT)

        except BookReview.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)