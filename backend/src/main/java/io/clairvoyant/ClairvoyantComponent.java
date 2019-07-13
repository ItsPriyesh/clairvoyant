package io.clairvoyant;

import dagger.Component;
import io.clairvoyant.api.ApiService;
import io.clairvoyant.gateway.ClairvoyantService;
import io.clairvoyant.test.DataPointTest;
import io.clairvoyant.test.UserTest;

import javax.inject.Singleton;

@Singleton
@Component(modules = ClairvoyantModule.class)
public interface ClairvoyantComponent {
    ClairvoyantService createGatewayRpcService();
    ApiService createWebApiService();
    UserTest createTestUser();
    DataPointTest createTestDataPoint();
}
