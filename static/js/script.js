// Live character counter for the suggestion textarea.
document.addEventListener("DOMContentLoaded", function () {
  const textarea = document.getElementById("message");
  const counter = document.querySelector(".char-count");

  if (textarea && counter) {
    const max = parseInt(counter.dataset.max, 10) || 2000;

    const update = () => {
      counter.textContent = `${textarea.value.length} / ${max}`;
    };

    update();
    textarea.addEventListener("input", update);
  }
});
