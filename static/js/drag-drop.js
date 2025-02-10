// Removed until I figure out how to get it working.
// The problem is that the bootstrap navbar stops working on this page
// when I include this script. Probably to do with the ev.preventdefault
// but I haven't found a way to fix it yet

// Allow the drop
function allowDrop(ev) {
  if (["LOW", "MEDIUM", "HIGH"].includes(ev.target.id)) {
    ev.preventDefault();
  }
}

// Start dragging a task
function drag(ev) {
  ev.dataTransfer.setData("taskId", ev.target.getAttribute("data-task-id"));
}

// Handle the drop event
function drop(ev) {
  if (["LOW", "MEDIUM", "HIGH"].includes(ev.target.id)) {
    ev.preventDefault();
  }

  var taskId = ev.dataTransfer.getData("taskId");
  var newPriority = ev.target.id;

  // Ensure the drop target is valid (e.g., not a nested div)
  if (!["LOW", "MEDIUM", "HIGH"].includes(newPriority)) {
    return;
  }

  // Send an API request to update the task priority in the database
  fetch(`/tasks/${taskId}/priority`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ priority: newPriority }),
  })
    .then((response) => {
      if (response.ok) {
        // Optionally, update the UI to reflect the new priority
        document
          .getElementById(newPriority)
          .appendChild(document.getElementById("task-" + taskId));
      }
    })
    .catch((error) => {
      console.error("Error updating task priority:", error);
    });
}
