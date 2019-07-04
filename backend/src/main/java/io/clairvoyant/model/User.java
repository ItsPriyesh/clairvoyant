package io.clairvoyant.model;

import org.davidmoten.rx.jdbc.annotations.Column;

import java.sql.Date;

public interface User {

    @Column
    int userID();

    @Column
    String firstName();

    @Column
    String lastName();

    @Column
    String email();

    @Column
    String passwordHash();

    @Column
    Date createdAt();
}
