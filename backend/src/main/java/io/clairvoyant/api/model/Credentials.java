package io.clairvoyant.api.model;

import com.google.auto.value.AutoValue;
import com.google.gson.JsonDeserializer;
import com.google.gson.JsonObject;

@AutoValue
public abstract class Credentials {
    public abstract int userId();
    public abstract String sessionToken();

    public static Credentials create(int userID, String token) {
        return new AutoValue_Credentials(userID, token);
    }

    public static JsonDeserializer<Credentials> DESERIALIZER = (json, type, context) -> {
        JsonObject obj = json.getAsJsonObject();
        return create(obj.get("user_id").getAsInt(), obj.get("session_token").getAsString());
    };
}
