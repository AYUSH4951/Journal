from django.shortcuts import render, redirect, get_object_or_404
from .models import JournalEntry
from .forms import JournalEntryForm
from .utils import analyze_entry
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .utils import analyze_entry, detect_mood
from django.db.models import Count
from django.http import JsonResponse

# Create your views here.
@login_required
def edit_entry(request, entry_id):
    entry = get_object_or_404(JournalEntry, id=entry_id, user=request.user)
    
    if request.method == 'POST':
        form = JournalEntryForm(request.POST, instance=entry)
        if form.is_valid():
            updated_entry = form.save(commit=False)
            updated_entry.user = request.user
            updated_entry.ai_analysis = analyze_entry(updated_entry.content)
            updated_entry.mood = detect_mood(updated_entry.content)
            updated_entry.save()
            return redirect('entry_detail', entry_id=entry.id)
    else:
        form = JournalEntryForm(instance=entry)
    
    return render(request, 'journal/edit_entry.html', {'form': form, 'entry': entry})


@login_required
def delete_entry(request, entry_id):
    entry = get_object_or_404(JournalEntry, id=entry_id, user=request.user)
    
    if request.method == 'POST':
        entry.delete()
        return redirect('entry_list')
    
    return render(request, 'journal/delete_entry.html', {'entry': entry})


def entry_detail(request, entry_id):
    entry = get_object_or_404(JournalEntry, id=entry_id, user=request.user)
    return render(request, 'journal/entry_detail.html', {'entry': entry})

@login_required
def entry_list(request):
    mood_filter = request.GET.get('mood')
    if mood_filter:
        entries = JournalEntry.objects.filter(user=request.user, mood=mood_filter).order_by('-date')
    else:
        entries = JournalEntry.objects.filter(user=request.user).order_by('-date')

    return render(request, 'journal/entry_list.html', {'entries': entries})


def create_entry(request):  # renamed from create_journal_entry
    if request.method == 'POST':
        form = JournalEntryForm(request.POST)
        if form.is_valid():
            journal = form.save(commit=False)
            journal.user = request.user
            journal.ai_analysis = analyze_entry(journal.content)
            journal.mood = detect_mood(journal.content)
            journal.save()
            return redirect('entry_list')
    else:
        form = JournalEntryForm()
    
    return render(request, 'journal/create_entry.html', {'form': form})



@login_required
def mood_stats(request):
    mood_data = JournalEntry.objects.filter(user=request.user)\
        .values('mood')\
        .annotate(count=Count('mood'))

    labels = [item['mood'] for item in mood_data]
    data = [item['count'] for item in mood_data]

    return JsonResponse({'labels': labels, 'data': data})

@login_required
def analytics_page(request):
    return render(request, 'journal/analytics.html')
