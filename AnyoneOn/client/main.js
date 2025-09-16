yourStatus = document.getElementById("yourStatus")

function updateStatusColors(){
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
});