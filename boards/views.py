import json

from django.http import JsonResponse, HttpResponseNotAllowed
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .models import Board, List, Card


def board_list(request):
    boards = Board.objects.all().order_by("-created_at")
    return render(request, "boards/board_list.html", {"boards": boards})


@require_POST
def board_create(request):
    name = request.POST.get("name", "").strip()
    if name:
        board = Board.objects.create(name=name)
        return redirect("board_detail", board_id=board.id)
    return redirect("board_list")


def board_detail(request, board_id):
    board = get_object_or_404(Board, id=board_id)
    lists = board.lists.prefetch_related("cards").all()
    return render(request, "boards/board_detail.html", {"board": board, "lists": lists})


@require_POST
def list_create(request, board_id):
    board = get_object_or_404(Board, id=board_id)
    name = request.POST.get("name", "").strip()
    if name:
        position = board.lists.count()
        List.objects.create(board=board, name=name, position=position)
    return redirect("board_detail", board_id=board.id)


@require_POST
def list_delete(request, list_id):
    lst = get_object_or_404(List, id=list_id)
    board_id = lst.board_id
    lst.delete()
    return redirect("board_detail", board_id=board_id)


@require_POST
def card_create(request, list_id):
    lst = get_object_or_404(List, id=list_id)
    title = request.POST.get("title", "").strip()
    if title:
        position = lst.cards.count()
        Card.objects.create(list=lst, title=title, position=position)
    return redirect("board_detail", board_id=lst.board_id)


@require_POST
def card_delete(request, card_id):
    card = get_object_or_404(Card, id=card_id)
    board_id = card.list.board_id
    card.delete()
    return redirect("board_detail", board_id=board_id)


@require_POST
def card_move(request, card_id):
    """AJAX endpoint used by drag-and-drop to move a card to a new list/position."""
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"ok": False, "error": "invalid json"}, status=400)

    card = get_object_or_404(Card, id=card_id)
    new_list_id = data.get("list_id")
    new_index = data.get("index", 0)

    new_list = get_object_or_404(List, id=new_list_id)
    card.list = new_list
    card.position = new_index
    card.save()

    # Re-sequence positions in the destination list so ordering stays consistent.
    cards = list(new_list.cards.exclude(id=card.id).order_by("position", "id"))
    cards.insert(new_index, card)
    for i, c in enumerate(cards):
        if c.position != i:
            c.position = i
            c.save(update_fields=["position"])

    return JsonResponse({"ok": True})
