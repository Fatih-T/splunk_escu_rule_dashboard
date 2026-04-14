from django.shortcuts import render, get_object_or_404, redirect
from .models import CBRule
def rule_list(request):
    return render(request, "carbonblack/list.html", {"rules": CBRule.objects.all()})
def rule_detail(request, pk):
    return render(request, "carbonblack/detail.html", {"rule": get_object_or_404(CBRule, pk=pk)})
def rule_create(request):
    if request.method == "POST":
        r = CBRule.objects.create(name=request.POST.get("name"), rule_id=request.POST.get("rule_id"), query=request.POST.get("query"))
        return redirect("cb_list")
    return render(request, "carbonblack/create.html")
