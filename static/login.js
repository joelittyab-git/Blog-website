window.addEventListener("load", function(){
    const reqButton = document.getElementById("btn-req-holder");

    const loading_tag = document.createElement("i");
    loading_tag.classList.add("fa");
    loading_tag.classList.add("fa-spinner");
    loading_tag.classList.add("fa-spin");

    reqButton.addEventListener("click", function(){
        reqButton.classList.add("buttonload");
        reqButton.appendChild(loading_tag);
        if(
            (document.getElementById("email-entry").value == "" ||
            document.getElementById("password-entry").value == "") &&
            document.getElementById("err-msg-otth").innerHTML == ""

        ){
            document.getElementById("err-msg").innerHTML = "Please enter all the fields.";
            setTimeout(() => {
                document.getElementById("err-msg").innerHTML = "";
            }, 3000
            );
        }else{
            reqButton.disabled = true;
            document.getElementById("login-form").submit();
        }
        setTimeout(
            () =>{
                reqButton.disabled = false;
                reqButton.value = 'Submit';
            },
            3000
        )
    
        
    });
});

