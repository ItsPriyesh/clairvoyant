package io.clairvoyant.model;

import com.google.gson.JsonObject;
import com.google.gson.JsonSerializer;
import org.davidmoten.rx.jdbc.annotations.Column;

import java.sql.Timestamp;

public interface Node {

    @Column
    String nodeID();

    @Column
    int userID();

    @Column
    Timestamp lastHeartbeat();

    @Column
    float batteryLevel();

    JsonSerializer<Node> SERIALIZER = (n, type, context) -> {
        JsonObject json = new JsonObject();
        json.addProperty("id", n.nodeID());
        json.addProperty("battery_level", n.batteryLevel());
        json.addProperty("user_id", n.userID());
        json.addProperty("created_at", n.lastHeartbeat().toString());
        return json;
    };
}
