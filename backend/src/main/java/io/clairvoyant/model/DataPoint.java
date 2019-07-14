package io.clairvoyant.model;

import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonSerializationContext;
import com.google.gson.JsonSerializer;
import org.davidmoten.rx.jdbc.annotations.Column;

import java.lang.reflect.Type;
import java.sql.Timestamp;

public interface DataPoint {

    @Column
    int dataPointId();

    @Column
    int nodeId();

    @Column
    Timestamp receivedAt();

    @Column
    String eventType();

    @Column
    float confidence();

    JsonSerializer<DataPoint> SERIALIZER = (dp, type, context) -> {
        JsonObject json = new JsonObject();
        json.addProperty("id", dp.dataPointId());
        json.addProperty("node_id", dp.nodeId());
        json.addProperty("type", dp.eventType());
        json.addProperty("confidence", dp.confidence());
        json.addProperty("time", dp.receivedAt().toString());
        return json;
    };
}