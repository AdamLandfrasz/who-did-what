const initWebSocket = () => {
    const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws';
    const socket = new WebSocket(`${protocol}://${window.location.host}/ws/connect`);
    socket.onmessage = event => {
        const jsonData = JSON.parse(event.data);
        const { messageType } = jsonData;
        switch (messageType) {
            case 'ping':
                alert(jsonData.message);
                break;
            case 'player_joined':
                showPlayers(jsonData.playersJoined);
                break;
        }
    }
}

const showPlayers = (players) => {
    const joinedPlayers = document.querySelector('#joined-players');
    joinedPlayers.innerHTML = '';
    players.forEach(player => {
        let newPlayerElement = document.createElement('p');
        newPlayerElement.textContent = player;
        joinedPlayers.appendChild(newPlayerElement);
    });
}

initWebSocket();
