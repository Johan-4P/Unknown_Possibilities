// static/js/stripe_elements.js
document.addEventListener('DOMContentLoaded', () => {
    // 1) Fetch your keys from the JSON blocks in the template
    const publicKey = JSON.parse(document.getElementById('id_stripe_public_key').textContent);
    const clientSecret = JSON.parse(document.getElementById('id_client_secret').textContent);
  
    // 2) Initialize Stripe.js and the Elements instance
    const stripe = Stripe(publicKey);
    const elements = stripe.elements();
  
    // 3) Create and mount the card Element
    const style = {
      base: {
        color: '#fff',
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': { color: '#bbb' }
      },
      invalid: { color: '#e5424d', iconColor: '#e5424d' }
    };
    const card = elements.create('card', { style: style });
    card.mount('#card-element');
  
    // 4) Real-time validation errors
    card.on('change', ({ error }) => {
      const errDiv = document.getElementById('card-errors');
      errDiv.textContent = error ? error.message : '';
    });
  
    // 5) Handle the form submission
    const form = document.getElementById('payment-form');
    form.addEventListener('submit', async (ev) => {
      ev.preventDefault();
  
      // disable the card and button
      card.update({ disabled: true });
      form.querySelector('button').disabled = true;
  
      // Confirm the PaymentIntent with card details
      const { error, paymentIntent } = await stripe.confirmCardPayment(clientSecret, {
        payment_method: {
          card: card,
          billing_details: {
            name: document.getElementById('id_full_name').value,
            email: document.getElementById('id_email').value,
          },
        }
      });
  
      if (error) {
        // Show error and re-enable
        document.getElementById('card-errors').textContent = error.message;
        card.update({ disabled: false });
        form.querySelector('button').disabled = false;
      } else if (paymentIntent && paymentIntent.status === 'succeeded') {
        // Everything went well — submit the Django form
        form.submit();
      }
    });
  });
  