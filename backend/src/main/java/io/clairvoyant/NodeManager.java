package io.clairvoyant;

import com.google.common.flogger.FluentLogger;
import io.clairvoyant.proto.Heartbeat;

import javax.inject.Inject;
import javax.inject.Singleton;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

@Singleton
public class NodeManager {

    class Node {
        private final int id;
        private float batteryLevel;
        private long lastHeartbeat;

        Node(int id, long timestamp, float batteryLevel) {
            this.id = id;
            this.batteryLevel = batteryLevel;
            this.lastHeartbeat = timestamp;
        }

        void updateHeartbeat(long timstamp, float batteryLevel) {
            this.lastHeartbeat = timstamp;
            this.batteryLevel = batteryLevel;
        }
    }

    private final FluentLogger logger;
    private final Map<Integer, Node> nodes = new ConcurrentHashMap<>();

    @Inject NodeManager(FluentLogger logger) {
        this.logger = logger;
    }

    void addNode(Heartbeat heartbeat) {
        int id = heartbeat.getId();
        logger.atInfo().log("Received heartbeat from node %s", id);
        if (nodes.containsKey(id)) {
            nodes.get(id).updateHeartbeat(heartbeat.getTimestamp(), heartbeat.getBatteryLevel());
        } else {
            Node n = new Node(id, heartbeat.getTimestamp(), heartbeat.getBatteryLevel());
            nodes.put(id, n);
        }
    }
}
