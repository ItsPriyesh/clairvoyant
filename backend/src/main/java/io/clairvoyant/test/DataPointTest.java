package io.clairvoyant.test;

import io.clairvoyant.db.DataPointStore;
import io.clairvoyant.model.DataPoint;
import io.clairvoyant.model.EventType;
import io.clairvoyant.model.auto.DataPointAuto;

import javax.inject.Inject;
import java.sql.Timestamp;

public class DataPointTest {

    private DataPointStore dataPointStore;

    @Inject
    public DataPointTest(DataPointStore dataPointStore) {
        this.dataPointStore = dataPointStore;
    }

    public void createDataPoint() throws Exception {
        DataPoint dataPoint1 = DataPointAuto.builder()
                .setNodeID(1)
                .setReceivedAt(new Timestamp(System.currentTimeMillis()))
                .setEventType((EventType.EXPLOSION.toString()))
                .setConfidence((float)0.87)
                .build();

        DataPoint dataPoint2 = DataPointAuto.builder()
                .setNodeID(1)
                .setReceivedAt(new Timestamp(System.currentTimeMillis()))
                .setEventType((EventType.GUNSHOT.toString()))
                .setConfidence((float)0.55)
                .build();

        DataPoint dataPoint3 = DataPointAuto.builder()
                .setNodeID(1)
                .setReceivedAt(new Timestamp(System.currentTimeMillis()))
                .setEventType((EventType.VEHICLE.toString()))
                .setConfidence((float)0.34)
                .build();

        Throwable error1 = dataPointStore.insert(dataPoint1).blockingGet();
        Throwable error2 = dataPointStore.insert(dataPoint2).blockingGet();
        Throwable error3 = dataPointStore.insert(dataPoint3).blockingGet();
        if(error1 != null) {
            throw new Exception(error1.getMessage());
        } else if (error2 != null) {
            throw new Exception(error2.getMessage());
        } else if (error3 != null) {
            throw new Exception(error3.getMessage());
        }
    }
}
