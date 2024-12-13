

if (uploadedPdfUrl) {
    
    pdfjsLib.getDocument(uploadedPdfUrl).promise.then(function(pdfDoc) {
        
        for (let pageNum = 1; pageNum <= pdfDoc.numPages; pageNum++) {
            pdfDoc.getPage(pageNum).then(function(page) {
                var viewport = page.getViewport({scale: 1.5});
                var canvas = document.createElement('canvas');
                var ctx = canvas.getContext('2d');
                canvas.height = viewport.height;
                canvas.width = viewport.width;

                document.getElementById('pdf-viewer-container').appendChild(canvas);

                page.render({
                    canvasContext: ctx,
                    viewport: viewport
                });
            });
        }
    }).catch(function(error) {
        console.error("Error loading PDF: ", error); 
    });
}

const chatLog = document.getElementById('chat-container');
const questionInput = document.getElementById('question-input');
const sendButton = document.getElementById('send-button');
let chatHistory = [];
let tokenCount = 0;

const updateChatLog = (role, text) => {
    const chatLog = document.getElementById('chat-log'); 
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', role === 'user' ? 'user-message' : 'openai-message');
    messageDiv.textContent = text;
    chatLog.appendChild(messageDiv);
    chatLog.scrollTop = chatLog.scrollHeight; 
};


sendButton.addEventListener('click', function() {
    const question = questionInput.value.trim();
    if (question !== '') {
        updateChatLog('user', question);
        chatHistory.push({ role: 'user', content: question });
        const loadingIndicator = document.getElementById('loading-indicator'); 
        loadingIndicator.style.display = 'block'; 
        

        fetch('/chatbot/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({ chatHistory: chatHistory })
        })
        .then(response => response.json())
        .then(data => {
            const response = data.response;
            const tokensUsed = data.tokens_used;
            tokenCount += tokensUsed;
            document.getElementById('token-count').textContent = `Tokens used: ${tokenCount}`;
            updateChatLog('openai', response);
            chatHistory.push({ role: 'assistant', content: response });
            loadingIndicator.style.display = 'none';
        })
        .catch(error => console.error('Error:', error));
      


        questionInput.value = ''; 
    }
});
