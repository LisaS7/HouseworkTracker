async function delete_item(endpoint, id) {
  if (!confirm("Are you sure?")) return;

  const url = `/${endpoint}/${id}`;

  const response = await fetch(url, {
    method: "DELETE",
    headers: {
      "Content-Type": "application/json",
    },
  });

  if (response.ok) {
    alert("Deleted!");
    window.history.go(-1);
  } else {
    const errorData = await response.json();
    alert(errorData);
  }
}
