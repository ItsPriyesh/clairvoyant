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
    String dataPointId();

    @Column
    String nodeId();

    @Column
    Timestamp createdAt();

    @Column
    String classification();

    @Column
    float confidence();

    JsonSerializer<DataPoint> SERIALIZER = (dp, type, context) -> {
        JsonObject json = new JsonObject();
        json.addProperty("id", dp.dataPointId());
        json.addProperty("node_id", dp.nodeId());
        json.addProperty("classification", dp.classification());
        json.addProperty("confidence", dp.confidence());
        json.addProperty("created_at", dp.createdAt().toString());
        return json;
    };
}
