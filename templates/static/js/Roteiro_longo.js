document.getElementById("roteiroForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const dataInicio = document.getElementById("data_inicio").value;
    const dataFim = document.getElementById("data_fim").value;
    const preferenciasTexto = document.getElementById("preferencias").value;
    const preferenciasSelecionadas = preferenciasTexto.split(',').map(p => p.trim());

    try {
        const response = await fetch("http://127.0.0.1:8000/api/v1/roteiro/gerar-roteiro-longo/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                destino: "Belém do Pará",  // Valor fixo se destino for sempre Belém
                data_inicio: dataInicio,
                data_fim: dataFim,
                preferencias: preferenciasSelecionadas
            })
        });

        const resultado = await response.json();
        const resultadoDiv = document.getElementById("resultado");

        if (!response.ok) {
            resultadoDiv.innerText = resultado.erro || "Erro desconhecido ao gerar roteiro.";
        } else {
            resultadoDiv.innerText = resultado.roteiro;
        }

    } catch (erro) {
        document.getElementById("resultado").innerText = "Erro ao buscar roteiro: " + erro.message;
        document.getElementById("recarregar").innerHTML = "<button onclick='location.reload()'>Recarregar Página</button>";
    }
});
