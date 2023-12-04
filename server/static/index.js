const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws';
const socket = new WebSocket(`${protocol}://${window.location.host}/ws/connect`);
socket.onmessage = event => {
    const { message } = JSON.parse(event.data);
    alert(message);
}

const joinButton = document.querySelector('#join');
const nameField = document.querySelector('#name');
joinButton.addEventListener('click', async  (event) => {
    event.preventDefault();
    await fetch(`/ws/ping?name=${nameField.value}`);
});

