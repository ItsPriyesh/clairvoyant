package io.clairvoyant.api;

import com.google.common.flogger.FluentLogger;
import com.google.gson.Gson;
import io.clairvoyant.api.model.Credentials;
import io.clairvoyant.db.UserStore;
import io.clairvoyant.gateway.HeartbeatPublisher;
import io.clairvoyant.gateway.MotionEventPublisher;
import io.clairvoyant.model.MotionEvent;
import io.clairvoyant.model.Node;
import io.clairvoyant.model.auto.MotionEventAuto;
import io.reactivex.disposables.Disposable;
import io.reactivex.schedulers.Schedulers;
import org.eclipse.jetty.websocket.api.Session;
import org.eclipse.jetty.websocket.api.annotations.OnWebSocketClose;
import org.eclipse.jetty.websocket.api.annotations.OnWebSocketConnect;
import org.eclipse.jetty.websocket.api.annotations.OnWebSocketMessage;
import org.eclipse.jetty.websocket.api.annotations.WebSocket;

import javax.inject.Inject;
import java.sql.Timestamp;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;


@WebSocket
public class HeartbeatSocketHandler {

    private static final FluentLogger logger = FluentLogger.forEnclosingClass();

    private final Gson gson;
    private final UserStore userStore;
    private final HeartbeatPublisher heartbeatPublisher;
    private final Map<Session, Disposable> clients = new ConcurrentHashMap<>();

    @Inject
    public HeartbeatSocketHandler(HeartbeatPublisher heartbeatPublisher, UserStore userStore, Gson gson) {
        this.heartbeatPublisher = heartbeatPublisher;
        this.userStore = userStore;
        this.gson = gson;
    }

    @OnWebSocketConnect
    public void onConnect(Session user) throws Exception {
        logger.atInfo().log("Client connected: %s ", user.getLocalAddress());
    }

    @OnWebSocketClose
    public void onClose(Session user, int statusCode, String reason) {
        logger.atInfo().log("Client disconnected: %s ", user.getLocalAddress());

        Disposable clientDisposable = clients.get(user);
        if (clientDisposable != null && !clientDisposable.isDisposed()) {
            clientDisposable.dispose();
            clients.remove(user);
        }
    }

    @OnWebSocketMessage
    public void onMessage(Session user, String message) {
        logger.atInfo().log("Received socket message %s from %s", message, user.getLocalAddress());

        Credentials creds = gson.fromJson(message, Credentials.class);
        userStore.isUserSessionValid(creds.userId(), creds.sessionToken())
                .subscribeOn(Schedulers.newThread())
                .subscribe(isValid -> {
                    if (isValid) startListening(user, creds.userId());
                });
    }

    private void startListening(Session session, int userID) {
        logger.atInfo().log("Forwarding events to user=%s, address=%s", userID, session.getLocalAddress());

        Disposable disposable = heartbeatPublisher.listenForUser(userID)
                .filter(n -> n.nodeID().equals("3"))
                .subscribeOn(Schedulers.newThread())
                .subscribe(data -> session.getRemote().sendString(gson.toJson(data, Node.class)),
                        Throwable::printStackTrace);

        clients.put(session, disposable);
    }
}
