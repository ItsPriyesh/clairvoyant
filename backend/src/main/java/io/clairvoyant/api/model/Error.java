package io.clairvoyant.api.model;

import com.google.auto.value.AutoValue;

@AutoValue
public abstract class Error {

    public abstract String message();

    public static Error create(String message) {
        return new AutoValue_Error(message);
    }
}
