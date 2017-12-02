async def soft_delete(ctx):
    try:
        await ctx.message.delete()
    except:
        pass
