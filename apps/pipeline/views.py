from django.shortcuts import render, get_object_or_404, redirect
from apps.escu.models import ESCURule
from apps.carbonblack.models import CBRule
def pipeline_board(request):
    stages = ["new", "under_review", "applicable", "in_progress", "ready_for_cb", "converted", "active"]
    board = {s: {"escu": ESCURule.objects.filter(status=s), "cb": CBRule.objects.filter(status=s)} for s in stages}
    return render(request, "pipeline/board.html", {"board": board, "stages": stages})
def stage_transition(request, type, pk):
    new_stage = request.POST.get("new_stage")
    model = ESCURule if type == "escu" else CBRule
    obj = get_object_or_404(model, pk=pk)
    obj.status = new_stage; obj.save()
    return redirect(request.META.get('HTTP_REFERER', '/'))
def convert_wizard(request, escu_pk):
    escu = get_object_or_404(ESCURule, pk=escu_pk)
    step = int(request.POST.get("step", 1)) if request.method == "POST" else 1
    if request.method == "POST" and step == 3:
        cb = CBRule.objects.create(name=f"CB: {escu.name}", rule_id=f"CB-{escu.rule_id}", query=request.POST.get("cb_query"), source_escu_rule=escu)
        escu.status = "converted"; escu.save()
        return redirect("cb_detail", pk=cb.pk)
    return render(request, "pipeline/convert_wizard.html", {"escu_rule": escu, "step": step})
