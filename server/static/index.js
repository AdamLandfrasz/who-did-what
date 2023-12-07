const joinButton = document.querySelector('#join');
const nameField = document.querySelector('#name');
joinButton.addEventListener('click', async (event) => {
    event.preventDefault()
    const joinResponse = await fetch(`/players/join?player_name=${nameField.value}`);
    const { success } = await joinResponse.json();
    if (success) {
        const createRoomResp = await fetch(
            "/rooms/create",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
            }
        );
        const {id} = await createRoomResp.json()
        if (id) {
            window.location.replace(`/room/${id}`)
        }
    }
});

