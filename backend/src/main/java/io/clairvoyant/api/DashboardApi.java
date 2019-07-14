package io.clairvoyant.api;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
import io.clairvoyant.api.model.Error;
import io.clairvoyant.db.DataPointStore;
import io.clairvoyant.db.UserStore;
import io.clairvoyant.model.DataPoint;
import spark.Request;
import spark.Response;

import javax.inject.Inject;

import java.util.List;
import java.util.Optional;

public class DashboardApi extends ApiBase {

    private final DataPointStore dataPointStore;

    @Inject
    public DashboardApi(UserStore userStore, DataPointStore dataPointStore, Gson gson) {
        super(gson, userStore);
        this.dataPointStore = dataPointStore;
    }

    public String getDataPoints(Request req, Response res) {
        Optional<Error> err = authenticateUser(req, res);
        if (err.isPresent()) return toJson(err.get());

        int userId = Integer.parseInt(req.queryParams("user_id"));
        List<DataPoint> data = dataPointStore.getDataPoints(userId).blockingGet();
        return toJson(data, new TypeToken<List<DataPoint>>() {}.getType());
    }
}
