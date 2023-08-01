byID("signup").addEventListener("click", async () => {
    const username = byID('username').value;
    const email = byID('email').value;
    const password = byID('password').value;
    const confirmPassword = byID('confirmPassword').value;
    const success = byID("success");
    const error = byID("error");
  
    const response = await fetch(window.location.href, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({"username":username,"email": email,"password": password,"confirmPassword":confirmPassword})
    });
  
    if (response.ok) {
      const message = await response.json();
      if (message.status == "success"){
        success.hidden = false;
        success.innerText = message.detail;
        setTimeout(()=>{success.hidden = true;},5000);
        console.log('Signup successful', message.detail);
        setTimeout(()=>{window.location.href=message.redirect},1000);
      }else{
        error.hidden = false;
        error.innerText = message.detail;
        setTimeout(()=>{error.hidden = true;},5000);
        console.log('Signup failed', message.detail);
      }
    } else {
      console.log('Signup failed');
      error.hidden = false;
      error.innerText = "Unexpected Error";
      setTimeout(()=>{error.hidden = true;},5000);
    }
  });
    