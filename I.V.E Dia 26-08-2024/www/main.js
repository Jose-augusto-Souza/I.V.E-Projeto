$(document).ready(function () {
    // Inicializa o plugin textillate para animar o texto dentro dos elementos com a classe .text
    $('.text').textillate({
        loop: false,
        sync: true,
        in: {
            effect: "bounceIn", // Efeito de animação de entrada
        },
        out: {
            effect: "bounceOut", // Efeito de animação de saída
        },
    });

    // Cria uma instância do SiriWave para exibir uma animação de onda sonora
    var siriWave = new SiriWave({
        container: document.getElementById("siri-container"), // Elemento onde a animação será exibida
        width: 800, // Largura da animação
        height: 200, // Altura da animação
        style: "ios9", // Estilo da onda
        amplitude: "1", // Amplitude da onda
        speed: "0.30", // Velocidade da onda
        autostart: true // Inicia a animação automaticamente
    });

    // Inicializa o plugin textillate para animar o texto dentro dos elementos com a classe .siri-message
    $('.siri-message').textillate({
        loop: false,
        sync: true,
        in: {
            effect: "fadeInUp", // Efeito de animação de entrada
            sync: true,
        },
        out: {
            effect: "fadeOutUp", // Efeito de animação de saída
            sync: true,
        },
    });

    // Adiciona um evento de clique ao botão com o ID MicBtn
    $("#MicBtn").click(function () {
        $("#Oval").attr("hidden", true); // Esconde o elemento com o ID Oval
        $("#SiriWave").attr("hidden", false); // Mostra o elemento com o ID SiriWave
        eel.allCommands()(); // Chama a função allCommands do módulo eel
    });

    // Função para tratar o evento de liberar uma tecla
    function doc_keyUp(e) {
        if (e.key === 'j' && e.metaKey) {
            eel.playAssistantSound(); // Chama a função playAssistantSound do módulo eel
            $("#Oval").attr("hidden", true); // Esconde o elemento com o ID Oval
            $("#SiriWave").attr("hidden", false); // Mostra o elemento com o ID SiriWave
            eel.allCommands()(); // Chama a função allCommands do módulo eel
        }
    }

    // Adiciona um listener para o evento keyup no documento
    document.addEventListener('keyup', doc_keyUp, false);

    // Função para processar a mensagem e atualizar a interface
    function PlayAssistant(message) {
        if (message != "") {
            $("#Oval").attr("hidden", true); // Esconde o elemento com o ID Oval
            $("#SiriWave").attr("hidden", false); // Mostra o elemento com o ID SiriWave
            eel.allCommands(message); // Chama a função allCommands do módulo eel com a mensagem
            $("#chatbox").val(""); // Limpa o valor do chatbox
            $("#MicBtn").attr('hidden', false); // Mostra o botão MicBtn
            $("#SendBtn").attr('hidden', true); // Esconde o botão SendBtn
        }
    }

    // Função para mostrar ou esconder os botões com base no conteúdo da mensagem
    function ShowHideButton(message) {
        if (message.length == 0) {
            $("#MicBtn").attr("hidden", false); // Mostra o botão MicBtn
            $("#SendBtn").attr("hidden", true); // Esconde o botão SendBtn
        } else {
            $("#MicBtn").attr("hidden", true); // Esconde o botão MicBtn
            $("#SendBtn").attr("hidden", false); // Mostra o botão SendBtn
        }
    }

    // Adiciona um listener para o evento keyup no chatbox
    $("#chatbox").keyup(function () {
        let message = $("#chatbox").val(); // Obtém o valor do chatbox
        ShowHideButton(message); // Atualiza a visibilidade dos botões
    });

    // Adiciona um evento de clique ao botão SendBtn
    $("#SendBtn").click(function () {
        let message = $("#chatbox").val(); // Obtém o valor do chatbox
        PlayAssistant(message); // Processa a mensagem
    });

    // Adiciona um evento de keypress ao chatbox
    $("#chatbox").keypress(function (e) {
        key = e.which; // Obtém o código da tecla pressionada
        if (key == 13) { // Verifica se a tecla pressionada é Enter
            let message = $("#chatbox").val(); // Obtém o valor do chatbox
            PlayAssistant(message); // Processa a mensagem
        }
    });

    // Adiciona um evento de clique ao botão SettingsBtn
    $("#SettingsBtn").click(function () {
        $("#settingsModal").modal('show'); // Exibe o modal de configurações
    });

    // Variável para armazenar o GIF selecionado
    let selectedGif;
    // Adiciona um evento de clique aos elementos com a classe selectable-gif
    $(".selectable-gif").click(function () {
        $(".selectable-gif").removeClass("selected"); // Remove a classe selected de todos os GIFs
        $(this).addClass("selected"); // Adiciona a classe selected ao GIF clicado
        selectedGif = $(this).attr("src"); // Armazena a URL do GIF selecionado
    });

    // Adiciona um evento de clique ao botão saveGifBtn
    $("#saveGifBtn").click(function () {
        if (selectedGif) {
            $("#Oval img").attr("src", selectedGif); // Define a URL do GIF como plano de fundo
            $("#settingsModal").modal('hide'); // Fecha o modal de configurações
        }
    });

    // Adiciona um evento de clique ao botão QuestionBtn
    $("#QuestionBtn").click(function () {
        $("#questionModal").modal('show'); // Exibe o modal de perguntas
    });

    // Adiciona um evento de clique ao botão CodeBtn
    $("#CodeBtn").click(function () {
        $("#codeModal").modal('show'); // Exibe o modal de códigos
        loadWebCommands(); // Carrega os comandos da web
        loadWindowsCommands(); // Carrega os comandos do Windows
    });

    // Adiciona um evento de clique ao botão saveWebCommand
    $("#saveWebCommand").click(function () {
        let webCommand = $("#webCommand").val(); // Obtém o comando da web
        let webUrl = $("#webUrl").val(); // Obtém a URL do comando da web
        if (webCommand && webUrl) {
            eel.saveWebCommand(webCommand, webUrl)(); // Salva o comando da web
            $("#webCommand").val(""); // Limpa o campo do comando da web
            $("#webUrl").val(""); // Limpa o campo da URL
            loadWebCommands(); // Recarrega os comandos da web
        }
    });

    // Adiciona um evento de clique ao botão saveWindowsCommand
    $("#saveWindowsCommand").click(function () {
        let windowsCommand = $("#windowsCommand").val(); // Obtém o comando do Windows
        let windowsPath = $("#windowsPath").val(); // Obtém o caminho do comando do Windows
        if (windowsCommand && windowsPath) {
            eel.saveWindowsCommand(windowsCommand, windowsPath)(); // Salva o comando do Windows
            $("#windowsCommand").val(""); // Limpa o campo do comando do Windows
            $("#windowsPath").val(""); // Limpa o campo do caminho
            loadWindowsCommands(); // Recarrega os comandos do Windows
        }
    });

    // Função para carregar e exibir os comandos da web
    function loadWebCommands() {
        eel.getWebCommands()().then(commands => {
            $("#savedWebCommands").empty(); // Limpa a lista de comandos salvos
            commands.forEach(command => {
                // Adiciona cada comando à lista de comandos salvos
                $("#savedWebCommands").append(`
                    <div class="row mb-2 command-row" data-command="${command.command}">
                        <div class="col-4">
                            <input type="text" class="form-control command-input" value="${command.command}" readonly>
                        </div>
                        <div class="col-4">
                            <input type="text" class="form-control url-input" value="${command.url}" readonly>
                        </div>
                        <div class="col-2">
                            <button class="btn btn-warning edit-web-command">Editar</button> 
                        </div>
                        <div class="col-2">
                            <button class="btn btn-danger delete-web-command">Excluir</button>
                        </div>
                    </div>
                `);
            });

            // Adiciona evento de clique para os botões de exclusão
            $(".delete-web-command").click(function() {
                let row = $(this).closest('.command-row');
                let command = row.data('command');
                eel.deleteWebCommand(command)(); // Exclui o comando da web
                row.remove(); // Remove a linha da lista
            });

            // Adiciona evento de clique para os botões de edição 
            $(".edit-web-command").click(function() {
                let row = $(this).closest('.command-row');
                let commandInput = row.find('.command-input');
                let urlInput = row.find('.url-input');
                let oldCommand = commandInput.val();

                commandInput.prop('readonly', false); // Torna o campo editável
                urlInput.prop('readonly', false); // Torna o campo editável
                $(this).removeClass('btn-warning edit-web-command').addClass('btn-success save-web-command').text('Salvar');

                // Adiciona evento de clique para o botão Salvar
                row.find('.save-web-command').click(function() {
                    let newCommand = commandInput.val(); // Obtém o novo comando
                    let newUrl = urlInput.val(); // Obtém a nova URL
                    eel.updateWebCommand(oldCommand, newCommand, newUrl)(); // Atualiza o comando da web
                    commandInput.prop('readonly', true); // Torna o campo somente leitura
                    urlInput.prop('readonly', true); // Torna o campo somente leitura
                    $(this).removeClass('btn-success save-web-command').addClass('btn-warning edit-web-command').text('Editar');
                    row.data('command', newCommand); // Atualiza o comando nos dados da linha
                });
            });
        });
    }

    // Função para carregar e exibir os comandos do Windows
    function loadWindowsCommands() {
        eel.getWindowsCommands()().then(commands => {
            $("#savedWindowsCommands").empty(); // Limpa a lista de comandos salvos
            commands.forEach(command => {
                // Adiciona cada comando à lista de comandos salvos
                $("#savedWindowsCommands").append(`
                    <div class="row mb-2 command-row" data-command="${command.command}">
                        <div class="col-4">
                            <input type="text" class="form-control command-input" value="${command.command}" readonly>
                        </div>
                        <div class="col-4">
                            <input type="text" class="form-control path-input" value="${command.path}" readonly>
                        </div>
                        <div class="col-2">
                            <button class="btn btn-warning edit-windows-command">Editar</button>
                        </div>
                        <div class="col-2">
                            <button class="btn btn-danger delete-windows-command">Excluir</button>
                        </div>
                    </div>
                `);
            });

            // Adiciona evento de clique para os botões de exclusão
            $(".delete-windows-command").click(function() {
                let row = $(this).closest('.command-row');
                let command = row.data('command');
                eel.deleteWindowsCommand(command)(); // Exclui o comando do Windows
                row.remove(); // Remove a linha da lista
            });

            // Adiciona evento de clique para os botões de edição 
            $(".edit-windows-command").click(function() {
                let row = $(this).closest('.command-row');
                let commandInput = row.find('.command-input');
                let pathInput = row.find('.path-input');
                let oldCommand = commandInput.val();

                commandInput.prop('readonly', false); // Torna o campo editável
                pathInput.prop('readonly', false); // Torna o campo editável
                $(this).removeClass('btn-warning edit-windows-command').addClass('btn-success save-windows-command').text('Salvar');

                // Adiciona evento de clique para o botão Salvar
                row.find('.save-windows-command').click(function() {
                    let newCommand = commandInput.val(); // Obtém o novo comando
                    let newPath = pathInput.val(); // Obtém o novo caminho
                    eel.updateWindowsCommand(oldCommand, newCommand, newPath)(); // Atualiza o comando do Windows
                    commandInput.prop('readonly', true); // Torna o campo somente leitura
                    pathInput.prop('readonly', true); // Torna o campo somente leitura
                    $(this).removeClass('btn-success save-windows-command').addClass('btn-warning edit-windows-command').text('Editar');
                    row.data('command', newCommand); // Atualiza o comando nos dados da linha
                });
            });
        });
    }
});
