/*!
 * Start Bootstrap - Shop Homepage v5.0.1 (https://startbootstrap.com/template/shop-homepage)
 * Copyright 2013-2021 Start Bootstrap
 * Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-shop-homepage/blob/master/LICENSE)
 */
// This file is intentionally blank
// Use this file to add JavaScript to your project

const handleCollapseAccountForms = () => {
  const collapseProductBtn = document.getElementById("collapseProductBtn");
  const collapseProfileBtn = document.getElementById("collapseProfileBtn");

  const collapseProfileForm = document.getElementById("collapseProfileForm");
  const collapseProductForm = document.getElementById("collapseProductForm");

  collapseProfileBtn.addEventListener("click", () => {
    collapseProductForm.classList.contains("show") &&
      collapseProductForm.classList.remove("show");
  });
  collapseProductBtn.addEventListener("click", () => {
    collapseProfileForm.classList.contains("show") &&
      collapseProfileForm.classList.remove("show");
  });
};

handleCollapseAccountForms();
