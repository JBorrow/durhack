// This is where it all goes :)

window.onload = function () {
	days = ['monday', 'tuesday', 'weds'];
	weather_pics = ['sun-o', 'bolt', 'cloud'];
	weather_temps = [22, 23, 23];
	ffall = [2123, 1231, 2343];
	ffallpc = [22, 22, 24];

	pages = ['silva', 'x'];

        silva_data = pretty_data(days, weather_pics, weather_temps, ffall, ffallpc);
	document.getElementById('silva_data').innerHTML = silva_data;
	document.getElementById('x_data').innerHTML = silva_data;

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

function pretty_data(days, weather_types, weather_temps, ffall, ffall_pc) {
  // Prints the data prettily into your id :)
  data_op = ""
  for (var i=0; i < days.length; i++) {
    this_data = "<div class='vbox my2'><div class='flex justify-between'><div class='day'>" + days[i] + "</div><div class='weather'><i class='fa fa-" + weather_types[i] + " fa-lg'></i> " + weather_temps[i] + " C</div><div class='footfall'>" + ffall[i] + " (" + ffall_pc[i] + ")</div></div></div>";
    data_op += this_data;
  }
  return data_op;
}
