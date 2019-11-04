var toggler = document.getElementsByClassName("caret");
var i;
var save_data = [];

for (i = 0; i < toggler.length; i++) {
    save_data.push(false);
  toggler[i].addEventListener("click", function() {
    for (i = 0; i < toggler.length; i++) {
        save_data[i] = toggler[i].classList.contains("caret-down");
    }
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
    window.localStorage.setItem("tree", this.JSON.stringify(this.save_data));
};