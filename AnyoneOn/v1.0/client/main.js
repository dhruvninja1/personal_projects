username=""
yourStatus = document.getElementById("yourStatus");
yourUsernameLabel = document.getElementById("yourUsernameLabel")
userNameInputButton = document.getElementById("userNameInputButton");
popup = document.getElementById("popup");
overlay = document.getElementById("overlay");
const serverUrl = "http://localhost:18080";

async function updateStatus(name, status){
    try {
    const response = await fetch(`${serverUrl}/status`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ name, status })
    });

    if (response.ok) {
      console.log("Status updated successfully!");
    } else {
      console.error("Failed to update status:", response.status);
    }
  } catch (error) {
    console.error("Error:", error);
  }
}

async function getStatuses(){
    const response = await fetch(`${serverUrl}/statuses`, {
      method: "GET"
    })

    if (response.ok) {
          const data = await response.json();
          console.log("Data received:", data);
          updateScreenStatuses(data);
    }
}

async function updateScreenStatuses(data){
    otherStatuses = document.getElementById("otherStatuses")
    const children = otherStatuses.children;
    arr = data;
    console.log("data");

    otherStatuses.innerHTML = '';

    arr.forEach(user =>{
        if (user.name == username){
            yourStatus.textContent = user.status;
            return;
        }
        tempDiv = document.createElement('div');
        tempDiv.id = user.name;
        tempDiv.classList.add('otherCard');
        tempDiv.innerHTML = `
          <h1 class="othername">${user.name}</h1>
          <h1 class="status">${user.status}</h1>
        `;
        otherStatuses.appendChild(tempDiv);
    })
    updateStatusColors()
}

async function updateStatusColors(){
    document.querySelectorAll(".status").forEach(el => {
        if (el.textContent.includes("Online")) el.style.color = "green";
        if (el.textContent.includes("Offline"))   el.style.color = "gray";
        if (el.textContent.includes("Away"))   el.style.color = "orange";
    });

    if (yourStatus.textContent.includes("Online")) yourStatus.style.color = "green";
    if (yourStatus.textContent.includes("Offline"))   yourStatus.style.color = "gray";
    if (yourStatus.textContent.includes("Away"))   yourStatus.style.color = "orange";
}
const menu = document.getElementById("your-status-menu");

menu.addEventListener("sl-select", event => {
    const item = event.detail.item;
    yourStatus.textContent = item.value;
    console.log("Cliecked");
    updateStatusColors();
    updateStatus(username, yourStatus.textContent);

});

userNameInputButton.addEventListener('click', function(){
    usernameInputField = document.getElementById("usernameInputField");
    username = usernameInputField.value;
    popup.style.display='none';
    overlay.style.display='none';
    yourUsernameLabel.textContent=username;
    console.log(username);
    getStatuses();
    setInterval(getStatuses, 1000);
});


