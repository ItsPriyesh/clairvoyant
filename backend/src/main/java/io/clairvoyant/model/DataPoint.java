package io.clairvoyant.model;

import org.davidmoten.rx.jdbc.annotations.Column;

import java.sql.Date;

public interface DataPoint {

    @Column
    int dataPointID();

    @Column
    int nodeID();

    @Column
    Date receivedAt();

    @Column
    String eventType();

    @Column
    float confidence();
}