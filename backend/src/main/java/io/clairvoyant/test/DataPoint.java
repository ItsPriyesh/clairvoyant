package io.clairvoyant.test;

import io.clairvoyant.db.DataPointStore;

import javax.inject.Inject;

public class DataPoint {

    private DataPointStore dataPointStore;

    @Inject
    public DataPoint(DataPointStore dataPointStore) {
        this.dataPointStore = dataPointStore;
    }

    public void createDataPoint() {

    }
}
