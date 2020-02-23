package io.clairvoyant.db;

import io.clairvoyant.model.DataPoint;
import io.clairvoyant.model.auto.DataPointAuto;
import io.reactivex.Completable;
import io.reactivex.Single;
import org.davidmoten.rx.jdbc.Database;

import javax.inject.Inject;
import java.util.List;

public class DataPointStore {

    private final Database database;

    @Inject
    public DataPointStore(Database database) {
        this.database = database;
    }

    public Completable insert(io.clairvoyant.proto.DataPoint point) {
        return database
                .update("insert into DataPoint values(?, ?, from_unixtime(?), ?, ?)")
                .parameters(
                        point.getMessageId(),
                        point.getNodeId(),
                        point.getTimestamp(),
                        point.getClassification(),
                        point.getConfidence()
                )
                .complete();
    }

    public Single<Boolean> contains(io.clairvoyant.proto.DataPoint point) {
        return database.select("select data_point_id from DataPoint where data_point_id = ?")
                .parameter(point.getMessageId())
                .getAs(String.class)
                .toList()
                .map(res -> !res.isEmpty());
    }

    public Single<List<DataPoint>> getDataPoints(int userId) {
        return database
                .select("select distinct DataPoint.* from DataPoint " +
                        "join Node using (node_id) where user_id = ? " +
                        "order by created_at desc")
                .parameter(userId)
                .autoMap(DataPoint.class)
                .toList();
    }

    public Single<List<DataPoint>> getDataPointsForNode(int userId, int nodeId) {
        return database
                .select("select distinct DataPoint.* from DataPoint " +
                        "join Node using (node_id) where user_id = ? and node_id = ? " +
                        "order by created_at desc")
                .parameters(
                        userId,
                        nodeId
                )
                .autoMap(DataPoint.class)
                .toList();
    }
}
