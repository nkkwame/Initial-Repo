// const paymentForm = document.getElementById('paymentForm');
const selectedPayment= document.querySelectorAll('.payment-method input')
const submitBtn= document.querySelector('#submit')
const el=document.querySelector('.otp')
const optBtn= document.querySelector('#opt-btn')
const refText= document.querySelector('#refrence-code')
const accountNumberInput = document.getElementById('account-number');
const cardNumberInput = document.getElementById('card-number');
  
    
// paymentForm.addEventListener("submit", payWithPaystack, false);
selectedPayment.forEach(x => {
  x.addEventListener('click', () => {
    console.log(x.value);
    const mf= document.querySelector('.momoForm')
    const bf= document.querySelector('.bankForm')
    if (x.value == 'Bank') {
        mf.style.display= 'none'
        bf.style.display= 'block'
    }else{
        mf.style.display= 'block'
        bf.style.display= 'none'
    }
  })
})

// Intiating transanction
submitBtn.addEventListener('click', (e) => {
  e.preventDefault()
  const email= document.getElementById('email-ad').value
  const phone= document.getElementById('accnumber').value
  const amount= document.getElementById('amount').value
  const carrier= document.getElementById('network-carriers').value
  console.log(email, phone, amount, carrier);
  $.ajax({
    type: 'POST',
    url: '/payment/intiate-transaction/',
    data:{
        email:email,
        phone: phone,
        amount: amount,
        carrier: carrier,
        csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
    },
    success: function(response) {
      console.log(response)
      if (response.data.status == "send_otp"){
        el.style.display= 'flex'
        refText.value= response.data.reference
      }else {
        el.style.display= 'none'
      }
      alert(response.data.display_text)
      },
    error: function(response) {
      alert('An error occurred');
    }
  });
});

// Submiting otp
optBtn.addEventListener('click', () => {
  const opt_code= $('#opt-text').val()
  $.ajax({
    type: 'POST',
    url: '/payment/firstTransaction/submit-otp/',
    data:{
      opt_code:opt_code,
      ref_code: refText.value,
      csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
    },
    success: function(response) {
      console.log(response)
      },
    error: function(response) {
      alert('An error occurred');
    }
  });
})

// Format account number
accountNumberInput.addEventListener('input', function() {
    let value = this.value.replace(/\D/g, ''); // removing all non digits characters
    const formattedValue = value.replace(/(\d{4})(\d{4})(\d{4})(\d{4})/g, '$1 $2 $3 $4'); // grouping them into four to reach 16 inputs, format them with space
    this.value = formattedValue;
  });

  // Format card number
  cardNumberInput.addEventListener('input', function() {
    let value = this.value.replace(/\D/g, '');
    const formattedValue = value.replace(/(\d{2})(\d{2})/, '$1 / $2');
    this.value = formattedValue;
  });