var main = function () {
    "use strict";
    $(".comment-input button").on("click", function (event) {
        var $divPadre = $("<div>", { "class": "container p-3 my-3 border" });

        var $div1 = $("<div>");
        var nombre = document.getElementById("username");
        var $names = $("<p>").text(nombre.textContent);
        
        var $div2 = $("<div>", { "class": "container p-3 my-3 border" });
        var $comments = $("<p>").text($(".comment-input input").val());
        

        $($div2).append($comments);
        $($div1).append($names);
        $($divPadre).append($div1);
        $($divPadre).append($div2);
        $(".comments").append($divPadre);
    });
    cargarComentarios();
};
$(document).ready(main);
