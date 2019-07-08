package io.clairvoyant;

import dagger.Component;
import io.clairvoyant.api.ApiService;
import io.clairvoyant.api.DataPointSocketHandler;
import io.clairvoyant.gateway.ClairvoyantService;

import javax.inject.Singleton;

@Singleton
@Component(modules = ClairvoyantModule.class)
public interface ClairvoyantComponent {
    ClairvoyantService createGatewayRpcService();
    ApiService createWebApiService();
    DataPointSocketHandler createSocketHandler();
}
