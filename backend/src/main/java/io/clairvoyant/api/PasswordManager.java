package io.clairvoyant.api;

import org.mindrot.jbcrypt.BCrypt;

import javax.inject.Inject;

public class PasswordManager {

    @Inject
    public PasswordManager() {}

    public String hash(String password) {
        return BCrypt.hashpw(password, BCrypt.gensalt());
    }

    public boolean check(String password, String hash) {
        return BCrypt.checkpw(password, hash);
    }
}
