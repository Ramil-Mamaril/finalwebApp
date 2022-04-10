
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
				playAudioFile(e.target.result);
				console.log(("Filename: '" + files[0].name + "'"), ( "(" + ((Math.floor(files[0].size/1024/1024*100))/100) + " MB)" ));
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




var modal = document.getElementById("myModal");

// Get the button that opens the modal
var btn = document.getElementById("myBtn");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks on the button, open the modal
btn.onclick = function() {
  modal.style.display = "block";
  $('body').css('overflow', 'hidden');
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
  $('body').css('overflow', 'auto');
}


