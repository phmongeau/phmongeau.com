var $ = function(sel, element) {
    if(element) {
        return Array.prototype.slice.call(element.querySelectorAll(sel));
    }
    else {
        return Array.prototype.slice.call(document.querySelectorAll(sel));
    }
}

var z = $(".zoom")[0];
var c = document.getElementById("imgContainer");
var d = document.getElementById("desc");

activeImg = null;

z.onclick = function(evt) {
    z.style.display = "none";
    c.style.display = "none";
    z.src = "";
}
c.onclick = z.onclick;



function showImg(img){
    z.src = img.src;
    z.style.display = "block";
    c.style.display = "block";

    activeImg = img;
    //set description
    try {
        var fig = img.parentElement.parentElement;
        d.innerHTML = fig.querySelector("figcaption").innerHTML;
    }
    catch (e) {
        d.innerHTML = "";
    }
}

$("#portfolio .thumbs img").forEach(function(v, i, a) {
    v.onclick = function(evt) {
        if(z.style.display == "none") {
            showImg(this);

        }

        evt.preventDefault();
    }
});

function parentLi(el) {
    var c = el;
    while (c.tagName !== "LI") {
        c = c.parentElement;
    }
    return c;
}

function next() {
    nextLi = parentLi(activeImg);
    if (nextLi.classList.contains("last"))
        img= activeImg;
    else
        img = $("img", nextLi.nextElementSibling)[0];

    showImg(img);
}
function prev() {
    nextLi = parentLi(activeImg);
    if (nextLi.classList.contains("first"))
        img= activeImg;
    else
        img = $("img", nextLi.previousElementSibling)[0];

    showImg(img);
}

document.getElementById("next").onclick = function(e) { 
    e.preventDefault();
    e.stopPropagation();
    next();
}
document.getElementById("prev").onclick = function(e) {
    e.preventDefault();
    e.stopPropagation();
    prev();
}

function clearClass(cls) {
    $("." + cls).forEach(function(v,i,a) {
        v.classList.remove(cls);
    });
}

function lightsOff(state) {
    var h = $("header")[0];
    if(state) {
        document.body.classList.add("dark");
        h.classList.add("semi-transp");
    }
    else {
        document.body.classList.remove("dark");
        h.classList.remove("semi-transp");
    }
}

window.onload = function() {
    if (window.location.hash === "") {
        window.location.hash = "portfolio";
    }
    window.onhashchange();
};

window.onhashchange = function() {
    clearClass('active');

    menuItem = $(".nav a[href='"+window.location.hash+"']")[0];
    if(menuItem) {
        menuItem.parentElement.classList.add('active');
    }

    if (window.location.hash === "#lesiege") {
        lightsOff(true);
    }
    else {
        lightsOff(false);
        // stop video
        var c = $("#video")[0].innerHTML;
        $("#video")[0].innerHTML = c;
    }
};
