document.addEventListener("DOMContentLoaded", function () {
  fetch("/tags/", {
    method: "GET",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
  })
    .then((response) => response.json())
    .then((tags) => {
      const choices = tags.map((tag) => ({
        value: tag.name,
        label: tag.name,
      }));

      Choices("#tags", {
        removeItemButton: true, // Adds an "X" button to remove tags
        removeItems: true,
        duplicateItemsAllowed: false,
        placeholderValue: "Add a tag",
        addItems: true,
        allowHTML: false,
        choices: choices,
      });
    });
});
