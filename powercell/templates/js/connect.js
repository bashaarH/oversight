var session;
var connectionCount = 0;

function connect() {
  // Replace apiKey and sessionId with your own values:
  apiKey = "47084204"
  sessionId = "2_MX40NzA4NDIwNH5-MTYxMDgxMjcxNTQzMX42QXY4dktCWkFJWUowVVRIaTJ5T29IWnZ-UH4"
  token = "cGFydG5lcl9pZD00NzA4NDIwNCZzaWc9MGI3OGM2YzVhODA1MDZlYjg3ZTE3ZjJjNzkxODFkNjBmMjNmODM0NzpzZXNzaW9uX2lkPTJfTVg0ME56QTROREl3Tkg1LU1UWXhNRGd4TWpjeE5UUXpNWDQyUVhZNGRrdENXa0ZKV1Vvd1ZWUklhVEo1VDI5SVduWi1VSDQmY3JlYXRlX3RpbWU9MTYxMDgxMjcxNCZleHBpcmVfdGltZT0xNjEwODk5MTE0JnJvbGU9cHVibGlzaGVyJm5vbmNlPTEyODY3NSZpbml0aWFsX2xheW91dF9jbGFzc19saXN0PSZjb25uZWN0aW9uX2RhdGE9dXNlcm5hbWUlM0RCb2IlMkN1c2VyTGV2ZWwlM0Q0"
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

connect();
