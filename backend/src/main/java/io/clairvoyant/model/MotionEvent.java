package io.clairvoyant.model;

import com.google.gson.JsonObject;
import com.google.gson.JsonSerializer;
import io.clairvoyant.api.DateFormat;
import org.davidmoten.rx.jdbc.annotations.Column;

import java.sql.Timestamp;

public interface MotionEvent {

    @Column
    String motionEventId();

    @Column
    String nodeId();

    @Column
    Timestamp createdAt();

    @Column
    String motionType();

    @Column
    String orientation();

    @Column
    int roll();

    @Column
    int pitch();

    @Column
    int yaw();

    JsonSerializer<MotionEvent> SERIALIZER = (me, type, context) -> {
        JsonObject json = new JsonObject();
        json.addProperty("id", me.motionEventId());
        json.addProperty("node_id", me.nodeId());
        json.addProperty("created_at", DateFormat.toReadableDate(me.createdAt()));
        json.addProperty("motion_type", me.motionType());
        json.addProperty("orientation", me.orientation());
        json.addProperty("roll", me.roll());
        json.addProperty("pitch", me.pitch());
        json.addProperty("yaw", me.yaw());
        return json;
    };
}
