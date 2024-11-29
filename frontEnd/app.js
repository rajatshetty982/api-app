const apiUrl = "https://someethingg.com"; // need to replace the actual API URL

// Fetch all tasks and display them
async function fetchTasks() {
    try {
        const response = await fetch(`${apiUrl}/todos`);
        const data = await response.json();
        const taskList = document.getElementById('tasks');
        taskList.innerHTML = '';

        data.tasks.forEach(task => {
            const li = document.createElement('li');
            li.innerHTML = `
                <span>${task.title} - ${task.finished ? 'Completed' : 'Pending'}</span>
                <button onclick="deleteTask(${task.id})">Delete</button>
                <button onclick="toggleTask(${task.id}, ${!task.finished})">${task.finished ? 'Unmark' : 'Mark as Completed'}</button>
            `;
            taskList.appendChild(li);
        });
    } catch (error) {
        console.error("Error fetching tasks:", error);
    }
}

// Add a new task
async function addTask() {
    const title = document.getElementById('title').value;
    const description = document.getElementById('description').value;
    const startDate = document.getElementById('start_date').value;
    const finished = document.getElementById('finished').checked;

    if (!title) {
        alert('Title is required');
        return;
    }

    const taskData = {
        title,
        description,
        start_date: startDate,
        finished
    };

    try {
        const response = await fetch(`${apiUrl}/todos`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(taskData)
        });

        const newTask = await response.json();
        fetchTasks(); // Refresh the task list
    } catch (error) {
        console.error("Error adding task:", error);
    }
}

// Toggle task completion (mark as finished or unmark)
async function toggleTask(taskId, finishedStatus) {
    try {
        const response = await fetch(`${apiUrl}/todos/${taskId}`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ finished: finishedStatus })
        });

        const updatedTask = await response.json();
        fetchTasks(); // Refresh the task list
    } catch (error) {
        console.error("Error toggling task completion:", error);
    }
}

// Delete a task
async function deleteTask(taskId) {
    try {
        const response = await fetch(`${apiUrl}/todos/${taskId}`, {
            method: 'DELETE'
        });

        const result = await response.json();
        fetchTasks(); // Refresh the task list
    } catch (error) {
        console.error("Error deleting task:", error);
    }
}

// Initial fetch of tasks when the page loads
fetchTasks();

