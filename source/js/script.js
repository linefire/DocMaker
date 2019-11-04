var toggler = document.getElementsByClassName("caret");
var i;

for (i = 0; i < toggler.length; i++) {
  toggler[i].addEventListener("click", function() {
    this.parentElement.querySelector(".nested").classList.toggle("active");
    this.classList.toggle("caret-down");
  });
}

var saved_data = window.localStorage.getItem("tree");
if (saved_data != null) {
    saved_data = JSON.parse(saved_data);
    for (i = 0; i < this.toggler.length; i++) {
        if (saved_data[i]) {
            toggler[i].parentElement.querySelector('.nested').classList.toggle("active");
            toggler[i].classList.toggle("caret-down");
        }
    }
}

window.onbeforeunload = function(e) {
    var save_data = [];
    for (i = 0; i < this.toggler.length; i++) {
        save_data.push(this.toggler[i].classList.contains("caret-down"));
    }
    window.localStorage.setItem("tree", this.JSON.stringify(save_data));
};