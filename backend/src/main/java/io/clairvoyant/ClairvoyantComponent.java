package io.clairvoyant;

import dagger.Component;
import io.clairvoyant.api.WebApiService;
import io.clairvoyant.gateway.ClairvoyantService;

import javax.inject.Singleton;

@Singleton
@Component(modules = ClairvoyantModule.class)
public interface ClairvoyantComponent {
    ClairvoyantService createGatewayRpcService();
    WebApiService createWebApiService();
}
