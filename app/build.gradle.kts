import com.github.benmanes.gradle.versions.updates.DependencyUpdatesTask

plugins {
    alias(libs.plugins.jte)
    alias(libs.plugins.kotlin.jvm)
    alias(libs.plugins.ktlint)
    alias(libs.plugins.shadow)
    alias(libs.plugins.versions)
    application
}

println("Kotlin v${KotlinVersion.CURRENT}")
println("Java v${System.getProperty("java.version")}")
println("Arch: ${System.getProperty("os.arch")}")

group = "github.buriedincode"
version = "0.1.0"

repositories {
    mavenCentral()
    mavenLocal()
}

dependencies {
    implementation(libs.bundles.exposed)
    implementation(libs.bundles.jackson)
    implementation(libs.bundles.javalin)
    implementation(libs.bundles.jte)
    implementation(libs.hoplite.core)
    implementation(libs.kotlin.logging)
    runtimeOnly(libs.log4j2.slf4j2)
    runtimeOnly(libs.sqlite.jdbc)
    implementation("nl.jacobras:Human-Readable:1.10.0")
}

kotlin {
    jvmToolchain(17)
}

java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(17)
    }
}

application {
    mainClass = "github.buriedincode.FreyrKt"
    applicationName = "Freyr"
}

jte {
    precompile()
    kotlinCompileArgs = arrayOf("-jvm-target", "17")
}

configure<org.jlleitschuh.gradle.ktlint.KtlintExtension> {
    version = "1.4.1"
}

tasks.jar {
    dependsOn(tasks.precompileJte)
    from(
        fileTree("jte-classes") {
            include("**/*.class")
            include("**/*.bin") // Only required if you use binary templates
        },
    )
    manifest.attributes["Main-Class"] = "github.buriedincode.FreyrKt"
}

tasks.shadowJar {
    dependsOn(tasks.precompileJte)
    from(
        fileTree("jte-classes") {
            include("**/*.class")
            include("**/*.bin") // Only required if you use binary templates
        },
    )
    manifest.attributes["Main-Class"] = "github.buriedincode.FreyrKt"
    mergeServiceFiles()
}

fun isNonStable(version: String): Boolean {
    val stableKeyword = listOf("RELEASE", "FINAL", "GA").any { version.uppercase().contains(it) }
    val regex = "^[0-9,.v-]+(-r)?$".toRegex()
    val isStable = stableKeyword || regex.matches(version)
    return isStable.not()
}

tasks.withType<DependencyUpdatesTask> {
    gradleReleaseChannel = "current"
    resolutionStrategy {
        componentSelection {
            all {
                if (isNonStable(candidate.version) && !isNonStable(currentVersion)) {
                    reject("Release candidate")
                }
            }
        }
    }
}
