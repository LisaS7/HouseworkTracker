async function show_input(id) {
  const inputField = document.getElementById(`tag-input-${id}`);
  const heading = document.getElementById(`heading-${id}`);
  const editBtn = document.getElementById(`edit-${id}`);
  const tickBtn = document.getElementById(`tick-${id}`);
  const cancelBtn = document.getElementById(`cancel-${id}`);

  //   hide edit button and heading, show inputfield and tick/cross buttons
  inputField.classList.remove("d-none");
  heading.classList.add("d-none");
  editBtn.classList.add("d-none");
  tickBtn.classList.remove("d-none");
  cancelBtn.classList.remove("d-none");
}

async function cancel_input(id) {
  const inputField = document.getElementById(`tag-input-${id}`);
  const heading = document.getElementById(`heading-${id}`);
  const editBtn = document.getElementById(`edit-${id}`);
  const tickBtn = document.getElementById(`tick-${id}`);
  const cancelBtn = document.getElementById(`cancel-${id}`);
  inputField.classList.add("d-none");
  heading.classList.remove("d-none");
  editBtn.classList.remove("d-none");
  tickBtn.classList.add("d-none");
  cancelBtn.classList.add("d-none");
}

async function edit_task(id) {
  const inputField = document.getElementById(`tag-input-${id}`);
  const newValue = inputField.value;

  fetch(`/tags/${id}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ id: id, name: newValue }),
  }).then((response) => {
    if (!response.ok) {
      throw new Error("Failed to update tag");
    } else {
      window.location.reload();
      return response.json();
    }
  });
}

//   function updateTag() {
//     const newName = tagInput.value.trim();
//     if (!newName || newName === "{{ tag.name }}") {
//       tagName.classList.remove("d-none");
//       tagInput.classList.add("d-none");
//       return;
//     }

//     fetch(`/tags/${tagId}`, {
//       method: "PUT",
//       headers: {
//         "Content-Type": "application/json",
//       },
//       body: JSON.stringify({ name: newName }),
//     })
//       .then((response) => {
//         if (!response.ok) throw new Error("Failed to update tag");
//         return response.json();
//       })
//       .then((data) => {
//         tagName.textContent = data.name;
//         tagName.classList.remove("d-none");
//         tagInput.classList.add("d-none");
//       })
//       .catch((error) => {
//         console.error("Error updating tag:", error);
//         alert("Failed to update tag. Try again.");
//       });
//   }
// });
