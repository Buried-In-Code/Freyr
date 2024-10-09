package github.buriedincode.controllers

import github.buriedincode.Utils
import github.buriedincode.models.Device
import github.buriedincode.models.Reading
import github.buriedincode.models.ReadingTable
import io.github.oshai.kotlinlogging.KotlinLogging
import io.javalin.http.Context
import io.javalin.http.NotFoundResponse
import org.jetbrains.exposed.sql.max

object HtmlController {
    @JvmStatic
    private val LOGGER = KotlinLogging.logger { }

    fun index(ctx: Context) = Utils.query {
        ctx.render("templates/index.kte", mapOf("devices" to Device.all().toList()))
    }

    fun device(ctx: Context) = Utils.query {
        val device = ctx.pathParam("device-id")?.toLongOrNull()?.let(Device::findById) ?: throw NotFoundResponse("Device not found.")
        ctx.render("templates/device.kte", mapOf("device" to device))
    }

    fun deviceReadings(ctx: Context) = Utils.query {
        val latestReadings = ReadingTable
            .select(
                ReadingTable.timestampCol.max(),
                ReadingTable.id,
                ReadingTable.deviceCol,
                ReadingTable.timestampCol,
                ReadingTable.temperatureCol,
                ReadingTable.humidityCol,
            ).groupBy(ReadingTable.deviceCol)
        ctx.render("components/htmx/device-readings.kte", mapOf("readings" to Reading.wrapRows(latestReadings).toList()))
    }
}
