package io.clairvoyant.model.auto;

import com.google.auto.value.AutoValue;
import io.clairvoyant.model.User;

import java.sql.Date;
import java.sql.Timestamp;

@AutoValue
public abstract class UserAuto implements User {
    @AutoValue.Builder
    public abstract static class Builder {
        public abstract Builder setUserID(int id);

        public abstract Builder setFirstName(String name);

        public abstract Builder setLastName(String name);

        public abstract Builder setEmail(String email);

        public abstract Builder setPasswordHash(String passwordHash);

        public abstract Builder setCreatedAt(Timestamp date);

        public abstract Builder setSessionToken(String token);

        public abstract UserAuto build();
    }

    public static Builder builder() {
        return new AutoValue_UserAuto.Builder()
                .setUserID(0); // This gets overwritten by auto_increment id in SQL, but needs to be set here for builder to work
    }

}
