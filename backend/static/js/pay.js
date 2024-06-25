// const paymentForm = document.getElementById('paymentForm');
// const selectedPayment= document.querySelectorAll('.payment-method input')
// const submitBtn= document.querySelector('#submit')
// const el=document.querySelector('.otp')
// const optBtn= document.querySelector('#opt-btn')
// const refText= document.querySelector('#refrence-code')
const accountNumberInput = document.getElementById('account-number');
const DoBInput = document.getElementById('birth-day');
const bkPay= document.getElementById('submitbk')
  
    
// paymentForm.addEventListener("submit", payWithPaystack, false);
// selectedPayment.forEach(x => {
//   x.addEventListener('click', () => {
//     const mf= document.querySelector('.momoForm')
//     const bf= document.querySelector('.bankForm')
//     if (x.value == 'Bank') {
//         mf.style.display= 'none'
//         bf.style.display= 'block'
//     }else{
//         mf.style.display= 'block'
//         bf.style.display= 'none'
//     }
//   })
// })

// Intiating transanction
// submitBtn.addEventListener('click', (e) => {
//   e.preventDefault()
//   const email= document.getElementById('email-ad').value
//   const phone= document.getElementById('accnumber').value
//   const amount= document.getElementById('amount').value
//   const carrier= document.getElementById('network-carriers').value
//   console.log(email, phone, amount, carrier);
//   $.ajax({
//     type: 'POST',
//     url: '/payment/intiate-Momo-transaction/',
//     data:{
//         email:email,
//         phone: phone,
//         amount: amount,
//         carrier: carrier,
//         csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
//     },
//     success: function(response) {
//       console.log(response)
//       if (response.data.status == "send_otp"){
//         el.style.display= 'flex'
//         refText.value= response.data.reference
//       }else {
//         el.style.display= 'none'
//       }
//       alert(response.data.display_text)
//       },
//     error: function(response) {
//       alert('An error occurred');
//     }
//   });
// });

// Submiting otp
// optBtn.addEventListener('click', () => {
//   const opt_code= $('#opt-text').val()
//   $.ajax({
//     type: 'POST',
//     url: '/payment/first-Momo-Transaction/submit-otp/',
//     data:{
//       opt_code:opt_code,
//       ref_code: refText.value,
//       csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
//     },
//     success: function(response) {
//       console.log(response)
//       },
//     error: function(response) {
//       alert('An error occurred');
//     }
//   });
// })

// Format account number
accountNumberInput.addEventListener('input', function() {
    let value = this.value.replace(/\D/g, ''); // removing all non digits characters
    const formattedValue = value.replace(/(\d{4})(\d{4})(\d{4})(\d{4})/g, '$1 $2 $3 $4'); // grouping them into four to reach 16 inputs, format them with space
    this.value = formattedValue;
  });

  // Format card number
  DoBInput.addEventListener('input', function() {
    let value = this.value.replace(/\D/g, '');
    const formattedValue = value.replace(/(\d{4})(\d{2})(\d{2})/, '$1-$2-$3');
    this.value = formattedValue;
  });

  bkPay.addEventListener('click', () => {
    let acNumber= document.getElementById('account-number').value.split(' ')
    const DoB= document.getElementById('birth-day').value
    const amount= document.getElementById('amountBk').value
    const bankName= document.getElementById('bank-name').value
    acNumber= acNumber.join('')

    $.ajax({
      type: 'POST',
      url: '/payment/intiate-Bank-transaction/',
      data:{
       accountNumber: acNumber,
       dob: DoB,
       amount: amount,
       bank: bankName,
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


  var paymentForm = document.getElementById('paymentForm');
  paymentForm.addEventListener('submit', payWithPaystack, false);
  function payWithPaystack(e) {
    e.preventDefault();
    var handler = PaystackPop.setup({
      key: 'pk_test_3726cb3381554b0c4013bf04bac900e83b5816fd', // Replace with your public key
      email: document.getElementById('email-address').value,
      amount: document.getElementById('amount').value * 100, // the amount value is multiplied by 100 to convert to the lowest currency unit
      currency: 'GHS', // Use GHS for Ghana Cedis or USD for US Dollars
      first_name: document.getElementById('first-name').value,
      last_name: document.getElementById('last-name').value,
      // phone: document.getElementById('phone-number').value,
      // address: {
      ref: ''+Math.floor((Math.random() * 1000000000) + 1), // Replace with a reference you generated
      callback: function(response) {
        //this happens after the payment is completed successfully
        var reference = response.reference;
        console.log(response);
        // Making an AJAX call to server with the reference to verify the transaction
        $.ajax({
          type: 'GET',
          url: `/payment/verifyDeposite/${parseInt(reference)}/`,
          // data:{
          //  accountNumber: acNumber,
          //  dob: DoB,
          //  amount: amount,
          //  bank: bankName,
          //   csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
          // },
          success: function(response) {
            console.log('verify response');
            console.log(response)
            window.location.href = '/payment/successful-transaction/'; // Redirect to success page with
            },
          error: function(response) {
            alert('An error occurred');
          }
        });
      },
      onClose: function() {
        alert('Transaction was not completed, window closed.');
      },
    });
    handler.openIframe();
  }  
