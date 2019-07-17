package io.clairvoyant.model.auto;

import com.google.auto.value.AutoValue;
import io.clairvoyant.model.DataPoint;

import java.sql.Date;
import java.sql.Timestamp;

@AutoValue
public abstract class DataPointAuto implements DataPoint {
    @AutoValue.Builder
    public static abstract class Builder {
        public abstract Builder setDataPointId(String id);

        public abstract Builder setNodeId(String id);

        public abstract Builder setCreatedAt(Timestamp createdAt);

        public abstract Builder setClassification(String classification);

        public abstract Builder setConfidence(float confidence);

        public abstract DataPointAuto build();
    }

    public static Builder builder() {
        return new AutoValue_DataPointAuto.Builder();
    }
}
