# serializers.py
from rest_framework import serializers
from .models import TodoItem, TodoStatus

class TodoItemSerializer(serializers.ModelSerializer):
    """
    Serializer for TodoItem model
    """
    class Meta:
        model = TodoItem
        fields = [
            'id', 'title', 'description', 'due_date', 
            'tag', 'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate_title(self, value):
        """
        Additional title validation
        """
        if len(value) < 1 or len(value) > 100:
            raise serializers.ValidationError(
                "Title must be between 1 and 100 characters"
            )
        return value

    def validate_description(self, value):
        """
        Additional description validation
        """
        if len(value) < 1 or len(value) > 1000:
            raise serializers.ValidationError(
                "Description must be between 1 and 1000 characters"
            )
        return value

# views.py
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import TodoItem, TodoStatus
from .serializers import TodoItemSerializer

class TodoItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet for TodoItem with full CRUD operations
    """
    queryset = TodoItem.objects.all()
    serializer_class = TodoItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Custom queryset filtering
        """
        queryset = super().get_queryset()
        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)
        return queryset

    @action(detail=True, methods=['patch'], url_path='change-status')
    def change_status(self, request, pk=None):
        """
        Custom action to change task status
        """
        todo_item = self.get_object()
        status = request.data.get('status')

        if status not in dict(TodoStatus.choices):
            return Response(
                {'error': 'Invalid status'},
                status=400
            )

        todo_item.status = status
        todo_item.save()

        serializer = self.get_serializer(todo_item)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='overdue')
    def overdue_tasks(self, request):
        """
        List all overdue tasks
        """
        overdue_tasks = TodoItem.objects.filter(
            status=TodoStatus.OVERDUE
        )
        serializer = self.get_serializer(overdue_tasks, many=True)
        return Response(serializer.data)