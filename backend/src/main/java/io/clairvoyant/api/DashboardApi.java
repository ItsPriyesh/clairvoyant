package io.clairvoyant.api;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.reflect.TypeToken;
import io.clairvoyant.api.model.Credentials;
import io.clairvoyant.api.model.Error;
import io.clairvoyant.db.DataPointStore;
import io.clairvoyant.db.UserStore;
import io.clairvoyant.model.DataPoint;
import spark.Request;
import spark.Response;

import javax.inject.Inject;

import java.util.List;

import static io.clairvoyant.api.ApiService.hasParams;

public class DashboardApi {

    private final UserStore userStore;
    private final DataPointStore dataPointStore;
    private final Gson gson;

    @Inject
    public DashboardApi(UserStore userStore, DataPointStore dataPointStore, Gson gson) {
        this.userStore = userStore;
        this.dataPointStore = dataPointStore;
        this.gson = gson;
    }


    public String getDataPoints(Request req, Response res) {
        if (!hasParams(req, "user_id", "session_token")) {
            res.status(400);
            return gson.toJson(Error.create("Missing credentials!"));
        }

        int userId = Integer.parseInt(req.queryParams("user_id"));
        boolean isValid = userStore.isUserSessionValid(
                userId, req.queryParams("session_token")).blockingGet();
        if (!isValid) {
            res.status(401);
            return gson.toJson(Error.create("Invalid credentials!"));
        }

        List<DataPoint> data = dataPointStore.getDataPoints(userId).blockingGet();
        return gson.toJson(data, new TypeToken<List<DataPoint>>(){}.getType());
    }
}
