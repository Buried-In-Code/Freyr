package github.buriedincode.controllers

import github.buriedincode.Utils
import github.buriedincode.models.Device
import github.buriedincode.models.Reading
import github.buriedincode.models.ReadingInput
import io.github.oshai.kotlinlogging.KotlinLogging
import io.javalin.http.BadRequestResponse
import io.javalin.http.ConflictResponse
import io.javalin.http.Context
import io.javalin.http.HttpStatus
import io.javalin.http.NotFoundResponse
import kotlinx.datetime.Clock
import kotlinx.datetime.Instant
import kotlinx.datetime.LocalDate
import kotlinx.datetime.LocalDateTime
import kotlinx.datetime.TimeZone
import kotlinx.datetime.atStartOfDayIn
import kotlinx.datetime.toInstant

object ReadingController : BaseController<Reading>(entity = Reading, plural = "readings") {
    @JvmStatic
    private val LOGGER = KotlinLogging.logger { }

    private fun Context.getDevice(): Device = this.pathParam(DeviceController.paramName).toLongOrNull()?.let {
        Device.findById(id = it) ?: throw NotFoundResponse("${DeviceController.title} not found.")
    } ?: throw BadRequestResponse("Invalid ${DeviceController.paramName}")

    override fun filterResources(ctx: Context): List<Reading> {
        var readings = ctx.getDevice().readings.toList()
        try {
            ctx.queryParam("before")?.let(Instant::parse)?.let { timestamp ->
                readings = readings.filter { it.timestamp < timestamp }
            }
        } catch (iae: IllegalArgumentException) {
            try {
                ctx.queryParam("before")?.let(LocalDateTime::parse)?.let { timestamp ->
                    readings = readings.filter { it.timestamp < timestamp.toInstant(TimeZone.currentSystemDefault()) }
                }
            } catch (_: IllegalArgumentException) {
                try {
                    ctx.queryParam("before")?.let(LocalDate::parse)?.let { timestamp ->
                        readings = readings.filter { it.timestamp < timestamp.atStartOfDayIn(TimeZone.currentSystemDefault()) }
                    }
                } catch (_: IllegalArgumentException) {
                    throw BadRequestResponse(iae.localizedMessage)
                }
            }
        }
        try {
            ctx.queryParam("after")?.let(Instant::parse)?.let { timestamp ->
                readings = readings.filter { it.timestamp > timestamp }
            }
        } catch (iae: IllegalArgumentException) {
            try {
                ctx.queryParam("after")?.let(LocalDateTime::parse)?.let { timestamp ->
                    readings = readings.filter { it.timestamp > timestamp.toInstant(TimeZone.currentSystemDefault()) }
                }
            } catch (_: IllegalArgumentException) {
                try {
                    ctx.queryParam("after")?.let(LocalDate::parse)?.let { timestamp ->
                        readings = readings.filter { it.timestamp > timestamp.atStartOfDayIn(TimeZone.currentSystemDefault()) }
                    }
                } catch (_: IllegalArgumentException) {
                    throw BadRequestResponse(iae.localizedMessage)
                }
            }
        }
        return readings
    }

    override fun create(ctx: Context) = ctx.processInput<ReadingInput> { body ->
        Utils.query {
            val device = ctx.getDevice()
            val timestamp = Clock.System.now()
            Reading.findOrNull(device = device, timestamp = timestamp)?.let {
                throw ConflictResponse("Reading already exists")
            }
            val reading = entity.new {
                this.device = device
                this.timestamp = timestamp
                humidity = body.humidity
                temperature = body.temperature
            }
            ctx.json(reading.toJson(showAll = true))
        }
    }

    override fun read(ctx: Context): Unit = Utils.query {
        val device = ctx.getDevice()
        val resource = ctx.getResource()
        if (device != resource.device) {
            throw NotFoundResponse("$title not found.")
        }
        ctx.json(resource.toJson(showAll = true))
    }

    override fun delete(ctx: Context): Unit = Utils.query {
        val device = ctx.getDevice()
        val resource = ctx.getResource()
        if (device != resource.device) {
            throw NotFoundResponse("$title not found.")
        }
        resource.delete()
        ctx.status(HttpStatus.NO_CONTENT)
    }
}
