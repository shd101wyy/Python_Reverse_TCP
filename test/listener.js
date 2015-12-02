"use strict"

let net = require('net')

const PORT = 31000

let server = net.createServer(function(socket) {
  process.stdin.pipe(socket)
  socket.pipe(process.stdout)
})

server.listen(PORT)
