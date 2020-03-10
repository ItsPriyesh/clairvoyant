package io.clairvoyant.db;

import io.clairvoyant.model.DataPoint;
import io.clairvoyant.model.MotionEvent;
import io.clairvoyant.model.auto.DataPointAuto;
import io.reactivex.Completable;
import io.reactivex.Single;
import org.davidmoten.rx.jdbc.Database;

import javax.inject.Inject;
import java.util.List;

public class MotionEventStore {

    private final Database database;

    @Inject
    public MotionEventStore(Database database) {
        this.database = database;
    }

    public Completable insert(io.clairvoyant.proto.MotionEvent me) {
        return database
                .update("insert into MotionEvent values(?, ?, from_unixtime(?), ?, ?, ? , ? , ?)")
                .parameters(
                        me.getMessageId(),
                        me.getNodeId(),
                        me.getTimestamp(),
                        me.getMotionType(),
                        me.getOrientation(),
                        me.getRoll(),
                        me.getPitch(),
                        me.getYaw()
                )
                .complete();
    }

    public Single<Boolean> contains(io.clairvoyant.proto.MotionEvent event) {
        return database.select("select motion_event_id from MotionEvent where motion_event_id = ?")
                .parameter(event.getMessageId())
                .getAs(String.class)
                .toList()
                .map(res -> !res.isEmpty());
    }

    public Single<List<MotionEvent>> getMotionEvents(int userId) {
        return database
                .select("select distinct MotionEvent.* from MotionEvent " +
                        "join Node using (node_id) where user_id = ? " +
                        "order by created_at desc")
                .parameter(userId)
                .autoMap(MotionEvent.class)
                .toList();
    }


}
