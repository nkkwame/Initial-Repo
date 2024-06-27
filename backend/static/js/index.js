const copyBtn = document.getElementById('cp-reflink');

copyBtn.addEventListener('click', () => {
    const refLink = document.getElementById('ref-link').textContent;
    console.log(refLink);
    navigator.clipboard.writeText(refLink);
    alert('Referral link copied to clipboard!');
    window.location.reload();  // Reload the page to update the referral link in the clipboard
});