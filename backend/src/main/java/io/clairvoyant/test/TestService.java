package io.clairvoyant.test;

import javax.inject.Inject;
import javax.inject.Singleton;

@Singleton
public class TestService {

    public final User user;

    @Inject
    public TestService(User user) { this.user = user; }
}
