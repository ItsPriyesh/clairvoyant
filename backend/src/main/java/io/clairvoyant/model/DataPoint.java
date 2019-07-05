package io.clairvoyant.model;

import org.davidmoten.rx.jdbc.annotations.Column;

import java.sql.Date;
import java.sql.Timestamp;

public interface DataPoint {

    @Column
    int dataPointID();

    @Column
    int nodeID();

    @Column
    Timestamp receivedAt();

    @Column
    String eventType();

    @Column
    float confidence();
}