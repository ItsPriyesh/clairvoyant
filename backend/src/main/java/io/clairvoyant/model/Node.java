package io.clairvoyant.model;

import com.google.auto.value.AutoValue;

@AutoValue
public abstract class Node {

    public static Builder builder() {
        return new AutoValue_Node.Builder();
    }

    @AutoValue.Builder
    public abstract static class Builder {
        public abstract Builder setId(int id);

        public abstract Builder setLastHeartbeat(long timestamp);

        public abstract Builder setBatteryLevel(float batteryLevel);

        public abstract Node build();
    }

    public abstract int id();

    public abstract long lastHeartbeat();

    public abstract float batteryLevel();
}