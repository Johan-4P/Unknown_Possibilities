document.addEventListener('DOMContentLoaded', function () {
  const today = new Date().toISOString().split('T')[0];
  const cards = document.querySelectorAll('.flip-card');
  const modal = document.getElementById('customModal');
  const modalName = document.getElementById('modal-card-name');
  const modalMessage = document.getElementById('modal-card-message');
  const modalImg = document.getElementById('modal-card-img');
  const resetBtn = document.getElementById('reset-card-draw');
  const closeModalBtn = document.querySelector('.close-modal');

  console.log("Page loaded, found", cards.length, "cards");

  cards.forEach(card => {
    const productId = card.dataset.product;
    const drawKey = `cardDrawn_product_${productId}`;

   
    if (localStorage.getItem(drawKey) === today) {
      card.classList.add('flipped');
      card.style.pointerEvents = 'none';
      console.log("Already drawn for product ID:", productId);
    }

    card.addEventListener('click', () => {
      if (localStorage.getItem(drawKey) === today) return;

      
      card.classList.add('flipped');
      localStorage.setItem(drawKey, today);
      card.style.pointerEvents = 'none';
      console.log("Card clicked:", drawKey);

     
      modalName.textContent = card.dataset.name;
      modalMessage.textContent = card.dataset.message;
      modalImg.src = card.dataset.img;
      modal.classList.remove('hidden');
    });
  });

  
  closeModalBtn.addEventListener('click', () => {
    modal.classList.add('hidden');
  });

 
  window.addEventListener('click', (e) => {
    if (e.target === modal) {
      modal.classList.add('hidden');
    }
  });

  
  if (resetBtn) {
    resetBtn.addEventListener('click', () => {
      cards.forEach(card => {
        const drawKey = `cardDrawn_product_${card.dataset.product}`;
        localStorage.removeItem(drawKey);
        card.classList.remove('flipped');
        card.style.pointerEvents = 'auto';
      });
      modal.classList.add('hidden');
      console.log("Card draw reset");
    });
  }
});
