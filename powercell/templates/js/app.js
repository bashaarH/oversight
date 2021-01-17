// replace these values with those generated in your TokBox Account
var apiKey = "47084204";
var sessionId = "2_MX40NzA4NDIwNH5-MTYxMDgzNDEzODM5MX5ibWJqd0twZHp0NWxzS2xVcXoyU2taclV-UH4";
var token = "T1==cGFydG5lcl9pZD00NzA4NDIwNCZzaWc9OTViZjBjYjM1MTA4ODE0MmVjNjMyYmE2ZTBjYjcxOGVkY2ZlZGU3YTpzZXNzaW9uX2lkPTJfTVg0ME56QTROREl3Tkg1LU1UWXhNRGd6TkRFek9ETTVNWDVpYldKcWQwdHdaSHAwTld4elMyeFZjWG95VTJ0YWNsVi1VSDQmY3JlYXRlX3RpbWU9MTYxMDgzNDEzOCZleHBpcmVfdGltZT0xNjEwOTIwNTM4JnJvbGU9cHVibGlzaGVyJm5vbmNlPTY0Nzc3JmluaXRpYWxfbGF5b3V0X2NsYXNzX2xpc3Q9";

// Handling all of our errors here by alerting them
function handleError(error) {
  if (error) {
    alert(error.message);
  }
}

// (optional) add server code here
initializeSession();

function initializeSession() {
  var session = OT.initSession(apiKey, sessionId);

  // Subscribe to a newly created stream
  session.on('streamCreated', function(event) {
    session.subscribe(event.stream, 'subscriber', {
      insertMode: 'append',
      width: '100%',
      height: '100%'
    }, handleError);
  });

  // Create a publisher
  var publisher = OT.initPublisher('publisher', {
    insertMode: 'append',
    width: '100%',
    height: '100%'
  }, handleError);

  // Connect to the session
  session.connect(token, function(error) {
    // If the connection is successful, publish to the session
    if (error) {
      handleError(error);
    } else {
      session.publish(publisher, handleError);
    }
  });
}

function connect() {
  // Replace apiKey and sessionId with your own values:
  session = OT.initSession(apiKey, sessionId);
  session.on({
    connectionCreated: function (event) {
      connectionCount++;
      console.log(connectionCount + ' connections.');
    },
    connectionDestroyed: function (event) {
      connectionCount--;
      console.log(connectionCount + ' connections.');
    },
    sessionDisconnected: function sessionDisconnectHandler(event) {
      // The event is defined by the SessionDisconnectEvent class
      console.log('Disconnected from the session.');
      document.getElementById('disconnectBtn').style.display = 'none';
      if (event.reason == 'networkDisconnected') {
        alert('Your network connection terminated.')
      }
    }
  });
  // Replace token with your own value:
  session.connect(token, function(error) {
    if (error) {
      console.log('Unable to connect: ', error.message);
    } else {
      document.getElementById('disconnectBtn').style.display = 'block';
      console.log('Connected to the session.');
      connectionCount = 1;
    }
  });
}

function disconnect() {
  session.disconnect();
}
