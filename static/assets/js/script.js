const header = document.querySelector("header");

window.addEventListener("scroll", () => {
  header.classList.toggle("sticky", window.scrollY > 0);
});

const headerMenu = document.querySelector(".header__menu"),
  menuBtn = document.querySelector(".menu-btn"),
  headerMenuItems = headerMenu.querySelectorAll("li a");

menuBtn.addEventListener("click", () => {
  headerMenu.classList.toggle("show");
});

headerMenuItems.forEach((item) => {
  item.addEventListener("click", () => {
    headerMenu.classList.remove("show");
  });
});

// //-- DROPDOWN MENU NAVBAR --//

// const dropdowns = document.querySelectorAll(".dropdown");

// //Loop through all dropdown elements
// dropdowns.forEach((dropdown) => {
//   // Get inner elements from each dropdown
//   const select = dropdown.querySelector(".select");
//   const caret = dropdown.querySelector(".caret");
//   const menu = dropdown.querySelector(".menu");
//   const options = dropdown.querySelectorAll(".menu li");
//   const selected = dropdown.querySelector(".selected");
// });

// /*

// we are using this method in order to have
// multiple dropdown menus on the page work

// */

// //Add a click event to the select element
// select.addEventListener("click", () => {
//   //Add the clicked select styles to the select element
//   select.classList.toggle("select-clicked");
//   //Add the rotate styles to the caret element
//   caret.classList.toggle("caret-rotate");
//   //Add the open styles to the menu element
//   menu.classList.toggle("menu-open");
// });

// //Loop through all option elements
// options.forEach((option) => {
//   //Add a click event to the option element
//   option.addEventListener("click", () => {
//     //Change selected inner text to clicked option inner text
//     selected.innerText = option.innerText;
//     //Add the clicked select styles to the select element
//     select.classList.remove("select-clicked");
//     //Add the rotate styles to the caret element
//     caret.classList.remove("caret-rotate");
//     //Add the open styles to the menu element
//     menu.classList.remove("menu-open");
//     //remove active class from all option elements
//     options.forEach((option) => {
//       option.classList.remove("active");
//     });
//     //Add active class to clicked option element
//     option.classList.add("active");
//   });
// });
