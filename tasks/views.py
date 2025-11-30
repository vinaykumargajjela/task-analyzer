import json
from datetime import date
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .scoring import calculate_task_score
from .models import Task

@csrf_exempt
@require_http_methods(["POST", "OPTIONS"])
def analyze_tasks(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            # Support both list input or dict with 'tasks' key
            tasks = body.get('tasks', body) if isinstance(body, dict) else body
            sort_strategy = body.get('strategy', 'default') if isinstance(body, dict) else 'default'
            
            if not isinstance(tasks, list):
                tasks = []

            processed_tasks = []
            for task in tasks:
                score = calculate_task_score(task)
                task['score'] = score
                processed_tasks.append(task)

            # Sorting Logic
            if sort_strategy == 'fastest':
                # Sort by shortest time first, then importance
                sorted_tasks = sorted(processed_tasks, key=lambda x: (x.get('estimated_hours', 0), -x.get('importance', 0)))
            else:
                # Default: Sort by calculated Smart Score
                sorted_tasks = sorted(processed_tasks, key=lambda x: x['score'], reverse=True)

            return JsonResponse(sorted_tasks, safe=False)
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    return JsonResponse({'error': 'POST method required'}, status=405)

@require_http_methods(["GET"])
def suggest_tasks(request):
    """
    Requirement: Returns top 3 tasks for 'today'.
    Note: Since the app currently analyzes raw JSON without saving to DB,
    this returns a placeholder or tasks from DB if you choose to save them.
    """
    # Fetching from DB example (if you were saving them):
    today = date.today()
    tasks = Task.objects.filter(due_date=today).order_by('-importance')[:3]
    
    data = [{
        'title': t.title,
        'due_date': t.due_date,
        'importance': t.importance
    } for t in tasks]
    
    return JsonResponse({
        'message': f"Top 3 suggestions for {today}",
        'tasks': data
    })