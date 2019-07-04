package io.clairvoyant.db;

import com.google.auto.value.AutoValue;

@AutoValue
public abstract class DatabaseConfig {

    public static Builder builder() {
        return new AutoValue_DatabaseConfig.Builder();
    }

    @AutoValue.Builder
    public abstract static class Builder {
        public abstract Builder setName(String name);

        public abstract Builder setAddress(String address);

        public abstract Builder setPort(int port);

        public abstract Builder setUser(String user);

        public abstract Builder setPassword(String password);

        public abstract Builder setTimezone(String timezone);

        public abstract DatabaseConfig build();
    }

    public abstract String name();

    public abstract String address();

    public abstract int port();

    public abstract String user();

    public abstract String password();

    public abstract String timezone();
}