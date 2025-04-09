document.addEventListener('DOMContentLoaded', function () {
    const clicked = sessionStorage.getItem('cardPicked');
    const cards = document.querySelectorAll('.card-of-the-day');

    if (clicked) {
        cards.forEach(card => card.style.pointerEvents = "none");
    }

    cards.forEach(card => {
        card.addEventListener('click', () => {
            if (sessionStorage.getItem('cardPicked')) return;

            // Flip animation
            card.style.transform = "rotateY(180deg)";
            card.innerHTML = `
                <div class="mystic-content">
                    <h4 class="mystic-title">${card.dataset.title}</h4>
                    <p class="mystic-text">${card.dataset.message}</p>
                </div>
            `;

            document.getElementById('card-title').innerText = card.dataset.title;
            document.getElementById('card-message').innerText = card.dataset.message;
            document.getElementById('card-reveal').style.display = "block";

            // Disable further clicks
            sessionStorage.setItem('cardPicked', true);
            cards.forEach(c => c.style.pointerEvents = "none");
        });
    });
});
