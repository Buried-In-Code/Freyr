package github.buriedincode.controllers

import github.buriedincode.Utils
import github.buriedincode.Utils.titlecase
import github.buriedincode.models.Device
import github.buriedincode.models.Reading
import github.buriedincode.models.ReadingTable
import io.github.oshai.kotlinlogging.KotlinLogging
import io.javalin.http.Context
import io.javalin.http.NotFoundResponse
import kotlinx.datetime.Month
import kotlinx.datetime.number
import org.jetbrains.exposed.sql.and
import org.jetbrains.exposed.sql.avg
import org.jetbrains.exposed.sql.kotlin.datetime.day
import org.jetbrains.exposed.sql.kotlin.datetime.hour
import org.jetbrains.exposed.sql.kotlin.datetime.month
import org.jetbrains.exposed.sql.kotlin.datetime.year
import org.jetbrains.exposed.sql.max
import org.jetbrains.exposed.sql.min
import org.jetbrains.exposed.sql.stringLiteral

object HtmlController {
    @JvmStatic
    private val LOGGER = KotlinLogging.logger { }

    fun index(ctx: Context) = Utils.query {
        ctx.render("templates/index.kte", mapOf("devices" to Device.all().toList()))
    }

    private fun loadYearlyReadings(device: Device): Map<String, List<Any?>> {
        val query = ReadingTable
            .select(
                ReadingTable.deviceCol,
                ReadingTable.timestampCol.year(),
                ReadingTable.temperatureCol.max(),
                ReadingTable.temperatureCol.min(),
                ReadingTable.temperatureCol.avg(),
                ReadingTable.humidityCol.max(),
                ReadingTable.humidityCol.min(),
                ReadingTable.humidityCol.avg(),
            ).where { ReadingTable.deviceCol eq device.id }
            .groupBy(ReadingTable.timestampCol.year())

        return mapOf(
            "labels" to query.map { it[ReadingTable.timestampCol.year()] }.distinct(),
            "tempRange" to query.map { it[ReadingTable.temperatureCol.max()] to it[ReadingTable.temperatureCol.min()] },
            "tempAvg" to query.map { it[ReadingTable.temperatureCol.avg()] },
            "humidRange" to query.map { it[ReadingTable.humidityCol.max()] to it[ReadingTable.humidityCol.min()] },
            "humidAvg" to query.map { it[ReadingTable.humidityCol.avg()] },
        )
    }

    private fun loadMonthlyReadings(device: Device, year: Int): Map<String, List<Any?>> {
        val query = ReadingTable
            .select(
                ReadingTable.deviceCol,
                ReadingTable.timestampCol.year(),
                ReadingTable.timestampCol.month(),
                ReadingTable.temperatureCol.max(),
                ReadingTable.temperatureCol.min(),
                ReadingTable.temperatureCol.avg(),
                ReadingTable.humidityCol.max(),
                ReadingTable.humidityCol.min(),
                ReadingTable.humidityCol.avg(),
            ).where { (ReadingTable.deviceCol eq device.id) and (ReadingTable.timestampCol.year() eq stringLiteral(year.toString())) }
            .groupBy(ReadingTable.timestampCol.month())

        return mapOf(
            "labels" to query
                .map { it[ReadingTable.timestampCol.month()] }
                .map {
                    Month.values()[it - 1].titlecase()
                }.distinct(),
            "tempRange" to query.map { it[ReadingTable.temperatureCol.max()] to it[ReadingTable.temperatureCol.min()] },
            "tempAvg" to query.map { it[ReadingTable.temperatureCol.avg()] },
            "humidRange" to query.map { it[ReadingTable.humidityCol.max()] to it[ReadingTable.humidityCol.min()] },
            "humidAvg" to query.map { it[ReadingTable.humidityCol.avg()] },
        )
    }

    private fun loadDailyReadings(device: Device, year: Int, month: Int): Map<String, List<Any?>> {
        val query = ReadingTable
            .select(
                ReadingTable.deviceCol,
                ReadingTable.timestampCol.year(),
                ReadingTable.timestampCol.month(),
                ReadingTable.timestampCol.day(),
                ReadingTable.temperatureCol.max(),
                ReadingTable.temperatureCol.min(),
                ReadingTable.temperatureCol.avg(),
                ReadingTable.humidityCol.max(),
                ReadingTable.humidityCol.min(),
                ReadingTable.humidityCol.avg(),
            ).where {
                (ReadingTable.deviceCol eq device.id) and (ReadingTable.timestampCol.year() eq stringLiteral(year.toString())) and
                    (ReadingTable.timestampCol.month() eq stringLiteral(month.toString().padStart(2, '0')))
            }.groupBy(ReadingTable.timestampCol.day())

        return mapOf(
            "labels" to query.map { it[ReadingTable.timestampCol.day()] }.distinct(),
            "tempRange" to query.map { it[ReadingTable.temperatureCol.max()] to it[ReadingTable.temperatureCol.min()] },
            "tempAvg" to query.map { it[ReadingTable.temperatureCol.avg()] },
            "humidRange" to query.map { it[ReadingTable.humidityCol.max()] to it[ReadingTable.humidityCol.min()] },
            "humidAvg" to query.map { it[ReadingTable.humidityCol.avg()] },
        )
    }

    private fun loadHourlyReadings(device: Device, year: Int, month: Int, day: Int): Map<String, List<Any?>> {
        val query = ReadingTable
            .select(
                ReadingTable.deviceCol,
                ReadingTable.timestampCol.year(),
                ReadingTable.timestampCol.month(),
                ReadingTable.timestampCol.day(),
                ReadingTable.timestampCol.hour(),
                ReadingTable.temperatureCol.max(),
                ReadingTable.temperatureCol.min(),
                ReadingTable.temperatureCol.avg(),
                ReadingTable.humidityCol.max(),
                ReadingTable.humidityCol.min(),
                ReadingTable.humidityCol.avg(),
            ).where {
                (ReadingTable.deviceCol eq device.id) and (ReadingTable.timestampCol.year() eq stringLiteral(year.toString())) and
                    (ReadingTable.timestampCol.month() eq stringLiteral(month.toString().padStart(2, '0'))) and
                    (ReadingTable.timestampCol.day() eq stringLiteral(day.toString().padStart(2, '0')))
            }.groupBy(ReadingTable.timestampCol.hour())

        return mapOf(
            "labels" to query.map { it[ReadingTable.timestampCol.hour()] }.distinct(),
            "tempRange" to query.map { it[ReadingTable.temperatureCol.max()] to it[ReadingTable.temperatureCol.min()] },
            "tempAvg" to query.map { it[ReadingTable.temperatureCol.avg()] },
            "humidRange" to query.map { it[ReadingTable.humidityCol.max()] to it[ReadingTable.humidityCol.min()] },
            "humidAvg" to query.map { it[ReadingTable.humidityCol.avg()] },
        )
    }

    fun String.toMonthIntOrNull(): Int? {
        return try {
            Month.valueOf(this.uppercase()).number
        } catch (iae: IllegalArgumentException) {
            null
        }
    }

    fun device(ctx: Context) = Utils.query {
        val device = ctx.pathParam("device-id").toLongOrNull()?.let(Device::findById) ?: throw NotFoundResponse("Device not found.")
        val output = mutableMapOf<String, Any>(
            "device" to device,
            "selected" to mapOf("year" to ctx.queryParam("year")?.toIntOrNull(), "month" to ctx.queryParam("month"), "day" to ctx.queryParam("day")?.toIntOrNull()),
        )

        output.put("yearly", loadYearlyReadings(device = device))
        ctx.queryParam("year")?.toIntOrNull()?.let { year ->
            output.put("monthly", loadMonthlyReadings(device = device, year = year))
            ctx.queryParam("month")?.toMonthIntOrNull()?.let { month ->
                output.put("daily", loadDailyReadings(device = device, year = year, month = month))
                ctx.queryParam("day")?.toIntOrNull()?.let { day ->
                    output.put("hourly", loadHourlyReadings(device = device, year = year, month = month, day = day))
                }
            }
        }

        ctx.render("templates/device.kte", output)
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
