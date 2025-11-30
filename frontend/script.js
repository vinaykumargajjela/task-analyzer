async function analyzeTasks() {
    const inputVal = document.getElementById('taskInput').value;
    const resultsDiv = document.getElementById('resultsList');
    const statusDiv = document.getElementById('status');
    
    statusDiv.textContent = 'Processing...';
    
    try {
        const tasks = JSON.parse(inputVal);
        console.log('Parsed tasks:', tasks);

        // Fetch to our Django Backend
        const response = await fetch('http://127.0.0.1:8000/api/tasks/analyze/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(tasks)
        });

        console.log('Response status:', response.status);

        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`Server error: ${response.status} - ${errorText}`);
        }

        const sortedTasks = await response.json();
        console.log('Sorted tasks:', sortedTasks);
        
        // Clear previous results
        resultsDiv.innerHTML = '';
        statusDiv.textContent = '';

        if (sortedTasks.length === 0) {
            resultsDiv.innerHTML = '<p>No tasks to display</p>';
            return;
        }

        // Generate Cards
        sortedTasks.forEach(task => {
            const card = document.createElement('div');
            // Determine Color Class based on score
            let priorityClass = 'priority-low';
            if (task.score > 80) priorityClass = 'priority-high';
            else if (task.score > 40) priorityClass = 'priority-medium';

            card.className = `task-card ${priorityClass}`;
            card.innerHTML = `
                <div class="task-header">
                    <span>${task.title}</span>
                    <span>Score: ${task.score}</span>
                </div>
                <div class="task-meta">
                    Due: ${task.due_date} | Effort: ${task.estimated_hours}h | Imp: ${task.importance}
                </div>
            `;
            resultsDiv.appendChild(card);
        });

    } catch (error) {
        console.error('Error:', error);
        statusDiv.textContent = 'Error: ' + error.message;
        resultsDiv.innerHTML = '<p style="color: red;">Error: ' + error.message + '</p>';
    }
}

// Pre-fill with dummy data for easy testing
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('taskInput').value = JSON.stringify([
        {"title": "Submit Assignment", "due_date": "2023-11-28", "importance": 10, "estimated_hours": 2},
        {"title": "Grocery Shopping", "due_date": "2025-12-05", "importance": 3, "estimated_hours": 1},
        {"title": "Learn Django", "due_date": "2025-11-30", "importance": 8, "estimated_hours": 20}
    ], null, 4);
    
    // Auto-analyze on load
    setTimeout(function() {
        analyzeTasks();
    }, 500);
});