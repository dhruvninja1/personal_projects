username=""
yourTill = document.getElementById('yourTill');
tillHrInput = document.getElementById('tillHourInput');
tillMinuteInput = document.getElementById('tillMinuteInput');
yourStatus = document.getElementById("yourStatus");
yourUsernameLabel = document.getElementById("yourUsernameLabel")
userNameInputButton = document.getElementById("userNameInputButton");
popup = document.getElementById("popup");
overlay = document.getElementById("overlay");
const proxyUrl = "https://dhruvsharma.org:15555";
const managementUrl = "https://dhruvsharma.org:15565";
servers = [];
const otherStatuses = document.getElementById("otherStatuses")
const serverStatusContainers = new Map();



async function addSever(dport, dname){
    const response = await fetch(`${managementUrl}/joinServer/${dport}`, {
      method: "GET"
    });
    const responseBodyText = await response.text()
    if (responseBodyText == "Success"){
      servers.push({port: dport, name: dname});
      console.log("DONE")
      //close popup
    }
    else{
      //write text
    }
    
}

async function createServer(name){
  const response = await fetch(`${managementUrl}/createServer`, {method: "GET"});
  d = await response.text();
  console.log(parseInt(d))
  addSever(parseInt(d), name);
  createServerPopup.style.display = 'none';
}

async function updateStatus(name, status, till_hr, till_min){
    servers.forEach(async server =>{
      console.log(`Server found: ${server.name}`)
      try {
          const response = await fetch(`${proxyUrl}/${server.port}/status`, {
            method: "POST",
            headers: {
              "Content-Type": "application/json" 
            },
            body: JSON.stringify({ name, status, till_hr, till_min })
          });

          if (response.ok) {
            console.log("Status updated successfully!");
          } else {
            console.error("Failed to update status:", response.status);
          }
        } catch (error) {
          console.error("Error:", error);
        }
    });
    
}

async function getStatuses(){
  servers.forEach(async server =>{
    console.log(`found: ${server.name}`)
    const response = await fetch(`${proxyUrl}/${server.port}/statuses`, {
      method: "GET"
    })

    if (response.ok) {
          const data = await response.json();
          console.log("Data received:", data);
          updateScreenStatuses(data, server);
    }
  })
    
}

async function updateScreenStatuses(data, server) {
  let serverContainer = serverStatusContainers.get(server.port);
  let statusCardsContainer;

  if (!serverContainer) {
    serverContainer = document.createElement('div');
    serverContainer.classList.add('server-statuses-container');
    serverContainer.id = `server-${server.port}`;
    otherStatuses.appendChild(serverContainer);
    serverStatusContainers.set(server.port, serverContainer);

    const headerContainer = document.createElement('div');
    headerContainer.classList.add('server-header');
    
    headerContainer.innerHTML = `
      <h1>${server.name}</h1>
      <button class="hidden" onclick="
          if (this.classList.contains('shown')) {
              this.classList.remove('shown');
              this.classList.add('hidden');
              this.textContent = '*****';
          } else {
              this.classList.remove('hidden');
              this.classList.add('shown');
              this.textContent = '${server.port}';
          }
      ">*****</button>
    `;
    serverContainer.appendChild(headerContainer);

    statusCardsContainer = document.createElement('div');
    statusCardsContainer.classList.add('status-cards-container');
    serverContainer.appendChild(statusCardsContainer);
    
    serverStatusContainers.set(`cards-${server.port}`, statusCardsContainer);

  } else {
    statusCardsContainer = serverStatusContainers.get(`cards-${server.port}`);
  }

  statusCardsContainer.innerHTML = '';

  data.forEach(user => {
    if (user.name === username) {
      yourStatus.textContent = user.status;
      const tillTime = (user.till_hr === '' || user.till_min === '') ? "IDK" : `${user.till_hr}:${user.till_min}`;
      yourTill.textContent = "till " + tillTime;
      return;
    }
    
    const tempDiv = document.createElement('div');
    tempDiv.id = user.name;
    tempDiv.classList.add('otherCard');
    const tillTime = (user.till_hr === '' || user.till_min === '') ? "IDK" : `${user.till_hr}:${user.till_min}`;
    tempDiv.innerHTML = `
      <h1 class="othername">${user.name}</h1>
      <h1 class="status">${user.status}</h1>
      <h1 class="till">till ${tillTime}</h1>
    `;
    statusCardsContainer.appendChild(tempDiv);
  });

  updateStatusColors();
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
const addbutton = document.getElementById("addButton");
const addSubmitButton = document.getElementById("portInputButton");
const addInputField = document.getElementById("portInputField");
const addPopup = document.getElementById("addPopup");
const addNameInputField = document.getElementById("serverNameInputField")
const createServerPopup = document.getElementById("createPopup")
const createServerInputName = document.getElementById("createServerNameInputField")
const createServerSubmitButton = document.getElementById("createServerNameInputButton")
const createServerBtn = document.getElementById("createButton")

addbutton.addEventListener('click', function(){
  addPopup.style.display = 'block';
});

addSubmitButton.addEventListener('click', function(){
  console.log(addInputField.value);
  addSever(parseInt(addInputField.value), addNameInputField.value);
  addInputField.value = '';
  addPopup.style.display = 'none';
});

createServerBtn.addEventListener('click', function(){
  createServerPopup.style.display = 'block';
});

createServerSubmitButton.addEventListener('click', function(){
  createServer(createServerInputName.value);
});

menu.addEventListener("sl-select", event => {
    const item = event.detail.item;
    yourStatus.textContent = item.value;
    console.log("Cliecked");
    updateStatus(username, yourStatus.textContent, tillHrInput.value, tillMinuteInput.value);
    tillHrInput.value = '';
    tillMinuteInput.value = '';
});

tillHrInput.addEventListener('click', (event) => {
  event.stopPropagation();
});

tillMinuteInput.addEventListener('click', (event) => {
  event.stopPropagation();
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


