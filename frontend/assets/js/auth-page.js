// Variables
const btnSignIn_Up= document.querySelector('#btn-signUp-signIn');
const signIn_Up_model= document.querySelector('.signIn-join-model');
const btn_close_model= document.querySelector('.btn-close');
const tabSwitch = document.querySelectorAll('.tab > ul > li');
const signInForm= document.querySelector('.sign-in-form');
const signUpForm= document.querySelector('.sign-up-form');
const footerSignIn= document.querySelector('.l-s-container > div:nth-child(3)');
const footerSignUp= document.querySelector('.l-s-container > div:last-child');
const signInSwitchToSignUp= document.querySelector('#btn-signUp');
const signUpSwitchToSignIn= document.querySelector('#btn-signIn');


//Event listners

// Event listner to activate modal
btnSignIn_Up.addEventListener('click', () => {
    signIn_Up_model.classList.remove('modal-fade-out');
    signIn_Up_model.classList.add('modal-fade-in');
});

// Event listner to deactivate modal
btn_close_model.addEventListener('click', () => {
    signIn_Up_model.classList.replace('modal-fade-in', 'modal-fade-out');
})

// Event listner to toggle signIn and signUp switch
tabSwitch.forEach(item => {
    item.addEventListener('click', () => {
        tabSwitch.forEach(item => {
            item.classList.remove('active')
        })
        item.classList.add('active')
        if (item.id == 'signUp') {
            signInForm.classList.remove('active');
            signUpForm.classList.add('active');
            footerSignUp.style.display= 'flex';
            footerSignIn.style.display= 'none';
        }else if (item.id == 'signIn') {
            signUpForm.classList.remove('active');
            signInForm.classList.add('active');
            footerSignUp.style.display= 'none';
            footerSignIn.style.display= 'flex';
        }else {
            console.log();
        }
    })
})



// Handling content switch with the footer
signInSwitchToSignUp.addEventListener('click', () => {
    const signInTab= document.querySelector('.tab > ul > li:first-child')
    const signUpTab= document.querySelector('.tab > ul > li:last-child')

    // Toggling the active
    signInTab.classList.remove('active')
    signUpTab.classList.add('active')

    // Toggling the active form
    signInForm.classList.remove('active');
    signUpForm.classList.add('active');

    // Toggling the active footer
    footerSignUp.style.display= 'flex';
    footerSignIn.style.display= 'none';
})

signUpSwitchToSignIn.addEventListener('click', () => {
    const signInTab= document.querySelector('.tab > ul > li:first-child')
    const signUpTab= document.querySelector('.tab > ul > li:last-child')
    // Toggling the active
    signInTab.classList.add('active')
    signUpTab.classList.remove('active')

    // Toggling the active form
    signInForm.classList.add('active');
    signUpForm.classList.remove('active');

    // Toggling the active footer
    footerSignUp.style.display= 'none';
    footerSignIn.style.display= 'flex';
})