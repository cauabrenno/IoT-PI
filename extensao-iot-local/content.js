console.log("--- Extensão IoT Local Ativa ---");

// Observador que fica vigiando mudanças na página
const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
        if (mutation.addedNodes.length) {
            mutation.addedNodes.forEach((node) => {
                // Pega o texto que apareceu
                const texto = node.innerText || node.textContent;
                
                // Se o texto tiver o formato "id:...,umidade:..."
                if (texto && texto.includes("id:") && texto.includes("umidade:")) {
                    processarLinha(texto);
                }
            });
        }
    });
});

// Começa a vigiar o corpo da página
observer.observe(document.body, {
    childList: true,
    subtree: true,
    characterData: true
});

function processarLinha(linha) {
    try {
        // Limpa a linha
        linha = linha.trim();
        console.log("Lendo:", linha);

        // Formato esperado: id:1,umidade:500,vibracao:0,botao:0
        const partes = linha.split(',');
        const dados = {};
        
        partes.forEach(p => {
            const [chave, valor] = p.split(':');
            if(chave && valor) {
                dados[chave.trim()] = parseInt(valor.trim());
            }
        });

        // Monta o pacote
        const payload = {
            'sensor_id': dados.id,
            'field1': dados.umidade,
            'field2': dados.vibracao,
            'field3': dados.botao
        };

        // Manda para o background.js (o carteiro)
        chrome.runtime.sendMessage({
            tipo: "DADOS_SENSOR",
            payload: payload
        });

    } catch (e) {
        // Ignora erros de leitura (linhas incompletas, etc)
    }
}