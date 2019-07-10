package io.clairvoyant;

import dagger.Component;
import io.clairvoyant.api.ApiService;
import io.clairvoyant.api.LoginApi;
import io.clairvoyant.gateway.ClairvoyantService;
import io.clairvoyant.test.TestService;

import javax.inject.Singleton;

@Singleton
@Component(modules = ClairvoyantModule.class)
public interface ClairvoyantComponent {
    ClairvoyantService createGatewayRpcService();
    ApiService createWebApiService();
    TestService createTestService();
}
