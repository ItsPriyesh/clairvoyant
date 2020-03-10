package io.clairvoyant.model.auto;

import com.google.auto.value.AutoValue;
import io.clairvoyant.model.DataPoint;
import io.clairvoyant.model.MotionEvent;

import java.sql.Date;
import java.sql.Timestamp;

@AutoValue
public abstract class MotionEventAuto implements MotionEvent {
    @AutoValue.Builder
    public static abstract class Builder {
        public abstract Builder setMotionEventId(String id);

        public abstract Builder setNodeId(String id);

        public abstract Builder setCreatedAt(Timestamp createdAt);

        public abstract Builder setMotionType(String motionType);

        public abstract Builder setOrientation(String orientation);

        public abstract Builder setRoll(int roll);

        public abstract Builder setPitch(int pitch);

        public abstract Builder setYaw(int yaw);

        public abstract MotionEventAuto build();
    }

    public static Builder builder() {
        return new AutoValue_MotionEventAuto.Builder();
    }
}
