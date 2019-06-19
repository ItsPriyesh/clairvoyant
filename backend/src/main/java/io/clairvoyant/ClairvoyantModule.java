package io.clairvoyant;

import com.google.common.flogger.FluentLogger;
import dagger.Module;
import dagger.Provides;

@Module
public class ClairvoyantModule {

    @Provides public static FluentLogger provideLogger() {
        return FluentLogger.forEnclosingClass();
    }
}
