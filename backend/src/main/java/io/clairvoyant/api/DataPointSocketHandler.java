package io.clairvoyant.api;

import org.eclipse.jetty.websocket.api.Session;
import org.eclipse.jetty.websocket.api.annotations.OnWebSocketClose;
import org.eclipse.jetty.websocket.api.annotations.OnWebSocketConnect;
import org.eclipse.jetty.websocket.api.annotations.OnWebSocketMessage;
import org.eclipse.jetty.websocket.api.annotations.WebSocket;

@WebSocket
public class DataPointSocketHandler {

    @OnWebSocketConnect
    public void onConnect(Session user) throws Exception {
        // User joined
        System.out.println("onConnect");

        user.getRemote().sendString("hello");

    }

    @OnWebSocketClose
    public void onClose(Session user, int statusCode, String reason) {
        // User left
        System.out.println("onClose");
    }

    @OnWebSocketMessage
    public void onMessage(Session user, String message) {
        // User sent message
        System.out.printf("user % sent : \n", user, message);
    }
}
