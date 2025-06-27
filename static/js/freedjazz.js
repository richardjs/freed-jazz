window.addEventListener("load", (e) => {
  let previewDiv = document.querySelector("#songPreview");
  if (previewDiv) {
    if (localStorage.getItem("showPreviews")) {
      let previewImg = document.querySelector("#songPreview img");
      previewImg.src = previewImg.dataset.src;
    } else {
      let notice = document.createElement("p");
      notice.innerHTML =
        'Previews are disabled by default because copyright laws vary by country. Only enable previews if you are located in the United States. <a href="javascript:enablePreviews();">Enable previews</a>';
      previewDiv.appendChild(notice);
    }
  }

  if (localStorage.getItem("hideCopyightWarning")) {
      let copyrightWarning = document.querySelector("#copyrightWarning");
      copyrightWarning.style.display = "none";
  }
});

function enablePreviews() {
  localStorage.setItem("showPreviews", "true");
  location.reload();
}

function hideCopyightWarning() {
  localStorage.setItem("hideCopyightWarning", "true");
  let copyrightWarning = document.querySelector("#copyrightWarning");
  copyrightWarning.style.display = "none";
}
