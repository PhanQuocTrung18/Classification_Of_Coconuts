const wrapper = document.querySelector('.wrapper');
const loginLink = document.querySelector('.login-link');
const registerLink = document.querySelector('.register-link');
const btnPopup = document.querySelector('.btnLogin-popup');
const iconClose = document.querySelector('.icon-close');
let isRegisterShown = false;

if (registerLink) {
  registerLink.addEventListener('click', (event) => {
    wrapper.classList.add('active');
    isRegisterShown = true; // Đánh dấu rằng khung đăng ký đang hiển thị
  });
}

if (loginLink) {
  loginLink.addEventListener('click', () => {
    wrapper.classList.remove('active');
    isRegisterShown = false; // Đánh dấu rằng khung đăng nhập đang hiển thị
  });
}
btnPopup.addEventListener('click', () => {
  if (isRegisterShown) {
    wrapper.classList.add('active-popup');
  }
});
iconClose.addEventListener('click', ()=> {
  wrapper.classList.remove('active-popup');
  window.location.href = "/";
});