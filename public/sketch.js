var connection = null;
var state = {
    volume : 0,
    freq: 0
}

//event handler for getting websocket data
function handleMessage(d){
    d = JSON.parse(d);
    console.log(d);
    state.volume = d.vol;
    state.freq = d.freq;
}

//connect to the websocket
function preload(){
    connection = new WebSocket('ws://localhost:8001/websocket');
    connection.onopen = () => console.log("Conneceted to websocket!");
    connection.onerror = err => console.log("Error: ", err);
    connection.onmessage = e => handleMessage(e.data);
    //not sending anything back to socket
}

function setup(){
    createCanvas(windowWidth, 300);
}

function draw(){
    background(20);
    fill(state.volume, 90, 34);
    ellipse(50, 50, 80, 80);

    fill(23, state.freq, 233);
    ellipse(100,100, 23, 23);
}