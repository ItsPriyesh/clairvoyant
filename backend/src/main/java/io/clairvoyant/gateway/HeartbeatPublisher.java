package io.clairvoyant.gateway;

import io.clairvoyant.db.UserStore;
import io.clairvoyant.model.Node;
import io.clairvoyant.model.auto.MotionEventAuto;
import io.clairvoyant.model.auto.NodeAuto;
import io.clairvoyant.proto.Heartbeat;
import io.clairvoyant.proto.MotionEvent;
import io.reactivex.Observable;
import io.reactivex.subjects.PublishSubject;

import javax.inject.Inject;
import javax.inject.Singleton;
import java.sql.Timestamp;

@Singleton
public class HeartbeatPublisher {

    private final UserStore userStore;
    private final PublishSubject<Node> subject = PublishSubject.create();

    @Inject
    HeartbeatPublisher(UserStore userStore) {
        this.userStore = userStore;
    }

    public void publish(Heartbeat heartbeat) {
        Node node = NodeAuto.builder()
                .setBatteryLevel(heartbeat.getBatteryLevel())
                .setLastHeartbeat(new Timestamp(System.currentTimeMillis()))
                .setNodeID(heartbeat.getNodeId())
                .setUserID(1)
                .build();

        subject.onNext(node);
    }

    public Observable<Node> listenForUser(int userId) {
        return subject
                .flatMapSingle(node -> userStore
                        .getUserForNode(node.nodeID())
                        .map(u -> new NodeUser(node, u))
                )
                .filter(d -> d.userId == userId)
                .map(d -> d.node);
    }

    private static class NodeUser {
        private final Node node;
        private final int userId;

        NodeUser(Node node, int userId) {
            this.node = node;
            this.userId = userId;
        }
    }
}
