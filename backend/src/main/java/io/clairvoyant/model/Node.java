package io.clairvoyant.model;

import com.google.auto.value.AutoValue;

@AutoValue
public abstract class Node {

    public static Node create(int id, long timestamp, float batteryLevel) {
        return new AutoValue_Node(id, timestamp, batteryLevel);
    }

    public abstract int id();

    public abstract long lastHeartbeat();

    public abstract float batteryLevel();
}