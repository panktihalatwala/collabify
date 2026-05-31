from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('', views.inbox, name='inbox'),
    path('new/', views.select_campaign_to_message, name='select_campaign'),
    path('<int:room_id>/', views.chat_room, name='chat'),
    path('start/<int:user_id>/', views.start_chat, name='start_chat'),
    path('<int:room_id>/send/', views.send_message_http, name='send_message'),
]