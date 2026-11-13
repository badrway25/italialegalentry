from django.urls import path

from community import views

app_name = "community"

urlpatterns = [
    path("", views.index, name="index"),
    path("rejoindre/", views.join, name="join"),
    path("calendrier/", views.calendar, name="calendar"),
    path("initiatives/", views.initiatives, name="initiatives"),
    path("salles/<slug:slug>/", views.room_detail, name="room"),
    path("discussions/<int:pk>/", views.discussion_detail, name="discussion"),
    path("discussions/<int:pk>/moderation/", views.discussion_moderate, name="discussion_moderate"),
    path("messages/<int:pk>/modifier/", views.post_edit, name="post_edit"),
    path("messages/<int:pk>/signaler/", views.post_report, name="post_report"),
    path("messages/<int:pk>/moderation/", views.post_moderate, name="post_moderate"),
]
