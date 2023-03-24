const chatForm = document.getElementById("chat-form");
const chatInput = document.getElementById("chat-input");
const chatBox = document.getElementById("chat-box");
const emailButton = document.getElementById("email-button");
const coachSelect = document.getElementById("coach-select");

// Define function to add message to chat box
function addMessage(message, sender) {
    const messageElement = document.createElement("div");
    messageElement.classList.add("message");
    messageElement.classList.add(sender);
    messageElement.innerHTML = message;
    chatBox.appendChild(messageElement);
}

// Define function to send user input to backend and display response
async function sendMessage() {
    // Get user input and coach selection from input fields
    const userInput = chatInput.value;
    const coach = coachSelect.value;
    // Clear input field
    chatInput.value = "";
    // Add user input to chat box
    addMessage(userInput, "user");
    // Send user input and coach selection to backend
    const response = await fetch("/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ user_input: userInput, coach: coach }),
    });
    const responseData = await response.json();
    const chatbotResponse = responseData.response;
    // Add chatbot response to chat box
    addMessage(chatbotResponse, "chatbot");
}

// Define function to email transcript to user
async function emailTranscript() {
    // Get user input, coach selection, and transcript from chat box
    const userInputs = Array.from(chatBox.querySelectorAll(".user")).map(
        (element) => element.textContent
    );
    const chatbotResponses = Array.from(
        chatBox.querySelectorAll(".chatbot")
    ).map((element) => element.textContent);
    const transcript = userInputs
        .map((input, index) => `${input}\n${chatbotResponses[index]}`)
        .join("\n");
    const coach = coachSelect.value;
    // Send transcript and coach selection to backend
    const response = await fetch("/email", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ user_input: "", coach: coach, transcript: transcript }),
    });
    const responseData = await response.json();
    const message = responseData.message;
    // Display success message
    alert(message);
}

// Add event listener to chat form
chatForm.addEventListener("submit", (event) => {
    event.preventDefault();
    sendMessage();
});

// Add event listener to email button
emailButton.addEventListener("click", (event) => {
    event.preventDefault();
    emailTranscript();
});
