package github.buriedincode

import io.github.oshai.kotlinlogging.KLogger
import io.github.oshai.kotlinlogging.KotlinLogging
import io.github.oshai.kotlinlogging.Level
import kotlinx.datetime.Instant
import nl.jacobras.humanreadable.HumanReadable
import org.jetbrains.exposed.sql.Database
import org.jetbrains.exposed.sql.DatabaseConfig
import org.jetbrains.exposed.sql.ExperimentalKeywordApi
import org.jetbrains.exposed.sql.Slf4jSqlDebugLogger
import org.jetbrains.exposed.sql.addLogger
import org.jetbrains.exposed.sql.transactions.transaction
import java.nio.file.Files
import java.nio.file.Path
import java.nio.file.Paths
import java.sql.Connection
import java.time.Duration
import java.time.LocalDateTime
import java.time.temporal.ChronoUnit
import kotlin.io.path.div

object Utils {
    @JvmStatic
    private val LOGGER = KotlinLogging.logger {}
    private val HOME_ROOT: Path by lazy { Paths.get(System.getProperty("user.home")) }
    private val XDG_CACHE: Path by lazy { System.getenv("XDG_CACHE_HOME")?.let(Paths::get) ?: (HOME_ROOT / ".cache") }
    private val XDG_CONFIG: Path by lazy { System.getenv("XDG_CONFIG_HOME")?.let(Paths::get) ?: (HOME_ROOT / ".config") }
    private val XDG_DATA: Path by lazy { System.getenv("XDG_DATA_HOME")?.let(Paths::get) ?: (HOME_ROOT / ".local" / "share") }

    internal val CACHE_ROOT: Path = XDG_CACHE / "freyr"
    internal val CONFIG_ROOT: Path = XDG_CONFIG / "freyr"
    internal val DATA_ROOT: Path = XDG_DATA / "freyr"
    internal const val VERSION = "0.1.0"

    private val DATABASE: Database by lazy {
        val settings = Settings.load()
        Database.connect(
            url = when (settings.database.source) {
                Settings.Database.Source.POSTGRES -> "jdbc:postgres:${settings.database.url}"
                else -> "jdbc:sqlite:${settings.database.url}"
            },
            driver = when (settings.database.source) {
                Settings.Database.Source.POSTGRES -> "org.postgresql.Driver"
                else -> "org.sqlite.JDBC"
            },
            user = settings.database.user ?: "user",
            password = settings.database.password ?: "password",
            databaseConfig = DatabaseConfig {
                @OptIn(ExperimentalKeywordApi::class)
                preserveKeywordCasing = true
            },
        )
    }

    init {
        listOf(CACHE_ROOT, CONFIG_ROOT, DATA_ROOT).forEach {
            if (!Files.exists(it)) it.toFile().mkdirs()
        }
    }

    internal fun KLogger.log(level: Level, message: () -> Any?) {
        when (level) {
            Level.TRACE -> this.trace(message)
            Level.DEBUG -> this.debug(message)
            Level.INFO -> this.info(message)
            Level.WARN -> this.warn(message)
            Level.ERROR -> this.error(message)
            else -> return
        }
    }

    inline fun <reified T : Enum<T>> T.titlecase(): String = this.name.lowercase().split("_").joinToString(" ") {
        it.replaceFirstChar(Char::uppercaseChar)
    }

    internal fun <T> query(block: () -> T): T {
        val startTime = LocalDateTime.now()
        val transaction = transaction(transactionIsolation = Connection.TRANSACTION_SERIALIZABLE, db = DATABASE) {
            addLogger(Slf4jSqlDebugLogger)
            block()
        }
        LOGGER.debug { "Took ${ChronoUnit.MILLIS.between(startTime, LocalDateTime.now())}ms" }
        return transaction
    }

    internal fun toHumanReadable(milliseconds: Float): String {
        val duration = Duration.ofMillis(milliseconds.toLong())
        val minutes = duration.toMinutes()
        val seconds = duration.seconds - minutes * 60
        val millis = duration.toMillis() - (minutes * 60000 + seconds * 1000)
        return when {
            minutes > 0 -> "${minutes}min ${seconds}sec ${millis}ms"
            seconds > 0 -> "${seconds}sec ${millis}ms"
            else -> "${millis}ms"
        }
    }

    fun Instant.toHumanReadable(): String = HumanReadable.timeAgo(this)
}
