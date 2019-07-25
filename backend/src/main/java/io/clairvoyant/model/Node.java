package io.clairvoyant.model;

import org.davidmoten.rx.jdbc.annotations.Column;

public interface Node {

    @Column
    String nodeID();

    @Column
    int userID();

    @Column
    long lastHeartbeat();

    @Column
    float batteryLevel();
}
