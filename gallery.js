const dialog = document.querySelector('dialog');
const largeImage = dialog.querySelector('img');
document.querySelectorAll('.photo').forEach(link => {
  link.addEventListener('click', event => {
    if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    event.preventDefault();
    largeImage.src = link.href;
    largeImage.alt = link.querySelector('img').alt;
    dialog.querySelector('p').textContent = largeImage.alt;
    dialog.showModal();
  });
});
dialog.querySelector('button').addEventListener('click', () => dialog.close());
dialog.addEventListener('click', event => {
  if (event.target === dialog) {
    const bounds = dialog.getBoundingClientRect();
    if (event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom) dialog.close();
  }
});
