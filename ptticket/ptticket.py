from redbot.core import commands, checks
from redbot.core.utils.predicates import MessagePredicate, ReactionPredicate
from redbot.core.utils.menus import start_adding_reactions
from phabricator import Phabricator

class PTTicket(commands.Cog):
    """My custom cog"""

    @commands.group(pass_context=True, invoke_without_command=True, no_pm=True)
    @checks.mod_or_permissions(manage_messages=True)
    async def ticket(self, ctx):
        """Starts a ticket creation workflow."""

        await ctx.send("What is the title of your problema? {.author.mention}".format(ctx))
        title = await ctx.bot.wait_for("message", check=MessagePredicate.same_context(user=ctx.author))

        await ctx.send("What is the description of your problema? {.author.mention}".format(ctx))
        description = await ctx.bot.wait_for("message", check=MessagePredicate.same_context(user=ctx.author))

        msg = await ctx.send("""**Title: ** %s
**Description:** %s
**Severity:** Normal [Posttwo]

    Should I send this?
        """ % (title.content, description.content))

        start_adding_reactions(msg, ReactionPredicate.YES_OR_NO_EMOJIS)

        pred = ReactionPredicate.yes_or_no(msg, ctx.author)
        await ctx.bot.wait_for("reaction_add", check=pred)
        if pred.result is True:
            await self.create_ticket(ctx, title.content, description.content)
            await ctx.send("Sent")
        else:
            await ctx.send("Ticket creation cancelled")

    @ticket.command(pass_context=True, name='escalate')
    @checks.mod_or_permissions(manage_messages=True)
    async def ticket_escalate(self, ctx, ticket_id):
        """Wakes posttwo up, you better know what youre doing"""
        auth_token = await ctx.bot.get_shared_api_tokens("phabricator")
        auth_token = auth_token['FJBot']
        phab = Phabricator(host='https://p.mongla.net/api/', token=auth_token)

        ticket = phab.maniphest.search(
            constraints={
                "ids": [
                    int(ticket_id)
                ]
            },
            attachments={"projects": True}
        )

        projects = ticket.data[0]['attachments']['projects']['projectPHIDs']

        if 'PHID-PROJ-y23i6ly7jw6f3llup4m5' in projects:
            tt = ticket.data[0]['fields']
            print(tt)
            msg = await ctx.send("""Are you sure you want to escalate the following ticket and wake up posttwo?:
**Title:** %s
            """ % (tt['name']))

            start_adding_reactions(msg, ReactionPredicate.YES_OR_NO_EMOJIS)
            pred = ReactionPredicate.yes_or_no(msg, ctx.author)
            await ctx.bot.wait_for("reaction_add", check=pred)
            if pred.result is True:
                await self.escalate_ticket(ctx, ticket_id)
                await ctx.send("Escalated, you better know what youre doing.")
            else:
                await ctx.send("Ticket escalation cancelled")
        else:
            await ctx.send("Sorry that ticket is not part of the #FunnyJunk project. {.author.mention}".format(ctx))


    async def escalate_ticket(self, ctx, ticket_id):
        auth_token = await ctx.bot.get_shared_api_tokens("phabricator")
        auth_token = auth_token['FJBot']
        phab = Phabricator(host='https://p.mongla.net/api/', token=auth_token)
        phab.maniphest.edit(objectIdentifier=ticket_id, transactions=[
            {
                "type": "comment",
                "value": "Escalation thanks to %s with ID `%s`" % (ctx.author, ctx.author.id)
            },
            {
                "type": "priority",
                "value": "unbreak"
            }
        ])

    async def create_ticket(self, ctx, title, description):
        auth_token = await ctx.bot.get_shared_api_tokens("phabricator")
        auth_token = auth_token['FJBot']
        phab = Phabricator(host='https://p.mongla.net/api/', token=auth_token)
        x = phab.maniphest.edit(transactions=[
            {
                "type": "title",
                "value": title

            },
            {
                "type": "description",
                "value": description
            },
            {
                "type": "projects.add",
                "value": ['PHID-PROJ-y23i6ly7jw6f3llup4m5']
            },
            {
                "type": "priority",
                "value": "triage"
            }
        ])
        await ctx.send("Opened ticket with ID: **%s**" % x.object['id'])
