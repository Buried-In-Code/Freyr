package github.buriedincode

import gg.jte.TemplateEngine
import gg.jte.resolve.DirectoryCodeResolver
import github.buriedincode.Utils.log
import github.buriedincode.controllers.DeviceController
import github.buriedincode.controllers.HtmlController
import github.buriedincode.controllers.ReadingController
import io.github.oshai.kotlinlogging.KotlinLogging
import io.github.oshai.kotlinlogging.Level
import io.javalin.Javalin
import io.javalin.apibuilder.ApiBuilder.delete
import io.javalin.apibuilder.ApiBuilder.get
import io.javalin.apibuilder.ApiBuilder.path
import io.javalin.apibuilder.ApiBuilder.post
import io.javalin.http.ContentType
import io.javalin.rendering.FileRenderer
import io.javalin.rendering.template.JavalinJte
import java.nio.file.Path
import java.util.TimeZone
import kotlin.io.path.div
import gg.jte.ContentType as JteType

object Freyr {
    @JvmStatic
    private val LOGGER = KotlinLogging.logger { }

    private fun createTemplateEngine(environment: Settings.Environment): TemplateEngine {
        return if (environment == Settings.Environment.DEV) {
            val codeResolver = DirectoryCodeResolver(Path.of("src") / "main" / "jte")
            TemplateEngine.create(codeResolver, JteType.Html)
        } else {
            TemplateEngine.createPrecompiled(Path.of("jte-classes"), JteType.Html)
        }
    }

    private fun createJavalinApp(renderer: FileRenderer): Javalin {
        return Javalin.create {
            it.fileRenderer(renderer)
            it.http.prefer405over404 = true
            it.http.defaultContentType = ContentType.JSON
            it.requestLogger.http { ctx, ms ->
                val level = when {
                    ctx.statusCode() in (100..<200) -> Level.WARN
                    ctx.statusCode() in (200..<300) -> Level.INFO
                    ctx.statusCode() in (300..<400) -> Level.INFO
                    ctx.statusCode() in (400..<500) -> Level.WARN
                    else -> Level.ERROR
                }
                LOGGER.log(level) { "${ctx.statusCode()}: ${ctx.method()} - ${ctx.path()} => ${Utils.toHumanReadable(ms)}" }
            }
            it.router.ignoreTrailingSlashes = true
            it.router.treatMultipleSlashesAsSingleSlash = true
            it.router.caseInsensitiveRoutes = true
            it.router.apiBuilder {
                path("/") {
                    get(HtmlController::index)
                    get("{device-id}", HtmlController::device)
                }
                path("/components") {
                    get("device-readings", HtmlController::deviceReadings)
                }
                path("/api") {
                    path("devices") {
                        get(DeviceController::list)
                        post(DeviceController::create)
                        path("{device-id}") {
                            get(DeviceController::read)
                            delete(DeviceController::delete)
                            path("readings") {
                                get(ReadingController::list)
                                post(ReadingController::create)
                                path("{reading-id}") {
                                    get(ReadingController::read)
                                    delete(ReadingController::delete)
                                }
                            }
                        }
                    }
                }
            }
            it.staticFiles.add {
                it.hostedPath = "/static"
                it.directory = "/static"
            }
        }
    }

    fun start(settings: Settings) {
        val engine = createTemplateEngine(settings.environment)
        engine.setTrimControlStructures(true)
        val renderer = JavalinJte(engine)

        val app = createJavalinApp(renderer)
        app.start(settings.website.host, settings.website.port)
    }
}

fun main(
    @Suppress("UNUSED_PARAMETER") vararg args: String,
) {
    println(TimeZone.getDefault())
    TimeZone.setDefault(TimeZone.getTimeZone("Pacific/Auckland"))
    println(TimeZone.getDefault())
    println("Freyr v${Utils.VERSION}")
    println("Kotlin v${KotlinVersion.CURRENT}")
    println("Java v${System.getProperty("java.version")}")
    println("Arch: ${System.getProperty("os.arch")}")

    val settings = Settings.load()
    println(settings)

    Freyr.start(settings = settings)
}
