var boton = document.getElementById("btn-ask");
boton.addEventListener("click", async function () {
  var container = document.getElementById("loaderContainer");
  var askrender = document.getElementById("askrender");
  container.style.display = "block";
  var question = document.getElementById("questionModel");
  const gpt = {
    question: question.value,
  };
  document.getElementById("questionModel").textContent = "";
  //https://gptaudit.azurewebsites.net/gpt for azure development - http://localhost:5000/gpt for local development
  await fetch("http://localhost:5000/gpt", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(gpt),
  })
    .then((response) => response.json())
    .then((data) => {
      askrender.innerHTML =
        '<h5 for="askModel">Respuesta del modelo GPT:</h5> <textarea class="form-control" disabled="true" id="askModel" rows="3"></textarea>';
      document.getElementById("askModel").textContent = data.answer;
    })
    .catch((error) => console.log(error));
  var pre_q = document.getElementById("pre-question");
  pre_q.innerHTML = `<h5 style="display: inline">Pregunta realizada: </h5><p style="display: inline">${question.value}</p>`;
  const btnAsk = document.getElementById("btn-ask");
  btnAsk.disabled = true;
  question.value = "";
  container.style.display = "none";
  pre_q.style.display = "block";
});
