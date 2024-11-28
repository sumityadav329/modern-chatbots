document.addEventListener('DOMContentLoaded', () => {
    const messageInput = document.getElementById('message-input');
    const sendBtn = document.getElementById('send-btn');
    const chatBox = document.getElementById('chat-box');
    const newChatBtn = document.getElementById('new-chat-btn');
    const clearChatBtn = document.getElementById('clear-chat-btn');

    // Auto-resize textarea
    messageInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
    });

    // Send message function
    function sendMessage() {
        const message = messageInput.value.trim();
        if (message) {
            // Add user message
            const userMessageElement = createMessageElement(message, 'user');
            chatBox.appendChild(userMessageElement);

            // Simulate AI response (replace with actual backend call)
            setTimeout(() => {
                const aiResponse = createMessageElement('Processing your request...', 'assistant');
                chatBox.appendChild(aiResponse);
                scrollToBottom();
            }, 500);

            // Clear input and reset height
            messageInput.value = '';
            messageInput.style.height = 'auto';

            scrollToBottom();
        }
    }

    // Create message element
    function createMessageElement(content, role) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', role);
        
        const messageContent = document.createElement('div');
        messageContent.classList.add('message-content');
        
        const messageText = document.createElement('p');
        messageText.textContent = content;
        messageContent.appendChild(messageText);

        if (role === 'assistant') {
            const actionDiv = document.createElement('div');
            actionDiv.classList.add('message-actions');
            
            const copyBtn = document.createElement('button');
            copyBtn.classList.add('copy-btn');
            copyBtn.innerHTML = '<i class="fas fa-copy"></i>';
            copyBtn.title = 'Copy';
            copyBtn.addEventListener('click', () => {
                navigator.clipboard.writeText(content);
                copyBtn.innerHTML = '<i class="fas fa-check"></i>';
                setTimeout(() => {
                    copyBtn.innerHTML = '<i class="fas fa-copy"></i>';
                }, 1500);
            });

            actionDiv.appendChild(copyBtn);
            messageContent.appendChild(actionDiv);
        }

        messageDiv.appendChild(messageContent);
        return messageDiv;
    }

    // Scroll to bottom of chat
    function scrollToBottom() {
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    // Event Listeners
    sendBtn.addEventListener('click', sendMessage);
    messageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    // New Chat Button
    newChatBtn.addEventListener('click', () => {
        const messagesExceptWelcome = document.querySelectorAll('#chat-box .message:not(.welcome-message)');
        messagesExceptWelcome.forEach(msg => msg.remove());
        
        const welcomeMessage = document.querySelector('.welcome-message');
        if (!welcomeMessage) {
            const newWelcomeMessage = createMessageElement('How can I help you today?', 'assistant');
            newWelcomeMessage.classList.add('welcome-message');
            chatBox.appendChild(newWelcomeMessage);
        }
    });

    // Clear Chat Button
    clearChatBtn.addEventListener('click', () => {
        const allMessages = document.querySelectorAll('#chat-box .message');
        allMessages.forEach(msg => msg.remove());
        
        const welcomeMessage = createMessageElement('How can I help you today?', 'assistant');
        welcomeMessage.classList.add('welcome-message');
        chatBox.appendChild(welcomeMessage);
    });
});