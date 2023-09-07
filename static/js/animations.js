if (document.getElementById("btn-upload")) {
  const btnFile = document.getElementById("btn-upload");
  const uploadFile = document.getElementById("LoadFile");
  uploadFile.addEventListener("change", () => {
    btnFile.disabled = uploadFile.files.length === 0;
  });
  btnFile.addEventListener("click", function () {
    var container = document.getElementById("loaderContainer");
    container.style.display = "block";
  });
}
