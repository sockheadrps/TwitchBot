let user
let username_box_div
let username_elm
const socket = new WebSocket('ws://0.0.0.0:8181/');


document.addEventListener('DOMContentLoaded', function () {
    username_box_div = document.getElementById('box');
    username_elm = document.getElementById("username");
    user = document.getElementById("username")

    document.body.style.backgroundImage = "url('idle.png')";
    username_box_div.style.display = 'none';
});


socket.addEventListener('open', () => {
    content = document.getElementById('display');
    content.style.opacity = '0%';
    console.log('WebSocket connection established');
    socket.send(JSON.stringify(
        {
            "event": "CONNECT",
            "client": "OBS_CLIENT"
        }
    ))
});


socket.addEventListener('message', async (event) => {
    const data = JSON.parse(event.data);
    if (!data.event) {
        return
    } else {
        switch (data.event) {
            case "IS_SPEAKING":
                username_box_div.style.display = 'block';
                username_elm.innerText = data.user
                document.body.style.backgroundImage = "url('talking.png')";
                break;

            case 'SPEAKING_COMPLETE':
                username_box_div.style.display = 'none';
                username_elm.innerText = ""
                document.body.style.backgroundImage = "url('idle.png')";
        }
    }
});

socket.addEventListener('close', () => {
    document.getElementById('display').innerText = 'Websocket not connected';
});

