package io.clairvoyant.model;

import org.davidmoten.rx.jdbc.annotations.Column;

import java.sql.Timestamp;

public interface DataPoint {

    @Column
    int dataPointId();

    @Column
    int nodeId();

    @Column
    Timestamp receivedAt();

    @Column
    String eventType();

    @Column
    float confidence();
}