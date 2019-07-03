package io.clairvoyant;

import dagger.Module;
import dagger.Provides;
import io.clairvoyant.db.Database;

/**
 * Define static factory methods for dependencies that don't support
 * constructor injection
 */
@Module
public class ClairvoyantModule {

    @Provides
    static Database.Config provideDatabaseConfig() {
//        return Database.Config.builder()
//                .setAddress(System.getProperty("CLAIRVOYANT_DB_ADDRESS"))
//                .setPort(Integer.parseInt(System.getProperty("CLAIRVOYANT_DB_PORT")))
//                .setUser(System.getProperty("CLAIRVOYANT_DB_USER"))
//                .setPassword(System.getProperty("CLAIRVOYANT_DB_PASS"))
//                .build();
        return Database.Config.builder()
                .setAddress("localhost")
                .setPort(8084)
                .setUser("root")
                .setPassword("pass123")
                .build();
    }
}
