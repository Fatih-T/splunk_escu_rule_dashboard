document.addEventListener("DOMContentLoaded", function () {
  const selectAll = document.getElementById("select-all");
  const checkboxes = document.querySelectorAll(".row-checkbox");
  const actionBar = document.getElementById("bulk-action-bar");
  const countLabel = document.getElementById("selected-count");
  function updateBar() {
    const checked = document.querySelectorAll(".row-checkbox:checked");
    if (countLabel) countLabel.textContent = checked.length + " kural seçildi";
    if (actionBar) actionBar.style.display = checked.length > 0 ? "flex" : "none";
  }
  if (selectAll) {
    selectAll.addEventListener("change", function () {
      checkboxes.forEach(cb => { cb.checked = this.checked; });
      updateBar();
    });
  }
  checkboxes.forEach(cb => cb.addEventListener("change", updateBar));
});
