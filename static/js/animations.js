// Animación para el boton de carga de archivos
if (document.getElementById("btn-upload")) {
  const btnFile = document.getElementById("btn-upload");
  const uploadFile = document.getElementById("LoadFile");
  uploadFile.addEventListener("change", () => {
    btnFile.disabled =
      uploadFile.files.length === 0 || uploadFile.files.length > 7;
  });
  btnFile.addEventListener("click", function () {
    var container = document.getElementById("loaderContainer");
    container.style.display = "block";
  });
}
function displaySelectedFiles() {
  //Identificación de archivos
  const inputElement = document.getElementById("LoadFile");
  const fileNamesElement = document.getElementById("fileNames");

  // Verificar si se han seleccionado archivos
  if (inputElement.files.length > 0 && inputElement.files.length < 7) {
    // Crear una lista de nombres de archivo
    const fileNames = Array.from(inputElement.files).map((file) => file.name);
    // Mostrar los nombres de archivo en un elemento HTML
    fileNamesElement.innerHTML = `<strong>Archivos seleccionados:</strong> ${fileNames.join(
      ", "
    )}`;
  } else {
    // Si no se han seleccionado archivos, borrar el contenido
    fileNamesElement.innerHTML = "Selecciona máximo 6 archivos";
  }
}
