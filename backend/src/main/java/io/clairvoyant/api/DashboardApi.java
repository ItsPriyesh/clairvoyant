package io.clairvoyant.api;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
import io.clairvoyant.api.model.Error;
import io.clairvoyant.db.DataPointStore;
import io.clairvoyant.db.MotionEventStore;
import io.clairvoyant.db.NodeStore;
import io.clairvoyant.db.UserStore;
import io.clairvoyant.model.DataPoint;
import io.clairvoyant.model.MotionEvent;
import io.clairvoyant.model.Node;
import spark.Request;
import spark.Response;

import javax.inject.Inject;

import java.util.List;
import java.util.Optional;

public class DashboardApi extends ApiBase {

    private final NodeStore nodeStore;
    private final DataPointStore dataPointStore;
    private final MotionEventStore motionEventStore;

    @Inject
    public DashboardApi(UserStore userStore, DataPointStore dataPointStore, NodeStore nodeStore, Gson gson, MotionEventStore motionEventStore) {
        super(gson, userStore);
        this.dataPointStore = dataPointStore;
        this.nodeStore = nodeStore;
        this.motionEventStore = motionEventStore;
    }

    public String getDataPoints(Request req, Response res) {
        Optional<Error> err = authenticateUser(req, res);
        if (err.isPresent()) return toJson(err.get());

        int userId = Integer.parseInt(req.queryParams("user_id"));
        List<DataPoint> data = dataPointStore.getDataPoints(userId).blockingGet();
        return toJson(data, new TypeToken<List<DataPoint>>() {}.getType());
    }

    public String getNodes(Request req, Response res) {
        Optional<Error> err = authenticateUser(req, res);
        if (err.isPresent()) return toJson(err.get());

        int userId = Integer.parseInt(req.queryParams("user_id"));
        List<Node> data = nodeStore.getNodes(userId).blockingGet();
        return toJson(data, new TypeToken<List<Node>>() {}.getType());
    }

    public String getMotionEvents(Request req, Response res) {
        Optional<Error> err = authenticateUser(req, res);
        if (err.isPresent()) return toJson(err.get());

        int userId = Integer.parseInt(req.queryParams("user_id"));
        List<MotionEvent> data = motionEventStore.getMotionEvents(userId).blockingGet();
        return toJson(data, new TypeToken<List<MotionEvent>>() {}.getType());
    }
}
