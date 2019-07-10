package io.clairvoyant.test;

import io.clairvoyant.api.PasswordManager;
import io.clairvoyant.db.UserStore;
import io.clairvoyant.model.auto.UserAuto;
import io.reactivex.Maybe;

import javax.inject.Inject;
import javax.xml.bind.DatatypeConverter;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.sql.Timestamp;
import java.util.UUID;

public class User {

    private final UserStore userStore;
    private final PasswordManager passManager;

    @Inject
    public User(UserStore userStore, PasswordManager pwManager) {
        this.userStore = userStore;
        this.passManager = pwManager;
    }

    public void createUser(String fn, String ln, String em, String pw) throws Exception {
        Maybe<io.clairvoyant.model.User> userMaybe = userStore.getUser(em);
        if(userMaybe.isEmpty().blockingGet()) {
            String sessionToken = UUID.randomUUID().toString();
            String initialHashPw = initialHash(pw);
            io.clairvoyant.model.User user = UserAuto.builder()
                    .setFirstName(fn)
                    .setLastName(ln)
                    .setEmail(em)
                    .setPasswordHash(passManager.hash(initialHashPw))
                    .setCreatedAt(new Timestamp(System.currentTimeMillis()))
                    .setSessionToken(sessionToken)
                    .build();

            Throwable error = userStore.insert(user).blockingGet();
            if(error != null) {
                throw new Exception(error.getMessage());
            }
        }

    }

    private String initialHash(String pw) throws NoSuchAlgorithmException {
        MessageDigest md = MessageDigest.getInstance("MD5");
        md.update(pw.getBytes());
        byte[] digest = md.digest();
        return DatatypeConverter.printHexBinary(digest).toLowerCase();
    }
}
