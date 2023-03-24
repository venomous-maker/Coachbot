function sendDataToApi(event) {
  // Prevent the default form submission behavior
  event.preventDefault();

  // Get the form element
  const form = event.target;

  // Get the form data
  const formData = new FormData(form);

  // Convert form data to URL-encoded format
  const urlEncodedData = new URLSearchParams(formData).toString();

  // Send the form data to the API endpoint using the fetch API
  fetch("/register/add", {
    method: "POST",
    body: urlEncodedData,
    headers: {
      "Content-Type": "application/x-www-form-urlencoded"
    }
  })
  .then(response => {
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
    alert("Data to be processed later");
    //location.replace("/");
    // Handle the successful API response here
  })
  .catch(error => {
    // Handle any errors that occurred while sending data to the API here
    console.error("Error sending data to API:", error);
  });
}

/*document.addEventListener("DOMContentLoaded", () => {
  // Get the form element and add an event listener to listen for submit events
  const form = document.querySelector("form");
  if (form) {
    form.addEventListener("submit", sendDataToApi);
  }
});*/
