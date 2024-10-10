package github.buriedincode.controllers

import github.buriedincode.Utils
import github.buriedincode.models.Device
import github.buriedincode.models.Reading
import github.buriedincode.models.ReadingTable
import io.github.oshai.kotlinlogging.KotlinLogging
import io.javalin.http.Context
import io.javalin.http.NotFoundResponse
import org.jetbrains.exposed.sql.and
import org.jetbrains.exposed.sql.avg
import org.jetbrains.exposed.sql.kotlin.datetime.month
import org.jetbrains.exposed.sql.kotlin.datetime.year
import org.jetbrains.exposed.sql.max
import org.jetbrains.exposed.sql.min

object HtmlController {
    @JvmStatic
    private val LOGGER = KotlinLogging.logger { }

    fun index(ctx: Context) = Utils.query {
        ctx.render("templates/index.kte", mapOf("devices" to Device.all().toList()))
    }

    private fun loadYearlyReadings(device: Device): Map<String, List<Any?>> {
        val maxTemp = ReadingTable
            .select(ReadingTable.timestampCol.year(), ReadingTable.temperatureCol.max(), ReadingTable.deviceCol)
            .where { ReadingTable.deviceCol eq device.id }
            .groupBy(ReadingTable.timestampCol.year())
            .map { it[ReadingTable.timestampCol.year()] to it[ReadingTable.temperatureCol.max()] }
        val minTemp = ReadingTable
            .select(ReadingTable.timestampCol.year(), ReadingTable.temperatureCol.min(), ReadingTable.deviceCol)
            .where { ReadingTable.deviceCol eq device.id }
            .groupBy(ReadingTable.timestampCol.year())
            .map { it[ReadingTable.timestampCol.year()] to it[ReadingTable.temperatureCol.min()] }
        val avgTemp = ReadingTable
            .select(ReadingTable.timestampCol.year(), ReadingTable.temperatureCol.avg(), ReadingTable.deviceCol)
            .where { ReadingTable.deviceCol eq device.id }
            .groupBy(ReadingTable.timestampCol.year())
            .map { it[ReadingTable.timestampCol.year()] to it[ReadingTable.temperatureCol.avg()] }
        val maxHumid = ReadingTable
            .select(ReadingTable.timestampCol.year(), ReadingTable.humidityCol.max(), ReadingTable.deviceCol)
            .where { ReadingTable.deviceCol eq device.id }
            .groupBy(ReadingTable.timestampCol.year())
            .map { it[ReadingTable.timestampCol.year()] to it[ReadingTable.humidityCol.max()] }
        val minHumid = ReadingTable
            .select(ReadingTable.timestampCol.year(), ReadingTable.humidityCol.min(), ReadingTable.deviceCol)
            .where { ReadingTable.deviceCol eq device.id }
            .groupBy(ReadingTable.timestampCol.year())
            .map { it[ReadingTable.timestampCol.year()] to it[ReadingTable.humidityCol.min()] }
        val avgHumid = ReadingTable
            .select(ReadingTable.timestampCol.year(), ReadingTable.humidityCol.avg(), ReadingTable.deviceCol)
            .where { ReadingTable.deviceCol eq device.id }
            .groupBy(ReadingTable.timestampCol.year())
            .map { it[ReadingTable.timestampCol.year()] to it[ReadingTable.humidityCol.avg()] }
        return mapOf(
            "labels" to maxTemp
                .map { it.first }
                .plus(minTemp.map { it.first })
                .plus(maxHumid.map { it.first })
                .plus(minHumid.map { it.first })
                .distinct(),
            "tempRange" to maxTemp.map { it.second }.zip(minTemp.map { it.second }),
            "tempAvg" to avgTemp.map { it.second },
            "humidRange" to maxHumid.map { it.second }.zip(minHumid.map { it.second }),
            "humidAvg" to avgHumid.map { it.second },
        )
    }

    private fun loadMonthlyReadings(device: Device, year: Int): Map<String, List<Any?>> {
        val maxTemp = ReadingTable
            .select(
                ReadingTable.timestampCol.year(),
                ReadingTable.timestampCol.month(),
                ReadingTable.temperatureCol.max(),
                ReadingTable.deviceCol,
            ).where { (ReadingTable.deviceCol eq device.id) and (ReadingTable.timestampCol.year() eq year) }
            .groupBy(ReadingTable.timestampCol.month())
            .map { it[ReadingTable.timestampCol.month()] to it[ReadingTable.temperatureCol.max()] }
        val minTemp = ReadingTable
            .select(
                ReadingTable.timestampCol.year(),
                ReadingTable.timestampCol.month(),
                ReadingTable.temperatureCol.min(),
                ReadingTable.deviceCol,
            ).where { (ReadingTable.deviceCol eq device.id) and (ReadingTable.timestampCol.year() eq year) }
            .groupBy(ReadingTable.timestampCol.month())
            .map { it[ReadingTable.timestampCol.month()] to it[ReadingTable.temperatureCol.min()] }
        val avgTemp = ReadingTable
            .select(
                ReadingTable.timestampCol.year(),
                ReadingTable.timestampCol.month(),
                ReadingTable.temperatureCol.avg(),
                ReadingTable.deviceCol,
            ).where { (ReadingTable.deviceCol eq device.id) and (ReadingTable.timestampCol.year() eq year) }
            .groupBy(ReadingTable.timestampCol.month())
            .map { it[ReadingTable.timestampCol.month()] to it[ReadingTable.temperatureCol.avg()] }
        val maxHumid = ReadingTable
            .select(
                ReadingTable.timestampCol.year(),
                ReadingTable.timestampCol.month(),
                ReadingTable.humidityCol.max(),
                ReadingTable.deviceCol,
            ).where { (ReadingTable.deviceCol eq device.id) and (ReadingTable.timestampCol.year() eq year) }
            .groupBy(ReadingTable.timestampCol.month())
            .map { it[ReadingTable.timestampCol.month()] to it[ReadingTable.humidityCol.max()] }
        val minHumid = ReadingTable
            .select(
                ReadingTable.timestampCol.year(),
                ReadingTable.timestampCol.month(),
                ReadingTable.humidityCol.min(),
                ReadingTable.deviceCol,
            ).where { (ReadingTable.deviceCol eq device.id) and (ReadingTable.timestampCol.year() eq year) }
            .groupBy(ReadingTable.timestampCol.month())
            .map { it[ReadingTable.timestampCol.month()] to it[ReadingTable.humidityCol.min()] }
        val avgHumid = ReadingTable
            .select(
                ReadingTable.timestampCol.year(),
                ReadingTable.timestampCol.month(),
                ReadingTable.humidityCol.avg(),
                ReadingTable.deviceCol,
            ).where { (ReadingTable.deviceCol eq device.id) and (ReadingTable.timestampCol.year() eq year) }
            .groupBy(ReadingTable.timestampCol.month())
            .map { it[ReadingTable.timestampCol.month()] to it[ReadingTable.humidityCol.avg()] }
        return mapOf(
            "labels" to maxTemp
                .map { it.first }
                .plus(minTemp.map { it.first })
                .plus(maxHumid.map { it.first })
                .plus(minHumid.map { it.first })
                .distinct(),
            "tempRange" to maxTemp.map { it.second }.zip(minTemp.map { it.second }),
            "tempAvg" to avgTemp.map { it.second },
            "humidRange" to maxHumid.map { it.second }.zip(minHumid.map { it.second }),
            "humidAvg" to avgHumid.map { it.second },
        )
    }

    fun device(ctx: Context) = Utils.query {
        val device = ctx.pathParam("device-id").toLongOrNull()?.let(Device::findById) ?: throw NotFoundResponse("Device not found.")
        val output = mutableMapOf<String, Any>("device" to device, "selected" to mapOf("year" to ctx.queryParam("year")?.toIntOrNull()))

        output.put("yearly", loadYearlyReadings(device = device))
        ctx.queryParam("year")?.toIntOrNull()?.let {
            output.put("monthly", loadMonthlyReadings(device = device, year = it))
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
