/*!
 * Start Bootstrap - Shop Homepage v5.0.1 (https://startbootstrap.com/template/shop-homepage)
 * Copyright 2013-2021 Start Bootstrap
 * Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-shop-homepage/blob/master/LICENSE)
 */
// This file is intentionally blank
// Use this file to add JavaScript to your project

const displayModalOnFormFailure = () => {
  const loginModal = new bootstrap.Modal(
    document.getElementById("loginModalToggle"),
    {
      keyboard: true,
    }
  );
  const registerModal = new bootstrap.Modal(
    document.getElementById("registerModalToggle"),
    {
      keyboard: true,
    }
  );

  const checkLogin = document.getElementById("checklogin");
  const checkRegister = document.getElementById("checkregister");
  if (checkRegister && !checkLogin) {
    registerModal.show();
  }
  if (!checkRegister && checkLogin) {
    loginModal.show();
  }
};

displayModalOnFormFailure();

