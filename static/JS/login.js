let login_success = function(){
  document.getElementByID("login-btn").onclick = function(){
      location.href = "http://127.0.0.1:5000/signup";
    };
}


let validate = function(){
  let uname = document.getElementById("usname").value;
  let passwd = document.getElementById("passwd").value;
  let form = document.getElementById("form");

  if (uname === "" || passwd === ""){
    alert("Please Enter A Valid Username and Password");
    form.method = "get";
  } else{
    form.action = "http://127.0.0.1:5000/login-success";
  }
}

