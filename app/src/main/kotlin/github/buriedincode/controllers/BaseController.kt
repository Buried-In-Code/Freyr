package github.buriedincode.controllers

import github.buriedincode.Utils
import github.buriedincode.models.IJson
import io.javalin.http.BadRequestResponse
import io.javalin.http.Context
import io.javalin.http.HttpStatus
import io.javalin.http.NotFoundResponse
import io.javalin.http.bodyAsClass
import org.jetbrains.exposed.dao.LongEntity
import org.jetbrains.exposed.dao.LongEntityClass

abstract class BaseController<T>(protected val entity: LongEntityClass<T>, protected val plural: String) where T : LongEntity, T : IJson {
    internal val name: String = entity::class.java.declaringClass.simpleName.lowercase()
    internal val paramName: String = "$name-id"
    internal val title: String = name.replaceFirstChar(Char::uppercaseChar)

    protected fun Context.getResource(): T = this.pathParam(paramName).toLongOrNull()?.let {
        entity.findById(id = it) ?: throw NotFoundResponse("$title not found.")
    } ?: throw BadRequestResponse("Invalid $paramName")

    protected open fun filterResources(ctx: Context): List<T> = entity.all().toList()

    protected inline fun <reified I> Context.processInput(crossinline block: (I) -> Unit) = block(bodyAsClass(I::class.java))

    open fun list(ctx: Context): Unit = Utils.query {
        ctx.json(filterResources(ctx = ctx).map { it.toJson() })
    }

    abstract fun create(ctx: Context)

    open fun read(ctx: Context): Unit = Utils.query {
        ctx.json(ctx.getResource().toJson(showAll = true))
    }

    open fun delete(ctx: Context): Unit = Utils.query {
        ctx.getResource().delete()
        ctx.status(HttpStatus.NO_CONTENT)
    }
}
