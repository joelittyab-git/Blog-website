

window.addEventListener('load', function () {
    const password_field = document.getElementById('password_field');
    const msg_display_field = document.getElementById('password-error-field-js');

    password_field.addEventListener('keydown', (event) =>{
        entry = String(password_field.value);
        let counter = 0;

        

        for(let a  = 0; a < entry.length; a++){
            ascii_val = entry.charCodeAt(a);

            if(ascii_val >= 65 && ascii_val <= 90){
                counter += 1.5;
            }else if(ascii_val >= 97 && ascii_val<=122){
                counter ++;
            }
            else{
                counter += entry.length/2;
            }
        }

        if(counter<=entry.length){
            msg_display_field.style.color = 'red';
            msg_display_field.innerHTML = 'Password strength: Weak';
        }else if(counter<=(entry.length + entry.length/2)){
            msg_display_field.style.color = 'yellow';
            msg_display_field.innerHTML = 'Password strength: Moderate';
        }else{
            msg_display_field.style.color = 'limegreen';
            msg_display_field.innerHTML = 'Password strength: Strong';
        }
    });
});