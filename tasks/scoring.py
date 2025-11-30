from datetime import date, datetime

def calculate_task_score(task_data):
    """
    Calculates priority. Higher score = Higher priority.
    Formula: Urgency + (Importance * Weight) + Quick Win Bonus
    """
    score = 0
    
    # 1. Parse Date (Handle string input from JSON)
    due_date_str = task_data.get('due_date')
    if isinstance(due_date_str, str):
        try:
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
        except ValueError:
            return 0 # Invalid date format, push to bottom
    else:
        due_date = due_date_str

    # 2. Urgency Calculation
    today = date.today()
    days_until_due = (due_date - today).days

    if days_until_due < 0:
        score += 100  # OVERDUE! Top priority
    elif days_until_due == 0:
        score += 75   # Due today
    elif days_until_due <= 3:
        score += 50   # Due soon
    else:
        # Subtract points if it's far in the future
        score -= days_until_due 

    # 3. Importance Weighting (Scale 1-10)
    importance = task_data.get('importance', 5)
    score += (importance * 10) 

    # 4. Effort (Quick wins logic)
    hours = task_data.get('estimated_hours', 1)
    if hours < 2:
        score += 20 # Bonus for quick tasks
    elif hours > 10:
        score -= 10 # Slight penalty for huge tasks (break them down!)

    return score