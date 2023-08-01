byID("login").addEventListener("click", async () => {
  const email = byID('email').value;
  const password = byID('password').value;
  const success = byID("success");
  const error = byID("error");

  const response = await fetch(window.location.href, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ "email": email, "password": password })
  });

  if (response.ok) {
    const message = await response.json();
    if (message.status == "success"){
      success.hidden = false;
      success.innerText = message.detail;
      setTimeout(()=>{success.hidden = true;},5000);
      console.log('Login successful', message.detail);
      setTimeout(()=>{window.location.href=message.redirect},1000);
    }else{
      error.hidden = false;
      error.innerText = message.detail;
      setTimeout(()=>{error.hidden = true;},5000);
      console.log('Login failed', message.detail);
    }
  } else {
    console.log('Login failed');
    error.hidden = false;
    error.innerText = "Unexpected Error";
    setTimeout(()=>{error.hidden = true;},5000);
  }
});
  