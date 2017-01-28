// This is where it all goes :)

window.onload = function () {
	pages = ['silva', 'x'];

	current_page = 0;

	display_pages(current_page);
}

function display_pages(page) {
  for (var i=0; i < pages.length; i++) {
    console.log(pages[i])
    if (i == page) {
      document.getElementById(pages[i]).style.display = "block";
    } else {
      document.getElementById(pages[i]).style.display = "none";
    }
  }
}

function right() {
  if (current_page + 1 < pages.length) {
    current_page += 1;
    display_pages(current_page);
  }
}

function left() {
  if (current_page - 1 >= 0) {
    current_page -= 1;
    display_pages(current_page);
  }
}

