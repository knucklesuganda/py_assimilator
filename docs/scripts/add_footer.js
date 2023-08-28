
const footer = document.getElementsByClassName("md-footer-meta__inner md-grid")[0];

footer.innerHTML += `
<div style="display: flex">

    <div class="md-copyright">
        <a href="https://knucklesuganda.github.io/py_assimilator/management/privacy"
            target="_blank" rel="noopener">Privacy policy</a>
    </div>
    
    <div class="md-copyright">
        <a href="https://knucklesuganda.github.io/py_assimilator/management/terms.pdf"
            target="_blank" rel="noopener">Terms and conditions</a>
    </div>

</div>`;
