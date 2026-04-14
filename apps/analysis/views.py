from django.shortcuts import render, redirect
from .models import Note
def note_add(request, rule_type, rule_id):
    if request.method == "POST":
        Note.objects.create(rule_type=rule_type, rule_id=rule_id, title=request.POST.get("title"), content=request.POST.get("content"), author=request.POST.get("author"))
        return redirect(request.META.get('HTTP_REFERER', '/'))
    return render(request, "analysis/note_form.html", {"rule_type": rule_type, "rule_id": rule_id})
def assignment_list(request):
    from .models import RuleAssignment
    return render(request, "analysis/assignment_list.html", {"assignments": RuleAssignment.objects.all()})
