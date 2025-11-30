import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .scoring import calculate_task_score

@csrf_exempt
@require_http_methods(["GET", "POST", "OPTIONS"])
def analyze_tasks(request):
    # Handle the actual Analysis logic
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            tasks = data if isinstance(data, list) else []

            processed_tasks = []
            for task in tasks:
                score = calculate_task_score(task)
                task['score'] = score
                processed_tasks.append(task)

            sorted_tasks = sorted(processed_tasks, key=lambda x: x['score'], reverse=True)

            return JsonResponse(sorted_tasks, safe=False)
        
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    return JsonResponse({'error': 'POST method required'}, status=405)