# Django Trello Clone

A minimal Trello-style board app: Boards → Lists → Cards, with drag-and-drop
to move cards between lists.

## Setup

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Then open http://127.0.0.1:8000/

Optional: create an admin user to manage data via /admin/:

```bash
python manage.py createsuperuser
```

## Features

- Create boards
- Add/delete lists within a board
- Add/delete cards within a list
- Drag and drop cards between lists (and reorder within a list) — saved live via AJAX
- Django admin enabled for Board, List, Card models

## Project structure

```
config/        Django project settings/urls
boards/        App: models, views, templates
  models.py    Board, List, Card
  views.py     CRUD + the card_move AJAX endpoint
  templates/   board_list.html, board_detail.html, base.html
```

## Notes

This is intentionally minimal — no auth, no per-user boards, no API layer.
Good extension points: user accounts + per-user boards, card descriptions/labels/due dates,
list reordering via drag-and-drop, WebSocket-based live updates for collaboration.
