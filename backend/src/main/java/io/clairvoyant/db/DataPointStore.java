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
                .update("insert into DataPoint values(?, ?, FROM_UNIXTIME(?), ?, ?)")
                .parameters(
                        point.getMessageId(),
                        point.getNodeId(),
                        point.getTimestamp(),
                        point.getClassification(),
                        point.getConfidence()
                )
                .complete();
    }

    public Single<List<DataPoint>> getDataPoints(int userId) {
        return database
                .select("select DataPoint.* from DataPoint " +
                        "join Node using (node_id) where user_id = ?")
                .parameter(userId)
                .autoMap(DataPoint.class)
                .toList();
    }
}
