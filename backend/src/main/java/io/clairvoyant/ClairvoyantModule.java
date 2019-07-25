package io.clairvoyant;

import com.google.gson.FieldNamingPolicy;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.mysql.cj.jdbc.MysqlDataSource;
import dagger.Module;
import dagger.Provides;
import io.clairvoyant.api.model.Credentials;
import io.clairvoyant.db.DatabaseConfig;
import io.clairvoyant.model.DataPoint;
import io.clairvoyant.model.Node;
import org.davidmoten.rx.jdbc.Database;

import javax.inject.Singleton;
import java.sql.SQLException;

/**
 * Define static factory methods for dependencies that don't support
 * constructor injection
 */
@Module
public class ClairvoyantModule {

    @Provides
    static DatabaseConfig provideDatabaseConfig() {
//        return Database.DatabaseConfig.builder()
//                .setAddress(System.getProperty("CLAIRVOYANT_DB_ADDRESS"))
//                .setPort(Integer.parseInt(System.getProperty("CLAIRVOYANT_DB_PORT")))
//                .setUser(System.getProperty("CLAIRVOYANT_DB_USER"))
//                .setPassword(System.getProperty("CLAIRVOYANT_DB_PASS"))
//                .build();
        return DatabaseConfig.builder()
                .setName("clairvoyant")
                .setAddress("localhost")
                .setPort(3306)
                .setUser("root")
                .setPassword("")
                .setTimezone("EST5EDT")
                .build();
    }

    @Provides
    @Singleton
    static Database provideDatabase(DatabaseConfig config) {
        MysqlDataSource source = new MysqlDataSource();
        source.setServerName(config.address());
        source.setPort(config.port());
        source.setUser(config.user());
        source.setPassword(config.password());
        source.setDatabaseName(config.name());
        try {
            source.setServerTimezone(config.timezone());
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return Database.fromBlocking(source);
    }

    @Provides
    @Singleton
    static Gson provideGson() {
        return new GsonBuilder()
                .registerTypeAdapter(Credentials.class, Credentials.DESERIALIZER)
                .registerTypeAdapter(DataPoint.class, DataPoint.SERIALIZER)
                .registerTypeAdapter(Node.class, Node.SERIALIZER)
                .setFieldNamingPolicy(FieldNamingPolicy.LOWER_CASE_WITH_UNDERSCORES)
                .create();
    }
}
