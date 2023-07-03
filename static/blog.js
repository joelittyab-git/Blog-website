window.addEventListener('load', function(){
    const redirect__button = document.getElementById('new-post-redirect');

    redirect__button.onclick = function(){
        window.location.href = 'http://localhost:1000/blogs/new-post'
    }
});