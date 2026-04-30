(function () {
  function initEditors() {
    if (!window.ClassicEditor) {
      return;
    }

    document.querySelectorAll("textarea.ckeditor-textarea").forEach(function (textarea) {
      if (textarea.dataset.ckeditorReady) {
        return;
      }

      textarea.dataset.ckeditorReady = "true";
      window.ClassicEditor.create(textarea, {
        toolbar: [
          "heading",
          "|",
          "bold",
          "italic",
          "link",
          "bulletedList",
          "numberedList",
          "blockQuote",
          "|",
          "undo",
          "redo",
        ],
      }).catch(function (error) {
        console.error(error);
      });
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initEditors);
  } else {
    initEditors();
  }
})();
