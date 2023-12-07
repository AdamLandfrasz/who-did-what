const joinButton = document.querySelector('#join');
const nameField = document.querySelector('#name');
joinButton.addEventListener('click', async (event) => {
    event.preventDefault()
    const resp = await fetch(`/players/join?player_name=${nameField.value}`);
    if (resp.ok) {
        window.location.replace('/joined')
    }
});

