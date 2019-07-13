package io.clairvoyant.test;

import io.clairvoyant.db.DataPointStore;
import io.clairvoyant.model.auto.DataPointAuto;

import javax.inject.Inject;
import java.sql.Timestamp;

public class DataPoint {

    private DataPointStore dataPointStore;

    @Inject
    public DataPoint(DataPointStore dataPointStore) {
        this.dataPointStore = dataPointStore;
    }

    public void createDataPoint(int nodeId, Timestamp timestamp, String eventType, float confidence)
            throws Exception {
        io.clairvoyant.model.DataPoint dataPoint = DataPointAuto.builder()
                .setNodeID(nodeId)
                .setReceivedAt(timestamp)
                .setEventType(eventType)
                .setConfidence(confidence)
                .build();

        Throwable error = dataPointStore.insert(dataPoint).blockingGet();
        if(error != null) {
            throw new Exception(error.getMessage());
        }
    }
}
