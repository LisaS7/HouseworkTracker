document
  .querySelector("form")
  .addEventListener("submit", async function (event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const formObject = {};

    // This is required because formData is not json
    // and the backend cannot accept a formData object
    formData.forEach((value, key) => {
      formObject[key] = value;
    });

    const response = await fetch("/tags/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(formObject),
    });

    if (response.ok) {
      alert("Tag added!");
      window.location.href = "/tags";
    } else {
      // HANDLE ERRORS
      const errorData = await response.json();
      alert(errorData);
    }
  });
