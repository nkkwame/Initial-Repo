const displaySmallScreenNav= document.getElementById('show-nav');
const displaySmallScreenNavIcon= document.querySelector('#show-nav > i')
const linksModalSm= document.querySelector('.links-modal');
const linksContainer= document.querySelector('.links-small-screens');

let isOpen= false
//Event listners
displaySmallScreenNav.addEventListener('click', () => {
    if (isOpen) {
        linksModalSm.classList.remove('modal-fade-in');
        linksModalSm.classList.add('modal-fade-out');
        linksContainer.classList.remove('links-slide-in');
        displaySmallScreenNavIcon.classList.replace('ri-close-large-fill','ri-menu-3-line' )
    }else {
        linksModalSm.classList.remove('modal-fade-out');
        linksModalSm.classList.add('modal-fade-in');
        linksContainer.classList.add('links-slide-in');
        displaySmallScreenNavIcon.classList.replace('ri-menu-3-line','ri-close-large-fill' )
    }

    isOpen=!isOpen;
});


