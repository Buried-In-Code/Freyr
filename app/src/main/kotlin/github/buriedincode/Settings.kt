package github.buriedincode

import com.sksamuel.hoplite.ConfigLoaderBuilder
import com.sksamuel.hoplite.ExperimentalHoplite
import com.sksamuel.hoplite.addPathSource
import com.sksamuel.hoplite.addResourceSource
import kotlin.io.path.div

data class Settings(
    val database: Database,
    val environment: Environment,
    val website: Website,
) {
    enum class Environment {
        DEV,
        PROD,
    }

    data class Database(val source: Source, val url: String, val user: String? = null, val password: String? = null) {
        enum class Source {
            POSTGRES,
            SQLITE,
        }
    }

    data class Website(val host: String, val port: Int)

    companion object {
        @OptIn(ExperimentalHoplite::class)
        fun load(): Settings = ConfigLoaderBuilder
            .default()
            .withExplicitSealedTypes()
            .addPathSource(Utils.CONFIG_ROOT / "settings.properties", optional = true, allowEmpty = true)
            .addResourceSource("/default.properties")
            .build()
            .loadConfigOrThrow<Settings>()
    }
}
