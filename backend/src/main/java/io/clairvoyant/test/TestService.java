package io.clairvoyant.test;

import javax.inject.Inject;
import javax.inject.Singleton;

@Singleton
public class TestService {

    public final User user;
    public final DataPoint dataPoint;
    public final Node node;

    @Inject
    public TestService(User user, DataPoint dataPoint, Node node) {
        this.user = user;
        this.dataPoint = dataPoint;
        this.node = node;
    }
}
