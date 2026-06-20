from django.contrib import admin
from django.urls import path
from boards import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.board_list, name="board_list"),
    path("board/new/", views.board_create, name="board_create"),
    path("board/<int:board_id>/", views.board_detail, name="board_detail"),
    path("board/<int:board_id>/list/new/", views.list_create, name="list_create"),
    path("list/<int:list_id>/card/new/", views.card_create, name="card_create"),
    path("card/<int:card_id>/move/", views.card_move, name="card_move"),
    path("card/<int:card_id>/delete/", views.card_delete, name="card_delete"),
    path("list/<int:list_id>/delete/", views.list_delete, name="list_delete"),
]
