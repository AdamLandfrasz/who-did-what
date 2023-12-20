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
                showPlayers(jsonData);
                break;
        }
    }
}

const showPlayers = ({playersJoined, host}) => {
    const joinedPlayers = document.querySelector('#joined-players');
    joinedPlayers.innerHTML = '';
    playersJoined.forEach(player => {
        let newPlayerElement = document.createElement('p');
        newPlayerElement.textContent = player;
        if (host === player) {
            newPlayerElement.classList.add('host');
        }
        joinedPlayers.appendChild(newPlayerElement);
    });
}

initWebSocket();
