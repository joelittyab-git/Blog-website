

 function closePopUp(){
  document.getElementById('profile-img-popup').style.visibility = 'hidden';
  document.getElementById('new-img').style.transitionDuration = '0s';
}

function openPopUp(){
  document.getElementById('profile-img-popup').style.visibility = 'visible';
}

function update(){
  document.getElementById('form-t').submit();
}


