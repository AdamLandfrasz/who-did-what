const joinButton = document.querySelector('#join');
const nameField = document.querySelector('#name');
const queryParams = new URLSearchParams(window.location.search);
joinButton.addEventListener('click', async (event) => {
    event.preventDefault()
    const joinResponse = await fetch(`/players/join?player_name=${nameField.value}`);
    const { success } = await joinResponse.json();
    if (success) {
        let roomId = queryParams.get('room_id');
        if (!roomId) {
            const createRoomResp = await fetch('/rooms/create');
            const { id } = await createRoomResp.json();
            roomId = id;
        }
        if (roomId) {
            window.location.replace(`/room/${roomId}`)
        }
    }
});

