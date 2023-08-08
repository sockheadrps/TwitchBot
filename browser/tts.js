const socket = new WebSocket('ws://0.0.0.0:8181/');
let speaking = false;
let messageQueue = [];
let playing = false

let idle = document.getElementById("chatter_idle");
let talking = document.getElementById("username");


let user = document.getElementById("username")
document.body.style.backgroundImage = "url('idle.png')";

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
    console.log("data is: ", data.event)
    if (!data.event) {
        return
    }
    if (data.event === "IS_SPEAKING"){
        console.log(" if")
        console.log(data)
        talking.innerText = data.user
        document.body.style.backgroundImage = "url('talking.png')";
    }
    else if (data.event ==='SPEAKING_COMPLETE') {
        console.log("else if")
        talking.innerText = ""
        document.body.style.backgroundImage = "url('idle.png')";
    }
    else {
        console.log('no....')
    }
});

socket.addEventListener('close', () => {
    document.getElementById('display').innerText = 'Websocket not connected';
});

