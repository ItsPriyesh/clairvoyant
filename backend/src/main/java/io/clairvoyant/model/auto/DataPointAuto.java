package io.clairvoyant.model.auto;

import com.google.auto.value.AutoValue;
import io.clairvoyant.model.DataPoint;

import java.sql.Date;

@AutoValue
public abstract class DataPointAuto implements DataPoint {
    @AutoValue.Builder
    public static abstract class Builder {
        public abstract Builder setDataPointID(int id);

        public abstract Builder setNodeID(int id);

        public abstract Builder setReceivedAt(Date receivedAt);

        public abstract Builder setEventType(String eventType);

        public abstract Builder setConfidence(float confidence);

        public abstract DataPointAuto build();
    }

    public static Builder builder() {
        return new AutoValue_DataPointAuto.Builder();
    }
}