package io.clairvoyant;

import com.google.auto.value.AutoValue;
import com.google.common.flogger.FluentLogger;
import io.clairvoyant.model.Node;
import io.clairvoyant.proto.Heartbeat;

import javax.inject.Inject;
import javax.inject.Singleton;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

@Singleton
public class NodeManager {

    private static final FluentLogger logger = FluentLogger.forEnclosingClass();

    private final Map<Integer, Node> nodes = new ConcurrentHashMap<>();

    @Inject
    NodeManager() {

    }

    void addNode(Heartbeat heartbeat) {
        int id = heartbeat.getId();
        logger.atInfo().log("Received heartbeat from node %s", id);

        Node node = Node.create(id, heartbeat.getTimestamp(), heartbeat.getBatteryLevel());
        nodes.put(id, node);
    }
}
