let user;
let username_box_div;
let username_elm;
let user_level;
let char_container;
let ttsContainer;
let text;

function levelToColor(level) {
  if (level >=0 && level <= 10) {
    // green
    return 'rgb(255, 255, 255)'
  } else if (level >= 11 && level <= 21) {
    // Yellow
    return "rgb(255,255,51)";
  } else if (level >= 22) {
    // red
    return "rgb(139,0,0)";
  }
}

document.addEventListener("DOMContentLoaded", function () {
  username_box_div = document.getElementById("box");
  username_elm = document.getElementById("username");
  user_level = document.getElementById("level");
  user = document.getElementById("username");

  char_container = document.getElementById("tts-char");
  ttsContainer = document.querySelector(".tts-container");
  text = document.querySelector(".text")
});

function connectWS(url, maxRetries, retryInterval) {
  let retries = 0;

  function createWebSocket() {
    const socket = new WebSocket(url);

    socket.addEventListener("open", () => {
      content = document.getElementById("display");
      content.style.opacity = "0%";
      console.log("WebSocket connection established");
      socket.send(
        JSON.stringify({
          event: "CONNECT",
          client: "OBS_CLIENT",
        })
      );
    });

    let speaking_started;
    let timeout_id = null;
    socket.addEventListener("message", async (event) => {
      const data = JSON.parse(event.data);
      console.log(data);
      if (!data.event) {
        return;
      } else {
        switch (data.event) {
          case "IS_SPEAKING":
            speaking_started = new Date();

            // User label
            username_box_div.style.display = "block";
            text.style.color = levelToColor(data.level);
            username_elm.innerText = data.user;
            user_level.innerText = `(level-${data.level})`;

            // TTS on gif
            console.log(char_container);
            char_container.src = `gifs/ttsoverlay.gif?ts=${new Date().getTime()}`;

            break;

          case "SPEAKING_COMPLETE":
            let t_delta = new Date() - speaking_started;

            if (t_delta > 3000) {
              // User label
              username_box_div.style.display = "none";
              username_elm.innerText = "";

              // TTS off gif
              char_container.src = `gifs/ttsoverlaystopped.gif?ts=${new Date().getTime()}`;
            } else {
              clearTimeout(timeout_id);

              timeout_id = setTimeout(() => {
                // User label
                username_box_div.style.display = "none";
                username_elm.innerText = "";

                // TTS off gif
                char_container.src = `gifs/ttsoverlaystopped.gif`;
                console.log(char_container);

                timeout_id = null;
              }, 1000);
            }
        }
      }
    });

    socket.addEventListener("close", () => {
      document.getElementById("display").innerText = "Websocket not connected";
      if (retries < maxRetries || maxRetries === 0) {
        retries++;
        console.log(`reconnecting in ${retryInterval} / 1000`)
        setTimeout(createWebSocket, retryInterval)
      } else {
        console.log('Max retries reached, WS server unavailable')
      }
    });

    socket.addEventListener("error", (event) => {
      console.error("WebSocket error:", event);
      socket.close();
    });
  }
  createWebSocket()
}
const url = "ws://localhost:8181/";
const maxRetries = 30;
const retryInterval = 5000
connectWS(url, maxRetries, retryInterval)




