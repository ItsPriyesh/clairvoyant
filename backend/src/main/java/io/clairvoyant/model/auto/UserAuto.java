package io.clairvoyant.model.auto;

import com.google.auto.value.AutoValue;
import io.clairvoyant.model.User;

import java.sql.Date;

@AutoValue
public abstract class UserAuto implements User {
    @AutoValue.Builder
    public abstract static class Builder {
        public abstract Builder setUserID(int id);

        public abstract Builder setFirstName(String name);

        public abstract Builder setLastName(String name);

        public abstract Builder setEmail(String email);

        public abstract Builder setPasswordHash(String passwordHash);

        public abstract Builder setCreatedAt(Date date);

        public abstract UserAuto build();
    }

    public static Builder builder() {
        return new AutoValue_UserAuto.Builder();
    }

}
