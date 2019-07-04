package io.clairvoyant;

import dagger.Component;
import io.clairvoyant.api.LoginApi;
import io.clairvoyant.gateway.ClairvoyantService;

import javax.inject.Singleton;

@Singleton
@Component(modules = ClairvoyantModule.class)
public interface ClairvoyantComponent {
    ClairvoyantService createGatewayRpcService();
    LoginApi createWebApiService();
}
