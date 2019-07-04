package io.clairvoyant.api;

import javax.inject.Inject;
import javax.inject.Singleton;

@Singleton
public class ApiService {

    public final LoginApi login;

    @Inject
    public ApiService(LoginApi login) {
        this.login = login;
    }
}
