$(document).ready(function () {

    // Display Falar mensagem
    // Expoe a função DisplayMessage para ser chamada pelo Python (usando eel)
    eel.expose(DisplayMessage)

    // Função para exibir a mensagem do Jarvis na interface
    function DisplayMessage(message) {

        // Define o texto do primeiro item da lista na classe "siri-message" como a mensagem recebida
        $(".siri-message li:first").text(message);

        // Inicia a animação "textillate" na classe "siri-message"
        $('.siri-message').textillate('start');

    }

    // Display hood
    // Expoe a função ShowHood para ser chamada pelo Python (usando eel)
    eel.expose(ShowHood)

    // Função para mostrar o "hood" (a animação circular do Jarvis)
    function ShowHood() {

        // Remove o atributo "hidden" do elemento com ID "Oval" (torna o elemento visível)
        $("#Oval").attr("hidden", false);

        // Adiciona o atributo "hidden" ao elemento com ID "Siriwave" (torna o elemento invisível)
        $("#Siriwave").attr("hidden", true);
    }

    // Expoe a função senderText para ser chamada pelo Python (usando eel)
    eel.expose(senderText)

    // Função para exibir mensagens enviadas pelo usuário
    function senderText(message) {

        // Obtém o elemento com ID "chat-canvas-body"
        var chatBox = document.getElementById("chat-canvas-body");

        // Verifica se a mensagem não está vazia
        if (message.trim() !== "") {
            // Adiciona a mensagem enviada pelo usuário ao chat
            chatBox.innerHTML += `<div class="row justify-content-end mb-4">
            <div class = "width-size">
            <div class="sender_message">${message}</div>
        </div>`; 
    
            // Rola a caixa de bate-papo para baixo para mostrar a última mensagem
            chatBox.scrollTop = chatBox.scrollHeight;
        }
    }

    // Expoe a função receiverText para ser chamada pelo Python (usando eel)
    eel.expose(receiverText)

    // Função para exibir mensagens recebidas do I.V.E
    function receiverText(message) {

        // Obtém o elemento com ID "chat-canvas-body"
        var chatBox = document.getElementById("chat-canvas-body");

        // Verifica se a mensagem não está vazia
        if (message.trim() !== "") {
            // Adiciona a mensagem recebida do Jarvis ao chat
            chatBox.innerHTML += `<div class="row justify-content-start mb-4">
            <div class = "width-size">
            <div class="receiver_message">${message}</div>
            </div>
        </div>`; 
    
            // Rola a caixa de bate-papo para baixo para mostrar a última mensagem
            chatBox.scrollTop = chatBox.scrollHeight;
        }
        
    }


});