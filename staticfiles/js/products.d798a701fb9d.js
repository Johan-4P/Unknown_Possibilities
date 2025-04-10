document.addEventListener("DOMContentLoaded", function () {
    const cards = document.querySelectorAll(".tarot-card");
    const revealSection = document.getElementById("card-reveal");
    const revealImg = document.getElementById("reveal-img");
    const revealName = document.getElementById("reveal-name");
    const revealMessage = document.getElementById("reveal-message");
  
    let cardDrawn = false;
  
    cards.forEach(card => {
      card.addEventListener("click", () => {
        if (cardDrawn) return;
  
        const name = card.dataset.name;
        const message = card.dataset.message;
        const imgSrc = card.dataset.img;
  
        revealImg.src = imgSrc;
        revealName.textContent = name;
        revealMessage.textContent = message;
  
        revealSection.classList.remove("d-none");
        cardDrawn = true;
  
        // Flip the selected card (optional visual)
        card.querySelector("img").src = imgSrc;
      });
    });
  });
  