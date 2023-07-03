

    this.document.getElementById('logout_button').addEventListener('click', function() {
        document.getElementById('log-out-button').style.display= 'block';
        document.getElementById('close-pop-up').style.display= 'block';
        document.getElementById('pop-up').classList.toggle('action');
    });


    this.document.getElementById('close-pop-up').onclick = function() {
        document.getElementById('log-out-button').style.display= 'none';
        document.getElementById('close-pop-up').style.display= 'none';
        document.getElementById('logout_button').click();
    }

    this.document.getElementById('log-out-button').onclick = function() {
        window.location.href = 'http://localhost:1000/logout';
    }

