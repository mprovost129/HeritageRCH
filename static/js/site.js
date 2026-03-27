(function () {
  const forms = document.querySelectorAll("form[data-portal-form]");
  forms.forEach(function (form) {
    form.querySelectorAll("input, select, textarea").forEach(function (el) {
      if (el.type === "hidden") return;
      if (el.type === "checkbox") {
        if (!el.classList.contains("form-check-input")) el.classList.add("form-check-input");
        return;
      }
      if (el.tagName === "SELECT") {
        if (!el.classList.contains("form-select")) el.classList.add("form-select");
        return;
      }
      if (!el.classList.contains("form-control")) el.classList.add("form-control");
    });
  });
})();
