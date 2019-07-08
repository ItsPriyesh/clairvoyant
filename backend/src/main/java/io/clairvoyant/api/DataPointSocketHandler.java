package io.clairvoyant.api;

import com.google.common.flogger.FluentLogger;
import com.google.gson.Gson;
import io.clairvoyant.api.model.Credentials;
import io.clairvoyant.db.UserStore;
import io.clairvoyant.gateway.DataPointPublisher;
import io.clairvoyant.model.auto.DataPointAuto;
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

/**
 * Socket protocol to listen for real-time DataPoint updates:
 * 1) Client connects to socket endpoint @host:port/listenDataPoint
 * 2) Client sends their userID and sessionToken as a Credential json
 * 3) Server checks credentials
 * 4) Server sends DataPoint json whenever it receives from the gateway node
 */
@WebSocket
public class DataPointSocketHandler {

    private static final FluentLogger logger = FluentLogger.forEnclosingClass();

    private final Gson gson;
    private final UserStore userStore;
    private final DataPointPublisher dataPointManager;
    private final Map<Session, Disposable> clients = new ConcurrentHashMap<>();

    @Inject
    public DataPointSocketHandler(DataPointPublisher dataPointManager, UserStore userStore, Gson gson) {
        this.dataPointManager = dataPointManager;
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

        Disposable disposable = dataPointManager.listenForUser(userID)
                .map(proto -> DataPointAuto.builder()
                        .setDataPointId(proto.getId())
                        .setNodeId(proto.getNodeId())
                        .setEventType(proto.getEventType())
                        .setConfidence(proto.getConfidence())
                        .setReceivedAt(new Timestamp(proto.getTimestamp()))
                )
                .subscribeOn(Schedulers.newThread())
                .subscribe(data -> session.getRemote().sendString(gson.toJson(data)));

        clients.put(session, disposable);
    }
}
