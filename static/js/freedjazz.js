window.addEventListener("load", (e) => {
  let previewDiv = document.querySelector("#songPreview");
  if (previewDiv) {
    if (localStorage.getItem("showPreviews")) {
      let previewImg = document.querySelector("#songPreview img");
      previewImg.src = previewImg.dataset.src;
    } else {
      let notice = document.createElement("p");
      notice.innerHTML =
        'Previews are not shown by default, in case the song is not in the public domain in your jurisdiction. <a href="javascript:enablePreviews();">Enable previews</a>';
      previewDiv.appendChild(notice);
    }
  }
});

function enablePreviews() {
  localStorage.setItem("showPreviews", "true");
  window.reload();
}
