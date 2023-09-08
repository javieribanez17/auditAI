var boton = document.getElementById("btn-ask");
boton.addEventListener("click", async function() {
    var container = document.getElementById("loaderContainer");
    container.style.display = "block";
    var question = document.getElementById("questionModel")
    const gpt = {
        question: question.value
    };
    document.getElementById("questionModel").textContent = "";
    await fetch("http://localhost:5000/gpt", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(gpt)
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("askModel").textContent = data.answer
    })
    .catch(error => console.log(error));
    var pre_q = document.getElementById("pre-question");
    pre_q.textContent = "Pregunta previa: " + question.value
    question.value = "";
    container.style.display = "none";
    pre_q.style.display = "block";
});