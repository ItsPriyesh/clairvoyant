package io.clairvoyant.model;

import org.davidmoten.rx.jdbc.annotations.Column;

public interface Node {

    @Column
    int nodeID();

    @Column
    int userID();

    @Column
    long lastHeartbeat();
}