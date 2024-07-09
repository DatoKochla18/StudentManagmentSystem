from django.urls import path
from .views import CourseCreateView,CourseListView,CourseDetailView,enroll_in_course,\
    CourseDeleteView,CourseUpdateView,my_courses,complete_course,uncomplete_course,get_messages\
    ,forum_list,create_forum_post,ForumDeleteView
    

urlpatterns = [
#    path('<int:pk>/edit/',ArticleUpdateView.as_view(), name='article_edit'), # new
#path('<int:pk>/',ArticleDetailView.as_view(), name='article_detail'), # new
#path('<int:pk>/delete/',ArticleDeleteView.as_view(), name='article_delete'), # new
path('', CourseListView.as_view(), name='course_list'),
path('<int:pk>',CourseDetailView.as_view(), name='course_detail'),
path('enroll/<int:pk>', enroll_in_course, name='enroll'),

path('update/<int:pk>', CourseUpdateView.as_view(), name='update_course'),
path('complete/<int:pk>', complete_course, name='complete_course'),
path('uncomplete/<int:pk>', uncomplete_course, name='uncomplete_course'),
path('forum/<int:course_pk>/create_post/', create_forum_post, name='create_forum_post'),
path('courses/<int:course_pk>/forums/', forum_list, name='forum_list'),
path('delete/<int:pk>', CourseDeleteView.as_view(), name='delete_course'),
path('my_courses', my_courses, name='my_courses'),
path('forum/<int:pk>/delete/', ForumDeleteView.as_view(), name='forum_delete'),

path('new/', CourseCreateView.as_view(), name='course_new'), 
]
