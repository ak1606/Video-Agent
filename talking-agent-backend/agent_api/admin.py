from django.contrib import admin
from .models import Conversation, Message

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['session_id', 'created_at', 'updated_at']
    list_filter = ['created_at']
    search_fields = ['session_id']

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['conversation', 'message_type', 'content', 'timestamp']
    list_filter = ['message_type', 'timestamp']
    search_fields = ['content']