package github.buriedincode.models

import github.buriedincode.Utils
import org.jetbrains.exposed.dao.LongEntity
import org.jetbrains.exposed.dao.LongEntityClass
import org.jetbrains.exposed.dao.id.EntityID
import org.jetbrains.exposed.dao.id.LongIdTable
import org.jetbrains.exposed.sql.Column
import org.jetbrains.exposed.sql.SchemaUtils

class Device(id: EntityID<Long>) : LongEntity(id), IJson, Comparable<Device> {
    companion object : LongEntityClass<Device>(DeviceTable) {
        val comparator = compareBy(Device::name)

        fun findOrNull(name: String): Device? {
            return find { DeviceTable.nameCol eq name }.firstOrNull()
        }
    }

    var name: String by DeviceTable.nameCol

    val readings by Reading referrersOn ReadingTable.deviceCol

    override fun toJson(showAll: Boolean): Map<String, Any?> {
        return mutableMapOf<String, Any?>(
            "id" to id.value,
            "name" to name,
        ).apply {
            if (showAll) {
                put("readings", readings.sorted().map { it.toJson() })
            }
        }.toSortedMap()
    }

    override fun compareTo(other: Device): Int = comparator.compare(this, other)
}

object DeviceTable : LongIdTable(name = "devices") {
    val nameCol: Column<String> = text(name = "name").uniqueIndex()

    init {
        Utils.query {
            SchemaUtils.create(this)
        }
    }
}

data class DeviceInput(
    val name: String,
)
