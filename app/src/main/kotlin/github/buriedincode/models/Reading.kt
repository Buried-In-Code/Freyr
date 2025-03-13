package github.buriedincode.models

import github.buriedincode.Utils
import kotlinx.datetime.Clock
import kotlinx.datetime.Instant
import org.jetbrains.exposed.dao.LongEntity
import org.jetbrains.exposed.dao.LongEntityClass
import org.jetbrains.exposed.dao.id.EntityID
import org.jetbrains.exposed.dao.id.LongIdTable
import org.jetbrains.exposed.sql.Column
import org.jetbrains.exposed.sql.ReferenceOption
import org.jetbrains.exposed.sql.SchemaUtils
import org.jetbrains.exposed.sql.and
import org.jetbrains.exposed.sql.kotlin.datetime.timestamp

class Reading(id: EntityID<Long>) : LongEntity(id), IJson, Comparable<Reading> {
    companion object : LongEntityClass<Reading>(ReadingTable) {
        val comparator = compareBy(Reading::device).thenBy(Reading::timestamp)

        fun findOrNull(device: Device, timestamp: Instant): Reading? {
            return find { (ReadingTable.deviceCol eq device.id) and (ReadingTable.timestampCol eq timestamp) }.firstOrNull()
        }
    }

    var device by Device referencedOn ReadingTable.deviceCol
    var timestamp: Instant by ReadingTable.timestampCol
    var humidity: Double? by ReadingTable.humidityCol
    var temperature: Double? by ReadingTable.temperatureCol

    override fun toJson(showAll: Boolean): Map<String, Any?> {
        return mutableMapOf<String, Any?>(
            "id" to id.value,
            "timestamp" to timestamp.toString(),
            "humidity" to humidity,
            "temperature" to temperature,
        ).apply {
            if (showAll) {
                put("device", device.toJson(showAll = false))
            } else {
                put("deviceId", device.id.value)
            }
        }.toSortedMap()
    }

    override fun compareTo(other: Reading): Int = comparator.compare(this, other)

    override fun toString(): String {
        return "Reading(id=${id.value}, device=$device, timestamp=$timestamp, temperature=$temperature, humidity=$humidity)"
    }
}

object ReadingTable : LongIdTable(name = "readings") {
    val deviceCol: Column<EntityID<Long>> = reference(
        name = "device_id",
        foreign = DeviceTable,
        onDelete = ReferenceOption.CASCADE,
        onUpdate = ReferenceOption.CASCADE,
    )
    val timestampCol: Column<Instant> = timestamp(name = "timestamp").clientDefault { Clock.System.now() }
    val humidityCol: Column<Double?> = double(name = "humidity").nullable()
    val temperatureCol: Column<Double?> = double(name = "temperature").nullable()

    init {
        Utils.query {
            uniqueIndex(deviceCol, timestampCol)
            SchemaUtils.create(this)
        }
    }
}

data class ReadingInput(
    val humidity: Double? = null,
    val temperature: Double? = null,
    val timestamp: String? = null,
)
