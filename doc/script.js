function toggle_show(element) {
  var calculated_class_name = "only-" + element.value;
  var calculated_display = element.checked ? "initial" : "none";
  console.log(calculated_class_name + ": " + calculated_display);
  all_elements = document.getElementsByClassName(calculated_class_name);
  for (var i = 0; i < all_elements.length; ++i) {
    all_elements[i].style.display = calculated_display;
  }
}
