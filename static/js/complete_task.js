async function complete_task(id) {
  if (!confirm("Are you sure?")) return;

  const url = `/tasks/${id}/complete`;

  const response = await fetch(url, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
    },
  });

  if (response.ok) {
    alert("Task completed!");
    window.location.reload();
  } else {
    const errorData = await response.json();
    alert(errorData);
  }
}
