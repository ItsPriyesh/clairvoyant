package io.clairvoyant.api.model;

import com.google.auto.value.AutoValue;

@AutoValue
public abstract class SessionToken {

    public abstract String token();

    public static SessionToken create(String token) {
        return new AutoValue_SessionToken(token);
    }
}
