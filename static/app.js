// Toggle Chatbot Visibility
const toggleChatbotButton = document.getElementById("toggle-chatbot");
const chatContainer = document.getElementById("chat-container");

toggleChatbotButton.addEventListener("click", () => {
  chatContainer.classList.toggle("hidden");
});

// Handle Chat Input
document.getElementById("send-btn").addEventListener("click", () => {
  const userInput = document.getElementById("user-input").value.trim();
  if (userInput) {
    addMessage(userInput, "user");
    fetchResponse(userInput);
    document.getElementById("user-input").value = "";
  }
});
document.getElementById('toggle-chatbot').addEventListener('click', () => {
  const chatContainer = document.getElementById('chat-container');
  chatContainer.classList.toggle('visible');
});


function addMessage(message, sender) {
  const chatBox = document.getElementById("chat-box");
  const messageElement = document.createElement("div");
  messageElement.className = `chat-message ${sender}`;
  messageElement.innerHTML = `<span>${message}</span>`;
  chatBox.appendChild(messageElement);
  chatBox.scrollTop = chatBox.scrollHeight;
}

async function fetchResponse(message) {
  try {
    const response = await fetch("http://localhost:5000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    });
    const data = await response.json();
    addMessage(data.reply, "bot");
  } catch (error) {
    addMessage("Error: Unable to connect to the server.", "bot");
  }
}
