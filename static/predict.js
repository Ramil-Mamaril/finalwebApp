function handleFiles(event) {
  var files = event.target.files;
  $("#src").attr("src", URL.createObjectURL(files[0]));
  document.getElementById("audio").load();
}

document.getElementById("file").addEventListener("change", handleFiles, false);


var coll = document.getElementsByClassName("collapsible");
var i;

for (i = 0; i < coll.length; i++) {
  coll[i].addEventListener("click", function() {
    this.classList.toggle("active");
    var content = this.nextElementSibling;
    if (content.style.maxHeight){
      content.style.maxHeight = null;
    } else {
      content.style.maxHeight = content.scrollHeight + "px";
    }
  });
}
const hamburger = document.querySelector('.header .nav-bar .nav-list .hamburger');
const mobile_menu = document.querySelector('.header .nav-bar .nav-list ul');
const menu_item = document.querySelectorAll('.header .nav-bar .nav-list ul li a');
const header = document.querySelector('.header.container');

hamburger.addEventListener('click', () => {
  hamburger.classList.toggle('active');
  mobile_menu.classList.toggle('active');
});

document.addEventListener('scroll', () => {
  var scroll_position = window.scrollY;
  if (scroll_position > 250) {
    header.style.backgroundColor = '#29323c';
  } else {
    header.style.backgroundColor = '#29323c';
  }
});

menu_item.forEach((item) => {
  item.addEventListener('click', () => {
    hamburger.classList.toggle('active');
    mobile_menu.classList.toggle('active');
  });
});


let button = document.querySelector(".subBtn");


function readFile(files) {
		var fileReader = new FileReader();
			fileReader.readAsArrayBuffer(files[0]);
			fileReader.onload = function(e) {
				button.style.cursor = "pointer";
				button.disabled = false;
				button.style.display = "inline-block";

			}
	}
	function playAudioFile(file) {
		var context = new window.AudioContext();
			context.decodeAudioData(file, function(buffer) {
				var source = context.createBufferSource();
					source.buffer = buffer;
					source.loop = false;
					source.connect(context.destination);
					source.start(0);
			});
	}




