package io.clairvoyant.model.auto;

import com.google.auto.value.AutoValue;
import io.clairvoyant.model.Node;

@AutoValue
public abstract class NodeAuto implements Node {
    @AutoValue.Builder
    public abstract static class Builder {
        public abstract Builder setNodeID(int id);

        public abstract Builder setUserID(int id);

        public abstract Builder setLastHeartbeat(long timestamp);

        public abstract NodeAuto build();
    }

    public static Builder builder() {
        return new AutoValue_NodeAuto.Builder();
    }

}
