
// Change this to your backend API URL (e.g. ALB DNS name)
const API_BASE_URL = "http://recipehub-alb-1177327530.eu-central-1.elb.amazonaws.com";

function getToken() {
  return localStorage.getItem("token");
}

function setToken(token) {
  localStorage.setItem("token", token);
}

function clearToken() {
  localStorage.removeItem("token");
}
