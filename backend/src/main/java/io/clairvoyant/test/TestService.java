package io.clairvoyant.test;

import javax.inject.Inject;
import javax.inject.Singleton;

@Singleton
public class TestService {

    public final User user;
    public final DataPoint dataPoint;

    @Inject
    public TestService(User user, DataPoint dataPoint) {
        this.user = user;
        this.dataPoint = dataPoint;
    }
}
