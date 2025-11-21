// Ouve mensagens vindas da página do Tinkercad (content.js)
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.tipo === "DADOS_SENSOR") {
        
        // Envia para o seu servidor local
        fetch("http://127.0.0.1:5000/dados", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(request.payload)
        })
        .then(response => {
            if (response.ok) console.log("✅ Sucesso ao enviar para localhost");
            else console.log("❌ Erro do servidor:", response.status);
        })
        .catch(error => console.log("❌ Erro de conexão local:", error));
    }
});