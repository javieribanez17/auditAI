if(document.getElementById("btn-ask")){
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
  await fetch("https://gptaudit.azurewebsites.net/gpt", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(gpt),
    })
      .then((response) => response.json())
      .then((data) => {
        askrender.innerHTML =
        '<div id="test"><h5 for="questionModel">Respuesta del modelo</h5><form action="/" method="get"><button style="margin-bottom: 5px;" type="submit" class="btn btn-outline-secondary consult close"aria-label="Close">Borrar archivos</button></form></div> <textarea class="form-control" disabled="true" id="askModel" rows="3"></textarea>';
      document.getElementById("askModel").textContent = data.answer;
      })
      .catch((error) => console.log(error));
    var pre_q = document.getElementById("pre-question");
    pre_q.innerHTML = `<h5>Consulta anterior: </h5><p style="display: inline">"${question.value}"</p>`;
    const btnAsk = document.getElementById("btn-ask");
    btnAsk.disabled = true;
    question.value = "";
    container.style.display = "none";
    pre_q.style.display = "block";
  });
}


if(document.getElementById('login-btn')){
  var loginBtn = document.getElementById('login-btn');
  loginBtn.addEventListener("click", function(){
    var user = document.getElementById("btn-user");
    var password = document.getElementById("btn-password");
    const userData = {
      user: user.value,
      password: password.value
    }
    fetch("http://localhost:5000/login", {
      method: "POST",
      headers: {
        "Content-type": "application/json"
      },
      body: JSON.stringify(userData),
    })
    .then(response => {
      if(response.status === 200){
        window.location.href = response.url;
      }else {
        alert("error")
      }
      
    })
  })
}


