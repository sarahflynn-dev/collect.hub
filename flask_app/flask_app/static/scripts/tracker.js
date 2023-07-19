document.getElementById("fav").onclick = function() {switchHeart()};

    function switchHeart() {
        if (document.getElementById("fav").innerHTML == '<a class="link-light"><i class="bi bi-heart"></i></a>'){
            document.getElementById("fav").innerHTML = '<a class="link-light"><i class="bi bi-heart-fill"></i></a>';
        } else {
            document.getElementById("fav").innerHTML = '<a class="link-light"><i class="bi bi-heart"></i></a>';
        }
    }