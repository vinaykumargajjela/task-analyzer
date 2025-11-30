async function analyzeTasks() {
    const inputVal = document.getElementById('taskInput').value;
    const strategyVal = document.getElementById('sortStrategy').value;
    const resultsDiv = document.getElementById('resultsList');
    const statusDiv = document.getElementById('status');
    const statsBar = document.getElementById('statsBar');
    
    statusDiv.textContent = 'Processing...';
    
    try {
        const tasks = JSON.parse(inputVal);

        // Prepare payload with strategy
        const payload = {
            tasks: tasks,
            strategy: strategyVal
        };

        const response = await fetch('/api/tasks/analyze/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (!response.ok) throw new Error('Network response was not ok');

        const sortedTasks = await response.json();
        
        // Render
        resultsDiv.innerHTML = '';
        statusDiv.textContent = '';
        statsBar.innerHTML = `<span>Analyzed <strong>${sortedTasks.length}</strong> tasks</span>`;

        if (sortedTasks.length === 0) {
            resultsDiv.innerHTML = '<div class="empty-state">No tasks found</div>';
            return;
        }

        sortedTasks.forEach(task => {
            const card = document.createElement('div');
            
            // Determine Class
            let priorityClass = 'priority-low';
            if (task.score > 80) priorityClass = 'priority-high';
            else if (task.score > 40) priorityClass = 'priority-medium';

            card.className = `task-card ${priorityClass}`;
            
            // Format Date
            const dateObj = new Date(task.due_date);
            const dateStr = dateObj.toLocaleDateString();

            card.innerHTML = `
                <div class="card-header">
                    <h3>${task.title}</h3>
                    <span class="score-badge">Score: ${task.score}</span>
                </div>
                <div class="card-body">
                   <p>Importance: <strong>${task.importance}/10</strong></p>
                </div>
                <div class="card-meta">
                    <span>📅 ${dateStr}</span>
                    <span>⏱ ${task.estimated_hours} hrs</span>
                </div>
            `;
            resultsDiv.appendChild(card);
        });

    } catch (error) {
        statusDiv.textContent = 'Error: Invalid JSON format';
        console.error(error);
    }
}

// Pre-fill Dummy Data
document.addEventListener('DOMContentLoaded', () => {
    const dummyData = [
        {"title": "Critical Bug Fix", "due_date": "2023-11-28", "importance": 10, "estimated_hours": 2, "dependencies": []},
        {"title": "Long Term Project", "due_date": "2025-12-05", "importance": 8, "estimated_hours": 20, "dependencies": []},
        {"title": "Blocked Task", "due_date": "2025-11-30", "importance": 5, "estimated_hours": 3, "dependencies": [101]}
    ];
    document.getElementById('taskInput').value = JSON.stringify(dummyData, null, 4);
});