const container = document.querySelector(".container");

const htmlEl = document.getElementsByTagName("html")[0];
const currentTheme = localStorage.getItem("theme")
  ? localStorage.getItem("theme")
  : null;
if (currentTheme) {
  htmlEl.dataset.theme = currentTheme;
}
const toggleTheme = (theme) => {
  htmlEl.dataset.theme = theme;
  localStorage.setItem("theme", theme);
};

const togglePassword = document.querySelector("#togglePassword");
const password = document.querySelector("#id_password");

togglePassword.addEventListener("click", function (e) {
  const type =
    password.getAttribute("type") === "password" ? "text" : "password";
  password.setAttribute("type", type);
  this.classList.toggle("fa-eye-slash");
});



const runColorMode = (fn) => {
  if (!window.matchMedia) {
    return;
  }


  const query = window.matchMedia('(prefers-color-scheme: dark)');

  fn(query.matches);

  query.addEventListener('change', (event) => fn(event.matches));
}

runColorMode((isDarkMode) => {
  if(isDarkMode){
    toggleTheme('dark')
  }
});
