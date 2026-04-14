from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Note, NoteVersion, Comment, RuleAssignment

def note_add(request, rule_type, rule_id):
    if request.method == "POST":
        Note.objects.create(rule_type=rule_type, rule_id=rule_id, rule_label=request.POST.get("rule_label", ""), title=request.POST.get("title"), content=request.POST.get("content"), author=request.POST.get("author"))
        return redirect(request.META.get('HTTP_REFERER', '/'))
    return render(request, "analysis/note_form.html", {"rule_type": rule_type, "rule_id": rule_id})

def note_list(request, rule_type, rule_id):
    return render(request, "analysis/note_list.html", {"notes": Note.objects.filter(rule_type=rule_type, rule_id=rule_id), "rule_type": rule_type, "rule_id": rule_id})

def note_edit(request, pk):
    n = get_object_or_404(Note, pk=pk)
    if request.method == "POST": n.title = request.POST.get("title", n.title); n.content = request.POST.get("content", n.content); n.save(); return redirect(request.META.get('HTTP_REFERER', '/'))
    return render(request, "analysis/note_form.html", {"note": n, "edit": True})

def note_history(request, pk):
    n = get_object_or_404(Note, pk=pk); return render(request, "analysis/note_history.html", {"note": n, "versions": n.versions.all()})

def comment_add(request):
    if request.method == "POST": Comment.objects.create(rule_type=request.POST.get("rule_type"), rule_id=request.POST.get("rule_id"), author=request.POST.get("author"), content=request.POST.get("content"), parent_id=request.POST.get("parent_id") or None)
    return redirect(request.META.get('HTTP_REFERER', '/'))

def assignment_list(request):
    return render(request, "analysis/assignment_list.html", {"assignments": RuleAssignment.objects.all().order_by("-assigned_at")})
