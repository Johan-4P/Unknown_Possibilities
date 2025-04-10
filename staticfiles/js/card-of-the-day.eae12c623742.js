document.addEventListener('DOMContentLoaded', function () {
    const clicked = sessionStorage.getItem('cardPicked');
    const cards = document.querySelectorAll('.flip-card');
  
    if (clicked) {
      cards.forEach(card => card.classList.add('flipped'));
    
    }
    // Add event listeners to each card
    cards.forEach(card => {
      card.addEventListener('click', () => {
        if (sessionStorage.getItem('cardPicked')) return;
  
       
        card.classList.add('flipped');
  
        // Get the card's data attributes and set them in the modal
        document.getElementById('card-title').innerText = card.dataset.name;
        document.getElementById('card-message').innerText = card.dataset.message;
        document.getElementById('card-reveal').style.display = 'block';
  
   
        sessionStorage.setItem('cardPicked', true);
  
        // Disable all cards after one is clicked
        cards.forEach(c => c.style.pointerEvents = 'none');
      });
    });
  });
  