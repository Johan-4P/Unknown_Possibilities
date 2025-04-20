document.addEventListener('DOMContentLoaded', () => {
  console.log("✅ stripe_elements.js is running!");

  const publicKey = JSON.parse(document.getElementById('id_stripe_public_key').textContent);
  const clientSecret = JSON.parse(document.getElementById('id_client_secret').textContent);

  const stripe = Stripe(publicKey);
  const elements = stripe.elements();

  const card = elements.create('card', {
    style: {
      base: {
        color: '#ffffff',
        fontFamily: '"Poppins", "Helvetica Neue", sans-serif',
        fontSize: '16px',
        '::placeholder': {
          color: '#bbb',
        }
      },
      invalid: {
        color: '#ff6b6b',
        iconColor: '#ff6b6b'
      }
    }
  });

  card.mount('#card-element');

  // 🔍 Feedback vid input
  card.on('change', function(event) {
    const cardErrors = document.getElementById('card-errors');
    if (event.complete) {
      console.log("✅ Card entry complete");
      cardErrors.textContent = '';
    } else if (event.error) {
      console.log("❌ Stripe error:", event.error.message);
      cardErrors.textContent = event.error.message;
    } else {
      console.log("⌨️ Typing in card field...");
      cardErrors.textContent = '';
    }
  });

  const form = document.getElementById('payment-form');
  const submitButton = document.getElementById('submit-button');
  const cardErrors = document.getElementById('card-errors');

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    console.log("🧾 Intercepted form submit");

    form.classList.add('loading');
    submitButton.disabled = true;
    form.querySelectorAll('input, select, textarea, button').forEach(el => el.disabled = true);

    const { error, paymentIntent } = await stripe.confirmCardPayment(clientSecret, {
      payment_method: {
        card: card,
        billing_details: {
          name: document.getElementById('id_full_name')?.value || '',
          email: document.getElementById('id_email')?.value || '',
        }
      }
    });

    if (error) {
      console.log("❌ Payment error:", error.message);
      cardErrors.textContent = error.message;

      form.classList.remove('loading');
      submitButton.disabled = false;
      form.querySelectorAll('input, select, textarea, button').forEach(el => el.disabled = false);
    } else if (paymentIntent.status === 'succeeded') {
      console.log("💳 Payment succeeded – submitting form");

      // 🛡 Re-append CSRF token (safety net)
      const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]');
      if (csrfToken) {
        const hiddenInput = document.createElement('input');
        hiddenInput.setAttribute('type', 'hidden');
        hiddenInput.setAttribute('name', 'csrfmiddlewaretoken');
        hiddenInput.setAttribute('value', csrfToken.value);
        form.appendChild(hiddenInput);
      } else {
        console.warn("⚠️ CSRF token not found in DOM – this may cause a 403 error.");
      }

      form.submit();
    }
  });
});
