from datetime import date, datetime

def calculate_task_score(task_data):
    """
    Calculates priority. Higher score = Higher priority.
    """
    score = 0
    
    # 1. Parse Date
    due_date_str = task_data.get('due_date')
    if isinstance(due_date_str, str):
        try:
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
        except ValueError:
            return 0 
    else:
        due_date = due_date_str

    # 2. Urgency
    today = date.today()
    days_until_due = (due_date - today).days

    if days_until_due < 0:
        score += 100  # Overdue
    elif days_until_due == 0:
        score += 75   # Due today
    elif days_until_due <= 3:
        score += 50   # Due soon
    else:
        score -= days_until_due 

    # 3. Importance (Weighted)
    importance = task_data.get('importance', 5)
    score += (importance * 10) 

    # 4. Effort (Quick wins)
    hours = task_data.get('estimated_hours', 1)
    if hours < 2:
        score += 20 
    elif hours > 10:
        score -= 10 

    # 5. Dependencies (NEW Logic)
    # If a task has dependencies, it's blocked. Penalize it heavily.
    dependencies = task_data.get('dependencies', [])
    if dependencies:
        score -= 50 

    return score