function freeman() {
    setInterval(function() {
        var cat = document.createElement("div");
        cat.className = "cat";
        var width = Math.floor(Math.random() * 200 + 100);
        var height = Math.floor(Math.random() * 200 + 50);
        var startLeft = Math.floor(Math.random() * screen.width);
        var startTop = Math.floor(Math.random() * screen.height);
        var img = document.createElement("img");
        img.setAttribute("width", width);
        img.setAttribute("height", height);
        img.setAttribute(
            "src",
            "https://morganfillman.space/" + width + "/" + height
        );
        cat.style["position"] = "fixed";
        cat.style["margin-left"] = startLeft + "px";
        cat.appendChild(img);
        document.getElementsByTagName("body")[0].appendChild(cat);
        setTimeout(function() {
            cat.style.top = startTop + "px";
        }, 100);
    }, 1000);
}

export default freeman;
