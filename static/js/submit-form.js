document
  .querySelector("form")
  .addEventListener("submit", async function (event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const formObject = {};

    formData.forEach((value, key) => {
      if (key === "tags") {
        if (!formObject["tags"]) {
          formObject["tags"] = [];
        }
        formObject[key].push({ name: value });
      } else {
        formObject[key] = value;
      }
    });

    console.log(formObject);

    const response = await fetch("/tasks/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(formObject),
    });

    if (response.ok) {
      alert("Task added!");
      window.location.href = "/tasks";
    } else {
      // HANDLE ERRORS
      const errorData = await response.json();
      const errorMessages = errorData.errors
        .map((error) => `${error.loc[1]}: ${error.msg}`)
        .join(", ");
      alert(errorMessages);
    }
  });
