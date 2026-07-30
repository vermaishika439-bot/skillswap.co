/* ============================================================
   chat.js
   Small UX behaviors for the Chat page:
   - Auto-scroll the message list to the latest message on load
   - Keep focus on the input after sending (handled by page reload
     via form submission, so we just re-focus if present)
   ============================================================ */

document.addEventListener("DOMContentLoaded", () => {

    // Scroll the message thread to the bottom so the newest message is visible
    const chatMessages = document.getElementById("chatMessages");
    if (chatMessages) {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Focus the message input automatically when a conversation is open
    const messageInput = document.querySelector(".chat-input-row input[name='content']");
    if (messageInput) {
        messageInput.focus();
    }

});
