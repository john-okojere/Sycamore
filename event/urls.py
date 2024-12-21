from django.urls import path
from . import views


urlpatterns = [
    path('coming_soon', views.coming_soon, name="coming_soon"),
    path('', views.event_list_view, name='event_list'),
    path('create_event/', views.create_event_view, name='create_event'),
    path('create_event_list/<int:event_id>/', views.create_event_list_view, name='create_event_list'),
    path('event_details/<int:event_id>/', views.event_details_view, name='event_details'),

    path('list/', views.registrant_list_view, name='registrant_list_view'),
    path('list/<int:list_id>/', views.list_view, name='list_view'),
    path('list/<int:list_id>/scan', views.scan, name='list_scan'),
    path('list/<int:list_id>/getscan', views.getscan, name='list_getscan'),
    path('add_attendee/<int:list_id>/', views.add_attendee_view, name='add_attendee'),
    path('list/<int:list_id>/', views.list_view, name='list_view'),
    path('user_add_attendee/<int:list_id>/', views.add_user_attendee_view, name='user_add_attendee'),
    path('user_list/<int:list_id>/', views.user_list_view, name='user_list_view'),

    path('event-search/', views.event_search, name='event_search'),
    path('create-follow-up/', views.create_follow_up, name='create_follow_up'),
    path('follow-up/', views.follow_up_system, name='follow_up_system'),

    path('view_comments/', views.view_comments, name='view_comments'),
    path('add_comment/', views.add_comment, name='add_comment'),
    path('attendee_bio/<int:attendee_id>/', views.attendee_bio, name='attendee_bio'),
    path('soul_delete/<int:attendee_id>/', views.soul_delete, name='soul_delete'),
    path('follow_ups/<int:pk>', views.follow_up_view, name='follow_up_view'),
    path('follow_ups/delete/<int:pk>/', views.follow_up_delete, name='follow_up_delete'),
    path('get_persons_not_in_follow_up/', views.get_persons_not_in_follow_up, name='get_persons_not_in_follow_up'),
path('add_single_person/<int:pk>', views.add_single_person, name='add_single_person'),
]
