# README

This gradle project was generated via [spring initializr](https://start.spring.io/) using Spring Boot version 2.4.3 and Java 11. To allow for Java version flexibility, we're using [gradle toolchains](https://docs.gradle.org/current/userguide/toolchains.html#sec:consuming). If you do not have JDK 11, simply update the toolchain block in `build.gradle` to the appropriate version:

```
java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(11)
    }
}
```

Run `./gradlew tasks` to see what targets you can run.

Default target to build the project is `./gradlew assemble`
Default target to launch the app is `./gradlew bootRun`
