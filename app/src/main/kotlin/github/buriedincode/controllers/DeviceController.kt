package github.buriedincode.controllers

import github.buriedincode.Utils
import github.buriedincode.models.Device
import github.buriedincode.models.DeviceInput
import io.github.oshai.kotlinlogging.KotlinLogging
import io.javalin.http.ConflictResponse
import io.javalin.http.Context

object DeviceController : BaseController<Device>(entity = Device, plural = "devices") {
    @JvmStatic
    private val LOGGER = KotlinLogging.logger { }

    override fun filterResources(ctx: Context): List<Device> {
        var devices = entity.all().toList()
        ctx.queryParam("name")?.let { name ->
            devices = devices.filter { it.name == name }
        }
        return devices
    }

    override fun create(ctx: Context) = ctx.processInput<DeviceInput> { body ->
        Utils.query {
            Device.findOrNull(name = body.name)?.let {
                throw ConflictResponse("Device already exists")
            }
            val device = entity.new {
                name = body.name
            }
            ctx.json(device.toJson(showAll = true))
        }
    }
}
